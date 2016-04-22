#!/usr/bin/env python                                                                                                                                    
from troposphere import Ref, Tags,Template
from troposphere.ec2 import VPC

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
