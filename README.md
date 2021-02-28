# Sudoku_py

## About
This is a personal mini-project where I made a functional Sudoku game using the Tkinter framework.  
This is a learning exercise for Tkinter and coding with recursion for fun.

### Pre-Requsites / Dependencies
1. Tkinter
2. Python 3.9
3. Pandas, Numpy and Matplotlib for `sudogenanalysis`

This build was tested on a Windows 10 machine.

## Repo Highlights
### 1.  **Full Sudoku Board Algorithms**  
  sudogen, sudogen1, sudogen2 and sudogen3 are scripts to generate a full sudoku grid (2D List) using recursive algorithms with some variation between them.  
### sudogen
The most efficient script. It is a greedy and naiive algorithm, building the sudoku grid row by row randomly, choosing a number to populate each cell from a pool of possible values.    
When there are no solutions possible while building the row, the entire row is thrown away and re-built recursively.   
There may be a case where no permutation of values in the row can satisfy sudoku rules due to the arrangement of the previous row.  
A recursion counter is used to prevent infinite looping. When its threshold is met, the current row and the row before it are cleared and re-built.  

### sudogen2
sudogen2 operates similarly to sudogen. However, it allows backtracking within a row.  
If all possible permutations in the row do not produce a valid solution, the row and the row before it is thrown away and re-built.

### sudogen3  
sudogen3 implements a more thorough backtracking algorithm, tracking all failed values for every cell in the sudoku matrix.  

### 2. Algorithm Analysis 
  I compared the efficiency of the algorithms based on how many ```getAvailValues()``` calls are made to generate the matrix. (sudogenanalysis.py)  
  Each function call relates to how many cells have been built.
  The graphs made with matplotlib will be included in an additional folder soon.
  
### 3. Sudoku Game
  A functional Sudoku GUI game with the ability to change difficulty and check value correctness.  
  For now, the game will only start if sudoku.py is called from the terminal. 
 
## How to play
If you wish to play the game:

1. Ensure you have the pre-requisites as mentioned above first.
2. Download `sudogen.py`, `sudoku.py` and `sudodatahandler`
3. Run sudoku.py