---
name: env-check
description: Validates current environment variables against .env.example requirements
user-invocable: true
allowed-tools: Bash Read
effort: low
---

## Environment Variable Check

1. Read requirements:
```bash
cat .env.example 2>/dev/null || cat .env.template 2>/dev/null
```

2. Check which are set in the current environment:
```bash
while IFS='=' read -r key _; do
  [[ "$key" =~ ^#|^$ ]] && continue
  if [[ -z "${!key}" ]]; then
    echo "MISSING: $key"
  else
    echo "  SET: $key"
  fi
done < .env.example
```

3. Additional checks:
   - DATABASE_URL: can it actually connect?
   - API keys: correct format (prefix check)?
   - URLs: valid format?

4. Output:
```
Environment Check:
  ✅  DATABASE_URL
  ✅  JWT_SECRET
  ❌  STRIPE_SECRET_KEY  ← MISSING (required for payments)
  ⚠️  REDIS_URL          ← Missing (optional, caching disabled)

Result: 1 required var missing - app will fail to start.
```

5. Suggest how to obtain missing variables.
