from __future__ import print_function
from __future__ import division

import numpy as np
import csv
import argparse
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import cv2
import math
import os

tc2_u = np.array( [0.180046,
                   0.180638,
                   0.181309,
                   0.182067,
                   0.182919,
                   0.183872,
                   0.184932,
                   0.186103,
                   0.187389,
                   0.188792,
                   0.190312,
                   0.191949,
                   0.193701,
                   0.195566,
                   0.197540,
                   0.199619,
                   0.201799,
                   0.204074,
                   0.206440,
                   0.208891,
                   0.211423,
                   0.214030,
                   0.216706,
                   0.219449,
                   0.222251,
                   0.225110,
                   0.228020,
                   0.230978,
                   0.233979,
                   0.237020,
                   0.240097,
                   0.243206,
                   0.246345,
                   0.249511,
                   0.252699,
                   0.255909,
                   0.259136,
                   0.262379,
                   0.265635,
                   0.268902,
                   0.272179,
                   0.275462,
                   0.278750,
                   0.282042,
                   0.285335,
                   0.288629,
                   0.291922,
                   0.295211,
                   0.298497,
                   0.301778,
                   0.305053,
                   0.308320,
                   0.311579,
                   0.314829,
                   0.318068,
                   0.321297,
                   0.324514,
                   0.327718,
                   0.330909,
                   0.334087,
                   0.337250,
                   0.340397,
                   0.343530,
                   0.346646,
                   0.349746])

tc2_v = np.array( [0.263577,
                   0.265948,
                   0.268506,
                   0.271236,
                   0.274118,
                   0.277131,
                   0.280251,
                   0.283452,
                   0.286709,
                   0.289997,
                   0.293293,
                   0.296575,
                   0.299825,
                   0.303025,
                   0.306162,
                   0.309223,
                   0.312199,
                   0.315083,
                   0.317868,
                   0.320550,
                   0.323126,
                   0.325595,
                   0.327956,
                   0.330208,
                   0.332354,
                   0.334393,
                   0.336329,
                   0.338163,
                   0.339897,
                   0.341536,
                   0.343080,
                   0.344534,
                   0.345901,
                   0.347183,
                   0.348384,
                   0.349508,
                   0.350557,
                   0.351534,
                   0.352443,
                   0.353287,
                   0.354069,
                   0.354791,
                   0.355457,
                   0.356070,
                   0.356631,
                   0.357144,
                   0.357611,
                   0.358034,
                   0.358417,
                   0.358760,
                   0.359066,
                   0.359338,
                   0.359577,
                   0.359785,
                   0.359964,
                   0.360115,
                   0.360240,
                   0.360342,
                   0.360420,
                   0.360477,
                   0.360513,
                   0.360531,
                   0.360531,
                   0.360515,
                   0.360483])

tc2_c = np.array( [-4.09562,
                   -3.91330,
                   -3.71055,
                   -3.49513,
                   -3.27420,
                   -3.05386,
                   -2.83890,
                   -2.63279,
                   -2.43778,
                   -2.25517,
                   -2.08544,
                   -1.92856,
                   -1.78409,
                   -1.65136,
                   -1.52956,
                   -1.41784,
                   -1.31534,
                   -1.22121,
                   -1.13468,
                   -1.05503,
                   -0.981592,
                   -0.913771,
                   -0.851035,
                   -0.792904,
                   -0.738952,
                   -0.688801,
                   -0.642113,
                   -0.598586,
                   -0.557953,
                   -0.519975,
                   -0.484439,
                   -0.451151,
                   -0.419941,
                   -0.390652,
                   -0.363145,
                   -0.337292,
                   -0.312978,
                   -0.290097,
                   -0.268554,
                   -0.248261,
                   -0.229137,
                   -0.211108,
                   -0.194104,
                   -0.178063,
                   -0.162926,
                   -0.148638,
                   -0.135149,
                   -0.122412,
                   -0.110382,
                   -0.099019,
                   -0.088284,
                   -0.078141,
                   -0.068557,
                   -0.059499,
                   -0.050939,
                   -0.042848,
                   -0.035200,
                   -0.027970,
                   -0.021135,
                   -0.014673,
                   -0.008564,
                   -0.002787,
                   0.002674,
                   0.007839,
                   0.012722])

