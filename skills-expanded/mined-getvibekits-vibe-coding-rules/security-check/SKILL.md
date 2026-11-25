---
name: security-check
description: Check the project for beginner security mistakes before publishing.
argument-hint: [optional: area to focus on]
disable-model-invocation: true
---

Check this project for security problems a beginner might miss. Focus on $ARGUMENTS if I named something.

1. Secret keys, passwords or tokens written in the code or committed to git.
2. Database tables anyone can read or change.
3. Pages or API routes that should need a login but don't.
4. Forms that trust user input without checking it.

List what you find in priority order, with the file and line. Don't change any files yet.
