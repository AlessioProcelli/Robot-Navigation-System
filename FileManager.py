#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:53:45 2023

@author: alessio
"""
import numpy as np
import os
from shutil import copyfile
FOLDER_PATH="static/images/scans"
class FileManager:
    def __init__(self):
        self.folder_path = FOLDER_PATH

    def save_3d_image(self, image_data,filename):
        if not os.path.exists(self.folder_path):
            print("path not exist")  
            os.makedirs(self.folder_path)
            print("folder created")   
        destination_path = os.path.join(self.folder_path, filename)

        np.save(destination_path, image_data)
        print("Image saved to: {destination_path}")

        #print("Image saved to: {destination_path}")

# Example usage

