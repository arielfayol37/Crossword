#!/usr/bin/env python3
"""
Example usage of the Crossword Puzzle Generator

This script demonstrates how to use the crossword generator with the provided
structure and word files.
"""

import sys
import os
from crossword import Crossword
from generate import CrosswordCreator

def test_crossword(structure_file, words_file, example_num):
    """Test a specific crossword structure and word list."""
    print(f"\nExample {example_num}: {os.path.basename(structure_file).split('.')[0].upper()} Crossword")
    print("-" * 50)
    
    if not os.path.exists(structure_file) or not os.path.exists(words_file):
        print(f"Error: Missing data files. Please ensure {structure_file} and {words_file} exist.")
        return False
    
    try:
        # Create crossword puzzle
        crossword = Crossword(structure_file, words_file)
        creator = CrosswordCreator(crossword)
        
        print(f"Structure loaded from: {structure_file}")
        print(f"Words loaded from: {words_file}")
        print(f"Crossword size: {crossword.width}x{crossword.height}")
        print(f"Number of variables: {len(crossword.variables)}")
        
        # Solve the crossword
        print("\nSolving crossword puzzle...")
        assignment = creator.solve()
        
        if assignment is None:
            print("No solution found!")
            return False
        else:
            print("Solution found!")
            print("\nCrossword Solution:")
            creator.print(assignment)
            
            # Save to image if possible
            try:
                output_file = f"crossword_example{example_num}.png"
                creator.save(assignment, output_file)
                print(f"\nCrossword saved to: {output_file}")
            except Exception as e:
                print(f"Could not save image: {e}")
                print("(This is normal if the font file is missing)")
            return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run example crossword generations."""
    
    print("Crossword Puzzle Generator - Extended Examples")
    print("=" * 60)
    
    # Test all four crossword structures
    test_cases = [
        ("data/structures/0.txt", "data/words/words0.txt", 1),
        ("data/structures/1.txt", "data/words/words1.txt", 2),
        ("data/structures/2.txt", "data/words/words2.txt", 3),
        ("data/structures/3.txt", "data/words/words3.txt", 4),
        ("data/structures/4.txt", "data/words/words4.txt", 5),
    ]
    
    successful_tests = 0
    total_tests = len(test_cases)
    
    for structure_file, words_file, example_num in test_cases:
        if test_crossword(structure_file, words_file, example_num):
            successful_tests += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {successful_tests}/{total_tests} crosswords solved successfully!")
    
    if successful_tests == total_tests:
        print("🎉 All crosswords solved! The CSP algorithms are working perfectly.")
    elif successful_tests > 0:
        print("✅ Some crosswords solved. The system is working but some puzzles may be too complex.")
    else:
        print("❌ No crosswords solved. There may be an issue with the word lists or structures.")

if __name__ == "__main__":
    main()
