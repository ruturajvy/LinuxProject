#!/usr/bin/python
import subprocess
import os

var_arr = []
with open('inputfile.txt') as my_file:
    for line in my_file:
        var_arr.append(line.split(":")[1].rstrip("\n\r"))

router = var_arr[4]
output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' "+router, stdout=subprocess.PIPE, shell=True)
(out, err) = output.communicate()
pid_r = out.rstrip("\n\r")
i=1
j=2
pubnet = var_arr[3].split(".")
public_network = pubnet[0]+ '.' + pubnet[1] + '.' + pubnet[2]

prinet = var_arr[2].split(".")
private_network = prinet[0]+ '.' + prinet[1] + '.' + prinet[2]

#connecting router with public network
os.system("sudo ip link add pub1 type veth peer name veth2")
port1 = "eth"+str(i)
port2 = "eth"+str(j)
os.system("sudo docker exec -i -t "+router+" yum update")
os.system("sudo docker exec -i -t "+router+" yum -y install iproute")
os.system("sudo ip link set dev veth2 netns "+pid_r+" name "+port1+" up")
os.system("sudo brctl addif "+var_arr[1]+" pub1")
os.system("sudo ip link set pub1 up")
os.system("sudo docker exec -i -t "+router+" ip route del default")
os.system("sudo docker exec -i -t "+router+" ip addr add "+public_network+".2/24 dev "+port1)
os.system("sudo docker exec -i -t "+router+" ip route add default via "+public_network+".1 dev "+port1)

#connecting router with private network
os.system("sudo ip link add priv1 type veth peer name veth2")
os.system("sudo ip link set dev veth2 netns "+pid_r+" name "+port2+" up")
os.system("sudo brctl addif "+var_arr[0]+" priv1")
os.system("sudo ip link set priv1 up")
os.system("sudo docker exec -i -t "+router+" ip addr add "+private_network+".1/24 dev "+port2)

cont_list = var_arr[5].split()
c=2
for cont in cont_list:
        output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' "+cont, stdout=subprocess.PIPE, shell=True)
        (out, err) = output.communicate()
        pid1 = out.rstrip("\n\r")
        int_name = "priv"+str(c)
        os.system("sudo ip link add "+int_name +" type veth peer name veth2")
        port = "eth1"
        os.system("sudo docker exec -i -t "+cont+" yum update")
        os.system("sudo docker exec -i -t "+cont+" yum -y install iproute")
        os.system("sudo ip link set dev veth2 netns "+pid1+" name "+port+" up")
        os.system("sudo brctl addif "+var_arr[0]+" "+int_name)
        os.system("sudo ip link set "+int_name+" up")
        os.system("sudo docker exec -i -t "+cont+" ip addr add "+private_network+"."+str(c)+"/24 dev "+port)
        os.system("sudo docker exec -i -t "+cont+" ip route del default")
        os.system("sudo docker exec -i -t "+cont+" ip route add default via "+private_network+".1 dev "+port)
        c=c+1

