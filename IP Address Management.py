import ipaddress
from pprint import pprint

'''
https://docs.python.org/3/howto/ipaddress.html#networks-as-lists-of-addresses
'''
class Subnet:
    def __init__(self,subnet_range,subnet_mask,subnet_gateway, subnet_desc):
        self.subnet=ipaddress.ip_network(f'{subnet_range}/{subnet_mask}', strict=False)   #ipaddress.IPv4Network
        self.gateway=ipaddress.ip_address(subnet_gateway)   #ipaddress.IPv4Address
        self.desc=subnet_desc
        self.h=0
        self.range=f"{self.subnet[1]} TO {self.subnet[-2]}"
        self.hosts=[]

    def addHost(self,ip_address):
        if ip_address in self.hosts:
            print(f"HOST {ip_address} ALREADY EXISTS")
        elif ip_address not in [str(host) for host in list(self.subnet.hosts())]:
            print(f"IP ADDRESS {ip_address} IS OUT OF RANGE ({self.range})")
        else:
            self.h+=1
            self.hosts.append(ip_address.strip())
            self.hosts.sort()

    def addHosts(self,ip_addresses):
        for ip in ip_addresses:
            if ip in self.hosts:
                print(f"HOST {ip} ALREADY EXISTS")
            elif ip not in [str(host) for host in list(self.subnet.hosts())]:
                print(f"IP ADDRESS {ip} IS OUT OF RANGE ({self.range})")
            else:
                self.hosts.append(ip.strip())
                self.h+=1
                self.hosts.sort()

    def delHost(self,ip_address):
        if ip_address not in self.hosts:
            print(f"HOST {ip_address} CANNOT BE DELETED. IT IS UNUSED")
        else:
            self.h-=1
            self.hosts.remove(ip_address)
            self.hosts.sort()

    def delHosts(self, ip_addresses):
        for ip in ip_addresses:
            if ip not in self.hosts:
                print(f"HOST {ip} CANNOT BE DELETED. IT IS UNUSED")
            else:
                self.hosts.remove(ip.strip())
                self.h-=1
                self.hosts.sort()

    def updateHost(self,old_ip,new_ip):
        if old_ip not in self.hosts:
            print("HOST CANNOT BE MODIFIED. HOST DOESN'T EXIST")
        elif new_ip not in [str(host) for host in list(self.subnet.hosts())]:
            print(f"NEW IP ADDRESS {new_ip} IS OUT OF RANGE ({self.range})")
        else:
            self.hosts.remove(old_ip)
            self.hosts.append(new_ip)
            self.hosts.sort()

    def isFree(self,ip_address):
        if ip_address not in self.hosts:
            return True
        else:
            return False

    def __str__(self):
        return f"SUBNET: {self.subnet}\nGATEWAY: {self.gateway}\nDESCRIPTION: {self.desc}\nRANGE: {self.range}\nNUMBER OF HOSTS: {self.h}\nUSED ADDRESSES:\n{self.hosts}"

class Network():
    def __init__(self):
        self.s=0
        self.subnets={}

    def addSubnet(self,subnet_range,subnet_mask,subnet_gateway, subnet_desc):
        self.subnet=Subnet(subnet_range,subnet_mask,subnet_gateway, subnet_desc)
        self.subnets[str(self.subnet.subnet)]={"DESCRIPTION":str(self.subnet.desc),"RANGE":str(self.subnet.range)}
        self.s+=1
        return self.subnet

    def delSubnet(self,subnet):
        try:
            del(self.subnets[str(ipaddress.ip_network(subnet))])
            self.s-=1
            print("DELETED")
            return True
        except KeyError:
            print("SUBNET CANNOT BE DELETED. SUBNET DOESNT EXIST")
            return False

    def isFree(self,subnet):
        subnet=ipaddress.ip_network(subnet,strict=False)
        for sub in self.subnets.keys():
            sub=ipaddress.ip_network(sub, strict=False)
            if (set(subnet.hosts()) & set(sub.hosts())):
                return False
            else:
                return True

    def __str__(self):
        return f"THERE ARE CURRENTLY {self.s} SUBNETS CONFIGURED ON THIS NETWORK:\n{pprint(self.subnets)}"




## Testing block:
building_c=Network()

it=building_c.addSubnet("10.20.221.10","25","10.20.221.1", "IT Department")
mkt=building_c.addSubnet("192.168.20.128","26","192.168.20.128", "Marketing Department")
guests=building_c.addSubnet("172.20.0.0","24","172.20.0.1","For Guests")

print(building_c)
print("\n")

print(it)
print("\n")

print(building_c.isFree("10.20.221.5/28"))
print(building_c.isFree("10.30.221.5/28"))

print("\n")
print(it.isFree("10.20.221.50"))
it.addHost("10.20.221.50")
print(it.isFree("10.20.221.50"))

print("\n")
it.addHosts(["10.20.221.1","10.20.221.2","10.20.221.3","10.20.221.4"])
it.addHost("10.20.221.1")
it.addHosts(["10.20.221.3","10.20.221.4","10.20.221.5","10.20.221.6"])
print(it)

print("\n")
it.delHost("10.20.221.1")
print(it.hosts)
it.updateHost("10.20.221.2","10.20.221.1")
print(it.hosts)

print("\n")
pprint(building_c.subnets)
building_c.delSubnet(guests.subnet)
pprint(building_c.subnets)
