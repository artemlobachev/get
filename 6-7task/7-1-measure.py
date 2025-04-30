import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from time import time, sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11,  9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

def dec2bin(num):
    return [int(elem) for elem in bin(num)[2:].zfill(8)]

def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        GPIO.output(dac, dec2bin(k))
        sleep(0.001)
        if GPIO.input(comp) == 0:
            k -= 2**i
    return k

def show_leds(value):
    value = int(value / 256 * len(led))
    GPIO.output(led, [1 if i < value else 0 for i in range(len(led))])

def measure_voltage():
    return adc()

def save_data(filename, data):
    with open(filename, 'w') as f:
        for value in data:
            f.write(f"{value}\n")

def save_settings(filename, sample_rate, quantization_step):
    with open(filename, 'w') as f:
        f.write(f"Частота дискретизации: {sample_rate:.2f} Гц\n")
        f.write(f"Шаг квантования: {quantization_step:.4f} В\n")

try:
    measurements = []
    start_time = time()
    
    GPIO.output(troyka, GPIO.HIGH)
    print("Начало фазы заряда конденсатора")
    
    input_voltage = 3.3
    target_voltage = 0.97 * input_voltage * 255 / 3.3 
    while True:
        value = measure_voltage()
        measurements.append(value)
        show_leds(value)
        if value >= target_voltage:
            break
    
    GPIO.output(troyka, GPIO.LOW)
    print("Начало фазы разряда конденсатора")
    
    target_voltage = 0.02 * input_voltage * 255 / 3.3
    
    while True:
        value = measure_voltage()
        measurements.append(value)
        show_leds(value)
        if value <= target_voltage:
            break
    
    end_time = time()
    duration = end_time - start_time
    sample_count = len(measurements)
    sample_rate = sample_count / duration
    quantization_step = 3.3 / 256
    
    save_data("data.txt", measurements)
    save_settings("settings.txt", sample_rate, quantization_step)
    
    plt.plot(measurements)
    plt.title("Процесс заряда и разряда конденсатора в RC-цепи")
    plt.xlabel("Номер измерения")
    plt.ylabel("Показание АЦП")
    plt.show()
    
    print("\nРезультаты эксперимента:")
    print(f"Общая продолжительность: {duration:.2f} сек")
    print(f"Количество измерений: {sample_count}")
    print(f"Период одного измерения: {duration/sample_count:.6f} сек")
    print(f"Средняя частота дискретизации: {sample_rate:.2f} Гц")
    print(f"Шаг квантования АЦП: {quantization_step:.4f} В")

finally:
    GPIO.output(dac, 0)
    GPIO.output(led, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()