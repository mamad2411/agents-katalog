---
name: epost-delivery
version: 1.0.0
description: "e-post: List email delivery records for a schedule."
metadata:
  category: "email-marketing"
  requires:
    bins: ["epost"]
  cliHelp: "epost delivery --help"
---

# epost delivery

List email delivery records for a specific send schedule in the e-post platform.

> **PREREQUISITE:** A valid access token must be set before use.
> Run `epost set-token <your_token>` once to save your token.

```bash
epost delivery <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List delivery records for a schedule |
| `get <id>` | Get a delivery record by ID |

## Usage Examples

```bash
# Get a delivery record by ID
epost delivery get 12345
epost delivery get 12345 --json

# List delivery records for a schedule
epost delivery list --schedule 53700

# List with pagination
epost delivery list --schedule 53700 --limit 10 --offset 0

# Output as JSON
epost delivery list --schedule 53700 --json
```

## Flags

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--schedule <id>` | `-s` | Yes | Schedule ID to query deliveries for |
| `--limit <n>` | `-l` | No | Max results (default: 50) |
| `--offset <n>` | `-o` | No | Results to skip (default: 0) |
| `--json` | | No | Output as JSON |

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `delivery_id` | Int | Unique ID of the delivery record |
| `name` | String | Recipient name |
| `email` | String | Recipient email address |
| `time` | String | Time the system sent the email |
| `letter_id` | Int | ID of the letter that was sent |
| `viewed` | Boolean | Whether the email was opened |
| `view_ip` | String | IP address when email was opened |
| `view_time` | String | Time the email was opened |
| `statusLabel` | String | Delivery status label |
| `bounceCode` | String | Bounce code if delivery failed |
