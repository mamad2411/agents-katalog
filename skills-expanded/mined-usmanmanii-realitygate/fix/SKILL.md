---
name: fix
description: Fix the problems a RealityGate audit or check found — replace stubs and placeholders with real implementations, remove invented packages, add input validation, stop swallowing errors, and add missing tests — then re-run until the score improves. Use after an audit, or when the user asks to make their vibe-coded app real, production ready, or to raise its Reality Score.
---

# RealityGate fix

Turn findings into real code, one verified step at a time.

1. Get current findings (skip if an audit just ran):

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/bin/realitygate.mjs" audit . --json
   ```

   (Outside the plugin: `npx --yes realitygate audit . --json`.)

2. Fix in this order, and tell the user before each group:
   1. **Secrets** (R-011, R-012, committed `.env`): move values to environment variables the
      human sets, add `.env*` to `.gitignore`, and tell the human to rotate the exposed keys.
      Never print or copy a secret value.
   2. **Invented imports** (R-014): confirm on the npm registry whether the package exists.
      If it doesn't, remove it and implement the needed function for real. If it does,
      **ask the human** before adding it as a dependency.
   3. **Stubs and simulations** (R-001…R-005): implement the real behaviour. If you can't
      (missing API key, unclear requirement), stop and ask. Never replace one placeholder
      with another.
   4. **Unvalidated routes** (R-015): add schema validation (zod, or whatever the project
      already uses) and a test that sends an invalid body.
   5. **Swallowed errors** (R-013): log with context and surface a failure to the caller/user.
   6. **Types** (R-006, R-008): replace `any` and `@ts-ignore` with real types, or keep them
      with a `justified: <reason>` comment if they're truly necessary.
   7. **Tests**: add a test for the main user journey, plus a negative-authorization test
      (user A gets 401/403 on user B's data) for every route that touches data.

3. After each group, re-run `audit` and show the score change. Run the project's own tests if
   it has them.

Rules:
- Never disable a rule, add an exclude, or weaken a test to raise the score. That fakes the
  result the tool exists to prevent.
- Schema changes, auth changes, money logic, deleting data and new dependencies need the
  user's explicit approval first.
- Keep each change small and explain it in plain language.
