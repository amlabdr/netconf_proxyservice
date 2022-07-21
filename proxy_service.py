from config.config import Config
import os,json, time
from threading import Thread

TOKEN = ''
def mgmt_netconf():
    print("netconfprotocole")

    None
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
        devicesConfig = open('config/devices.json', 'r')
        devicesConfigData = json.load(devicesConfig)
        devicesConfig.close()
        cfg.__init__()
        for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
            try:
                match devicesConfigData[device]["management_protocol"]:
                    case "netconf":
                        mgmt_netconf()
                    case "restconf":
                        mgmt_restconf()
                    case "gnmi":
                        mgmt_gnmi()
                    case default:
                        print("invalid protocol")

                
            except:
                print(device,"'s management_protocol unknown")
        time.sleep(10)

        







if __name__ == '__main__':
    cfg = Config()
    Thread(target=controllerAuthentication, args=(cfg.conf_file_contents,)).start()
    Thread(target=collectConfig,).start()