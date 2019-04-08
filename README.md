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
4. Ctrl+alt+t to open up terminal
5. Type `sudo apt-get update && suso apt-get upgrade` and hit Enter.
6. Type `sudo apt-get install xrdp` and hit on Enter to install XRDP. What is Xterminal? Find that out.
7. Shut Down your raspberry pi using command `sudo halt` or `sudo shutdown -h now`. (In order to reboot you can press `sudo reboot`).
8. Remove keyboard, mouse, display from RPi and turn power supply on.
9. Open windows remote desktop(pre-installed on every windows system).
10. Type IP address of RPi on Remote desktop client's window. In order to find out device's ip address connected to your smart phone you can use [network ip scanner](https://play.google.com/store/apps/details?id=com.network.networkip).
11. Type your username and password on RD client window to access RPi.

> Remember:
> Make a network on your smartphone with
> `SSID: anuja`
> `Password : ar3k57u4`
> Then access your RPi using Windows RD Client. `Your ip address: 192.168.43.215`

> Caution: The RPi is now in DHCP mode. So that ip address will change with different ssid and passwd of wi-fi network you connected after a reboot. So try to use above ssid and passwd everytime.
> `RPi username: pi`
> `password: raspberry`

## Reading Keypad
1. For reading or scanning keypad pull-up resistors are inevitable. Why? Google it. Or go through these articles: 
    1. [sparkfun article](https://learn.sparkfun.com/tutorials/pull-up-resistors/all).
    2. [Iamzxlee](https://www.google.com/amp/s/iamzxlee.wordpress.com/2013/07/24/4x4-matrix-keypad/amp/)
    3. [Chipprogrammer](https://chipprogrammer.blogspot.com/2016/12/8051-keyboard-interfacing.html?m=1)
2. In RPi we have built-in pull up or down resistors of 1.8KOhms. So that we don't want to use external pull-up resistors as scene in article 3.
3. The idea in single word is as follows. As the key press occurs there will be a short circuit. Short circuit indicates zero voltage while open circuit indicates equivalent to logical HIGH voltage. Being a CMOS device for RPi it is about 3.3v level.
4. [Read alternative functions assigned to each GPIO pins in RPi arm based processor](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf).(Page102). You can see which pins are pulled to **LOW** or logical zero. These pins are really useful for us. Note down GPIO/BCM numbering of those pins.
5. Then go to terminal. Using command `pinout` we can find out corresponding BOARD number of these pins.
6. I chose some pins that may not interrupt regular SPI and I2C functioning of RPi. The program look alike:
```python3
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

rows = [8, 10, 11, 12]
cols = [32, 33, 35,36]
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']]

for row_pin in rows:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for col_pin in cols:
    GPIO.setup(col_pin, GPIO.OUT)

def get_key():
    key = 0
    for col_num, col_pin in enumerate(cols):
        GPIO.output(col_pin, 1)
        for row_num, row_pin in enumerate(rows):
            if GPIO.input(row_pin):
                key = keys[row_num][col_num]
        GPIO.output(col_pin, 0)
    return key

while True:
    key = get_key()
    if key :
        print(key)
    time.sleep(0.3)
GPIO.cleanup()
```

### Notations
RPi: Raspberry Pi
RD: Remote Desktop
DHCP: Dynamic host control protocol
