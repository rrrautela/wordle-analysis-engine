
#########################
# STATE BASED FUNCTIONS
#########################
# Create a fresh game state
def createInitialState():
    state = {
        # Locked letters by position
        "greens": ["", "", "", "", ""],

        # Letters known to exist in the word
        "yellows": {},

        # Eliminated letters
        "blacks": [],

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
            if (
                letter not in state["blacks"]
                and letter not in state["yellows"]
                and letter not in state["greens"]
            ):
                state["blacks"].append(letter)

