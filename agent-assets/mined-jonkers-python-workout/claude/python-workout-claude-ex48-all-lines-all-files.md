# Exercise 48: All Lines All Files

## Requirements

- Write a generator function `all_lines` that takes a directory name as an argument.
- With each iteration, the function should return a single string, representing a single line from one file in the directory.
- If there are five files of ten lines each, the function will return a total of 50 strings.
- If you encounter a file that can't be opened (e.g., it's a directory, you don't have permission, etc.), the file should be ignored.
- Use Pythonic conventions.

## Exercise Notes

- The proper Python solution would be to use os.walk, but that's not intended for this exercise.
- Consider using the glob module to help with path/filename handling.
- Consider trapping an OSError exception if you can't read from the file.
