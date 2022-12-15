from ncclient import manager
import xml.etree.ElementTree as ET
import json
import xmltodict

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

cassini_switch = {"host":"10.11.200.18",
                    "port":"830",
                    "username":"ocnos",
                    "password":"ocnos"}
with manager.connect_ssh(host=cassini_switch["host"],port = cassini_switch["port"],username = cassini_switch["username"],password = cassini_switch["password"],hostkey_verify= False) as m:
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
