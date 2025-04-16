import RPi.GPIO as GPIO
import time


def BinTranslator(num):
    number  = [0 for i in range(8)]
    dec_num = num % 256
    bin_num = bin(dec_num)

    i = -1
    while bin_num[i] != 'b':
        number[i] = int(bin_num[i])
        i -= 1

    print("{} => {}".format(num, number))

    GPIO.output(dac, number)
    volt = float(input())
    voltage.append(volt)
    return(0)


dac = [8, 11, 7, 1, 0, 5, 12, 6]
voltage = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

nums = [0, 5, 32, 64, 127, 255, 256]

for i in nums:
    BinTranslator(i)

print(voltage)

GPIO.output(dac, 0)
GPIO.cleanup()