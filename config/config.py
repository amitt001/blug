from configparser import ConfigParser


class Configuration:
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read('config/setup.cfg')
