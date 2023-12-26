
# AI_Checkers_Game

## Table of Contents
- [Introduction](#introduction)
- [Pygame](#pygame)
- [Game Rules Overview](#game-rules-overview)
  - [Objective](#objective)
  - [Capturing](#capturing)
  - [King Promotion](#king-promotion)
  - [Winning the Game](#winning-the-game)
- [Implementation of AIs](#implementation-of-ais)
  - [Evaluation Function](#evaluation-function)
  - [Minimax and Depth of Search](#minimax-and-depth-of-search)
  - [Alpha-Beta Pruning](#alpha-beta-pruning)
  - [Difficulty Levels: Easy, Intermediate, Hard](#difficulty-levels--easy-intermediate-hard)
- [Statistical Results](#statistical-results)
  - [Easy AI vs Intermediate AI](#easy-ai-vs-intermediate-ai)
  - [Easy AI vs Hard AI](#easy-ai-vs-hard-ai)
  - [Intermediate AI vs Hard AI](#intermediate-ai-vs-hard-ai)
- [Results Analysis](#results-analysis)
- [Conclusion](#conclusion)
- [Sources](#sources)

## Introduction
As part of the Artificial Intelligence course in the third year of the Computer Science and Applications degree at the University of Paris Cité, we were tasked with designing and developing a turn-based two-player perfect information game. The game should facilitate human player versus artificial player matches and provide an option to choose between three difficulty levels. For this project, we chose a variant of the checkers game: Anglo-American checkers. In this document, we will attempt to explain the path we followed to achieve our goals, detailing the obtained statistical results.

## Pygame
To execute the source code, you will need the Pygame library. You can install it on your machine using the following command:

    pip install pygame

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

## Implementation of AIs
One of the main challenges of this project was initially implementing artificial intelligence capable of making a decision to determine the best next move based on available information and computational capacity. Once done, we had to create AIs of different difficulty levels, using strategic concepts to enhance their abilities. Advanced AIs can use more complex strategies, giving them an advantage over weaker AIs and less experienced human players. Implementing difficulty levels involves a solid understanding of the rules and mechanics of the game to analyze and determine the best possible state based on various factors and situations.

### Evaluation Function
In artificial intelligence, an evaluation function is a method used to assess a given state or configuration in a given problem. In our case, it is used in the minimax algorithm we implemented. The goal of the evaluation function is to assign a numerical value to a state, which can be used to compare it with other possible states and determine the best action to take from that situation. In general, the more factors the evaluation function considers, the better the AI will be at making the best possible decision. In our case, it must provide precise and useful information about the position of pieces on the board, enabling the AI to make informed decisions about movements. Additionally, adding coefficients to our factors to give them more or less weight can be beneficial. A more sophisticated evaluation function allows the AI to better understand complex configurations and interactions between pieces on the board, resulting in more advanced decisions. Here are our choices for the evaluation function:

    ▪ Easy AI: Considers the difference in the number of pieces for each player on the board.

    ▪ Intermediate AI: Same as the Easy AI, also considers the difference in the number of kings on the board.

    ▪ Hard AI: Same as the Intermediate AI, also considers the position of the pieces (close to king promotion, blocked pieces, attacking pieces).

### Minimax and Depth of Search
The Minimax algorithm is a search algorithm used in artificial intelligence for decision-making in two-player zero-sum games, such as chess or tic-tac-toe. Its goal is to find the best possible move for a player from a given state. It assumes that each player seeks to maximize their own gain and minimize the opponent's gain. The Minimax algorithm uses a maximum depth to not exceed. By limiting the depth of the search, the Minimax algorithm can explore the search tree up to a certain depth and evaluate the reached positions, determining the best move to play in that situation. The depth of the search is a compromise between the quality of the decision made and the time required for computation.

It is important to note that a higher depth of search makes it more likely for the Minimax algorithm to find the best possible decision, but it also increases computation time. Conversely, a low depth of search may result in less precise decisions obtained more quickly. Additionally, changing the depth of search will significantly impact the performance of the AI. Here are our choices for the depth:

    ▪ Easy AI: Depth 1.
    ▪ Intermediate AI: Depth 3.
    ▪ Hard AI: Depth 5.

### Alpha-Beta Pruning
Alpha-beta pruning is a technique used in the Minimax algorithm to reduce the number of nodes in the search tree to explore, optimizing the performance of the AI. Pruning involves eliminating certain branches of the search tree that are unlikely to lead to an optimal solution, saving computation time. This technique eliminates branches of the search tree that are not relevant based on the minimum and maximum values already calculated for previous nodes. It works by comparing the calculated minimum and maximum values for previous nodes with those of the following nodes. If a branch has a minimum or maximum value that cannot improve the already obtained result, it can be pruned without affecting the final result. In our project, we implemented this technique to minimize the time complexity of our search algorithm.


### Difficulty Levels : Easy, Intermediate, Hard
We were tasked with implementing three different difficulty levels for the AIs, ranging from easy to hard. To achieve this goal, we assigned each AI a different evaluation function and search depth. Indeed, the complexity of the evaluation function and the search depth are two key factors in determining the difficulty of the AI in the context of our game. In other words, the given evaluation function is more or less complex depending on the desired AI difficulty, and the associated search depth is more or less significant to widen the difficulty gap between our AIs.

## Statistical Results
To compare our AIs and gain a better understanding of their performances for optimization, we had them play against each other for a total of 1000 consecutive games. After adjusting certain parameters to obtain distinct and consistent results, here's what we obtained:

### Easy AI vs Intermediate AI
Victory Rates:

    ▪ Easy AI: 1.6%
    ▪ Intermediate AI: 98.4%
Draws:
    
    ▪ None

*   Note: Draws are relatively rare. Generally, one of the AIs will eventually prevail.

### Easy AI vs Hard AI
Victory Rates:

    ▪ Easy AI: 0.3%
    ▪ Hard AI: 99.7%

Draws:

    ▪ None

### Intermediate AI vs Hard AI
For this case, we each ran 500 games on our side to optimize our time and avoid letting the code run for too long. Here are the results:

Victory Rates:

    ▪ Intermediate AI: 18.5%
    ▪ Hard AI: 81.2%

Draws:

    ▪ 3 draws: 0.3%

### Results Analysis
It's noticeable that the Hard AI prevails significantly against each difficulty level. Additionally, the Easy AI wins very rarely, which is quite consistent. The assigned parameters that led to this outcome have thus been retained.

## Conclusion
In conclusion, the observed results are more than satisfactory concerning our expectations. Moreover, this project allowed us to develop and put into practice our skills in Artificial Intelligence. Furthermore, it provided us with the opportunity to work as a team on a concrete problem. We are confident that the knowledge gained will be valuable for our future work in Artificial Intelligence.

## Sources
Below is a GitHub link to a similar project that helped us code the base of the game without AI: https://github.com/techwithtim/Python-Checkers
We drew inspiration from the functions and classes to have a functional game base that we later optimized and improved to align more closely with our goals. For instance, we added different functions to modify certain rules and game modes. We implemented mandatory capturing, a draw condition based on move limits, methods for having AIs play against each other, a method to let a human play against an AI by choosing the desired difficulty, a menu to launch the desired game mode (player vs. player, player vs. AI, AI vs. AI), and various methods to implement the AIs.
