from random import randint

# This generator backtracks one value at a time rather than retrying a new row
"""
SUDOGEN 2.0
This sudoku board generator does not re-do rows
This algorithm backtracks cell by cell and keeps testing for pool values, blacklisting 
However, this algorithm does not keep track of previous *row* blacklists
A master blacklist list might improve efficiency
"""
# [[],[],[],[],[],[],[],[],[]]
__blacklistedVals = [[0 for x in range(10)] for x in range(9)]
__timesCalled = 0

# Returns the row/col limits for the cell's square
def getSquareLimits(rowIndex, colIndex):
    rowLimits, colLimits = [],[]
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
def getAvailValues(rowIndex, colIndex, grid):
    global __blacklistedVals
    global __timesCalled
    __timesCalled +=1
    vmap = [0 for x in range(10)] #0-9 so 10 vals
    sqLim = getSquareLimits(rowIndex, colIndex)
    # Disgusting time complexity
    # Logs occurences in row
    for i in range(0,colIndex+1):
        vmap[grid[rowIndex][i]] +=1
    # Log occurences in col
    for i in range(0,rowIndex+1):
        vmap[grid[i][colIndex]] +=1
    # Log occurences in the cell's square
    for ri in range(sqLim[0][0], sqLim[0][1]):
        for ci in range(sqLim[1][0], sqLim[1][1]):
            vmap[grid[ri][ci]] +=1
    unused = []
    for i in range(1,10):
        if vmap[i] == 0 and __blacklistedVals[colIndex][i]==0:
            unused.append(i)
    return unused

# Generate the sudoku board row in accordance with sdku rules
def generateRow(rowIndex, grid):
    global __blacklistedVals

    i = 0
    # Cell controller
    while i<9:
        #print("Curr Coords: "+str(rowIndex)+', '+str(i))
        pool = getAvailValues(rowIndex, i, grid)
        # Recursion managed by the global counter field
        if(len(pool)==0):
            # No solution. Backtrack one step, blacklist the prev value and try again
            # print("Inner Backtracked")
            __blacklistedVals[i] = [0 for x in range(10)]
            i-=1
            if i<0:
                return True
            __blacklistedVals[i][grid[rowIndex][i]] +=1
            grid[rowIndex][i] = 0
        else:
            rdi = randint(0,8)
            if rdi >= len(pool):
                rdi = rdi%len(pool)
            grid[rowIndex][i] = pool[rdi]
            i+=1
    # Row is built
    #print("Row Built!")
    return False

# Driver function to generate rows and manage recurion errors
def generateSudoku():
    # For debug
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
    global __blacklistedVals
    i = 0
    while i<9:
        if generateRow(i, grid):
            # Row has failed to build. Re-build the previous row and blacklist
            grid[i] = [0 for x in range(9)]
            __blacklistedVals = [[0 for x in range(10)] for x in range(9)]
            i-=1
            grid[i] = [0 for x in range(9)]
        else:
            i+=1
    return grid

def getCalls():
    global __timesCalled
    return __timesCalled


def debug():
    for row in generateSudoku():
        print(row)
    print(__timesCalled)
