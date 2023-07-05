#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 17:52:59 2023

@author: alessio
"""

import json
CONFIG_FILE="static/config/config.json"
class ConstantManager:
    def __init__(self):
        self.constants = self.load_constants(CONFIG_FILE)

    def load_constants(self, config_file):
        with open(config_file) as file:
            constants = json.load(file)
        return constants

    def get_constant(self, constant_name):
        return self.constants.get(constant_name)

    def set_constant(self, constant_name, constant_value):
        self.constants[constant_name] = constant_value



