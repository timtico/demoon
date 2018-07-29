import configparser

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
