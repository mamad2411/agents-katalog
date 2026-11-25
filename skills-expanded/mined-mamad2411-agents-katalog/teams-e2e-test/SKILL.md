---
name: teams-e2e-test
description: Trigger when user wants to E2E test a Teams bot example. Reads e2e-instructions.md for infra setup and e2e.spec.md for assertions. Supports running, generating, healing tests, and auth setup. Everything in generated/ is disposable.
allowed-tools: Bash(*), Read(*), Glob(*), Grep(*), Edit(*), Write(*)
---

# E2E Test a Teams Bot Example

## Overview

Two source-of-truth files drive everything:

| File | Scope | Contains |
|---|---|---|
| `e2e-instructions.md` | Repo-wide | How to start infra (env path, devtunnel, bot start command, ready pattern) |
| `examples/<name>/e2e.spec.md` | Per-bot | What to test (act + assert pairs) |

Everything in `e2e-test/generated/` is disposable — Claude can delete and regenerate it at any time.

| Mode | When to use | What happens |
|---|---|---|
| **Run** | `generated/<name>.spec.ts` exists | Start infra → run Playwright → stop infra |
| **Generate** | `e2e.spec.md` exists but no generated spec | Start infra → explore interactively → generate spec → verify → stop infra |
| **Heal** | Tests are failing | Run tests → diagnose → fix generated files → re-run |
| **Auth Setup** | Login required or expired | Headed browser → user MFA → save state |

## Execution Rules

1. **Never send a text-only turn between tool calls.** Always bundle narration with the next tool call.
2. **Parallelize independent tool calls.**
3. **Never modify `e2e.spec.md` or `e2e-instructions.md`** — only modify files in `generated/`.

---

## First-Time Setup

Before any mode, check that prerequisites exist.

### Check `e2e-instructions.md`

If it **doesn't exist**, ask the user:

1. "What command starts your bot?" (e.g. `npm run dev`, `uv run python -m main`, `dotnet run`)
2. "How does it load env vars?" (e.g. `DOTENV_CONFIG_PATH=../../e2e-test/.env` prefix, or copies `.env` to cwd)
3. "What output means the bot is ready?" (e.g. `listening`, `started`, `ready`)

Then write `e2e-instructions.md`:

```md
# E2E Instructions

## Environment
- env: `e2e-test/.env`
- devtunnel: `devtunnel host $DEVTUNNEL_NAME`

## Bot Start
- command: `<env-loading> <start-command>`
- ready: `<ready-pattern>`
```

### Check `e2e-test/.env`

Verify it exists and contains `DEVTUNNEL_NAME`. If missing, tell the user:

> E2E tests need `e2e-test/.env` with at minimum `DEVTUNNEL_NAME=<your-tunnel>`. Create this file and re-run.

### Bootstrap `e2e-test/` as a standalone test project

The test harness is self-contained — it does **not** depend on the host repo's package manager or language.

```bash
# Only run if e2e-test/package.json doesn't exist yet
cd e2e-test
npm init -y
npm install --save-dev @playwright/test typescript
npx playwright install chromium
cd ..
```

This ensures Playwright works regardless of whether the bot is TypeScript, Python, C#, Java, etc.

---

## Infrastructure Lifecycle

The skill manages infra directly by reading `e2e-instructions.md`.

### Start infra

1. Read `e2e-instructions.md` for env path, devtunnel command, bot start command, ready pattern
2. `source` the env file
3. Kill stale processes: `playwright-cli kill-all 2>/dev/null`; kill any process on bot ports
4. Run the devtunnel command (background), wait for "ready to accept connections"
5. `cd examples/<name>` and run the bot start command (background), wait for the ready pattern

### Stop infra

Kill the bot and devtunnel processes started above.

---

## Mode: Run

Use when `e2e-test/generated/<name>.spec.ts` exists.

### Prerequisites (single turn, all parallel)

1. `Read`: `e2e-instructions.md`
2. `Bash`: check `e2e-test/.env` exists and has `DEVTUNNEL_NAME`
3. `Bash`: check `e2e-test/generated/<name>.spec.ts` exists
4. `Bash`: check `e2e-test/package.json` exists (if not → run Bootstrap step)
5. `Bash`: kill stale processes

### Execute

1. Start infra
2. Run tests:
   ```bash
   cd e2e-test && npx playwright test --config generated/playwright.config.ts generated/<name>.spec.ts
   ```
