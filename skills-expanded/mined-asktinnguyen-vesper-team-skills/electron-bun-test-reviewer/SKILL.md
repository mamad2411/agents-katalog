---
name: electron-bun-test-reviewer
description: This skill should be used when reviewing, debugging, and improving Electron Bun tests in the Vesper repository, especially for typecheck failures, test-discovery bleed into release artifacts, runtime import/export mock mismatches, and flaky mock.module lifecycles.
---

# Electron Bun Test Reviewer

## Overview

Review failing Bun type/tests in `apps/electron` and `packages/shared`, classify failure mode quickly, apply the smallest durable fix, and verify with deterministic command sequences. Prioritize strict TypeScript correctness, mock isolation, and repeatable test discovery.

## Trigger Cues

Activate this skill when requests include:
- "fix bun test failures" in Electron code
- "typecheck passes but tests fail" or vice versa
- runtime import/mocking errors such as missing named exports (`ipcMain`, resolver helpers, etc.)
- Bun discovering packaged output (`release/*`, `dist/*`) instead of `src/*` tests
- flaky behavior caused by cross-file `mock.module` state

## Setup Prerequisites

Use the repository’s documented setup flow before debugging tests:
1. Install Bun and Node 18+.
2. Install dependencies at repository root.
3. Ensure `.env` is configured from `.env.example` when required by integration tests.
4. Confirm baseline typecheck runs.

Use:
```bash
curl -fsSL https://bun.sh/install | bash
node -v
cd /Users/tinnguyen/vesper
bun install
bun run typecheck:all
```

References:
- `docs/developer/development-setup.md`
- `apps/electron/package.json`
- `package.json`

## Workflow
1. Reproduce the exact failing signal first.
Run targeted tests first (avoid broad discovery while triaging):
```bash
cd apps/electron
bun test src/main/__tests__/personas.test.ts src/main/__tests__/sessions.unexpected-exit.test.ts
```
2. Classify the failure mode before patching.
Use the mapping in `references/failure-patterns.md` to classify:
- strict TypeScript issues in tests
- runtime import/export mismatch
- mock surface mismatch
- test discovery scope bleed
- mock lifecycle race between files
3. Apply the smallest fix that stabilizes behavior.
Prefer test changes when the break is test brittleness; do not change production behavior to satisfy weak assertions.
4. Check mock surfaces before rerunning broad suites.
Use:
```bash
./skills/electron-bun-test-reviewer/scripts/audit-main-test-mocks.sh
```
Use strict mode when closing out a large test-hygiene pass:
```bash
./skills/electron-bun-test-reviewer/scripts/audit-main-test-mocks.sh --strict
```
5. Verify in layers.
Run:
```bash
cd /Users/tinnguyen/vesper
bun run typecheck:all
cd apps/electron
bun test <same targeted files>
```
Expand test scope only after targeted tests pass.
6. Run quick end-to-end verification when triage scope is complete.
Use:
```bash
./skills/electron-bun-test-reviewer/scripts/run-electron-bun-checks.sh
```
7. Document what changed and why.
Include:
- failure signature
- root cause class
- exact files touched
- verification commands and outcomes

## Fix Rules

- Keep fixes local to failing scope first (specific test files, local mocks, local helper typing).
- For Bun discovery leaks, constrain discovery at workspace level.
Path: `apps/electron/bunfig.toml`
```toml
[test]
root = "./src"
```
- For shared mocked modules, ensure mocked export surface includes all named exports imported by downstream modules in the same test run.
- For `mock.module('electron', ...)`, include commonly imported members (`app`, `ipcMain`, `BrowserWindow`, `nativeImage`) when tests import `sessions.ts` or other main-process modules.
- Avoid `mock.restore()` in `afterEach` when module-level mocks are required across imports in one file; prefer `afterAll`.
- Keep strict-null safety in tests explicit with local guards instead of broad `any`.
- Prefer source-backed command and config paths only; do not invent workflow steps.

## Script Toolkit

Run script-based checks for deterministic reviews:
- `scripts/audit-main-test-mocks.sh`
Purpose: detect likely missing exports in shared mocks (`workspace-path-resolver`, `electron`) across `apps/electron/src/main/__tests__` (warnings by default, strict failure mode available).
- `scripts/run-electron-bun-checks.sh`
Purpose: run the standard verification sequence (`typecheck:all`, targeted Electron tests, targeted shared tests).

## Verification Gates

Do not declare completion until all relevant gates pass:
1. `bun run typecheck:all` succeeds from repo root.
2. Targeted failing Electron tests pass together (not only individually).
3. If touched, related shared tests pass:
`packages/shared/src/agent/__tests__/artifact-tools.test.ts`
`packages/shared/src/agent/__tests__/code-executor.test.ts`
4. Test discovery remains scoped to source (`apps/electron/bunfig.toml`).

## References

Load as needed:
- `references/failure-patterns.md` for signature-to-fix mapping
- `references/command-recipes.md` for reproducible command sequences
- `references/repo-map.md` for source-backed file/command locations
