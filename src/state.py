"""
state.py

Maintains the solver's knowledge about the hidden Wordle answer.

The game state tracks:
- Green letters (confirmed positions)
- Yellow letters (known letters with forbidden positions)
- Black letters (currently believed absent)
- Guess history
- Remaining attempts

This state is updated after every guess and is used by both
candidate filtering and ML state encoding.
"""

# Create a fresh state before a new game begins.
def createInitialState():
    state = {
        # Confirmed letter for each position.
        "greens": ["", "", "", "", ""],

        # Known letters mapped to positions where they cannot appear.
        "yellows": {},

        # Letters currently believed absent from the answer.
        "blacks": [],

        # Chronological list of previous guesses.
        "guessHistory": [],

        # Remaining guesses available to the solver.
        "attemptsLeft": 6
    }

    return state

# Incorporate feedback from a completed guess.
def updateState(state, guess, feedback):
    # Record the guess for future analysis and debugging.
    state["guessHistory"].append(guess)

    # A valid guess consumes one attempt.
    state["attemptsLeft"] -= 1

    # Update state using G/Y/B feedback for each position.
    for i in range(5):
        letter = guess[i]

        # Green: exact letter and position are now known.
        if feedback[i] == "G":
            state["greens"][i] = letter

        # Yellow: letter exists but not at this position.
        elif feedback[i] == "Y":
            if letter not in state["yellows"]:
                state["yellows"][letter] = []

            state["yellows"][letter].append(i)

        # Black: mark absent only if the letter is not already known to exist.
        elif feedback[i] == "B":
            # Prevent conflicts caused by duplicate-letter feedback.
            if (
                letter not in state["blacks"]
                and letter not in state["yellows"]
                and letter not in state["greens"]
            ):
                state["blacks"].append(letter)
