import RPi.GPIO as GPIO
import time

leds = [2, 3, 4, 17, 27, 22, 10, 9]

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT)

for i in range(3):
    for j in range(8):
        GPIO.output(leds[j],GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(leds[j], GPIO.LOW)

GPIO.output(leds, GPIO.LOW)
GPIO.cleanup()