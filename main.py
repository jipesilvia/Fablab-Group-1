from machine import (Pin, ADC, PWM)
import machine
import uasyncio as asyncio
import random


beepTimes = 25
timeToComplete = 3
buzzTime = 0.200
speedinPercentage = 0.85

recursions = 0

previousColor = "nul"
colors = ["green", "red", "yellow", "white"]

potentiometer = machine.ADC(26)

#button_red = Pin(28, Pin.IN, Pin.PULL_DOWN)
button_green = Pin(14, Pin.IN, Pin.PULL_UP)
#button_yellow = Pin(17, Pin.IN, Pin.PULL_DOWN)

pressed = False
failed = False

#red_led = Pin(3, Pin.OUT)
green_led = Pin(15, Pin.OUT)
#yellow_led = Pin(12, Pin.OUT)
#white_led = Pin(0, Pin.OUT)


buzzer = PWM(Pin(16))

async def buzz(frequency: int, duration: float):
    if frequency > 0:
        buzzer.freq(frequency)  # Set frequency
        buzzer.duty_u16(32768)  # 50% duty cycle (half power)
    await asyncio.sleep(duration)
    if frequency > 0:
        buzzer.duty_u16(0)      # Turn buzzer off



async def blink(duration: float, color: str):
    

    if color == "green":
        green_led.on()
        #print("green")
    elif color == "red":
        #red_led.on()
        print("red")
    elif color == "yellow":
        #yellow_led.on()
        print("yellow")
    elif color == "white":
        #hite_led.on()
        print("white")
    else:
        print("error")
        quit()
        
    
    await asyncio.sleep(duration)

    if color == "green":
        green_led.off()
        #print("green")
    elif color == "red":
        #red_led.off()
        print("red")
    elif color == "yellow":
        #yellow_led.off()
        print("yellow")
    elif color == "white":
        #hite_led.off()
        print("white")
    else:
        print("error")
        quit()
        


async def watchButton(button: Pin):
    global pressed, beepTimes, buzzTime
    while True:
        if button.value() == 0:
            if failed: break
            if pressed: break
            print("button pressed!")
            pressed = True

            await asyncio.sleep(buzzTime)
            beepTimes = 25
            buzzTime = 0.2

            await playSuccessfulTune()
            #asyncio.run(main())
            return
            

        await asyncio.sleep_ms(10)



async def playTune(frequencies_and_durations: list[tuple[int, float]]):
    #print(frequencies_and_durations)
    for frequency_and_duration in frequencies_and_durations:
        #print(frequency_and_duration[0])
        await buzz(frequency_and_duration[0], frequency_and_duration[1])
    

async def playSuccessfulTune():
    frequencies_and_durations = [(4000, 0.05),(0, 0.05),(4000, 0.05), (0, 0.05), (4000, 0.05), (0, 0.05), (4000, 0.05), (0, 0.05), (4000, 0.05)]
    await playTune(frequencies_and_durations)

async def playFailTone():
    frequencies_and_durations = [(10000, 2.0),(0, 1.0)]
    await playTune(frequencies_and_durations)

async def blinkAndBuzz(frequency: int, duration: float, color: str):
    await asyncio.gather(buzz(frequency,duration), blink(duration, color))



async def buzzerLoop(color: str):
    global beepTimes, buzzTime, failed
    while True:
        if pressed: break
        if beepTimes <= 0:
            if failed: break
            failed = True
            await playFailTone()
            quit()
            break
        #print("buzz")
        await blinkAndBuzz(1000, buzzTime, color)
        await asyncio.sleep(buzzTime)
        beepTimes -= 1
        buzzTime *= speedinPercentage
    print("buzzerBreak")




async def main():
    global pressed, failed, previousColor, recursions
    
    while True:

        pressed = False
        
        availableColors: list[str] = colors
        
        if previousColor != "nul":
            availableColors.remove(previousColor)
        
        randomIndex = random.randint(0, len(availableColors) - 1)
        color = availableColors[randomIndex]
        color = "green"

        recursions += 1
        print("recursions: ")
        print(recursions)

        await asyncio.gather(buzzerLoop(color), watchButton(button_green))



asyncio.run(main())



