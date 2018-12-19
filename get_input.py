#!/usr/bin/python

var_arr = []
with open('inputfile.txt') as my_file:
    for line in my_file:
        var_arr.append(line.split(":")[1].rstrip("\n\r"))

file =open('vars_file.yaml','a')
file.write("privatenet:\n")
file.write(" name: "+var_arr[0]+"\n")
file.write(" subnet: "+var_arr[2]+"\n")

pubnet = var_arr[3].split(".")
public_network = pubnet[0]+ '.' + pubnet[1] + '.' + pubnet[2]

file.write("publicnet:\n")
file.write(" name: "+var_arr[1]+"\n")
file.write(" subnet: "+var_arr[3]+"\n")
file.write(" ip: "+public_network+'.1\n')

prn = var_arr[2].split(".")
priv_network = prn[0]+ '.' + prn[1] + '.' + prn[2]

file.write("public_container_names:\n")
file.write(" name: "+var_arr[4]+"\n")


file.write("priv_container_names:\n")
name_list = var_arr[5].split()
n=len(name_list)
for i in name_list:
        file.write(" - "+i+"\n")

grenet = var_arr[8].split(".")
gre_network = grenet[0]+ '.' + grenet[1] + '.' + grenet[2]

file.write("connection:\n")
file.write(" name: connection"+var_arr[12]+"\n")
file.write(" publicip: "+var_arr[10]+"\n")
file.write(" tunneldst: "+var_arr[10]+"\n")
file.write(" privatenet: "+var_arr[2]+"\n")
file.write(" vpnconnname: "+var_arr[7]+"\n")
file.write(" vpnpass: "+var_arr[11]+"\n")
file.write(" tunnelhubip: "+gre_network+".2\n")
file.write(" tunnelspokeip: "+gre_network+".1\n")
