---
name: fintech-audit
description: >-
  Use when asked to audit, review, check or harden a repository's money code, or before merging a
  change that touches payments, balances, ledgers, webhooks, reconciliation, accounting sync or
  personal and card data. Runs the deterministic lint that ships with this skill, confirms each hit
  by reading the code, applies the review checklists of the relevant fintech skills, and reports
  findings with file and line, the rule broken, the fix and the test to add. Triggers on "audit my
  payments code", "review this PR, it touches billing", "is our money handling safe", "check this
  repo with fintech-skills". Not a replacement for a security audit or a penetration test; it covers
  correctness and operability of money handling.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Fintech audit

The entry point for the pack. Point it at a repository or a diff and get a ranked list of money
defects with the rule each one breaks, the fix and the test that proves the fix. It reads code; it
never changes it unless the request says so after the report.

## When to use

- "Audit this repo's money code", "review our payments module", "is this safe to merge".
- A pull request that touches amounts, balances, charges, refunds, payouts, webhooks, ledgers,
  reconciliation, accounting integrations, or fields such as CPF, CNPJ, card, account.
- Onboarding to a codebase that moves money, before the first change.

## How to run it

1. **Lint first.** Run the script that ships with this skill on the repository root or the changed
   files:

   ```sh
   python3 <skill-dir>/scripts/money_lint.py <path> [--json]
   ```

   It prints findings with a code, a file and line, the matched text, the skill and the rule it
   maps to. Codes: `FLOAT_MONEY`, `DIV100`, `ROUND_MONEY`, `RATE_FLOAT`, `RANDOM_IDEMPOTENCY`,
   `BALANCE_UPDATE`, `BODY_LOG`, `PARSED_BODY_VERIFY`, `CVV_FIELD`, `DIGITS_ONLY_CNPJ`,
   `WALL_CLOCK_MONEY`, `PAID_ON_ISSUE`.
2. **Confirm every hit by reading the code around it.** A lint line is a lead, not a finding.
   Drop the hit when the surrounding code shows it is not money (a `/ 100` on a percentage, a
   `uuid4()` for a log id). Report only what you confirmed, and say what you dropped.
3. **Map the repository to the skills.** Grep for processor clients (`stripe`, `adyen`, `pagarme`,
   `asaas`, `efi`), webhook routes, `balance` columns, `UPDATE` statements on money tables,
   accounting clients (`quickbooks`, `xero`), classification code, `cpf`, `cnpj`, `card`, `cvv`,
   logging near payment handlers. For each area present, read the matching skill
   (`money-arithmetic`, `double-entry-ledger`, `idempotent-payments`, `webhook-handling`,
   `reconciliation`, `accounting-sync`, `transaction-classification`, `pii-and-card-data`,
   `audit-trail`, `interest-and-amortization`, `brazil-payment-rails`, `money-tests`) and walk its
   **Review checklist** against the code.
4. **Run the vectors when there is a money module.** Point the matching vector suite at it
   (for example `MONEY_SOLUTION=src/money.py pytest <skill-dir>/../money-arithmetic/evals/vectors`)
   and report failures as findings.
5. **Write the report** in the format below. Rank by consequence: double charge and lost money
   first, then data exposure, then drift and operability.

## Report format

```
# Money audit: <repo or PR> at <sha>

## Findings (ranked)
| # | Severity | Where | Rule | What happens | Fix | Test to add |
|---|----------|-------|------|--------------|-----|-------------|
| 1 | critical | src/charges.py:14 | idempotent-payments 4 | new key per retry; a timeout double charges | derive the key from the order id | same key twice -> one charge |

## Checked and clean
- <area>: <what was checked> (<skill> checklist)

## Not checked
- <area or file>: <why> (no access, generated code, out of scope)

## Next three changes
1. <smallest change that removes the most consequence>
2. ...
3. ...
```

Rules for the report:

- Every finding has a file and line, the skill and rule number, and a test. No finding without
  a test is complete.
- Severity: `critical` (money lost, duplicated or exposed now), `high` (will drift or break at
  month end or on a retry), `medium` (operability: no replay, no reconciler, no audit),
  `low` (style that hides risk, such as a float in a display helper).
- Numbers over adjectives: "3 endpoints without idempotency keys", not "several".
- Say what you did not check. An audit that claims completeness is wrong.
- Do not edit code during the audit. If the request also asks for fixes, finish the report
  first, then fix in the order of the ranking, one finding per change, each with its test.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent. An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". This skill
reports and does not edit; the rewrite rule in the domain skills applies when the user asks for a
review of code they own.

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- The lint on the planted fixture repository finds every planted defect by code and file
  (`evals/vectors/test_lint.py`), and reports none on the clean sample.
- A report produced on the fixture names at least the planted defects, each with a test.
- Reference vectors: `skills/fintech-audit/evals/vectors/test_lint.py` with `AUDIT_LINT`
  pointing at your lint script.

## Review checklist

- Did every finding come from reading the code, not from the lint line alone?
- Is there a test to add for each finding?
- Which skills' checklists were walked, and which areas were not checked?
- Are the three next changes the ones that remove the most consequence?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Pasting lint output as the report | False positives, no severity, no tests | Confirm, rank, add tests |
| Fixing while auditing | Scope creeps, findings get lost | Report first, then fix one by one |
| "Looks fine" without a not-checked list | Hidden gaps | Always list what was not checked |
| Only grepping, no vectors | Logic bugs survive | Run the vector suites on the money module |
