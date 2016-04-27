# coding: utf-8
from __future__ import print_function

import json
import urllib
import boto3
import string
from troposphere import Ref, Tags,Template
from troposphere.ec2 import VPC,Subnet,InternetGateway,VPNGateway,CustomerGateway,VPCGatewayAttachment,\
DHCPOptions,VPCDHCPOptionsAssociation,RouteTable,Route,SubnetRouteTableAssociation,NetworkAcl,NetworkAclEntry,\
SubnetNetworkAclAssociation,SecurityGroup,SecurityGroupIngress,SecurityGroupEgress,PortRange

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
        # u'VPCの作成'
        VPC_CidrBlockList = body_list[0].split(',')
        VPC_EnableDnsHostnamesList = body_list[1].split(',')
        VPC_TagsValueList = body_list[2].split(',')
        # u'サブネットの作成'
        Subnet_CidrBlockList = body_list[3].split(',')
        Subnet_AzList = body_list[4].split(',')
        Subnet_MapPublicIpOnLaunchList = body_list[5].split(',')
        Subnet_TagsValueList = body_list[6].split(',')
        Subnet_VpcIdList = body_list[7].split(',')
        # u'各種GateWayの作成
        InternetGateway_TagsValueList = body_list[8].split(',')
        VPNGateway_TagsValueList = body_list[9].split(',')
        CustomerGateway_TagsValueList = body_list[10].split(',')
        CustomerGateway_IpAddressList = body_list[11].split(',')
        CustomerGateway_BgpAsnList = body_list[12].split(',')
        # u'各種GatewayのVPCへのアタッチ'
        VPCGatewayAttachment_InternetGatewayIdList = body_list[13].split(',')
        VPCGatewayAttachment_VpcId_IGList = body_list[14].split(',')
        VPCGatewayAttachment_VpnGatewayIdList = body_list[15].split(',')
        VPCGatewayAttachment_VpcId_VPNList = body_list[16].split(',')
        # u'DHCPオプションの作成'
        DHCPOptions_DomainNameList = body_list[17].split(',')
        DHCPOptions_ValueList = body_list[18].split(',')
        # u'VPCへのDHCPオプションの関連付け'
        VPCDHCPOptionsAssociation_DhcpOptionsIdList = body_list[19].split(',')
        VPCDHCPOptionsAssociation_VpcIdList = body_list[20].split(',')
        # u'ルートテーブルの作成'
        RouteTable_VpcIdList = body_list[21].split(',')
        RouteTable_TagsValueList = body_list[22].split(',')
        # u'ルートテーブルへのGatewayの関連付け'
        Route_GatewayIdList = body_list[23].split(',')
        Route_RouteTableId_GWList = body_list[24].split(',')
        # u'サブネットへのルートテーブルの関連付け'
        SubnetRouteTableAssociation_RouteTableIdList = body_list[25].split(',')
        SubnetRouteTableAssociation_SubnetIdList = body_list[26].split(',')
        # u'ネットワークACLの作成'
        NetworkAcl_TagsValueList = body_list[27].split(',')
        NetworkAcl_VpcIdList = body_list[28].split(',')
        # 'ネットワークACLへのルールの追加'
        NetworkAclEntry_CidrBlockList = body_list[29].split(',')
        NetworkAclEntry_EgressList = body_list[30].split(',')
        NetworkAclEntry_NetworkAclIdList = body_list[31].split(',')
        NetworkAclEntry_PortRangeFromList = body_list[32].split(',')
        NetworkAclEntry_PortRangeToList = body_list[33].split(',')
        NetworkAclEntry_ProtocolList = body_list[34].split(',')
        NetworkAclEntry_RuleActionList = body_list[35].split(',')
        NetworkAclEntry_RuleNumberList = body_list[36].split(',')
        # 'サブネットへのネットワークACLの関連付け'
        SubnetNetworkAclAssociation_SubnetIdList = body_list[37].split(',')
        SubnetNetworkAclAssociation_NetworkAclIdList = body_list[38].split(',')
        # 'セキュリティグループの作成'
        SecurityGroup_TagsValueList = body_list[39].split(',')
        SecurityGroup_GroupDescriptionList = body_list[40].split(',')
        SecurityGroup_VpcIdList = body_list[41].split(',')
        # 'セキュリティグループへのインバウンドルールの設定_ソースにIPを指定'
        SGIngressIP_CidrIpList = body_list[42].split(',')
        SGIngressIP_FromPortList = body_list[43].split(',')
        SGIngressIP_ToPortList = body_list[44].split(',')
        SGIngressIP_GroupIdList = body_list[45].split(',')
        SGIngressIP_IpProtocolList = body_list[46].split(',')
        # 'セキュリティグループへのインバウンドルールの設定_ソースにセキュリティグループを指定'
        SGIngressSG_FromPortList = body_list[47].split(',')
        SGIngressSG_ToPortList = body_list[48].split(',')
        SGIngressSG_GroupIdList = body_list[49].split(',')
        SGIngressSG_IpProtocolList = body_list[50].split(',')
        SGIngressSG_SourceSecurityGroupIdList = body_list[51].split(',')
        # 'セキュリティグループへのアウトバウンドルールの設定_宛先にIPを指定'
        SGEgressIP_CidrIpList = body_list[52].split(',')
        SGEgressIP_FromPortList = body_list[53].split(',')
        SGEgressIP_ToPortList = body_list[54].split(',')
        SGEgressIP_GroupIdList = body_list[55].split(',')
        SGEgressIP_IpProtocolList = body_list[56].split(',')
        # 'セキュリティグループへのアウトバウンドルールの設定_宛先にセキュリティグループを指定'
        SGEgressSG_FromPortList = body_list[57].split(',')
        SGEgressSG_ToPortList = body_list[58].split(',')
        SGEgressSG_GroupIdList = body_list[59].split(',')
        SGEgressSG_IpProtocolList = body_list[60].split(',')
        SGEgressSG_DestinationSecurityGroupIdList = body_list[61].split(',')


        t = Template()
        t.add_version("2010-09-09")
        t.add_description("ROOP&ROOP")
        # u'VPCの作成'
        if len(VPC_CidrBlockList) > 1:
            for (address,dns,value) in zip(VPC_CidrBlockList[1:],VPC_EnableDnsHostnamesList[1:],VPC_TagsValueList[1:]):
                t.add_resource(VPC(
                              value.translate(string.maketrans("", ""), "-_"),
                              EnableDnsSupport="true",
                              CidrBlock=address,
                              EnableDnsHostnames=dns,
                              Tags=Tags(
                                       Name=value
                              )
                ))
        # u'サブネットの作成'
        if len(Subnet_CidrBlockList) > 1:
            for (address,az,pip,value,vpcid) in zip(Subnet_CidrBlockList[1:],Subnet_AzList[1:],Subnet_MapPublicIpOnLaunchList[1:],\
                                                    Subnet_TagsValueList[1:],Subnet_VpcIdList[1:]):
                t.add_resource(Subnet(
                              value.translate(string.maketrans("", ""), "-_")
                              CidrBlock=address,
                              AvailabilityZone=az,
                              MapPublicIpOnLaunch=pip,
                              VpcId=Ref(vpcid.translate(string.maketrans("", ""), "-_")),
                              Tags=Tags(
                                       Name=value
                              )
                ))
        # u'各種GateWayの作成
        if len(InternetGateway_TagsValueList) > 1:
            for (value) in (InternetGateway_TagsValueList[1:]):
                t.add_resource(InternetGateway(
                              value,
                              Tags=Tags(
                                       Name=value
                              )
                ))
        if len(CustomerGateway_TagsValueList) > 1:
            for (value,ipaddress,bgpasn) in zip(CustomerGateway_TagsValueList[1:],CustomerGateway_IpAddressList[1:],CustomerGateway_BgpAsnList[1:]):
                t.add_resource(CustomerGateway(
                              value,
                              Type="ipsec.1",
                              IpAddress=ipaddress,
                              BgpAsn=bgpasn,
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
        # u'各種GatewayのVPCへのアタッチ'
        if len(VPCGatewayAttachment_InternetGatewayIdList) > 1:
            for i,(gatewayid,vpcid) in enumerate(zip(VPCGatewayAttachment_InternetGatewayIdList[1:],VPCGatewayAttachment_VpcId_IGList[1:])):
                t.add_resource(VPCGatewayAttachment(
                              "VPCGatewayAttachmentInternetGateway"+str(i),
                              InternetGatewayId=Ref(gatewayid),
                              VpcId=Ref(vpcid)
                ))
        if len(VPCGatewayAttachment_VpnGatewayIdList) > 1:
            for i,(gatewayid,vpcid) in enumerate(zip(VPCGatewayAttachment_VpnGatewayIdList[1:],VPCGatewayAttachment_VpcId_VPNList[1:])):
                t.add_resource(VPCGatewayAttachment(
                              "VPCGatewayAttachmentVPNGateway"+str(i),
                              VpnGatewayId=Ref(gatewayid),
                              VpcId=Ref(vpcid)
                ))
        # u'DHCPオプションの作成'
        if len(DHCPOptions_DomainNameList) > 1:
            for (domainname,value) in zip(DHCPOptions_DomainNameList[1:],DHCPOptions_ValueList[1:]):
                t.add_resource(DHCPOptions(
                              value,
                              DomainName=domainname,
                              DomainNameServers=["AmazonProvidedDNS"]
                ))
        # u'VPCへのDHCPオプションの関連付け'
        if len(VPCDHCPOptionsAssociation_DhcpOptionsIdList) > 1:
            for i,(dhcpoptionid,vpcid) in enumerate(zip(VPCDHCPOptionsAssociation_DhcpOptionsIdList[1:],VPCDHCPOptionsAssociation_VpcIdList[1:])):
                t.add_resource(VPCDHCPOptionsAssociation(
                              "VPCDHCPOptionsAssociation" + str(i),
                              DhcpOptionsId=Ref(dhcpoptionid),
                              VpcId=vpcid
                ))
        # u'ルートテーブルの作成'
        if len(RouteTable_VpcIdList) > 1:
            for (vpcid,value) in zip(RouteTable_VpcIdList[1:],RouteTable_TagsValueList[1:]):
                t.add_resource(RouteTable(
                              value,
                              VpcId=Ref(vpcid),
                              Tags=Tags(
                                       Name=value
                              )
                ))
        # u'ルートテーブルへのGatewayの関連付け'
        if len(Route_GatewayIdList) > 1:
            for i,(gatewayid,routetable) in enumerate(zip(Route_GatewayIdList[1:],Route_RouteTableId_GWList[1:])):
                t.add_resource(Route(
                              "RouteGatewayId" + str(i),
                              DestinationCidrBlock="0.0.0.0/0",
                              GatewayId=Ref(gatewayid),
                              RouteTableId=Ref(routetable)
                ))
        # u'サブネットへのルートテーブルの関連付け'
        if len(SubnetRouteTableAssociation_RouteTableIdList) > 1:
            for i,(routetableid,subnetid) in enumerate(zip(SubnetRouteTableAssociation_RouteTableIdList[1:],SubnetRouteTableAssociation_SubnetIdList[1:])):
                t.add_resource(SubnetRouteTableAssociation(
                              "SubnetRouteTableAssociation" + str(i),
                              RouteTableId=Ref(routetableid),
                              SubnetId=Ref(subnetid)
                ))
        # u'ネットワークACLの作成'
        if len(NetworkAcl_TagsValueList) > 1:
            for (value,vpcid) in zip(NetworkAcl_TagsValueList[1:],NetworkAcl_VpcIdList[1:]):
                t.add_resource(NetworkAcl(
                              value,
                              VpcId=Ref(vpcid),
                              Tags=Tags(
                                       Name=value
                              )
                ))
        # 'ネットワークACLへのルールの追加'
        if len(NetworkAclEntry_CidrBlockList) > 1:
            for i,(cidr,egress,naclid,pfrom,pto,protocol,ruleaction,rulenumber) in enumerate(zip(NetworkAclEntry_CidrBlockList[1:],NetworkAclEntry_EgressList[1:],\
                                                                                                 NetworkAclEntry_NetworkAclIdList[1:],NetworkAclEntry_PortRangeFromList[1:],\
                                                                                                 NetworkAclEntry_PortRangeToList[1:],NetworkAclEntry_ProtocolList[1:],\
                                                                                                 NetworkAclEntry_RuleActionList[1:],NetworkAclEntry_RuleNumberList[1:])):
                t.add_resource(NetworkAclEntry(
                              "NetworkAclEntry" + str(i),
                              CidrBlock=cidr,
                              Egress=egress,
                              NetworkAclId=Ref(naclid),
                              PortRange=PortRange(
                                       From=pfrom,
                                       To=pto
                              ),
                              Protocol=protocol,
                              RuleAction=ruleaction,
                              RuleNumber=rulenumber
                ))
        # 'サブネットへのネットワークACLの関連付け'
        if len(SubnetNetworkAclAssociation_SubnetIdList) > 1:
            for i,(subnetid,naclid) in enumerate(zip(SubnetNetworkAclAssociation_SubnetIdList[1:],SubnetNetworkAclAssociation_NetworkAclIdList[1:])):
                t.add_resource(SubnetNetworkAclAssociation(
                              "SubnetNetworkAclAssociation" + str(i),
                              SubnetId=Ref(subnetid),
                              NetworkAclId=Ref(naclid)
                ))
        # 'セキュリティグループの作成'
        if len(SecurityGroup_TagsValueList) > 1:
            for (value,description,vpcid) in zip(SecurityGroup_TagsValueList[1:],SecurityGroup_GroupDescriptionList[1:],SecurityGroup_VpcIdList[1:]):
                t.add_resource(SecurityGroup(
                              value,
                              GroupDescription=description,
                              VpcId=Ref(vpcid),
                              Tags=Tags(
                                       Name=value
                              )
                ))
        # 'セキュリティグループへのインバウンドルールの設定_ソースにIPを指定'
        if len(SGIngressIP_CidrIpList) > 1:
            for i,(cidr,pfrom,pto,sgid,protocol) in enumerate(zip(SGIngressIP_CidrIpList[1:],SGIngressIP_FromPortList[1:],SGIngressIP_ToPortList[1:],\
                                                                  SGIngressIP_GroupIdList[1:],SGIngressIP_IpProtocolList[1:])):
                t.add_resource(SecurityGroupIngress(
                              "SecurityGroupIngress_IP" + str(i),
                              CidrIp=cidr,
                              FromPort=pfrom,
                              ToPort=pto,
                              GroupId=sgid,
                              IpProtocol=protocol
                ))
        # 'セキュリティグループへのインバウンドルールの設定_ソースにセキュリティグループを指定'
        if len(SGIngressSG_FromPortList) > 1:
            for i,(pfrom,pto,sgid,protocol,sourcesgid) in enumerate(zip(SGIngressSG_FromPortList[1:],SGIngressSG_ToPortList[1:],SGIngressSG_GroupIdList[1:],\
                                                                        SGIngressSG_IpProtocolList[1:],SGIngressSG_SourceSecurityGroupIdList[1:])):
                t.add_resource(SecurityGroupIngress(
                              "SecurityGroupIngress_SG" + str(i),
                              FromPort=pfrom,
                              ToPort=pto,
                              GroupId=sgid,
                              IpProtocol=protocol,
                              SourceSecurityGroupId=sourcesgid
                ))
        # 'セキュリティグループへのアウトバウンドルールの設定_宛先にIPを指定'
        if len(SGEgressIP_CidrIpList) > 1:
            for i,(cidr,pfrom,pto,sgid,protocol) in enumerate(zip(SGEgressIP_CidrIpList[1:],SGEgressIP_FromPortList[1:],SGEgressIP_ToPortList[1:],\
                                                                  SGEgressIP_GroupIdList[1:],SGEgressIP_IpProtocolList[1:])):
                t.add_resource(SecurityGroupEgress(
                              "SecurityGroupEgress_IP" + str(i),
                              CidrIp=cidr,
                              FromPort=pfrom,
                              ToPort=pto,
                              GroupId=sgid,
                              IpProtocol=protocol
                ))
        # 'セキュリティグループへのアウトバウンドルールの設定_宛先にセキュリティグループを指定'
        if len(SGEgressSG_FromPortList) > 1:
            for i,(pfrom,pto,sgid,protocol,distsgid) in enumerate(zip(SGEgressSG_FromPortList[1:],SGEgressSG_ToPortList[1:],SGEgressSG_GroupIdList[1:],\
                                                                      SGEgressSG_IpProtocolList[1:],SGEgressSG_DestinationSecurityGroupIdList[1:])):
                t.add_resource(SecurityGroupEgress(
                              "SecurityGroupEgress_SG" + str(i),
                              FromPort=pfrom,
                              ToPort=pto,
                              GroupId=sgid,
                              IpProtocol=protocol,
                              DestinationSecurityGroupId=distsgid
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
