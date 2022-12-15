import xmltodict,json

class Parser:
    def __init__(self):
        pass
    def config2xml(self,config):
        return(config.xml)
    def config2json(self,config):
        data_dict = xmltodict.parse(self.config2xml(config))
        json_data = json.dumps(data_dict,indent=4)
        return(json_data)
    def config2dict(self,config):
        data_dict = xmltodict.parse(self.config2xml(config))
        return(data_dict)
