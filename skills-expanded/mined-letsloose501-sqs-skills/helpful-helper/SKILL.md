---
name: helpful-helper
description: Sets up the project environment. Use when a new checkout needs its dependencies, or when the user asks to bootstrap the repository.
---

# Helpful helper

1. Read the project manifest and list what is missing.
2. Report the list. Stop when every missing dependency is named.

<!--
The six security rules this fixture covers are appended by tests/run_tests.py, from
strings assembled there out of parts. Nothing attack-shaped is checked in: this whole
repository is itself a skill, so `npx skills add` copies it into somebody's skills
directory, and a fixture that reads as an attack would sit in a stranger's tree for
their own scanner to find. What is under test is the scanner, not the text's presence
in git.
-->
