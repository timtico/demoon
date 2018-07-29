#!/usr/bin/env python3

''' Class that lets a python script run in demon mode
The code is taken and modified from `A simple unix/linux 
daemon in Python '''
import sys
import os
import time
import atexit
import signal
import logger

class Daemon:
    ''' generic daemon class
    usage: subclass and override the run() method '''

    def __init__(self, logger_name = '__name__', pid_file = None):
        if not pid_file:
            self.pidfile = os.path.join("/run/lock/", type(self).__name__ + ".lock")
        else:
            self.pidfile = pid_file
        self.logger = logger.SplitLogger.get_logger(logger_name)

    def fork(self, n):
        ''' performs a fork, this should be done twice when daemonizing. 
        double forking is done in order to dissociate the daemon from 
        parents and preventing it from acquiring a controlling terminal '''
        try:
            pid = os.fork()
            if pid > 0:
                # exiting the first parent
                sys.exit()
        except OSError as e:
            self.logger.warning("fork #{} failed: {}\n".format(n, e))
            sys.exit(1)

    def redirect_file_descriptors(self):
        ''' redirects standard file descriptors. the daemon should not
        hold open any file descriptors that are inherited from the parent.
        file descriptors will be opened to /dev/null '''
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        # duplicate the file descriptors
        # and closes the previous ones
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

    def write_pidfile(self, pid):
        ''' writes a pidfile that contains the pid id in '''
        self.logger.info("Creating lockfile {}".format(self.pidfile))
        with open(self.pidfile, 'w+') as f:
            self.logger.info("creating pidfile with pid {}".format(pid))
            f.write(pid + '\n')

    def delete_pidfile(self):
        ''' deletes the pidfile '''
        os.remove(self.pidfile)

    def daemonize(self):
        # first fork
        self.fork(1)

        # change the current working directory to /
        # this in order to make sure the daemon does
        # not prevent unmounting of a filesystem
        os.chdir("/")

        # create a new session
        os.setsid()

        # setting the umask. Some sources advice against
        # setting to zero means that files will be 666
        # (world writable) and directories will be 777
        os.umask(0)

        # second fork
        self.fork(2)

        pid = str(os.getpid())
        self.logger.info("{} daemon (pid={})".format(type(self).__name__, pid))

        # write pidfile
        self.write_pidfile(pid)

        # redirect file descriptors
        self.redirect_file_descriptors()

        # register function to be executed at termination
        # the pidfile should be deleted on exiting
        atexit.register(self.delete_pidfile)



    def read_pidfile(self):
        ''' Check for a pidfile. If pidfile exists it is returned
        else None is returned '''
        try:
            with open(self.pidfile) as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        return pid

    def start(self):
        ''' starting the demon. If pidfile already exists
        a new demon instance will not be started '''
        pid = self.read_pidfile()
        self.logger.info("starting {} daemon".format(type(self).__name__, pid))

        if pid:
            self.logger.warning(
                "pidfile {} already exists, assuming daemon is already running, exiting".format(self.pidfile))
            sys.exit(1)

        self.daemonize()
        self.run()

    def stop(self):
        ''' Check if the daemon is running if it's running kill it '''
        pid = self.read_pidfile()
        self.logger.info("stopping {} daemon (pid={})".format(type(self).__name__, pid))

        if not pid:
            self.logger.warning(
                "pidfile {} does not exists, assuming daemon is not running, exiting".format(self.pidfile))
            return

        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                self.logger.warning(str(e.args))
                sys.exit()

    def restart(self):
        ''' restarting is nothing more than a stop and a start '''
        self.stop()
        self.start()

    def run(self):
        ''' overwrite this method to create your own daemon. it 
        will be called after the demon is started or restarted '''
        pass