3. Stop infra

**If all pass** → done.
**If tests fail** → switch to **Heal**.
**If auth fails** (login URL in error) → switch to **Auth Setup**.

---

## Mode: Generate

Use when `examples/<name>/e2e.spec.md` exists but no generated spec.

### Phase 1: Interactive exploration

Read `e2e.spec.md` and walk through each assertion manually using `playwright-cli`.

Start infra, then open the browser:

```bash
playwright-cli -s=teams open --persistent
playwright-cli -s=teams goto "https://teams.cloud.microsoft/v2/#/conversations"
sleep 20 && playwright-cli -s=teams snapshot
```

If auth fails → switch to **Auth Setup** first, then resume.

For each assertion:
1. **Snapshot** current state
2. **Perform the action** (type, click, fill)
3. **Wait** (`sleep 5`) for bot response
4. **Snapshot again** to verify
5. **Record** exact selectors, text, and timing that worked

**Rules:**
- `sleep 5` between actions and checks
- Snapshot after every action
- Debug failures here before moving on

Close when done: `playwright-cli -s=teams close`

### Phase 2: Generate the spec

Write `e2e-test/generated/<name>.spec.ts` using selectors discovered in Phase 1.

If `generated/` is missing infrastructure, also generate:
- `playwright.config.ts`, `tsconfig.json`, `helpers/teams-fixture.ts`

All generated files get: `// Auto-generated from e2e.spec.md — do not edit manually`

Pattern:

```typescript
import { test, expect, sendAndExpect } from './helpers/teams-fixture';

test.describe('<Bot Name>', () => {
  test('description', async ({ teamsPage: page }) => {
    await sendAndExpect(page, 'message', 'expected response');
  });
});
```

**Rules:**
- Use selectors from Phase 1 — don't guess
- Accessibility selectors: `getByText()`, `getByRole()`, `getByLabel()`
- Always `.last()` on response locators (chat history accumulates)
- `sendAndExpect()` for simple send → verify flows
- 10s timeout for bot responses
- Tests run serially, state carries between tests

### Phase 3: Verify

Run generated tests headless. Stop infra when done.
If tests fail → fix from Phase 1 knowledge, don't re-explore unless unexpected.

---

## Mode: Heal

Use when tests are failing.

1. **Start infra, run tests, capture output**
2. **Diagnose:**
   | Error | Cause | Fix |
   |---|---|---|
   | login URL in error | Auth expired | Auth Setup |
   | element not found | Selector changed | Inspect UI, update selector |
   | Timeout | Bot slow / not responding | Increase timeout, check bot |
   | strict mode violation | Multiple matches | Add `.last()` or narrow selector |
3. **If not obvious** → open `playwright-cli` to inspect current UI
4. **Patch** `e2e-test/generated/<name>.spec.ts` — never modify `e2e.spec.md`
5. **Re-run** until all pass
6. **Stop infra**

---

## Auth Setup

If errors contain `login.microsoftonline.com` → auth expired.

```bash
playwright-cli -s=teams open --persistent --headed
playwright-cli -s=teams goto "https://teams.cloud.microsoft/"
```

**Prompt the user:**
> Please complete the Microsoft login (including MFA). Let me know once you're on the Teams main page.

After confirmation:
```bash
playwright-cli -s=teams state-save ./e2e-test/browser-state.json
playwright-cli -s=teams close
```

---

## File Layout

```
e2e-instructions.md                # Repo-wide infra config (human-owned)
e2e-test/
  package.json                      # Standalone test project (auto-bootstrapped)
  .env                              # Credentials (gitignored)
  .browser-profile/                 # Fallback auth profile (gitignored)
  generated/                        # Disposable, Claude-owned
    playwright.config.ts
    tsconfig.json
    helpers/
      teams-fixture.ts
    <name>.spec.ts
examples/
  <name>/e2e.spec.md                # Human-authored assertions (source of truth)
```

## Quick Reference

| Action | Command |
|---|---|
| Run tests | `cd e2e-test && npx playwright test --config generated/playwright.config.ts generated/<name>.spec.ts` |
| Run headed | `cd e2e-test && E2E_HEADED=1 npx playwright test --config ...` |
| Auth setup | `playwright-cli -s=teams open --persistent --headed` |
| Kill stale | `playwright-cli kill-all; lsof -ti:<ports> \| xargs kill` |
