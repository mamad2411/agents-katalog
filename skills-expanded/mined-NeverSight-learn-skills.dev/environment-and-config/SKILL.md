---
name: environment-and-config
description: Use when wiring up env vars, secrets, or runtime config — validate them with zod at boot, split server-only from public (NEXT_PUBLIC_) values, and fail fast with a clear error instead of a cryptic undefined at runtime.
---

# Environment & Config

## Overview

Untyped `process.env` is a runtime landmine: a missing `STRIPE_SECRET_KEY` shows up as `undefined` three layers deep at 2am. **Validate the whole environment once at boot with zod**, expose a typed `env` object, and make a misconfiguration a startup crash with an actionable message.

## When to use

- Adding any new secret or config value.
- A bug traces back to an undefined/empty env var.
- You need to keep server secrets out of the client bundle.

## The pattern

```ts
// src/env.ts
import { z } from "zod";

const server = z.object({
  DATABASE_URL: z.string().url(),
  AUTH_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith("whsec_"),
  RESEND_API_KEY: z.string().startsWith("re_"),
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
});

const client = z.object({
  NEXT_PUBLIC_APP_URL: z.string().url(),
});

const parsed = server.merge(client).safeParse(process.env);
if (!parsed.success) {
  console.error("❌ Invalid environment:", parsed.error.flatten().fieldErrors);
  throw new Error("Invalid environment variables");
}

export const env = parsed.data;
```

Import `env` everywhere instead of `process.env`. TypeScript now knows every key exists and its type.

## Server vs client

- Only `NEXT_PUBLIC_*` vars reach the browser. **Never** prefix a secret with `NEXT_PUBLIC_`.
- Keep a `client` schema separate so it's obvious which values are public.
- For strict isolation, put `import "server-only"` in a `env.server.ts` and only merge public keys into a client-safe export.

## Operational hygiene

- Commit a **`.env.example`** with every key (empty or dummy values) — it's the contract for new devs and CI.
- Add `.env*.local` to `.gitignore`; never commit real secrets.
- In CI/prod, set vars in the platform (Vercel/Doppler/1Password), not in files.

## Pitfalls

- **Reading `process.env` directly** — bypasses validation and types; you lose the safety net.
- **`NEXT_PUBLIC_` on a secret** — it gets inlined into client JS and shipped to every visitor.
- **Validating lazily per-request** — validate once at module load so boot fails loudly.
- **No `.env.example`** — onboarding becomes guesswork and CI breaks mysteriously.
- **Trusting defaults in prod** — require critical vars; only default the harmless ones.

## Hand-off

A typed `env` that the whole app trusts. `database-schema`, `authentication`, `payments-stripe`, and `transactional-email` all read their secrets from here.
