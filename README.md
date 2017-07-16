# Artificial Intelligence Nanodegree
## Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We identify all naked twins, or two boxes with identical values in the same unit of size 2. Those two characters can only occur in those two boxes. Meaning that all other boxes in that unit cannot contain those characters. So we iterate through the boxes, excluding the naked twins themselves, and eliminate the two characters.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: To create a Diagonal Sudoku we add two extra diagonal units to account for diagonal constraints.  This creates another constraint that the Sudoku must be solved with the numbers 1 through 9 appearing only once in each of the diagonals.# AIND-Sudoku
