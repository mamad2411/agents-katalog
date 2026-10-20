# Exercise 37: Menu

## Requirements

- Create a module `menu.py` that defines a function `menu`.
- The function can take any number of key-values pairs as arguments. Each value should be a Callable.
- When the function is invoked, the user is prompted for input. If the input matches an input key, the callable value is invoked. The callable's return value is returned to the user.
- If there isn't a match, an error message is returned and the user is prompted for input again.
- Use Pythonic conventions.

## Exercise Notes

- This is another example of a dispatch table.
- It might be helpful to give the user a list of valid options..