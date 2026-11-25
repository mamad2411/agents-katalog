---
name: engagement-retest
description: Plan and execute a pentest retest — re-scope, re-execute the validation steps from prior findings, detect regressions, and write the retest report. Use when the user mentions retest, re-test, remediation validation, regression coverage, "verify the fixes", "validate remediation", retest scoping, retest report, posture trajectory, or compares "before vs after" findings.
---

# Engagement Retest

Drive a focused retest using the prior engagement's findings as the test plan.

## Library root

`$PENTEST_LIBRARY` — caminho absoluto deste repositório clonado (definido pelo instalador; veja INSTALL.md).

Methodology: `00-engagement/04-retest-and-remediation.md`.
Template: `templates/retest-report-template.md`.

## How to operate

1. **Inventory prior findings** — collect the prior engagement's findings (IDs, severity, status, asset, methodology used). For each, the validation steps live in the prior `Reproduction steps` and per-library checklist item.
2. **Re-scope window** — confirm:
   - Which findings are in scope for this retest (typically all High+ closed/mitigated, plus Medium fixes).
   - Whether the asset surface has changed (new endpoints, new accounts, new build) — material change shifts retest into a delta-pentest.
   - Test perspective (which credentials / role / network position to re-use).
   - Time window + blackout windows.
3. **Per-finding execution** — for each finding:
   1. Re-read the original `Reproduction steps`.
   2. Re-execute exactly. Record the new request/response.
   3. Classify the outcome:
      - **Closed** — exact reproduction no longer succeeds.
      - **Partially mitigated** — original payload blocked, but a near-equivalent variant still succeeds (document the variant).
      - **Open** — still reproducible.
      - **Regressed** — was Closed at some point, now Open again.
      - **Mitigated by compensating control** — root cause unfixed, but a control (WAF, MFA, network ACL) prevents exploitation; document residual risk.
   4. For variants: walk the matching library checklist item's `How to test` block to broaden test coverage in the same vulnerability class.
4. **Regression sweep** — for each fix, test the *adjacent* attack surface (same parameter family, same role boundary, same trust edge). A correct fix at one entry point rarely covers siblings.
5. **Posture trajectory** — quantify before/after counts by severity; flag categories of finding that recurred (indicates process gap, not just a missed patch).
6. **Report** — fill `templates/retest-report-template.md`:
   - Header: prior engagement reference, retest scope, retest window.
   - Per-finding table: ID, prior severity, new status, evidence reference, residual risk.
   - Regression / new finding section (anything found during sibling sweep).
   - Posture trajectory + recommendations (process-level, not just patch-level).

## When NOT to use

- New engagement (no prior findings to validate) → use the type-specific `pentest-*` skill plus `engagement-scoping`.
- Single-finding sanity check → `pentest-checklist-lookup` to re-read the methodology, then re-run manually; full retest skill is overkill.

## Pre-conditions

- Prior engagement deliverable (findings list + reproduction steps).
- Client confirmation that remediation is complete and ready to validate.
- Same access posture as prior engagement (where possible).

## OPSEC

- Avoid re-running destructive payloads on production unless explicitly re-authorised — prior ROE may not extend to retest.
- Critical findings that are still Open: notify live, not at report time.

## References inside the library

- `00-engagement/04-retest-and-remediation.md`
- `templates/retest-report-template.md`
- `templates/finding-template.md` (for any new findings discovered during sibling sweep)
