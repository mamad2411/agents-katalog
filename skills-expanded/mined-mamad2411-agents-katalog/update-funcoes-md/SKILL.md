---
name: update-funcoes-md
description: Keeps the project funcoes.md file updated when functions are created, changed, or removed. Use after adding or modifying a function, or when the user asks to document functions or update funcoes.md.
---

# Update funcoes.md

The file `funcoes.md` at the project root must list and briefly explain every function created in the project. Update it whenever a function is added, changed, or removed.

## When to update

- **New function**: Add an entry with name, purpose, parameters, return value, and location (module/path).
- **Changed function**: Update the existing entry to match the new behavior/signature.
- **Removed function**: Remove or mark the entry as removed so the list stays accurate.

## What to record per function

- **Name** and **location** (file/module).
- **Purpose**: What it does in one or two sentences.
- **Parameters**: Names and roles (and types if relevant).
- **Return value**: Meaning and type if relevant.
- **Notes**: Side effects, exceptions, or important usage details (optional).

## Format

Use Markdown. Prefer a simple structure, e.g.:

```markdown
## module_or_area

### function_name
- **Arquivo**: path/to/file.py
- **Propósito**: ...
- **Parâmetros**: ...
- **Retorno**: ...
```

Or a compact table if the project already uses one. Keep terminology consistent with the codebase.

## Rules

- Prioritize reusing existing functions before adding new ones; document the reuse in the relevant entry if useful.
- Each function version that changes behavior should be reflected in `funcoes.md`.
- Consider null safety and documented exceptions where they matter for callers.

If `funcoes.md` does not exist, create it at the project root with a short intro and then add the entries.
