import messaging
from messaging import message_t, clear, say, give_choice, charcter_schemes_e
from colorama import Fore, Back, Style
from gamedata import gamedata_t
from world import place_t, place_load, place_find, interactable_t, InteractableTypes
from commander import *

gameData = gamedata_t()

def intro():
    say(message_t("This is a story about " + gameData.name + "."))
    say(message_t(gameData.name + " is a shut-in gamer."))
    say(message_t("He lives alone in a small town, and hasn't left his house in over 10 years."))
    say(message_t(gameData.name + " lives a happy life. He plays video games every day, and never has to work."))
    say(message_t("However, today he found a shocking surprise when he opened his mini-fridge."))
    say(message_t(Fore.RED + "He was out of juice."))
    say(message_t("As carefree as he was, juice was his top pleasure in life."))
    say(message_t("His coffee in the morning."))
    say(message_t("His special someone."))
    say(message_t("His necessity that he couldn't live without."))
    say(message_t(gameData.name + " decides that he has no choice but to go buy some more from the supermarket."))
    say(message_t("But wait! He doesn't remember what the town looks like, or who lives there."))
    say(message_t("Surely it couldn't have changed THAT much in the last 10 years.."))
    say(message_t("Right?"))
    say(message_t("You're mission is to assist " + gameData.name + " in his mission to get juice."))

    say(message_t(Fore.CYAN + "Introducing, " + Fore.YELLOW + "Juice Quest"))
    say(message_t(Fore.CYAN + "By Ralph El Massih"))

intro()
gameData.place = place_load(place_find("Home"))

while(True):
    clear()
    response = input(Fore.GREEN + "What would you like to do? (type 'help' to see a list of commands) " + Style.RESET_ALL)
    command_run(response, gameData)
