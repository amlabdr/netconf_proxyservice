from config.config import Config
from parser.parser import Parser
from netconf.mgmt_netconf import Mgmt_netconf
import os,json, time
from threading import Thread

TOKEN = ''

def mgmt_restconf():
    print("restconfprotocole")
    None
def mgmt_gnmi():
    print("gnmiprorocole")
    None

def controllerAuthentication(conf_file_contents):
    global TOKEN
    while True:
        print('controllerAuthentication')
        time.sleep(int(conf_file_contents['CONTROLLER_AUTH']['authentication_periode']))
        


def collectConfig():
    while(True):
        network_state = {}
        devicesConfig = open('config/devices.json', 'r')
        devicesConfigData = json.load(devicesConfig)
        devicesConfig.close()
        cfg.__init__()
        for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
            try:
                match devicesConfigData[device]["management_protocol"]:
                    
                    case "netconf":
                        config = mgmt_netconf.get_all_config(devicesConfigData[device])
                        #jsonDeviceConfig = parser.config2json(config)
                        dictDeviceConfig = parser.config2dict(config)
                        network_state[device]=dictDeviceConfig

                        


                    

            except:
                print("Error in collecting data for ",device)
            
        with open("%s.json" %"network_state", 'w') as json_file:
            
            json_file.write(json.dumps(network_state,indent=4))
            json_file.close()
        print("done")
        time.sleep(10)

        







if __name__ == '__main__':
    cfg = Config()
    parser = Parser()
    mgmt_netconf = Mgmt_netconf()
    Thread(target=controllerAuthentication, args=(cfg.conf_file_contents,)).start()
    Thread(target=collectConfig,).start()