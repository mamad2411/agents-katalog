# Persona Manager

**Manage agent personas (create, list, read, update)**

## Features
- List all available personas (`memory/personas/`)
- Create new personas from a template (`template.md`)
- Read existing persona files (markdown/json)
- Delete personas

## Usage

```bash
# List all personas
node skills/persona-manager/index.js list

# Create a new persona
node skills/persona-manager/index.js create my_persona

# Read a persona file
node skills/persona-manager/index.js read my_persona

# Delete a persona
node skills/persona-manager/index.js delete my_persona
```

## Persona Format
Markdown files in `memory/personas/` are parsed and used by `skills/persona-engine` (in future).
The structure should follow the template.

## Dependencies
- `node:fs`
- `node:path`
- No external npm packages required.
