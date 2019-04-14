import RPi.GPIO as GPIO
import time
import sys
from mfrc522 import SimpleMFRC522


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

rows = [8, 37, 11, 12]
cols = [32, 33, 35,36]
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']]

product = [
    ['Product1', 858624605840, 8000],
    ['Product2', 236811894460, 1000],
    ['Product3', 650705026722, 1200],
    ['Product4', 99658219146, 800],
    ['Product5', 30953647075, 900]
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
print("Enter your Budget as a 5 digit number on keypad:")
fixed = 5
Budget_enter = False
reader = SimpleMFRC522()
while True:
    key = get_key()
    if count < 6:
        if key :
            print("count = ",count)
            count = count + 1
            temp = int(key) * (10 ** (fixed - count))
            budget = budget + temp
            print("sum = ", budget)
            if count >= 5:
                Budget_enter = True
                print("You can't enter more than 5 digits")
    if Budget_enter:
        print("Hold a tag near the reader")
        id, text = reader.read() 
        print("ID: ", id)
        print(type(id))
        for index in range(5):
            
            if id == product[index][1]:
                prize = product[index][2]
                print(index)
                print("prize = ", prize)
        cart = cart + prize
        print("cart = ", cart)
        if cart > budget:
            print("Warning: Your Budget Exceeded")
    time.sleep(0.3)
GPIO.cleanup()
