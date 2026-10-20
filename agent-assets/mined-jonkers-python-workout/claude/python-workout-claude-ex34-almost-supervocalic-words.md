# Exercise 34: Almost Supervocalic Words

## Requirements

- Create a function `get_sv` that returns a set of all supervocalic words in a dict.
- A supervocalic word contains each of the letters a, e, i, o and u, each appearing once and in alphabetical order.
- For this exercise, we'll accept any word with all five letters, any number of times in any order. Find all words that match these criteria and return a set containing them.
- The function should take a single argument: the name of a text file containing one word per line, like a UNIX words file.
- Use Pythonic conventions.

## Exercise Notes

- Could use `in' here, but using it five times isn't ideal.
- Consider using the < operator: in the case of sets, it returns True if the item on the left is a subset of the item on the right.
- You might need to handle mixtures of case in a coherent way.
- Remember: use curly braces for a set comprehension.

