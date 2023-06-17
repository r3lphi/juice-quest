from dataclasses import dataclass
from parsing import parsing_remove_list_articles
from messaging import say, message_t, prompt_pause
from gamedata import gamedata_t
from world import place_describe, interact, storage_print_contents, place_load, InteractableTypes

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

def command_run(inputCmd, gamedata=gamedata_t):
    processed = parsing_remove_list_articles(inputCmd.lower().split())

    if not processed:
        return
    
    matchedCmd = None

    for cmd in master_cmds:
        if cmd.keyword == processed[0] or cmd.keyword == inputCmd:
            matchedCmd = cmd

    if not matchedCmd:
        return

    if matchedCmd.parameters:
        if len(processed) - 1 < len(matchedCmd.parameters):
            return

    match matchedCmd.keyword:
        case "quit":
            exit()
        case "help":
            for cmd in master_cmds:
                print("-- " + cmd.keyword, end=" ")
                if cmd.parameters == None:
                    print()
                    continue
                for param in cmd.parameters:
                    print("<" + param + ">", end=" ")
                print()
            prompt_pause()
        case "look around":
            print(gamedata.place == None)
            place_describe(gamedata.place)
        case "check":
            if processed[1].lower() == "inventory" or (processed[1].lower() == gamedata.storage.name.lower() or inputCmd[len(matchedCmd.keyword) + 1:].lower() == gamedata.storage.name.lower()):
                storage_print_contents(gamedata.storage)
                return
            for interactable in gamedata.place.interactables:
                if interactable.name.lower() == processed[1].lower() or interactable.name.lower() == inputCmd[len(matchedCmd.keyword) + 1:].lower():
                    interact(interactable, falseInteract=True if interactable.type == InteractableTypes.PERSON else False)
                    return
            say(message_t("There's nothing like that to check."))
            
        case "pickup":
            for interactable in gamedata.place.interactables:
                if interactable.name.lower() == processed[1].lower() or interactable.name.lower() == inputCmd[len(matchedCmd.keyword) + 1:].lower():
                    sentenceFittedName = (interactable.name if interactable.alwaysCapitalized else interactable.name.lower())
                    if not interactable.canPickup:
                        say("You can't carry that around with you!")
                        return
                    if gamedata.storage.level < interactable.storageLevelRequirement:
                        say(message_t("The " + interactable.name + " was too large to possibly fit into your " + gamedata.storage.name.lower() + ". Maybe if you had something bigger to put it in.."))
                        return
                    if gamedata.storage.capacity - len(gamedata.storage.contents) < interactable.storageFreeSlotsRequirement:
                        say(message_t("You don't have enough room in your " + gamedata.storage.name.lower() + " for the " + sentenceFittedName + "."))
                        return
                    say(message_t("You picked up the " + sentenceFittedName + "."))
                    gamedata.storage.contents.append(interactable)
                    gamedata.place.interactables.remove(interactable)
                    return
            say(message_t("There's nothing like that to put in your " + gamedata.storage.name.lower() + "."))
        case "discard":
            for interactable in gamedata.storage.contents:
                if interactable.name.lower() == processed[1].lower() or interactable.name.lower() == inputCmd[len(matchedCmd.keyword) + 1:].lower():
                    sentenceFittedName = (interactable.name if interactable.alwaysCapitalized else interactable.name.lower())
                    say(message_t("You threw away the " + sentenceFittedName))
                    gamedata.place.interactables.append(interactable)
                    gamedata.storage.contents.remove(interactable)
                    return
            say(message_t("You don't have anything like that in your " + gamedata.storage.name.lower() + " to throw away.."))
        case "go":
            for place in gamedata.world:
                if place.name.lower() == processed[1].lower() or place.name.lower() == inputCmd[len(matchedCmd.keyword) + 1:].lower():
                    say(message_t("You went to " + place.name))
                    gamedata.place = place_load(place)
        case "speak":
            for interactable in gamedata.place.interactables:
                if interactable.type == InteractableTypes.PERSON and (interactable.name.lower() == processed[1].lower() or interactable.name.lower() == inputCmd[len(matchedCmd.keyword) + 1:].lower()):
                    interact(interactable)
                    return
            say(message_t("There's nobody here called that to speak to."))