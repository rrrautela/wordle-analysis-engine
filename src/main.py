import random
from words import allWords

# Create a fresh game state

def createInitialState():
    state = {
        # Locked letters by position
        "greens": ["", "", "", "", ""],

        # Letters known to exist in the word
        "yellows": {},

        # Eliminated letters
        "greys": [],

        # Previous guesses
        "guessHistory": [],

        # Guesses remaining
        "attemptsLeft": 6
    }

    return state

# Update state after a valid guess

def updateState(state, guess, feedback):
    # Store guess history
    state["guessHistory"].append(guess)

    # One less attempt remaining
    state["attemptsLeft"] -= 1

    # Process each letter's feedback
    for i in range(5):
        letter = guess[i]

        # Correct letter and position
        if feedback[i] == "G":
            state["greens"][i] = letter

        # Letter exists somewhere in answer
        elif feedback[i] == "Y":
            if letter not in state["yellows"]:
                state["yellows"][letter] = []

            state["yellows"][letter].append(i)

        # Letter not present in answer
        elif feedback[i] == "B":
            if letter not in state["greys"]:
                state["greys"].append(letter)



# Convert state into ML-friendly structured format
def encodeState(state):

    # 5 x 26
    greenMatrix = []

    for greenLetter in state["greens"]:
        positionVector = [0] * 26

        if greenLetter != "":
            letterIndex = ord(greenLetter) - ord("A")
            positionVector[letterIndex] = 1

        greenMatrix.append(positionVector)

    # 26 x 5
    yellowMatrix = []

    for asciiCode in range(ord("A"), ord("Z") + 1):
        currentLetter = chr(asciiCode)

        forbiddenPositions = [0] * 5

        if currentLetter in state["yellows"]:
            for position in state["yellows"][currentLetter]:
                forbiddenPositions[position] = 1

        yellowMatrix.append(forbiddenPositions)

    # 26
    greyVector = [0] * 26

    for greyLetter in state["greys"]:
        letterIndex = ord(greyLetter) - ord("A")
        greyVector[letterIndex] = 1

    return {
        "greens": greenMatrix,
        "yellows": yellowMatrix,
        "greys": greyVector,
        "attemptsLeft": state["attemptsLeft"]
    }


def flattenEncodedState(encodedState):
    flatVector = []

    # Flatten green matrix
    for row in encodedState["greens"]:
        flatVector.extend(row)

    # Flatten yellow matrix
    for row in encodedState["yellows"]:
        flatVector.extend(row)

    # Add grey vector
    flatVector.extend(encodedState["greys"])

    # Add attempts left
    flatVector.append(encodedState["attemptsLeft"])

    return flatVector

def playGame():
    print("wordle engine started")

    # Pick a random secret answer for this game
    answer = random.choice(allWords)

    # Track everything the player knows
    state = createInitialState()

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

        # Validate word, it should be a word from the dataset
        if guess not in allWords:
            print("Warning ⚠️ : Not a valid word")
            continue

        else:
            print("✓ Valid guess")
            print(f"You guessed: {guess}")


        # Now process the user's input by comparing it with the actual answer

        # Count letters that are not already matched as green
        remainingLetters = {}

        # First pass: mark greens
        for i in range(5):
            if guess[i] == answer[i]:
                feedback[i] = "G"
            else:
                letter = answer[i]
                currentCount = remainingLetters.get(letter, 0)
                remainingLetters[letter] = currentCount + 1

        # Second pass: mark yellows and blacks
        for i in range(5):
            if feedback[i] == "G":
                continue

            # Yellow only if an unused copy still exists
            if remainingLetters.get(guess[i], 0) > 0:
                feedback[i] = "Y"
                remainingLetters[guess[i]] -= 1
            else:
                feedback[i] = "B"
        print("".join(feedback))


        # Update player knowledge
        updateState(state, guess, feedback)

        # Debug: show current state
        print(state)

        encodedState = encodeState(state)

        flatVector = flattenEncodedState(encodedState)

        print(f"Encoded vector length: {len(flatVector)}")

        # print(flatVector)

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

playGame()
