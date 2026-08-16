
#? Show Levels
def show_levels():
    print('''Game Levels :
    (1) Easy:
        - Limits: [1:10]
        - No. of trails: 3
    (2) Intermediate:
        - Limits: [1:100]
        - No. of trails: 7
    (3) Hard:
        - Limits: [1:1000]
        - No. of trails: 15''')


#? Game Level choice
def game_level_choice():
    while True:
        print("\nPlease enter the game level:")
        print("(1) Easy")
        print("(2) Intermediate")
        print("(3) Hard")

        try:
            game_level = int(input("Your choice: ").strip())

            if game_level in (1, 2, 3):
                return game_level

            print("Invalid choice. Please choose 1, 2, or 3.")

        except ValueError:
            print("Invalid input. Please enter a number: 1, 2, or 3.")

#? set the game settings
def setGameSettings(game_level):
    if game_level== 1:
        limits = range(1,10)
        n_trails = 3
    elif game_level == 2:
        limits = range(1,100)
        n_trails = 7
    elif game_level == 3:
        limits = range(1,1000)
        n_trails = 15
    return limits, n_trails


#? start Playing
import random

def start_play(limits, n_tries):
    hidden = random.choice(limits)
    user_tries = 0

    while user_tries < n_tries:
        try:
            guess = int(input("Guess the number: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        user_tries += 1

        if guess == hidden:
            print(f"You got it successfully in {user_tries} tries!")
            return True

        if user_tries == n_tries:
            print(
                f"Unfortunately, you used the maximum number "
                f"of tries ({n_tries})."
            )
            print(f"The hidden number was: {hidden}")
            return False

        if guess < hidden:
            print("No, increase!")
        else:
            print("No, decrease!")


#? Play Again
def play_again():
    while True:
        print("Play Again? [0] No, [1] Yes")
        try:
            playAgain = int(input("Your Choice? ").strip())
            if playAgain in (0, 1):
                return playAgain
            print("Enter 0 or 1 Only!!")
        except ValueError:
            print("Please Enter 0 or 1")

#? Main ame
def play():
    show_levels()
    while True:
        game_level = game_level_choice()
        limits, n_trails = setGameSettings(game_level=game_level)
        start_play(limits= limits, n_tries= n_trails)
        if not play_again():
            print("\nThanks for playing!")
            break

#? Program Entry Point
if __name__ == "__main__":
    play()    