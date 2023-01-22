from abc import ABC, abstractmethod
from gensim.models import KeyedVectors
import time
import os
import sys

class Bot(ABC):
    def __init__(self):
        self.model = KeyedVectors.load(os.path.join("components", "glove300.word_vectors"))
        self.related_words = []
        self.all_cards = []

    @abstractmethod
    def populate_board(self):
        pass

    @abstractmethod
    def print_board(self, guessed, clue):
        pass

    @abstractmethod
    def remove_cards(self, cards):
        pass

    @abstractmethod
    def play(self):
        pass

    # @abstractmethod
    # def get_cards_from_file(file_path):
    #     pass


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
