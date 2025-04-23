import RPi.GPIO as GPIO
import time

def dec2bin(dec):
    return [int(num) for num in bin(dec)[2:].zfill(8)]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
comp   = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)


REFERENCE_VOLTAGE = 3.3

def adc():
    for value in range(256):
        binary = dec2bin(value)

        GPIO.output(dac, binary)
        comp_value = GPIO.input(comp)
        time.sleep(0.01)
        if comp_value:
            return value
        
    return 0

try:
    while True:
        value   = adc()
        voltage = value * REFERENCE_VOLTAGE / 256.0
        if value: print("Цифровое значение = {:^3}, Напряжение = {:.2f} B".format(value, voltage))

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
    print("EOP")