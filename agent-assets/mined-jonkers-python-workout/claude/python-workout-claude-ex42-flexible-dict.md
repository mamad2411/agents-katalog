# Exercise 42: Flexible Dict

## Requirements

- Create a subclass of dict - `FlexibleDict` - that allows strings to be used to access integer keys, and vice versa.
- Example:
```
fd = FlexibleDict()

fd[1] = 100
print(fd[1]) # Prints 100
print(fd['1']) # Also prints 100
fd['2'] = 200
print(fd['2']) # Prints 200
print(fd[2]) # Also prints 200
```
- If FlexibleDict doesn't find a user's key, it will convert to both str and int before giving up.
- Use Pythonic conventions.

## Exercise Notes

- You should only need to inherit from `dict` and write one method.
- You'll probably need to make a call on the superclass to complete the read.