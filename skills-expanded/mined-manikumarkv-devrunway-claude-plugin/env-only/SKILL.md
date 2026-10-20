---
name: env-only
description: Environment variable conventions — .env discipline, .env.example, startup validation, and separation by environment. Load when working with .env files or environment variable access.
user-invocable: false
stack: secrets/env-only
paths:
  - ".env*"
  - "**/config/env*"
---

Full standards in [env-only.md](env-only.md). Always-on summary:

**The golden rule:** Secret values live only in environment variables. Never in source code, config files, or version control.

**.env file discipline:**
- `.env` — never committed; in `.gitignore`; contains real secrets for local dev
- `.env.example` — always committed; contains keys with placeholder values; documents all required variables
- `VITE_` prefix exposes variables to the browser bundle — never use `VITE_` for secrets
- `.env.production` — never exists as a file; production vars live in the deployment platform

**Validation at startup:**
- Validate all required env vars at app startup using `z.object({ ... }).safeParse(process.env)` — fail loudly if any are missing
- `safeParse`, not `parse`: a thrown ZodError leaves module load with the whole environment in the frame, and a crash reporter captures the frame. `safeParse` returns a value, so you choose what gets printed — field names and messages, never values
- Never read `process.env.VAR` scattered across the codebase — centralise in one config module
- A missing env var at startup is better than a cryptic runtime error at 3 AM

**The config object holds everything — make it safe to print:**
- The validated object concentrates every secret the process has into one value, one `console.log` away from a log aggregator
- Override `toJSON` and `[Symbol.for('nodejs.util.inspect.custom')]` on it to redact the secret keys, so both routes out of a JS value are covered. Direct reads still return the real value
- This is a backstop for accidents, not permission to log config. Pass a secret to the client that needs it; never into a message

**Access pattern:**
- One `config.ts` / `config.py` / `config.go` file that reads and validates all env vars
- Every other file imports from `config`, never from `process.env` directly

**Never:**
- Hardcode secrets, API keys, or connection strings in source code
- Log env var values (even in debug mode — they end up in log aggregators)
- Log or serialise the config object without redaction, which logs every value at once
- Interpolate a secret into a string that might be printed — a log message, an error, a URL
- Use the same secret in multiple environments
- Commit `.env.local` or any file with real values

**Related skills:** `security-principles` (never log a secret or a full Authorization header; redact before logging, not after), `secret-scanning` (detect committed secrets), your cloud/secrets layer for production secret management
