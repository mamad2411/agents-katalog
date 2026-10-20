# Exercise 47: Circle

## Requirements

- Define a class `Circle` that takes two arguments when defined: a sequence and a number.
- The object will then return elements the defined number of times. If the number is greater than the number of elements, the sequence repeats as necessary.
- You should define the class such that it uses a helper, `CircleIterator`.
- Example:
  - c = Circle('abc', 5)
  - print(list(c)) # Prints a, b, c, d, e
- Use Pythonic conventions.

## Exercise Notes

- Consider using modulo operator to support circular buffering.