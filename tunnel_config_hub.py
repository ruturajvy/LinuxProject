#!/usr/bin/python
import subprocess
import os
import time

var_arr = []
with open('inputfile.txt') as my_file:
    for line in my_file:
        var_arr.append(line.split(":")[1].rstrip("\n\r"))

router = 'httpd'

tunnel_name = var_arr[7]
grenet = var_arr[8].split(".")
gre_network = grenet[0]+ '.' + grenet[1] + '.' + grenet[2]
tunnel_src = '20.1.1.2'
tunnel_dst = var_arr[10]
os.system("sudo docker exec -i -t "+router+" modprobe ip_gre")
os.system("sudo docker exec -i -t "+router+" modprobe nf_nat_proto_gre")
os.system("sudo docker exec -i -t "+router+" modprobe nf_conntrack_proto_gre")
os.system("sudo docker exec -i -t "+router+" ip tunnel add "+tunnel_name+" mode gre remote "+tunnel_dst+" local "+tunnel_src+" ttl 255")
os.system("sudo docker exec -i -t "+router+" ip link set "+tunnel_name+" up")
os.system("sudo docker exec -i -t "+router+" ip addr add "+gre_network+".2/24 dev "+tunnel_name)
os.system("sudo iptables -t nat -A PREROUTING -i eth1 -s "+tunnel_dst+" -j  DNAT --to-destination "+tunnel_src)

network = var_arr[2]
os.system("sudo docker exec -i -t "+router+" ip route add "+network+" via "+gre_network+".1 dev "+var_arr[7])

os.system("sudo modprobe ip_gre")
os.system("sudo modprobe nf_nat_proto_gre")
os.system("sudo modprobe nf_conntrack_proto_gre")

os.system("sudo docker exec -i -t "+router+" yum -y install openswan")
os.system("sudo docker exec -i -t "+router+" yum -y install sysvinit-tools")
f= open("ipsec_script.bash","w+")
f.write("#!/bin/bash\n")
f.write("cat <<EOT >> /etc/ipsec.conf\n")
f.write("conn "+tunnel_name+"\n")
f.write("\tauthby=secret"+"\n")
f.write("\tauto=start\n")
f.write("\ttype=tunnel\n")
f.write("\tleft="+gre_network+".2\n")
f.write("\tleftid="+gre_network+".2\n")
f.write("\tleftsubnet="+var_arr[9]+"\n")
f.write("\tright="+gre_network+".1\n")
f.write("\trightsubnet="+var_arr[2]+"\n")
f.write("\tike=aes256-sha1;modp2048\n")
f.write("\tphase2=esp\n")
f.write("\tphase2alg=aes256-sha1;modp2048\n")
f.write("EOT\n\n")
f.write("cat <<EOT >> /etc/ipsec.secrets\n")
f.write("%any %any : PSK "+var_arr[11]+"\n")
f.write("EOT\n\n")
f.write("iptables -A INPUT -p udp --dport 500 -j ACCEPT\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/default/send_redirects\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/default/accept_redirects\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/all/send_redirects\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/all/accept_redirects\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/all/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/default/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/eth1/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/eth0/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/eth2/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/gre0/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/"+tunnel_name+"/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/gretap0/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/ip_vti0/rp_filter\n")
f.write("echo 0 > /proc/sys/net/ipv4/conf/lo/rp_filter\n")
f.close()
f=None
os.system("sudo docker cp ipsec_script.bash "+router+":/ipsec_script.bash")
os.system("sudo docker exec -i -t "+router+" bash ipsec_script.bash")
os.system("sudo docker exec -i -t "+router+" ipsec start")
os.system("sudo docker exec -i -t "+router+" ipsec restart")
