import os
import time
import sys
# try:
#     from gensim.models import KeyedVectors
# except:
#     raise Exception("Please execute the 'setup.sh' bash script before running this program.")

class Bot:
    def __init__(self):
        board = [[None]*4 for i in range(4)]

    def populate_board(self):
        print("\nPopulating game board works as follows: Enter the name of the card (and if bot is spymaster, the type of the card too) starting from the top left and going across to the right before going down a row.\n\nCard types: red ('r'), blue ('b'), neutral ('n'), black ('black')\n\ne.g bot is spymaster: 'mountain red'\ne.g bot is player: 'mountain'\n")
        colours = ["red", "r", "blue", "b", "neutral", "n", "black"]
        for i in range(4):
            for j in range(4):
                while True:
                    entry = input("Enter name and card type (r, b, n, black) ('q' to quit): ").lower()
                    if entry == "q":
                        sys.exit()
                    try:                        
                        card, colour = entry.split()
                    except:
                        print("Invalid. Please enter two words for 'card' and 'colour'")
                        continue
                    if colour not in colours:
                        print("Invalid colour, try again.")
                        continue
                    confirm = input(f"\nConfirming card = '{card}' and colour = {colour}? (Press ENTER for yes, any other key for no)")
                    if confirm != "\n":
                        print("Confirmed.")
                        time.sleep(1)
                        break
                    else:
                        print("Cancelled.")
                        continue
                self.print_board()
                    




    def play(self):
        pass

    def get_best_spymaster_move(self, team):
        pass

    def get_best_player_guess(self, clue):
        pass

    def print_board(self):
        os.system("clear")
        print("Current board:")
        for i in range(4):
            for j in range(4):
                print(f"{self.board[i][j]} ", end="")
            print()

# find out whether bot is playing as spymaster or player
def get_role():
    role = None
    while not role:
        role = input("Are we playing as Spymaster (s) or player (p)? ").lower()
        if "s" in role:
            role = "s"
        elif "p" in role:
            role = "p"
        else:
            print("Invalid input. Please enter 's' for Spymaster or 'p' for player.")
    print()
    os.system("clear")
    print(f'{"Spymaster" if role == "s" else "Player"} selected!')
    time.sleep(1)
    return role

def main():
    # check requirements
    # if not os.path.isfile("glove300.word_vectors"):
    #     raise Exception("Please execute the 'setup.sh' bash script before running this program.")
    os.system("clear")
    print("Welcome to the Codenames Bot!\n")
    role = get_role()
    bot = Bot()
    bot.populate_board()
    # then play!
    bot.play()

if __name__=="__main__":
    main()