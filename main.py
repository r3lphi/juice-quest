import messaging
from messaging import message_t, clear, say, give_choice, charcter_schemes_e
from colorama import Fore, Back
from gamedata import gamedata_t
from date import date_t, date_cycle, date_build, date_out
from world import place_t, place_load, interactable_t
from commander import *

gameData = gamedata_t()

world = [
    place_t(
        "CP9",
        "a white, raggidy looking house.",
        interactables=[
            interactable_t("Bob The Jokesperson", [
                message_t("Hey there! Wanna hear a joke?")
            ])
        ]
    )
]

active_place = place_load(world[0])

while(True):
    clear()
    response = input("What would you like to do? ")
    command_run(response)
