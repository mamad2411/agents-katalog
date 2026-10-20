---
description: Run Secret Management and Hygiene Verification
globs: ['**/*.env*', '**/src/lib/server/**/*.ts', '**/*.config.*']
---

# Security: Secret Management & Hygiene

<audit_rules>

- You MUST scan the codebase for potential secret leakage, including hardcoded credentials (`password=`, `api_key=`, `secret=`).
- You MUST verify that any `NEXT_PUBLIC_` prefixed environment variables do NOT contain sensitive information (e.g., API keys, database URLs, private tokens).
- You MUST ensure server-side files accessing secrets utilize `import "server-only"` to prevent client-side exposure.
- You MUST verify `.env` files are included in `.gitignore` and not committed to the repository.
- You MUST verify least privilege principles for integrations (e.g., Supabase anon key for client, service role for server only).
  </audit_rules>

<example_good>

```typescript
import 'server-only'
const dbUrl = process.env.DATABASE_URL
```

</example_good>

<example_bad>

```typescript
// Missing 'server-only' import
const dbUrl = process.env.DATABASE_URL

// Client-exposed secret
const NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5c...'
```

</example_bad>
