---
name: inline-docs
description: Document code using efficient inline comments. Use whenever writing, editing, or reviewing code or if the user mentions documentation.
---

# Inline Documentation

Documentation serves to remedy ambiguity and provide otherwise missing context. A comment must earn its place and should not be added solely for ceremony. Keep docs lean to avoid token bloat.

## Style

- Avoid long, unnecessary prose. Write like a senior developer in terse fragments.
-  Only write about what is directly relevant and necessary to understand the code. 
- **Don’t** include historical references or specifics to the current session’s context. Assume that the docs will live long past the current situation.
- Avoid over-explaining obvious code. Do not include a reason for code if it is highly situational/references past conversations.
- Inline docs (`//` comments) should consist of short phrases and only explain highly-complicated logic. 
- Doc comments (JavaDoc, JSDoc, docstrings) must be placed on every required declaration according to the language specification. These help to provide a standard way for devs to read docs. Use special tags (@ tags) as necessary to make docs more organized and concise.
- Avoid verbose, generic, or non-human names when creating files, variables, or classes.
- Don’t use filler words (keeps, so, because, stays). Full sentences are not necessary, use semicolons or commas.

## Formatting

- **Don’t** use ceremonial section headers (`// --------Variables--------`) since they cause visual/token bloat and add no new additional information
- Only use typeable/ASCII characters. **Don’t** use emojis, em/en dashes, arrow symbols, since they make docs hard to edit.