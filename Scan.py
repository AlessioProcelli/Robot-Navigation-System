#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 18:28:31 2023

@author: Alessio Procelli
"""
import numpy as np

class Scan:
    def __init__(self,idstr,img_3d,img_2d1,img_2d2):
        self.idstr=idstr
        self.img_3d=img_3d
        self.img_2d1=img_2d1
        self.img_2d2=img_2d2
        
    def load_3d_image(self):
        data = np.load(self.img_3d)
        return data
    def load_2d1_image(self):
        data = np.load(self.img_2d1)
        return data
    def load_2d2_image(self):
        data = np.load(self.img_2d2)
        return data