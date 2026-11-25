---
name: mes-test-verification
description: Use when deciding or running verification for AI-MES Copilot changes, including Maven tests, frontend builds, schema/entity consistency checks, smoke tests, or documenting validation results before commit.
---

# MES Test Verification

## Choose Verification by Change Type

| Change | Minimum verification |
|---|---|
| Backend Java | Maven test from `workspace/idea/ems` |
| Mapper/entity/schema | Maven test plus schema/entity check |
| PC frontend | `npm test` and `npm run build` from `workspace/vscode/ems-forword` |
| API integration | backend test plus frontend build or smoke request |
| Docs only | Markdown path/link/table review |
| Git hook or workflow | dry-run relevant Git command when safe |

## Backend Command

First prepare your own isolated test database and environment variables using `docs/SETUP.md`. Database-writing tests must not target a shared business database. From `workspace/idea/ems` on Windows PowerShell:

```powershell
.\mvnw.cmd -B test
```

On Linux/macOS, use `./mvnw -B test`. Use the `package` goal when packaging is part of the task. Full prerequisites and prior execution scopes are recorded in `docs/SETUP.md` and `docs/VERIFICATION.md`.

## Frontend Command

From `workspace/vscode/ems-forword`:

```powershell
npm test
npm run build
```

## Runtime Tools

From the repository root:

```powershell
node --test scripts/local-runtime.test.mjs scripts/ai-decision-preflight.test.mjs
```

## Reporting Format

Record:

- command;
- working directory;
- pass/fail;
- important warnings;
- reason if not run.

## Must Not

- Do not claim tests passed if only compilation or file review was done.
- Do not skip validation silently.
- Do not treat unrelated warnings as fixed unless actually addressed.
