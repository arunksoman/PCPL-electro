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

