---
name: epost-schedules
version: 1.0.0
description: "e-post: Manage email send schedules."
metadata:
  category: "email-marketing"
  requires:
    bins: ["epost"]
  cliHelp: "epost schedules --help"
---

# epost schedules

Manage email send schedules in the e-post email marketing platform.

> **PREREQUISITE:** A valid access token must be set before use.
> Run `epost set-token <your_token>` once to save your token.

```bash
epost schedules <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List all schedules |
| `get <id>` | Get a schedule by ID |
| `add` | Create a new send schedule |
| `update <id>` | Update an existing schedule |
| `delete <id>` | Delete a schedule by ID |

## Usage Examples

```bash
# List all schedules
epost schedules list

# List with pagination
epost schedules list --limit 10 --offset 0 --json

# Get a schedule by ID
epost schedules get 10
epost schedules get 10 --json

# Add a new schedule
epost schedules add \
  --letter 5 \
  --date 2026-04-01 \
  --time 09:00:00 \
  --group 42 \
  --sender-email sender@example.com \
  --sender-name "My Company" \
  --reply-to reply@example.com \
  --reply-to-name "Support"

# Add with multiple contact groups (comma-separated)
epost schedules add --letter 5 --date 2026-04-01 --time 09:00:00 --group 42,43,44 --sender-email sender@example.com

# Update a schedule
epost schedules update 10 --letter 5 --date 2026-04-10 --time 10:00:00 --group 42 --sender-email sender@example.com

# Delete a schedule
epost schedules delete 10
```

## Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--letter <id>` | Yes | Letter ID to send |
| `--date <date>` | Yes | Send date in `YYYY-MM-DD` format |
| `--time <time>` | Yes | Send time in `HH:MM:SS` format |
| `--group <ids>` | Yes | Contact group ID(s), comma-separated for multiple |
| `--sender-email <email>` | Yes | Sender email address |
| `--sender-name <name>` | No | Sender display name |
| `--reply-to <email>` | No | Reply-to email address |
| `--reply-to-name <name>` | No | Reply-to display name |
| `--limit <n>` | No | Max results (default: 50) |
| `--offset <n>` | No | Results to skip (default: 0) |
| `--json` | No | Output as JSON |

## Output Fields (list)

| Field | Type | Description |
|-------|------|-------------|
| `schedule_id` | Int | Unique ID of the schedule |
| `letter_id` | Int | ID of the letter to be sent |
| `date` | String | Scheduled send date |
| `time` | String | Scheduled send time |
| `sender_name` | String | Sender display name |
| `sender_email` | String | Sender email address |
| `reply_to_name` | String | Reply-to display name |
| `reply_to` | String | Reply-to email address |
