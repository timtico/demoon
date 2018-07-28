#!/usr/bin/env python3

from daemon import Daemon
import subprocess

class HDDDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        Daemon.__init__(self, *args, **kwargs)

    def run(self):
        pass
        
