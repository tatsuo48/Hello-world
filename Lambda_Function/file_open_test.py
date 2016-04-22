#!/usr/bin/env python

f = open('text.txt', 'r')
line = f.readline()
CidrBlockList = line[:-1].split(',')    
print  CidrBlockList
line = f.readline()
EnableDnsSupportList = line[:-1].split(',') 
print  EnableDnsSupportList    
f.close
