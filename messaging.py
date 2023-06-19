from dataclasses import dataclass
from enum import Enum
from colorama import Fore, Back, Style
import sys
import time
import os
import random
import inflect
import monstergame

infEngine = inflect.engine()

class charcter_schemes_e:
    NARRATOR: str=Fore.BLUE

@dataclass
class event_invoke_t:
    func_name: str
    func_object: object

@dataclass
class message_t:
    text: str
    color: str=Style.RESET_ALL
    printPause: float=0.025
    playerReward: object=None
    placeReward: str=None
    shallowPrompt: bool=False
    showRewardMsg: bool=True
    eventInvoke: event_invoke_t=None

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

def say(msg=message_t, pause=True, newLine=True, gamedata: object=None):
    clear()
    print(msg.color + msg.text, end="\n" if newLine else "")
    if pause and not msg.shallowPrompt:
        prompt_pause()
    print(Style.RESET_ALL, end="")

    if msg.shallowPrompt:
        response = input(f"{Fore.GREEN}Type your answer here: {Style.RESET_ALL}")
        if not response:
            say(msg, pause, newLine, gamedata)
    if msg.playerReward:
        from world import storage_t, storage_add, interactables_compile
        from gamedata import gamedata_t
        from parsing import parsing_get_article, parsing_generate_quantity

        gamedata = gamedata_t

        if msg.showRewardMsg:
            say(message_t(f"You were gifted {interactables_compile([msg.playerReward], gamedata)}", color=Fore.YELLOW))

        storage_add(gamedata.storage, msg.playerReward, msg.playerReward.quantity)
    if msg.placeReward:
        from world import place_t
        from gamedata import gamedata_t
        gamedata = gamedata_t

        for place in gamedata.world:
            if place.nameFormal.lower() == msg.placeReward.lower():
                place.visible = True
        
        say(message_t(f"Congrats, you've unlocked {place.nameConvo}!", color=Fore.YELLOW))
    
    if msg.eventInvoke:
        found = getattr(msg.eventInvoke.func_object, msg.eventInvoke.func_name)
        if found:
            found()

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
    input(f"{Fore.CYAN}Press any key to continue >>{Style.RESET_ALL}")
