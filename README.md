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

## Pinout

In order to know more about GPIO headers visit [pinout.xyz](https://pinout.xyz)The RPi GPIO(General purpose IO) pinout given below.
![GPIO Headers](/images/1554777830796.png)
> Caution: RPi GPIO pins are very important in electronics perspective. You have to count Pin number as given in the picture. The **first pin is near to BLE(Bluetooth Low Energy Module which has Raspberry logo)**.

> Important: In programming we can use both BCM GPIO numbering or physical board numbering. For beginners I recommend physical bord numbering. In physical numbering left column of GPIO headers is `odd numbers` while right column is `even number`.

> Important: **In every program I am telling you about Physical BOARD pin numbering in order to void confusion.**

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

7. In order to run this program rig up the wires with keypad and Raspberry Pi.
8. Then execute following commands one by one on terminal
```bash
cd ~
mkdir my_project
cd my_project
touch keypad.py
```
9. In order to create program open command line editor called **nano** using following command `sudo nano keypad.py`. Copy and paste above program on this window. In order to paste press `ctrl+shift+v`. 
10. Press `ctrl+x` to exit command line editor
11. Press `y` and hit Enter key on next prompt to save and exit.
12. Rig up circuit according to your program. Face up your 4×4 keypad. First 4 pins on the left represents rows while next 4 pins represents columns. All connections are made with physical pin numbering of RPi.Rows are connected to 8, 10, 11, 12. Next 4 pins are connected to 32, 33, 35 and 36 as you can see list in the program.
13. Then in order to run program  `python3 keypad.py`

### Notations
RPi: Raspberry Pi
RD: Remote Desktop
DHCP: Dynamic host control protocol

## RC522 RFID reader/ writer interfacing

1. Enable SPI. Read [Raspberry-sPi.co.uk](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/) article. **__Use method 1__** . In order to toggle b/w **Select**, **Finish**, **yes**, and  **no** use Tab keys.
2. Reboot your Pi using `sudo reboot`
3. Check SPI is enabled or not using following command `lsmod grep | spi`
4. Install python3-dev using command `sudo apt-get install python3-dev python3`.
5. Install spi-dev using command `sudo pip3 install spidev`
6. Enter to your project directory using `cd ~/my_project`
7. Clone Pymilifeup SPI MFRC522 library using command `git clone https://github.com/pimylifeup/MFRC522-python.git`
8. In order to install this Python package execute following commands one by one
```bash
cd MFRC522-python
python setup.py install
```
9. Write program using following commands
```bash
touch read.py
sudo nano read.py
```
Copy following program and paste using `ctrl+shift+v`. Then press `ctrl+x`. Hit on `y` followed by Enter to exit from command line text editor.

```python
###read.py
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read() 
        print("ID: %s\nText: %s" % (id,text))
        sleep(5) 
except KeyboardInterrupt:
    GPIO.cleanup() 
    raise
```
