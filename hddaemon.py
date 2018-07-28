#!/usr/bin/env python3

from daemon import Daemon
import fancontrol
import tempread

class HDDaemon(Daemon):
    def __init__(self, config_file, *args, **kwargs):
        #Daemon.__init__(self, *args, **kwargs)
        #control = hddcontrol.HDDDaemon 
        super(HDDDaemon, self).__init__(*args, **kwargs)
        self.configuration = self.parse_config(config_file)
        self.temp_control = hddcontrol.HDDTemperature(self.configuration) 
        self.temp_reader =  

    def parse_config(self, config_file):
        """
        Parse the configuration file and return it as a dictionary
        The keys and values of the dictionary are encoded to UTF-8
        """ 
        parser = configparser.ConfigParser()
        with open(config_file) as f:
            config_string = '[top]\n' + f.read()
        parser.read_string(config_string.decode("UTF-8"))
        return {k.encode("utf-8") : v.encode("utf-8") for k,v in dict(parser['top']).items()}
    
    def run(self):
        pass
        
