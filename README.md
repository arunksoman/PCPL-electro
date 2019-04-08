# Raspberry Pi PCPL Step-by-step Guide
## Installing OS [Done]

1. Go to [Raspberry pi downloads](https://www.raspberrypi.org/downloads/)
2. Download [Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/) (New official debian os distro). Then extract zip file. Then you can see an iso file.
3. Insert SD card on your PC using SD card reader
4. Download and install [SD card formatter](https://www.sdcard.org/downloads/formatter/index.html)
5. Format SD card.(**Important: make sure that Drive letter shown on SD card formatter is correct. Otherwise it will format your hard disk**)
6. Download and install [Belena etcher](https://www.balena.io/etcher/). Win32Diskimager, Rufus etc. are other best options. But I personally like Etcher
7. Write Downloaded OS on SD card using Helena etcher. Etcher will find SD card automatically. Choose iso file to write. Wait until write and verification completes. It will take more than half hour.
8. Insert SD card on RPi
9. Connect 2000mAh/ 2Ah(atleast, but do not exceed 2.5Ah. 2Ah or 2.1Ah will be good.) to microUSB port.
10. You can see Red LED is blinking... Then followed by Green LED. Red LED indicates sufficient power. Blinking of red LED indicate insufficient power. Blinking of Green LED indicates read/write operation of SD card.
> Caution: After powering up do not put RPi on metal surface. Do not touch on exposed solder leads on the bottom since these regions are ESD prone and that may permanently damage your Pi.

##  Accessing Raspberry Pi via Remote Desktop[Done]
1. In order to access remote desktop we have install windows xrdp on RPi. So that connect display to HDMI (if you have no HDMI cable, use HDMI to VGA adapter), USB keyboard, Mouse, LAN (also we can use Wi-Fi) to RPi. Then boot up RPi by connecting microUSB adapter(specs are mentioned above)
2. Create a Wi-Fi said and password on your smartphone.
3. Connect RPi on that using WiFi symbol on the task bar of RPi Desktop.
2. Ctrl+alt+t to open up terminal
3. Type `sudo apt-get update && suso apt-get upgrade` and hit Enter.
4. Type `sudo apt-get install xrdp` and hit on Enter to install XRDP. What is Xterminal? Find that out.
5. Shut Down your raspberry pi using command `sudo halt` or `sudo shutdown -h now`. (In order to reboot you can press `sudo reboot`).
6. Remove keyboard, mouse, display from RPi and turn power supply on.
7. Open windows remote desktop(pre-installed on every windows system).
8. Type IP address of RPi on Remote desktop client's window. In order to find out device's ip address connected to your smart phone you can use [network ip scanner](https://play.google.com/store/apps/details?id=com.network.networkip).
9. Type your username and password on RD client window to access RPi.

> Remember:
> Make a network on your smartphone with
> `SSID: anuja`
> `Password : ar3k57u4`
> Then access your RPi using Windows RD Client. `Your ip address: 192.168.43.215`

> Caution: The RPi is now in DHCP mode. So that ip address will change with different ssid and passwd of wi-fi network you connected after a reboot. So try to use above ssid and passwd everytime.
> `RPi username: pi`
> `password: raspberry`
