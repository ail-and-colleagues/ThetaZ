# ThetaZ
RICOH　ThetaZ1用の輝度計測システム

Raspberry Pi DesktopをVMWareで仮想マシンとしてセットアップする場合は[set_up_raspi_as_vm](https://github.com/ail-and-colleagues/ThetaZ/blob/refactoring/set_up_raspi_as_vm/README.md)を参考のこと。

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
うまく動かず…。

なお、[setup.txt](./docs/setup.txt)にてlibptpのインストール（正確にはソースコードのダウンロード）を行う`sudo svn checkout svn://svn.code.sf.net/p/libptp/code/trunk libptp-code` は以下のように接続が拒否される。
>svn: E170013: Unable to connect to a repository at URL 'svn://svn.code.sf.net/p/libptp/code/trunk'
>svn: E000111: Can't connect to host 'svn.code.sf.net': Connection refused

よって、[RICOH THETA Development on Linux](https://codetricity.github.io/theta-linux/usb_api/)を参考に別途libptpを用意することを試行したがうまく動かず。詳細は[issue #1: libptp problem with Theta Z1/SC2](https://github.com/ail-and-colleagues/ThetaZ/issues/1)。

## sidenote
[PTPy](https://github.com/Parrot-Developers/sequoia-ptpy)なるPython向けのlibptp実装もあり。
ただ、基本がlibptpなので[issue #1: libptp problem with Theta Z1/SC2](https://github.com/ail-and-colleagues/ThetaZ/issues/1)と同様のエラーが起きる。