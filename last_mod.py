import RPi.GPIO as GPIO
import random
import time
import sys
import requests
import json
import serial

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
    
def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
        
    GPIO.output(LCD_RS, mode)  # RS
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits& 0x10== 0x10:
        GPIO.output(LCD_D4, True)
    if bits& 0x20== 0x20 :
        GPIO.output(LCD_D5, True)
    if bits& 0x40 == 0x40 :
        GPIO.output(LCD_D6, True)
    if bits& 0x80 == 0x80 :
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits& 0x01 == 0x01 :

        GPIO.output(LCD_D4, True)
    if bits& 0x02 == 0x02 :
        GPIO.output(LCD_D5, True)
    if bits& 0x04 == 0x04 :
        GPIO.output(LCD_D6, True)
    if bits& 0x08 == 0x08 :
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH," " )
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)
def force(message, force):
    message = message.ljust(LCD_WIDTH," " )
    lcd_byte(force, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

product = json.loads(requests.get("http://192.168.43.94:8084/SmartTrolley/Files/ProductData.txt").text)
print(type(product))
print(product)
print(len(product))
length_of_list=len(product)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)
loop = False
LCD_RS = 21 
LCD_E = 24
LCD_D4 = 23
LCD_D5 = 19
LCD_D6 = 18
LCD_D7 = 22
# Display constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.005
E_DELAY = 0.005

low = 0
high = 999
trolly_id = random.uniform(low,high)
trolley_id = int(trolly_id)
print("Trolley id= ", trolley_id)
str_trolley = str(trolley_id)
frmt_str_trolley = "    " + str_trolley
main()
lcd_init()
lcd_string("  Trolly id   ", LCD_LINE_1)
lcd_string(frmt_str_trolley, LCD_LINE_2)
time.sleep(40)
trolley_id_ret = json.loads(requests.get("http://192.168.43.94:8084/SmartTrolley/Files/PINVerify.txt").text)
print(trolley_id_ret)
print(type(trolley_id_ret))
print(type(trolley_id_ret[0][0]))
if trolley_id == trolley_id_ret[0][0]:
    lcd_string("Pin Verified", LCD_LINE_1)
    lcd_string("Thank you", LCD_LINE_2)
    loop = True
elif trolley_id != trolley_id_ret[0][0]:
    loop = False 
    lcd_string("Pin Verification", LCD_LINE_1)
    lcd_string("     Failed", LCD_LINE_2)
    time.sleep(2)
    lcd_string("", LCD_LINE_1)
    lcd_string("     Exiting...", LCD_LINE_2)
    time.sleep(1)
    sys.exit()
print(product)
out_dict = {}
out_dict['RFID'] = [] 
buzzer = 31

rows = [8, 37, 11, 12]
cols = [32, 33, 35,36]
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']]

GPIO.setup(buzzer, GPIO.OUT)
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
count = 0
budget = 0
cart = 0
fixed = 4
print("Press A for Entering budget and B for skipping.")
lcd_string("A :Enter Budget", LCD_LINE_1)
lcd_string("B: skip Budget", LCD_LINE_2)
Budget_enter = False
data = {}
while loop:
    key = get_key()
    if key :
        if key == "D":
            lcd_string("Thank You", LCD_LINE_1)
            lcd_string("Visit Again", LCD_LINE_2)
            GPIO.cleanup()
            sys.exit()
        if key == "A":
            count = 0
            print(key)
            print("Enter your Budget as a 4 digit number on keypad:")
            lcd_string("Enter 4 digit ", LCD_LINE_1)
            lcd_string("number on keypad", LCD_LINE_2)
            skip = False
        if key == "B":
            print(key)
            count = 4
            Budget_enter = True
            skip = True
        if not skip and key != "A" and count < 4:
            print(skip)
            key = get_key()
            print("count = ", count)
            force_cursor = [0xC6, 0xC5, 0xC4, 0xC3, 0xC2, 0xC1, 0xC0]
            temp = int(key) * (10 ** (fixed - count))
            budget = (budget + temp/10)
            budget=int(budget)
            bud_lcd = str(budget)
            conc_budg = "budget = " + bud_lcd
            lcd_string("", LCD_LINE_1)
            lcd_string("", LCD_LINE_2)
            lcd_string(conc_budg, force_cursor[count])
            print("Budget = ", budget)
            count = count + 1
            if count >= 4:
                Budget_enter = True
                print("You can't enter more than 4 digits")
                lcd_string("Can't enter more", LCD_LINE_1)
                lcd_string("than 4 digits", LCD_LINE_2)
                time.sleep(0.5)
    if Budget_enter:
        print("Hold a tag near the reader")
        lcd_string("Hold Card Near", LCD_LINE_1)
        lcd_string(" the Reader ", LCD_LINE_2)
        id = ser.readline()
        print(id)
        id = id.decode('utf-8')
        id = id[0:7]
        
        if key == "D":
            lcd_string("Thank You", LCD_LINE_1)
            lcd_string("Visit Again", LCD_LINE_2)
            GPIO.cleanup()
            sys.exit()
        lcd_string("", LCD_LINE_1)
        lcd_string(id , LCD_LINE_2)
        print("ID: ", id)
        for index in range((length_of_list-1)): 
            if id == product[index][1] and not product[index][3]:
                product[index][3] = True
                # out_dict.update({product[index][0]:product[index][3]})
                out_dict['RFID'].append({  
                'product': product[index][4],
                'status': product[index][3]
                })
                prize = product[index][2]
                print(out_dict)
                cart = cart + prize
                str_cart = str(cart)
                conc_cart = "cart = "+ str_cart
                lcd_string(product[index][0] + " added", LCD_LINE_1)
                lcd_string(conc_cart, LCD_LINE_2)
                time.sleep(0.5)
                print("prize added= ", prize)
            
            elif id == product[index][1] and product[index][3]:
                product[index][3] = False
                prize = product[index][2]
                
                cart = cart - prize
                # out_dict.update({product[index][0]:product[index][3]})
                str_cart = str(cart)
                conc_cart = "cart = "+ str_cart
                lcd_string(product[index][0] + " removed", LCD_LINE_1)
                lcd_string(conc_cart, LCD_LINE_2)
                print(product)
                print("prize removed= ", prize)
                out_dict['RFID'].append({  
                'product': product[index][4],
                'status': product[index][3]
                })
        print("cart = " , cart)
        out_json = json.dumps(out_dict, indent=4)
        print(out_json,file=open("output.json", "w"))
        print(out_json)
        if cart > budget and not skip:
            print("Warning: Your Budget Exceeded")
            lcd_string("Sorry Your", LCD_LINE_1)
            lcd_string(" Budget Exceeded ", LCD_LINE_2)
            time.sleep(2)
    time.sleep(0.3)
lcd_init()
GPIO.cleanup()

