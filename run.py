import os
import time
import sys
# try:
#     from gensim.models import KeyedVectors
# except:
#     raise Exception("Please execute the 'setup.sh' bash script before running this program.")

class Bot:
    def __init__(self, role, team):
        self.role = role
        self.team = team
        self.board = [[(None, None)]*4 for i in range(4)]
        self.blue_cards = []
        self.red_cards = []
        self.all_cards = []
        self.card_coords = {} # card: i, j

    def populate_board(self):
        if self.role == "s":
            self.populate_board_spymaster()
        else:
            self.populate_board_player()

    def populate_board_spymaster(self):
        print("\nPopulating game board works as follows: Enter the name and type of the card starting from the top left and going across to the right before going down a row.\n\nCard types: red ('r'), blue ('b'), neutral ('n'), black ('black')\n\ne.g 'mountain red'\n")
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
                    confirm = input(f"\nConfirming card = '{card}' and colour = '{colour}'? (Press 'y' for yes, any other key for no): ").lower()
                    if "y" in confirm:
                        print("\nConfirmed.")
                        self.board[i][j] = (card, colour)
                        if colour == "r" or colour == "red":
                            self.red_cards.append(card)
                        elif colour == "b" or colour == "blue":
                            self.blue_cards.append(card)
                        self.all_cards.append(card)
                        self.card_coords[card] = (i, j)
                        time.sleep(1)
                        break
                    else:
                        print("\nCancelled.\n")
                        continue
                self.print_board()
        print("Finished entering board, game begins now!")

    def populate_board_player(self):
        print("\nPopulating game board works as follows: Enter the name of the card starting from the top left and going across to the right before going down a row.\n\ne.g 'mountain'\n")
        for i in range(4):
            for j in range(4):
                while True:
                    card = input("Enter name of card ('q' to quit): ").lower()
                    if card == "q":
                        sys.exit()
                    confirm = input(f"\nConfirming card = '{card}'? (Press 'y' for yes, any other key for no): ").lower()
                    if "y" in confirm:
                        print("\nConfirmed.")
                        self.board[i][j] = (card, None)
                        self.all_cards.append(card)
                        self.card_coords[card] = (i, j)
                        time.sleep(1)
                        break
                    else:
                        print("\nCancelled.\n")
                        continue
                self.print_board()
        print("Finished entering board, game begins now!")
        time.sleep(1)
        os.system("clear")
                
    def play(self):
        if self.role == "s":
            self.play_spymaster()
        else:
            self.play_player()

    def play_spymaster(self):
        # could work out from number of red and blue cards whether bot is starting or not
        start = input("Is bot starting? 'y' for yes and anything else for no: ").lower()
        if "y" in start:
            start = True
            print("")
        else:
            start = False
        bot_turn = start
        while True:
            if bot_turn:
                print("Bot's turn\n")
                print("Thinking of clue...\n")
                time.sleep(3)
                print("Clue is... SPAGHETTI!\n")
                bot_turn = False
            else:
                print("Other team's turn\n")
                print("Enter which cards have been guessed, one by one, so the bot knows which ones are no longer in the game. Type 'q' when finished.\n")
                while True:
                    card = input("Enter card here: ").lower()
                    if card == 'q':
                        break
                    if card not in self.all_cards:
                        print("That is not a known card, please try again.")
                        continue
                    else:
                        print(f"Turning '{card}' over.")
                        i, j = self.card_coords[card]
                        self.board[i][j] = ("X", self.board[i][j][1])
                bot_turn = True
                self.print_board()
    
    def play_player(self):
        pass
            
    def get_best_spymaster_clue(self, team):
        # the best clue should take into account our teams similarity - other team similarity 
        pass

    def get_best_player_guess(self, clue):
        pass

    def print_board(self):
        os.system("clear")
        print("Current board:")
        for i in range(4):
            for j in range(4):
                print(f"{self.board[i][j][0]}\t", end="")
            print()
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

def get_team():
    team = None
    while not team:
        team = input("Are we playing as red (r) or blue (b)? ").lower()
        if "r" in team:
            team = "r"
        elif "b" in team:
            team = "b"
        else:
            print("Invalid input. Please enter 'r' for red team or 'b' for blue team.")
    print()
    os.system("clear")
    print(f'{"Red" if team == "r" else "Blue"} selected!')
    time.sleep(1)
    return team

def main():
    """Get the role of the bot and begin game"""
    if not os.path.isfile("glove300.word_vectors"):
        print("When running codenames bot for the first time, a one-off download is required.")
        model = gensim.downloader.load('glove-wiki-gigaword-300')
        model.save("glove300.word_vectors")
    os.system("clear")
    print("Welcome to the Codenames Bot!\n")
    role = get_role()
    team = get_team()
    bot = Bot(role, team)
    bot.populate_board()
    # then play!
    bot.play()

if __name__=="__main__":
    main()