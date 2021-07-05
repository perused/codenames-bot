import os
try:
    from gensim.models import KeyedVectors
except:
    raise Exception("Please execute the 'setup.sh' bash script before running this program.")

class Game:
    def __init__(self):
        board = [[None]*4 for i in range(4)]

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
    return role

# get the game board as input
def get_board():
    pass

def main():
    # check requirements
    if not os.path.isfile("glove300.word_vectors"):
        raise Exception("Please execute the 'setup.sh' bash script before running this program.")
    os.system('clear')
    print("Welcome to the Codenames Bot!\n")
    role = get_role()
    game = get_board()
    # then play!
    game.play()

if __name__=="__main__":
    main()