def calc_cct(ut, vt):
    cct = 1
    duv = 1
    if ut < 0.07 or 0.6 < ut or vt < 0.2 or 0.4 < vt:
        cct=0
        duv=0
    else:
        DT = np.zeros(65)
        j = -1
        while True:
            j = j+1
            DT[j] = ( (tc2_u[j] - ut ) - tc2_c[j]*( ( tc2_v[j] - vt ) ) ) / math.sqrt( 1.0 + tc2_c[j]* tc2_c[j] )
            if j == 64:
                break
            if DT[j] >= 0:
                break
                
        DDD = -DT[j-1] / ( DT[j] - DT[j-1] )
        Tm = j - 1.0 + DDD
        cct = 100000/Tm
        
        PPP = ( tc2_u[j] + tc2_u[j-2] )/2.0 - tc2_u[j-1]
        QQQ = ( tc2_u[j] - tc2_u[j-2] )/2.0
        UON = (PPP*DDD+QQQ)*DDD+tc2_u[j-1]
        PPP = (tc2_v[j] + tc2_v[j-2] )/2.0 - tc2_v[j-1]
        QQQ = (tc2_v[j] - tc2_v[j-2] )/2.0
        VON = (PPP*DDD+QQQ)*DDD+tc2_v[j-1]
        DUV = math.sqrt( (ut- UON)*(ut- UON) + (vt-VON)*(vt-VON) )*1000
        if vt < VON:
            duv = -DUV
        else:
            duv = DUV
            
    return cct, duv

def loadLuminanceFile(path):
    matData = np.genfromtxt(
        fname=path,
        dtype="float",
        delimiter=","
    )
    return matData

def geo_mean(iterable):
    log_sum = 0
    cnt_not_zero = 0
    for a in iterable:
        if a > 0:
            log_sum = log_sum + math.log10(a)
            cnt_not_zero += 1
    return 10**(log_sum/cnt_not_zero)

parser = argparse.ArgumentParser(description='Code for Pseudo Color Imaging tutorial.')
parser.add_argument('--input', type=str, help='Path to the directory that contains X Y Z csv data.')
args = parser.parse_args()
if not args.input:
    parser.print_help()
    exit(0)

#輝度CSVファイルの読み込み
print('Loding csv X data...')
matX = loadLuminanceFile(os.path.join(args.input, 'dataX.csv'))
print('done')
print('Loding csv Y data...')
matY = loadLuminanceFile(os.path.join(args.input, 'dataY.csv'))
print('done')
print('Loding csv Z data...')
matZ = loadLuminanceFile(os.path.join(args.input, 'dataZ.csv'))
print('done')

#csvファイルの分離
matX1 = matX[100:3550,  100:3550]
matX2 = matX[100:3550, 3775:7225]
matY1 = matY[100:3550,  100:3550]
matY2 = matY[100:3550, 3775:7225]
matZ1 = matZ[100:3550,  100:3550]
matZ2 = matZ[100:3550, 3775:7225]

imgH = matY1.shape[0]
imgW = matY1.shape[1]
imgR = 1725

#initialize matrix
print('matrix initialize...')
#solid angle of each pixel
# 2PI / ( PI * R^2 )
dw = (2/(imgR*imgR))
#projection correction
matCoeff = np.zeros((imgH,imgW))
for i in range(imgH):
    for j in range(imgW):
         p = imgH/2 - i
         q = imgW/2 - j
         d = math.sqrt(p*p + q*q)
         if d <= imgR:
             in_angle = 2 * math.asin( (math.sqrt(2)*d)/(2*imgR) )
             matCoeff[i,j] = math.cos(in_angle)
         else:
            matCoeff[i,j] = 0
print('done.')

#convert luminance to illuminance for each pixel
illumX1 = np.sum(dw * matX1 * matCoeff)
illumX2 = np.sum(dw * matX2 * matCoeff)
illumY1 = np.sum(dw * matY1 * matCoeff)
illumY2 = np.sum(dw * matY2 * matCoeff)
illumZ1 = np.sum(dw * matZ1 * matCoeff)
illumZ2 = np.sum(dw * matZ2 * matCoeff)

