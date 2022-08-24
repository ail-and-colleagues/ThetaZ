# ThetaZ
RICOH　ThetaZ1用の輝度計測システム

## prerequisites
* gphoto2
* ptpcam (libptp)
* dcraw
* opencv ?


## installation
### gphoto
ターミナルより下記コマンドを実行。
```
sudo apt-get install gphoto2
```
Thetaを接続すると次図のようなダイアログが表示され、基本的にはUSBメモリとしてマウントされる模様。

![Theta接続時の挙動](/assets/2022-08-24%20101247.png)

ファイルマネージャー（windowでいうエクスプローラー）を開くとUSBメモリとして扱われているので次図のように一方についてマウントを解除する。

![Thetaのマウントと解除する](./assets/2022-08-24%20101557.png)

`gphoto2 --summary`を実行してカメラのサマリ:
>Manufacturer: Ricoh Company, Ltd.  
>Model: RICOH THETA Z1  
>  Version: 2.00.1  
>  ...
が表示されればOK。

なお、USBメモリとしてマウントされている場合は以下のようなエラーが表示される。
>*** エラー ***  
>An error occurred in the io-library ('USB デバイスと断定できませんでした'):  
>...  

### libptp
Note: 色々試したがlibptp(ptpcam)ではうまく動かず。詳細は[issue #1: libptp problem with Theta Z1/SC2](#1) #1。


```
sudo apt-get install build-essential
sudo apt install libusb-dev


# sudo apt-get install libusb-1.0-0-dev


wget -P . http://sourceforge.net/projects/libptp/files/libptp2/libptp2-1.2.0/libptp2-1.2.0.tar.gz
tar -xzvf libptp2-1.2.0.tar.gz
cd libptp2-1.2.0/
./configure
make
sudo make install
sudo /sbin/ldconfig -v
```



#### note
```
sudo apt-get install build-essential
sudo svn checkout svn://svn.code.sf.net/p/libptp/code/trunk libptp-code`
```
`sudo svn checkout svn://svn.code.sf.net/p/libptp/code/trunk libptp-code` causes errors as follows:
>svn: E170013: Unable to connect to a repository at URL 'svn://svn.code.sf.net/p/libptp/code/trunk'
>svn: E000111: Can't connect to host 'svn.code.sf.net': Connection refused

Install libptp2 from sources to address the errors.

ref: [RICOH THETA Development on Linux](https://codetricity.github.io/theta-linux/usb_api/)

...but got results as follows under VMware Workstation 16 Player, Ubuntu 22.04.1, and Theta SC2.
![ptpcam error](./assets/2022-08-22%20183047.png)

## sidenote
There is a simple python library called PYPy that aims to control cameras with ptp.

[PTPy](https://github.com/Parrot-Developers/sequoia-ptpy)

Unfortunately, Theta SC2 does not work with PTPy (that may relate SC2 doesn't support the USB API officially. The errors noted above also may relate to this).

If the other Theta models work with PTPy, using PTPy will be a more easy way to control.

ref: https://api.ricoh/blog/2021/02/28/summary-of-theta-apis-2020-edition/
