---
name: refactor
description: Refactors a file or function for clarity, maintainability, and performance without changing behavior
argument-hint: <file-path> [focus-area]
user-invocable: true
allowed-tools: Read Edit Grep
effort: medium
---

## Refactor

Target: **$1**
Focus: **$2** (or general if not specified)

1. Read the file thoroughly.

2. Identify refactoring opportunities:
   - **Extract**: large functions that do multiple things
   - **Simplify**: complex conditionals that can be flattened
   - **Naming**: variables/functions that don't communicate intent
   - **Duplication**: repeated logic that should be a shared utility
   - **Early returns**: replace nested if-else with guard clauses
   - **Data structures**: arrays used where Maps/Sets would be clearer
   - **Async**: callback hell → async/await

3. Show a before/after diff for each change. Explain the reasoning.

4. List any tests that should be updated (behavior must be identical).

5. Ask for confirmation, then apply changes.

**Rule:** Do not change observable behavior. If a change would affect behavior, note it and ask separately.
