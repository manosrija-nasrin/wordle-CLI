from words import words
import random


def setColor(color: str, letter: str):
    colors = {'lightgray': 90, 'yellow': 93, 'green': 92, 'none': 00}
    colored_letter = f"\033[{colors[color]}m{letter}\033[{colors['none']}m"
    # returns colored string
    return colored_letter


def get_valid_word(words):
    word: str = random.choice(words)
    while len(word) > 5 or ' ' in word or '-' in word:
        word = random.choice(words)
    return word.upper()


class WordBoard:
    def __init__(self):
        # keep track of parameters
        self.num_guess = 0  # number of guesses
        self.game_won = None    # game status
        self.word = get_valid_word(words)

        # list of colored letters to print on screen
        self.colored_words = [[None for _ in range(5)] for _ in range(5)]
        # creates an array like ths:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [None, None, ..., None],
        #  [None, None, ..., None],
        #  [None, None, ..., None]]

    def color_letters(self, user_word):
        for i in range(len(user_word)):
            if user_word[i] not in self.word:
                self.colored_words[self.num_guess - 1][i] = setColor(
                    'lightgray', user_word[i])  # letter not in word
            elif user_word[i] == self.word[i]:
                self.colored_words[self.num_guess - 1][i] = setColor(
                    'green', user_word[i])  # letter at correct position
            else:
                # letter not at correct position
                self.colored_words[self.num_guess -
                                   1][i] = setColor('yellow', user_word[i])

    def update_guess(self):
        self.num_guess += 1

    def update_gameStatus(self, user_word):
        if user_word == self.word:
            self.game_won = True
        elif self.num_guess >= 5:
            self.game_won = False

    def check_status(self):
        return self.game_won

    def letter_in_word(self, letter):
        return letter in self.word

    def setResponse(self):
        responses = {6: f"Oh no! The word was {self.word}.", 5: "That was close!", 4: "Good!",
                     3: "Amazing!", 2: "Incredible!", 1: "Marvellous!"}
        return responses[self.num_guess]

    def __str__(self):
        # returns a string that shows the wordle board
        # to the player.

        visible_board = [[self.colored_words[i][j] if self.colored_words[i][j] else '' for j in range(
            5)] for i in range(5)]

        # put this together in a string
        string_rep = ''

        # get max column widths for printing
        widths = []
        for idx in range(5):
            widths.append(1)

        # rows of visible_board
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i + 1} |'
            cells = []
            for idx, col in enumerate(row):
                # string formatting using % - alignment
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            # stringing the column entries together
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / 5)

        header = '-'*6 + 'WORDLE' + '-'*6 + '\n'
        string_rep = header + string_rep + '-'*18
        if self.game_won == True and self.num_guess <= 5:
            response = self.setResponse()
            string_rep += '\n' + ' '*((18 - len(response)) // 2) + response
        elif self.game_won == False:
            self.num_guess += 1
            response = self.setResponse()
            string_rep += '\n' + ' '*((18 - len(response)) // 2) + response
        return string_rep


def get_user_word():
    valid_word = False
    while not valid_word:
        user_guess = input("Your word: ").lower()
        if len(user_guess) != 5:
            print("Word length is not 5!")
            continue
        if user_guess not in words:
            print("Not a valid word. Try again.")
            continue
        valid_word = True
    return user_guess.upper()  # str


def wordle(noRepeatedLetters=False):
    # return True if word is guessed correctly
    # False otherwise
    wB = WordBoard()
    guessed_words = []
    used_letters = set()
    while wB.check_status() is None:
        user_word = get_user_word()
        if user_word in guessed_words:
            print(f"You have already guessed {user_word}.")
            continue
        if noRepeatedLetters:
            letters = set(user_word)
            if letters & used_letters:
                print(', '.join(used_letters),
                      " are not in the word. Guess another word.")
                continue
            else:
                for letter in letters:
                    if not wB.letter_in_word(letter):
                        used_letters.add(letter)
        guessed_words.append(user_word)
        wB.update_guess()
        wB.color_letters(user_word)
        wB.update_gameStatus(user_word)
        print(wB)
    return wB.check_status()


if __name__ == '__main__':
    wordle()
