from components.bot import *


class Spymaster(Bot):
    def __init__(self):
        super(Spymaster, self).__init__()
        self.bot_cards = []
        self.not_bot_cards = []
        self.black_card = None
        self.neutral_cards = []

    def process_related(self):
        for word in self.bot_cards:
            similar = self.model.similar_by_word(word)
            for i in range(len(similar)):
                similar_word, _ = similar[i]
                if similar_word in word or word in similar_word:
                    continue
                self.related_words.append(similar_word)
        related = self.related_words.copy()
        for word in related:
            similar = self.model.similar_by_word(word)
            for i in range(len(similar)):
                similar_word, _ = similar[i]
                if similar_word in word or word in similar_word:
                    continue
                self.related_words.append(similar_word)

    def populate_board(self):
        self.request_cards("from the bot's team", self.bot_cards)
        self.request_cards("NOT from the bot's team", self.not_bot_cards)
        self.request_cards("neutral", self.neutral_cards)
        self.black_card = input("Please enter the black card here: ").lower()
        print("\nThank you, card accepted.\n\n Processing cards...\n")
        self.process_related()
        os.system("clear")
        self.all_cards = self.bot_cards + self.not_bot_cards + self.neutral_cards + [self.black_card]

    def print_board(self, clue):
        os.system("clear")
        print(f"Role: Spymaster")
        print("Cards remaining:")
        for i, card in enumerate(self.all_cards):
            print(i, card)
        print()
        if clue:
            print(f"Bot just gave this clue: '{clue}'\n")

    def remove_cards(self, cards):
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

    def play(self):
        clue = None
        while True:
            self.print_board(clue)
            print(f"Enter one of the following:\n'r' to remove cards that have been guessed.\n'c' to request a clue "
                  f"from the bot\n'q' to quit\n")
            entry = input("Enter here: ")
            print()
            if entry == "r":
                print("Please enter all the cards to be removed.\n")
                cards = input("Enter here: ").split()
                print()
                self.remove_cards(cards)
                if len(self.all_cards) == 0:
                    print("No more cards remaining, game over.")
                    sys.exit()
                clue = None
            elif entry == "c":
                clue = self.get_clue()
            elif entry == "q":
                print("Exiting.")
                sys.exit()

    def get_clue(self):
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

        # multipliers = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]
        # num_clue = [1, 2, 3, 4, 5]

        # for multiplier in multipliers:
        for i in range(len(all_words)):
            word = all_words[i]
            if word in self.bot_cards:
                continue
            #
            similarity_bots = sum([wv.similarity(word, x) for x in self.bot_cards])
            similarity_black = sum(wv.similarity(word, self.black_card) for i in range(len(self.bot_cards)))
            score = similarity_bots - similarity_black

            # similarity_bots = sum([wv.similarity(word, x) for x in self.bot_cards])
            # similarity_not_bots = sum([wv.similarity(word, x) for x in self.not_bot_cards])
            # similarity_black = wv.similarity(word, self.black_card) * multiplier
            # score = similarity_bots - (similarity_not_bots / 2) - similarity_black
            if score > best_clue[1]:
                best_clue[0] = word
                best_clue[1] = score
        time.sleep(10)
        return best_clue[0]

