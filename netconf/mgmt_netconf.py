from ncclient import manager

class Mgmt_netconf:
    def __init__(self):
        pass
    def get_all_config(self,device):
        with manager.connect_ssh(host=device["hostname"],port = device["port"],username = device["username"],password = device["password"],hostkey_verify= False) as m:
            cmd = "get"
            config = m.get()
            return(config)


