from __future__ import print_function
from __future__ import division

import numpy as np
import csv
import argparse
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2
import math
import os

#20220311aa

def loadLuminanceFile(path):
    matY = np.genfromtxt(
        fname=path,
        dtype="float",
        delimiter=","
    )
    return matY

def geo_mean(iterable):
    log_sum = 0
    cnt_not_zero = 0
    for a in iterable:
        if a > 0:
            log_sum = log_sum + math.log10(a)
            cnt_not_zero += 1
    return 10**(log_sum/cnt_not_zero)

parser = argparse.ArgumentParser(description='Code for Pseudo Color Imaging tutorial.')
parser.add_argument('--input', type=str, help='Path to the file that contains luminance values.')
args = parser.parse_args()
if not args.input:
    parser.print_help()
    exit(0)

#輝度CSVファイルの読み込み
print('Loding csv data...')
matY = loadLuminanceFile(args.input)
print('done')

#輝度csvファイルの分離
matY1 = matY[100:3550,  100:3550]
matY2 = matY[100:3550, 3775:7225]

#0をNaNで置換
matY1_n = np.where(matY1>0, matY1, np.nan)
matY2_n = np.where(matY2>0, matY2, np.nan)

#ヒストグラムファイル名
h_file = os.path.dirname(args.input) + "/hist_L.csv"

fig = plt.figure(figsize=(12,9))
fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.05, hspace=0.10)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)

mappable0 = ax1.imshow(matY1_n, cmap='jet', norm=LogNorm(vmin=1e-3, vmax=1e6))
mappable1 = ax2.imshow(matY2_n, cmap='jet', norm=LogNorm(vmin=1e-3, vmax=1e6))

ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

n1, bins1, patches1 = ax3.hist(matY1.flatten(), bins=np.logspace(-3,6,100), color='silver', alpha=0.75)
ax3.set_xscale('log')
ax3.set_xlim(1e-3, 1e6)
ax3.xaxis.set_visible(False)
ax3.tick_params('x', labelsize = 0)
ax3.set_yscale('log')
ax3.set_ylabel('num')

n2, bins2, patches2 = ax4.hist(matY2.flatten(), bins=np.logspace(-3,6,100), color='silver', alpha=0.75)
ax4.set_xscale('log')
ax4.set_xlim(1e-3, 1e6)
ax4.xaxis.set_visible(False)
ax4.tick_params('x', labelsize = 0)
ax4.set_yscale('log')
ax4.set_ylabel('num')

Amean1 = np.nansum(matY1)/(np.count_nonzero(matY1>0))  #算術平均輝度の算出
maxLumi1=np.nanmax(matY1)
minLumi1=np.nanmin(matY1[np.nonzero(matY1)])
#Gmean=geo_mean(matY.flatten())
Amean2 = np.nansum(matY2)/(np.count_nonzero(matY2>0))  #算術平均輝度の算出
maxLumi2=np.nanmax(matY2)
minLumi2=np.nanmin(matY2[np.nonzero(matY2)])

pp1 = fig.colorbar(mappable0, ax = ax3, orientation="horizontal", pad=0)
#pp1.set_clim(1e-3, 1e6)
pp1.set_label("Luminance [cd/m2]", fontsize=10)

pp2 = fig.colorbar(mappable0, ax = ax4, orientation="horizontal", pad=0)
#pp2.set_clim(1e-3, 1e6)
pp2.set_label("Luminance [cd/m2]", fontsize=10)

#plt.suptitle(args.input)

with open(h_file, "a") as fileobj:
    fileobj.write(str(os.path.dirname(args.input)) + ",\n")
    fileobj.write("表面,\n")
    fileobj.write("算術平均輝度,最大輝度,最小輝度,\n")
    fileobj.write(str(Amean1) + "," + str(maxLumi1) + "," + str(minLumi1) + ",\n")
    fileobj.write("階級,ピクセル数,\n")
    for i in range(0, len(bins1)):
        if i == len(bins1)-1:
            fileobj.write(str(bins1[i]) + ",-,\n")
        else:
            fileobj.write(str(bins1[i]) + "," + str(n1[i]) + "\n")

    fileobj.write("裏面,\n")
    fileobj.write("算術平均輝度,最大輝度,最小輝度,\n")
    fileobj.write(str(Amean2) + "," + str(maxLumi2) + "," + str(minLumi2) + ",\n")
    fileobj.write("階級,ピクセル数２,\n")
    for i in range(0, len(bins2)):
        if i == len(bins2)-1:
            fileobj.write(str(bins2[i]) + ",-,\n")
        else:
            fileobj.write(str(bins2[i]) + "," + str(n2[i]) + "\n")

plt.show()
