import socket
import ipaddress
import subprocess
import sys
import os

host = socket.gethostname()
ip   = socket.gethostbyname(host)
ip2  = socket.gethostbyname_ex(host)

print(host)
print(ip)
print(ip2)

cmd = "./get_ipaddr.sh"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
o, e = p.communicate()
lines = o.decode().split('\n')
for line in lines:
    if '127.0.0.1' in line:
        continue
    if ':' in line:
        continue
    print (line)

