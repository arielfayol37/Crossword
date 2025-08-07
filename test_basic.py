#!/usr/bin/env python3
"""
Basic test script for the Crossword Puzzle Generator

This script tests the core functionality to ensure everything works correctly.
"""

import sys
import os
from crossword import Crossword, Variable
from generate import CrosswordCreator

def test_variable_class():
    """Test the Variable class functionality."""
    print("Testing Variable class...")
    
    # Test variable creation
    var1 = Variable(0, 0, Variable.ACROSS, 3)
    var2 = Variable(0, 0, Variable.DOWN, 3)
    
    assert var1.i == 0
    assert var1.j == 0
    assert var1.direction == Variable.ACROSS
    assert var1.length == 3
    assert len(var1.cells) == 3
    
    # Test cell calculation
    expected_cells = [(0, 0), (0, 1), (0, 2)]
    assert var1.cells == expected_cells
    
    print("✓ Variable class tests passed")

def test_crossword_creation():
    """Test crossword creation from files."""
    print("Testing crossword creation...")
    
    structure_file = "data/structures/1.txt"
    words_file = "data/words/words1.txt"
    
    if not os.path.exists(structure_file) or not os.path.exists(words_file):
        print("⚠ Skipping crossword creation test (missing data files)")
        return
    
    crossword = Crossword(structure_file, words_file)
    
    assert crossword.width == 4
    assert crossword.height == 4
    assert len(crossword.variables) == 4
    assert len(crossword.words) > 0
    
    print("✓ Crossword creation tests passed")

def test_solver():
    """Test the crossword solver."""
    print("Testing crossword solver...")
    
    structure_file = "data/structures/1.txt"
    words_file = "data/words/words1.txt"
    
    if not os.path.exists(structure_file) or not os.path.exists(words_file):
        print("⚠ Skipping solver test (missing data files)")
        return
    
    crossword = Crossword(structure_file, words_file)
    creator = CrosswordCreator(crossword)
    
    # Test node consistency
    creator.enforce_node_consistency()
    for var in crossword.variables:
        for word in creator.domains[var]:
            assert len(word) == var.length
    
    # Test solving
    assignment = creator.solve()
    if assignment:
        print("✓ Solver found a solution")
        # Test that solution is valid
        assert creator.assignment_complete(assignment)
        assert creator.consistent(assignment)
        print("✓ Solution validation passed")
    else:
        print("⚠ Solver found no solution (this might be expected)")

def main():
    """Run all tests."""
    print("Crossword Puzzle Generator - Basic Tests")
    print("=" * 40)
    
    try:
        test_variable_class()
        test_crossword_creation()
        test_solver()
        
        print("\n" + "=" * 40)
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
