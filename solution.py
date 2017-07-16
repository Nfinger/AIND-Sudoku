def cross(a, b):
    return [s+t for s in a for t in b]

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[r+c for r,c in zip(rows,cols)],[r+c for r,c in zip(rows,cols[::-1])]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# This is the addition for the Hemisphere sudoku where there are 4 smaller boxes added within the 9 other boxes
# # otherRows = 'BCDFGH'
# # otherCols = '234678'
# # otherBoxes = cross(otherRows, otherCols)
# # otherRow_units = [cross(r, otherCols) for r in otherRows]
# # otherColumn_units = [cross(otherRows, c) for c in otherCols]
# # otherSquare_units = [cross(rs, cs) for rs in ('BCD','FGH') for cs in ('234','678')]
# # otherUnitlist = otherRow_units + otherColumn_units + otherSquare_units
# # otherUnits = dict((s, [u for u in otherUnitlist if s in u]) for s in otherBoxes)
# # otherPeers = dict((s, set(sum(otherUnits[s],[]))-set([s])) for s in otherBoxes)

# for peer in otherPeers:
#     for rc in otherPeers[peer]:
#         if rc not in peers[peer]:
#             peers[peer].add(rc)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        possible_twins = [values[box] for box in unit]
        naked_twins = [value for value in possible_twins if possible_twins.count(value) == 2 and len(value) == 2]
        for twin in naked_twins:
            for value in twin:
                for box in unit:
                    if values[box] != twin:
                        values = assign_value(values,box,values[box].replace(value,''))
    
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    newGrid = []
    allNumbers = '123456789'
    for num in grid:
        if num == ".":
            newGrid.append(allNumbers)
        else:
            newGrid.append(num)
    return dict(zip(boxes, newGrid))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    pass

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = only_choice(values)
        values = eliminate(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
     # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    # hemisphere_sudoku_1 = '......7....94..2......3..1.28..9........163......5.46..4.6....3.......2....58....'
    # hemisphere_sudoku_2 = '........8.4.3...........5...9....4...2..5.......6.9.....9...2..4....738..5.......'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
