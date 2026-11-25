---
name: env-setup
description: Creates .env.example, validates required env vars, and documents each one
user-invocable: true
allowed-tools: Read Grep Glob Edit Bash
effort: low
---

## Environment Setup

1. Find all env var usages:
```bash
grep -rn "process\.env\.\|Deno\.env\.get\|env\." src/ --include="*.ts" --include="*.js" | grep -oE "process\.env\.[A-Z_]+" | sort -u
```

2. Check existing `.env*` files:
```bash
ls .env* 2>/dev/null
cat .env.example 2>/dev/null
```

3. For each env var found:
   - What is it used for?
   - Is it required or optional?
   - What's a safe example value?
   - Any format constraints? (URL, UUID, comma-separated, etc.)

4. Generate/update `.env.example`:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Auth
JWT_SECRET=your-secret-key-min-32-chars
JWT_EXPIRES_IN=7d

# External APIs (optional)
STRIPE_SECRET_KEY=sk_test_...
```

5. Generate a startup validation script `src/lib/env.ts` using `zod` or `envalid` to fail fast if required vars are missing.
