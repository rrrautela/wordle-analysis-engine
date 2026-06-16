from words import allWords

# Return all words that satisfy the current state constraints
def filterCandidates(state):
    candidates = []

    # Check every word in dictionary
    for word in allWords:
        valid = True

        # Green check
        # Known letters must be at exact positions
        for i in range(5):
            if state["greens"][i] != "":
                if word[i] != state["greens"][i]:
                    valid = False
                    break

        # Skip further checks if already invalid
        if not valid:
            continue

        # Yellow check
        # Letter must exist, but not in forbidden positions
        for letter in state["yellows"]:

            # Letter must be present somewhere
            if letter not in word:
                valid = False
                break

            # Letter cannot appear in yellow-marked positions
            for pos in state["yellows"][letter]:
                if word[pos] == letter:
                    valid = False
                    break

            if not valid:
                break

        # Skip black check if already invalid
        if not valid:
            continue

        # black check
        # Eliminated letters cannot appear in the word
        # duplicate letter cases might break a bit due to flawed black check here
        for blackLetter in state["blacks"]:
            if blackLetter in word:
                valid = False
                break

        # Word satisfies all constraints
        if valid:
            candidates.append(word)

    return candidates

# Count how often each letter appears in candidate words
def buildLetterFrequency(words):
    frequency = {}

    for word in words:
        for letter in set(word):
            frequency[letter] = frequency.get(letter, 0) + 1

    return frequency

# Score a word using letter frequencies
def scoreWord(word, frequency):
    score = 0

    for letter in set(word):
        score += frequency.get(letter, 0)

    return score

# Return the highest scoring candidate word
def findBestGuess(candidates):
    frequency = buildLetterFrequency(candidates)

    bestWord = ""
    bestScore = -1

    for word in candidates:
        score = scoreWord(word, frequency)

        if score > bestScore:
            bestScore = score
            bestWord = word

    return bestWord
