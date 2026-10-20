# Exercise 31: Pig Latin Translation of a File

## Requirements

- Write a function `plfile()` that takes a filename as an argument. The function returns a string with the file's contents, but with each word translated into Pig Latin, as per exercise 5.
- The returned translation can ignore newlines and isn't required to handle capitalisation or punctuation in any particular way.
- Use Pythonic conventions.

## Exercise Notes

- Consider using a nested list comprehension to iterate over each line of a file, then each word of a line.
- Consider using a generator expression (as per exercise 28) - it uses parentheses rather than square brackets. Generators can be used with str.join and produce more memory efficient code.


