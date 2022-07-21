import logging
import os
import configparser

class Config:
    def __init__(self):
        self.conf_file_path = os.environ.get('CONF_FILE',"config/config.ini")
        self.conf_file_contents = self.read_config()

    def read_config(self):
        # open config file
        try:
            config = configparser.ConfigParser()
            config.read(self.conf_file_path)
            config.sections()
            return config
        except IOError:
            logging.critical("*********** ERROR reading config file **********")
            exit(1)
