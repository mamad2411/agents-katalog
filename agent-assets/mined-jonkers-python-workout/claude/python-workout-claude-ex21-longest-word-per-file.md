# Project: Longest Word Per File Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write two functions:
  - find_longest_word(): takes a filename as an argument and returns the longest word found in the file.
  - final_all_longest_words(): takes a dictionary name and returns a dict in which the keys are filenames and the values are the longest words from each file.
- Use Pythonic conventions.

## Design decisions
- find_longest_word() returns `list[str]` rather than `str`, so that ties (multiple words sharing the max length) are represented explicitly. This deviates from the original exercise but is a more Pythonic API.
- find_all_longest_words() values are correspondingly `list[str]`.
- Duplicate longest words are deduplicated (e.g. "cat" appearing on multiple lines is returned once).
- No guaranteed ordering of tied words in the returned list.

## Exercise notes
- Dict comprehensions probably offer the most Pythonic approach.
  - Iterate over the list of files in the named directory.
  - For each file, run find_longest_word().
  - Each filename-longest word combination will be a key-value pair in the final dictionary.