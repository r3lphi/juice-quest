from dataclasses import dataclass, field
from world import interactable_t, place_t, storage_t, InteractableTypes
from messaging import message_t, event_invoke_t, say, clear
import gamedata
from colorama import Fore, Style

@dataclass
class gamedata_t:
    name: str="Bob"
    place: place_t=None
    placeHistory = []
    storage = storage_t("Pockets", 1)
    world = [
        place_t(
            "Streets",
            "the streets",
            "the streets, you see a lot of greenery, although the streets are surprisingly empty. You don't appreciate the sunshine.",
            entranceLines=[
                message_t("Your eyes are blinded by the radiance of the sunlight as you step outside for the first time in 10 years."),
                message_t("A part of you wants to retreat to the safety of your bedroom, but you perservere, in desperate need of that juice.")
            ],
            paths=[
                "Home",
                "Jerry's House",
                "Karate Club",
                "Library",
                "Sand Pit",
                "Norman's House",
                "Supermarket"
            ],
            listContentsInDescribe=False
        ),
        place_t(
            "Home",
            "your house",
            "your house. It's got white and blue walls, and it's a little rundown. You think to yourself, 'It could definitely use some cleaning'",
            interactables=[
                interactable_t("Playstation 4", InteractableTypes.OBJECT, [
                    message_t("It's an original, launch-day edition."),
                    message_t("You remember hearing about how cool the midnight release was at GameStop from your friends over a discord call."),
                    message_t("You regret pre-ordering it on Amazon..")
                ],
                alwaysCapitalized=True,
                storageLevelRequirement=2,
                alternateNames=["PS4"],
                owner=name
                ),
                interactable_t("Fridge", InteractableTypes.OBJECT, [
                    message_t("It's well-stocked on meats and cereal."),
                    message_t("Your eyes fall over to the side, hoping to find juice that you failed to notice before."),
                    message_t("Alas, you're still out of juice.")
                ],
                canPickup=False,
                owner=name
                )
            ],
            paths=[
                "Streets"
            ]
        ),
        place_t(
            "Jerry's House",
            "Jerry's House",
            "Jerry's house. It's a circus-like house with pop art on the sides, and a big, red nose on the front side of the roof",
            interactables=[
                interactable_t("Jerry the Jokesperson", InteractableTypes.PERSON, [
                    message_t("Hey! Do you like jokes? I love them."),
                    message_t("I love them so much infact, that the 'Jokesperson' part of my name isn't even a nickname, it's on my legal documents."),
                    message_t("My wife didn't find that very amusing though.."),
                    message_t("Anyways, let's see if you can answer my riddle."),
                    message_t("I am yours, yet everybody else uses me more than you."),
                    message_t("What am I?", shallowPrompt=True),
                    message_t("Ha! Not even close."),
                    message_t("Come back when you've got a better guess.")
                ],
                itemReactionLines={
                    "Note of Nechan's Joke Guess": [
                        message_t(f"{Fore.LIGHTBLACK_EX}Jerry looks at the note and begins reading outloud"),
                        message_t("'I am yours, yet everybody else uses me more than you, what am I? My name'"),
                        message_t("Wow, that's exactly right!"),
                        message_t("I'd be a fool if I didn't give you a reward for that."),
                        message_t("Hmm.. let's see now..."),
                        message_t("Oh! I know!"),
                        message_t("It's a little random, but this is a bag I had from back when I was a clown traveling between towns. You may find it useful.", playerReward=interactable_t("Large Sack", InteractableTypes.STORAGE, storageLevelMod=2)),
                        message_t(f"{Fore.LIGHTBLACK_EX}The sack feels very spacious. You could likely fit some moderately large things in it."),
                    ]
                },
                alwaysCapitalized=True
                ),
            ],
            paths=[
                "Streets"
            ]
        ),
        place_t(
            "Karate Club",
            "the karate club",
            "the local karate club. It's a bit run-down from the outside. The paint on the signs and logos look a bit dry, and the windows could use some cleaning",
            interactables=[
                interactable_t("The Monk", InteractableTypes.PERSON, [
                    message_t("...")
                ],
                itemReactionLines={
                    "Pen and Paper": [
                        message_t("The monk writes on the piece of paper:", color=Fore.LIGHTBLACK_EX),
                        message_t("Thanks for that! Now I can communicate with my students and colleges."),
                        message_t("Oh yeah, can you do me a favor?"),
                        message_t(f"I've always wanted to tell {Fore.RED}Jerry the Jokesperson{Fore.WHITE} what I thought the answer to his joke was."),
                        message_t("The monk ripes a corner off the paper and rights a short phrase on it..", color=Fore.LIGHTBLACK_EX),
                        message_t("Please take this to him, and tell him it's from Nechan.", playerReward=interactable_t("Note of Nechan's Joke Guess", InteractableTypes.OBJECT))
                    ]
                }
                )
            ],
            paths=[
                "Streets"
            ]
        ),
        place_t(
            "Library",
            "the library",
            "the library. It's large and fairly fancy looking, albiet a little on the classic side. The place heavily reaks of middle-aged women",
            interactables=[
                interactable_t("Sally the Librarian", InteractableTypes.PERSON, [
                    message_t("SHHHHHH."),
                    message_t("QUIEEETTT!"),
                    message_t("I CAN'T STAND NOISY PEOPLE IN MY LIBRARY."),
                    message_t("HERE, TAKE THIS.", playerReward=interactable_t("Pen and Paper", InteractableTypes.OBJECT))
                ],
                alwaysCapitalized=True
                )
            ],
            paths=[
                "Streets"
            ]
        ),
        place_t(
            "Sand Pit",
            "the sand pit",
            "the sand pit. It's small, but compact. On the right it has a children's slide, on the left a seasaw, and a pair of swings in-between. You notice a kid playing with what looks like a handheld video game console on one end of the seasaw. Your vision has worsened from so many years of late-night gaming sessions in the dark, but you immediately recognize the console as a GameBoy from it's 8-bit audio.",
            interactables=[
                interactable_t("Kid", InteractableTypes.PERSON, rejectionLines=[
                    message_t("Hi there mister. Would you like to play with me?"),
                    message_t("Oh, you don't have a GameBoy? Too bad."),
                    message_t(f"{Fore.LIGHTBLACK_EX}The kid immediately loses interest in you and returns to his game.")
                ],
                interactionRequirements=["GameBoy"],
                interactionLines=[
                    message_t("Oh wow, you've got a GameBoy!"),
                    message_t("Hang on, I've got a link cable, we can have a monster battle."),
                    message_t(f"{Fore.LIGHTBLACK_EX}The kid pulls out a link cable from his pocket and connects each end to a console. His game pops up on your screen and you begin a monster battle."),
                    message_t(f"{Fore.LIGHTBLACK_EX}The battle was very intense. You only had a few heart points left on your last monster and no healing items, but you managed to win."),
                    message_t("Wow, that was a great battle."),
                    message_t("That made me really thirsty though.."),
                    message_t("I'mma go ask my Mom to take me to buy some juice"),
                    message_t("Oh, you wanna know where you can buy some?"),
                    message_t("Just take a right down the road and it's about then minutes from there.", placeReward="Supermarket")
                ]
                )
            ],
            paths=[
                "Streets"
            ],
            listContentsInDescribe=False
        ),
        place_t(
            "Norman's House",
            "Norman's House",
            "Norman's house. His garage is open, and he has several tables setup with boxes stacked on top. You noticed a GameBoy in one of the boxes after scouring through them for a while.",
            entranceLines=[
                message_t("You notice Norman is having a garage sale, and out of instinct, begin scouring for any video games he might have at a throwaway price."),
                message_t("Sure enough, he has a few. A couple of titles catch your eye in particular.."),
                message_t("Mega-Man NES"),
                message_t("Obnoxious People CD"),
                message_t("Oh hey! A GameBoy!")
            ],
            interactables=[
                interactable_t("Norman the Businessman", InteractableTypes.PERSON, interactionLines=[
                    message_t("Hey there, I saw you looking at that GameBoy earlier."),
                    message_t("Tell you what, I'll see it to you for the low, low price of $100,000 dollars."),
                    message_t("$50 in market value, $999,950 in nostalgia ;)"),
                    message_t("I'd also be open to exchanging it for a new-gen console. I'm more of an Xbox guy myself, but I wouldn't mind a PS4 either..")
                ],
                itemReactionLines={
                    "Playstation 4": [
                        message_t("Well, look who came back."),
                        message_t("I'll tell you, you're very lucky to be getting this deal."),
                        message_t("I'm not usually this generous..", playerReward=interactable_t("GameBoy", InteractableTypes.OBJECT), showRewardMsg=False),
                        message_t("You traded your precious PS4 for Norman's GameBoy", color=Fore.YELLOW)
                    ]
                },
                alwaysCapitalized=True
                )
            ],
            paths=[
                "Streets"
            ],
        ),
        place_t(
            "Supermarket",
            "the supermarket",
            "the supermarket, it's a little small, looking more like a convenience store at a supermarket, but besides that, it's exactly what you've dreamed of.",
            entranceLines=[
                message_t("When you arrived at the supermarket, you immediately rushed towards the produce aisle with a trolley on hand. You loaded it up with as much juice as you could fit, and spent everything you had in your wallet on it all."),
                message_t("Yes, even the emergency money you were saving in case your favorite video game franchise suddenly released a new title in the series.."),
                message_t("With this much juice, you'll probably be in retirement before you ever need to come out again."),
                message_t("That, or your inheritence money finally runs dry.."),
                message_t("In any case.."),
                message_t("That's the end!", eventInvoke=event_invoke_t("credits", gamedata)),
            ],
            unlocked=False
        )
    ]

def credits():
    say(message_t(f"Thanks for Playing {Fore.YELLOW}Juice Quest!{Style.RESET_ALL}"))
    exit()