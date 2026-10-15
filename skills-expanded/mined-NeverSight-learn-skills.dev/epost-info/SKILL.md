---
name: epost-info
version: 1.0.0
description: "e-post: Show account quota and expiry information."
metadata:
  category: "email-marketing"
  requires:
    bins: ["epost"]
  cliHelp: "epost info --help"
---

# epost info

Show account quota and expiry dates for email and SMS sending.

> **PREREQUISITE:** A valid access token must be set before use.
> Run `epost set-token <your_token>` once to save your token.

```bash
epost info [flags]
```

## Usage Examples

```bash
# Show account quota info
epost info

# Output as JSON
epost info --json
```

## Sample Output

```
=== Account Info ===

Email Quota:
  Quota      : 5000
  Expiry Date: 2026-12-31

SMS Quota:
  Quota      : 500
  Expiry Date: 2026-12-31
```

## Flags

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON |

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `quota.quota` | Int | Remaining email sending quota |
| `quota.expiry_date` | String | Email quota expiry date |
| `smsQuota.quota` | Int | Remaining SMS sending quota |
| `smsQuota.expiry_date` | String | SMS quota expiry date |
