# Project: Ubbi Dubbi Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a Python function (ubbi_dubbi) that converts an assumed English word into Ubbi Dubbi.
- In Ubbi Dubbi, every English vowel (a, e, i, o and u) is prefaced with the string 'ub'.
- Examples:
  - 'milk' becomes 'mubilk'
  - 'program' becomes 'prubogrubam'
  - 'octopus' becomes 'uboctubopubus'
  - 'elephant' becomes 'ubelubephubant'.
- When you have two vowels together, preface each individual vowel.
  - 'soap' becomes 'suboubap'.
- Use Pythonic conventions.

## Exercise notes
- Assume the input word includes no capital letters or punctuation.
- Python sees a string as a sequence. Consider using the built-in in() function to assist with finding vowels.
- Need to operate on a letter-by-letter basis. Take care to avoid infinite loops (i.e., recursion due to trying to add 'ub' in front of a 'u' of a previously added 'ub'.