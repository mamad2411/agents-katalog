---
name: code-refactorer
description: Refactor a user-scoped area of code for clarity, concision, and modularity while preserving behavior.
---

# Skill: Code Refactorer

## Skill Instructions

Given a narrow area or scope of code and some initial goals or instruction, your
job is to refactor code to prioritize:

* Human readability
* Verbosity reduction; prefer concise statements, avoid excessive comments
* Reduce code into modular, reusable components
* Avoid excessively long functions in favor of breaking them into smaller
  functions with a singular responsibility
* Re-organize lengthy spaghetti code into multiple, importable files with an
  organized purpose.

## Input

* Make sure the user provides an area or scope of code.
* Don't scan for code, require some input and direction on which aspect or even
  sub-directory of the project to work on.

## Output

* Ensure tests pass
* refactors shouldn't change the output; the goal is to have more organized
  underlying code.
* Engage the Plan Generator skill to create a plan document outlining the
  changes made. For a refactor the aim is to be brief and more task list
  oriented.
  * Assume a single plan document and add or amend to it per Code Refactorer
    session. Do not create multiple plan documents unless instructed, add
    changes to the task list.
