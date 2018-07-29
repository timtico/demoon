
import logging
import logging.handlers
import sys

class StdErrFilter(logging.Filter):
    ''' log messages of level warning and error will be forwarded '''
    def filter(self, rec):
        return rec.levelno in (logging.ERROR, logging.WARNING)

class StdOutFilter(logging.Filter):
    ''' Only log messages of level info and debug will be forwarded
    to the stdout '''
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


class SplitLogger():
    ''' the methods in this class generate a Splitlogger
    in this logger all messages with level info and debug will
    be forwarded to the stdout, while all message of level warning
    and error will be forwarded to the stderr '''

    @classmethod
    def get_logger(cls, logger_name, facility = 'local3', address = '/dev/log'):
        ''' generates a logger with two streams. All loglevels of INFO or lower
        will be sent to the standard out, all messages of WARNING and higher 
        will be sent to standard error '''
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(module)s %(levelname)s: %(message)s')

        # add streaming handler for stdout
        h1 = logging.StreamHandler(sys.stdout)
        h1.setLevel(logging.DEBUG)
        h1.setFormatter(formatter)
        h1.addFilter(StdOutFilter())
        logger.addHandler(h1)

        # add streaming handler for stderr
        h2 = logging.StreamHandler(sys.stderr)
        h2.setLevel(logging.WARNING)
        h2.setFormatter(formatter)
        h2.addFilter(StdErrFilter())
        logger.addHandler(h2)

        syslog_handler = logging.handlers.SysLogHandler(facility= facility, address= address)
        logger.addHandler(syslog_handler)
        return logger
