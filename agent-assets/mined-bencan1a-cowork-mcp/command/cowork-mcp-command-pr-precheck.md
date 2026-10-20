# PR Pre-Check

Run a full pre-push validation suite: format, lint, typecheck, security scan, and tests. Automatically fix issues found where possible, then report a summary.

## What To Do

Execute each phase sequentially. If a phase fails, fix the issues before moving to the next phase.

Track progress using the TodoWrite tool with these tasks:
1. Format and lint
2. Type check
3. Security scan
4. Run tests
5. Summary report

### Phase 1: Format & Lint

Run these **in parallel** since they are independent:

```bash
ruff format --check .
```

```bash
ruff check .
```

**If format check fails:**
- Run `ruff format .` to auto-fix formatting
- Re-run `ruff format --check .` to confirm

**If lint fails:**
- Run `ruff check --fix .` to auto-fix what it can
- Manually fix remaining errors
- Re-run `ruff check .` to confirm

### Phase 2: Type Check

```bash
mypy config.py auth/ graph/ server.py run_auth.py
```

**If typecheck fails:**
- Spawn a **general-purpose** subagent to fix the type errors. Provide the full error output.
- After the agent fixes, re-run mypy to confirm.

### Phase 3: Security Scan

```bash
bandit -r config.py auth/ graph/ server.py run_auth.py
```

Review any findings. `B101` (assert_used) and `B603`/`B607` (subprocess) are already suppressed in pyproject.toml for legitimate uses. Flag any new HIGH severity findings.

**If new HIGH severity findings exist:**
- Review each finding carefully — bandit has false positives
- If it's a real issue, fix it
- If it's a false positive, add `# nosec: <CODE>` with a justification comment

### Phase 4: Tests

```bash
pytest
```

This runs all tests with coverage. The coverage report will show current coverage.

**If tests fail:**
- Read the failure output carefully
- Spawn a **general-purpose** subagent to diagnose and fix failing tests. Provide the full test output and the test/source file paths.
- After the agent fixes, re-run pytest to confirm.
- If coverage drops below 80%, flag it (don't block on this, but note it).

### Phase 5: Summary Report

After all phases complete, produce a summary report:

```
## PR Pre-Check Report

### Results

| Phase          | Status          | Details                    |
|----------------|-----------------|----------------------------|
| Format         | PASS/FAIL/FIXED | (notes if fixed)           |
| Lint           | PASS/FAIL/FIXED | (notes if fixed)           |
| Type Check     | PASS/FAIL/FIXED | (notes if fixed)           |
| Security Scan  | PASS/FAIL/FIXED | (notes if fixed)           |
| Tests          | PASS/FAIL/FIXED | (coverage: X%)             |

### Changes Made
(List every file modified to fix issues, with a one-line description of what was changed)

### Verdict
- CLEAN: All phases passed on first run. Ready to push.
- FIXED: Issues were found and automatically fixed. Review the changes above, then push.
- BLOCKED: Some issues could not be automatically resolved. See details above.
```

Status values:
- **PASS** — passed on first run, no changes needed
- **FIXED** — failed initially but was automatically fixed
- **FAIL** — could not be automatically fixed (explain why)

## Important Notes

- Always run phases sequentially (format/lint → typecheck → security → tests)
- Format and lint within Phase 1 can run in parallel
- When spawning fix agents, provide them with the FULL error output — don't truncate
- After any fix, always re-run the check to verify the fix worked
- Do NOT commit any changes — leave that to the user
- If there are no changes to check (no modified files in git), say so and skip
