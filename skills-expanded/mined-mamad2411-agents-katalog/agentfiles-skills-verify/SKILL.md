---

## name: verify
description: Run the project’s quality gates, map results to spec acceptance criteria, and produce verification_report.json with evidence and severities.

# Verify

### When to use

- Verifier Agent after a change is claimed ready for review.
- You need a **pass/fail** tied to evidence, not gut feel.

### Part A — Automated gates (use the repo’s real commands)

Run what this repository already defines (examples—substitute from `package.json` scripts, `Makefile`, CI config):


| Layer | Typical commands (pick what exists)                                                                              |
| ----- | ---------------------------------------------------------------------------------------------------------------- |
| Lint  | `npm run lint`, `ruff check`, `php -d detect_unicode=0 $(which php-cs-fixer) fix --dry-run`, `golangci-lint run` |
| Types | `npm run typecheck`, `tsc --noEmit`, `phpstan`, `mypy`                                                           |
| Tests | `npm test`, `php artisan test`, `pytest -q`, `go test ./...`                                                     |


Record in `verification_report.json` → `checks`: `pass` | `fail` | `not_run` (only use `not_run` if the project truly has no check; say why in a finding).

### Part B — Spec coverage matrix

1. Open `spec.json` → `acceptance_criteria`.
2. For each **AC id**, list **evidence**:
  - test name + file, or
  - manual repro steps + screenshot/log (if no test yet—flag as **risk**).
3. Any AC with **no evidence** → finding (usually **high** until tests exist for must-have behavior).

### Part C — Severity rubric (use in every finding)


| Level        | Meaning                                              | Example                               |
| ------------ | ---------------------------------------------------- | ------------------------------------- |
| **critical** | Security hole, data loss, auth bypass, payment wrong | Missing auth check on mutating route  |
| **high**     | Wrong behavior vs spec, crash on main path, CI red   | AC fails, 500 on happy path           |
| **medium**   | Edge case, flaky test, incomplete error handling     | Wrong message body, race in rare case |
| **low**      | Polish, copy, minor a11y                             | Typo in validation message            |


Every finding needs `**owner`** (team or role), `**impact**`, `**evidence**`, `**remediation**`.

### Output

- `verification_report.json`: `status`, `build_ref`, `checks`, `findings`, `metadata` (see schema).

### Anti-patterns

- “Looks fine” without **AC → evidence** mapping.
- Downgrading **high** to please schedule—severity describes **user/system risk**, not comfort.