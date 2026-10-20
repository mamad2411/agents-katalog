# Project: Hexadecimal Output Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - hex_output - that asks the user for a hex number and prints the decimal equivalent (e.g. if the user enters 50 (hex), the value 80 (decimal) will be printed to the screen).
- You cannot convert the number all at once using the int() function, but you can use int() one digit at a time.
- Use Pythonic conventions.

## Exercise notes
- Strings are sequences of characters in Python, which are iterable.
- The built-in enumerate() function can be used to determine the numeric index of a character in a string: this might be useful for putting into power and digit variables.
- The built-in reversed() might be useful as well, to allow building up from the last character in the sequence to the first.
- The built-in int() can take two arguments. The first is mandatory (the string to be converted into an integer). The second is optional and contains the number base.