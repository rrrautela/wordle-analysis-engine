import time
from game import playGame


# Run many games and print solver statistics
def benchmarkSolver(numGames=2200):
    # Start timer
    startTime = time.time()

    # Result counters
    wins = 0
    losses = 0
    errors = 0

    # Store turns from winning games
    turnsTaken = []

    # Run benchmark games
    for gameNumber in range(numGames):
        result = playGame()

        if result["won"] is True:
            wins += 1
            turnsTaken.append(result["turns"])

        elif result["won"] is False:
            losses += 1

        else:
            errors += 1

        # Show progress every 100 games
        if (gameNumber + 1) % 100 == 0:
            print(f"Completed {gameNumber + 1}/{numGames} games")

    # Calculate total runtime
    totalTime = time.time() - startTime

    print("\n===== BENCHMARK RESULTS =====")

    print(f"Games Played: {numGames}")

    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Errors: {errors}")

    print(f"Win Rate: {(wins / numGames) * 100:.2f}%")
    print(f"Loss Rate: {(losses / numGames) * 100:.2f}%")
    print(f"Error Rate: {(errors / numGames) * 100:.2f}%")

    # Turn statistics
    if turnsTaken:
        print(f"Average Turns: {sum(turnsTaken) / len(turnsTaken):.2f}")
        print(f"Best Game: {min(turnsTaken)} turns")
        print(f"Worst Game: {max(turnsTaken)} turns")

    print(f"Total Runtime: {totalTime:.4f} seconds")
    print(f"Average Runtime/Game: {totalTime / numGames:.6f} seconds")
