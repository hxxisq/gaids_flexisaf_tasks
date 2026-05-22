"""
Create a Python program that simulates a game of Rock, Paper,
Scissors between the user and the computer. The program must
Define the possible choices, Get the user's choice, Generate
a random choice for the computer, Determine the winner based
on the rules of Rock, Paper, Scissors.

"""
import random


import random

def play_game():
    possible_choices = ["rock", "paper", "scissors"]

    # Mapping what each choice defeats
    wins_against = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    print("\n=== Rock, Paper, Scissors ===")

    # Keep asking until the user inputs a valid choice
    while True:
        user_choice = input("Enter rock, paper, or scissors: ").lower().strip()
        if user_choice in possible_choices:
            break
        print("Invalid choice! Please try again.")

    computer_choice = random.choice(possible_choices)
    print(f"The computer chose: {computer_choice}")

    # Determine the winner
    if user_choice == computer_choice:
        print("It's a tie!")
    elif wins_against[user_choice] == computer_choice:
        print("You win! 🎉")
    else:
        print("Computer wins! 🤖")

# Main game execution loop
if __name__ == "__main__":
    while True:
        play_game()
        again = input("\nDo you want to play again? (y/n): ").lower().strip()
        if again != "y":
            print("Thanks for playing!")
            break
