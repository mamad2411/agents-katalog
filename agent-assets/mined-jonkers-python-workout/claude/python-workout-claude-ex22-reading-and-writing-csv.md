# Project: Longest Word Per File Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - passwd_to_csv() - that takes two filenames as arguments.
  - The first argument is an input file in passwd-style format (colon-delimited).
  - The second argument is an output file in tab-separated format.
- The output file should contain the username and user ID from the input (input indexes 0 and 2).
- Input files may contain comments: lines beginning with '#'.
- Assume any input with two colon-separated fields is legitimate.
- Use Pythonic conventions.

## Exercise notes
- Use the csv module to handle input and output.
- Work out how to open input and output files using the same with statement.
