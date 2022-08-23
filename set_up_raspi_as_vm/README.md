# Set up Raspberry Pi Desktop as VM
## Install VMware Workstation 16 Player
インストーラを[ここ](https://www.vmware.com/jp/products/workstation-player/workstation-player-evaluation.html)からダウンロード。*VMware-player-full-16.x.x-x.exe*を起動し、インストールを行う。特に選択を迷うオプションは無いはず。

インストール完了後、VMWareを起動。ライセンスについては利用目的に応じて適切なものを選択する。

## Raspberry Pi Desktopのインストール
仮想マシンとしてRaspberry Pi Desktop（raspi_dtp）をインストールする。

まず、[ここ](https://www.raspberrypi.com/software/raspberry-pi-desktop/)からRaspiのディスクイメージ *20xx-x-x-raspios-bullseye-i386.iso*をダウンロードする。

VMWareにて、「新規仮想マシンの作成」をクリック。ウィザードが立ち上がるので、*インストーラディスクイメージファイル*に先程ダウンロードした*20xx-x-x-raspios-bullseye-i386.iso*を指定して（次図）次へ。
![インストーラディスクイメージファイルを指定して次へ](./assets/2022-08-23%20111411.png)

raspi_dtpの場合、OSの種類が自動判別されないので次図のように指定する。
![OSの指定](./assets/2022-08-23%20111517.png)

仮想マシンの名前の設定（次図）。場所で指定したフォルダ（ここでは`D:\VM\raspi_dtp`）に複数のファイルが展開されるのでトップレベルのフォルダを指定すること。
![仮想マシン名称・場所の指定](./assets/2022-08-23%20111558.png)

新しく作成するマシンのディスク容量が問われるのでホスト（もとのPC）を圧迫せず、かつ、作成するraspi_dtpでの作業に支障がない程度の容量を指定する。
![仮想マシンのディスク容量](./assets/2022-08-23%20161040.png)

続いて作成する仮想マシンの諸設定が表示される。後から変更もできるが仮想マシンのメモリをハードウェアをカスタマイズから変更しておく。
![ハードウェアのカスタマイズ](./assets/2022-08-23%20161121.png)

ホストのスペックによるが少なくとも2GB程度はあったほうが良いかもしれない。余裕があればプロセッサ数も増やすと良い。
![仮想マシンのメモリを増やす](./assets/2022-08-23%20161217.png)

設定を終えると次図のように仮想マシンの準備ができる。*仮想マシンの再生*をクリックしてraspi_dtpを起動する。
![仮想マシン名称・場所の指定](./assets/2022-08-23%20111741.png)

### Intel VT-x・AMD-V/SVM関係のエラーが出たら
昨今のPCにはハードウェアレベルの仮想化支援技術（要するにraspi_dtpのような仮想マシンを効率的に動作させる技術）が用意されている。普通の人にはこの機能は不要であるので、有効にするにはBIOS/UEFIにてIntel CPU（Core ixなど）のマシンならIntel VT-xを、AMD（Ryzen）のマシンならAMD-V/SVMを有効にする必要がある。自分のpcとCPUに応じて`let's note intel vt-z`などで検索してこの機能を有効にすること。

raspu_dtpを再生すると*Debian GNU/Linux boot menu*が表示されるので*Graphical install*を選択する。他のウインドウがアクティブになっていると操作を受け付けないので、Graphical installのあたりをクリックした上で上下キーで選択すると確実だと思われる。
あとは[ここ](https://www.kkaneko.jp/tools/vmware/vmwareclientraspdesktop.html)の「3. 画面が現れる」から「14. インストール終了の確認」までを行う。

## 仮想マシンの設定





