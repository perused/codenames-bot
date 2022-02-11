import os
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


def main():
    """Get the role of the bot and begin game"""
    if not os.path.isfile("glove300.word_vectors"):
        print("When running codenames bot for the first time, a one-off download is required.")
        model = gensim.downloader.load('glove-wiki-gigaword-300')
        model.save(os.path.join("glove300.word_vectors"))
    os.system("clear")
    print("Welcome to the Codenames Bot!\n")
    bot = get_bot()
    bot.populate_board()
    bot.play()


if __name__ == "__main__":
    main()
