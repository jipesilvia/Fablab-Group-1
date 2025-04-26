from machine import (Pin, ADC, PWM)
import machine
import time
import uasyncio as asyncio


beepTimes = 25
timeToComplete = 3
buzzTime = 0.200
speedinPercentage = 0.85




#button_red = Pin(28, Pin.IN, Pin.PULL_DOWN)
button_green = Pin(14, Pin.IN, Pin.PULL_UP)
#button_yellow = Pin(17, Pin.IN, Pin.PULL_DOWN)

pressed = False
failed = False

#red = Pin(3, Pin.OUT)
green = Pin(15, Pin.OUT)
#yellow = Pin(12, Pin.OUT)
#white = Pin(0, Pin.OUT)

#buzzer = Pin(16, Pin.OUT)


buzzer = PWM(Pin(16))

async def buzz(frequency, duration):
    if frequency > 0:
        buzzer.freq(frequency)  # Set frequency
        buzzer.duty_u16(32768)  # 50% duty cycle (half power)
    await asyncio.sleep(duration)
    if frequency > 0:
        buzzer.duty_u16(0)      # Turn buzzer off

async def blink(duration):
    green.on()
    await asyncio.sleep(duration)
    green.off()


async def watchButton():
    global pressed, beepTimes, buzzTime
    while True:
        if button_green.value() == 0:
            if failed: break
            if pressed: break
            print("button pressed!")
            pressed = True

            await asyncio.sleep(buzzTime)
            beepTimes = 25
            buzzTime = 0.2

            await playSuccessfulTune()
            asyncio.run(main())
            break
            

        await asyncio.sleep_ms(10)



async def playTune(frequencies_and_durations: list[tuple[int, float]]):
    #print(frequencies_and_durations)
    for frequency_and_duration in frequencies_and_durations:
        print(frequency_and_duration[0])
        await buzz(frequency_and_duration[0], frequency_and_duration[1])
    

async def playSuccessfulTune():
    frequencies_and_durations = [(4000, 0.05),(0, 0.05),(4000, 0.05), (0, 0.05), (4000, 0.05), (0, 0.05), (4000, 0.05), (0, 0.05), (4000, 0.05)]
    await playTune(frequencies_and_durations)

async def playFailTone():
    frequencies_and_durations = [(10000, 2.0),(0, 1.0)]
    await playTune(frequencies_and_durations)

async def blinkAndBuzz(frequency, duration):
    await asyncio.gather(buzz(frequency,duration), blink(duration))



async def buzzerLoop():
    global beepTimes, buzzTime, failed
    while True:
        if pressed:
            break
        if beepTimes <= 0:
            if failed: break
            failed = True
            await playFailTone()
            quit()
            break
        print("buzz")
        await blinkAndBuzz(1000, buzzTime)
        await asyncio.sleep(buzzTime)
        beepTimes -= 1
        buzzTime *= speedinPercentage
    print("buzzerBreak")




async def main():
    global pressed, failed
    pressed = False
    if failed: quit()

    await asyncio.gather(buzzerLoop(), watchButton())


asyncio.run(main())



