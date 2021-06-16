#!/bin/bash

#保存先ディレクトリの作成
DATE=`date '+%y%m%d_%H%M%S'`
mkdir /home/pi/ThetaZ/data/${DATE} 
chmod 777 /home/pi/ThetaZ/data/${DATE}

#カメラのアクティベート
gphoto2 --auto-detect
sleep 0.1
#露光モードをマニュアルに変更
ptpcam --set-property=0x500e --val=0x0001
sleep 0.1
#画像サイズを指定
ptpcam --set-property=0x5003 --val=6720x3360
sleep 0.1
#ホワイトバランスの設定
ptpcam --set-property=0x5005 --val=0x8002
sleep 0.1
#絞りの設定
ptpcam --set-property=0x5007 --val=560
sleep 0.1
#スリープ機能をOFF
ptpcam --set-property=0xd803 --val=0
sleep 0.1

#露光時間 ISO感度を変えて撮影
while read -r line
do
	col1=`echo ${line} | cut -d ',' -f 1`
	col2=`echo ${line} | cut -d ',' -f 2`
	col3=`echo ${line} | cut -d ',' -f 3`
	col4=`echo ${line} | cut -d ',' -f 4`
	col5=`echo ${line} | cut -d ',' -f 5`
	ptpcam --set-property=0x500f --val=100
	echo -e -n ${col4} > val.bin
	ptpcam -R 0x1016,0xd00f,0,0,0,0,val.bin
	sleep 0.1	
	ptpcam -c
	sleep ${col5}	
	echo ${col1}.dng,${col1}.ppm,100,${col3} >> /home/pi/ThetaZ/data/${DATE}/picInfo.csv
done < list.csv
#list.csvの書式
#１列目　画像No.
#２列目　ISO感度
#３列目　シャッタースピード
#４列目　シャッタースピード（１６進）
#5列目　画像取得待ち時間（シャッタースピードの２倍程度）

#画像のダウンロード
ptpcam -G
sudo chmod 777 *.DNG
sudo chmod 777 *.JPG
#画像のりネーム
ls *.DNG | awk '{ printf "mv %s %02d.DNG\n", $0, NR }' | sh
ls *.JPG | awk '{ printf "mv %s %02d.JPG\n", $0, NR }' | sh
#画像の移動
mv *.DNG /home/pi/ThetaZ/data/${DATE}/
mv *.JPG /home/pi/ThetaZ/data/${DATE}/
ptpcam -D

