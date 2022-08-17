# ThetaZ
RICOH　ThetaZ1用の輝度計測システム

## prerequisites
* gphoto2
* ptpcam
* dcraw
* opencv

## installation
### gphoto
```
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh
chmod 755 gphoto2-updater.sh
sudo ./gphoto2-updater.sh
```
### ptpcam
```
#sudo apt-get install subversion 
#sudo apt-get install libusb-dev
sudo apt-get install build essential
```
The next command causes errors as follows:
```
sudo svn checkout svn://svn.code.sf.net/p/libptp/code/trunk libptp-code
```
>svn: E170013: Unable to connect to a repository at URL 'svn://svn.code.sf.net/p/libptp/code/trunk'
>svn: E000111: Can't connect to host 'svn.code.sf.net': Connection refused

Install ptpcam2 from sources to address the errors. Ptpcam2
requires libusb-0.1.8, so install libusb first.
```
wget https://sourceforge.net/projects/libusb/files/libusb-0.1%20%28LEGACY%29/0.1.8/libusb-0.1.8.tar.gz
tar -xvf  libusb-0.1.8.tar.gz
cd libusb-0.1.8.tar.gz
sudo ./configure
sudo make
sudo make install 
cd ../
```
Install ptpcam2 as follows.
```
wget http://sourceforge.net/projects/libptp/files/libptp2/libptp2-1.2.0/libptp2-1.2.0.tar.gz
tar -xvf  libptp2-1.2.0.tar.gz 
cd libptp2-1.2.0/
sudo ./configure
sudo make
sudo make install
```
Check the installation via the below command.
```
ptpcam
```
In the case a library error is reported as follows, 
>ptpcam: error while loading shared libraries: libptp2.so.1: cannot open shared object file: No such file or directory

add paths to LD_LIBRARY_PATH with the below command.
```
export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib
```