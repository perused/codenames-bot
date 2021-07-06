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
        self.black_card = input("Please enter the black card here: ")
        print("\nThank you, card accepted.")
        time.sleep(1)
        os.system("clear")
        self.all_cards = self.bot_cards + self.not_bot_cards + self.neutral_cards

    def request_cards(self, req, ls):
        while True:
            print(f"Please enter the cards that are {req}, space separated.\n")
            try:
                cards = input("Enter here: ").split()
                for card in cards:
                    ls.append(card)
                break
            except:
                print("\nInvalid, try again.\n")

        print("\nThank you, cards accepted.")
        time.sleep(1)
        os.system("clear")

    def populate_board_player(self):
        while True:
            print("Please enter the names of all cards, space separated.\n")
            try:
                bot_cards = input("Enter here: ").split()
                for card in bot_cards:
                    self.bot_cards.append(card)
                    self.all_cards.append(card)
                break
            except:
                print("\nInvalid, try again.\n")

        print("\nThank you, cards accepted.")
        time.sleep(1)
        os.system("clear")
                
    def play(self):
        if self.role == "s":
            self.play_spymaster()
        else:
            self.play_player()

    def play_spymaster(self):
        # could work out from number of red and blue cards whether bot is starting or not
        pass
    
    def play_player(self):
        pass
            
    def get_best_spymaster_clue(self, team):
        # the best clue should take into account our teams similarity - other team similarity 
        pass

    def get_best_player_guess(self, clue):
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