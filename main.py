import messaging
from messaging import message_t, say, give_choice, charcter_schemes_e
from colorama import Fore, Back
from gamedata import gamedata_t
from date import date_t, date_cycle, date_build, date_out
from places import place_t, place_load

gameData = gamedata_t()

def scene_prologue():
    say(message_t("Why do people steal?"))
    say(message_t("Is it my carelessness that caused this?"))
    say(message_t("Because even when I choose to accept that as my one and only answer, I don't understand.."))
    say(message_t("I don't understand why I can't feel any better about it?"))
    say(message_t("Why can't I shake this feeling?"))
    say(message_t("This feeling of pure, unwavering anger?"))
    say(message_t("Why do I feel the desire to " + Fore.RED + "%!##" + Fore.WHITE + "?"))
    say(message_t("..."))
    say(message_t("It was the perfect crime."))
    say(message_t("No traces left behind, and no leads."))
    say(message_t("And yet, I look at the person I think stole it, and I despair in the fact that, even knowing he did it, I could never pin anything on him."))
    say(message_t("A peaceful rage drives me to do something about it, to expose him."))
    say(message_t("Whether I'll embarass him, or crush him in my own pitfall depends on one thing."))
    say(message_t("Whether or not I can take back what he stole from me using my head, before the emotions in my heart break free, marking both, or just one of our downfalls."))
    say(message_t("You do not know what it is he stole, or why I feel so much rage towards this unfortunately brutal world."))
    say(message_t("This world, even in the most honest and utopian places, will always house people that wish to inflict pain on others."))
    say(message_t("I do not ask for your guidance, nor your presence."))
    say(message_t("But in the end, you will witness one of two things:"))
    say(message_t("The conclusion to my struggle.."))
    say(message_t("Or the anthem of my doom."))

    date_out(gameData.date)

def scene_bedroom_one():
    say(message_t("You wake up to a familiar ceiling, drenched in old, white coating.."))
    say(message_t("You want to cry."))
    say(message_t("You're not sure why, but you don't want to leave your room."))
    say(message_t("You're just lying there on your bed, with your head facing towards your bedroom door."))
    say(message_t("You don't feel anger. You still want to cry, but you're not sad."))
    say(message_t("Oh, I understand."))
    say(message_t("You just want an excuse."))
    say(message_t("You want an excuse to forget the world around you, and release those emotions knotting your heart."))
    say(message_t("You're tired."))
    say(message_t("You want to kick and scream and loath the world at the expense of others."))
    say(message_t("You just want to quit."))
    
    choice = give_choice(message_t(charcter_schemes_e.NARRATOR + "So tell me, would you like to quit?"), [message_t("Yes"), message_t("No")])
    match choice:
        case "Yes":
            say(message_t("You give up."))
            say(message_t("You give up.."))
            say(message_t("You give up..."))

# Main Loop
scene_bedroom_one()
