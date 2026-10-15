---
name: epost-sms
version: 1.0.0
description: "e-post: Send and list SMS messages."
metadata:
  category: "sms-marketing"
  requires:
    bins: ["epost"]
  cliHelp: "epost sms --help"
---

# epost sms

Send and manage SMS messages via the e-post platform.

> **PREREQUISITE:** A valid access token must be set before use.
> Run `epost set-token <your_token>` once to save your token.

```bash
epost sms <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List sent SMS records |
| `get <id>` | Get an SMS record by ID |
| `send <phone>` | Send an SMS to a phone number |

## Usage Examples

```bash
# List all SMS records
epost sms list

# List with pagination
epost sms list --limit 20 --offset 0

# List as JSON
epost sms list --json

# Get an SMS record by ID
epost sms get 99
epost sms get 99 --json

# Send an SMS
epost sms send +85298765432 --content "Hello from e-post!"

# Send to a local HK number
epost sms send 98765432 --content "Your verification code is 1234"
```

## Flags

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--content <text>` | `-c` | Required (send) | SMS message content |
| `--limit <n>` | `-l` | No | Max results (default: 50) |
| `--offset <n>` | `-o` | No | Results to skip (default: 0) |
| `--json` | | No | Output as JSON |

## Output Fields (list)

| Field | Type | Description |
|-------|------|-------------|
| `sms_id` | Int | Unique ID of the SMS record |
| `phone` | String | Recipient phone number |
| `content` | String | SMS message content |
| `no_of_msg` | Int | Number of SMS segments used |
| `created_time` | String | Time the SMS was created |
| `receive_time` | String | Time the SMS was received |
| `receive_status` | String | Delivery status |
| `report_time` | String | Time of delivery report |
