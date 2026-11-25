---
name: breaking-changes
description: Detects breaking changes between two git refs and generates a migration guide
argument-hint: <base-ref> [head-ref]
user-invocable: true
allowed-tools: Bash Read
effort: medium
---

## Breaking Change Detection

Base: **$1** (e.g., `v1.2.0`, `main`)
Head: **$2** (default: current HEAD)

1. Get the diff:
```bash
git diff $1 ${2:-HEAD} -- src/ --name-only
git diff $1 ${2:-HEAD} -- src/
```

2. Analyze changes for breakage:

**Public API changes** (exports):
- Removed exported functions/types
- Changed function signatures (added required params, changed types)
- Changed return types

**Database changes:**
- Removed columns (app code still references them?)
- Renamed columns/tables
- Changed column types

**Config/env changes:**
- Renamed environment variables
- New required env vars without defaults

**Behavior changes:**
- Changed default values
- Changed error types/messages (if consumers check these)

3. For each breaking change, write a migration step:
```markdown
## Breaking Changes in v2.0.0

### `createUser()` now requires `role` parameter
**Before:** `createUser({ name, email })`
**After:** `createUser({ name, email, role: 'user' })`
**Migration:** Add `role: 'user'` as default to all call sites.
```
