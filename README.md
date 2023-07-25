# Generating Crossword Puzzles

This project aims to generate a crossword puzzle given a crossword structure and a list of words to use. The problem is modeled as a constraint satisfaction problem, where each sequence of squares represents a variable, and we need to find an appropriate word from the domain of possible words to fill in each variable. The solution uses a combination of node consistency, arc consistency, and backtracking search to find a satisfying assignment that meets all the constraints.

## Crossword Puzzle Structure

The crossword puzzle is represented using the `Variable` and `Crossword` classes defined in `crossword.py`. A `Variable` object represents a sequence of squares that needs to be filled with a word and is defined by its row, column, direction, and length. The `Crossword` class holds information about the puzzle, such as its structure (a 2D list representing blank cells), the vocabulary of words, and the set of variables in the puzzle along with their overlaps.

## Implemented Functions

The following functions have been implemented in `generate.py` to generate crossword puzzles:

### `enforce_node_consistency(self)`

This function updates the `self.domains` dictionary such that each variable becomes node consistent, ensuring that each value in its domain satisfies the variable's unary constraints (i.e., has the correct length).

### `revise(self, x, y)`

This function makes variable `x` arc consistent with variable `y`. `x` is arc consistent with `y` when every value in the domain of `x` has a corresponding possible value in the domain of `y` that does not cause a conflict.

### `ac3(self, arcs=None)`

This function enforces arc consistency on the problem using the AC3 algorithm. Arc consistency is achieved when all values in each variable's domain satisfy that variable's binary constraints. The function returns False if all the remaining values from any domain were removed, else it returns True.

### `assignment_complete(self, assignment)`

This function checks if a given assignment is complete, meaning every crossword variable is assigned to a value. The function returns True if the assignment is complete and False otherwise.

### `consistent(self, assignment)`

This function checks if a given assignment is consistent, satisfying all constraints of the problem: distinct values, correct length, and no conflicts between neighboring variables. The function returns True if the assignment is consistent and False otherwise.

### `order_domain_values(self, var)`

This function returns a list of all values in the domain of the variable `var`, ordered according to the least-constraining values heuristic. The heuristic is computed based on the number of values ruled out for neighboring unassigned variables.

### `select_unassigned_variable(self, assignment)`

This function returns a single unassigned variable in the crossword puzzle according to the minimum remaining value heuristic and then the degree heuristic. The variable with the fewest number of remaining values in its domain is selected, and in case of a tie, the variable with the largest degree (most neighbors) is chosen.

### `backtrack(self, assignment)`

This function performs backtracking search to find a complete satisfactory assignment of variables to values. If a satisfying assignment is possible, the function returns the complete assignment as a dictionary, where each variable is a key and the value is the word that the variable should take on. If no satisfying assignment is possible, the function returns None.

## Usage

To use the crossword puzzle generator, you need to have the structure of the crossword puzzle and a list of words as input. Create an instance of the `Crossword` class by providing the structure file and words file. Then, call the `solve()` method to find a satisfying assignment of words to the variables. If a solution is found, the `solution` attribute of the `Crossword` object will contain the final assignment.

```python
# Example usage
from crossword import Crossword

# Provide the structure_file and words_file paths
structure_file = 'path/to/structure_file.txt'
words_file = 'path/to/words_file.txt'

# Create a crossword puzzle
crossword = Crossword(structure_file, words_file)

# Solve the crossword puzzle
crossword.solve()

# Access the solution
if crossword.solution:
    print("Solved Crossword Puzzle:")
    crossword.print()
else:
    print("No solution found for the crossword puzzle.")

Note: Replace `'path/to/structure_file.txt'` and `'path/to/words_file.txt'` with the actual paths to the structure file and words file, respectively. The `solve()` method will use the implemented functions to find a satisfying assignment of words to the variables and update the `solution` attribute accordingly. If a solution is found, it will be printed using the `crossword.print()` method. Otherwise, it will indicate that no solution was found for the given crossword puzzle.
