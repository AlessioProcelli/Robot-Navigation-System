#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 18:04:36 2023

@author: alessio
"""
import time
import random

class CriticalPoint:
    def __init__(self, point, is_visited,unique_id=0 ):
        if unique_id==0:
            self.unique_id=self.generate_unique_id()
        else:
            self.unique_id=unique_id
        self.point = point
        self.is_visited = is_visited

    def to_dict(self):
            return {
                'unique_id': self.unique_id,
                'point': self.point.to_dict(),
                'is_visited': self.is_visited
            }
            
    def generate_unique_id(self):
        timestamp = int(time.time() * 1000)  # Get current timestamp in milliseconds
        random_num = random.randint(0, 9999)  # Generate a random number between 0 and 9999
        unique_id = str(timestamp)+"-"+str(random_num)  # Combine timestamp and random number
        return unique_id