import os
import time
import sys
import gensim.downloader as api
from gensim.models import KeyedVectors
from tqdm import tqdm


class Bot:
    def __init__(self, role):
        self.role = role
        self.bot_cards = []
        self.not_bot_cards = []
        self.black_card = None
        self.neutral_cards = []
        self.all_cards = []
        self.model = KeyedVectors.load("glove300.word_vectors")
        self.related_words = []

    def populate_board(self):
        if self.role == "s":
            self.populate_board_spymaster()
        else:
            self.populate_board_player()

    def process_related(self):
        for word in self.bot_cards:
            similar = self.model.similar_by_word(word)
            for i in range(len(similar)):
                similar_word, _ = similar[i]
                self.related_words.append(similar_word)
        related = self.related_words.copy()
        for word in related:
            similar = self.model.similar_by_word(word)
            for i in range(len(similar)):
                similar_word, _ = similar[i]
                self.related_words.append(similar_word)

    def populate_board_spymaster(self):
        self.request_cards("from the bot's team", self.bot_cards)
        self.request_cards("NOT from the bot's team", self.not_bot_cards)
        self.request_cards("neutral", self.neutral_cards)
        self.black_card = input("Please enter the black card here: ").lower()
        print("\nThank you, card accepted.\n\n Processing cards...\n")
        self.process_related()
        os.system("clear")
        self.all_cards = self.bot_cards + self.not_bot_cards + self.neutral_cards + [self.black_card]

    def populate_board_player(self):
        self.request_cards("on the board", self.all_cards)

    def print_board(self, guessed, clue):
        os.system("clear")
        print(f"Role: {'Spymaster' if self.role == 's' else 'Player'}")
        print("Cards remaining:")
        for i, card in enumerate(self.all_cards):
            print(i, card)
        print()
        if guessed:
            print(f"Bot just guessed these: {', '.join(guessed)}\n")
        elif clue:
            print(f"Bot just gave this clue: '{clue}'\n")

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

    def remove_append(self, card, ls, removed):
        try:
            ls.remove(card)
            removed.add(card)
        except:
            pass
        return
                
    def remove_cards_spymaster(self, cards):
        removed = set()
        for card in cards:
            card = card.strip().lower()
            self.remove_append(card, self.all_cards, removed)
            self.remove_append(card, self.bot_cards, removed)
            self.remove_append(card, self.not_bot_cards, removed)
            if card == self.black_card:
                print("Removing black card ends the game, are you sure?\n")
                response = input("Enter 'y' or 'n': ").lower()
                if response == "y":
                    print("\nGame over.")
                    sys.exit()
                else:
                    print("Skipping.")
                    continue
        print(f"Successfully removed {'no cards :/' if len(removed) == 0 else ', '.join(removed)}")
        time.sleep(2)

    def remove_cards_player(self, cards):
        removed = set()
        for card in cards:
            card = card.strip().lower()
            self.remove_append(card, self.all_cards, removed)
        print(f"Successfully removed {'no cards :/' if len(removed) == 0 else ', '.join(removed)}")
        time.sleep(2)
    
    def play(self):
        guessed, clue = None, None
        second_option = "give a bot a clue and a number to guess some cards" if self.role == "p" else "request a clue from the bot"
        while True:
            self.print_board(guessed, clue)
            print(f"Enter one of the following:\n'r' to remove cards that have been guessed.\n'c' to {second_option}\n'q' to quit\n")
            entry = input("Enter here: ")
            print()
            if entry == "r":
                print("Please enter all the cards to be removed.\n")
                cards = input("Enter here: ").split()
                print()
                if self.role == "s":
                    self.remove_cards_spymaster(cards)
                else:
                    self.remove_cards_player(cards)
                if len(self.all_cards) == 0:
                    print("No more cards remaining, game over.")
                    sys.exit()
                guessed, clue = None, None
            elif entry == "c":
                if self.role == "s":
                    clue = self.get_best_spymaster_clue()
                else:
                    try:
                        clue, number = input("Enter the clue and the number, space separated: ").split()
                        number = int(number)
                    except:
                        print("Invalid entry.\n")
                        continue
                    guessed = self.get_best_player_guess(clue, number)
            elif entry == "q":
                print("Exiting.")
                sys.exit()        

    def get_best_spymaster_clue(self):
        # the best clue should take into account our teams similarity - other team similarity
        print("Bot is thinking of a clue...")
        self.bot_cards = ["horse", "shoe", "gallop", "ride"]
        self.process_related()
        self.not_bot_cards = ["dog", "man", "woman", "cat"]
        self.neutral_cards = ["toaster", "oven", "kettle"]
        self.black_card = "hat"
        wv = self.model
        # all_words = self.model.index_to_key
        all_words = self.related_words
        best_clue = ["", float("-inf")]

        multipliers = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]

        for multiplier in multipliers:
            for i in range(len(all_words)):
                word = all_words[i]
                if word in self.bot_cards:
                    continue
                similarity_bots = sum([wv.similarity(word, x) for x in self.bot_cards])
                similarity_not_bots = sum([wv.similarity(word, x) for x in self.not_bot_cards])
                similarity_black = wv.similarity(word, self.black_card) * multiplier
                score = similarity_bots - (similarity_not_bots/2) - similarity_black
                if score > best_clue[1]:
                    best_clue[0] = word
                    best_clue[1] = score
            print(f"For the multiplier {multiplier}, the clue is '{best_clue[0]}'")
        time.sleep(10)
        return best_clue[0]


    def get_best_player_guess(self, clue, number):
        print("Beep beep... what to guess... beep boop...\n")
        similarities = {}
        wv = self.model
        for word in self.all_cards:
            similarities[word] = wv.similarity(clue, word)
        sorted_tuples = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        sorted_words = {k: v for k, v in sorted_tuples}
        count = 0
        guessed = []
        for word in sorted_words:
            time.sleep(1)
            print(f"{count+1}. {word}\n")
            guessed.append(word)
            count += 1
            if count == number:
                break
        time.sleep(7)
        return guessed


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
    print(f'{"Spymaster" if role == "s" else "Player"} selected!\n')
    time.sleep(1)
    return role


def main():
    bot = Bot("s")
    bot.get_best_spymaster_clue()
    # check requirements
    # if not os.path.isfile("glove300.word_vectors"):
    #     raise Exception("Please execute the 'setup.sh' bash script before running this program.")
    # os.system("clear")
    # print("Welcome to the Codenames Bot!\n")
    # role = get_role()
    # bot = Bot(role)
    # bot.populate_board()
    # # then play!
    # bot.play()


if __name__ == "__main__":
    main()
