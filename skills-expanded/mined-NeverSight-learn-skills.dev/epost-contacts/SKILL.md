---
name: epost-contacts
version: 1.0.0
description: "e-post: Manage contacts."
metadata:
  category: "email-marketing"
  requires:
    bins: ["epost"]
  cliHelp: "epost contacts --help"
---

# epost contacts

Manage contacts in the e-post email marketing platform.

> **PREREQUISITE:** A valid access token must be set before use.
> Run `epost set-token <your_token>` once to save your token.

```bash
epost contacts <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List contacts (optionally filtered by group) |
| `get <id>` | Get a contact by ID |
| `add <name>` | Add a new contact to a group |
| `delete <id>` | Delete a contact by ID |

## Usage Examples

```bash
# List all contacts
epost contacts list

# List contacts in a specific group
epost contacts list --group 42

# List with pagination
epost contacts list --limit 20 --offset 40

# List as JSON
epost contacts list --json

# Get a contact by ID
epost contacts get 101
epost contacts get 101 --json

# Add a contact to a group
epost contacts add "John Doe" --group 42 --email john@example.com --phone +85298765432

# Delete a contact by ID
epost contacts delete 101
```

## Flags

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--group <id>` | `-g` | Required (add) | Contact group ID |
| `--email <email>` | `-e` | No | Email address |
| `--phone <phone>` | `-p` | No | Phone number |
| `--limit <n>` | `-l` | No | Max results (default: 50) |
| `--offset <n>` | `-o` | No | Results to skip (default: 0) |
| `--json` | | No | Output as JSON |

## Output Fields (list)

| Field | Type | Description |
|-------|------|-------------|
| `contact_id` | Int | Unique ID of the contact |
| `name` | String | Full name |
| `email` | String | Email address |
| `phone` | String | Phone number |
| `contactgroup_id` | Int | Contact group ID |
