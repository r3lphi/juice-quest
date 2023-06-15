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

def flush_input_buffer():
    if os.name == 'nt':
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
        return
    from termios import tcflush, TCIOFLUSH
    tcflush(sys.stdin, TCIOFLUSH)

def say(msg=message_t, pause=True, pauseWithPrompt=False, instant=False, linebreaks=1, reverse=False):
    if instant:
        clear()
        print(msg.color + msg.text)
    else:
        if reverse:
            out = msg.text
            for i in range(len(msg.text) + 1):
                clear()
                print(msg.color + out)
                out = out[:-1]
                time.sleep(msg.printPause)
                flush_input_buffer()
        else:
            out = ""
            for c in msg.text:
                out += c
                clear()
                print(msg.color + out)
                time.sleep(msg.printPause)
                flush_input_buffer()
    if pauseWithPrompt:
        prompt_pause()
        if linebreaks > 0:
            linebreak(msg.printPause)
    elif pause:
        input()

def linebreak(times=1):
    for i in range(0, int(times + 1)):
        print()

def prompt_pause():
    input("Press any key to continue >>")
