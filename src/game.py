"""
game.py

Runs a complete automated Wordle game using the current solver.

Responsibilities:
- Select a random answer word
- Generate Wordle feedback (G/Y/B) for each guess
- Update the player's knowledge state
- Filter remaining candidate words
- Choose the next guess using the solver
- Encode game states for future ML dataset generation

Returns a summary containing whether the game was won and
how many turns were required.
"""

import random
from words import allWords
from state import createInitialState, updateState
from solver import filterCandidates, findBestGuess
from encoding import encodeState, flattenEncodedState


# Verify that a guess satisfies all Wordle input rules.
def isGuessValid(guess):

    # Guess must be exactly 5 alphabetic characters.
    if len(guess) != 5:
        print("Warning ⚠️ : Word should be exactly 5 letters")
        return False

    if not guess.isalpha():
        print("Warning ⚠️ : Only letters allowed")
        return False

    # Guess must exist in the Wordle dictionary.
    if guess not in allWords:
        print("Warning ⚠️ : Not a valid word")
        return False

    return True



# Generate Wordle feedback (G/Y/B) for a guess.
def evaluateGuess(guess, answer):

    # Tracks unmatched answer letters for duplicate-letter handling.
    remainingLetters = {}

    # Stores G/Y/B feedback for each position.
    feedback = [""] * 5

    # Pass 1: identify green letters and count all remaining letters.
    for i in range(5):
        if guess[i] == answer[i]:
            feedback[i] = "G"
        else:
            letter = answer[i]
            currentCount = remainingLetters.get(letter, 0)
            remainingLetters[letter] = currentCount + 1

    # Pass 2: assign yellow or black feedback.
    for i in range(5):
        if feedback[i] == "G":
            continue

        # Yellow only if an unused copy still exists.
        if remainingLetters.get(guess[i], 0) > 0:
            feedback[i] = "Y"
            remainingLetters[guess[i]] -= 1
        else:
            feedback[i] = "B"

    return feedback


def playGame(datasetStates, datasetLabels):
    # Randomly select the secret answer for this game.
    answer = random.choice(allWords)

    # Tracks everything learned about the answer so far.
    state = createInitialState()

    # Assume failure until the word is successfully guessed.
    gameLost = True

    # Wordle allows a maximum of 6 guesses.
    turn = 1

    # Fixed opening word used by the solver.
    bestGuess = "AISLE"

    # Main game loop.
    while turn <= 6:
        
        # commented this out for cleaner terminal
        # print(f"\nTurn {turn}")

        # Generate ML-ready state representation.
        encodedState = encodeState(state)
        flatVector = flattenEncodedState(encodedState)

        # Store (current_state, expert_move) training example.
        datasetStates.append(flatVector)
        datasetLabels.append(bestGuess)

        # Current guess chosen by the solver.
        guess = bestGuess

        # Ensure the solver produced a valid Wordle guess.
        if not isGuessValid(guess):
            continue

        feedback = evaluateGuess(guess, answer)

        # Update the player's knowledge using the latest feedback.
        updateState(state, guess, feedback)

        # Remove words that no longer satisfy known constraints.
        remainingWords = filterCandidates(state)

        # No valid candidates indicates a state-tracking inconsistency.
        if len(remainingWords) == 0:
            # only return all this at the time for inconsistency
            return {
                "won": "Error",
                "turns": turn,
                "answer": answer,
                "state": state,
                "guess": guess,
                "feedback": feedback
            }
        # Choose the next guess for the upcoming turn.
        if turn < 6:
            # to avoid computation after last turn is done, dont decide best guess for 7th turn
            bestGuess = findBestGuess(remainingWords)

        # Player successfully found the answer.
        if guess == answer:
            # commented it out fo rnow
            # print(f"🎉 You win! It took you {turn} turns")
            gameLost = False

            return {
                "won": True,
                "turns": turn
            }

        # Consume one valid attempt.
        turn += 1

    # Reveal answer if all attempts are exhausted.
    if gameLost:
        # commented it out fo rnow
        # print(f"The answer was: {answer}")

        return {
            "won": False,
            "turns": 6
        }