#CCT計算
u_1 = 4*illumX1 / (illumX1 + 15*illumY1 + 3*illumZ1)
v_1 = 6*illumY1 / (illumX1 + 15*illumY1 + 3*illumZ1)
u_2 = 4*illumX2 / (illumX2 + 15*illumY2 + 3*illumZ2)
v_2 = 6*illumY2 / (illumX2 + 15*illumY2 + 3*illumZ2)
CCT_1, Duv_1 = calc_cct(u_1, v_1)
CCT_2, Duv_2 = calc_cct(u_2, v_2)

print(illumY1)
print(CCT_1)
print(Duv_1)
print(illumY2)
print(CCT_2)
print(Duv_2)

#ヒストグラムファイル名
h_file = os.path.dirname(args.input) + "/hist_L.csv"

fig = plt.figure(figsize=(12,9))
gs = GridSpec(nrows=3, ncols=2, height_ratios=[3,1,2])
fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.05, hspace=0.10)
#ax1 = fig.add_subplot(6,2,1)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

mappable0 = ax1.imshow(matY1, cmap='jet', norm=LogNorm(vmin=1e-3, vmax=1e6))
mappable1 = ax2.imshow(matY2, cmap='jet', norm=LogNorm(vmin=1e-3, vmax=1e6))

ax3 = fig.add_subplot(gs[4])
ax4 = fig.add_subplot(gs[5])

n1, bins1, patches1 = ax3.hist(matY1.flatten(), bins=np.logspace(-3,6,90), color='silver', alpha=0.75)
ax3.set_xscale('log')
ax3.set_xlim(1e-3, 1e6)
ax3.xaxis.set_visible(False)
ax3.tick_params('x', labelsize = 0)
ax3.set_yscale('log')
ax3.set_ylabel('num')

n2, bins2, patches2 = ax4.hist(matY2.flatten(), bins=np.logspace(-3,6,90), color='silver', alpha=0.75)
ax4.set_xscale('log')
ax4.set_xlim(1e-3, 1e6)
ax4.xaxis.set_visible(False)
ax4.tick_params('x', labelsize = 0)
ax4.set_yscale('log')
ax4.set_ylabel('num')

Amean1 = np.nansum(matY1)/(np.count_nonzero(matY1))  #算術平均輝度の算出
maxLumi1=np.nanmax(matY1)
minLumi1=np.nanmin(matY1[np.nonzero(matY1)])
Gmean1=geo_mean(matY1.flatten())
Amean2 = np.nansum(matY2)/(np.count_nonzero(matY2))  #算術平均輝度の算出
maxLumi2=np.nanmax(matY2)
minLumi2=np.nanmin(matY2[np.nonzero(matY2)])
Gmean2=geo_mean(matY2.flatten())

pp1 = fig.colorbar(mappable0, ax = ax3, orientation="horizontal", pad=0)
pp1.set_clim(1e-3, 1e6)
pp1.set_label("Luminance [cd/m2]", fontsize=10)

pp2 = fig.colorbar(mappable0, ax = ax4, orientation="horizontal", pad=0)
pp2.set_clim(1e-3, 1e6)
pp2.set_label("Luminance [cd/m2]", fontsize=10)


ax5 = fig.add_subplot(gs[2])
ax6 = fig.add_subplot(gs[3])
column_labels = ["Illuminance","CCT","Duv","Mean Lumi.A", "Mean Lumi.G"]
data1 = [["[lx]","[K]","[-]","[cd/m2]","[cd/m2]"],
        [format(illumY1,'.2E'), format(CCT_1,'.0f'), format(Duv_1,'.2f'), format(Amean1,'.2E'), format(Gmean1,'.2E')]]
data2 = [["[lx]","[K]","[-]","[cd/m2]","[cd/m2]"],
        [format(illumY2,'.2E'), format(CCT_2,'.0f'), format(Duv_2,'.2f'), format(Amean2,'.2E'), format(Gmean2,'.2E')]]

ax5.axis('tight')
ax5.axis('off')
ax5.table(cellText=data1, colLabels=column_labels, fontsize=12,loc="center")
ax6.axis('tight')
ax6.axis('off')
ax6.table(cellText=data2, colLabels=column_labels, fontsize=12,loc="center")

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
