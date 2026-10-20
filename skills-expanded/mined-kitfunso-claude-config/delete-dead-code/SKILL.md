---
name: delete-dead-code
description: Find and delete dead code using ruff and vulture (Python) or equivalents
disable-model-invocation: true
---

Find and delete dead code in the codebase. Vibe coding leaves unused imports, functions, variables, and entire modules behind. Clean them out.

## Python projects

Run in this order:

1. **Ruff: unused imports, variables, and simple dead code**
   ```bash
   ruff check --select F401,F841,F601,F602,F811,F821,F823 --fix .
   ```
   - `F401`: unused imports
   - `F841`: unused local variables
   - `F811`: redefinitions
   - Auto-fixes most issues

2. **Vulture: unused functions, classes, attributes, methods**
   ```bash
   vulture . --min-confidence 80
   ```
   - 80+ confidence is usually safe to delete
   - Review 60-80 range manually (may be called via reflection, plugins, fixtures, or public API)
   - Add genuinely-used-but-dynamic items to a `.vulture_whitelist.py`

3. **Unreachable code**
   ```bash
   ruff check --select B018,ARG001,ARG002,ARG003,ARG004,ARG005 .
   ```

4. **Orphan files**: use `git log --diff-filter=A` to find files never referenced after creation

## TypeScript/JavaScript projects

1. **ts-prune or knip**
   ```bash
   npx knip
   ```
   - Reports unused files, exports, dependencies, types

2. **ESLint**
   ```bash
   npx eslint --rule "no-unused-vars: error" --rule "@typescript-eslint/no-unused-vars: error" --fix .
   ```

3. **depcheck** for unused npm dependencies
   ```bash
   npx depcheck
   ```

## Rules for deletion

- **Delete, don't comment out.** Git has history. Commented-out code is worse than deleted code.
- **One commit per category.** Separate commits for unused imports, unused functions, unused deps: makes review and rollback easy.
- **Run the full test suite after each batch.** If tests break, something was called dynamically. Investigate before re-deleting.
- **Watch out for false positives:**
  - Code called via reflection, string-based dispatch, or plugin loaders
  - Public API surface consumed by downstream users
  - Fixtures, conftest.py contents, framework hooks
  - CLI entry points registered via setup.py/pyproject.toml
  - Template-referenced functions (Jinja, Django templates)
  - Dynamically imported modules
- **Whitelist the ambiguous.** Don't delete things you're unsure about: add them to a whitelist and move on.

## Before declaring done

- [ ] All three tools ran clean (or flagged items are whitelisted with reason)
- [ ] Full test suite passes
- [ ] Application starts and basic smoke test passes
- [ ] Commits are grouped by category, not one mega-commit
- [ ] Report: X imports, Y functions, Z files, N lines removed

## Output format

Put this block in the PR description or the last commit body. In chat, give the
total lines removed, the test result and anything whitelisted, in prose.

```
## Dead code removed

| Category          | Count | Notes |
|-------------------|-------|-------|
| Unused imports    |   42  | ruff --fix auto-applied |
| Unused functions  |    8  | vulture >80% confidence |
| Unused files      |    3  | orphan modules, no inbound imports |
| Unused deps       |    5  | depcheck / pip-audit |
| Total lines       |  380  | |

## Whitelisted (kept)

- `handlers/webhook_stripe.py::_refund_callback`: called via Stripe webhook string dispatch
- ...

## Test results

- pytest: 312 passed
- app smoke test: ok
```

---

Target: $ARGUMENTS

If no target specified, run against the current working directory.
