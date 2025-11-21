import random

def select_difficulty():
    print("Please select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")

    while True:
        choice = input("Enter your choice: ")

        if choice == "1":
            return 10
        elif choice == "2":
            return 5
        elif choice == "3":
            return 3
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    # Difficulty selection
    chances = select_difficulty()
    print(f"Great! You have selected the difficulty level with {chances} chances.")
    print("Let's start the game!\n")

    # Generate random number
    secret_number = random.randint(1, 100)
    attempts = 0

    # Game loop
    while chances > 0:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        attempts += 1
        chances -= 1

        if guess == secret_number:
            print(f"Congratulations! You guessed the correct number in {attempts} attempts.")
            return
        
        elif guess < secret_number:
            print(f"Incorrect! The number is greater than {guess}.")
        else:
            print(f"Incorrect! The number is less than {guess}.")

        if chances > 0:
            print(f"You have {chances} chances left.\n")

    print("\nGame Over! You ran out of chances.")
    print(f"The correct number was: {secret_number}")


# Run the game
if __name__ == "__main__":
    number_guessing_game()
