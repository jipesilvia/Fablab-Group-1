from machine import (Pin, ADC, PWM)
import uasyncio as asyncio
import random


beepTimes = 25
timeToComplete = 3
buzzTime = 0.200
speedinPercentage = 0.85
potSpeedingPercentage = 0.95

recursions = 0

previousColor = "nul"
colors = ["green", "red", "yellow", "white"]

potentiometer = ADC(26)

potTarget = -1
POT_RANGE = 0.08

button_red = Pin(0, Pin.IN, Pin.PULL_UP)
button_green = Pin(12, Pin.IN, Pin.PULL_UP)
button_yellow = Pin(13, Pin.IN, Pin.PULL_UP)

pressed = False
failed = False

red_led = Pin(1, Pin.OUT)
green_led = Pin(14, Pin.OUT)
yellow_led = Pin(16, Pin.OUT)
white_led = Pin(15, Pin.OUT)


buzzer = PWM(Pin(10))

async def buzz(frequency: int, duration: float):
    duty = int(65535 * 0.5)
    if frequency > 0:
        buzzer.freq(frequency)  # Set frequency
        buzzer.duty_u16(duty)  # 50% duty cycle (half power)
    await asyncio.sleep(duration)
    if frequency > 0:
        buzzer.duty_u16(0)      # Turn buzzer off



async def blink(duration: float, color: str):

    if color == "green":
        green_led.on()
        #print("green")
    elif color == "red":
        red_led.on()
        #print("red")
    elif color == "yellow":
        yellow_led.on()
        #print("yellow")
    elif color == "white":
        white_led.on()
        #print("white")
    else:
        print("error")
        quit()
        
    
    await asyncio.sleep(duration)

    if color == "green":
        green_led.off()
        #print("green")
    elif color == "red":
        red_led.off()
        #print("red")
    elif color == "yellow":
        yellow_led.off()
        #print("yellow")
    elif color == "white":
        white_led.off()
        #print("white")
    else:
        print("error")
        quit()
        


async def watchButton(button: Pin):
    global pressed, beepTimes, buzzTime, speedinPercentage
    while True:
        if button.value() == 0:
            if failed: break
            if pressed: break
            print("button pressed!")
            pressed = True

            await asyncio.sleep(buzzTime)
            buzzTime = 0.2
            speedinPercentage *= 0.95
            print(speedinPercentage)

            await playSuccessfulTune()
            return
            

        await asyncio.sleep_ms(10)

async def watchPot():
    global buzzTime, speedinPercentage, potSpeedingPercentage, beepTimes, pressed

    counter = 0
    while True:
        if failed: return
        if isInRange():
            if counter >= int(potSpeedingPercentage*20):
                if pressed: break
                pressed = True
                await asyncio.sleep(buzzTime)
                buzzTime = 0.2
                potSpeedingPercentage *= 0.95
                await playSuccessfulTune()
                
                return
            counter += 1
        else:
            pressed = False
            counter = 0
        print(counter)
        await asyncio.sleep_ms(10)


async def playTune(frequencies_and_durations: list[tuple[int, float]]):
    #print(frequencies_and_durations)
    for frequency_and_duration in frequencies_and_durations:
        #print(frequency_and_duration[0])
        await buzz(frequency_and_duration[0], frequency_and_duration[1])
        

async def playSuccessfulTune():
    frequencies_and_durations = [(4000, 0.05),(0, 0.05),(4000, 0.05), (0, 0.05), (4000, 0.05), (0, 0.05), (4000, 0.05), (0, 0.05), (4000, 0.05)]
    await playTune(frequencies_and_durations)

async def playStartTune():
    fAndDs = [(4000, 0.5),(0,0.5),(4000, 0.5),(0,0.5),(4000, 0.5)]
    await playTune(fAndDs)

async def playFailTone():
    frequencies_and_durations = [(10000, 2.0),(0, 1.0)]
    await playTune(frequencies_and_durations)

async def blinkAndBuzz(frequency: int, duration: float, color: str):
    await asyncio.gather(buzz(frequency,duration), blink(duration, color))

def getPotValue():
    rawValue = potentiometer.read_u16()
    pm_max_value = 66000

    normalizedValue = rawValue/pm_max_value

    if normalizedValue > 1: return 1

    return normalizedValue

def getFrequency(randomValue, value):    
    MIN_FREQUENXY = 1000
    MAX_FREQUENXY = 5000



    targetRange = [randomValue - POT_RANGE, randomValue + POT_RANGE]
    if isInRange():
        return MAX_FREQUENXY
    else:
        return MIN_FREQUENXY
    
    if value > targetRange[0] - 0.25 and value < targetRange[1] + 0.25:
        distance = 0
        if value < targetRange[0]:
            distance = targetRange[0] - value
        elif value > targetRange[1]:
            distance = value - targetRange[1]
        else:
            print("error in gf")
            quit()
        normalizedDistance = distance/0.25
        frequencyRange = MAX_FREQUENXY - MIN_FREQUENXY
        frequency = int(MIN_FREQUENXY + frequencyRange*normalizedDistance)
        return MIN_FREQUENXY
    else:
        return MIN_FREQUENXY
        
        
def isInRange():
    potValue = getPotValue()
    if potValue >= potTarget - POT_RANGE and potValue <= potTarget + POT_RANGE:
        return True
    return False


async def buzzerLoop(color: str):
    global beepTimes, buzzTime, failed, potTarget, speedinPercentage
    potTarget = -1
    if color == "white": 
        potTarget = random.random()
        if isInRange():
            if potTarget > 0.5:
                potTarget -= 0.25
            else:
                potTarget += 0.25
        beepTimes = 50
        #speedinPercentage = 0.95
    else:
        beepTimes = 25
    
    print(potTarget)
    #potTarget = 0.5
    while True:
        if pressed: break
        if beepTimes <= 0:
            if failed: break
            failed = True
            await playFailTone()
            quit()
            break
        #print("buzz")
        if potTarget == -1:
            await blinkAndBuzz(1000, buzzTime, color)
            buzzTime *= speedinPercentage
        else:
            await blinkAndBuzz(getFrequency(potTarget, getPotValue()), buzzTime, color)
            buzzTime *= potSpeedingPercentage
        await asyncio.sleep(buzzTime)
        beepTimes -= 1
        
    print("buzzerBreak")




async def main():
    global pressed, failed, previousColor, recursions, potTarget
    await playStartTune()
    await asyncio.sleep(1)
    while True:

        pressed = False
        
        availableColors: list[str] = colors[:]
        
        if previousColor != "nul":
            availableColors.remove(previousColor)
        
        randomIndex = random.randint(0, len(availableColors) - 1)
        color = availableColors[randomIndex]
        previousColor = color


        button = button_green

        #color = "white"

        print(color)

        if color == "green": button = button_green
        elif color == "red": button = button_red
        elif color == "yellow": button = button_yellow
        elif color == "white":
            await asyncio.gather(buzzerLoop(color), watchPot())
            continue

        await asyncio.gather(buzzerLoop(color), watchButton(button))



asyncio.run(main())



