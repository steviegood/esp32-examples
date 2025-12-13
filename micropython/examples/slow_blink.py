from machine import Pin
from utime import sleep

delay = 1         # seconds
pin_number = 5    # pin for LED

led = Pin(pin_number, Pin.OUT)

while True:
    led.on()
    sleep(delay)
    led.off()
    sleep(delay*2)
    
    