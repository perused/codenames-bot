import os
import sys
from components.player import Player
from components.spymaster import Spymaster


def get_bot():
    """Find out whether the player is playing as player or spymaster"""
    role = None
    while not role:
        role = input("Are we playing as Spymaster (s) or player (p)? ").lower()
        if "s" in role:
            print("Spymaster selected!")
            return Spymaster()
        elif "p" in role:
            print("Player selected!")
            return Player()
        else:
            print("Invalid input. Please enter 's' for Spymaster or 'p' for player.")

def main(args):
    """Get the role of the bot and begin game"""
    if not os.path.isfile("components/glove300.word_vectors"):
        raise Exception("Please execute the 'setup.sh' bash script before running this program.")
    os.system("clear")
    print("Welcome to the Codenames Bot!\n")
    bot = get_bot()
    if args:
        bot.get_cards_from_file(args[0])
    else:
        bot.populate_board()
    bot.play()


if __name__ == "__main__":
    main(sys.argv[1:])
