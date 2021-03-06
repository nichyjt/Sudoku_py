# This module serves to handle the bulk of game logic
import sudogen as sg
from random import randint, sample

"""
SUDO DATA HANDLER
This module generates a full sudoku board and randomly pops values off to make a game.
NOTE: The answer checking implementation is lazy. It is not dynamic, and only checks inputs against the original board.
"""

def getSudokuData(difficulty:str='Easy')->tuple:
    """
    Returns a tuple (game:list, answer:list) containing a new game and its answer key.
    """
    # Difficulty is arbitrarily set with various ranges of numClues.
    numClues = 0
    if difficulty == 'Easy':
        numClues = randint(37,40)
    elif difficulty == 'Medium':
        numClues = randint(27,36)
    else:
        numClues = randint(20,26)
    answer = sg.generateSudoku()
    game = popClues(deepCopySudo(answer), numClues)
    return (game, answer)

def popClues(sudokuGrid, numClues)->list:
    """
    Remove answers from the full sudoku board to create a game.
    """
    popList = sample([i for i in range(0,81)], 81-numClues)
    for num in popList:
        row, col = int(num/9), int(num%9) 
        # print(str(row)+","+str(col))
        sudokuGrid[row][col] = 0
    return sudokuGrid

def deepCopySudo(grid)-> list:
    """
    Returns a deep copy list of a sudoku grid.
    """
    # Alternatively, only save answers & their indexes in a dict to save memory.
    newGrid = [[0 for j in range(9)]for i in range(9)]
    for i in range(9):
        for j in range(9):
            newGrid[i][j] = grid[i][j]
    return newGrid

def debug():
    sdku = sg.generateSudoku()
    game = deepCopySudo(sdku)
    game = popClues(game, 80)
    for rowA, rowB in zip(game, sdku):
        print(str(rowA)+"|"+str(rowB))
