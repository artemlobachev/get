import RPi.GPIO as GPIO
import time

def dec2bin(dec):
    return [int(num) for num in bin(dec)[2:].zfill(8)]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac           = [8, 11, 7, 1, 0, 5, 12, 6]
comp          = 14
troyka_module = 13

REFERENCE_VOLTAGE = 3.3

def adc():
    for value in range(256):
        binary = dec2bin(value)
        GPIO.output(dac, binary)

        time.sleep(0.001)

        comp_value = GPIO.input(comp)
        if comp_value == 0:
            return value
        
    return 255

try:
    while True:
        value   = adc()
        voltage = value / 255 * REFERENCE_VOLTAGE
        print("Цифровое значение = {:^3}, Напряжение = {:.2f} B".format(value, voltage))
        time.sleep(0.1)

finally:
    GPIO.output(dac, [0] * 8)
    GPIO.output(troyka_module, 0)
    GPIO.cleanup()