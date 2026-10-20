---
description: Run Environment Management and Parity Verification
globs: ["**/.env*", "**/package.json", "**/vercel.json", "**/.nvmrc"]
---
# Infrastructure: Environment Management & Parity

<audit_rules>
- You MUST verify that `.env.example` matches the structure of production environment variables, with no missing required variables.
- You MUST ensure there are no hardcoded secrets or `NEXT_PUBLIC_` prefixes on sensitive variables in `.env.example` or code.
- You MUST check that the Node.js version specified in `.nvmrc` or `package.json` (`engines`) matches the production environment (e.g., Vercel settings).
- You MUST verify that service dependencies (e.g., SQLite vs. Postgres, Redis configurations) are consistent between development and production environments.
- You MUST ensure all environment variables are validated on application startup (e.g., using Zod env validation).
</audit_rules>

<example_good>
```typescript
// src/env.ts
import { z } from "zod";

export const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXT_PUBLIC_API_URL: z.string().url(), // Safe public variable
});

envSchema.parse(process.env);
```
</example_good>

<example_bad>
```bash
# .env.example
DATABASE_URL=postgres://user:password@localhost:5432/mydb # BAD: Hardcoded secret in template
NEXT_PUBLIC_STRIPE_SECRET_KEY=sk_test_12345 # BAD: Secret exposed to client
```
</example_bad>

