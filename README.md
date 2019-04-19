# VPN-as-a-Service-in-VPC
Team Members:

- Aparajita Bagchi
- Atmadeep Sen
- Ruturaj Vyawahare
- Vemulapalli Venkata Naga Sai Krishna

To provide VPN as a service in the Virtual Private Cloud requested by the client.

- Objective: To provide the service to a customer to enable him/her to have the ability to establish a secure connection (VPN tunnel) between their Virtual Private Cloud and their private datacenter network and with multiple VPC sites present on same or different provider hosts without depending on the VPC service provider(not using the default VPN gateway provided by the service provider).

- Introduction: VPC helps in the extension of the client’s data centre (connecting VPC to the corporate network). VPN(Virtual Private Network) can be used to provide a connection between the VPC and client data centre. The VPN service designed in this project would help the customer to control the traffic data path between the multiple VPC and customer private network.

- System Architecture: For private network(VPC) present on each host, a virtual VPN gateway is configured. The components of our system are as follows:

- Provider(Public) network: The network on which provider host resides of the VPC like AWS or Google. We implement this network using a VCL host running Ubuntu 16.04 LTS Base. Router-VM: This is the virtual private gateway which has one interface connected to the Virtual Private Cloud of the customer and one interface facing the internet. In our implementation, we use a Centos 7 VM as the Router VM.

- Private Subnet: This is the customer’s private network in the VPC. This is creating by adding a bridge-mode network and customer can configure VM’s as per his/her requirements and attach to this bridge-mode network. The router-VM’s IP address which is part of the customer’s private network is configured as the default gateway in these VM’s.

- Customer Private Network: This can be a private cloud or a physical data centre network of the customer. We have designed hub and spoke topology such that if the spoke VPC wants to communicate with hub VPC or the private customer(datacenter) network, it first goes to the hub and then hub forwards the traffic to the intended destination.VPN(IPSEC) tunnels are configured between the hub and all the spoke VPC’s and also between the hub and customer private network as shown in the picture above.In order to establish communication between VPC’s present on different hosts, a GRE tunnel is established. For the communication between them to be secure IPSec tunnel is established.
