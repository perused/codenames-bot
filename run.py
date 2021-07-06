import os
import time
import sys
# try:
#     from gensim.models import KeyedVectors
# except:
#     raise Exception("Please execute the 'setup.sh' bash script before running this program.")

class Bot:
    def __init__(self, role):
        self.role = role
        self.bot_cards = []
        self.not_bot_cards = []
        self.black_cards = None
        self.neutral_cards = []
        self.all_cards = []

    def populate_board(self):
        if self.role == "s":
            self.populate_board_spymaster()
        else:
            self.populate_board_player()

    def populate_board_spymaster(self):
        self.request_cards("from the bot's team", self.bot_cards)
        self.request_cards("NOT from the bot's team", self.not_bot_cards)
        self.request_cards("neutral", self.neutral_cards)
        self.black_card = input("Please enter the black card here: ").lower()
        print("\nThank you, card accepted.")
        time.sleep(1)
        os.system("clear")
        self.all_cards = self.bot_cards + self.not_bot_cards + self.neutral_cards

    def populate_board_player(self):
        self.request_cards("on the board", self.all_cards)

    def print_board(self):
        print(f"Role: {'Spymaster' if self.role == 's' else 'Player'}")
        print("Cards remaining:")
        for i, card in enumerate(self.all_cards):
            print(i, card)
        print()

    def request_cards(self, req, ls):
        while True:
            print(f"Please enter the cards that are {req}, space separated.\n")
            try:
                cards = input("Enter here: ").lower().split()
                for card in cards:
                    ls.append(card)
                break
            except:
                print("\nInvalid, try again.\n")

        print("\nThank you, cards accepted.")
        time.sleep(1)
        os.system("clear")
                
    def remove_cards_spymaster(self, cards):
        for card in cards:
            card = card.strip().lower()
            removed = False
            self.all_cards.remove(card)
            self.bot_cards.remove(card)
            self.not_bot_cards.remove(card)
            if card == self.black_card:
                print("Removing black card ends the game, are you sure?")
                response = input("Enter 'y' or 'n': ").lower()
                if response == "y":
                    print("Game over.")
                    sys.exit()
                else:
                    print("Skipping.")
                    continue


    def remove_cards_player(self, cards):
        pass
    
    def play(self):
        second_option = "give a bot a clue and a number to guess some cards" if self.role == "p" else "request a clue from the bot"
        while True:
            self.print_board()
            print(f"Enter one of the following:\n'r' to remove cards that have been guessed.\n{second_option}\n'q' to quit\n")
            entry = input("Enter here: ")
            if entry == "r":
                print("Please enter all the cards that have been guessed, space separated: ")
                cards = input("Enter here: ").split()
                if self.role == "s":
                    self.remove_cards_spymaster(cards)
                else:
                    self.remove_cards_player(cards)
            elif entry == "c":
                if self.role == "s":
                    self.get_best_spymaster_clue()
                else:
                    try:
                        clue, number = input("Enter the clue and the number, space separated: ").split()
                        number = int(number)
                    except:
                        print("Invalid entry.\n")
                        continue
                    self.get_best_player_guess(clue, number)
            elif entry == "q":
                print("Exiting.")
                sys.exit()        

    def get_best_spymaster_clue(self, team):
        # the best clue should take into account our teams similarity - other team similarity 
        pass

    def get_best_player_guess(self, clue, number):
        pass

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
    bot = Bot(role)
    bot.populate_board()
    # then play!
    bot.play()

if __name__=="__main__":
    main()