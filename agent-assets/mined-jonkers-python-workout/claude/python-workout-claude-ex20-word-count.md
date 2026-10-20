# Project: Word Count Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - wordcount() - that mimics the wc Unix command. The function will take a filename as input and will print four lines of output:
  - Number of characters (including whitespace).
  - Number of words (separated by whitespace).
  - Number of lines.
  - Number of unique words (case sensitive, so "NO" is different to "no").
- Example:
  - For the following file input:
```
This is a test file.

It contains 28 words and 20 different words.

It also contains 165 characters.

It also contains 11 lines.

It is also self-referential.

Wow!
```
  - The output will be:
    - 165 characters.
    - 28 words.
    - 11 lines.
    - 20 unique words.
- Use Pythonic conventions.

## Exercise notes
- Consider using a dict to accumulate data in the file (e.g. line count).
- Sequencing of how this data is calculated should be carefully considered; you should only need to make one pass through the file for input.