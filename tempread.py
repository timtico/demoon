#!/usr/bin/env python3
""" Read HDD Temperatures """
import subprocess
import sys
import re 
import logging

class HDTemperature():
    """
    Read the temperature of one or more harddrives in degrees Celcius.
    It facilitates the hddtemp binary.

    :param hdd_list: A list of harddrive locations 
    """
    def __init__(self, hdd_list, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.re_hddtemp = re.compile(".+?\:.+?\:\s(\d\d)")
        self.hdd_list = hdd_list
        self.hddtemp_bin = self.get_hddtemp_bin()
    
    def get_hddtemp_bin(self):
        """
        Use linux which to determine if and where the hddtemp binary is installed
        Exit if hddtemp is not installed. 
        """
        try:
            location = subprocess.check_output(["/usr/bin/which", "hddtemp"])
            return location.strip()
        except subprocess.CalledProcessError:
            print("hddtemp could not be found, make sure you installed hddtemp")
            sys.exit(1)

    def run_hddtemp(self):
        """
        Execute the hddtemp binary using a list of hdd locations as arguments

        :returns: list of temperature values (integers)
        """
        args = [self.hddtemp_bin] + self.hdd_list + ['--numeric']
        response =  subprocess.check_output(args).splitlines()
        return [int(l.strip().decode("utf-8")) for l in response]

    def get_max_temp(self):
        """
        Take the temperature a list of hdds, return the maximum value in this list

        :returns: Maximum value of the hdd temperatures
        :rtype: int
        """
        temps = self.run_hddtemp()
        return max(temps)

if __name__ == '__main__':
    hd = HDTemperature(['/dev/sdc', '/dev/sdc1'], 'tempread')
    print(hd.get_max_temp())

