"""
encoding.py

Converts a Wordle game state into a fixed-size numerical representation
that can be used by machine learning models.

The encoded state captures:
- Green letters (known correct positions)
- Yellow letters (known letters with forbidden positions)
- Black letters (known absent letters)
- Remaining attempts

The final representation can also be flattened into a single 1D feature
vector for dataset generation and model training.
"""


# Convert a Wordle state into structured ML features
def encodeState(state):

    # Green information:
    # 5 positions × 26 letters
    # Each row is a one-hot vector representing the confirmed letter
    # for that position (or all zeros if unknown).
    greenMatrix = []

    for greenLetter in state["greens"]:
        positionVector = [0] * 26

        if greenLetter != "":
            letterIndex = ord(greenLetter) - ord("A")
            positionVector[letterIndex] = 1

        greenMatrix.append(positionVector)

    # Yellow information:
    # 26 letters × 5 positions
    # Marks positions where a known-present letter cannot appear.
    yellowMatrix = []

    for asciiCode in range(ord("A"), ord("Z") + 1):
        currentLetter = chr(asciiCode)

        forbiddenPositions = [0] * 5

        if currentLetter in state["yellows"]:
            for position in state["yellows"][currentLetter]:
                forbiddenPositions[position] = 1

        yellowMatrix.append(forbiddenPositions)

    # Black information:
    # 26-dimensional binary vector indicating absent letters.
    blackVector = [0] * 26

    for blackLetter in state["blacks"]:
        letterIndex = ord(blackLetter) - ord("A")
        blackVector[letterIndex] = 1

    return {
        "greens": greenMatrix,
        "yellows": yellowMatrix,
        "blacks": blackVector,
        "attemptsLeft": state["attemptsLeft"]
    }


# Convert the structured encoding into a single feature vector
# suitable for ML datasets and model input.
def flattenEncodedState(encodedState):
    flatVector = []

    # Append green-position features
    for row in encodedState["greens"]:
        flatVector.extend(row)

    # Append yellow-position constraints
    for row in encodedState["yellows"]:
        flatVector.extend(row)

    # Append absent-letter information
    flatVector.extend(encodedState["blacks"])

    # Append remaining attempts as the final feature
    flatVector.append(encodedState["attemptsLeft"])

    return flatVector