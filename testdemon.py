from daemon import Daemon
import sys
import time

class TestDemon(Daemon):
    def __init__(self, *args, **kwargs):
        Daemon.__init__(self, *args, **kwargs)

    def run(self):
        pass 
        # while True:
        #     self.logger.info("Hello World")
        #     time.sleep(10)
