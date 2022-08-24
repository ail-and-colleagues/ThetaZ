# Set up Raspberry Pi Desktop as VM
## Install VMware Workstation 16 Player
インストーラを[ここ](https://www.vmware.com/jp/products/workstation-player/workstation-player-evaluation.html)からダウンロード。**VMware-player-full-16.x.x-x.exe**を起動し、インストールを行う。特に選択を迷うオプションは無いはず。

インストール完了後、VMWareを起動。ライセンスについては利用目的に応じて適切なものを選択する。

## Raspberry Pi Desktopのインストール
仮想マシンとしてRaspberry Pi Desktop（raspi_dtp）をインストールする。

まず、[ここ](https://www.raspberrypi.com/software/raspberry-pi-desktop/)の[Download下のArchive](https://downloads.raspberrypi.org/rpd_x86/images/)からRaspiのディスクイメージ **rpd_x86-2021-01-12/**(2021-01-11-raspios-buster-i386.iso)をダウンロードする。なお、Ricoh Theta USB APIの[ドキュメント](https://codetricity.github.io/theta-linux/usb_api/#hardware-and-os
)には：
> Raspberry Pi 3 with Raspian 10, buster. Any version and any model should work.

とあるが、テストではRaspian 11 (bullseye, rpd_x86-2022-07-04/	(2022-07-01-raspios-bullseye-i386.iso))では、Z1、SC2共に適切に動作しなかった。

VMWareにて、「新規仮想マシンの作成」をクリック。ウィザードが立ち上がるので、**インストーラディスクイメージファイル**に先程ダウンロードした**2021-01-11-raspios-buster-i386.iso**を指定して（次図）次へ。

![インストーラディスクイメージファイルを指定して次へ](./assets/2022-08-23%20111411.png)
図はbullseye、正しくはbuster
raspi_dtpの場合、OSの種類が自動判別されないので次図のように指定する。

![OSの指定](./assets/2022-08-23%20111517.png)
正しくは「その他のLinux 5.xカーネル」で64bitではない

仮想マシンの名前の設定（次図）。場所で指定したフォルダ（ここでは`D:\VM\raspi_dtp`）に複数のファイルが展開されるのでトップレベルのフォルダを指定すること。

![仮想マシン名称・場所の指定](./assets/2022-08-23%20111558.png)

新しく作成するマシンのディスク容量が問われるのでホスト（もとのPC）を圧迫せず、かつ、作成するraspi_dtpでの作業に支障がない程度の容量を指定する。

![仮想マシンのディスク容量](./assets/2022-08-23%20161040.png)

続いて作成する仮想マシンの諸設定が表示される。後から変更もできるが仮想マシンのメモリをハードウェアをカスタマイズから変更しておく。

![ハードウェアのカスタマイズ](./assets/2022-08-23%20161121.png)

ホストのスペックによるが8GB確保することが推奨されている。余裕があればプロセッサ数も増やすと良い。

![仮想マシンのメモリを増やす](./assets/2022-08-23%20161217.png)

設定を終えると次図のように仮想マシンの準備ができる。**仮想マシンの再生**をクリックしてraspi_dtpを起動する。

![仮想マシン名称・場所の指定](./assets/2022-08-23%20111741.png)

raspu_dtpを再生すると**Debian GNU/Linux boot menu**が表示されるので**Graphical install**を選択する。他のウインドウがアクティブになっていると操作を受け付けないので、Graphical installのあたりをクリックした上で上下キーで選択すると確実だと思われる。
あとは[ここ](https://www.kkaneko.jp/tools/vmware/vmwareclientraspdesktop.html)の「3. 画面が現れる」から「14. インストール終了の確認」までを行う。

### Intel VT-x・AMD-V/SVM関係のエラーが出たら
昨今のPCにはハードウェアレベルの仮想化支援技術（要するにraspi_dtpのような仮想マシンを効率的に動作させる技術）が用意されている。普通の人にはこの機能は不要であるので、有効にするにはBIOS/UEFIにてIntel CPU（Core ixなど）のマシンならIntel VT-xを、AMD（Ryzen）のマシンならAMD-V/SVMを有効にする必要がある。自分のpcとCPUに応じて`let's note intel vt-z`などで検索してこの機能を有効にすること。

## open-vm-tools-desktopのインストール

open-vm-tools-desktopは仮想マシンを使いやすくするためのツール。ホストOSとraspi_dtpで間でテキストのコピペができるようになるなど便利なのでインストールしておく。

作業はTarminalで行う。TarminalはWindowsでいうコマンドプロンプト（Power Shell）。raspi_dtpはじめLinuxでは、GUIでは行えない細かい操作を行うのに用いる。

![Tarminal起動](./assets/2022-08-23%20171912.png)

インストールにはターミナルにて`sudo apt-get install open-vm-tools-desktop`を実行する。特にエラーメッセージが表示されなければ成功。

## USBデバイスを使えるようにする
一旦raspi_dtpをシャットダウンする。

![シャットダウン](./assets/2022-08-23%20173647.png)

ホストOSにて、仮想マシンが保存されているフォルダ（ここでは`D:\VM\raspi_dtp`）にある**raspi_dtp.vmx**をテキストエディタで開き、`usb.restrictions.defaultAllow = "False"`となっていれば`="True"`に、該当する行がなければ`usb.restrictions.defaultAllow = "True"`を末尾に加える。

### ホストOSとraspi_dtpでファイルのやり取りをできるようにする

**raspi_dtp.vmx**に以下の2行を加え保存。
```
isolation.tools.copy.disable = "FALSE"
isolation.tools.paste.disable = "FALSE"
```

raspi_dtpを起動し、取り外し可能デバイスの一覧が選択可能になっていること（次図、グレーアウトされていないこと）を確かめる。また、ファイルのコピペができることを確認する。
![取り外し可能デバイスが選択可能に](./assets/2022-08-24%20150127.png)
