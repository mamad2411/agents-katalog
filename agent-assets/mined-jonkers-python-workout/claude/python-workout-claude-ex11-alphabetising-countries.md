# Project: Alphabetising Countries Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - alphabetise_countries - that sorts a list of dictionaries holding information about countries. The function should return the list of dictionaries but sorted alphabetically by country name.
- Example input:

```
COUNTRIES = [
{'name': 'Canada', 'size': 9984670, 'population': 38250000},
{'name': 'Italy', 'size': 301340, 'population': 59110000},
{'name': 'United Kingdom', 'size': 242495, 'population': 67220000},
{'name': 'France', 'size': 551695, 'population': 67390000},
{'name': 'Germany', 'size': 357022, 'population': 83200000},
{'name': 'Japan', 'size': 377975, 'population': 125700000},
{'name': 'United States', 'size': 9833517, 'population': 331900000}]
```

- Use Pythonic conventions.

## Exercise notes
- Expect to use the sorted() method observed in chapter 3, along with a function passed as an argument to its key parameter.
- One option for solving this exercise involves using operator.itemgetter.

