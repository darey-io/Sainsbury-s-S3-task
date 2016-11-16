#!/usr/bin/python
import boto
import os.path
import sys
import os
import glob
from boto.s3.key import Key
from boto.ec2.connection import EC2Connection
action = input("Please type in : upload-emails ... ")
bucket_name = input("What is the bucket_name you wish to create: ")
s3 = boto.connect_s3(aws_access_key_id='AKIAIUUEBUOEBQZPZCIA', aws_secret_access_key= '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')
ec2 = EC2Connection(aws_access_key_id='AKIAIUUEBUOEBQZPZCIA', aws_secret_access_key= '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')
#Create a bucket incase one does not already exist

def create_bucket():
    if not s3.lookup(bucket_name):
        print ("Starting to create bucket")
        s3.create_bucket(bucket_name)
if action == "create-bucket":
    create_bucket()

#To create a website
#if action == "create-website":
def create_website():
    bucket = s3.create_bucket(bucket_name)
    index_file = bucket.new_key('index.html')
    index_file.content_type = "text/html"
    error_file = bucket.new_key('error.html')
    error_file.content_type = "text/html"
    index_html= '<html>\
<head>\
<title>AWS Admin Task</title>\
</head>\
<body>\
<h1>Welcome to Sainsburys AWS Administration task for Dare Olufunmilayo!</h1>\
<h4>Below is some of the Enron email files in "PST" format on Amazon S3. Click on the hyperlink to download </h4>\
<ol><p>Benjamin Rogers  <a href="https://s3.amazonaws.com/s3task/files/benjamin_rogers_001.pst"> benjamin_rogers_001.pst</a></p></ol>\
<ol><p>Louise Kitchen  <a href="https://s3.amazonaws.com/s3task/files/louise_kitchen_000.pst"> louise_kitchen_001.pst</a></ol>\
<ol><p>Robert Badeer   <a href="https://s3.amazonaws.com/s3task/files/robert_badeer_000.pst"> robert_badeer_000.pst</a></p></ol>\
<ol><p>John Griffith  <a href="https://s3.amazonaws.com/s3task/files/john_griffith_001.pst"> john_griffith_000.pst</a></ol>\
<ol><p>Kevin Presto  <a href="https://s3.amazonaws.com/s3task/files/kevin_presto_000.pst">  kevin_presto_000.pst</a></p></ol>\
<ol><p>Cara Semperger  <a href="https://s3.amazonaws.com/s3task/files/cara_semperger_000.pst"> cara_semperger_000.pst</a></ol>\
<br/><br/>\
  <ol><p>If you wish to browse the entire directory, please click <a href="https://s3.amazonaws.com/testfordare/index.html"> directory</a></p></ol>\
    </td>\
    <td bgcolor="#aaa" width="20%">\      
   </tr>\
</table>\
</p>\
</body>\
</html>'\
    
    error_html= '<html>\
<head>\
<title>Ooops! Error page</title>\
</head>\
<body>\
<h1>ERROR! Please use a valid URL</h1>\
</body>\
</html>'    
    error_file.set_contents_from_string(error_html, policy ='public-read')
    index_file.set_contents_from_string(index_html, policy ='public-read')
    bucket.configure_website('index.html', 'error.html')
    print ("Website URL for Bucket  " + bucket.get_website_endpoint())
    
    
#Upload data into S3
if action == "upload-emails":
    instances= ec2.get_all_instances()
    r = instances[0]
    for inst in r.instances:
        instance_status= inst.state
        if not instance_status =="running":
            print ("AWS Instance is not available")
            launch_instance=ec2.run_instances
            while True:
                inst.state == "running"
                create_bucket()                
                bucket = s3.get_bucket(bucket_name)
                print ("uploading emails to S3")
                for file in glob.glob("*.pst"):
                    key = bucket.new_key("files/"+file)
                    key.set_contents_from_filename(file)
                    print ("Uploaded file: " + file)
        else:
            create_bucket()
            bucket = s3.get_bucket(bucket_name)
            print ("uploading emails to S3")
            for file in glob.glob("*.pst"):
                key = bucket.new_key("files/"+file)
                key.set_contents_from_filename(file)
                print ("Uploaded file: " + file)
                print("setting up the HTML Page")
if bucket_name != " ":
    create_website()