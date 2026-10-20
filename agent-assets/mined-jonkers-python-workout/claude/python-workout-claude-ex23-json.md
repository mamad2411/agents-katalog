# Project: JSON Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- In this exercise, there will be a scores/ directory on the filesystem representing files in JSON format.
- Each file represents test scores for one class at a school.
- Write a function - print_scores() - that takes a directory name as an argument and prints a summary of the student scores it finds.
- Example: scores for class 9a would be in a file called 9a.json that contains data like the following:
```
[{"maths" : 90, "literature" : 98, "science" : 97},
{"maths" : 65, "literature" : 79, "science" : 85},
{"maths" : 78, "literature" : 83, "science" : 75},
{"maths" : 92, "literature" : 78, "science" : 85},
{"maths" : 100, "literature" : 80, "science" : 90}
]
```
- Each file contains the JSON equivalent of Python dicts.
- The print_scores() function should print the highest, lowest and average test scores for each subject in each class.
- Output would look something like this:
```
scores/9a.json
	science: min 75, max 97, average 86.4
	literature: min 78, max 98, average 83.6
	math: min 65, max 100, average 85.0
scores/9b.json
	science: min 35, max 95, average 82.0
	literature: min 38, max 98, average 72.0
	math: min 38, max 100, average 77.0
```
- Use Pythonic conventions.

## Exercise notes
- Use the Python json module to turn JSON-encoding strings into Python objects, and vice versa.
- Valid JSON uses double quotes, rather than single quotes. This can result in unexpected syntax errors for Python users.
- Consider using the glob() module to find JSON files.
- This exercise brings together several concepts from previous exercises.
- Consider using a dict of dicts to collate data.

