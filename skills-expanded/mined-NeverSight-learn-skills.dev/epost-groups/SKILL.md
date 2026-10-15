---
name: epost-groups
version: 1.0.0
description: "e-post: Manage contact groups."
metadata:
  category: "email-marketing"
  requires:
    bins: ["epost"]
  cliHelp: "epost groups --help"
---

# epost groups

Manage contact groups in the e-post email marketing platform.

> **PREREQUISITE:** A valid access token must be set before use.
> Run `epost set-token <your_token>` once to save your token.

```bash
epost groups <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List all contact groups |
| `get <id>` | Get a contact group by ID |
| `add <name>` | Create a new contact group |
| `delete <id>` | Delete a contact group by ID |

## Usage Examples

```bash
# List all contact groups
epost groups list

# List as JSON
epost groups list --json

# Get a contact group by ID
epost groups get 42
epost groups get 42 --json

# Add a new contact group
epost groups add "VIP Customers"

# Delete a contact group by ID
epost groups delete 42
```

## Flags

| Flag | Description |
|------|-------------|
| `--json` | Output results as JSON (list only) |

## Output Fields (list)

| Field | Type | Description |
|-------|------|-------------|
| `contactgroup_id` | Int | Unique ID of the contact group |
| `name` | String | Name of the contact group |
