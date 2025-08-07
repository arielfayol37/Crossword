# Crossword Puzzle Generator

This project generates crossword puzzles automatically using constraint satisfaction problem (CSP) algorithms. Given a crossword structure and a list of words, it finds a valid solution that satisfies all constraints using node consistency, arc consistency, and backtracking search.

## Features

- **Automatic Crossword Generation**: Creates complete crossword puzzles from structure files and word lists
- **CSP Algorithms**: Implements advanced constraint satisfaction techniques
- **Multiple Output Formats**: Text output and image generation (PNG)
- **Flexible Input**: Customizable crossword structures and word lists
- **Example Data**: Includes sample structures and word lists to get started

## Project Structure

```
Crossword/
├── crossword.py          # Core data structures (Variable, Crossword classes)
├── generate.py           # CSP solving algorithms and main logic
├── example.py            # Example usage script
├── requirements.txt      # Python dependencies
├── data/
│   ├── structures/       # Crossword layout files (.txt)
│   └── words/           # Word list files (.txt)
└── assets/
    └── fonts/           # Font files for image generation
```

## Quick Start

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Examples

The easiest way to get started is to run the example script:

```bash
python example.py
```

This will generate two example crosswords using the provided data files.

### Command Line Usage

You can also use the generator directly from the command line:

```bash
# Basic usage
python generate.py data/structures/0.txt data/words/words0.txt

# Save to image file
python generate.py data/structures/0.txt data/words/words0.txt output.png
```

### Programmatic Usage

```python
from crossword import Crossword
from generate import CrosswordCreator

# Create crossword puzzle
crossword = Crossword('data/structures/0.txt', 'data/words/words0.txt')
creator = CrosswordCreator(crossword)

# Solve the puzzle
assignment = creator.solve()

if assignment:
    print("Solution found!")
    creator.print(assignment)
    # Save to image
    creator.save(assignment, 'my_crossword.png')
else:
    print("No solution found!")
```

## Input File Formats

### Structure Files (.txt)
Structure files define the crossword layout using underscores (`_`) for blank cells and spaces for blocked cells:

```
_____
_   _
_   _
_   _
_____
```

### Word Lists (.txt)
Word lists contain one word per line (all uppercase):

```
CAT
DOG
BAT
RAT
HAT
```

## Image Generation

To generate PNG images of your crosswords, you'll need to:

1. Download the Open Sans font from [Google Fonts](https://fonts.google.com/specimen/Open+Sans)
2. Place `OpenSans-Regular.ttf` in the `assets/fonts/` directory

If you don't have the font, the program will still work for text output but will skip image generation.

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
