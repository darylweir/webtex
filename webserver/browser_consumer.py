import simplejson, boto, uuid
import os, thread, time

##
## Functions to retrieve and save updated pdfs from Amazon s3.
##

message_queue_name_request = 'webtex-tex-test-requests'
message_queue_name_replies = 'webtex-tex-test-replies'

message_bucket_name = 'webtext.text.com'


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
  print 'message is ', message.get_body()
  msg_data = simplejson.loads(message.get_body())
  key = boto.connect_s3().get_bucket(msg_data['bucket']).get_key(msg_data['key'])
  if key is not None:
	  print 'key is ', key.get_contents_as_string()
	  data = simplejson.loads(key.get_contents_as_string())
	  q.delete_message(message)
	  return data
  else:
	return None

# Store update/done messages into the message queue
def store_message(message_queue_name, message_bucket_name, message_bucket_key, message_structure):
  # sqs messages are contrained to 8kb/message. Store message data in a bucket on s3 - might be overkill!
  sqs = boto.connect_sqs()
  #this will return a new queue if one does not exist, or the existing queue
  #q = sqs.create_queue(message_queue_name) # Message queue points to message data.
  q = sqs.get_queue(message_queue_name)
  data = simplejson.dumps(message_structure)
  s3 = boto.connect_s3()
  bucket = s3.get_bucket(message_bucket_name)
  key = bucket.new_key((message_bucket_key + '/%s.json') % str(uuid.uuid4()))
  key.set_contents_from_string(data)
  message = q.new_message(body=simplejson.dumps({'bucket': bucket.name, 'key': key.name}))
  q.write(message)

##
## S3 File Storage Functions
##

def retrieve_file(bucket_name, file_key, file_name):
  s3 = boto.connect_s3()
  key = s3.get_bucket(bucket_name).get_key(file_key)
  key.get_contents_to_filename(file_name)

# Parse request
def do_some_work(data, file_name):
  print 'working on data... ', data
  if data['request'] == 'done':
    print 'performing update...'
    print data
    bucket_name = 'test_bucket.webtex.com'
    file_path = 'LATEX0/'
    file_name = 'temp.zip'
    #retrieve_file(data['bucket_name'], data['file_path'] + data['file_name'], file)
    retrieve_file(bucket_name, file_path + file_name, file_name)
    print 'file should have been retrieved, yaldi'
    return True
  
  print 'request != update'
  return False

def main(file_name):
  data = read_message(message_queue_name_replies)
  if data is not None:
    print 'got data ', data
    #thread.start_new_thread(do_some_work, (data, ))
    return do_some_work(data, file_name)

  print 'naw'
  return False


# Main daemon 
#if __name__ == '__main__':
#  main()
