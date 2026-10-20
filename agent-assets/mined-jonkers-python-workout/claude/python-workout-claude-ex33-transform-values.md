# Exercise 33: Transform values exercise

## Requirements

- Create a function `transform_values()` that applies a function to each of the values of a dict. The result is a new dict whose keys are the same as the input, but whose values have been transformed by the function.
- The function passed to transform_values() should take a single argument, the dict's value.
- Invokation: transform_values(lambda x: x*x, d)
  - This transformation squares the values in the provided dict.
- Use Pythonic conventions.

## Exercise Notes

- Iterate over a dict's key-value pairs with dict.items.
- Consider using a dict comprehension.

