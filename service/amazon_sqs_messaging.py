import simplejson, boto, uuid

##
## Functions to store and read messages with Amazon sqs.
##

message_queue_name = 'webtex-tex-test'
message_bucket_name = 'webtext.text.com'

message_structure = {
    "request": "update",
}

log_id = 'webtex-sqs >> '

def create_queue(message_queue_name, timeout_sec):
  sqs = boto.connect_sqs()
  q = sqs.create_queue(message_queue_name, timeout_sec)

def create_bucket(bucket_name):
  s3 = boto.connect_s3()
  bucket = s3.create_bucket(bucket_name)  # bucket names must be unique
  
def store_message(message_queue_name, message_bucket_name, message_bucket_key):
  # sqs messages are contrained to 8kb/message. Store message data in a bucket on s3 - might be overkill!
  sqs = boto.connect_sqs()
  q = sqs.create_queue(message_queue_name) # Message queue points to message data.
  data = simplejson.dumps(message_structure)
  s3 = boto.connect_s3()
  bucket = s3.get_bucket(message_bucket_name)
  key = bucket.new_key((message_bucket_key + '/%s.json') % str(uuid.uuid4()))
  key.set_contents_from_string(data)
  message = q.new_message(body=simplejson.dumps({'bucket': bucket.name, 'key': key.name}))
  q.write(message)

def read_message(message_queue_name):
  print log_id , 'reading message'
  sqs = boto.connect_sqs()
  q = sqs.get_queue(message_queue_name)
  message = q.read()
  if message is not None:   # if it is continue reading until you get a message
    msg_data = simplejson.loads(message.get_body())
    key = boto.connect_s3().get_bucket(msg_data['bucket']).get_key(msg_data['key'])
    data = simplejson.loads(key.get_contents_as_string())
    do_some_work(data)
    q.delete_message(message)

# Parse request
def do_some_work(data):
  print 'working on data...'
  print data
  if data['request'] == 'update':
    # TODO: run latex thread
    print 'update!'

create_queue(message_queue_name, 120)
create_bucket(message_bucket_name)
store_message(message_queue_name, message_bucket_name, 'text_key')
read_message(message_queue_name)
