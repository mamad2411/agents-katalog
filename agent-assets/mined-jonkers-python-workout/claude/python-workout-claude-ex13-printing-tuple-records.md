# Project: Word With Most Repeated Letters Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - format_sort_records - that takes a list of tuples and returns a formatted string that has each record appearing on its own line.
- Specifically, each tuple represents a record for a country, as in the following example:
```
COUNTRIES = [('Canada', 9984670, 38250000),
('Italy', 301340, 59110000),
('United Kingdom', 242495, 67220000),
('France', 551695, 67390000),
('Germany', 357022, 83200000),
('Japan', 377975, 125700000),
('United States', 9833517, 331900000)
]
```
- The output should be a formatted string with three nicely aligned columns:
```
Canada		9,984,670	38,250,000
France 		551,695   	67,390,000
Germany 	357,022		83,200,000
Italy 		301,340		59,110,000
Japan 		377,975		125,700,000
United Kingdom 	242,495		67,220,000
United States 	9,833,517	331,900,000
```
- Countries should be presented in alphabetical order by country name.
- Use Pythonic conventions.

## Exercise notes
- There are several parts to consider in this exercise.
- Think about the use of sorted() to sort the tuples.
- Potentially use a similar approach to the list of dicts in a prior exercise. Here the 'dict' is a list of tuples. Consider iterate over using the items() method.
- Consider if f-strings or str.format would be a better approach for formatting the strings (remember, you can use the splat operator * to pass multiple items to a function).
- Consider adding format codes to add comms between every three digits in numbers.