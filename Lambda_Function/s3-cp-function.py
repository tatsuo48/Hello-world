from __future__ import print_function

import json
import urllib
import boto3
from troposphere import Ref, Tags,Template
from troposphere.ec2 import VPC
from datetime import datetime
basename = datetime.now().strftime("%Y%m%d-%H%M%S")

print('Loading function')

s3 = boto3.resource('s3')

def lambda_handler(event, context):
        #print("Received event: " + json.dumps(event, indent=2))

        # Get the object from the event and show its content type
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
        print ("buket:" + bucket)
        print ("key:" + key)
        obj = s3.Object(bucket,key)
        response= obj.get()
        body = response['Body'].read()
        body_list= body.splitlines()
        CidrBlockList = body_list[0].split(',')
        EnableDnsSupportList = body_list[1].split(',')
        t = Template()

        t.add_version("2010-09-09")

        t.add_description("ROOP&ROOP")

        for i,(address,dns) in enumerate(zip(CidrBlockList,EnableDnsSupportList)):

                    t.add_resource(VPC(
                                "VPC"+str(i),
                                EnableDnsSupport=dns,
                                CidrBlock=address,
                                EnableDnsHostnames="true",
                                Tags=Tags(
                                                 Name="VPC"+str(i)
                                            )
                                ))

                    json_template = t.to_json()
                    bucket = s3.Bucket('yokoyama-config')
                    obj = bucket.Object('json-template-' + basename + ' .txt')
                    response = obj.put(
                            Body=json_template.encode('utf-8'),
                            ContentEncoding='utf-8',
                            ContentType='text/plane'
                    )
                    print(json_template)
