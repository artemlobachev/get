import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

n=10
p = GPIO.PWM(16, 1000)
p.start(0)

try:
    while True:
        f = float(input())
        if (f < 0.0 or f > 100.0 or type(f) == str):
            print("incorrect type it should be float number!")
            continue

        p.ChangeDutyCycle(f)
        print(3.3*f/100)

finally:
    p.stop()
    GPIO.output(16,0)
    GPIO.cleanup()