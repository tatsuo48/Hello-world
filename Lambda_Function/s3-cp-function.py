from __future__ import print_function



import json
import urllib
import boto3
from troposphere import Ref, Tags,Template
from troposphere.ec2 import VPC,Subnet
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
        VPC_CidrBlockList = body_list[0].split(',')
        VPC_EnableDnsSupportList = body_list[1].split(',')
        VPC_TagsValueList =  body_list[2].split(',')
        Subnet_CidrBlockList =  body_list[3].split(',')
        Subnet_AzList =  body_list[4].split(',')
        Subnet_MapPublicIpOnLaunchList =  body_list[5].split(',')
        Subnet_TagsValueList =  body_list[6].split(',')
        Subnet_VpcIdlist =  body_list[7].split(',')  
        t = Template()

        t.add_version("2010-09-09")

        t.add_description("ROOP&ROOP")

        if len(VPC_CidrBlockList) > 1:
            for (address,dns,value) in zip(VPC_CidrBlockList[1:],VPC_EnableDnsSupportList[1:],VPC_TagsValueList[1:]):

                    t.add_resource(VPC(
                                value,
                                EnableDnsSupport="true",
                                CidrBlock=address,
                                EnableDnsHostnames=dns,
                                Tags=Tags(
                                                 Name=value
                                            )
                                ))
        if len(Subnet_CidrBlockList) > 1:      
            for (address,az,pip,value,vpc) in zip(Subnet_CidrBlockList[1:],Subnet_AzList[1:],Subnet_MapPublicIpOnLaunchList[1:],Subnet_TagsValueList[1:],Subnet_VpcIdlist[1:]):

                    t.add_resource(Subnet(
                                value,
                                CidrBlock=address,
                                AvailabilityZone=az,
                                MapPublicIpOnLaunch=pip,
                                VpcId=Ref(vpc),
                                Tags=Tags(                                                                                                                                               
                                                 Name=value                                                                                                                          
                                            )
        
                               ))    
        json_template = t.to_json()
        bucket = s3.Bucket('cf-templates-hokan')
        obj = bucket.Object('json-template-' + basename + ' .txt')
        response = obj.put(
                       Body=json_template.encode('utf-8'),
                       ContentEncoding='utf-8',
                       ContentType='text/plane'
                    )
        print(json_template)
