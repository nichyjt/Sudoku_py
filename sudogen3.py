from random import randint

# This generator backtracks one value at a time rather than re-building the row.
"""
SUDOGEN 3.0
This sudoku board generator implements a more complete blacklist history.
The algorithm retains previous rows' blacklists so that when a row backtracks,
'Failable' values are excluded from the pool.
This comes at a high cost of space efficiency as the blacklist is 3 layers deep
"""
# Reset blacklist for bulk fn calls
def make_new_blacklist():
    return [[[0 for x in range(10)]for y in range(9)]for z in range(9)]
__blacklistedVals = make_new_blacklist()
__infiniteRecursion = False
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
        if vmap[i] == 0 and __blacklistedVals[rowIndex][colIndex][i]==0:
            unused.append(i)
    return unused

# Generate the sudoku board row in accordance with sdku rules
def generateRow(rowIndex, grid, index):
    global __blacklistedVals
    #print("Rowgen Called At: "+str(rowIndex)+", "+str(index))
    while index<9:
        pool = getAvailValues(rowIndex, index, grid)
        if(len(pool)==0):
            # No solutions found.
            # Backtrack one step, blacklist the changed value and try again 
            # s_grid[rowIndex][i] = 0
            index-=1
            if index<0:
                return True
            __blacklistedVals[rowIndex][index][grid[rowIndex][index]] +=1
            grid[rowIndex][index] = 0
        else:
            rdi = randint(0,8)
            if rdi >= len(pool):
                rdi = rdi%len(pool)
            grid[rowIndex][index] = pool[rdi]
            index+=1
    # Row is built
    #print("Row Built!")
    return False

# Driver function to generate rows and manage recurion errors
def generateSudoku():
    # For debug and analysis
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
    global __infiniteRecursion
    i = 0
    specificIndex = 0
    new_coords = []
    while i<9:
        if generateRow(i, grid, specificIndex):
            # recursion loops forever when the cell's pool is only 1 value when it backtracks
            # print("Recursion Start")
            i = backtrackRow(i)
            if i<0:
                for x in range(9):
                    print (grid[x])
                #print("List Error Caught")
                break
            tmp = backtrackCell(i, 8, grid, __infiniteRecursion)
            if new_coords == tmp:
                #print("Possible Infinite Recursion Caught")
                __infiniteRecursion = True
            else:
                __infiniteRecursion = False
                new_coords = tmp
                #print('New Coords: ' + str(new_coords))
                specificIndex = new_coords[1]
                i = new_coords[0]
        else:
            #print("Row OK")
            specificIndex = 0
            i+=1
    __blacklistedVals = make_new_blacklist()
    #print("------------------DONE--------------------")
    return grid

# Clear the blacklist for the row and try again
# returns the new rowIndex value
def backtrackRow(rowIndex):
    global __blacklistedVals
    __blacklistedVals[rowIndex] = [[0 for x in range(10)] for y in range(9)]
    return rowIndex-1

# Backtrack cell by cell until we have a pool of > 1
# Rare edge case whereby the backtrack cycles about a cell. The rows are built with no solution.
# This case + others caught by the infiniteLoop flag.
def backtrackCell(rowIndex, colIndex, grid, infiniteLoop):
    #print('Curr Coords: ' + str(rowIndex)+', '+str(colIndex))
    if(colIndex<0):
        rowIndex = backtrackRow(rowIndex)
        colIndex = 8
    pool = getAvailValues(rowIndex, colIndex, grid)
    if len(pool) > 1 and not infiniteLoop:
        return [rowIndex, colIndex]
    else:
        infiniteLoop = False
        grid[rowIndex][colIndex] = 0
        #print('Cell Backtracked')
        return backtrackCell(rowIndex, colIndex-1, grid, infiniteLoop)

def getCalls():
    global __timesCalled
    return __timesCalled

# Debug
def printBoard():
    for i in range(3):
        sudo = generateSudoku()
        for row in sudo:
            print(row)
        print(__timesCalled)

def debug():
    for row in generateSudoku():
        print(row)
    print(__timesCalled)