---
name: epost-letters
version: 1.0.0
description: "e-post: Manage email letters (templates)."
metadata:
  category: "email-marketing"
  requires:
    bins: ["epost"]
  cliHelp: "epost letters --help"
---

# epost letters

Manage email letters (templates) in the e-post email marketing platform.

> **PREREQUISITE:** A valid access token must be set before use.
> Run `epost set-token <your_token>` once to save your token.

```bash
epost letters <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List all letters |
| `get <id>` | Get a letter by ID |
| `add <subject>` | Create a new letter |
| `update <id>` | Update an existing letter |
| `delete <id>` | Delete a letter by ID |

## Usage Examples

```bash
# List all letters
epost letters list

# List with pagination
epost letters list --limit 10 --offset 0

# List as JSON
epost letters list --json

# Get a letter by ID
epost letters get 5
epost letters get 5 --json

# Add a new letter
epost letters add "Monthly Newsletter" --content "<h1>Hello!</h1>"

# Update a letter
epost letters update 5 --subject "Updated Subject" --content "<p>New content</p>"

# Delete a letter
epost letters delete 5
```

## Flags

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--content <html>` | `-c` | Required (add) | Letter HTML content |
| `--subject <text>` | `-s` | Required (update) | Letter subject |
| `--limit <n>` | `-l` | No | Max results (default: 50) |
| `--offset <n>` | `-o` | No | Results to skip (default: 0) |
| `--json` | | No | Output as JSON |

## Output Fields (list)

| Field | Type | Description |
|-------|------|-------------|
| `letter_id` | Int | Unique ID of the letter |
| `subject` | String | Email subject line |
| `content` | String | HTML content of the letter |
