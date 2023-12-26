
# AI_Checkers_Game

## Introduction
As part of the Artificial Intelligence course in the third year of the Computer Science and Applications degree at the University of Paris Cité, we were tasked with designing and developing a turn-based two-player perfect information game. The game should facilitate human player versus artificial player matches and provide an option to choose between three difficulty levels. For this project, we chose a variant of the checkers game: Anglo-American checkers. In this document, we will attempt to explain the path we followed to achieve our goals, detailing the obtained statistical results.

## Required
To execute the source code, you will need a Python 3.x version and the Pygame library. You can install it on your machine using the following command:

    pip install pygame

## How To Run The Game
To run the game, simply run *main.py* then choose a game mode and a difficulty level in the terminal prompt.

## Game Rules Overview
The Anglo-American checkers game is played on a 64-square board, alternately dark and light, arranged in a checkerboard pattern. Each player has 12 pieces of light or dark color, placed on the dark squares of the three rows closest to each player.

### Objective
The goal of the game is to capture all the opponent's pieces or block them in such a way that they cannot move anymore. Pieces can move diagonally to adjacent squares, but only forward. Movement is exclusively on dark squares.

### Capturing
A piece can capture (or "eat") an opponent's piece by jumping over it diagonally to an empty square behind the opponent's piece. Multiple captures in a single turn are possible. Note: Capturing is mandatory, meaning the player must capture if possible.

### King Promotion
If a piece reaches the last row of the opponent's side, it is promoted to a king. Kings can move diagonally in all directions (up to one square), but we did not implement the ability for kings to "fly," meaning they cannot jump over multiple squares at once.

### Draw
We imposed a move limit on AIs to prevent endless games. If the limit is reached and no captures have occurred, the game is declared a draw (which is relatively rare). Otherwise, with each new capture, the counter resets.

### Winning the Game
In our game, there are two ways to win. The first is to capture all the opponent's pieces. The second indirect way to win is if the opponent can no longer make a legal move.

## Sources
Below is a GitHub link to a similar project that helped us code the base of the game without AI: https://github.com/techwithtim/Python-Checkers
We drew inspiration from the functions and classes to have a functional game base that we later optimized and improved to align more closely with our goals. For instance, we added different functions to modify certain rules and game modes. We implemented mandatory capturing, a draw condition based on move limits, methods for having AIs play against each other, a method to let a human play against an AI by choosing the desired difficulty, a menu to launch the desired game mode (player vs. player, player vs. AI, AI vs. AI), and various methods to implement the AIs.
