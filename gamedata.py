from dataclasses import dataclass, field
from date import date_t
from world import interactable_t, place_t, storage_t, InteractableTypes
from messaging import message_t

@dataclass
class gamedata_t:
    name: str="Bob"
    date: date_t=field(default_factory=date_t)
    place: place_t=None
    placeHistory = []
    storage = storage_t("Pockets", 1, 2)
    world = [
        place_t(
            "Home",
            "your house. It's got white and blue walls, and it's a little rundown. You think to yourself, 'It could definitely use some cleaning'",
            interactables=[
                interactable_t("Playstation 4", InteractableTypes.OBJECT, [
                    message_t("It's an original, launch-day edition."),
                    message_t("You remember hearing about how cool the midnight release was at GameStop from your friends over a discord call."),
                    message_t("You regret pre-ordering it on Amazon..")
                ],
                alwaysCapitalized=True,
                storageLevelRequirement=2,
                alternateNames=["PS4"]
                ),
                interactable_t("Wallet", InteractableTypes.OBJECT, [
                    message_t("It's brown, and made with a choppy leather."),
                    message_t("It's got a single $10 bill inside it, along with a few credit cards.")
                ],
                owner=name,
                quantity=3
                ),
                interactable_t("8-Ball", InteractableTypes.OBJECT, [
                    message_t("This is an 8-Ball")
                ],
                owner="Nobody"
                )
            ],
            visible=True
        ),
        place_t(
            "Bob's House",
            "A funky circus-like house with pop art on the sides, and a big, red nose on the front side of the roof",
            interactables=[
                interactable_t("Bob the Jokesperson", InteractableTypes.PERSON, [
                    message_t("Hey! Wanna hear a joke?"),
                    message_t("Why'd the chicken cross the road?"),
                    message_t("BeCAWWSE!"),
                    message_t("Thanks for listening to my joke. Here's a little reward for your time.", playerReward=interactable_t("Dollar", InteractableTypes.OBJECT, quantity=10))
                ],
                alwaysCapitalized=True,
                ),
            ],
            visible=True
        )
    ]