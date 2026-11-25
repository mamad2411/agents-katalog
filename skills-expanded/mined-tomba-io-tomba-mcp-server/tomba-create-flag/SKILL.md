---
name: tomba-create-flag
description: "Report incorrect Tomba data (hard bounce, wrong person, outdated, and so on) for credit recovery using the create_flag tool."
user-invocable: true
argument-hint: "<value> <reason> [comment]"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🏳️"
        homepage: https://tomba.io
---

# Tomba Create Flag

This skill uses the `create_flag` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user reports that an email bounced or that data was wrong, and wants it flagged or their credits recovered.

Do not use it when:

- Do not flag data on your own initiative; this submits a report from the user's account.

## Inputs

| Parameter   | Type   | Required | Notes                                                                                                                |
| ----------- | ------ | -------- | -------------------------------------------------------------------------------------------------------------------- |
| `flag_type` | string | yes      | `email`, `organization`, `phone`, `author_url`, or `website`                                                         |
| `value`     | string | yes      | The value being flagged (the email address, domain, phone number, or URL)                                            |
| `reason`    | string | yes      | `hard_bounce`, `invalid_email`, `wrong_person`, `outdated`, `other`, `wrong_company`, `wrong_phone`, or `broken_url` |
| `comment`   | string | no       | Extra details                                                                                                        |

## Workflow

1. Map the user's complaint to `flag_type` and `reason`.
2. Confirm with the user, then call `create_flag`.

## Output Expectations

- Confirm the flag that was submitted and its status.

## Example Usage

```
/tomba:tomba-create-flag bob@acme.com hard_bounce
/tomba:tomba-create-flag jane@acme.com wrong_person "left the company"
/tomba:tomba-create-flag +14155552671 wrong_phone
```

## Example Tool Call

User: "bob@acme.com hard bounced, report it"

```json
{
    "tool": "create_flag",
    "arguments": {
        "flag_type": "email",
        "value": "bob@acme.com",
        "reason": "hard_bounce"
    }
}
```
