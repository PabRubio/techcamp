from fpioa_manager import *
from Maix import GPIO
from board import board_info

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
key = GPIO(GPIO.GPIOHS0, GPIO.PULL_UP)

while True:
    print(key.value())
