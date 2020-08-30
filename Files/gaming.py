import random

rps_choices = ["rock", "paper", "scissors"]
rps_process = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def rps_classic(choice):
    if choice not in rps_choices:
        return "That isn't a valid move."
    computer_choice = rps_choices[random.randint(0, 2)]
    victory = f"I picked {computer_choice}.\nLooks like "
    if choice.lower() == computer_choice:
        victory += "we tied!"
    elif rps_process[choice.lower()] == computer_choice:
        victory += "you won!"
    else:
        victory += "I won!"
    return victory

# TODO: vote rock paper scissors https://kakegurui.fandom.com/wiki/Vote_Rock-Paper-Scissors

# TODO: nim type zero https://kakegurui.fandom.com/wiki/Nim_Type_Zero

# TODO: m i n e s w e e p e r