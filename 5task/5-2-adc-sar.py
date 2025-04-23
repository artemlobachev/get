import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    return [int(elem) for elem in bin(num)[2:].zfill(8)]

def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        dac_val = dec2bin(k)
        GPIO.output(dac, dac_val)
        time.sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val:
            k -= 2**i
        print(dac_val)
    return k

start_time = time.time()
conversion_count = 0

try:
    while True:
        value = adc()
        voltage = value * 3.3 / 256.0
        if value: 
            print("Цифровое значение = {:^3}, Напряжение = {:.2f} B".format(value, voltage))
            conversion_count += 1
finally:
    end_time = time.time()
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
    print("Время работы {:.2f} секунд".format(end_time - start_time))
    print("Количество преобразований: ", conversion_count)
    print("Среднее время на преобразование: {:.3f} мс".format((end_time - start_time) * 1000 / max(1, conversion_count)))
    print("EOP")