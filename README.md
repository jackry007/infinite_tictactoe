# Infinite Tic-Tac-Toe 

This is a custom implementation of Tic-Tac-Toe using Pygame, with unique rules where each player is limited to three pieces on the board at a time. When a player tries to place a fourth piece, the game instead chooses a piece to be removed and then placed in an open spot. The goal is to align three pieces in a row (horizontally, vertically, or diagonally) to win.

## Game Rules

- The board is a standard 3x3 Tic-Tac-Toe grid.
- Players alternate turns, starting with 'X'.
- Each player can only have **three** pieces on the board at any given time.
- After placing three pieces, the game randomly selects an existing pieces to an open spot to continue.
- A player wins by forming a straight line of three pieces horizontally, vertically, or diagonally.

## How to Play

1. **Start the game**: 
   - Run the Python script to start the game.
   - The first player (X) clicks an empty spot on the grid to place their piece.
   - Players alternate turns.

2. **Move phase**: 
   - Once a player has three pieces on the board, they must move one of their existing pieces.
   - To move, first click on the piece you want to move, then click on the empty spot you want to move it to.

3. **Win the game**:
   - The first player to get three pieces in a row (horizontally, vertically, or diagonally) wins.

## Requirements

- Python 3.x
- Pygame library

You can install the necessary dependencies with:

```bash
pip install pygame
