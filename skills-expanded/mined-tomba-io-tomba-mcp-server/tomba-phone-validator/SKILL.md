---
name: tomba-phone-validator
description: "Validate a phone number and return its carrier, line type, and formatting using Tomba's phone_validator tool."
user-invocable: true
argument-hint: "<phone in +E.164 format>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "☎️"
        homepage: https://tomba.io
---

# Tomba Phone Validator

This skill uses the `phone_validator` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Checking whether a phone number is valid, mobile or landline, and which carrier it uses.

## Inputs

| Parameter | Type   | Required | Notes                                                                                                                                      |
| --------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `phone`   | string | yes      | E.164 number: `+`, country code, digits only, e.g. `+14155552671`. The hosted server rejects numbers that start with `0` or contain spaces |
| `country` | string | no       | Local server only: ISO 3166-1 alpha-2 code (e.g. `FR`) for numbers without a `+` prefix                                                    |

## Workflow

1. Convert the number to E.164 first: strip spaces and punctuation, drop the national leading `0`, and add `+` and the country code (e.g. French `06 12 34 56 78` becomes `+33612345678`). Ask for the country if you cannot infer it.
2. Call `phone_validator`.

## Output Expectations

- Valid or invalid, E.164 and local formats, line type, carrier, and country.

## Example Usage

```
/tomba:tomba-phone-validator +14155552671
/tomba:tomba-phone-validator +33612345678
/tomba:tomba-phone-validator +442079460958
```

## Example Tool Call

User: "Is 06 12 34 56 78 a valid French mobile?"

```json
{
    "tool": "phone_validator",
    "arguments": {
        "phone": "+33612345678"
    }
}
```
