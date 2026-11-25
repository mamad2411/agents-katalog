---
name: create-similar
description: Create a new skill or project file based on an existing example's structure
argument-hint: "[scope]"
related:
  - update-devin-global-skills
  - deep-review-codebase
  - use-related-skills
  - transform
  - deep-validate
  - search
---

## Goal

Create something new with a structure similar to an existing example, adjusting names and context as appropriate.

## Scope

Use when creating a new skill, file, component, or project structure based on an existing example, e.g. creating `edit-<repo>` from an existing `edit-*` example.

## Execute

### 1. Identify Example

> Goal: Identify the example to copy

1. If the user gives a path or skill name → read it immediately
2. If not specified → find the file or directory closest to the target with `/search-files-patterns`
3. Confirm the example is the correct canonical source

### 2. Analyze Structure

> Goal: Understand the structure and what must change

1. Read all files in the example
2. Separate the components: frontmatter, sections, commands, references, names
3. Identify the identifiers tied to the example (directory name, skill name, URLs, paths)
4. Record the list of items to replace

### 3. Define Target

> Goal: Define what will be created

1. Get the target name from the user
2. Validate the name (kebab-case, not duplicated, no special characters)
3. Get the context or scope that differs from the example
4. If unclear → run `/ask-me`

### 4. Create Copy

> Goal: Create the new file/directory

1. Create the target directory if needed
2. Copy the files from the example to the target
3. If there are multiple files → copy all of them
4. Never overwrite existing files

### 5. Replace Identifiers

> Goal: Adapt the example to match the target

1. Replace the example names with the target name in every file
2. Replace directory references
3. Replace URLs, paths, and project-specific names
4. If it is a skill → update `name` in the frontmatter
5. If there is a `description` → adjust it to match

### 6. Adapt Content

> Goal: Tailor the content to the target

1. Adjust `## Goal` and `## Scope` to fit the context
2. Adjust commands, examples, and paths
3. Remove example-specific details that are not relevant
4. If there is `related` → update it correctly

### 7. Validate

> Goal: Check correctness

1. Verify `name` matches the directory name
2. Verify there are no broken references
3. Run `/deep-validate` for the skill
4. If it fails → run `/resolve-errors` and retry (max 3)

## Rules

- Never overwrite existing files; if one already exists, stop or ask the user
- Change every identifier — none may be missed
- Do not copy secrets, API keys, or credentials
- For a skill, `name` must match the directory name
- Do not guess context; if unclear → use `/ask-me`
- If creating a new skill → update `AGENTS.md`

- Use /update-devin-global-skills if needed (similar)
- Use /deep-review-codebase if needed
- Use /use-related-skills if needed
- Use /use-scripts if needed

## Expected Outcome

- New file/directory created that mirrors the example but is adapted to the target
- No broken references
- `name` matches the directory name
- Passes validation
