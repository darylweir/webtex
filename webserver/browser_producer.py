import simplejson, boto, uuid
import os, thread, time

##
## Functions to store and read messages with Amazon sqs.
##

message_queue_name_request = 'webtex-tex-test-requests'
message_queue_name_replies = 'webtex-tex-test-replies'

message_bucket_name = 'webtext.text.com'

do_update_message = {
    "request": "update",
    "file_path": "",
    "file_name": "",
    "bucket_name": "",
}

done_update_message = {
    "request": "done",
}

log_id = 'webtex-sqs >> '

##
## SQS Message Queue Functions
##

def create_queue(message_queue_name, timeout_sec):
  sqs = boto.connect_sqs()
  q = sqs.create_queue(message_queue_name, timeout_sec)

def create_bucket(bucket_name):
  s3 = boto.connect_s3()
  bucket = s3.create_bucket(bucket_name)  # bucket names must be unique

# Blocking read of messages in message queue
def read_message(message_queue_name):
  print log_id , 'reading message'
  sqs = boto.connect_sqs()
  q = sqs.get_queue(message_queue_name)
  message = q.read()
  while message is None:   # if it is, continue reading until you get a message
    message = q.read()
  msg_data = simplejson.loads(message.get_body())
  key = boto.connect_s3().get_bucket(msg_data['bucket']).get_key(msg_data['key'])
  data = simplejson.loads(key.get_contents_as_string())
  q.delete_message(message)
  return data

# Store update/done messages into the message queue
def store_message(message_queue_name, message_bucket_name, message_bucket_key, message_structure):
  # sqs messages are contrained to 8kb/message. Store message data in a bucket on s3 - might be overkill!
  sqs = boto.connect_sqs()
  #this will return a new queue if one does not exist, or the existing queue
  q = sqs.create_queue(message_queue_name) # Message queue points to message data.
  data = simplejson.dumps(message_structure)
  s3 = boto.connect_s3()
  bucket = s3.get_bucket(message_bucket_name)
  key = bucket.new_key((message_bucket_key + '/%s.json') % str(uuid.uuid4()))
  key.set_contents_from_string(data)
  print data
  #key.set_contents_from_filename(data['file_name'])
  message = q.new_message(body=simplejson.dumps({'bucket': bucket.name, 'key': key.name}))
  q.write(message)

##
## S9 File Storage Functions
##

def store_file(bucket_name, file_key, file_content):
  s3 = boto.connect_s3()
  bucket = s3.create_bucket(bucket_name)  # bucket names must be unique
  key = bucket.new_key(file_key)
  key.set_contents_from_filename(file_content)
  key.set_acl('public-read')

def main(local_file):
  create_queue(message_queue_name_request, 120)
  create_bucket(message_bucket_name)
  local_file.writetofile('temp.zip')
  count=0
  print 'queues are created'
  # TODO Update on server to update zip file to be processed periodically
  do_update_message['file_path'] = 'LATEX%i/' % (count)
  count += 1
  do_update_message['file_name'] = 'temp.zip'
  do_update_message['bucket_name'] = 'test_bucket.webtex.com'
  print 'Updating ' + do_update_message['file_path'] + do_update_message['file_name']
  store_file(do_update_message['bucket_name'], do_update_message['file_path'] + do_update_message['file_name'], '/home/hacker-6-06/webtex/webserver/temp.zip')
  store_message(message_queue_name_request, message_bucket_name, 'text_key', do_update_message)
  print 'file stored, message update in queue'
#  os.remove('temp.zip')



# Main daemon 
#if __name__ == '__main__':
#  main()
#  time.sleep(10) # Timeout in sec
