import RPi.GPIO as GPIO

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup  (dac, GPIO.OUT)

try:
    while True:
        num = input("input number 0 to 255: ")
        try:
            num = int (num)
            if 0 <= num and num <= 255:
                GPIO.output(dac, decimal2binary(num))
                voltage = float(num) / 256.0 * 3.3
                print(f"output voltage is about {voltage:.4} volt")
            else:
                if num < 0:
                    print("number have to be >=0")
                elif num > 255:
                    print("number have to be <= 255")  
        except Exception:
            if num == "q": break
            if type(num) == str: print("you have to type a number, not string")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()