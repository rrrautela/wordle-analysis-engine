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

# Flaten the nested array to a 1D array
def flattenEncodedState(encodedState):
    flatVector = []

    # Flatten green matrix
    for row in encodedState["greens"]:
        flatVector.extend(row)

    # Flatten yellow matrix
    for row in encodedState["yellows"]:
        flatVector.extend(row)

    # Add black vector
    flatVector.extend(encodedState["blacks"])

    # Add attempts left
    flatVector.append(encodedState["attemptsLeft"])

    return flatVector
