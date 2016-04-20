from troposphere import Ref, Tags,Template
from troposphere.ec2 import VPC
import sys
params = sys.argv
t = Template()

t.add_version("2010-09-09")

t.add_description("""\
console. You will be billed for the AWS resources used if you create a stack \
from this template.""")


for i,address in enumerate(params):

    t.add_resource(VPC(
    "VPC"+str(i),
    EnableDnsSupport="true",
    CidrBlock=address,
    EnableDnsHostnames="true",
    Tags=Tags(
         Name="VPC"+str(i)
    )
    ))

print(t.to_json())