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

    def process_added(self):
        print("\nThank you, card accepted.\n\n Processing cards...\n")
        self.process_related()
        os.system("clear")
        self.all_cards = self.bot_cards + self.not_bot_cards + self.neutral_cards + [self.black_card]

    def populate_board(self):
        self.request_cards("from the bot's team", self.bot_cards)
        self.request_cards("NOT from the bot's team", self.not_bot_cards)
        self.request_cards("neutral", self.neutral_cards)
        self.black_card = input("Please enter the black card here: ").lower()
        self.process_added()

    def get_cards_from_file(self, file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
            lists = [self.bot_cards, self.not_bot_cards, self.neutral_cards]
            for line, list in zip(lines, lists):
                list += line.rstrip().split(" ")
            self.black_card = lines[-1].rstrip()
        self.process_added()

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

    def check_pair(self, word, card, similarity_not_bots, similarity_black):
        score = self.model.similarity(word, card) - similarity_not_bots - similarity_black
        return score

    def check_word(self, word, similarity_not_bots, similarity_black):
        scores = { x: self.check_pair(word, x, similarity_not_bots, similarity_black) for x in self.bot_cards}
        score_sum = sum(scores.values())
        score_average = score_sum/len(scores)
        good_cards = [ x for x in scores.values() if x >= score_average]
        return score_sum, len(good_cards)

    def get_clue(self):
        print("Bot is thinking of a clue...")
        wv = self.model

        all_words = self.related_words
        best_clue = [None, float("-inf"), 1]

        for i, word in enumerate(all_words):
            if word in self.bot_cards:
                continue

            similarity_not_bots = sum([wv.similarity(word, x) for x in self.not_bot_cards]) * 1/2
            similarity_black = wv.similarity(word, self.black_card) * 2
            score_sum, target_cards_amount = self.check_word(word, similarity_not_bots, similarity_black)

            if score_sum*target_cards_amount > best_clue[1]*best_clue[2]:
                best_clue[0] = word
                best_clue[1] = score_sum
                best_clue[2] = target_cards_amount

        time.sleep(10)
        if best_clue[0] != None:
            return f"{best_clue[0]}, {best_clue[2]}"
        else:
            return None
