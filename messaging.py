from dataclasses import dataclass
from enum import Enum
from colorama import Fore, Back, Style
import sys
import time
import os
import random

class charcter_schemes_e:
    NARRATOR: str=Fore.BLUE

@dataclass
class message_t:
    text: str
    color: str=Style.RESET_ALL
    printPause: float=0.025

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

# def say(msg=message_t, pause=True, pauseWithPrompt=False, instant=False, linebreaks=1, reverse=False):
#     if instant:
#         clear()
#         print(msg.color + msg.text)
#     else:
#         if reverse:
#             out = msg.text
#             for i in range(len(msg.text) + 1):
#                 clear()
#                 print(msg.color + out)
#                 out = out[:-1]
#                 time.sleep(msg.printPause)
#                 flush_input_buffer()
#         else:
#             out = ""
#             for c in msg.text:
#                 out += c
#                 clear()
#                 print(msg.color + out)
#                 time.sleep(msg.printPause)
#                 flush_input_buffer()
#     if pauseWithPrompt:
#         prompt_pause()
#         if linebreaks > 0:
#             linebreak(msg.printPause)
#     elif pause:
#         input()

def say(msg=message_t, pause=True, newLine=True):
    clear()
    print(msg.color + msg.text, end="\n" if newLine else "")
    if pause:
        prompt_pause()
    print(Style.RESET_ALL, end="")

def give_choice(question=message_t, options=list[message_t]):
    clear()
    print(question.color + question.text)
    
    k = 1
    for option in options:
        print(Style.RESET_ALL + str(k) + " -> " + option.color + option.text)
        k += 1

    response = input()

    # Selection by index
    if response.isnumeric():
        if int(response) <= len(options) and int(response) > 0:
            return options[int(response) - 1].text

    # Selection by match
    for option in options:
        if response.lower() == option.text.lower():
            return option.text
    give_choice(question, options)


def linebreak(times=1):
    for i in range(0, int(times + 1)):
        print()

def prompt_pause():
    input(Fore.CYAN + "Press any key to continue >>" + Style.RESET_ALL)
