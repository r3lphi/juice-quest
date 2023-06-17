from dataclasses import dataclass, field
from messaging import message_t, say
from parsing import parsing_generate_articled, vowels, parsing_ownerize
from enum import Enum

InteractableTypes = Enum('InteractableTypes', ['PERSON', 'OBJECT'])

@dataclass
class interactable_t:
    name: str
    type: InteractableTypes
    interactionLines: list[message_t]=None
    rejectionLines: list[message_t]=None
    interactionItemRequirements: list[str]=None
    alwaysCapitalized: bool=True if type == InteractableTypes.PERSON else False
    canPickup: bool=True if type != InteractableTypes.PERSON else False
    storageLevelRequirement: int=1
    storageFreeSlotsRequirement: int=1
    owner: str=None

def interact(interactable=interactable_t, falseInteract=False):
    if not interactable.interactionLines:
        say("You find nothing worth mentioning about the " + interactable.name + ".")
        return
    
    _name = interactable.name if interactable.alwaysCapitalized else interactable.name.lower()

    if falseInteract:
        say(message_t("You 'check out' " + interactable.name + "."))
        say(message_t(interactable.name + " looks at you funny."))
        return

    if interactable.type != InteractableTypes.PERSON:
        say(message_t("You take a closer look at the " + _name + ".."))

    for line in interactable.interactionLines:
        say(line)

def interactables_compile(list):
    if not list:
        return "nothing.."

    built = ""
    k = 0
    for interactable in list:
        if k == len(list) - 1 and len(list) > 1:
            built += "and "
        
        if interactable.type != InteractableTypes.PERSON:
            if interactable.owner:
                built += parsing_ownerize(interactable.owner) + " "
            else:
                if interactable.name[0] in vowels:
                    built + "an "
                else:
                    built += "a "
    
        built += interactable.name if interactable.alwaysCapitalized else interactable.name.lower()
        
        if k < len(list) - 1:
            built += ", "
        
        k += 1  
    return built + "."

@dataclass
class place_t:
    name: str
    qualities: str
    entranceLines: list[message_t]=None
    interactables: list[interactable_t]=None
    visible: bool=True

def place_load(place=place_t):
    if place.entranceLines:
        for line in place.entranceLines:
            say(line)
    return place

def place_describe(place=place_t):
    say(message_t("You look around " + place.qualities + " In it you see " + interactables_compile(place.interactables)))

@dataclass
class storage_t:
    name: str
    level: int
    capacity: int
    contents = []

def storage_print_contents(storage=storage_t):
    say(message_t("You take a look into your " + storage.name.lower() + ". You find " + interactables_compile(storage.contents)))
