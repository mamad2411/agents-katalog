---
name: tomba-create-lead
description: "Save a new lead (email plus name, company, and position) to a leads list in the user's Tomba account using the create_lead tool."
user-invocable: true
argument-hint: "<email> list <list_id> [first name] [last name] [company] [position]"
version: 1.0.0
metadata:
    openclaw:
        emoji: "➕"
        homepage: https://tomba.io
---

# Tomba Create Lead

This skill uses the `create_lead` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user explicitly asks to save or add a contact to their Tomba leads.

Do not use it when:

- Do not create leads on your own initiative; this changes the user's account.

## Inputs

| Parameter    | Type   | Required | Notes                |
| ------------ | ------ | -------- | -------------------- |
| `email`      | string | yes      | Lead email           |
| `list_id`    | number | yes      | ID of the leads list |
| `first_name` | string | no       | First name           |
| `last_name`  | string | no       | Last name            |
| `company`    | string | no       | Company name         |
| `position`   | string | no       | Job position         |

## Workflow

1. Make sure you have the email and the `list_id`; ask the user for the list ID if it is unknown.
2. Optionally verify the email first with `tomba-email-verifier`.
3. Confirm the details with the user, then call `create_lead`.
4. Check for duplicates with `tomba-list-leads` if the user is unsure.

## Output Expectations

- Confirm the lead that was created and which list it was added to.

## Example Usage

```
/tomba:tomba-create-lead jane@acme.com list 42
/tomba:tomba-create-lead jane@acme.com list 42 Jane Doe VP Sales Acme
```

## Example Tool Call

User: "Add jane@acme.com (Jane Doe, VP Sales, Acme) to list 42"

```json
{
    "tool": "create_lead",
    "arguments": {
        "email": "jane@acme.com",
        "list_id": 42,
        "first_name": "Jane",
        "last_name": "Doe",
        "company": "Acme",
        "position": "VP Sales"
    }
}
```
