from machine import (Pin, ADC, PWM)
import machine
import uasyncio as asyncio
import random
import time

button_red = Pin(0, Pin.IN, Pin.PULL_UP)
button_green = Pin(12, Pin.IN, Pin.PULL_UP)
button_yellow = Pin(13, Pin.IN, Pin.PULL_UP)

pressed = False
failed = False

red_led = Pin(1, Pin.OUT)
green_led = Pin(14, Pin.OUT)
yellow_led = Pin(16, Pin.OUT)
white_led = Pin(15, Pin.OUT)

pot = ADC(26)

buzzer = PWM(Pin(10))

frequency = 1000

def getPotValue():
    rawValue = pot.read_u16()
    pm_max_value = 66000

    normalizedValue = rawValue/pm_max_value
    print(normalizedValue)
    return normalizedValue

def buzz():
    global frequency
    buzzer.duty_u16(32768)  # 50% duty cycle (half power)

    while True:
        buzzer.freq(frequency)  # Set frequency
        



def trackPot():
    global frequency
    while True:
        frequency = int(500 + 10000*getPotValue())
        print(frequency)

#32768
while True:
    frequency = int(2000+4500*getPotValue())
    buzzer.duty_u16(32768)
    buzzer.freq(frequency)
    print(buzzer.freq())
    time.sleep_ms(100)
    buzzer.duty_u16(0)
    time.sleep_ms(100)