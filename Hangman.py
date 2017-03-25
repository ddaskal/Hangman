from random_words import RandomWords


class Answer(object):
    """The Answer Word For Hangman.

        Attributes:
            name: A randomized and capitalized string for the answer word.
            length: The length of the answer word.
            letters: A list of dicts with key as the letter and value as whether it has been guessed.
        """

    def __init__(self):
        self.name = self.new_game().upper()
        self.length = len(self.name)
        self.letters = self.format_letters()

    @staticmethod
    def new_game():
        """Creates a new answer for a new game."""
        rw = RandomWords()
        word = rw.random_word()
        return word

    def format_letters(self):
        """Turns answer string into a list of dicts with key as the letter and value as whether it has been guessed."""
        letter_list = [{str(letter).upper(): False} for letter in list(self.name)]
        return letter_list

    def print_answer(self):
        """Prints the answer out for the user to see current progress."""
        printed_answer = ""
        for letter in self.letters:
            if bool(letter.values()[0]):
                printed_answer += " " + str(letter.keys()) + " "
            else:
                printed_answer += " _ "
        return printed_answer

    def update_guess(self, user_input):
        """Returns true if correct guess and updates the existing guess with new letters."""
        old_guess = self.letters
        self.letters = map(lambda x: {user_input: True} if user_input in x else x, self.letters)
        return old_guess != self.letters


def hangman():
    # Grab a random word from imported dictionary
    answer = Answer()

    errors = 0
    existing_guess = set()

    # Tell users how many letters in word
    print("The answer has " + str(answer.length) + " letters.")

    while errors < 6:
        if " _ " not in answer.print_answer():
            print("CONGRATULATIONS! You win!")
            break

        print("You have this many attempts left: " + str(6-errors))
        print("Here are all of the letters that you have guessed, both correct and incorrect: "
              + str(sorted(existing_guess)))
        print("Here is what you've guessed correctly so far: " + answer.print_answer())
        # Ask user for input letter or attempt guess at word
        user_input = raw_input("Input a single letter guess A-Z or multiple letters to guess the answer: ")

        # Check if real letter, check if user has requested letter before, check if letter is in word
        if user_input.isalpha():
            user_input = user_input.upper()
            if len(user_input) == 1:
                if user_input in existing_guess:
                    print("You have already guessed the letter " + user_input + ", please guess again.")
                    continue
                else:
                    existing_guess.add(user_input)
                    if answer.update_guess(user_input):
                        print("Nice! The answer contained your letter: " + user_input)
                    else:
                        print("Oops! The answer does not contain your letter: " + user_input)
                        errors += 1
            # They guessed a word
            # TODO: IF THEY ALREADY HAVE LETTERS, MAKE SURE THE WORD MATCHES EXISTING GUESSES
            else:
                if len(user_input) != answer.length:
                    print("Oops! Your input word length of " + str(len(user_input)) +
                          " does not match the answer word length of " + str(answer.length) + ". Try again.")
                elif user_input == answer.name:
                    print("CONGRATULATIONS! You win!")
                    break
                else:
                    print("Sorry, your input word was incorrect: " + user_input)
                    errors += 1
        else:
            print("Non-Letter detected. Try again.")
            continue

    # Play again?
    if errors == 6:
        print("Here is what you've guessed correctly so far: " + answer.print_answer())
        print("The answer was: " + answer.name)
    play_again = raw_input("Would you like to play again? Type 'yes' or 'no'.")
    if play_again == 'yes':
        hangman()
    elif play_again == 'no':
        print("Exiting")
        exit()
    else:
        print("Exiting due to invalid input.")
        exit()

hangman()
