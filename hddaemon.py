#!/usr/bin/env python3

from daemon import Daemon
import fancontrol
import tempread
import config
import time

class HDDaemon(Daemon):
    def __init__(self, config_file, *args, **kwargs):
        super(HDDDaemon, self).__init__(*args, **kwargs)
        self.configuration = config.parse_config(config_file)
        self.fan_control = fancontrol.FanControl(self.configuration)
        self.temp_read = tempread.HDTemperature(self.configuration['disks'])
        self.interval = self.configuration['interval']

    def run(self):
        while True:
            max_t = self.temp_read.get_max_temp()
            self.fan_control.adjust_to_temp(max_t)
            time.sleep(self.interval)
            
