from __future__ import print_function

import json
import urllib
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
        #print("Received event: " + json.dumps(event, indent=2))

        # Get the object from the event and show its content type
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
        print ("buket:" + bucket)
        print ("key:" + key)
        obj = s3.get_object(Bucket=bucket,Key=key)
        body = obj['Body'].read()
        print(body)
        print("hello")
