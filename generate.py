import sys, copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            valid_words = set()
            for word in self.domains[variable]:
                if len(word) == variable.length:
                    valid_words.add(word)
            self.domains[variable] = valid_words
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        new_domain = set()
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            for word in self.domains[x]:
                if word[overlap[0]] in [wordy[overlap[1]] for wordy in self.domains[y]]:
                    new_domain.add(word)
                else:
                    revised = True
            self.domains[x] = new_domain
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = [(v1, v2) for v1 in self.crossword.variables for v2 in self.crossword.variables if v1 != v2]
        while arcs:
            x, y = arcs.pop(0) # dequeue
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                arcs.extend(set([(v, x) for v in self.crossword.neighbors(x)]) - {(y, x)})
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        complete = True
        vars_in_assignment = set(var for var in assignment)
        # Checking if all vars in the crossword has been assigned
        if vars_in_assignment != self.crossword.variables:
            complete = False
        for var in assignment:
            # making sure no var is empty
            assert isinstance(assignment[var], str)
            if not assignment[var]:
                complete = False
        return complete

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = [] # Must in be a list.
        consistent = True
        for var in assignment:
            assert isinstance(assignment[var], str)
            if assignment[var] in values:
                consistent = False
                break
            else:
                values.append(assignment[var])

            if var.length != len(assignment[var]):
                consistent = False
                break 
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                        consistent = False
                        break
        return consistent

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values_penalty = {value: 0 for value in self.domains[var]}
        for neighbor in self.crossword.neighbors(var):
            if neighbor not in assignment:
                overlap = self.crossword.overlaps[var, neighbor]
                for value in self.domains[var]:
                    for value2 in self.domains[neighbor]:
                        if value[overlap[0]] != value2[overlap[1]]:
                            values_penalty[value] += 1

        return sorted([value in self.domains[var]], key= lambda item: values_penalty[item])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        var_penalty = {}
        for var in self.crossword.variables:
            if var not in assignment:
                var_penalty[var] = len(self.domains[var])
        vars = sorted(var_penalty, key= lambda v: var_penalty[v])
        # if the two first variables have the same domain size
        if len(vars) > 1 and var_penalty[vars[0]] == var_penalty[vars[1]]:
            # Check number of neighbors and return highest degree
            if len(self.crossword.neighbors(vars[0])) < len(self.crossword.neighbors(vars[1])):
                return vars[1]
        return vars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment): return assignment # base case

        var = self.select_unassigned_variable(assignment)

        for value in self.domains[var]:
            new_assignment = copy.deepcopy(assignment)
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result != None: return result
        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
