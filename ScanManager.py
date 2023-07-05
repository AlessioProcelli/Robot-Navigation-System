#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:53:45 2023

@author: Alessio Procelli
"""


import numpy as np
import json
import Scan
import ConstantManager

class ScanManager:
    def __init__(self):

        self.cost_mng=ConstantManager.ConstantManager()
        self.folder_path =self.cost_mng.get_constant("FOLDER_PATH")
        
    def generate_2d_image(self,filename): 
        random_image = np.random.randint(0, 256, size=(60, 60), dtype=np.uint8)
        np.save(filename, random_image)

    def generate_3d_image(self, filename):
        random_image = np.random.randint(0, 256, size=(60, 60, 40), dtype=np.uint8)
        np.save(filename, random_image)
                
    def scanPoint(self,idstr):
        DATABASE_PATH=self.cost_mng.get_constant("DATABASE_PATH")
        DATABASE_FILE=self.cost_mng.get_constant("DATABASE_FILE")
        NAME_2D1=self.cost_mng.get_constant("NAME_2D1")
        NAME_2D2=self.cost_mng.get_constant("NAME_2D2")
        NAME_3D=self.cost_mng.get_constant("NAME_3D")
        EXTENSION=self.cost_mng.get_constant("EXTENSION")
        FOLDER_PATH=self.cost_mng.get_constant("FOLDER_PATH")
        
        with open(DATABASE_PATH+DATABASE_FILE, "a") as json_file:
            img_3d=FOLDER_PATH+idstr+NAME_3D+EXTENSION
            img_2d1=FOLDER_PATH+idstr+NAME_2D1+EXTENSION
            img_2d2=FOLDER_PATH+idstr+NAME_2D2+EXTENSION
            self.generate_3d_image(img_3d)
            self.generate_2d_image(img_2d1)
            self.generate_2d_image(img_2d2)
            data = {
                    idstr: {
                        "image3D": img_3d,
                        "image2D1":  img_2d1,
                        "image2D2": img_2d2,
                        
                        },
            }
            json.dump(data, json_file)
            json_file.write("\n")
    
    def findScan(self,idstr_target):
        DATABASE_PATH=self.cost_mng.get_constant("DATABASE_PATH")
        DATABASE_FILE=self.cost_mng.get_constant("DATABASE_FILE")
        with open(DATABASE_PATH+DATABASE_FILE, "r") as json_file:
            for line in json_file:
                # Parse each line as a JSON object
                data = json.loads(line)
                # Process the data if idstr is equal to id_target
                for idstr, values in data.items():
                    if idstr == idstr_target:
                        # Extract the values for the id_target
                        image3D = str(values.get("image3D"))
                        image2D1 =str( values.get("image2D1"))
                        image2D2 =str( values.get("image2D2"))                    
                        res=Scan.Scan(idstr,image3D,image2D1,image2D2)
                        return res



