from machine import (Pin, ADC)
import machine
import time

# Define LEDs
red = Pin(3, Pin.OUT)
green = Pin(5, Pin.OUT)
yellow = Pin(12, Pin.OUT)
white = Pin(0, Pin.OUT)


# Define Buttons with Internal Pull-Down Resistors

button_red = Pin(28, Pin.IN, Pin.PULL_DOWN)
button_green = Pin(22, Pin.IN, Pin.PULL_DOWN)
button_yellow = Pin(17, Pin.IN, Pin.PULL_DOWN)

potentiometer = machine.ADC(26)


count = 0

def click_button(color):
    if color == "red":
        red.on()
    elif color == "green":
        green.on()
    elif color == "yellow":
        yellow.on()
    while True:
            if color == "red":
                if button_red.value():
                    red.off()
                    return
            elif color == "green":
                if button_green.value():
                    green.off()
                    return
            elif color == "yellow":
                if button_yellow.value():
                    yellow.off()
                    return

def twist_potentiometer():
    value = potentiometer.read_u16()
    print(value)
    white.on()

    while True:
        currentValue = potentiometer.read_u16()
        print(currentValue)
        time.sleep(0.2)
        if abs(currentValue - value) > 50000:
            white.off()
            return




while True:

    time.sleep(0.5)

    if count <= 0:
        click_button("red")
        count += 1
    elif count == 1:
        click_button("green")
        count += 1
    elif count == 2:
        click_button("yellow")
        count += 1
    elif count == 3:
        twist_potentiometer()
        count = 0
        



