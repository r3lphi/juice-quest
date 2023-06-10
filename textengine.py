from dataclasses import dataclass
from colorama import Fore, Back, Style
import sys
import time
import os
import random

@dataclass
class Message:
    text: str
    color: str=Style.RESET_ALL
    printPause: float=0.05

def clear():
    if os.name == 'nt':
        os.system('cls')
        return
    os.system('clear')

def say(msg=Message, pause=True, linebreaks=1):
    clear()
    print(msg.color, end="")
    for c in msg.text:
        print(c, end="", flush=True)
        time.sleep(msg.printPause)

    if linebreaks > 0:
        linebreak(linebreaks)
    if pause:
        wait()

    clear()
    print(msg.color + msg.text)

def linebreak(times=1):
    for i in range(0, times):
        print()

def wait():
    input("Press any key to continue >>")