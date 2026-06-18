"""
benchmark.py

Evaluates solver performance by running a large number of automated
Wordle games and collecting aggregate statistics.

Metrics reported:
- Win / loss / error counts
- Win, loss, and error rates
- Average, best, and worst game length
- Total runtime and average runtime per game

Useful for measuring solver accuracy, consistency, and efficiency,
as well as validating changes to the solving algorithm.
"""

import time
from game import playGame
import pickle




# Run multiple automated games and summarize solver performance.
def benchmarkSolver(numGames):

    # Track benchmark execution time.
    startTime = time.time()

    # Aggregate game outcomes.
    wins = 0
    losses = 0
    errors = 0

    # Number of turns required for successful games.
    turnsTaken = []

    datasetStates = []
    datasetLabels = []

    # Execute the requested number of games.
    for gameNumber in range(numGames):
        result = playGame(datasetStates, datasetLabels)

        if result["won"] is True:
            wins += 1
            turnsTaken.append(result["turns"])

        elif result["won"] is False:
            losses += 1

        else:
           print(f"\nError in game {gameNumber}")
           print(result)
           errors += 1

        # Periodic progress update for long benchmark runs.
        if (gameNumber + 1) % 100 == 0:
            print(f"Completed {gameNumber + 1}/{numGames} games")

    totalTime = time.time() - startTime

    print("\n===== BENCHMARK RESULTS =====")

    print(f"Games Played: {numGames}")

    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Errors: {errors}")

    print(f"Win Rate: {(wins / numGames) * 100:.2f}%")
    print(f"Loss Rate: {(losses / numGames) * 100:.2f}%")
    print(f"Error Rate: {(errors / numGames) * 100:.2f}%")

    # Report game-length statistics for successful runs.
    if turnsTaken:
        print(f"Average Turns: {sum(turnsTaken) / len(turnsTaken):.2f}")
        print(f"Best Game: {min(turnsTaken)} turns")
        print(f"Worst Game: {max(turnsTaken)} turns")

    print(f"Total Runtime: {totalTime:.4f} seconds")
    print(f"Average Runtime/Game: {totalTime / numGames:.6f} seconds")



    
    print(f"Dataset Samples: {len(datasetStates)}")
    print(f"Feature Count: {len(datasetStates[0])}")

    # print("\nFirst State:")
    # print(datasetStates[0])

    # print("\nFirst Label:")
    # print(datasetLabels[0])

    # print("\nLast State:")
    # print(datasetStates[-1])

    # print("\nLast Label:")
    # print(datasetLabels[-1])

   


    filename = f"dataset_{numGames}_{int(time.time())}.pkl"

    print(f"\nSaving dataset to {filename}...")
    with open(filename, "wb") as f:
        pickle.dump(
            {
                "states": datasetStates,
                "labels": datasetLabels
            },
            f
        )

    print("Dataset saved successfully.")



