f = open('/var/tmp/data.txt')
body = f.read()
parameter_list= body.splitlines()
for i in range(len(parameter_list)):
  resource =  parameter_list[i].split(',')
  a = str(resource[0])
  ns = locals()
  ns[a] = resource
print(Subnet_Az)

print(SGEgressSG_DestinationSecurityGroupId)
