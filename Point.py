#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 11:43:47 2023

@author: alessio
"""

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def print_values(self):
        print("x value: "+ str(self.x)+"   y value: "+ str(self.y) )
        
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y
        }