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
count = 0
sum = 0
print("Enter your Budget as a 5 digit number on keypad:")
fixed = 5
while True:
    key = get_key()
    if count < 6:
        if key :
            print("count = ",count)
            count = count + 1
            print(key)
            temp = int(key) * (10 ** (fixed - count))
            print("temp = ", temp)
            sum = sum + temp
            print("sum = ", sum)
            if count >= 5:
                print("You can't enter more than 5 digits")
    time.sleep(0.3)
GPIO.cleanup()
