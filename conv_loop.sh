#!/bin/bash

#カレントディレクトリを取得
CDIR=`pwd`
#保存先ディレクトリをコマンドライン引数（１番目）から取得
DIRNAME=${1}

#画像保存先フォルダを読み込み現像
while read -r line
do
	#作業デレクトリを画像保存先に変更
	col1=`echo ${line} | cut -d ',' -f 1`
	dir_data=`basename ${col1}`
	cd ${DIRNAME}/${dir_data}
	#dcrawによるtiff変換
	dcraw -v -T -g 1 1 -W *.DNG
	cd ${CDIR}
	#pythonスクリプトでXYZ変換
	python3 conv_xyz.py --input ${DIRNAME}/${dir_data}
done < ${DIRNAME}/dirList.txt


#作業デレクトリをもとに戻す
cd ${CDIR}
