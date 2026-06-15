import random
from words import allWords

print("wordle engine started")

# Pick a random secret answer for this game
answer = random.choice(allWords)

# Track whether player failed to guess the word
gameLost = True

# Player gets up to 6 valid guesses
turn = 1
# Main game loop
while turn <= 6:
    # Stores G/Y/B feedback for each position
    feedback = [""] * 5
    # Read guess and normalize to uppercase
    print(f"\nTurn {turn}")
    guess = input("enter a guess: ").upper()

    # Track whether any validation rule failed
    hasError = False

    # Validate user input before processing
    if len(guess) != 5:
        print("Warning ⚠️ : Word should be exactly 5 letters")
        hasError = True
        
    if not guess.isalpha():
        print("Warning ⚠️ : Only letters allowed")
        hasError = True

    if hasError:
        continue
        
    if guess not in allWords:
        print("Warning ⚠️ : Not a valid word")
        continue
    else:
        print("✓ Valid guess")
        print(f"You guessed: {guess}")

    # Generate Wordle feedback for each letter
    for i in range(5):
        # Green: correct letter in correct position
        if guess[i] == answer[i]:
            result = "G"

        # Yellow: letter exists elsewhere in answer
        elif guess[i] in answer:
            result = "Y"

        # Black/Grey: letter not present in answer
        else:
            result = "B"

        feedback[i] = result
    print("".join(feedback))

    # Player guessed the secret word
    if guess == answer:
        print(f"🎉 You win! It took you {turn} turns")
        gameLost = False
        break

    # Consume one valid attempt
    turn += 1

# Reveal answer if player used all attempts
if gameLost:
    print(f"The answer was: {answer}")
