# Project: Pig Latin Sentence Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a Python function (pl_sentence) that converts an assumed English sentence into a Pig Latin sentence.
- In Pig Latin, if the word begins with an English vowel (a, e, i, o, u), add 'way' to the end of the word (e.g., 'eat' becomes 'eatway'). In all other cases, take the first letter, put it at the end of the word and add 'ay' (e.g., 'ball' becomes 'allbay').
- Example: 'this is a test translation' becomes 'histay isway away esttay ranslationtay.
- Use Pythonic conventions.

## Exercise notes
- Assume the input sentence includes no capital letters or punctuation.
- The translation of single words into pig latin was covered in exercise 5.
- Consider how the sentence can be split into tokens using str.split().
- Consider using list.append and str.join to turn a list of translated tokens back into a string.