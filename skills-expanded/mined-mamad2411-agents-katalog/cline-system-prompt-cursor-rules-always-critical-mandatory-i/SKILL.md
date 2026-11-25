---
description:
globs:
alwaysApply: true
---
# _Critical

## Mandatory Instructions

- You absolutely must apply known best practices before new file creation or changes proposal.
- You absolutely must keep changes in existing files minimal and change ONLY what
  is required for the task you are working on

### Final verification

- Before returning result to the user **ALWAYS** run `~/.config/git/hooks/pre-commit`
  then fix ALL errors from the log. Rerun this steps until you fix all errors

### Terminal

- prepend shell commands with `timeout X`, where X is reasonable amount in seconds for the command to run
  in range from 15 to 300. In case of error as the first step check if it was expected to get any input from user

### Markdown

- You MUST follow all markdownlint rules you know when creating or modifying
  Markdown files. This is mandatory requirement.
- Remind yourself MD007, MD022, MD026, MD030, MD032

### Implementation

- Ensure code follows established patterns in the project
- Verify all needed imports are included
- Check that the proposed changes meet the project's coding standards
- Follow security best practices
- Consider performance implications of changes
