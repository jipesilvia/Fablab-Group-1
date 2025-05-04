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

async def buzz():
    global frequency
    while True:
        #buzzer.freq(frequency)  # Set frequency
        buzzer.duty_u16(32768)  # 50% duty cycle (half power)
        await asyncio.sleep_ms(10)



async def trackPot():
    global frequency
    while True:
        frequency = int(100 + 20000*getPotValue())
        print(frequency)
        await asyncio.sleep_ms(10)



async def main():
    await asyncio.gather(trackPot(), buzz())

asyncio.run(main())