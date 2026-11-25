---
name: env-validator
description: |
  Validate .env files against a schema. Detects missing, empty, or malformed
  environment variables at startup. Triggers on "validate env", "check .env",
  "environment variables", "env schema".
metadata:
  type: tool
  version: "1.0.0"
  author: community
  tags: [env, validation, configuration, devops]
triggers:
  - "validate env"
  - "check environment variables"
  - "env schema"
  - "validate .env"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Environment Variable Validator

Validate `.env` files against a schema to catch misconfigurations at startup.

## When to Use
- Adding new environment variables to a project
- Debugging "works on my machine" config issues
- Setting up a new deployment environment
- User mentions "env", "environment variables", ".env validation"

## When NOT to Use
- Secrets management (use a vault/secrets manager for production secrets)
- Runtime config that changes frequently (use a config service)

## Workflow
1. Scan the project for `.env.example`, `.env`, and code that reads env vars
2. Build a schema of all required and optional env vars with types
3. Generate a validation module that runs at startup:
   - Check required vars are present
   - Validate types (string, number, boolean, URL, email)
   - Validate constraints (min/max length, enum values, regex patterns)
   - Warn on unused or misspelled vars
4. Create/update `.env.example` with all vars and descriptions
5. Add a pre-start check script

## Output
```typescript
// src/config/env.ts
const schema = z.object({
  PORT: z.coerce.number().min(1024).max(65535).default(3000),
  DATABASE_URL: z.string().url().startsWith("postgresql://"),
  REDIS_URL: z.string().url().optional(),
  JWT_SECRET: z.string().min(32),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
  CORS_ORIGIN: z.string().url(),
  SMTP_HOST: z.string().optional(),
  SMTP_PORT: z.coerce.number().optional(),
});

export const env = schema.parse(process.env);
```

## Key Principles
- Fail fast at startup — don't fail mid-request on missing config
- Use Zod/joi/yup for schema validation (match project's existing stack)
- Always provide clear error messages: "Missing DATABASE_URL. Expected: postgresql://..."
- Generate `.env.example` with descriptions and defaults
- Don't log secrets in validation errors

## Notes
- Add `.env` to `.gitignore` if not already there
- `.env.example` should be committed, `.env` should never be
- Consider adding an `npm run check-env` script for CI
