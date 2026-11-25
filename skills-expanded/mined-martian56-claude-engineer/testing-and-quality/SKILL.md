---
name: testing-and-quality
description: Use throughout the build and before claiming any phase or the project "done", to run the four mandatory quality gates and verify them with evidence. Covers the test pyramid, Playwright + Chrome DevTools browser verification, WCAG AA, and the commit/finish gate wiring.
---

# Testing & Quality

**Announce at start:** "I'm using claude-engineer:testing-and-quality to enforce the four quality gates."

## Iron Law
**No "done" without all four gates passing, verified by fresh evidence.** (Pairs with
`superpowers:verification-before-completion` - assertions follow evidence, never precede it.)

## The four gates (exact pass/fail commands; exit 0 = pass)
1. **Tests + coverage** - FE `vitest run --coverage`; BE `pytest --cov=app --cov-fail-under=80`.
2. **E2E + zero console errors** - `playwright test` (specs include a console-error/`pageerror` fixture and assert no 4xx/5xx on key routes). Drive flows and confirm every button/screen works via the Playwright + Chrome DevTools MCPs.
3. **Accessibility (WCAG AA)** - `playwright test a11y/` using `@axe-core/playwright` with tags `wcag2a,wcag2aa,wcag21aa,wcag22aa`; assert zero violations. Manual keyboard/focus spot-checks too.
4. **Strict types + lint clean** - `tsc --noEmit && eslint . && prettier --check . && ruff check . && ruff format --check . && mypy app`.

## The gate runner + commit gate
- Scaffold `scripts/quality-gate.mjs` from `templates/quality-gate.mjs`. It runs all four gates and writes
  `.claude-engineer/quality-gate-status.json` (`{ allPass, results }`).
- The claude-engineer **PreToolUse(Bash) hook blocks `git commit`** unless that file shows `allPass: true`.
  So: run `node scripts/quality-gate.mjs` → fix failures → commit. Intentional bypass: `git commit --no-verify`.
- The same four commands are the **finish** condition and the **CI** merge condition (`claude-engineer:ci-cd-pipeline`).

## Browser verification (MCPs - BYO install)
- **Chrome DevTools MCP** - capture/assert zero console errors per screen, Lighthouse audits, network-failure checks.
- **Playwright MCP** - drive real flows; confirm interactions actually work.
Install per `templates/recommended-mcps.md`.

**Full detail (test pyramid, coverage targets, Playwright setup, the console-error fixture, axe usage, exact commands):**
read `references/testing-and-gates.md` on demand.

## Red flags - STOP
- Claiming "done"/"passing" without re-running the gate now.
- Committing with a failing/stale gate (use `--no-verify` only with explicit reason).
- Treating console warnings/errors as acceptable - the E2E gate requires zero.
