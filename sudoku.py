from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
import sudodatahandler as sdh

root = Tk()
root.title("Sudoku")
# Geometry to keep window static
root.resizable(False, False)

# NOTE, widget.grid dictates the layout of widgets. If grid is not invoked it is not shown

class GameData:
    """Stores the game data and answers"""
    gameBoard = []
    answer = []
    def __init__(self):
        pass
    def firstGame(self, difficulty:str='Easy'):
        data = sdh.getSudokuData(difficulty)
        self.gameBoard = data[0]
        self.answer = data[1]
        self.difficulty = difficulty
    def newGame(self, difficulty:str='Easy'):
        self.gameBoard.clear()
        self.answer.clear()
        data = sdh.getSudokuData(difficulty)
        self.gameBoard = data[0]
        self.answer = data[1]
        self.difficulty = difficulty
        
class EntryCell:
    """Stores an sudoku entry's UI params."""
    # Each cell object relates to an index on the sudoku grid
    # The cell will provide params to create either an entry OR an label
    def __init__(self, rowIndex=0, colIndex=0):
        self.sudoku_index = (rowIndex, colIndex)
        self.entryStr = StringVar()
        self.entryStr.trace('w', self.charLimit)

    def setEntryObject(self, entryObj:ttk.Entry):
        # Holds the pointer to the ttk Entry object created for this cell
        self.entryUI = entryObj

    def charLimit(self, *args):
        entryStr = self.entryStr
        if not entryStr.get().isdigit():
            entryStr.set(entryStr.get()[:0])
        elif len(entryStr.get()) > 1:
            entryStr.set(entryStr.get()[:1])
        if self.entryUI['bg']!='snow':
            self.entryUI.config(bg='snow')

    def getEntryCoords(self):
        return self.sudoku_index
        

class Main:
    style = ttk.Style()
    style.configure("sudoFrame.TFrame", background = 'white')
    style.configure("optionStyle.TMenubutton", background='ivory')
    def __init__(self, root):
        titleFont = font.Font(size = 20)

        # Data Init
        self.gameData = GameData()
        self.entries = []
        # First Game Init
        self.gameData.firstGame()

        # MainFrame
        self.mainframe = ttk.Frame(root, padding="10")
        self.mainframe.grid(sticky=(N,S,E,W))
        self.mainframe.columnconfigure(0, weight=1)

        # Top Frame
        self.topFrame = ttk.Frame(self.mainframe, padding = '5')
        self.topFrame.grid(sticky=(N,S,E,W))
        self.topFrame.columnconfigure(0, weight=1)

        # Top Frame Widgets
        self.details = ttk.Label(self.topFrame, text=str(self.gameData.difficulty)+" Board",\
            font=titleFont)
        self.details.grid(column = 0, row = 0, sticky='W')
        
        diffOptions = ('Easy', 'Medium', 'Hard')
        self.difficultyVar = StringVar()
        #self.difficultyVar.set(diffOptions[0])
        self.difficultyPicker = ttk.OptionMenu(self.topFrame, self.difficultyVar, diffOptions[0],\
             *diffOptions, style='optionStyle.TMenubutton')
        self.difficultyPicker.grid(column = 3, row = 0, columnspan=3, sticky=E)
        #self.buttonPlaceholder = ttk.Label(self.mainframe, text="Buttons will be placed here soon")
        #self.buttonPlaceholder.grid(column = 0, row =2)
        
        # SudoBoardFrame
        self.sudoFrame = ttk.Frame(self.mainframe, padding = '10', style = 'sudoFrame.TFrame')
        self.sudoFrame.grid(column=0, row =1, sticky=(N,S,E,W))
        
        # Buttons Frame
        self.buttonsFrame = ttk.Frame(root, padding = "10" )
        self.buttonsFrame.grid(column=0, row =2)
        # Buttons Frame Widgets
        self.newGame = ttk.Button(self.buttonsFrame, text='New Game', command=self.startNewGame)
        self.newGame.grid(column = 0, row = 0, padx=20)
        self.clearBoardBtn = ttk.Button(self.buttonsFrame, text='Clear Board', command=self.clearBoard)
        self.clearBoardBtn.grid(column=1, row = 0, padx = 20)
        self.validate = ttk.Button(self.buttonsFrame, text='Check Answers', command=self.checkAnswers)
        self.validate.grid(column = 2, row = 0, padx=20)
        
    # When there is a new game, genUI creates a new set of data and cell UIs 
    def generateBoardUI(self):
        clueFont = font.Font(size = 22)
        for ri in range(0,18,2):
            for ci in range(0,18,2):
                cellVal = self.gameData.gameBoard[int(ri/2)][int(ci/2)]
                if(cellVal > 0):
                    # clue logic
                    clue_ui = Label(self.sudoFrame, text = cellVal, width = 2, height = 1,\
                     font=clueFont, bg='white')
                    clue_ui.grid(row = ri, column = ci, padx=2, pady=2)
                else:
                    # Populate entry list and create an entry cell
                    entryCell = EntryCell(int(ri/2), int(ci/2))
                    entry_ui = Entry(self.sudoFrame, font = clueFont, \
                     bg='snow', fg='navy', textvariable = entryCell.entryStr,\
                     width = 2, justify = CENTER)
                    entry_ui.grid(row = ri, column = ci, padx=2, pady=2)
                    entryCell.setEntryObject(entry_ui)
                    self.entries.append(entryCell)
        # Use an empty frame as a divider
        # This took too long
        for i in range(1,16,2):
            if(i==5 or i==11 or i==16):
                hori = Frame(self.sudoFrame, bg='black', height = 3)
                vert =  Frame(self.sudoFrame, bg='black', width = 3)
            else:
                hori = Frame(self.sudoFrame, bg='black', height = 1)
                vert =  Frame(self.sudoFrame, bg='black', width = 1)
            hori.grid(row = i, columnspan = 18, sticky = EW)
            vert.grid(column = i, row = 0, rowspan=100, sticky = NS)

    def checkAnswers(self):
        """
        Highlights answers in the grid that are wrong.
        """
        for entry in self.entries:
            wrong = False
            val = entry.entryStr.get()
            if val == '':
                wrong = not wrong
                continue
            rowIndex, colIndex = entry.getEntryCoords()
            if self.gameData.answer[rowIndex][colIndex] != int(val):
                wrong = not wrong
                entry.entryUI.config(bg='tomato')
            else:
                entry.entryUI.config(bg='light green')
        if not wrong:
            # TODO Congratulations dialog?
            print("You win!")

    
    def clearBoard(self):
        dialog = messagebox.askquestion(title='Clear Board',\
            message ='This cannot be undone. Clear board?')
        if dialog:
            for entry in self.entries:
                entry.entryStr.set(entry.entryStr.get()[:0])

    def startNewGame(self):
        dialog = messagebox.askyesno(title='New Game', \
            message='Are you sure you want to start a new game?')
        if dialog:
            self.gameData.newGame(difficulty=self.difficultyVar.get())
            self.setTopFrameDetails()
            self.entries.clear()
            self.generateBoardUI()

    def setTopFrameDetails(self):
        self.details['text'] = str(self.gameData.difficulty)+" Board"

            
# Event Driver
main = Main(root)
main.generateBoardUI()
root.mainloop()