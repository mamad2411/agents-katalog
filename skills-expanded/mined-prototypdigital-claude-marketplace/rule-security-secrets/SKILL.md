---
name: security-secrets
description: Never hardcode secrets, tokens, or credentials in source code.
---

# Security — secrets management

A secret committed to git lives in history forever — bots scrape public and leaked repos within minutes, so a single hardcoded key can mean account takeover or a compromised production database even after you delete the line. Secrets, tokens, API keys, and connection strings must never appear in source code.

## Rules

- Read secrets from environment variables or a secrets manager at runtime.
- Never commit `.env` files, credentials JSON, or private keys.
- Use placeholder values in example configs (e.g. `YOUR_API_KEY_HERE`).
- Rotate any secret that was accidentally committed, even after removal.
- Keep `.env.example` with variable names but no real values.
- Flag hardcoded strings that look like tokens, passwords, or connection strings in code review.

This is a non-negotiable invariant: back it with a secret-scanning gate (pre-commit hook or CI step such as gitleaks/trufflehog) that blocks the commit — a prose rule alone cannot guarantee no secret slips through.

## Examples

```ts
// BAD — hardcoded secret committed to source control
const stripe = new Stripe('sk_live_HARDCODED_DO_NOT_DO_THIS')
const db = new Client({ connectionString: 'postgresql://user:pass123@db.prod:5432/app' })

// GOOD — secrets read from environment at runtime
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
const db = new Client({ connectionString: process.env.DATABASE_URL! })
```

```sh
# .env.example — variable names only, no real values
STRIPE_SECRET_KEY=sk_live_YOUR_KEY_HERE
DATABASE_URL=postgresql://user:password@host:5432/dbname
```
