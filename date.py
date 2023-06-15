from dataclasses import dataclass
from messaging import message_t, say
from colorama import Fore, Back, Style

@dataclass
class date_t:
    day: int=1

def date_build(date=date_t):
    return str("June " + str(10 + date.day))

def date_out(date=date_t):
    say(message_t("Today is " + Fore.GREEN + date_build(date)))

def date_cycle(date=date_t):
    say(message_t(date_build(date), printPause=0.2), pause=False, reverse=True)
    date.day += 1 
    say(message_t(date_build(date), printPause=0.2), pauseWithPrompt=True)
