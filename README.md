# ThetaZ
RICOH　ThetaZ1用の輝度計測システム

Raspberry Pi DesktopをVMWareで仮想マシンとしてセットアップする場合は[set_up_raspi_as_vm](https://github.com/ail-and-colleagues/ThetaZ/blob/refactoring/set_up_raspi_as_vm/README.md)を参考のこと。

## prerequisites
* gphoto2
* ptpcam (libptp): [libptp problem with Theta Z1/SC2](https://github.com/ail-and-colleagues/ThetaZ/issues/1)
* dcraw
* opencv ?

## installation
### gphoto2
`sudo apt-get install gphoto2`でインストールしたgphoto2(少なくともlibgphoto<=2.5.27.1)だとシャッタースピードの変更ができないため、自分でソースをビルドしてインストールする必要がある模様（[#2 can not control shutter speed](https://github.com/ail-and-colleagues/ThetaZ/issues/2)）。

まず、必要なものをインストールしておく。
```
sudo apt-get update
sudo apt-get install libusb-1.0-0-dev libpopt-dev
sudo apt-get install automake autoconf pkg-config gettext libtool
```
#### libgphoto2
libgphoto2をダウンロード、解凍。
```
wget -O "libgphoto2.zip" https://github.com/ail-and-colleagues/libgphoto2/archive/refs/heads/master.zip .
unzip ./libgphoto2.zip
```



以下を実行し、ビルド・インストール。
```
cd libgphoto2-master
autoreconf --install --symlink
./configure --prefix=/usr/local
make
sudo make install
cd ../
```
`ls /usr/local/lib/`し、libgphoto2~で始まるファイルが配置されていればOK。

#### gphoto2
続いてgphoto2のダウンロード、インストール。
```
wget -O "gphoto2.zip" https://github.com/gphoto/gphoto2/archive/refs/heads/master.zip .
unzip gphoto2.zip
cd gphoto2-master/
autoreconf --install --symlink
./configure PKG_CONFIG_PATH="/usr/local/lib/pkgconfig${PKG_CONFIG_PATH+":${PKG_CONFIG_PATH}"}" --prefix=/usr/local
make
sudo make install
cd ../
```

Thetaを接続し、`gphoto2 --summary`を実行してカメラのサマリ:
>Manufacturer: Ricoh Company, Ltd.  
>Model: RICOH THETA Z1  
>  Version: 2.00.1  
>  ...

が表示されればOK。シャッタースピードの確認は`gphoto2 --get-config shutterspeed`から行える。以下のように情報が得られることを確認しておく。

>Label: Shutter Speed                                                           
Readonly: 0  
Type: RADIO  
Current: 1/100  
Choice: 0 1/25000  
Choice: 1 1/20000  
...

なお、USBメモリとしてマウントされている場合は以下のようなエラーが表示される。
>*** エラー ***  
>An error occurred in the io-library ('USB デバイスと断定できませんでした'):  
>...  

これは、Thetaを接続した際にUSBメモリとしてマウントされてしまった場合。おそらく次図のようなダイアログが表示される。

![Theta接続時の挙動](/assets/2022-08-24%20101247.png)

ファイルマネージャー（windowでいうエクスプローラー）を開くとUSBメモリとして扱われているのが確認できるので、次図のように一方についてマウントを解除する。

![Thetaのマウントと解除する](./assets/2022-08-24%20101557.png)


### libptp
うまく動かず…。

なお、[setup.txt](./docs/setup.txt)にてlibptpのインストール（正確にはソースコードのダウンロード）を行う`sudo svn checkout svn://svn.code.sf.net/p/libptp/code/trunk libptp-code` は以下のように接続が拒否される。
>svn: E170013: Unable to connect to a repository at URL 'svn://svn.code.sf.net/p/libptp/code/trunk'
>svn: E000111: Can't connect to host 'svn.code.sf.net': Connection refused

よって、[RICOH THETA Development on Linux](https://codetricity.github.io/theta-linux/usb_api/)を参考に別途libptpを用意することを試行したがうまく動かず。詳細は[issue #1: libptp problem with Theta Z1/SC2](https://github.com/ail-and-colleagues/ThetaZ/issues/1)。

## capture
Theta Z1のgphoto2でのキャプチャバージョンを**capture_gphoto2.sh**として実装。
gphoto2はカメラ内のファイルを削除する際にフォルダの指定が要る。ひとまず[.sh内で直接指定しているので注意](https://github.com/ail-and-colleagues/ThetaZ/blob/64ef82951a9aa8a7795c4d5df69c317105a167fd/tools/theta_z1/capture_gphoto2.sh#L113)。

https://github.com/ail-and-colleagues/ThetaZ/blob/64ef82951a9aa8a7795c4d5df69c317105a167fd/tools/theta_z1/capture_gphoto2.sh#L113

また、evList.csvでの撮影の設定では、シャッタースピードの設定は0.1でなく1/10のように分数で表記する必要があるので注意。

使い方はオリジナルの**capture.sh**と同じで、`sudo capture_gphoto2.sh [画像親ディレクトリ]`。

## sidenote
[PTPy](https://github.com/Parrot-Developers/sequoia-ptpy)なるPython向けのlibptp実装もあり。
ただ、基本がlibptpなので[issue #1: libptp problem with Theta Z1/SC2](https://github.com/ail-and-colleagues/ThetaZ/issues/1)と同様のエラーが起きる。