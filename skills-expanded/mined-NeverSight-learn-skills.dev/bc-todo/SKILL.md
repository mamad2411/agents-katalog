---
name: bc-todo
description: Manage a structured TODO.md tracking file in the project root. This skill should be used when the user asks to "add a todo file", "create TODO.md", "set up task tracking", "initialize a TODO list", "add a todo item", "add a bug/feature/chore", "add to my todo list", or runs the /todo command.
argument-hint: "[item description]"
---

# Manage TODO.md

Create or update a `TODO.md` file in the current working directory for tracking work.

## Determine Intent

- **No arguments provided**: Generate the TODO.md file (see "Generate TODO.md").
- **Arguments provided**: Add an item to the existing TODO.md (see "Add Item").

## Generate TODO.md

1. Check if `TODO.md` already exists in the current working directory.
2. If it exists, ask the user: "A TODO.md already exists. Would you like to overwrite it, or leave it as-is?"
   - If the user chooses to leave it, stop and confirm no changes were made.
   - If the user chooses to overwrite, proceed to step 3.
3. Write the following template to `TODO.md`:

```markdown
# TODO

## Bugs

## Features

## Chores
```

4. Confirm the file was created.

## Add Item

1. Read the existing `TODO.md`. If it does not exist, run "Generate TODO.md" first, then continue.
2. Determine the category from context:
   - **Bugs**: The item describes a defect, broken behavior, or something that needs fixing.
   - **Features**: The item describes new functionality or an enhancement.
   - **Chores**: The item describes maintenance, refactoring, cleanup, or operational work.
   - If the category is ambiguous, ask the user which category to use.
3. Append a new checkbox line (`- [ ] <description>`) under the appropriate `##` section heading.
4. Confirm what was added and under which category.
