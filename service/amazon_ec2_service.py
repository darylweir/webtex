import os.path
import boto

##
## Functions to start and stop instances of Amazon EC2.
##

key_id = 'AmznHack'
key_location = '~/.ssh'
ami_instance = 'ami-bb709dd2'

def start_instance(amazon_key_id, local_key_location, instance_id):
  ec2 = boto.connect_ec2()
  key_pair = ec2.create_key_pair(key_id)  # only needs to be done once
  key_pair.save(key_location)
  reservation = ec2.run_instances(image_id=ami_instance, key_name=key_id)
  return reservation

def output_instances():
  ec2 = boto.connect_ec2()
  # Wait a minute or two while it boots
  for r in ec2.get_all_instances():
    print r.id
    #if r.id == reservation.id:
        #break
  print r.instances[0].public_dns_name  
  # output: ubuntu@ec2-50-19-171-156.compute-1.amazonaws.com

def stop_instance(ids):
  ec2 = boto.connect_ec2()
  ec2.stop_instances(instance_ids=ids)

#$ chmod 600 key_location + '/' + key_id + '.pem'
#$ ssh -i ~/.ssh/amzn-hack-webtex.pem ubuntu@ec2-50-19-171-156.compute-1.amazonaws.com


