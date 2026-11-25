---
name: accept-system
description: Apply proportionate product acceptance within the current TODO: executable checks, actual role-based user paths, changed behavior and regressions, without a separate acceptance contract.
---

# Accept system

Use as a checklist in the current TODO for a significant system/application change.
A small local fix needs targeted checks, not a complete-system retest.

1. Check the owner's primary requested outcome against the original requirement,
   alongside the current TODO. Cosmetic completion or a test count does not accept
   an unfinished primary path. For each material requirement record expected behavior, actual result, environment
   and evidence. Independent model lineage reviews the current product, not the
   maker's self-report. Missing applicable checks/UAT means not accepted.
2. If a user path changed, exercise it under relevant roles and viewports: opening,
   action, visible response, terminal result, error and recovery. Prefer isolated
   remote-computer-use when available. Record route/role/expected/actual and the
   artifact tested. A screenshot alone or unit/lint/build does not prove the path.
   Validate interactive user-journey evidence with `scripts/browser_uat_check.py validate-report <report.json>`
   (fails closed on static-screenshot-only evidence, missing user interactions, console/5xx errors,
   missing mobile viewports, or mismatched screenshot hashes). Generate readiness skeletons
   via `scripts/browser_uat_check.py probe-url <url>`.
3. Test only the layers affected: API/business rules, role permissions, data quality,
   persistence/recovery, performance or accessibility where the change warrants it.
   Derive applicable criteria from the product; a reviewer may justify N/A without
   a separate owner approval for an irrelevant test.
4. DEV/TEST uses synthetic data and technically blocks real email, payment, CRM and
   calendar effects. STAGING has an allowlist. PROD and real effects retain their
   exact owner-consent gate. Evidence for one environment does not accept another.
5. Integrate once, retest changed behavior and material regressions. Reuse unchanged
   artifact/test evidence only when its inputs and checks still match. Report-format
   repair does not justify recoding or another full test cycle.
6. A reviewer returns concrete REPAIR findings or ACCEPT covering all criteria.
   Two unchanged failures require diagnosis or a different qualified executor.
   Add a security specialist only for a distinct risk, not to audit the reviewer.
7. Report function | exists | tested | integrated | missing for material outcomes.
   Keep product acceptance, preserved artifact, transport and Hub status separate.
   An accepted candidate is not a production deployment.
8. For code review acceptance, verify changed-file review coverage against the Git
   base/head diff (`review_coverage.py` in agent-graph; see
   `../agent-graph/references/review-coverage.md`): all modified, added, deleted, or
   renamed files must have an explicit review record or safe structured exclusion
   justification. Findings require exact, fresh line spans and anchor excerpts;
   stale anchors fail. Cross-file dependency context must be recorded and examined.
   Manifest completeness verifies inventory accounting, not semantic bug freedom;
   the reviewer must examine dependent behavior. Keep this accounting in the same
   review; it does not require another reviewer, planner, or acceptance contract.

Deeds, not counts: a capability, fix, or maintenance entry describes the product
effect plus its expected/actual evidence recorded above. Commit counts, file
counts, and test counts never proxy quality and never rank agents.

Keep secrets/cookies/client data out of evidence. Tokens are telemetry; an estimate
is not an acceptance gate. Real quota and explicit owner limits still apply.
End the session through the canonical Hub gateway. Missing knowledge receipt means
knowledge_closeout: BLOCKED independently of the true product-test result.

Historical init/approve/run-graph/acceptance.py recovery commands remain in
references/legacy-recovery.md, HISTORICAL ONLY; do not run them for new TODO work.

## Opt-in: baseline comparison

Only when a TODO actually compares, migrates, or rebuilds behavior against a
known baseline, read
[references/baseline-comparison.md](references/baseline-comparison.md). Do not
load it for ordinary acceptance; it adds no score calculator, contract, or
all-system retest. Historical `scripts/acceptance.py` stays untouched.
