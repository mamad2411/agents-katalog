---
name: deploy-check
description: Pre-deploy checklist - runs tests, checks env vars, verifies build, and flags risks
user-invocable: true
allowed-tools: Bash Read Glob
effort: low
---

## Pre-Deploy Checklist

Running production readiness checks...

### 1. Build
```bash
npm run build 2>&1 || bun run build 2>&1
```

### 2. Tests
```bash
npm test 2>&1 || bun test 2>&1
npx tsc --noEmit 2>&1
```

### 3. Env Vars
```bash
# Check all required vars from .env.example are set in current env
diff <(grep -oE "^[A-Z_]+=" .env.example | sort) <(env | grep -oE "^[A-Z_]+=" | sort)
```

### 4. Security
```bash
npm audit --audit-level=high 2>&1 | grep -E "critical|high" | head -10
```

### 5. Database
- Any pending migrations? (run migration status)
- Any seed data needed for new features?

### 6. Risk Assessment
- What changed since last deploy? (`git log --oneline $(git describe --tags --abbrev=0)..HEAD`)
- Any breaking API changes?
- Any new required environment variables?

---

Output a traffic-light summary:
- 🟢 Ready to deploy
- 🟡 Ready with warnings (list them)
- 🔴 Do NOT deploy (list blockers)
