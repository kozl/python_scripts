#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 12:23:08 2013

@author: q
"""

from PIL import Image
import os, os.path
from re import match
from shutil import copy
from optparse import OptionParser

def convert_image(src_path,dst_path,height):
    if match(r".*\.[jJ][pP][gG]$", os.path.basename(src_path)):
        try:
            im_src=Image.open(src_path)
            im_dst=im_src
            if im_src.size[1]>height:            
                size_ratio=float(im_src.size[0])/float(im_src.size[1])
#               print('''
#               Image: %s
#               size: %dx%d
#               size_ratio: %f
#               new size: %dx%d
#               ''' % (src_path, im_src.size[0], im_src.size[1], size_ratio, 1600, int(1600/size_ratio)))
                im_dst=im_src.resize((height,int(height/size_ratio)))
            im_dst.save(dst_path)
            print("%s -> %s" % (src_path, dst_path))
            return 1
        except:
            print("Can't process image file %s" % src_path)
            return 0
    else:
        copy(src_path,dst_path)
        return 0

parser=OptionParser(description="Script for copying tree of photo images and resizing them",
                    usage="usage: %prog [options] src_dir dst_dir")
parser.add_option("--height",
                  dest="height",
                  type="int",
                  default=1920,
                  help="Height of converted JPEG files")

(options, args) = parser.parse_args()

file_counter=0
input_dir=os.path.abspath(args[0])
output_dir=os.path.abspath(args[1])
height=options.height
for root,dirs,files in os.walk(input_dir):
    files=filter(lambda x: os.path.isfile(x),map(lambda x: os.path.join(root,x),files))
    for src_file in files:
        src_file=os.path.join(root,src_file)
        dst_file=os.path.join(output_dir, os.path.relpath(src_file,input_dir))
        dst_dir=os.path.dirname(dst_file)
        if not os.path.exists(dst_dir): os.makedirs(dst_dir, mode=0755)        
        file_counter+=convert_image(src_file,dst_file,height)        
print(
'''
+++++++++++++++++++++++++++++
%d images sucessfully resized
+++++++++++++++++++++++++++++
''' % file_counter)