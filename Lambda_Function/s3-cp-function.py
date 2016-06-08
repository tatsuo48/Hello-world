# coding: utf-8
from __future__ import print_function

import json
import urllib
import boto3
import string
from datetime import datetime
from troposphere import Ref, Tags,Template
from troposphere.ec2 import VPC,Subnet,InternetGateway,VPNGateway,CustomerGateway,VPCGatewayAttachment,\
DHCPOptions,VPCDHCPOptionsAssociation,RouteTable,Route,SubnetRouteTableAssociation,NetworkAcl,NetworkAclEntry,\
SubnetNetworkAclAssociation,SecurityGroup,SecurityGroupIngress,SecurityGroupEgress,PortRange

BASENAME = datetime.now().strftime("%Y%m%d-%H%M%S")

SAVE_BUCKET='cf-templates-hokan'

print('Loading function')

s3 = boto3.resource('s3')

def lambda_handler(event, context):
        print("Received event: " + json.dumps(event, indent=2))

        # lambda_handlerに渡されたイベントからｓ３バケットとキーを取り出してｓ３オブジェクトをgetする。
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
        print ("buket:" + bucket)
        print ("key:" + key)
        obj = s3.Object(bucket,key)
        response= obj.get()
        data = response['Body'].read()
        # パラメータシートの読み込み。
        #　作成したパラメータシートの先頭に書いてある文字列が変数名として使用されます。
        patrameter_list= data.splitlines()
        for i in range(len(parameter_list)):
               parameter =  parameter_list[i].split(',')
               a = str(parameter[0])
               ns = locals()
               ns[a] = parameter
      
        # テンプレートの作成
        t = Template()
        t.add_version("2010-09-09")
        t.add_description("ROOP&ROOP")
        # VPCの作成
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
                              value.translate(string.maketrans("", ""), "-_"),
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
                              value.translate(string.maketrans("", ""), "-_"),
                              Tags=Tags(
                                       Name=value
                              )
                ))
        if len(CustomerGateway_TagsValueList) > 1:
            for (value,ipaddress,bgpasn) in zip(CustomerGateway_TagsValueList[1:],CustomerGateway_IpAddressList[1:],CustomerGateway_BgpAsnList[1:]):
                t.add_resource(CustomerGateway(
                              value.translate(string.maketrans("", ""), "-_"),
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
                              value.translate(string.maketrans("", ""), "-_"),
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
                              InternetGatewayId=Ref(gatewayid.translate(string.maketrans("", ""), "-_")),
                              VpcId=Ref(vpcid.translate(string.maketrans("", ""), "-_"))
                ))
        if len(VPCGatewayAttachment_VpnGatewayIdList) > 1:
            for i,(gatewayid,vpcid) in enumerate(zip(VPCGatewayAttachment_VpnGatewayIdList[1:],VPCGatewayAttachment_VpcId_VPNList[1:])):
                t.add_resource(VPCGatewayAttachment(
                              "VPCGatewayAttachmentVPNGateway"+str(i),
                              VpnGatewayId=Ref(gatewayid.translate(string.maketrans("", ""), "-_")),
                              VpcId=Ref(vpcid.translate(string.maketrans("", ""), "-_"))
                ))
        # u'DHCPオプションの作成'
        if len(DHCPOptions_DomainNameList) > 1:
            for (domainname,domainnameservers,value,) in zip(DHCPOptions_DomainNameList[1:],DHCPOptions_DomainNameServersList[1:],DHCPOptions_ValueList[1:]):
                t.add_resource(DHCPOptions(
                              value.translate(string.maketrans("", ""), "-_"),
                              DomainName=domainname,
                              DomainNameServers=['"' + domainnameservers + '"'],
                              Tags=Tags(
                                       Name=value
                              )
                ))
        # u'VPCへのDHCPオプションの関連付け'
        if len(VPCDHCPOptionsAssociation_DhcpOptionsIdList) > 1:
            for i,(dhcpoptionid,vpcid) in enumerate(zip(VPCDHCPOptionsAssociation_DhcpOptionsIdList[1:],VPCDHCPOptionsAssociation_VpcIdList[1:])):
                t.add_resource(VPCDHCPOptionsAssociation(
                              "VPCDHCPOptionsAssociation" + str(i),
                              DhcpOptionsId=Ref(dhcpoptionid.translate(string.maketrans("", ""), "-_")),
                              VpcId=Ref(vpcid.translate(string.maketrans("", ""), "-_")),
                ))
        # u'ルートテーブルの作成'
        if len(RouteTable_VpcIdList) > 1:
            for (vpcid,value) in zip(RouteTable_VpcIdList[1:],RouteTable_TagsValueList[1:]):
                t.add_resource(RouteTable(
                              value.translate(string.maketrans("", ""), "-_"),
                              VpcId=Ref(vpcid.translate(string.maketrans("", ""), "-_")),
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
                              GatewayId=Ref(gatewayid.translate(string.maketrans("", ""), "-_")),
                              RouteTableId=Ref(routetable.translate(string.maketrans("", ""), "-_"))
                ))
        # u'サブネットへのルートテーブルの関連付け'
        if len(SubnetRouteTableAssociation_RouteTableIdList) > 1:
            for i,(routetableid,subnetid) in enumerate(zip(SubnetRouteTableAssociation_RouteTableIdList[1:],SubnetRouteTableAssociation_SubnetIdList[1:])):
                t.add_resource(SubnetRouteTableAssociation(
                              "SubnetRouteTableAssociation" + str(i),
                              RouteTableId=Ref(routetableid.translate(string.maketrans("", ""), "-_")),
                              SubnetId=Ref(subnetid.translate(string.maketrans("", ""), "-_"))
                ))
        # u'ネットワークACLの作成'
        if len(NetworkAcl_TagsValueList) > 1:
            for (value,vpcid) in zip(NetworkAcl_TagsValueList[1:],NetworkAcl_VpcIdList[1:]):
                t.add_resource(NetworkAcl(
                              value.translate(string.maketrans("", ""), "-_"),
                              VpcId=Ref(vpcid.translate(string.maketrans("", ""), "-_")),
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
                              NetworkAclId=Ref(naclid.translate(string.maketrans("", ""), "-_")),
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
                              SubnetId=Ref(subnetid.translate(string.maketrans("", ""), "-_")),
                              NetworkAclId=Ref(naclid.translate(string.maketrans("", ""), "-_"))
                ))
        # 'セキュリティグループの作成'
        if len(SecurityGroup_TagsValueList) > 1:
            for (value,description,vpcid) in zip(SecurityGroup_TagsValueList[1:],SecurityGroup_GroupDescriptionList[1:],SecurityGroup_VpcIdList[1:]):
                t.add_resource(SecurityGroup(
                              value.translate(string.maketrans("", ""), "-_"),
                              GroupDescription=description,
                              VpcId=Ref(vpcid.translate(string.maketrans("", ""), "-_")),
                              Tags=Tags(
                                       Name=value
                              )
                ))
        # 'セキュリティグループへのインバウンドルールの設定_ソースにIPを指定'
        if len(SGIngressIP_CidrIpList) > 1:
            for i,(cidr,pfrom,pto,sgid,protocol) in enumerate(zip(SGIngressIP_CidrIpList[1:],SGIngressIP_FromPortList[1:],SGIngressIP_ToPortList[1:],\
                                                                  SGIngressIP_GroupIdList[1:],SGIngressIP_IpProtocolList[1:])):
                t.add_resource(SecurityGroupIngress(
                              "SecurityGroupIngressIP" + str(i),
                              CidrIp=cidr,
                              FromPort=pfrom,
                              ToPort=pto,
                              GroupId=Ref(sgid.translate(string.maketrans("", ""), "-_")),
                              IpProtocol=protocol
                ))
        # 'セキュリティグループへのインバウンドルールの設定_ソースにセキュリティグループを指定'
        if len(SGIngressSG_FromPortList) > 1:
            for i,(pfrom,pto,sgid,protocol,sourcesgid) in enumerate(zip(SGIngressSG_FromPortList[1:],SGIngressSG_ToPortList[1:],SGIngressSG_GroupIdList[1:],\
                                                                        SGIngressSG_IpProtocolList[1:],SGIngressSG_SourceSecurityGroupIdList[1:])):
                t.add_resource(SecurityGroupIngress(
                              "SecurityGroupIngressSG" + str(i),
                              FromPort=pfrom,
                              ToPort=pto,
                              GroupId=Ref(sgid.translate(string.maketrans("", ""), "-_")),
                              IpProtocol=protocol,
                              SourceSecurityGroupId=Ref(sourcesgid.translate(string.maketrans("", ""), "-_"))
                ))
        # 'セキュリティグループへのアウトバウンドルールの設定_宛先にIPを指定'
        if len(SGEgressIP_CidrIpList) > 1:
            for i,(cidr,pfrom,pto,sgid,protocol) in enumerate(zip(SGEgressIP_CidrIpList[1:],SGEgressIP_FromPortList[1:],SGEgressIP_ToPortList[1:],\
                                                                  SGEgressIP_GroupIdList[1:],SGEgressIP_IpProtocolList[1:])):
                t.add_resource(SecurityGroupEgress(
                              "SecurityGroupEgressIP" + str(i),
                              CidrIp=cidr,
                              FromPort=pfrom,
                              ToPort=pto,
                              GroupId=Ref(sgid.translate(string.maketrans("", ""), "-_")),
                              IpProtocol=protocol
                ))
        # 'セキュリティグループへのアウトバウンドルールの設定_宛先にセキュリティグループを指定'
        if len(SGEgressSG_FromPortList) > 1:
            for i,(pfrom,pto,sgid,protocol,distsgid) in enumerate(zip(SGEgressSG_FromPortList[1:],SGEgressSG_ToPortList[1:],SGEgressSG_GroupIdList[1:],\
                                                                      SGEgressSG_IpProtocolList[1:],SGEgressSG_DestinationSecurityGroupIdList[1:])):
                t.add_resource(SecurityGroupEgress(
                              "SecurityGroupEgressSG" + str(i),
                              FromPort=pfrom,
                              ToPort=pto,
                              GroupId=Ref(sgid.translate(string.maketrans("", ""), "-_")),
                              IpProtocol=protocol,
                              DestinationSecurityGroupId=Ref(distsgid.translate(string.maketrans("", ""), "-_"))
                ))
        # 作成したテンプレートファイルを整形
        json_template = t.to_json()
        # 保存先のｓ３バケットの指定と保存処理
        bucket = s3.Bucket(SAVE_BUCKET)
        obj = bucket.Object('json-template-' + BASENAME  + ' .txt')
        response = obj.put(
                       Body=json_template.encode('utf-8'),
                       ContentEncoding='utf-8',
                       ContentType='text/plane'
                    )
        print(json_template)
