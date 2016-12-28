# -*- coding: utf-8 -*-
import ConfigParser

from b5c_interface.Log import Log


class BaseMode:
    def __init__(self):
        self.log = Log()
        self.cf = ConfigParser.ConfigParser()


