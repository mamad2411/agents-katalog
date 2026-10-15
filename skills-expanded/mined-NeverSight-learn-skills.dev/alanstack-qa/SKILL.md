---
name: alanstack-qa
description: "Verify a change against the repo's own scripts: lint + typecheck + smallest relevant tests, broadened when touching shared behavior. Reads package.json scripts, fans out filtered in Bun workspaces, reports what ran and what changed. Use when user says 'verify', 'qa this', 'run check', 'test it', '/alanstack-qa', or after coding work needs proof of correctness before commit/PR."
---

Verify the change actually does what it should. Run the repo's own scripts. Report what ran, what failed, what changed.

## Operating loop

1. **Identify scope.** What files changed (`git status --short`, `git diff --name-only`). Which package(s) own them.
2. **Read the repo's scripts.** `package.json` at root and at each touched package. Use the repo's actual `typecheck` / `lint` / `test` / `check` names; do not invent commands.
3. **Run the narrowest relevant suite first.** Touched one package? `bun run --filter <pkg> typecheck && bun run --filter <pkg> lint && bun test <pkg-path>`. Don't run the entire monorepo unless the change is shared.
4. **Broaden when needed.** Shared module, generated client, db migration, public API, lockfile change → run root-level `bun check` (or its equivalent).
5. **Report concrete results.** Pass/fail per step, test counts, any unexpected output. Don't claim "working" without evidence.

## What "verify" means by change type

| Change | Minimum | Broaden when |
|---|---|---|
| One file in one package | `tsc --noEmit` for that package + targeted `*.spec.ts` | spec didn't exist before — add one first |
| Multiple files, one package | package `check` script (typecheck + lint + test) | any file re-exported from the package |
| Multiple packages | root `check` script | always |
| Public API of a published package | root check + a downstream consumer's typecheck if reachable locally | always |
| `package.json` deps / lockfile | `bun install && bun check` from root | always |
| Generated client (OpenAPI, proto) | regen via existing script, then root check | always |
| DB schema / Drizzle migration | run migration locally + the package's integration tests + targeted handler smoke | always |
| Bun.serve / Hono route | start the dev server, hit the route, verify response shape — **do not** claim done from typecheck alone | always |
| Frontend visible behavior | start dev server, exercise the path in the browser, screenshot when relevant — typecheck/tests do not prove UX | always |

## Patterns Alan's repos use

| Repo shape | Verify command |
|---|---|
| Bun workspace, single package | `bun run check` (often = typecheck + lint + test) |
| Bun workspace, monorepo | `bun typecheck && bun lint && bun test` from root, or `bun run --filter '<scope>/*' typecheck` for one scope |
| Python sidecar (FastAPI / inference / ML) | run Bun checks AND `uv run pytest` / `pytest` in the Python package |
| Frontend that already uses vitest | `bun run --filter <pkg> test` (vitest under the hood) |
| E2E | `bun run --filter <pkg> test:e2e` or Playwright — only when the change is user-facing |

Match the existing script names. Do not invent `bun test:everything` if the repo only has `bun test`.

## Reporting

Output a tight summary:

```
qa: <pkg-or-scope>
  typecheck: ✓ (1.2s)
  lint:      ✓ (0.1s)
  test:      ✓ 44 passed, 0 failed, 10 spec files (18ms)
verdict: ready
```

If something fails, lead with the failing step and the first error line:

```
qa: @onrails/result
  typecheck: ✗ src/compat/neverthrow.ts(259,36): TS2322 Result<unknown, unknown> not assignable to Result<T, unknown>
  lint:      not run (typecheck failed)
  test:      not run
verdict: needs fix in src/compat/neverthrow.ts:259
```

When manual UI / server verification is required and not run, **say so explicitly**:

```
verdict: typecheck + tests green. Browser verification not run — feature is UI-visible; cannot claim done from this layer.
```

## What not to do

- Don't claim "tests pass" without showing the count.
- Don't run `npm test` or `pnpm test` in a Bun repo.
- Don't run the full monorepo suite for a one-line typo fix in a leaf package.
- Don't skip lint to make output shorter; it catches real issues.
- Don't run with `--no-verify`, `--no-gpg-sign`, or any hook-skipping flag unless the user explicitly asked.
- Don't run destructive scripts (`db:wipe`, `clean`, `reset`) as part of verification.
- Don't conclude success from a typecheck alone for UI-visible or HTTP-route changes — exercise the path.

## Companion skills

- [alanstack](../alanstack/SKILL.md) — full principles
- [alanstack-review](../alanstack-review/SKILL.md) — find issues before running tests
- [alanstack-refactor](../alanstack-refactor/SKILL.md) — moves to apply when QA flags a violation
- [alanstack-commit](../alanstack-commit/SKILL.md) — once QA is green
