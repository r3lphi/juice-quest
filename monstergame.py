from colorama import Fore, Style
from dataclasses import dataclass
from enum import Enum
import random
from random import choice
from parsing import parsing_ownerize

MonsterTypes = Enum('MonsterTypes', ["MELEE", "MAGIC", "TANK", "HEALER"])
MoveTypes = Enum('MoveTypes', ["MELEE", "MAGIC", "GUARD", "HEALING"])

@dataclass
class move_t:
    name: str
    type: MonsterTypes
    damage: int
    maxHit: int=1
    maxUse: int=-1
    uses = 0
    superEffectiveOnTypes: list[MonsterTypes]=None
    accuracy: int=1
    printColor: str=Fore.WHITE

@dataclass
class monster_t:
    name: str
    health: int
    type: MonsterTypes
    moveset: list[move_t]=None

@dataclass
class trainer_t:
    name: str
    team: list[monster_t]
    activeMonster: monster_t=None

#Hardcoded the teams in this case just because why not.
ai = trainer_t("Kid", [
    monster_t("Doomsday Dragon", 50, MonsterTypes.TANK, [
        move_t("Blast Breath", MoveTypes.MAGIC, 10, printColor=Fore.LIGHTRED_EX),
        move_t("Dragon's Whiplash", MoveTypes.MELEE, 10, printColor=Fore.BLUE),
        move_t("Defense Curl", MoveTypes.GUARD, 0, printColor=Fore.LIGHTBLACK_EX),
        move_t("Destroyer Beam", MoveTypes.MAGIC, 40, maxUse=1, printColor=Fore.RED)
    ]),
    monster_t("Half-Fallen Archangel", 30, MonsterTypes.HEALER, [
        move_t("Blessed Shield", MoveTypes.GUARD, 0),
        move_t("Benten's Prayer", MoveTypes.HEALING, 10),
        move_t("Winged Assault", MoveTypes.MELEE, 10),
        move_t("Cursed Kiss", MoveTypes.MAGIC, 20, maxUse=1, printColor=Fore.BLACK)
    ]),
    monster_t("White Knight", 20, MonsterTypes.MELEE, moveset=[
        move_t("Pure Jest Series", MoveTypes.MELEE, 3,  maxHit=8),
        move_t("Breakneck Blitz", MoveTypes.MELEE, 15, maxUse=3, printColor=Fore.LIGHTYELLOW_EX),
        move_t("Valiant Stance", MoveTypes.GUARD, 0),
        move_t("Corkscrew Crash", MoveTypes.MELEE, 20, maxUse=1, printColor=Fore.YELLOW)
    ])
])
me = trainer_t("You", [
    monster_t("Inferno Swordsmen", 20, MonsterTypes.MELEE, [
        move_t("Phoenix Slice", MoveTypes.MELEE, 10, printColor=Fore.LIGHTRED_EX),
        move_t("Daigo Defend", MoveTypes.GUARD, 0),
        move_t("Sinful Scorch Spread", MoveTypes.MELEE, 4, maxHit=5, printColor=Fore.LIGHTMAGENTA_EX),
        move_t("Light That Burns The Sky", MoveTypes.MAGIC, 20, maxUse=1, superEffectiveOnTypes=[MonsterTypes.TANK], printColor=Fore.MAGENTA)
    ]),
    monster_t("Warhead Dinosaur", 35, MonsterTypes.TANK, [
        move_t("Earth Crusher", MoveTypes.MELEE, 12, printColor=Fore.LIGHTGREEN_EX),
        move_t("Tail Smash", MoveTypes.MELEE, 10),
        move_t("Horn Drill", MoveTypes.MELEE, 50, accuracy=0.1, printColor=Fore.LIGHTBLACK_EX),
        move_t("Nuclear Winner", MoveTypes.MELEE, 35, maxHit=1, printColor=Fore.GREEN)
    ]),
    monster_t("Starborn Warlock", 30, MonsterTypes.MAGIC, [
        move_t("Star of Saber", MoveTypes.MAGIC, 15, printColor=Fore.YELLOW),
        move_t("Gravity Crush", MoveTypes.MAGIC, 15, printColor=Fore.MAGENTA),
        move_t("Freeze Frame", MoveTypes.MAGIC, 15, printColor=Fore.LIGHTBLUE_EX),
        move_t("End of Time and Space", MoveTypes.MAGIC, 35, maxUse=1, printColor=Fore.LIGHTCYAN_EX)
    ])
])

def move_use(move=move_t, using_monster=monster_t, user=trainer_t, opposing_monster=monster_t, opponent=trainer_t):
    from messaging import prompt_pause, clear

    if move.uses >= move.maxUse and move.maxUse > 0:
        return
    
    clear()

    print(f"{using_monster.name} used {move.name} on {opposing_monster.name}.")

    if move.maxHit > 1:
        hitTimes = random.random() * move.maxHit

        for i in range(0, int(hitTimes)):
            if i + 1 > 1:
                print(f"Hit {i} times")
            else:
                print("Hit once.")
            prompt_pause()
    else:
        prompt_pause()

    move.uses += 1
    opposing_monster.health -= move.damage

    if opposing_monster.health <= 0:
        temp = opposing_monster.name

        opponent.team.remove(opposing_monster)
        opponent.activeMonster = random.choice(opponent.team)

        clear()
        print(f"{opponent.name}'s {temp} fainted.")
        prompt_pause()

        clear()
        print(f"{opponent.name} sent out {opponent.activeMonster.name}!")
        prompt_pause()
        return
    
    move_use(random.choice(opponent.activeMonster.moveset), opponent.activeMonster, opponent, user.activeMonster, user)

def begin_battle(user=trainer_t, opponent=trainer_t):
    from messaging import clear

    user.activeMonster = random.choice(user.team)
    opponent.activeMonster = random.choice(opponent.team)

    while(True):
        clear()

        print(f"{Fore.YELLOW}{user.activeMonster.name} {Fore.WHITE}<HP: {user.activeMonster.health}> {Fore.LIGHTMAGENTA_EX}(you){Style.RESET_ALL}")
        print("vs.")
        print(f"{Fore.RED}{opponent.activeMonster.name} {Fore.WHITE}<HP: {opponent.activeMonster.health}>")

        choice = input(f"{Fore.GREEN}What would you like to do? (Fight/Heal/Switch){Style.RESET_ALL} ")

        match choice.lower():
            case "fight":
                while(True):
                    clear()
                    for move in user.activeMonster.moveset:
                        print(f"{move.printColor}{move.name} <TYPE: {move.type}> <DAMAGE: {move.damage}>")
                    print(Style.RESET_ALL)
                    moveSelect = input("Please select a move: ")

                    selectedMove = None

                    for move in user.activeMonster.moveset:
                        if moveSelect.lower() == move.name.lower():
                            selectedMove = move
                    
                    if selectedMove:
                        move_use(selectedMove, user.activeMonster, user, opponent.activeMonster, opponent)
