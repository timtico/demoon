from testdemon import TestDemon
import sys

demon = TestDemon("/tmp/mydemon.pid")
demon.start()
sys.exit(0)
