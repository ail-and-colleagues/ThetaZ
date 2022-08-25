#!/bin/bash

#カレントディレクトリを取得
CDIR=`pwd`
#保存先ディレクトリをコマンドライン引数（１番目）から取得
DIRNAME=${1}

#作業デレクトリを画像保存先に変更
cd ${DIRNAME}

#dcrawによるtiff変換
dcraw -v -T -g 1 1 -W *.DNG
echo raw to tiff convert done.

#作業デレクトリをもとに戻す
cd ${CDIR}




