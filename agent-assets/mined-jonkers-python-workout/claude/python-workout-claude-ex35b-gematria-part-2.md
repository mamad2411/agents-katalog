# Exercise 35b: Gematria, part 2

## Requirements

- Create two functions:
  - `gematria_for`, that takes a single word (string) as an argument and returns the Gematria score for that word. Example: 'cat' -> (3 + 1 + 20) = 24
  - `gematria_equal_words`, that takes a single word and returns a list of those dict words whose Gematria score matches the current word's score. The source for the dict words is the UNIX dictionary file.
- Use the function created in exercise 35a (duplicate into this project if that's easiest).
- It might be useful to create a local copy of the UNIX dictionary file used to simplify file handling.
- Use Pythonic conventions.

## Exercise Notes

- Use of generators might be helpful to avoid unnecessary memory consumption.
- For correct operation, you probably need to convert words in the UNIX dictionary file to lowercase.