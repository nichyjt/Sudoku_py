# Sudogen Graphs

## About
This folder contains some graphs comparing the different sudoku generator algorithms.
The main metric being evaluated is the number of `getAvailValues()` lookup calls being made.
This is because the call is always execuetd before a cell is populated with a value or a backtrack decision is made, and is the most 'costly' part of the generator.

### Figure 1
The Figure 1 set of graphs contain scatters of each sudogen script to the number of lookup calls.

### Figure 2
The Figure 2 set of graphs contain box plots of each sudogen script.
It is clearly seen that in terms of efficiency, sudogen1 > sudogen2 > sudogen3.  

### Figure 3
The Figure 3 set of graphs contain box plots of sudogen1 variations.
'Rec Lim' refers to the number of recursions for `generateRow` is allowed before giving up and throwing away the entire row.
'Control' refers to `sudogen.py` where the recursion limit = 9.

Sudogen_Box and Sudogen_Scatter are image-scaled graphs for website use.