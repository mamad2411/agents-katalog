# Project: First Last Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a Python function (firstlast) that takes a sequence (string, list or tuple) and returns the first and last elements of that sequence in a two-element sequence of the same type.
- Examples:
  - firstlast('abc') -> 'ac'
  - firstlast([1,2,3,4]) -> [1,4]
- Use Pythonic conventions.

## Exercise notes
- You can retrieve the first element of a sequence with x[0] and the last element with x[-1].
- Slices allow retieval of a subset: x[2:5] returns a subset beginning at index 2 up to (but not including) index 5.
- When you use a slice, you're guaranteed to get the same type back as the input type.
- Use of the + operator on the first and last elements may give unexpected results! Remember, the output type must be the same as the input type.
