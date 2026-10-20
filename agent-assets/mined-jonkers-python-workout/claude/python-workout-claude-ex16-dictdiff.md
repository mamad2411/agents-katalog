# Project: Dictdiff Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - dictdiff() - that takes two dicts as arguments. The function returns a new dict that expresses the difference between the two dicts.
  - If there are no differences, the function returns an empty dict.
  - For each key-value pair that differs, the return value will have a key-value pair in which the value is a list containing the values from the two different dicts. If one of the dicts doesn't contain that key, it should contain None.
- Examples:
```
d1 = {'a':1, 'b':2, 'c':3}
d2 = {'a':1, 'b':2, 'c':4}
print(dictdiff(d1, d1)) # Empty dict - compares with itself
print(dictdiff(d1, d2)) # prints {'c': [3,4]}
d3 = {'a':1, 'b':2, 'd':3}
d4 = {'a':1, 'b':2, 'c':4}
print(dictdiff(d3, d4)) # prints {'c': [None, 4], 'd': [3, None]}
d5 = {'a':1, 'b':2, 'd':4}
print(dictdiff(d1, d5)) # prints {'c': [3, None], 'd': [None, 4]}
```
- Use Pythonic conventions.

## Exercise notes
- Consider use of dict.get to make shorter, more elegant, more maintainable code.
- Consider getting all of the keys from the two dicts and adding them to a set, then iterating over them. Using dict.keys would be useful here.
