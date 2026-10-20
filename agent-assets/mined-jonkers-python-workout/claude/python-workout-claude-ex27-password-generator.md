# Project: Password Generator Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - create_password_generator() - that takes a string as an argument and returns a function that takes an integer argument.
- Calling the returned function will return a random password of the specified length using characters provided to the function's generator.
- Example:
```
alpha_password = create_password_generator('abcdef')
symbol_password = create_password_generator('!@#$%')

print(alpha_password(5)) # efeaa
print(symbol_password(5)) # %%$!#
```
- Use Pythonic conventions.

## Exercise notes
- Look at using the random.choice function.