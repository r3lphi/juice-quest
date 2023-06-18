from dataclasses import dataclass, field
from messaging import message_t, say, clear
from parsing import parsing_generate_articled, vowels, parsing_ownerize, parsing_rough_compare, parsing_generate_quantity
from enum import Enum
from colorama import Fore, Back, Style
import inflect

InteractableTypes = Enum('InteractableTypes', ['PERSON', 'OBJECT'])

infEngine = inflect.engine()

@dataclass
class interactable_t:
    name: str
    type: InteractableTypes
    interactionLines: list[message_t]=None
    itemReactionLines = {}
    alwaysCapitalized: bool=True if type == InteractableTypes.PERSON else False
    canPickup: bool=True if type != InteractableTypes.PERSON else False
    storageLevelRequirement: int=1
    storageFreeSlotsRequirement: int=1
    alternateNames: list[str]=None
    owner: str=None
    quantity: int=1

def interact(interactable=interactable_t, falseInteract=False, gamedata=None):
    if not interactable.interactionLines:
        say(f"You find nothing worth mentioning about the {interactable.name}.")
        return
    
    _name = interactable.name if interactable.alwaysCapitalized else interactable.name.lower()

    if falseInteract:
        say(message_t(f"You 'check out' {interactable.name}."))
        say(message_t(f"{interactable.name} looks at you funny."))
        return

    if interactable.type != InteractableTypes.PERSON:
        say(message_t(f"You take a closer look at the {_name}.."))

    for line in interactable.interactionLines:
        say(line, gamedata)

def interactables_compile(list, gamedata):
    if not list:
        return "nothing.."

    built = ""
    k = 0
    for interactable in list:
        if k == len(list) - 1 and len(list) > 1:
            built += "and "
        
        if interactable.type != InteractableTypes.PERSON:
            if interactable.owner:
                built += parsing_ownerize(interactable.owner, gamedata) + " "
                
                if interactable.quantity > 1:
                    built += parsing_generate_quantity(interactable.name, interactable.quantity)
            else:
                built += parsing_generate_quantity(interactable.name, interactable.quantity)
            
        if interactable.quantity > 1:
            built += infEngine.plural(interactable.name) if interactable.alwaysCapitalized else infEngine.plural(interactable.name.lower())
        else:
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
    visible: bool=False

def place_load(place=place_t):
    if place.entranceLines:
        for line in place.entranceLines:
            say(line)
    return place

def place_describe(place=place_t, gamedata=None):
    say(message_t(f"You look around {place.qualities}. In it you see {interactables_compile(place.interactables, gamedata)}"))

def place_find_interactable(place=place_t, query=str, typemask=None):
    suspect = None
    for interactable in place.interactables:
        if typemask:
            if interactable.type not in typemask:
                continue
        
        if interactable.name == query:
            return interactable
        
        if interactable.alternateNames:
            for alt in interactable.alternateNames:
                if alt.lower() == query:
                    return interactable

        if parsing_rough_compare(interactable.name, query):
            suspect = interactable
    if suspect:
        return suspect

@dataclass
class storage_t:
    name: str
    level: int
    capacity: int
    contents = []

def storage_print_contents(storage=storage_t, gamedata=None):
    say(message_t(f"You take a look into your {storage.name.lower()}. You find {interactables_compile(storage.contents, gamedata)}"))

def storage_calc_free_space(storage=storage_t):
    taken = 0
    for i in storage.contents:
        taken += i.quantity * i.storageFreeSlotsRequirement
    return storage.capacity - taken

def storage_find_interactable(storage=storage_t, query=str):
    suspect = None
    for interactable in storage.contents:        
        if interactable.name == query:
            return interactable
        
        if interactable.alternateNames:
            for alt in interactable.alternateNames:
                if alt.lower() == query:
                    return interactable

        if parsing_rough_compare(interactable.name, query):
            suspect = interactable
    if suspect:
        return suspect

def storage_add(storage=storage_t, i=interactable_t):
    if storage_calc_free_space(storage) < i.storageFreeSlotsRequirement * i.quantity:
        return

    lf = storage_find_interactable(storage, i.name)
    if lf:
        lf.quantity += 1
        return
    storage.contents.append(i)
