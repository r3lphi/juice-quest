from dataclasses import dataclass
from colorama import Fore, Back, Style
import sys
import time
import os
import random

@dataclass
class message_t:
    text: str
    color: str=Style.RESET_ALL
    printPause: float=0.05

def clear():
    if os.name == 'nt':
        os.system('cls')
        return
    os.system('clear')

def say(msg=message_t, pauseWithPrompt=False, linebreaks=1):
    clear()
    print(msg.color + msg.text)
    
    if pauseWithPrompt:
        promptPause()
        if linebreaks > 0:
            linebreak(msg.printPause)
    else:
        input()

def slow_say(msg=message_t, pauseWithPrompt=False, linebreaks=1):
    clear()
    print(msg.color, end="")
    for c in msg.text:
        print(c, end="", flush=True)
        time.sleep(msg.printPause)

    if pauseWithPrompt:
        promptPause()
        if linebreaks > 0:
            linebreak(msg.printPause)
    else:
        input()

def linebreak(times=1):
    for i in range(0, int(times + 1)):
        print()

def promptPause():
    input("Press any key to continue >>")
