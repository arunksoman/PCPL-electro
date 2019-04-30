import RPi.GPIO as GPIO
import time
import sys
from mfrc522 import SimpleMFRC522
import json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

rows = [14, 26, 17, 18]
cols = [12, 13, 19,16]
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']]

product = [
    ['Product1', 858624605840, 8000, False],
    ['Product2', 236811894460, 1000, False],
    ['Product3', 650705026722, 1200, False],
    ['Product4', 99658219146, 800, False],
    ['Product5', 30953647075, 900, False]
    ]

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
fixed = 5
print("Press A for Entering budget and B for skipping.")
Budget_enter = False
reader = SimpleMFRC522()
data = {}
data['RFID'] = []
while True:
    key = get_key()
    if key :
        if key == "A":
            count = 0
            print(key)
            print("Enter your Budget as a 5 digit number on keypad:")
            skip = False
        if key == "B":
            print(key)
            count = 6
            Budget_enter = True
            print("Enter your Budget as a 5 digit number on keypad:")
            skip = True
        if not skip and key != "A" and count < 6:
            print(skip)
            key = get_key()
            print("count = ", count)
            count = count + 1
            temp = int(key) * (10 ** (fixed - count))
            budget = budget + temp
            print("budget = ", budget)
            if count >= 5:
                Budget_enter = True
                print("You can't enter more than 5 digits")
                
    if Budget_enter:
        print("Hold a tag near the reader")
        print("ID: ", id)
        id, text = reader.read()
        # print(type(id))
        key = get_key()
        if key == "D":
            print("Thank you")
            GPIO.cleanup()
            sys.exit()
        print('{"data":[{', file=open("output.json", "a"))
        for index in range(5): 
            if id == product[index][1] and not product[index][3]:
                product[index][3] = True
                prize = product[index][2]
                print(product)

                cart = cart + prize
                print("prize added= ", prize)
            
            elif id == product[index][1] and product[index][3]:
                product[index][3] = False
                prize = product[index][2]
                print(product)
                cart = cart - prize
                print("prize removed= ", prize)
        print("cart = " , cart)
        if cart > budget and not skip:
            print("Warning: Your Budget Exceeded")
    time.sleep(0.3)
GPIO.cleanup()

