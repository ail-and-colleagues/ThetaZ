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
IMGi_H = 3640
IMGi_W = 7280
#output image size
IMGo_H = 728
IMGo_W = 1458
IMGo_R = 345

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
#解像度圧縮関数(高さ・幅ともに1/5)
def compImg(i_img):
    o_img = np.zeros((IMGo_H, IMGo_W))
    for po in range(IMGo_H):
        for qo in range(IMGo_W):
            #i_imgの対応領域を抽出
            voi_i_img = i_img[(5*po):(5*po+5), (5*qo):(5*qo+5)]
            o_img[po,qo] = np.mean(voi_i_img)
    print("CSV file comp done.")
    return o_img


#視線方向変換関数
def rotateImg(theta, phy, inimg):
    outimg = np.zeros((IMGo_H, IMGo_W))
    for po in range(IMGo_H):
        for qo in range(IMGo_W):
            #光軸を中心とする座標系に変換
            if qo <= IMGo_W/2:
                xo = qo - IMGo_W/4
                yo = IMGo_H/2 - po
                x_so = xo
                y_so = yo
                ro = math.sqrt(xo**2 + yo**2)
                z_so = IMGo_R * (1-(ro/IMGo_R)**2)
            else:
                xo = qo - 3*IMGo_W/4
                yo = IMGo_H/2 - po
                x_so = xo
                y_so = yo
                ro = math.sqrt(xo**2 + yo**2)
                z_so = (-1) * IMGo_R * (1-(ro/IMGo_R)**2)
            #出力画像の作成
            if ro > IMGo_R:
                outimg[po,qo]=0
            else:
                #theta, phy 回転後の入力側球面座標へ変換
                x_si = x_so * math.cos(theta) \
                        + z_so * math.sin(theta)
                y_si = x_so * math.sin(theta) * math.sin(phy) \
                        + y_so * math.cos(phy) \
                        + (-1) * z_so * math.cos(theta) * math.sin(phy)
                z_si = x_so * (-1) * math.sin(theta) * math.cos(phy) \
                        + y_so * math.sin(phy) \
                        + z_so * math.cos(theta) * math.cos(phy)
                #入力画像上の座標特定
                r_si = math.sqrt(x_si**2 + y_si**2)
                if z_si >= 0:
                    xi = IMGo_R * math.sqrt(1-(z_si/IMGo_R)) * x_si / r_si
                    yi = IMGo_R * math.sqrt(1-(z_si/IMGo_R)) * y_si / r_si
                    q  = xi + IMGo_W/4
                    p  = IMGo_H/2 - yi
                else:
                    xi = IMGo_R * math.sqrt(1+(z_si/IMGo_R)) * (-1) * x_si / r_si
                    yi = IMGo_R * math.sqrt(1+(z_si/IMGo_R)) * y_si / r_si
                    q  = xi + 3*IMGo_W/4 
                    p  = IMGo_H/2 - yi
                #変換元の座標を算出
                pi = math.floor(p)
                qi = math.floor(q)
                dp = p - pi
                dq = q - qi
                #変換元の座標の周囲4画素の値でバイリニア補間
                if pi >= IMGi_H-1 and qi >= IMGi_W-1:
                    val_0_0 = inimg[pi, qi]
                    val_0_1 = 0
                    val_1_0 = 0
                    val_1_1 = 0
                    outimg[po,qo] = val_0_0
                elif pi >= IMGi_H-1:
                    val_0_0 = inimg[pi, qi]
                    val_0_1 = inimg[pi, qi + 1]
                    val_1_0 = 0
                    val_1_1 = 0
                    outimg[po,qo] = val_0_0 + (val_0_1 - val_0_0)*dq
                elif qi >= IMGi_W-1:
                    val_0_0 = inimg[pi, qi]
                    val_0_1 = 0
                    val_1_0 = inimg[pi + 1, qi]
                    val_1_1 = 0
                    outimg[po,qo] = val_0_0 + (val_1_0 - val_0_0)*dp
                else:
                    val_0_0 = inimg[pi, qi]
                    val_0_1 = inimg[pi, qi + 1]
                    val_1_0 = inimg[pi + 1, qi]
                    val_1_1 = inimg[pi + 1, qi + 1]
                    outimg[po,qo]=(1-dq)*(1-dp)*val_0_0 \
                                 + dq*(1-dp)*val_0_1 \
                                 + (1-dq)*dp*val_1_0 \
                                 + dq*dp*val_1_1
                
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
#解像度圧縮
InImg_trim = np.hstack([InImg[4:3644, 4:3649], InImg[4:3644, 3647:7292]])
inimg = compImg(InImg_trim)

#視線回転角の設定(単位rad)
theta = math.radians(45)
phy = math.radians(45)

#視線方向の変換
OutImg = rotateImg(theta, phy, inimg)

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
