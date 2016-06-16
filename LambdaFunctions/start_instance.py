#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import boto3

import pprint

TAG_KEY_AUTO_START = 'auto-start'


print('Loading function')

pp = pprint.PrettyPrinter(indent=4)

# 関数名 ： lambda_handler
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    ec2_client   = boto3.client('ec2')

    ret = execute_start_instance(ec2_client)
    print 'Start instance success(%s).' % (ret)

    return 0
    raise Exception('Something went wrong')

# 関数名 ： execute_start_instance
# 戻り値 ： 実行結果
# 引数　 ： ec2_client
#       ： ec2_resource
# 機能　 ： インスタンスを起動する。
def execute_start_instance(ec2_client):
    response = ec2_client.describe_instances()

    result = True
    for ec2_group in response['Reservations']:
        for instance_info in ec2_group['Instances']:
            ret = is_target(instance_info)
            
            if (ret == False):
                continue
            instance_id = instance_info.get('InstanceId')
            response = ec2_client.start_instances(InstanceIds=[instance_id,])
            print response
    return result

# 関数名 ： is_target
# 戻り値 ： 起動要否
# 引数　 ： instance_info <dict>
# 機能　 ： 起動要否を判定する
def is_target(instance_info):
    val = get_tag_value(
        instance_info,
        TAG_KEY_AUTO_START
    )

    if val is None:
        return False

    return True

# 関数名 ： get_tag_value
# 戻り値 ： タグ値（当該キーに合致するものがなければNone）
# 引数　 ： instance_info <dict>
#       ： key <str>
# 機能　 ： インスタンス情報から指定キーのタグ値を取得する
def get_tag_value(instance_info, key):
    tags = instance_info.get('Tags')
    if tags == None:
        return None

    for tag in tags:
        if not (key == tag['Key']):
            continue

        tag_value = tag['Value']
        if tag_value == "true":
            return True

    return None

