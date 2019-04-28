#!/usr/bin/env ML
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 22:25:06 2018

@author: prashant
"""

import os
from PIL import Image

# Confogration 

classes = ["a", "b", "d", "g"]
label_base_path = "Labels"
output_base_path = "Output"
image_base_path = "Images"

try:
    os.makedirs(output_base_path)
except:
    print('Path "'+output_base_path+'" Already exist... Overwriting !!!')

class Convert:
    """Convert"""
    def __init__(self, image_folder, label_folder, output_folder, classes):
        self.label_folder = label_folder
        self.classes = classes
        self.image_folder = image_folder
        self.output_folder = output_folder
        self.img_ext = '.jpg'
    
    def yolo_convertor(self,):        
        for root, dirs, files in os.walk(self.label_folder):
            for file in files:
                with open(root + os.sep + file, 'r') as file_content:
                    content = file_content.readlines()
                    out_dir = self.output_folder + root[len(self.label_folder):] + os.sep 
                    print(out_dir)
                    if not os.path.exists(out_dir):
                    	os.makedirs(out_dir)
                    out_stream = open(out_dir + file, 'w+')
                    for line in content:
                        points = line.split()
                        if len(points) == 5:
                            cl = self.classes.index(points[4])
                            xmin = points[0]
                            xmax = points[2]
                            ymin = points[1]
                            ymax = points[3]
                            file_name = file.split('.')[0]
                            img_path = self.image_folder + root[len(self.label_folder):] + os.sep + file_name + self.img_ext
                            img = Image.open(img_path)
                            w= int(img.size[0])
                            h= int(img.size[1])
                            b = (float(xmin), float(xmax), float(ymin), float(ymax))
                            # print((w,h), b)
                            bb = self.__scale_convert((w,h), b)
                            # print(bb)

                            print(out_dir + file)

                            if not os.path.exists(out_dir):
                                os.makedirs(out_dir)

                            out_stream.write(str(cl) + " " + " " + " ".join([str(a) for a in bb]) + '\n')
                    out_stream.close()
                print("-----------------------------------")

    def __scale_convert(self, size, box):
        dw = 1./size[0]
        dh = 1./size[1]
        x = (box[0] + box[1])/2.0
        y = (box[2] + box[3])/2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x,y,w,h)


c = Convert(image_base_path, label_base_path, output_base_path, classes)
c.yolo_convertor()
