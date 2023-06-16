from dataclasses import dataclass, field
from messaging import message_t, say

@dataclass
class interactable_t:
    name: str
    qualities: str

@dataclass
class place_t:
    name: str
    qualities: str
    entrance_lines: list[message_t]=None
    interactables: list[interactable_t]=None
    visible: bool=True

def place_load(place=place_t):
    if place.entrance_lines:
        for line in place.entrance_lines:
            say(line)
    else:
        if place.qualities:
            say(message_t("You enter " + place.qualities))
