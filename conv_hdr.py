from __future__ import print_function
from __future__ import division
from PIL import Image
import cv2 as cv
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
from fractions import Fraction

###variables setting ###############
#image size
imgH = 3648 
imgW = 7296
#fisheye radius
imgR = 1725
#fisheye center
c1_x = 1825
c1_y = 1825
c2_x = 5500
c2_y = 1825
#conversion matrix
RX = 133.1042
GX = 90.39311
BX = 65.21242
RY = 72.39415
GY = 204.0351
BY = 34.29615
RZ = 7.149386
GZ = 41.19635
BZ = 296.3546
#Range of RGB values to convert
TH_H = 200
TH_L = 20
####################################

#Load images and integration
def makeHDRimage(path):
    #initialize matrix
    hdr_img = []
    summed_Rimg = np.zeros((imgH, imgW), dtype='float32')
    summed_Gimg = np.zeros((imgH, imgW), dtype='float32')
    summed_Bimg = np.zeros((imgH, imgW), dtype='float32')
    total_Rimg = np.zeros((imgH, imgW), dtype='int8')
    total_Gimg = np.zeros((imgH, imgW), dtype='int8')
    total_Bimg = np.zeros((imgH, imgW), dtype='int8')
    
    #Loop for the number of images
    with open(os.path.join(path, 'picInfo.csv')) as f:
        content = f.readlines()
    for line in content:
        #Load image and EV values
        tokens = line.split(',')
        img = np.array(Image.open(os.path.join(path, tokens[1])), np.float16)
        ev = 1/(float(tokens[2])*float(Fraction(tokens[3])))
        print(tokens[1], 'load image and convert')
        #Blue ch
        img_b = np.where( (img[:,:,2]>TH_H) | (img[:,:,2]<TH_L), 0, img[:,:,2] )
        cnt_b = np.where( (img[:,:,2]>TH_H) | (img[:,:,2]<TH_L), 0, 1 )
        summed_Bimg = summed_Bimg + ev*img_b
        total_Bimg  = total_Bimg + cnt_b
        #Green ch
        img_g = np.where( (img[:,:,1]>TH_H) | (img[:,:,1]<TH_L), 0, img[:,:,1] )
        cnt_g = np.where( (img[:,:,1]>TH_H) | (img[:,:,1]<TH_L), 0, 1 )
        summed_Gimg = summed_Gimg + ev*img_g
        total_Gimg  = total_Gimg + cnt_g
        #Red ch
        img_r = np.where( (img[:,:,0]>TH_H) | (img[:,:,0]<TH_L), 0, img[:,:,0] )
        cnt_r = np.where( (img[:,:,0]>TH_H) | (img[:,:,0]<TH_L), 0, 1 )
        summed_Rimg = summed_Rimg + ev*img_r
        total_Rimg  = total_Rimg + cnt_r
    #calculating the average value for each pixel
    summed_Rimg = np.divide(summed_Rimg, total_Rimg, out=np.zeros_like(summed_Rimg), where=total_Rimg!=0)
    summed_Gimg = np.divide(summed_Gimg, total_Gimg, out=np.zeros_like(summed_Gimg), where=total_Gimg!=0)
    summed_Bimg = np.divide(summed_Bimg, total_Bimg, out=np.zeros_like(summed_Bimg), where=total_Bimg!=0)
    hdr_img.append(summed_Bimg)
    hdr_img.append(summed_Gimg)
    hdr_img.append(summed_Rimg)
    return hdr_img

###main()################    
#input the location of images
parser = argparse.ArgumentParser(description='Code for High Dynamic Range Imaging tutorial.')
parser.add_argument('--input', type=str, help='Path to the directory that contains images and exposure times.')
args = parser.parse_args()
if not args.input:
    parser.print_help()
    exit(0)

print('load images done.')

#Load images and integration
print('making HDR image...')
hdr = makeHDRimage(args.input)
print('done.')

#initialize matrix
print('matrix initialize...')
matX = np.zeros((imgH,imgW), dtype='float32')
matY = np.zeros((imgH,imgW), dtype='float32')
matZ = np.zeros((imgH,imgW), dtype='float32')
#Lens correction
matLens = np.zeros((imgH,imgW))
for i in range(imgH):
    for j in range(imgW):
         if j < imgW/2:
            p = c1_y - i
            q = c1_x - j
            d = math.sqrt(p*p + q*q)
            if d < imgR:
                matLens[i, j] = 1
            else:
                matLens[i, j] = 0
         else:
            p = c2_y - i
            q = c2_x - j
            d = math.sqrt(p*p + q*q)
            if d < imgR:
                matLens[i, j] = 1
            else:
                matLens[i, j] = 0
print('done.')

#convert RGB to XYZ
print('convert RGB...')
matX = hdr[2]
matY = hdr[1] 
matZ = hdr[0]
matX_trim = matX*matLens
matY_trim = matY*matLens
matZ_trim = matZ*matLens
print('done.')

#Output csv files
print('saving csv files...')
np.savetxt(os.path.join(args.input,'dataR.csv'), matX_trim, delimiter=",", fmt='%f')
np.savetxt(os.path.join(args.input,'dataG.csv'), matY_trim, delimiter=",", fmt='%f')
np.savetxt(os.path.join(args.input,'dataB.csv'), matZ_trim, delimiter=",", fmt='%f')
print('done.')
