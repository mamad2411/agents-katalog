# Project: Rainfall Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - get_rainfall() - that tracks rainfall in a number of cities.
- Users of the program will enter the name of a city.
  - If the city name is blank, the function prints a report and exits.
  - If the city name isn't blank, the user is prompted again for how much rain has fallen in the city. After entering a value, The user is then prompted for the name of a city again.
- Example interaction:
```
Boston
5
New York
7
Boston
5
[Enter; blank line]
```
- With these inputs, the program should output:
```
Boston: 10
New York: 7
```
- The order in which the city names are presented in the report is unimportant. The cities are not known to the program in advance.
- Use Pythonic conventions.

## Exercise notes
- This exercise uses dicts as tiny key-value databases.
- Consider how to handle an invalid rainfall value as input.
