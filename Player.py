class Player(Bot):
    def __init__(self):
        super(Player, self).__init__()

    def populate_board(self):
        self.request_cards("on the board", self.all_cards)

    @override
    def print_board(self, guessed):
        os.system("clear")
        print(f"Role: Player")
        print("Cards remaining:")
        for i, card in enumerate(self.all_cards):
            print(i, card)
        print()
        print(f"Bot just guessed these: {', '.join(guessed)}\n")

    @override
    def remove_cards(self, cards):
        removed = set()
        for card in cards:
            card = card.strip().lower()
            self.remove_append(card, self.all_cards, removed)
        print(f"Successfully removed {'no cards :/' if len(removed) == 0 else ', '.join(removed)}")
        time.sleep(2)

    @override
    def play(self):
        guessed = None
        while True:
            self.print_board(guessed)
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
                guessed = None
            elif entry == "c":
                try:
                    clue, number = input("Enter the clue and the number, space separated: ").split()
                    number = int(number)
                except:
                    print("Invalid entry.\n")
                    continue
                guessed = self.get_guess(clue, number)
            elif entry == "q":
                print("Exiting.")
                sys.exit()

    def get_guess(self, clue, number):
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
            print(f"{count + 1}. {word}\n")
            guessed.append(word)
            count += 1
            if count == number:
                break
        time.sleep(7)
        return guessed

