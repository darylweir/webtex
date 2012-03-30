import boto

##
## Functions to store and retrieve a file with Amazon s3.
##

def store_file(bucket_name, file_key, filename):
  s3 = boto.connect_s3()
  bucket = s3.create_bucket(bucket_name)  # bucket names must be unique
  key = bucket.new_key(file_key)
  key.set_contents_from_filename(filename)
  key.set_acl('public-read')

def retrieve_file(bucket_name, file_key, filename):
  s3 = boto.connect_s3()
  key = s3.get_bucket(bucket_name).get_key(file_key)
  key.get_contents_to_filename('/' + filename)
  
def move_file(bucket_name, new_bucket_name, file_key, filename):
  s3 = boto.connect_s3()
  key = s3.get_bucket(bucket_name).get_key(file_key)
  new_key = key.copy(new_bucket_name, filename)
  if new_key.exists:
      key.delete()

store_file('test_bucket.webtex.com', 'test/test_file.txt', '/home/hacker-6-05/test_file.txt')
retrieve_file('test_bucket.webtex.com', 'test/test_file.txt', '/home/hacker-6-05/test_file.txt')
