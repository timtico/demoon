#!/usr/bin/env python3

from daemon import Daemon
import fancontrol
import tempread
import config
import time
import logging
import sys

class HDDaemon(Daemon):
    def __init__(self, config_file, *args, **kwargs):
        self.logger = logging.getLogger('hddaemon')
        self.config_file = config_file
        self.configuration = config.parse_config(self.config_file)
        self.print_init()
        self.fan_control = fancontrol.FanControl(self.configuration, "hddaemon.fancontrol")
        self.disks = self.configuration['disks'].split()
        self.temp_read = tempread.HDTemperature(self.disks, "hddaemon.temp_read")
        self.interval = int(self.configuration['interval'])
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            max_t = self.temp_read.get_max_temp()
            self.fan_control.adjust_to_temp(max_t)
            time.sleep(self.interval)

    def print_init(self):
        """
        Print a initalization message showing all settings
        """
        self.logger.info("HDDaemon initialized")
        self.logger.info("config file: {}".format(self.config_file))
        for k,v in self.configuration.items():
            self.logger.info("{}={}".format(k,v))


if __name__ == '__main__':
    d = HDDaemon(config_file = './config/hddaemon.conf')

    if len(sys.argv) == 2:
        command = sys.argv[1]
        if command == 'start':
            d.start()
        elif command == 'stop':
            d.stop()
        elif command == 'restart':
            d.restart()
        sys.exit(0)


