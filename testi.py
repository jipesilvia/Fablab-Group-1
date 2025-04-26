from machine import (Pin, ADC)
import machine
import time
import uasyncio as asyncio

button_green = Pin(14, Pin.IN, Pin.PULL_UP)

green = Pin(15, Pin.OUT)

buzzer = Pin(16, Pin.OUT)

async def playSound(arrayOfIntervals_ms: list[float]):
    print(arrayOfIntervals_ms)
    for interval in arrayOfIntervals_ms:
        print(interval)
        time.sleep(interval)
        buzzer.toggle()
    
    buzzer.off()

async def playSuccessfulSound():
    arrayOfIntervals = [0.0, 0.1, 0.1, 0.1, 0.1, 0.2]
    await playSound(arrayOfIntervals)



async def vittu():
    buzzer.on()

async def nappi():
    while True:
        if not button_green.value():
            print("button pressed")
            buzzer.off()
            await playSuccessfulSound()
            await asyncio.sleep(1)
            asyncio.run(main())
        await asyncio.sleep(0.1)


async def main():
    await asyncio.gather(vittu(), nappi())


asyncio.run(main())


    


