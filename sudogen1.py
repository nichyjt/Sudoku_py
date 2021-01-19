from random import randint
"""
SUDOKU (SOLUTION) BOARD GENERATION
This module is a copy of sudogen. This script varies the recursion limit to see how
it affects the variance and performance of the alg.
"""
recursionCounter = 0
__recursionLimit = 50
__timesCalled = 0

# Returns the row/col limits for the cell's square
def getSquareLimits(rowIndex, colIndex):
    rowLimits = []
    colLimits = [] 
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
    # rowIndex+1 is set as the endlimit
    # This saves computation time for the unfilled '0' rows
    return (rowLimits, colLimits)

# Main logic for sifting through usable data
# Aim here is to minimise memory usage
def getAvailValues(rowIndex, colIndex, sudokuGrid):
    # For debug
    global __timesCalled
    __timesCalled +=1

    grid = sudokuGrid
    vmap = [0 for x in range(10)]
    sqLim = getSquareLimits(rowIndex, colIndex)
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
    global recursionCounter
    global __recursionLimit

    if(recursionCounter>__recursionLimit):
        return
    for i in range(9):
        pool = getAvailValues(rowIndex, i, sudokuGrid)
        # Recursion managed by the global counter field
        if(len(pool)==0):
            # No solution. Re-build row
            recursionCounter +=1
            sudokuGrid[rowIndex] = [0 for x in range(9)]
            generateRow(rowIndex, sudokuGrid)
            return
        else:
            rdi = randint(0,8)
            if rdi >= len(pool):
                rdi = rdi%len(pool)
            sudokuGrid[rowIndex][i] = pool[rdi]
    #print("Row Built!")

# Driver function to generate rows and manage recursion errors
def generateSudoku():
    # For testing
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
        global recursionCounter
        global __recursionLimit
        if recursionCounter > __recursionLimit:
            #print("Backtracked")
            recursionCounter = 0
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
def debug():
    for row in generateSudoku():
        print(row)
    print(__timesCalled)


