# Chkobba Game

**Author** : [Assil Rguez](https://assilrguez.github.io)

## Overview
Chkobba is a traditional North African card game. This Python implementation allows you to play against another player or challenge an AI opponent(**coming late**).
[learn more](./RULES.md)

## File Structure
- `main.py`: The core of the game, managing the game flow and user interface.
- `ai.py`: Handles AI logic and decision-making based on the game's current state. (*Not ready yet*)
- `RULES.md`: Detailed Chkobba game rules.

## How to Play
1. Run `main.py`.
2. Choose to play against another player or the AI.
3. Play by choosing cards to match or add up to values on the table.
4. The game tracks your points, and the winner is determined at the end of the deck.

## Game Statistics
At the end of each game, the statistics, including points and Chkobba counts, are displayed. The statistics help you track your performance over multiple games.

## How to Run
1. Ensure you have Python 3.x installed .
2. Ensure that both `main.py` and `ai.py` are in the same directory .
3. Run the game with:
   ```bash
   python main.py