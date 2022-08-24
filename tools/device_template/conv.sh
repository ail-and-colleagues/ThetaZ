#!/bin/bash

#カレントディレクトリを取得
CDIR=`pwd`

#保存先ディレクトリをコマンドライン引数（１番目）から取得
DIRNAME=${1}
FLG=${2}

#作業デレクトリを画像保存先に変更
cd ${DIRNAME}

#dcrawによるtiff変換
case "$FLG" in
  "2") dcraw -v -T -g 2.4 12.92 -W *.DNG
       echo sRGB
       ;;
  *)   dcraw -v -T -g 1 1 -W *.DNG
       echo g11
       ;;
esac
echo raw to tiff convert done.


#作業デレクトリをもとに戻す
cd ${CDIR}

#pythonスクリプトでXYZ変換
case "$FLG" in
  "2") python3 conv_xyz_g24.py --input ${DIRNAME}
       echo sRGB
       ;;
  *)   python3 conv_xyz_g10.py --input ${DIRNAME}
       echo g11
       ;;
esac
