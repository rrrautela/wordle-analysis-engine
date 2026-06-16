import random

from words import allWords

from state import createInitialState, updateState

from solver import filterCandidates, findBestGuess

from encoding import encodeState, flattenEncodedState


def playGame():
    # print("wordle game started")

    # Pick a random secret answer for this game
    answer = random.choice(allWords)

    # Track everything the player knows
    state = createInitialState()

    # Track whether player failed to guess the word
    gameLost = True

    # Player gets up to 6 valid guesses
    turn = 1

    bestGuess = "AISLE"
    # Main game loop
    while turn <= 6:
        # Stores G/Y/B feedback for each position
        feedback = [""] * 5
        # Read guess and normalize to uppercase
        print(f"\nTurn {turn}")
        
        # guess = input("enter a guess: ").upper()
        guess = bestGuess

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

        # else:
            # print("✓ Valid guess")
            # print(f"You guessed: {guess}")


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
        # print("".join(feedback))


        # Update player knowledge
        updateState(state, guess, feedback)

        remainingWords = filterCandidates(state)
        # print(f"Candidates left: {len(remainingWords)}")

        if len(remainingWords) == 0:
            return {
                "won": "Error",
                "turns": turn
            }

        bestGuess = findBestGuess(remainingWords)

        # print(f"Best next guess: {bestGuess}")
                
        # for word in remainingWords:
        #     print(word, scoreWord(word, frequency))


        # print(remainingWords[:20])

        # Debug: show current state
        # print(state)

        encodedState = encodeState(state)

        flatVector = flattenEncodedState(encodedState)
        # print(f"Encoded vector length: {len(flatVector)}")

        # print(flatVector)

        # Player guessed the secret word
        if guess == answer:
            print(f"🎉 You win! It took you {turn} turns")
            gameLost = False

            return {
                "won": True,
                "turns": turn
            }

        # Consume one valid attempt
        turn += 1

    # Reveal answer if player used all attempts
    if gameLost:
        print(f"The answer was: {answer}")

        return {
            "won": False,
            "turns": 6
        }



