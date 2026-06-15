Wordle Analysis Engine

A machine learning project that aims to build a Chess.com-style post-game analysis system for Wordle.

The long-term goal is to analyze completed Wordle games, replay every move, compare player decisions against strong Wordle solvers and ML models, and generate natural-language explanations for better moves.

Features (Planned)

* Wordle game environment
* Rule-based expert solver
* Dataset generation through self-play
* PyTorch model training
* Move-by-move game analysis
* Structured JSON reports
* LLM-generated explanations
* Integration with Wordle PvP

Current Progress

Day 1

* Playable Wordle environment
* Input validation
* Green / Yellow / Grey feedback
* Win/Loss detection
* Dictionary validation

Tech Stack

* Python
* PyTorch (planned)
* NumPy (planned)
* Matplotlib (planned)

Example Goal

Player guess:

CRANE

Solver recommendation:

SLATE

Generated explanation:

“The solver preferred SLATE because it would have eliminated more candidate words and provided higher information gain.”

Status

Work in progress.