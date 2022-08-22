# ThetaZ
RICOH　ThetaZ1用の輝度計測システム

## prerequisites
* gphoto2
* ptpcam (libptp)
* dcraw
* opencv ?

Note: Does gphoto2 require a libptp installation? On Ubuntu 22.04.1, gphoto2 can be installed via Ubuntu software without additional libraries.

## installation
### gphoto
```
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh
chmod 755 gphoto2-updater.sh
sudo ./gphoto2-updater.sh
```

Note: We can install gphoto2 from Ubuntu software.

### libptp

```
sudo apt-get install build essential
sudo svn checkout svn://svn.code.sf.net/p/libptp/code/trunk libptp-code`
```

Note: `sudo svn checkout svn://svn.code.sf.net/p/libptp/code/trunk libptp-code` causes errors as follows:
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
