# Project: Mysum Extended Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Redefine the mysum() function from exercise 1, such that it can take any number of arguments.
- Arguments must all be of the same type and respond appropriately to the + operator.
  - 'Appropriately': the function should work with numbers, strings, lists and tuples, but not sets and dicts.
- The result should be a new, longer sequence of the type provided by the parameters.
  - Examples:
    - mysum('abc', 'def') -> 'abcdef'
    - mysum([1, 2, 3],[4, 5, 6]) -> [1,2,3,4,5,6]
    - mysum(1, 2, 3) -> 6
- Use Pythonic conventions.

## Exercise notes
- This exercise aims to think about sequences and types and how to easily return values of different types from a function.
- Consider use of the splat (*) operator in the function definition.
