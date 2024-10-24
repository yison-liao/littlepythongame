import random


class Bagels:
    def __init__(self, MAX_GUESS: int, NUM_DIGIT: int) -> None:
        self.MAX_GUESS = MAX_GUESS
        self.NUM_DIGIT = NUM_DIGIT
        self.DIGIT_RANGE = "0123456789"

    def gameStart(self):
        print(f"""
            Start playing Bagels, guess a {self.NUM_DIGIT}-digit number,
            and I will respond you :
            1. 'Pico' : One digit is correct but wrong place.
            2. 'Fermi' : One digit is correct and right place.
            3. 'Bagels' : No digit is correct.

            You have {self.MAX_GUESS} times to guess.
          """)

        while True:
            answer = self.getSecretNum()

            num_guess = 1
            while num_guess <= self.MAX_GUESS:
                guess = input(f"{num_guess} time guess: ")
                if self.formatCheck(guess) is False:
                    print(f"Not a {self.NUM_DIGIT}-digit number, input again")
                    continue

                if guess == answer:
                    print("Correct Answer!!!")
                    break

                print(self.getClues(guess, answer))
                num_guess += 1
            else:
                print(f"Guess out of {self.MAX_GUESS}")

            print("Do you want to play again? (yes/no)")
            if input("> ").lower().startswith("y"):
                continue
            break

    def getSecretNum(self) -> str:
        f"""
        Give a random {self.NUM_DIGIT}-digit number in string.
        """
        numbers = list(self.DIGIT_RANGE)
        random.shuffle(numbers)
        return "".join(numbers[: self.NUM_DIGIT])

    def getClues(self, guess: str, answer: str) -> str:
        clue = {
            "Pico": 0,
            "Fermi": 0,
            "Bagels": True,
        }
        for i in range(len(answer)):
            if guess[i] == answer[i]:
                clue["Fermi"] += 1
                clue["Bagels"] = False
            elif guess[i] in answer:
                clue["Pico"] += 1
                clue["Bagels"] = False

        if clue["Bagels"]:
            return "You got Bagels"
        return f"You have {clue['Fermi']} Fermi, and {clue['Pico']} Pico."

    def formatCheck(self, guess: str):
        if len(guess) != self.NUM_DIGIT:
            return False
        for digit in guess:
            if digit not in self.DIGIT_RANGE:
                return False
        return True


if __name__ == "__main__":
    game = Bagels(5, 3)
    game.gameStart()
