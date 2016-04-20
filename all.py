#!/usr/bin/python
# -*- coding: utf-8 -*-
# Converted from VPC_With_VPN_Connection.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates

from troposphere import Base64, FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Tags, Template
from troposphere.autoscaling import Metadata
from troposphere.ec2 import PortRange, NetworkAcl, Route, \
    VPCGatewayAttachment, SubnetRouteTableAssociation, Subnet, RouteTable, \
    VPC, NetworkInterfaceProperty, NetworkAclEntry, \
    SubnetNetworkAclAssociation, EIP, Instance, InternetGateway, \
    SecurityGroupRule, SecurityGroup
from troposphere.policies import CreationPolicy, ResourceSignal
from troposphere.cloudformation import Init, InitFile, InitFiles, \
    InitConfig, InitService, InitServices
import sys

params = sys.argv
t = Template()
t.add_version('2010-09-09')

t.add_description("""\
AWS CloudFormation Sample Template VPC_Single_Instance_In_Subnet: Sample \
template showing how to create a VPC and add an EC2 instance with an Elastic \
IP address and a security group. \.""")

t.add_resource(
    VPC(
            'VPC',
            CidrBlock="'"+ params[1]+ "'",
            Tags=Tags(
                   Name ='yokoyama')))


t.add_resource(
    Subnet(
        'Subnet1',
        CidrBlock="'"+params[2]+"'",
        VpcId=Ref(VPC),
        Tags=Tags(
                   Name='yokoyama-sub')))          

t.add_resource(
    Instance(
         "myinstance",
         ImageId="ami-951945d0", 
         InstanceType="t1.micro"))


print(t.to_json())
