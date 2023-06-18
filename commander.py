from dataclasses import dataclass
from parsing import parsing_remove_articles, parsing_rough_compare
from messaging import say, message_t, prompt_pause, clear
from gamedata import gamedata_t
from colorama import Fore, Style
from world import place_describe, interact, storage_print_contents, storage_calc_free_space, storage_find_interactable, place_load, InteractableTypes, place_find_interactable
import copy

@dataclass
class command_t:
    keyword: str
    parameters: list[str]=None

master_cmds = [
    command_t("quit"),
    command_t("help"),
    command_t("look around"),
    command_t("check", ["thing"]),
    command_t("pickup", ["thing"]),
    command_t("discard", ["thing in your inventory"]),
    command_t("go", ["to where"]),
    command_t("speak", ["person"])
]

def tp_hub(gamedata=gamedata_t):
    gamedata.place = None

    while(not gamedata.place):
        clear()

        for place in gamedata.world:
            if not place.visible:
                continue

            print(f": {place.name} :")

        print()

        response = input(Fore.GREEN + "Where would you like to go? " + Style.RESET_ALL)
        command_run(f"go {response}", gamedata)

def command_run(inputCmd, gamedata=gamedata_t):
    processed = parsing_remove_articles(inputCmd.lower())

    if not processed:
        return
    
    matchedCmd = None

    for cmd in master_cmds:
        if cmd.keyword == processed[:len(cmd.keyword)].lower() or cmd.keyword == inputCmd:
            matchedCmd = cmd

    if not matchedCmd:
        return

    if matchedCmd.parameters:
        if len(processed) - 1 < len(matchedCmd.parameters):
            return
    
    keywordExcludedPhrase = processed[len(matchedCmd.keyword) + 1:].lower()

    match matchedCmd.keyword:
        case "quit":
            exit()
        case "help":
            for cmd in master_cmds:
                print(f"-- {cmd.keyword}", end=" ")

                if cmd.parameters == None:
                    print()
                    continue

                for param in cmd.parameters:
                    print(f"< {param} >", end=" ")

                print()

            prompt_pause()
        case "look around":
            place_describe(gamedata.place, gamedata)
        case "check":
            if keywordExcludedPhrase == "inventory" or keywordExcludedPhrase == gamedata.storage.name.lower():
                storage_print_contents(gamedata.storage, gamedata)
                return
            
            found = place_find_interactable(gamedata.place, keywordExcludedPhrase)

            if found:
                interact(found, falseInteract=True if found.type == InteractableTypes.PERSON else False, gamedata=gamedata)
                return
            
            say(message_t("There's nothing like that to check."))
            
        case "pickup":
            found = place_find_interactable(gamedata.place, keywordExcludedPhrase)

            if found:
                    sentenceFittedName = (found.name if found.alwaysCapitalized else found.name.lower())
                    
                    if not found.canPickup:
                        say("You can't carry that around with you!")
                        return
                    
                    if gamedata.storage.level < found.storageLevelRequirement:
                        say(message_t(f"The {found.name} was too large to possibly fit into your {gamedata.storage.name.lower()}. Maybe if you had something bigger to put it in.."))
                        return
                    
                    if storage_calc_free_space(gamedata.storage) < found.storageFreeSlotsRequirement:
                        say(message_t(f"You don't have enough room in your {gamedata.storage.name.lower()} for the {sentenceFittedName}."))
                        return
                    say(message_t(f"You picked up the {sentenceFittedName}."))

                    if storage_find_interactable(gamedata.storage, found.name):
                        storage_find_interactable(gamedata.storage, found.name).quantity += 1
                    else:
                        temp = copy.deepcopy(found)
                        temp.quantity = 1

                        gamedata.storage.contents.append(temp)
                    
                    found.quantity -= 1
                    if found.quantity == 0:
                        gamedata.place.interactables.remove(found)

                    return
            say(message_t(f"There's nothing like that to put in your {gamedata.storage.name.lower()}."))
        case "discard":
            if keywordExcludedPhrase == "all" or keywordExcludedPhrase == "everything":
                if len(gamedata.storage.contents) == 0:
                    say(message_t(f"You had nothing in your {gamedata.storage.name.lower()} to throw away.."))
                    return

                say(message_t(f"You threw everything out of your {gamedata.storage.name.lower()}."))

                for i in gamedata.storage.contents:
                    if place_find_interactable(gamedata.place, i.name):
                        place_find_interactable(gamedata.place, i.name).quantity += i.quantity
                    else:
                        gamedata.place.interactables.append(i)

                gamedata.storage.contents.clear()

                return

            found = storage_find_interactable(gamedata.storage, keywordExcludedPhrase)

            if found:
                    sentenceFittedName = (found.name if found.alwaysCapitalized else found.name.lower())
                    
                    say(message_t(f"You threw away the {sentenceFittedName}."))

                    if place_find_interactable(gamedata.place, found.name):
                        place_find_interactable(gamedata.place, found.name).quantity += 1
                    else:
                        gamedata.place.interactables.append(found)
                    
                    found.quantity -= 1
                    if found.quantity == 0:
                        gamedata.storage.contents.remove(found)

                    return
            say(message_t(f"You don't have anything like that in your {gamedata.storage.name.lower()} to throw away.."))
        case "go":
            if keywordExcludedPhrase == "outside":
                say(message_t("You went outside."))
                tp_hub()
                return

            for place in gamedata.world:
                if place.name.lower() == keywordExcludedPhrase and place.visible:
                    say(message_t(f"You went to {place.name}."))
                    gamedata.place = place_load(place)
        case "speak":
            found = place_find_interactable(gamedata.place, keywordExcludedPhrase, [InteractableTypes.PERSON])

            if found:
                interact(found, gamedata=gamedata)
                return
            
            say(message_t("There's nobody here called that to speak to."))