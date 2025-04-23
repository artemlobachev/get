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

total_conversions = 0
total_time = 0

def dec2bin(num):
    return [int(elem) for elem in bin(num)[2:].zfill(8)]

def adc():
    global total_conversions
    start_time = time.time()
    
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        dac_val = dec2bin(k)
        GPIO.output(dac, dac_val)
        time.sleep(0.001)  # такая же задержка как в первом скрипте
        comp_val = GPIO.input(comp)
        if comp_val == 0:
            k -= 2**i
    
    end_time = time.time()
    total_conversions += 1
    return k, end_time - start_time

try:
    print("Starting binary search ADC...")
    test_duration = 5  # секунд тестирования
    start_test = time.time()
    
    while time.time() - start_test < test_duration:
        value, conv_time = adc()
        voltage = value * 3.3 / 256.0
        total_time += conv_time
        
        if value:
            print(f"Напряжение = {voltage:.2f} V, Время преобразования = {conv_time*1000:.2f} мс")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    
    if total_conversions > 0:
        avg_time = total_time / total_conversions * 1000
        print(f"\nИтоги:")
        print(f"Всего преобразований: {total_conversions}")
        print(f"Общее время: {total_time:.2f} сек")
        print(f"Среднее время одного преобразования: {avg_time:.2f} мс")
        print(f"Максимальная частота: {1/avg_time*1000:.2f} преобразований/сек")
    print("EOP")