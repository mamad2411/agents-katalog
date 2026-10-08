---
name: blt
description: >
  Build-Test-Lint health check. Detects build errors, lint violations, and
  test failures in the current project, fixes them, then outputs a conventional
  commit message summarizing all changes. Trigger: user runs /btl or asks to
  "check build/tests/lint" before committing.
---

# BTL Skill — Build · Test · Lint

Run this skill when the user invokes `/btl` or asks to verify the project is healthy before committing.

## Goal

Leave the repo in a green state: builds clean, linter happy, tests passing. Then produce a single conventional commit message (≤72 chars subject) summarizing all current changes.

---

## Step 1 — Detect tooling

Sniff the project to find which tools are available. Check `package.json` scripts, `Makefile`, `pyproject.toml`, `Cargo.toml`, etc.

```bash
# Examples — adapt to what exists:
cat package.json | grep -E '"(build|lint|test|typecheck|check)"'
cat Makefile 2>/dev/null | grep -E '^(build|lint|test):'
cat pyproject.toml 2>/dev/null
```

Priority order for each phase:
- **Build**: `npm run build` / `cargo build` / `make build` / `tsc --noEmit` / `python -m py_compile`
- **Lint**: `npm run lint` / `eslint` / `ruff check` / `clippy` / `make lint`
- **Test**: `npm test` / `pytest` / `cargo test` / `make test`

If no script exists for a phase, skip it and note that.

---

## Step 2 — Run each phase, fix failures

### Build

Run the build command. If it fails:
- Read the error output carefully
- Fix the root cause in source files
- Re-run until clean

### Lint

Run the linter. If violations exist:
- Auto-fix where safe (`eslint --fix`, `ruff check --fix`, `cargo clippy --fix`)
- Manually fix remaining issues
- Re-run until clean

### Test

Run the test suite. For each failure:
1. **Failing test** — fix the source code (or the test if the test itself is wrong)
2. **Missing coverage** — if a new function/module exists with no tests, add minimal tests
3. **Stale tests** — if tests reference deleted code, remove or update them
4. Re-run until all pass

**Do not delete tests just to make the suite green.** Only remove tests that are genuinely obsolete (testing deleted functionality).

---

## Step 3 — Summarize changes via `git diff`

```bash
git diff HEAD --stat
git diff HEAD --name-only
```

Read the staged + unstaged diff to understand what changed across the whole branch/working tree.

---

## Step 4 — Output commit message

Produce one conventional commit message:

```
<type>(<scope>): <subject>
```

Rules:
- **type**: `feat` | `fix` | `chore` | `refactor` | `test` | `docs` | `style` | `perf` | `ci`
- **scope**: short noun for affected area (optional but preferred), e.g. `auth`, `api`, `ui`
- **subject**: imperative mood, no period, ≤72 chars total for the whole first line
- If multiple types apply, pick the highest-impact one (`feat` > `fix` > `refactor` > `chore`)

### Examples

```
feat(auth): add JWT refresh token rotation
fix(api): handle null response from upstream payment service
chore(deps): upgrade eslint to v9 and fix new rule violations
refactor(db): extract query builder into standalone module
test(cart): add unit tests for discount edge cases
```

---

## Output format

After all phases pass, reply with:

```
Build ✓  Lint ✓  Tests ✓

<conventional commit message here>
```

If any phase was skipped (no tooling found), note it:

```
Build ✓  Lint — (no linter found)  Tests ✓

fix(parser): correct off-by-one in token boundary detection
```

---

## Caveats

- Never skip or bypass hooks (`--no-verify`)
- Never delete tests to force green — fix the code or update the test
- If a fix requires a breaking change, note it in the commit body (separate line after blank line): `BREAKING CHANGE: <description>`
- If the project has no git changes at all, say so and exit
