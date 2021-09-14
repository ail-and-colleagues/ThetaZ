##applied for theta Z1
from __future__ import print_function
from __future__ import division

import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math


##parameters setting
#input  image size
IMGi_H = 3648
IMGi_W = 3648
IMGi_R = 1725
#output image size
IMGo_H = 1800
IMGo_W = 1800


#loading csv file
#csvファイル読み込み関数(japanese)
def loadLuminanceFile(path):
    matY = np.genfromtxt(
        fname=path,
        dtype="float",
        delimiter=","
    )
    print("CSV file load done.")
    return matY

#transform to Equidistant Cylindrical Projection from Equisolidangle Projection
#等立体角射影から正距円筒図への変換(japanese)
def trans_EDC_img(inimg):
    outimg = np.zeros((IMGo_H, IMGo_W))
    for po in range(IMGo_H):
        for qo in range(IMGo_W):
            #光軸を中心とする座標系に変換
            xo = qo - IMGo_W/2
            yo = IMGo_H/2 - po
            #方位角・仰角へ変換[rad]
            theta = xo * math.pi / IMGo_W
            phi   = yo * math.pi / IMGo_H
            #球面座標の算出
            x_sph = IMGi_R * math.cos(phi) * math.sin(theta)
            y_sph = IMGi_R * math.sin(phi)
            z_sph = IMGi_R * math.cos(phi) * math.cos(theta)
            #座標変換
            if xo ==0 and yo == 0:
                outimg[po,qo]=inimg[int(IMGi_H/2), int(IMGi_W/2)]
            else:
                #変換元の座標を算出
                xi = IMGi_R * math.sqrt(1 - z_sph/IMGi_R) * x_sph/math.sqrt(x_sph**2+y_sph**2)
                yi = IMGi_R * math.sqrt(1 - z_sph/IMGi_R) * y_sph/math.sqrt(x_sph**2+y_sph**2)
                pi = math.floor(IMGi_H/2 - yi)
                qi = math.floor(xi + IMGi_W/2)
                dp = (IMGi_H/2 - yi) - pi
                dq = (xi + IMGi_W/2) - qi
                #変換元の座標の周囲4画素の値でバイリニア補間
                outimg[po,qo] = (1-dq)*(1-dp)*inimg[pi,qi] + \
                                dq*(1-dp)*inimg[pi,qi+1] + \
                                (1-dq)*dp*inimg[pi+1,qi] + \
                                dq*dp*inimg[pi+1,qi+1]
    print("convert done.")
    return outimg


#############################
##main()#####################
#############################
##input the location of CSV file
parser = argparse.ArgumentParser(description='Code for Trans Imaging tutorial.')
parser.add_argument('--input', type=str, help='Path to the file that contains luminance values.')
args = parser.parse_args()
if not args.input:
    parser.print_help()
    exit(0)

##Load csv file
InImg = loadLuminanceFile(args.input)
#輝度csvファイルの分離
InImg1 = InImg[:, :3648]
InImg2 = InImg[:, 3648:]

##transform to Equidistant Cylindrical Projection from Equisolidangle Projection
OutImg1 = trans_EDC_img(InImg1) 
OutImg2 = trans_EDC_img(InImg2)       
OutImg  = np.concatenate([OutImg1, OutImg2], 1)
#グラフエリアの作成
fig = plt.figure(figsize=(6,9))
fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.05, hspace=0.10)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
plt.suptitle(args.input)

#疑似カラー画像の作成
mappable0 = ax1.imshow(OutImg, cmap='jet', norm=LogNorm(vmin=1e-3, vmax=1e6))

#ヒストグラムの作成
ax2.hist(OutImg.flatten(), bins=np.logspace(-3,6,90), color='silver', alpha=0.75)
ax2.set_xscale('log')
ax2.set_xlim(1e-3, 1e6)
ax2.xaxis.set_visible(False)
ax2.tick_params('x', labelsize = 0)
ax2.set_yscale('log')
ax2.set_ylabel('num')


#カラーバーの描画
pp = fig.colorbar(mappable0, ax = ax2, orientation="horizontal", pad=0)
pp.set_clim(1e-3, 1e6)
pp.set_label("Luminance [cd/m2]", fontsize=10)

#グラフの表示
plt.show()
