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

#幾何平均輝度算出
def geo_mean(iterable):
    log_sum = 0
    cnt_not_zero = 0
    for a in iterable:
        if a > 0:
            log_sum = log_sum + math.log10(a)
            cnt_not_zero += 1
    return 10**(log_sum/cnt_not_zero)
    
#picinfo.csvを読み込んでimageと露光時間を取得
def loadExposureSeq(path):
    images = []
    times = []
    with open(os.path.join(path, 'picInfo.csv')) as f:
        content = f.readlines()
    for line in content:
        tokens = line.split(',')
        images.append(cv.imread(os.path.join(path, tokens[1])))
        times.append(1/float(tokens[3]))
    return images, np.asarray(times, dtype=np.float32)
parser = argparse.ArgumentParser(description='Code for High Dynamic Range Imaging tutorial.')
parser.add_argument('--input', type=str, help='Path to the directory that contains images and exposure times.')
args = parser.parse_args()
if not args.input:
    parser.print_help()
    exit(0)

images, times = loadExposureSeq(args.input)
print('load images done.')

calibrate = cv.createCalibrateDebevec()
response = calibrate.process(images, times)

merge_debevec = cv.createMergeDebevec()
hdr = merge_debevec.process(images, times, response)
print('hdr image made.')

#配列の初期化
matX = np.zeros((3648,7296))
matY = np.zeros((3648,7296))
matZ = np.zeros((3648,7296))
matLens = np.zeros((3648,7296))
for i in range(3648):
    for j in range(7296):
        if j < 3648:
            p = 1824 - i
            q = 1824 - j
            d = math.sqrt(p*p + q*q)
            if d < 1744:
                matLens[i, j] = 1
            else:
                matLens[i, j] = 0
        else:
            p = 1824 - i
            q = 5472 - j
            d = math.sqrt(p*p + q*q)
            if d < 1744:
                matLens[i, j] = 1
            else:
                matLens[i, j] = 0

print('matrix initialize done.')


#変換係数
RX = 1.0
GX = 1.0
BX = 1.0
RY = 1.0
GY = 1.0
BY = 1.0
RZ = 1.0
GZ = 1.0
BZ = 1.0


print('convert RGB to XYZ.')
matX = RX * hdr[:,:,2] + GX * hdr[:,:,1] + BX * hdr[:,:,0]
matY = RY * hdr[:,:,2] + GY * hdr[:,:,1] + BY * hdr[:,:,0]
matZ = RZ * hdr[:,:,2] + GZ * hdr[:,:,1] + BZ * hdr[:,:,0]
matX_trim = matX*matLens
matY_trim = matY*matLens
matZ_trim = matZ*matLens
print('convert RGB to XYZ done.')
#hdr_3 = [hdr[:,:,i] for i in range(3)]

#tonemap = cv.createTonemap(1.0)
#ldr = tonemap.process(hdr)

#cv.imwrite(os.path.join(args.input,'ldr.png'), ldr * 255)
#cv.imwrite(os.path.join(args.input,'hdr.hdr'), hdr)
print('now saving csv files.')
np.savetxt(os.path.join(args.input,'dataX.csv'), matX_trim, delimiter=",", fmt='%f')
np.savetxt(os.path.join(args.input,'dataY.csv'), matY_trim, delimiter=",", fmt='%f')
np.savetxt(os.path.join(args.input,'dataZ.csv'), matZ_trim, delimiter=",", fmt='%f')
print('saving csv files done.')


#ヒストグラムファイル名
h_file = os.path.join(args.input, "hist_L.csv")

fig = plt.figure(figsize=(6,9))
fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.05, hspace=0.10)
ax1 = fig.add_subplot(211)

mappable0 = ax1.imshow(matY_trim, cmap='jet', norm=LogNorm(vmin=1e-3, vmax=1e6))


#ax1.imshow(matY, cmap='jet', norm=LogNorm(vmin=1e-3, vmax=1e6))

ax2 = fig.add_subplot(212)


n, bins, patches = ax2.hist(matY_trim.flatten(), bins=np.logspace(-3,6,90), color='silver', alpha=0.75)
ax2.set_xscale('log')
ax2.set_xlim(1e-3, 1e6)
ax2.xaxis.set_visible(False)
ax2.tick_params('x', labelsize = 0)
ax2.set_yscale('log')
ax2.set_ylabel('num')

Amean = np.nansum(matY_trim)/(matY_trim.size-np.count_nonzero(matY_trim))  #算術平均輝度の算出
maxLumi=np.nanmax(matY_trim)
minLumi=np.nanmin(matY_trim[np.nonzero(matY_trim)])
Gmean=geo_mean(matY_trim.flatten())
#ax2.text(1000,1000000,'a-mean = %.2e' % Amean, size=10)
#ax2.text(1000,310000,'g-mean = %.2e' % Gmean, size=10)
#ax2.text(1000,100000,'maxLumi = %.2e' % maxLumi, size=10)
#ax2.text(1000,31000,'minLumi = %.2e' % minLumi, size=10)

pp = fig.colorbar(mappable0, ax = ax2, orientation="horizontal", pad=0)
pp.set_clim(1e-3, 1e6)
pp.set_label("Luminance [cd/m2]", fontsize=10)

plt.suptitle(args.input)

with open(h_file, "a") as fileobj:
    fileobj.write(str(os.path.dirname(args.input)) + ",\n")
    fileobj.write("算術平均輝度,幾何平均輝度,最大輝度,最小輝度,\n")
    fileobj.write(str(Amean) + "," + str(Gmean) + "," + str(maxLumi) + "," + str(minLumi) + ",\n")
    fileobj.write("階級,ピクセル数,\n")
    for i in range(0, len(bins)):
        if i == len(bins)-1:
            fileobj.write(str(bins[i]) + ",-,\n")
        else:
            fileobj.write(str(bins[i]) + "," + str(n[i]) + "\n")

plt.show()
