import socket
import os
# import wmi

def check_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()
        print(ip)
    finally:
        s.close()

def check_local_gateway():
    routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]

def check_local_interface():
    ifs = netifaces.interfaces()
    ips = list()
    for _if in ifs:
        _d = netifaces.ifaddresses(_if)
        if 2 in _d.keys():
            for i in _d[2]:
                ips.append([i['addr'], i['netmask']])
    print(ips)


def check_interface_info_wmi():
    tmplist = []
    c = wmi.WMI()
    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
        tmpdict = {}
        tmpdict["Description"] = interface.Description
        tmpdict["IPAddress"] = interface.IPAddress[0]
        tmpdict["IPSubnet"] = interface.IPSubnet[0]
        tmpdict["MAC"] = interface.MACAddress
        tmplist.append(tmpdict)
    for i in tmplist:
        for interfacePerfTCP in c.Win32_PerfRawData_Tcpip_TCPv4():
            print('\t' + 'TCP Connect :\t' + str(interfacePerfTCP.ConnectionsEstablished))


if __name__ == '__main__':
    check_local_interface()