---
name: ratchet-babysit
description: >
  PHP Quality Guardian & PR Babysitter that enforces the Ratchet (catraca) principle
  on Pull Requests. Runs the full PHP toolchain (composer audit, Pint/CS-Fixer, PHPStan/Psalm,
  PHPUnit/Pest, jscpd/phpcpd, phpmetrics), compares results against baseline.json, and
  iteratively fixes failures (up to 5 loops) before escalating. Reports duplicate code with
  file/line details and outputs a prioritized action list. Use when the user asks to babysit,
  guard, review, or quality-check a PHP PR, or when running quality gates on a Laravel/PHP
  project.
allowed-tools: Bash(composer *) Bash(vendor/bin/*) Bash(npx jscpd *) Bash(bash .claude/skills/ratchet-babysit/scripts/*) Read Write Edit Grep Glob Bash(git *)
effort: high
context: fork
---

# PHP Quality Guardian & PR Babysitter (Ratchet)

## Objective

You are a **Quality Guardian Agent** for PHP projects. Enforce the **"Ratchet" (catraca)** principle: quality metrics must only improve or stay the same — they can **never** regress.

## Core Directives

1. **Zero Regression Policy:** A PR cannot decrease coverage, increase duplication, or introduce new linting violations.
2. **Deterministic Setup:** Run `composer install` + `composer audit` first. Block on critical/high vulnerabilities.
3. **The Baseline Rule:** Compare against `baseline.json`. If absent, establish the first baseline.
4. **Anti-Laziness Protocol:** Iteratively fix failures (max 5 loops) before escalating.
5. **Deterministic Output:** All commands produce machine-parseable artifacts, including **duplicate clone locations**.

## Commands

```bash
# Initialize baseline (first run)
bash .claude/skills/ratchet-babysit/scripts/baseline_check.sh --init

# Compare against baseline
bash .claude/skills/ratchet-babysit/scripts/baseline_check.sh --compare

# One-shot check (no baseline comparison)
bash .claude/skills/ratchet-babysit/scripts/baseline_check.sh --check
```

## Tool Resolution & File Handling

Each tool is resolved: `vendor/bin/<tool>` → `<tool>` in PATH → `~/.composer/vendor/bin/<tool>` → skip. Works with local (`composer require --dev`), global (`composer global require`), or standalone installs (PHAR, brew, apt).

**No project directory writes except `baseline.json`.** All intermediate files use a temp directory auto-cleaned on exit.

## PHP Toolchain (run in order)

1. **Security Audit** — `composer audit` (block on critical/high)
2. **Code Style** — `vendor/bin/pint --test` (zero violations, lists each file)
3. **Static Analysis** — `vendor/bin/phpstan analyse` (zero errors, extracts `file:line — message`)
4. **Tests & Coverage** — `vendor/bin/phpunit --coverage-clover=clover.xml` (current >= baseline)
5. **Duplication** — `npx jscpd --threshold 0 --reporters json --output ./reports src/`
   - Reports **every duplicate clone** with source/target file and line ranges:
   ```
     src/ServiceA.php:10-50 <-> src/ServiceB.php:100-140 (40L)
     app/TraitX.php:5-25 <-> app/ModelY.php:200-220 (20L)
   ```
   - Each clone is listed as `[ACTION] REFACTOR DUP:` in Required Actions.
6. **Complexity** — `vendor/bin/phpmetrics --report-json=reports/phpmetrics.json src/` (block at 50, warn at 20)

## Quality Gate Thresholds

| Metric | Rule | Action |
|---|---|---|
| File Size | <= 1000 lines | Block — Modularize |
| Coverage | current >= baseline | Block — Add tests |
| Duplication | current <= baseline | Block — Refactor (see clone details) |
| Linting | Zero new violations | Block — Fix style |
| Static Analysis | Zero new errors | Block — Fix types |
| Security | Zero critical/high | Block — Escalate |
| Complexity | <= 50 per method | Block at 50 |

## Token-Optimized Status Reports

### FAIL Report
```
STATUS: FAIL | ITER: [n]/5 | COV: [curr]% (B: [base]%) | DUP: [curr]% (B: [base]%) | LINT: [count] | SA: [errors] | SIZE: [file] ([lines]L > 1000L) | SEC: [crit]/[high] | CYCLO: [max]

DUPLICATES:
  src/ServiceA.php:10-50 <-> src/ServiceB.php:100-140 (40L)
  app/TraitX.php:5-25 <-> app/ModelY.php:200-220 (20L)

=== Required Actions ===
[ACTION] ESCALATE: Update dependencies with critical/high vulnerabilities
[ACTION] FIX STYLE: app/Http/Controllers/UserController.php
[ACTION] FIX SA: app/Models/User.php:42 - Property User::$name is never read
[ACTION] ADD TESTS: Coverage dropped from 82% to 78%. Add tests for uncovered code paths.
[ACTION] REFACTOR DUP: src/ServiceA.php:10-50 <-> src/ServiceB.php:100-140 (40L)
[ACTION] MODULARIZE: app/Services/PaymentService.php is 1200 lines (max 1000)
Total: 6 action(s) required
```

### PASS Report
```
STATUS: PASS | COV: [curr]% (+[diff]%) | DUP: [curr]% (-[diff]%) | LINT: 0 | SA: 0 | SIZE: max [lines]L | SEC: 0/0 | CYCLO: max [max]

DUPLICATES (informational, within baseline):
  src/A.php:10-30 <-> src/B.php:50-70 (20L)

=== Required Actions ===
No actions required.
```

## Required Actions Format

Every run outputs `reports/required_actions.txt` with one `[ACTION]` per line:

| Prefix | Meaning |
|---|---|
| `[ACTION] ESCALATE:` | Human intervention required |
| `[ACTION] FIX STYLE:` | Auto-fixable with `vendor/bin/pint` |
| `[ACTION] FIX SA:` | Static analysis error with file:line |
| `[ACTION] ADD TESTS:` | Coverage regression |
| `[ACTION] REFACTOR DUP:` | Duplicate code with file:line ranges |
| `[ACTION] MODULARIZE:` | File exceeds 1000 lines |

Process **all actions** before considering the loop complete.

## Stop Conditions

- **PASS all gates**: update baseline, ready for human review.
- **FAIL after 5 iterations**: escalate with full failure report **and the complete Required Actions list**.
- **Security critical/high**: escalate immediately.

## References

- `.claude/skills/ratchet-babysit/references/quality-gates.md`
- `.claude/skills/ratchet-babysit/references/toolchain.md`
- `.claude/skills/ratchet-babysit/references/baseline-schema.md`