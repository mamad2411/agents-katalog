---
description: Linting workflow for api and webapp (Oxlint)
globs: api/**/*.js, webapp/**/*.{js,jsx}
alwaysApply: false
---

# Linting Workflow

This repo uses **Oxlint** (`oxlint` + `oxlint-plugin-eslint`) in **`api/`** and **`webapp/`**.

After any substantive edit under `api/` or `webapp/`:

1. Run `npm run lint` in the package you changed (`cd api` or `cd webapp`).
2. Optionally run `npm run lint:fix` for safe auto-fixes.
3. Use editor diagnostics / `ReadLints` on edited files for anything Oxlint does not auto-fix.
4. Never leave a task marked complete with outstanding lint **errors** (warnings are acceptable unless the runbook phase requires zero warnings).

# No Conditional Spread

Never use `...(condition && { key: value })` to build objects conditionally. Prefer explicit branches or building an object in steps.

```javascript
// ❌ BAD
const payload = { ...(flag && { extra: 1 }) };

// ✅ GOOD
const payload = {};
if (flag) payload.extra = 1;
```
