---
name: secret-guard
description: "Use whenever you are about to put a credential, API key, token, or password into code — or whenever a secret already appears in a file you're editing. Triggers on \"add the API key\", \"paste the token\", \"hardcode the secret\", \"set the password\", \"AWS/Stripe/OpenAI/GitHub key\", \"connect to <service>\", \"use this credential\", config/setup work that wires up a third-party service, and any moment a real secret value is in hand. The rule: secrets go in the environment, never in source."
---

# Secret Guard

**A secret in source is a secret that's already leaked.** The moment a live key
lands in a tracked file it gets committed, pushed, mirrored, cached, and shared
— and you can't un-publish it. The only safe assumption for a hardcoded
credential is that it's burned.

Secret Guard makes the safe path the default: a PreToolUse hook scans the new
content of every `Edit`/`Write`/`MultiEdit` and **blocks the write** when it
carries a real-looking credential into a non-env source file.

## The rule

> **Secrets live in the environment, never in source.** Read them at runtime;
> commit a placeholder, never the value.

## The method

1. **Never type the literal into code.** Put the real value in a `.env` file
   (which is gitignored) or your secret manager:

   ```bash
   # .env  (gitignored — the correct home for the real value)
   STRIPE_SECRET_KEY=sk_live_...realvalue...
   ```

2. **Read it at runtime** instead of hardcoding it:

   ```js
   const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
   ```
   ```python
   stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
   ```

3. **Commit a placeholder, not the secret**, so teammates know what's needed:

   ```bash
   # .env.example  (committed — safe, no real value)
   STRIPE_SECRET_KEY=sk_live_your_key_here
   ```

4. **If a real key ever touched a file or a commit, rotate it now.** Don't
   `git rm` and hope — assume it's compromised, revoke it, issue a new one, and
   move the new one into `.env`.

## What this catches

The hook blocks a write when the added text contains a live-looking secret —
AWS access key ids (`AKIA…`), GitHub tokens (`ghp_…`), OpenAI/Anthropic keys
(`sk-…`, `sk-ant-…`), Stripe live keys (`sk_live_…`, `pk_live_…`), Google API
keys (`AIza…`), Slack tokens (`xox…`), `-----BEGIN PRIVATE KEY-----` blocks, and
a long high-entropy literal assigned to a secret-named variable
(`apiKey = "…"`).

It deliberately **does not** block the safe patterns:

- `.env`, `.env.*`, `*.env`, and `*.example` / `*.sample` / `*.template` files
  — that's where secrets and their placeholders belong.
- `process.env.X`, `os.environ["X"]`, `getenv(...)` — reading from the
  environment is the pattern we *want*.
- Placeholders and examples — `your-key-here`, `<TOKEN>`, `${VAR}`, `xxxxx`,
  `changeme`, `REDACTED`, `...`, all-same-char values.

## When the hook blocks you

It's telling you a real value is about to be committed. Don't reword it to slip
past — fix the design: move the value to `.env`, read it at runtime, leave a
placeholder in `.env.example`. If the value is a **deliberately fake**,
shaped-like-a-key test fixture (not a live credential), say so on its own line:

```
SECRET-GUARD: ALLOW — fake Stripe key, test fixture only
```

## Kill switch

False positive, or a context where the gate doesn't apply:
`touch .secret-guard-off` in the project root (or
`~/.claude/.secret-guard-off` globally), or `export SECRET_GUARD_GATE=off`.
Fails open on any error — a broken guard never blocks your work.

## Pairs with

- **`scope-guard`** — scope says *which* files; secret-guard says *what must
  never be in them*.
- **`verify-before-done`** — once the key is in `.env` and read at runtime,
  prove the integration actually connects.
