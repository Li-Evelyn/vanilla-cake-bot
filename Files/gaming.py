import random

rps_choices = ["rock", "paper", "scissors"]
rps_process = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def rps_classic(choice):
    computer_choice = rps_choices[random.randint(0, 2)]
    victory = f"I picked {computer_choice}.\nLooks like "
    if choice.lower() == computer_choice:
        victory += "we tied!"
    elif rps_process[choice.lower()] == computer_choice:
        victory += "you won!"
    else:
        victory += "I won!"
    return victory