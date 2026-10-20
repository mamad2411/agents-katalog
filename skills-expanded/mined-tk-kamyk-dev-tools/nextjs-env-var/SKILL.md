---
name: nextjs-env-var
metadata:
  stack: [nextjs]
description: Add a new environment variable end-to-end — secret store (e.g. Key Vault), Zod validation in lib/env.ts, source map, .env.example, local .env. Triggers when adding or modifying env vars in the Next.js frontend.
---

# Add Environment Variable

This skill guides the full workflow for adding a new environment variable to a Next.js frontend that uses a `lib/env.ts` Zod-validated source-mapped pattern.

## Required Input

Ask the user for:
1. **Variable name** (e.g., `NEXT_PUBLIC_MY_FEATURE`)
2. **Type** — one of: `urlEnv()`, `boolEnv()`, `secretEnv()`, `enumEnv([...])`, `listEnv(...)`, or raw `z.string()`
3. **Required or optional** — should it have `.optional()` or a `.default(value)`?
4. **Description** — what is this variable for?
5. **Default value** (if any)

## Steps

### 1. Add to the secret store

Instruct the user to add the secret manually to the project's secret backend (Azure Key Vault, AWS Secrets Manager, Vercel env settings, etc.):

```
Secret name: <VARIABLE_NAME> (use the backend's naming convention — e.g. hyphens for Key Vault)
```

Remind them to authenticate (`az login`, `aws sts get-caller-identity`, Vercel login) before adding the secret, then pull it locally (`pnpm env:pull:force` or equivalent).

### 2. Add Zod validation to `lib/env.ts`

Edit `<frontend-app>/lib/env.ts`:

**a) Add to the Zod schema object** (first argument of `createEnv`):
- Place it in the appropriate section (grouped with related vars)
- Use the correct env helper type

**b) Add to the source map** (second argument of `createEnv`):
- Add explicit `process.env.VARIABLE_NAME` reference
- This is required for Next.js to inline `NEXT_PUBLIC_*` vars at build time

Example for a new feature flag:
```typescript
// In schema:
NEXT_PUBLIC_FT_ENABLE_MY_FEATURE: boolEnv().default(false),

// In source map:
NEXT_PUBLIC_FT_ENABLE_MY_FEATURE: process.env.NEXT_PUBLIC_FT_ENABLE_MY_FEATURE,
```

### 3. Update `.env.example`

Edit `<frontend-app>/.env.example`:
- Add the variable with a placeholder/example value
- Add a comment explaining what it does
- Place it in the correct section

### 4. Verify

After all edits:
1. Run `pnpm check-types` to verify the Zod schema compiles
2. Confirm the variable is accessible via `import { env } from '@/lib/env'`

## Important Rules

- **NEVER** access the new variable via `process.env` anywhere except `lib/env.ts`
- **ALWAYS** use the appropriate env helper (`urlEnv`, `boolEnv`, `secretEnv`, etc.)
- **ALWAYS** add to both the schema AND the source map in `lib/env.ts`
- Feature flags should follow the naming convention: `NEXT_PUBLIC_FT_ENABLE_*`
- Server-only secrets should NOT have the `NEXT_PUBLIC_` prefix
