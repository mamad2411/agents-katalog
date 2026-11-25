---
name: tomba-email-verifier
description: "Check whether an email address is deliverable (valid, invalid, accept-all, disposable, webmail) using Tomba's email_verifier tool."
user-invocable: true
argument-hint: "<email>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "✅"
        homepage: https://tomba.io
---

# Tomba Email Verifier

This skill uses the `email_verifier` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user asks whether an email is valid, deliverable, or safe to send to.
- Confirming an address found by `tomba-email-finder` before you present it as final.

Do not use it when:

- Verifying a long list without the user's agreement: each call uses credits.

## Inputs

| Parameter                        | Type         | Required | Notes                                                                  |
| -------------------------------- | ------------ | -------- | ---------------------------------------------------------------------- |
| `email`                          | string       | yes      | Email address to verify                                                |
| `enrich_mobile` / `enrichMobile` | boolean      | no       | Also return mobile phone data when available (may use extra credits)   |
| `webhook_url`                    | string (URL) | no       | Hosted server only: public URL that receives the result asynchronously |

Where a row shows two names (`hosted / local`), the hosted server at `mcp.tomba.io` uses the first and the local npm server uses the second. Use the name in the connected tool's input schema.

## Workflow

1. Call `email_verifier` with the address.
2. Read the overall status together with the SMTP/MX checks, accept-all, disposable, and webmail flags.
3. If the status is invalid or the address bounced, suggest reporting it with `tomba-create-flag`.

## Output Expectations

- A clear verdict: valid, invalid, accept-all/risky, or unknown.
- The key reasons (MX records, SMTP check, accept-all, disposable, webmail).
- Never call an accept-all result "verified".

## Example Usage

```
/tomba:tomba-email-verifier jane@acme.com
/tomba:tomba-email-verifier snadella@microsoft.com with mobile
/tomba:tomba-email-verifier is support@zapier.com deliverable?
```

## Example Tool Call

User: "Is jane@acme.com a real address?"

```json
{
    "tool": "email_verifier",
    "arguments": {
        "email": "jane@acme.com"
    }
}
```
