# Exercise 46: MyEnumerate

## Requirements

- The built-in enumerate() function provides the index of an element in a sequence, as well as the element itself.
- Write a class `MyEnumerate` such that someone could use it instead of enumerate().
- It will need to return a tuple with each enumeration, with the first element in the tuple being the index (starting at 0), and the second element being the current element from the underlying data structure.
- Trying to use MyEnumerate with a noniterable argument will result in an error.
- Use Pythonic conventions.

## Exercise Notes

- Creating an iterable requires:
  - __iter__, which returns an iterator.
  - __next__, which must be defined on the iterator.
  - StopIteration exception, which the iterator raises to signal the end of iterations.
- Consider use of an object attribute to maintain state.
