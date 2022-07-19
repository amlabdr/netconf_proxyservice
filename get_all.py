from socket import socket
from ncclient import manager
import xml.etree.ElementTree as ET
import json
import os
import xmltodict
from paramiko import SSHClient, AutoAddPolicy


def exe_cmd(client,cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    output = ''
    status = 0
    for line in stdout.readlines():
        output += line
    for line in stderr.readlines():
        status=1
        output += line
    print(output)
    return status

xml_dict = {
    'interfaces':'<interfaces xmlns="http://openconfig.net/yang/interfaces"/>',
    'terminal-device':'<terminal-device xmlns="http://openconfig.net/yang/terminal-device"><logical-channels> </logical-channels></terminal-device>',
    'operational':'<components xmlns="http://openconfig.net/yang/platform"><component><name>OCH-2/1</name><optical-channel xmlns="http://openconfig.net/yang/terminal-device"><state><operational-mode/></state></optical-channel></component></components>',
    'optical-channel':'<components xmlns="http://openconfig.net/yang/platform"><component><name>OCH-2/1</name><optical-channel xmlns="http://openconfig.net/yang/terminal-device"><state><operational-mode/></state></optical-channel></component></components>'
}
paths={
    'frequency':'/terminal-device/logical-channels/channel[131074]/config/admin-state',
    'freq':'/terminal-device/coherent-module/network-interfaces/interface/config/frequency'
}
openconfig_paths={
    'frequency':'/components',
    'freq':'/terminal-device/coherent-module/network-interfaces/interface/config/frequency'
}

cassini_switch = {"host":"10.11.200.16",
                    "port":"830",
                    "username":"ocnos",
                    "password":"ocnos"}



client = SSHClient()
vm = SSHClient()
vm.set_missing_host_key_policy(AutoAddPolicy())

# load host ssh keys
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())

vm.connect(hostname = 'worker05.air.nvidia.com',
                port = 25453,
                username = 'cumulus',
                password='password',
                key_filename='config/simulation_key')

vmtransport = vm.get_transport()
dest_addr = ('spine01', 22) #edited#
local_addr = ('localhost', 22) #edited#
vmchannel = vmtransport.open_channel("direct-tcpip",dest_addr= dest_addr,src_addr= local_addr)
'''
client.connect(
                'spine01',
                username='admin',
                password='YourPaSsWoRd',
                sock=vmchannel)
exe_cmd(client,'hostname')
#print(stdout)
client.close()
'''

#with manager.connect_ssh(host=cassini_switch["host"],port = cassini_switch["port"],username = cassini_switch["username"],password = cassini_switch["password"],hostkey_verify= False,socket=vmchannel) as m:
with manager.connect_ssh(host='spine01',port = 830,username = 'admin',password = 'YourPaSsWoRd',hostkey_verify= False,sock=vmchannel) as m:
    cmd = "get"
    
    #config = m.get_config(source='running',filter=('subtree', xml_dict["optical-channel"])).xml
    #config = m.get(filter=('subtree', xml_dict['terminal-device'])).xml
    #config = m.get(filter=('xpath', openconfig_paths["frequency"])).xml
    config = m.get().xml
with open("%s.xml" %cmd, 'w') as f:
    f.write(config)
f.close()


data_dict = xmltodict.parse(config)
json_data = json.dumps(data_dict,indent=4)
with open("%s.json" %cmd, 'w') as json_file:
    json_file.write(json_data)
    json_file.close()
print("Done")


