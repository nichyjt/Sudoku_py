from random import randint
"""
SUDOKU (SOLUTION) BOARD GENERATION v0.2
1. Sudoku board is built row by row with recursion
2. For every cell, its row, square and col value availability is checked
3. If no solution can be found, the row is re-built via recursion
4. If row is re-built too many times (500), break out of recursion..
4a. ..and re-build the row before.
5. Continue until every row is built.

There is some RNG involved for every iteration as
the row-generating algorithm is not aware what extra constraints are
added when it inserts a randomly chosen value in. The extra constraints
may make the sdku unsolvable, hence the need to backtrack.

"""
__recursionCounter = 0
__timesCalled = 0

# Returns the row/col limits for the cell's square
def getSquareLimits(rowIndex, colIndex):
    rowLimits, colLimits = [], []
    if colIndex < 3:
        colLimits = [0,3]
    elif colIndex < 6:
        colLimits = [3,6]
    else:
        colLimits = [6,9]
    if rowIndex < 3:
        rowLimits = [0,rowIndex+1]
    elif rowIndex < 6:
        rowLimits = [3,rowIndex+1]
    else:
        rowLimits = [6,rowIndex+1]
    # rowIndex+1 is set as the endlimit, saving computation time for the unfilled '0' rows
    return (rowLimits, colLimits)

# Main logic for sifting through usable data
# Aim here is to minimise memory usage
def getAvailValues(rowIndex, colIndex, grid):
    # For debugging and analysis purposes
    global __timesCalled
    __timesCalled +=1
    # Mapping of number of values that appear
    vmap = [0 for x in range(10)] 
    sqLim = getSquareLimits(rowIndex, colIndex)
    # Fn has disappointing time complexity (10+colIndex+rowIndex+9)
    # Logs occurences in row
    for i in range(colIndex+1):
        vmap[grid[rowIndex][i]] +=1
    # Log occurences in col
    for i in range(rowIndex+1):
        vmap[grid[i][colIndex]] +=1
    # Log occurences in the cell's square
    for ri in range(sqLim[0][0], sqLim[0][1]):
        for ci in range(sqLim[1][0], sqLim[1][1]):
            vmap[grid[ri][ci]] +=1
    unused = []
    for i in range(1,10):
        if vmap[i] == 0:
            unused.append(i)
    return unused

# Generate the sudoku board row in accordance with sdku rules
def generateRow(rowIndex, sudokuGrid):
    global __recursionCounter
    # Break recursion to backtrack and rebuild the previous row
    # Arbitrary number chosen 
    if(__recursionCounter>9):
        return
    for i in range(9):
        pool = getAvailValues(rowIndex, i, sudokuGrid)
        # Recursion managed by the global counter field
        if len(pool)==0:
            # No solution. Re-build row
            __recursionCounter +=1
            # print("Inner Backtrack")
            sudokuGrid[rowIndex] = [0 for x in range(9)]
            generateRow(rowIndex, sudokuGrid)
            return
        else:
            rdi = randint(0,8)
            if rdi >= len(pool):
                rdi = rdi%len(pool)
            sudokuGrid[rowIndex][i] = pool[rdi]
    # Row is built
    # print("Row Built!")

# Driver function to generate rows and manage recurion errors
def generateSudoku():
    # Reset times called for analysis purposes
    global __timesCalled
    __timesCalled = 0
    grid = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
    ]
    i = 0
    while i<9:
        global __recursionCounter
        if __recursionCounter > 9:
            # print("Backtracked")
            __recursionCounter = 0
            i-=1
            generateRow(i,grid)
        else:
            generateRow(i,grid)
            i+=1
    return grid

def getCalls():
    global __timesCalled
    return __timesCalled

# Debug
def sudoku_debug():
    """
    Prints out the sudoku board for debugging purposes
    """
    sudo = generateSudoku()
    for row in sudo:
        print(row)
    print(__timesCalled)
