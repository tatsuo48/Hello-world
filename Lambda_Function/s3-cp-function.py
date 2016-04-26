# coding: utf-8
from __future__ import print_function 

import json
import urllib
import boto3
from troposphere import Ref, Tags,Template
from troposphere.ec2 import VPC,Subnet,InternetGateway,VPNGateway,VPCGatewayAttachment,\
DHCPOptions,VPCDHCPOptionsAssociation,RouteTable,Route,SubnetRouteTableAssociation
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
        # u'VPC関係'
        VPC_CidrBlockList = body_list[0].split(',')
        VPC_EnableDnsSupportList = body_list[1].split(',')
        VPC_TagsValueList =  body_list[2].split(',')
        # u'Subnet関係'
        Subnet_CidrBlockList =  body_list[3].split(',')
        Subnet_AzList =  body_list[4].split(',')
        Subnet_MapPublicIpOnLaunchList =  body_list[5].split(',')
        Subnet_TagsValueList =  body_list[6].split(',')
        Subnet_VpcIdlist =  body_list[7].split(',')
        # u'Gateway関係'
        InternetGateway_TagsValueList = body_list[8].split(',')
        VPNGateway_TagsValueList = body_list[9].split(',')
        VPCGatewayAttachment_InternetGatewayIdList = body_list[10].split(',')
        VPCGatewayAttachment_VpcId_IGList = body_list[11].split(',')
        VPCGatewayAttachment_VpnGatewayIdList = body_list[12].split(',')
        VPCGatewayAttachment_VpcId_VPNList = body_list[13].split(',')
        # u'DHCP関係'
        DHCPOptions_DomainNameList = body_list[14].split(',')
        DHCPOptions_ValueList = body_list[15].split(',')
        VPCDHCPOptionsAssociation_DhcpOptionsIdList = body_list[16].split(',')
        VPCDHCPOptionsAssociation_VpcIdList = body_list[17].split(',')
        # u'RouteTable関係'
        RouteTable_VpcIdList = body_list[18].split(',')
        RouteTable_TagsValueList = body_list[19].split(',')
        # u'Route関係'
        Route_GatewayIdList = body_list[20].split(',')
        Route_RouteTableId_GWList = body_list[21].split(',')
        Route_InstanceIdList = body_list[22].split(',')
        Route_RouteTableId_INList = body_list[23].split(',')
        Route_NatGatewayIdList = body_list[24].split(',')
        Route_RouteTableId_NATList = body_list[25].split(',')
        Route_NetworkInterfaceIdList = body_list[26].split(',')
        Route_RouteTableId_NIList = body_list[27].split(',')
        Route_VpcPeeringConnectionIdList = body_list[28].split(',')
        Route_RouteTableId_PeeringList = body_list[29].split(',')
        # u'RouteTableとSubnetの紐付け'
        SubnetRouteTableAssociation_RouteTableIdList = body_list[30].split(',')
        SubnetRouteTableAssociation_SubnetIdList = body_list[31].split(',')

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
            for (address,az,pip,value,vpcid) in zip(Subnet_CidrBlockList[1:],Subnet_AzList[1:],Subnet_MapPublicIpOnLaunchList[1:],Subnet_TagsValueList[1:],Subnet_VpcIdlist[1:]):
                t.add_resource(Subnet(
                              value,
                              CidrBlock=address,
                              AvailabilityZone=az,
                              MapPublicIpOnLaunch=pip,
                              VpcId=Ref(vpcid),
                              Tags=Tags(
                                       Name=value
                              )
                ))
        if len(InternetGateway_TagsValueList) > 1:
            for (value) in (InternetGateway_TagsValueList[1:]):
                t.add_resource(InternetGateway(
                              value,
                              Tags=Tags(
                                       Name=value
                              )
                ))
        if len(VPNGateway_TagsValueList) > 1:
            for (value) in (VPNGateway_TagsValueList[1:]):
                t.add_resource(VPNGateway(
                              value,
                              Type="ipsec.1",
                              Tags=Tags(
                                       Name=value
                              )
                ))
        if len(VPCGatewayAttachment_InternetGatewayIdList) > 1:
            for i,(gatewayid,vpcid) in enumerate(zip(VPCGatewayAttachment_InternetGatewayIdList[1:],VPCGatewayAttachment_VpcId_IGList[1:])):
                t.add_resource(VPCGatewayAttachment(
                              "VPCGatewayAttachmentInternetGateway"+str(i),
                              InternetGatewayId=gatewayid,
                              VpcId=Ref(vpcid)
                ))
        if len(VPCGatewayAttachment_VpnGatewayIdList) > 1:
            for i,(gatewayid,vpcid) in enumerate(zip(VPCGatewayAttachment_VpnGatewayIdList[1:],VPCGatewayAttachment_VpcId_VPNList[1:])):
                t.add_resource(VPCGatewayAttachment(
                              "VPCGatewayAttachmentVPNGateway"+str(i),
                              VpnGatewayId=gatewayid,
                              VpcId=Ref(vpcid)
                ))
        if len(DHCPOptions_DomainNameList) > 1:
            for (domainname,value) in zip(DHCPOptions_DomainNameList[1:],DHCPOptions_ValueList[1:]):
                t.add_resource(DHCPOptions(
                              value,
                              DomainName=domainname,
                              DomainNameServers=["AmazonProvidedDNS"]
                ))
        if len(VPCDHCPOptionsAssociation_DhcpOptionsIdList) > 1:
            for i,(dhcpoptionid,vpcid) in enumerate(zip(VPCDHCPOptionsAssociation_DhcpOptionsIdList[1:],VPCDHCPOptionsAssociation_VpcIdList[1:])):
                t.add_resource(VPCDHCPOptionsAssociation(
                              "VPCDHCPOptionsAssociation" + str(i),
                              DhcpOptionsId=Ref(dhcpoptionid),
                              VpcId=vpcid
                ))
        if len(RouteTable_VpcIdList) > 1:
            for (vpcid,value) in zip(RouteTable_VpcIdList[1:],RouteTable_TagsValueList[1:]):
                t.add_resource(RouteTable(
                              value,
                              VpcId=Ref(vpcid),
                              Tags=Tags(
                                       Name=value
                              )
                ))
        if len(Route_GatewayIdList) > 1:
            for i,(gatewayid,routetable) in enumerate(zip(Route_GatewayIdList[1:],Route_RouteTableId_GWList[1:])):
                t.add_resource(Route(
                              "RouteGatewayId" + str(i),
                              DestinationCidrBlock="0.0.0.0/0",
                              GatewayId=Ref(gatewayid),
                              RouteTableId=Ref(routetable)
                ))
        if len(Route_InstanceIdList) > 1:
            for i,(instanceid,routetable) in enumerate(zip(Route_InstanceIdList[1:],Route_RouteTableId_INList[1:])):
                t.add_resource(Route(
                              "RouteInstanceId" + str(i),
                              DestinationCidrBlock="0.0.0.0/0",
                              InstanceId=Ref(instanceid),
                              RouteTableId=Ref(routetable)
                ))
        if len(Route_NatGatewayIdList) > 1:
            for i,(natgatewayid,routetable) in enumerate(zip(Route_NatGatewayIdList[1:],Route_RouteTableId_NATList[1:])):
                t.add_resource(Route(
                              "RouteNatGatewayId" + str(i),
                              DestinationCidrBlock="0.0.0.0/0",
                              NatGatewayId=Ref(natgatewayid),
                              RouteTableId=Ref(routetable)
                ))
        if len(Route_NetworkInterfaceIdList) > 1:
            for i,(networkinterfaceid,routetable) in enumerate(zip(Route_NetworkInterfaceIdList[1:],Route_RouteTableId_NIList[1:])):
                t.add_resource(Route(
                              "RouteNetworkInterfaceId" + str(i),
                              DestinationCidrBlock="0.0.0.0/0",
                              NetworkInterfaceId=Ref(networkinterfaceid),
                              RouteTableId=Ref(routetable)
                ))
        if len(Route_VpcPeeringConnectionIdList) > 1:
            for i,(vpcpeeringconnectionid,routetable) in enumerate(zip(Route_VpcPeeringConnectionIdList[1:],Route_RouteTableId_PeeringList[1:])):
                t.add_resource(Route(
                              "RouteGateway" + str(i),
                              DestinationCidrBlock="0.0.0.0/0",
                              VpcPeeringConnectionId=Ref(vpcpeeringconnectionid),
                              RouteTableId=Ref(routetable)
                ))
        if len(SubnetRouteTableAssociation_RouteTableIdList) > 1:
            for i,(routetableid,subnetid) in enumerate(zip(SubnetRouteTableAssociation_RouteTableIdList[1:],SubnetRouteTableAssociation_SubnetIdList[1:])):
                t.add_resource(SubnetRouteTableAssociation(
                              "SubnetRouteTableAssociation" + str(i),
                              RouteTableId=Ref(routetableid),
                              SubnetId=Ref(subnetid)
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
