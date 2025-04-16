import RPi.GPIO as GPIO
# import time

GPIO.setmode (GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(24, GPIO.IN)



if (GPIO.input(24) == GPIO.HIGH):
    GPIO.output(21, GPIO.HIGH)

else:
    GPIO.output(21, GPIO.LOW)