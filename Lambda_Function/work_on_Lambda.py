#!/usr/bin/env python
# -*- coding:utf-8 -*-                                                                                                                                   

import  json
import  boto3 
from troposphere import Ref, Tags,Template
from troposphere.ec2 import VPC
print('Loading function')

s3 = boto3.client('s3')

def cFn_maker_handler(event,context):
    
    

f = open('text.txt', 'r')                                                                                                                               
line = f.readline()                                                                                                                                     
CidrBlockList = line[:-1].split(',')                                                                                                                    
print  CidrBlockList                                                                                                                                    
line = f.readline()                                                                                                                                    
EnableDnsSupportList = line[:-1].split(',')                                                                                                              
print  EnableDnsSupportList                                                                                                                              
f.close 

t = Template()

t.add_version("2010-09-09")

t.add_description("""\
console. You will be billed for the AWS resources used if you create a stack \
from this template.""")


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

print(t.to_json())
