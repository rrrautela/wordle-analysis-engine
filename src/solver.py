"""
solver.py

Contains the core Wordle-solving logic.

Responsibilities:
- Filter dictionary words using known game constraints
- Estimate letter usefulness using candidate frequencies
- Score candidate guesses
- Select the next guess expected to reveal the most information

The solver follows a frequency-based strategy: letters that appear
in many remaining candidate words are considered more valuable.
"""

from words import allWords

# Return all dictionary words that satisfy the current game state.
def filterCandidates(state):
    candidates = []

    # Evaluate every possible answer word.
    for word in allWords:
        valid = True

        # Green constraints:
        # confirmed letters must remain in their known positions.
        for i in range(5):
            if state["greens"][i] != "":
                if word[i] != state["greens"][i]:
                    valid = False
                    break

        # No need to evaluate additional constraints.
        if not valid:
            continue

        # Yellow constraints:
        # letter must exist but cannot occupy forbidden positions.
        for letter in state["yellows"]:

            # Yellow letters are known to exist in the answer.
            if letter not in word:
                valid = False
                break

            # Exclude positions already proven incorrect.
            for pos in state["yellows"][letter]:
                if word[pos] == letter:
                    valid = False
                    break

            if not valid:
                break

        # Avoid unnecessary work for rejected words.
        if not valid:
            continue

        # Black constraints:
        # letters believed absent should not appear in the candidate.
        # Known limitation: duplicate-letter scenarios are not fully modeled.
        for blackLetter in state["blacks"]:
            if blackLetter in word:
                valid = False
                break

        # Candidate survives every constraint.
        if valid:
            candidates.append(word)

    return candidates

# Count how many candidate words contain each unique letter.
def buildLetterFrequency(words):
    frequency = {}

    for word in words:
        # Count each letter once per word to avoid rewarding duplicates.
        for letter in set(word):
            frequency[letter] = frequency.get(letter, 0) + 1

    return frequency

# Score a word based on the information value of its letters.
def scoreWord(word, frequency):
    score = 0

    # Sum frequencies of unique letters only.
    for letter in set(word):
        score += frequency.get(letter, 0)

    return score

# Select the highest-scoring candidate as the next guess.
def findBestGuess(candidates):
    # Estimate letter usefulness across remaining candidates.
    frequency = buildLetterFrequency(candidates)

    bestWord = ""
    bestScore = -1

    # Evaluate every remaining candidate.
    for word in candidates:
        score = scoreWord(word, frequency)

        # Keep track of the best candidate seen so far.
        if score > bestScore:
            bestScore = score
            bestWord = word

    return bestWord
