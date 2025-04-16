import RPi.GPIO as GPIO
import time

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup  (dac, GPIO.OUT)

flag = 1
num  = 0

try:
    period = float(input("input period: "))
    while (True):
        binNum = decimal2binary(num)
        GPIO.output(dac, binNum)
        print(f'number is {num}. In binary {binNum}')
        if num == 0:
            flag = 1
        
        elif num == 255:
            flag = 0

        num = num + 1 if flag == 1 else  num - 1
        time.sleep(period/512)

except ValueError:
    print("Incorrect period")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()