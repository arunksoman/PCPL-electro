import RPi.GPIO as GPIO
import random
import time
import sys
from mfrc522 import SimpleMFRC522
import requests
import json
import subprocess

"""output = subprocess.run('python3 -m http.server 8000', shell=True, stdout=subprocess.PIPE, 
                        universal_newlines=True)"""

product = json.loads(requests.get("http://192.168.43.54:8084/SmartTrolley/Files/hello.txt").text)
print(product)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

low = 0
high = 999
user_id = random.uniform(low,high)
pi_id = int(user_id)
print("pi_id= ", pi_id)

out_dict = {}
buzzer = 31

rows = [8, 37, 11, 12]
cols = [32, 33, 35,36]
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']]

"""product = [
    ['Product1', 858624605840, 8000, False],
    ['Product2', 236811894460, 1000, False],
    ['Product3', 650705026722, 1200, False],
    ['Product4', 99658219146, 800, False],
    ['Product5', 30953647075, 900, False]
    ]
"""
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
fixed = 5
trolley_id = {"trolley": pi_id}
out = json.dumps(trolley_id, indent=4, separators = (". ", " :"))
print(out,file=open("trolley.json", "w"))
time.sleep(60)
trolley_id = json.loads(requests.get("http://192.168.43.94:8084/SmartTrolley/Files/Limit.txt").text)
print("trolley_id return= ", trolley_id[0])
loop = False
if pi_id == trolley_id[0]:
    print("Press A for Entering budget and B for skipping.")
    loop = True
else:
    loop = False
Budget_enter = False
reader = SimpleMFRC522()
data = {}

while loop:
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
        try:
            id, text = reader.read()
            print("ID: ", id)
            get_key()
        except key == 'D':
            print("Thank you")
            sys.exit()
        for index in range(10): 
            if id == product[index][1] and not product[index][3]:
                product[index][3] = True
                prize = product[index][2]
                """GPIO.OUT(31, True)
                time.sleep(0.7)
                GPIO.output(buzzer,False)"""
                out_dict.update({product[index][0]:product[index][3]})
                
                cart = cart + prize
                print("prize added= ", prize)
            
            elif id == product[index][1] and product[index][3]:
                product[index][3] = False
                prize = product[index][2]
                out_dict.update({product[index][0]:product[index][3]})
                print(product)
                """GPIO.OUT(31, True)
                time.sleep(0.7)
                GPIO.output(buzzer,False)"""
                cart = cart - prize
                print("prize removed= ", prize)
        print("cart = " , cart)
        out_json = json.dumps(out_dict, indent=4, separators = (". ", " :"))
        print(out_json,file=open("output.json", "w"))
        print(out_json)
        if cart > budget and not skip:
            print("Warning: Your Budget Exceeded")
    time.sleep(0.3)
GPIO.cleanup()

