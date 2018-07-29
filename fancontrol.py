#!/usr/bin/env python3

import os
import logging

class FanControl():
    """
    Read the (average) temperature of a range of harddrives

    :param config: configuration dictionary
    """
    def __init__(self, config, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.configuration = config
        self.current_pwm = 0
        self.pwm_address = os.path.join("/sys/class/hwmon/", str(self.configuration['fan_address']))
        self.logger.info("Controlling fan with pwm: {}".format(self.pwm_address))
        self.mintemp = float(self.configuration['mintemp'])
        self.maxtemp = float(self.configuration['maxtemp'])
        self.minstop = int(self.configuration['minstop'])
        self.minstart = int(self.configuration['minstart'])
        self.maxpwm = int(self.configuration['maxpwm'])


    def set_pwm(self,pwm_value):
        """
        Write the pwm value to the pwm file
        """
        with open(self.pwm_address, 'w') as pwm:
            pwm.write(str(pwm_value))
        self.current_pwm = pwm_value

    def decide_on(self, temp):
        """
        Given a temperature, decide if the fan should
        be off or on. If on, return True
        """
        return float(temp) > self.maxtemp

    def stop_fan(self):
        """
        stop the fan from spinning 
        """
        self.set_pwm(self.minpwm)

    def start_fan(self):
        """
        start finning the fan 
        """
        self.set_pwm(self.maxpwm)
        
    def adjust_to_temp(self, temp):
        """
        adjust the pwm to the given temperature,
        start or stop the fan if necessary
        """
        if self.decide_on(temp):
            if self.current_pwm != self.maxpwm:
                self.start_fan()
        else:
            self.stop_fan()

if __name__ == '__main__':
    h = FanControl('./config/hddaemon.conf')
    h.adjust_to_temp(60)
    print(h.current_pwm)
    



