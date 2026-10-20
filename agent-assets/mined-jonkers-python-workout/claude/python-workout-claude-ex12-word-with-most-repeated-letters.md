# Project: Word With Most Repeated Letters Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - most_repeating_word() - that takes a sequence of words as input.
- The function should return the word that includes the greatest number of instances of any letter.
- That is, for each word identify the count of the most frequently appearing letter. Compare this value across all provided input words.
- Example:
  - Input: ['hello','there','elephant','lullaby']
  - Output: 'lullaby'. The word contains 3 l characters, where l is the most frequent letter. It's frequency - 3 - is the highest of any letter across the input words.
- Example:
  - Input: ['this','is','an','elementary','test','example']
  - Output: 'elementary', due to the 3 e characters.
- If there's a tie, any of the appropriate words can be returned.
- Use Pythonic conventions.

## Exercise notes
- Suggest using collections.Counter. Pay particular attention to the most_common method for this exercise.


