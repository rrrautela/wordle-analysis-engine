"""
main.py

Project entry point.

Used to launch benchmark runs and evaluate the current Wordle solver.

Adjust the number of games passed to `benchmarkSolver()` to control
benchmark size and runtime.
"""

from benchmark import benchmarkSolver


# Run a benchmark and print aggregate solver statistics.
benchmarkSolver(1000)