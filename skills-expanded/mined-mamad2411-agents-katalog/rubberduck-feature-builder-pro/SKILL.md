---
name: rubberduck-feature-builder-pro
description: RubberDuck Feature Builder Pro consumes an immutable sealed_plan.json plus SIGNOFF.json or AUTO_AUTHORIZATION.json, applies tests first, writes production code under a machine-readable Spec Heartbeat, re-indexes changed files, reverts regressions, adjudicates warnings, validates generated diffs, optionally publishes a GitHub-indexable validation branch for repo-backed RubberDuck validation, runs a PR security delta gate when required, and emits PR_READY.diff only when gates pass.
trigger: when the user has a sealed feature plan and wants to build the feature, consume sealed_plan.json, generate production code, apply tests-first implementation, produce PR_READY.diff, or run Spec Heartbeat build mode
version: 2026-05-feature-builder-pro
---

# RubberDuck Feature Builder Pro

This skill mutates files. It consumes a sealed Feature Planner Pro contract.

```text
sealed_plan.json + SIGNOFF.json
  -> worktree safety
  -> apply tests first
  -> Spec Heartbeat loop
  -> incremental re-index
  -> regression revert
  -> validate_generated_diff
  -> final command gate
  -> GitHub publish/re-index gate when repo-backed RubberDuck validation is required
  -> Security Delta Gate when PR security validation is required
  -> PR_READY.diff
```

## RubberDuck CI bootstrap gate

When Builder refreshes RubberDuck evidence, validates changed files through RubberDuck, or consumes a Planner artifact that claims RubberDuck coverage, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, repo-backed RubberDuck validation must use an authorized GitHub repo or mirror with completed `detailed_repo_analysis(..., semantic_mode="full")` before semantic graph claims are made.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user is unsure whether to use build mode or autonomous mode, use `RUBBERDUCK-SKILL-ADVISOR.md` to explain the control tradeoff and ask for approval before starting or escalating multi-skill execution.

## RubberDuck security delta gate

For GitHub-validated builds, autonomous builds, security-sensitive features, or user requests for a security sweep before PR readiness, read `RUBBERDUCK-SECURITY-DELTA-GATE.md`. Builder must compare the PR head against the base branch, auto-fix true-positive new Critical/High findings inside the approved mutation envelope, adjudicate false positives with evidence, and keep pre-existing repository findings separate.

## Hard rules

1. Build requires `sealed_plan_path`.
2. Build requires `SIGNOFF.json` for USER mode or `AUTO_AUTHORIZATION.json` for AUTO_MODE.
3. `sealed_plan.json` is immutable; do not edit it for signoff.
4. Verify `sha256(sealed_plan.json)` against signoff/authorization before writing.
5. Run Worktree Safety before any file write.
6. Apply `test_diff.patch` before production code.
7. Heartbeat is machine-readable JSON, not prose.
8. Every GREEN heartbeat dimension requires evidence.
9. No self-declared completion.
10. Do not emit `PR_READY.diff` unless final gates pass.
11. Do not call `end_codegen_session` unless Spec Heartbeat passes and `validate_generated_diff` returns PASS.
12. Do not claim full RubberDuck Codebase Intelligence validation unless repo-backed validation ran on the pushed commit or branch and includes new files.
13. If repo-backed validation is unavailable, skipped, or declined, final output must say: "Local build complete; repo-backed RubberDuck validation is pending."
14. The final answer must include exactly one validation status label from the completion-label section.
15. The final answer must include exactly one security delta status label from the security-delta-label section.
16. Do not promote a PR as ready when `Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS` or `Security delta status: NOT_RUN_LOCAL_ONLY`.

## Execution modes

```text
LOCAL_BUILD_ONLY
GITHUB_VALIDATED_BUILD
AUTO_GITHUB_VALIDATED_BUILD
```

`LOCAL_BUILD_ONLY` can edit files, run local tests, and emit `PR_READY.diff` after local gates pass. It must not claim full RubberDuck Codebase Intelligence validation. If RubberDuck CI cannot read newly created local files, final output must label validation as degraded and say GitHub re-index remains required.

`GITHUB_VALIDATED_BUILD` is required when the user asks for RubberDuck Codebase Intelligence, Phase 2 indexing, semantic validation, codegen validation that depends on pushed repo state, or validation of newly created local files. After explicit user approval, create or switch a scoped branch, commit only intended files, push, and run or re-poll RubberDuck Codebase Intelligence and Semantic Intelligence. Do not finalize as fully RubberDuck-validated until repo-backed indexing completes or a blocker is reported.

`AUTO_GITHUB_VALIDATED_BUILD` is allowed only when `AUTO_AUTHORIZATION.json` or an explicit user message authorizes external GitHub mutation. It follows the same repo-backed requirements without step-by-step prompting. It must still avoid secrets, unrelated files, and destructive git commands.

## Required inputs

```text
sealed_plan_path
signoff_path OR auto_authorization_path
invoked_under: USER | AUTO_MODE
max_iterations default 50
tier: QUICK | STANDARD | DEEP
```

## Build phases

```text
B0  Worktree safety
B1  Plan/signoff/session integrity
B2  Initialize HEARTBEAT.json
B3  Apply test_diff.patch
B4  Enter build loop
B5  Cheap prevalidate proposed change
B6  Apply smallest change
B7  Incremental re-index changed file
B8  Refresh affected heartbeat dimensions
B9  Revert regressions
B10 Drift/doppelganger gates
B11 Pulse validation
B12 WARN adjudication
B13 Final validation
B14 Final command gate
B14.5 GitHub Publish/Re-index Gate
B14.6 Security Delta Gate
B15 Seal session and emit PR_READY.diff
```

## B14.5 GitHub Publish/Re-index Gate

Read `GITHUB-PUBLISH-REINDEX-GATE.md` before final completion. Trigger this gate if any of these are true:

- The user explicitly asks for RubberDuck Codebase Intelligence, Phase 2, indexing, re-indexing, semantic validation, or "use RubberDuck to validate."
- `load_code`, semantic indexing, or codebase-intelligence validation cannot read newly created local files.
- `validate_generated_diff` passes only on a subset of changed files because new files are unindexed.
- The feature creates substantial new modules that need repo-backed analysis.
- The plan, `SIGNOFF.json`, `AUTO_AUTHORIZATION.json`, or Skill Advisor selection says the run should be RubberDuck-validated end-to-end.

Gate behavior:

- If GitHub mutation is not already authorized, pause and ask the user to approve branch creation, scoped staging, commit, push, PR creation if appropriate, and RubberDuck re-indexing/validation.
- If GitHub mutation is authorized, proceed automatically under the git hygiene rules.
- If the user declines, mark the run `LOCAL_BUILD_ONLY` and final status `Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING`.
- If pushing or indexing is blocked, mark final status `Validation status: BLOCKED_BEFORE_REPO_BACKED_VALIDATION` and record the concrete blocker.

Before commit or push:

- Run `git status --short`.
- Identify unrelated dirty files and exclude them.
- Stage only files required by the feature.
- Run a secret scan over staged changes.
- Never stage `.env`, `.env.local`, local databases, caches, screenshots with secrets, browser artifacts, cookies, or API keys.
- Never use `git reset --hard` or destructive checkout.
- Prefer a new branch named `codex/<feature-slug>`.
- If already on `main`, create a feature branch before committing.
- If unexpected changes exist in files Builder must edit, inspect and preserve them.

After pushing:

- Run or re-run Codebase Intelligence against the GitHub repo and branch.
- Use `detailed_repo_analysis(repo=..., branch=..., semantic_mode="full")` where applicable.
- Re-poll until the full report completes or a concrete blocker is reached.
- If semantic-intelligence `get_started` returns an `instance_id`, save it and pass it to `load_code`.
- Load changed files or relevant file patterns with sufficient coverage and validate new files, not only pre-existing tracked files.
- Record repo, branch, commit hash, PR URL if created, indexing status, validation IDs, validation coverage, and blockers.

## B14.6 Security Delta Gate

Read `RUBBERDUCK-SECURITY-DELTA-GATE.md` before PR-ready completion. Trigger the gate for `GITHUB_VALIDATED_BUILD`, `AUTO_GITHUB_VALIDATED_BUILD`, security-sensitive features, or any request for PR security validation.

The gate compares RubberDuck findings on the base branch versus the PR head. Builder may auto-fix only true-positive new Critical/High findings in changed or newly created code and only within the approved file/mutation envelope. Pre-existing findings are baseline debt and must be documented separately.

If the gate cannot produce a comparable base/head delta, or a new Critical/High remains unresolved, keep the PR draft or blocked and use `Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS`.

## Ten Spec Heartbeat dimensions

```text
H1 Acceptance Criteria Ledger
H2 Pattern Fidelity
H3 Symbol Reuse Map
H4 Avoid-List Integrity
H5 Doppelganger Watch
H6 Test Coverage Parity
H7 Type Contract Preservation
H8 Effect Manifest
H9 CFG Path Coverage
H10 Drift Detector
```

Statuses:

```text
GREEN
YELLOW_ACCEPTED
YELLOW_UNACKED
RED
BLOCKED
NOT_APPLICABLE
UNAVAILABLE
```

Completion requires:

```text
No RED
No BLOCKED
No YELLOW_UNACKED
validate_generated_diff PASS
Final Command Gate PASS or explicitly accepted unavailable
iteration_count <= max_iterations
AUDIT.json complete
```

## Completion labels

Every final answer must include exactly one:

```text
Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED
Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING
Validation status: BLOCKED_BEFORE_REPO_BACKED_VALIDATION
```

Use `FULL_REPO_BACKED_RUBBERDUCK_VALIDATED` only when local tests pass, py_compile/type/lint gates pass as applicable, `validate_generated_diff` passes, repo-backed RubberDuck validation ran on the pushed commit or branch, new files are included in validation, no RED/BLOCKED heartbeat dimensions remain, and warnings are explicitly adjudicated.

If GitHub re-indexing is unavailable, skipped, or declined, say exactly: "Local build complete; repo-backed RubberDuck validation is pending." Do not say "fully RubberDuck validated." Do not mark Codebase Intelligence Phase 2 complete.

## Security delta labels

Every final answer must include exactly one:

```text
Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH
Security delta status: NEW_FINDINGS_ADJUDICATED
Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS
Security delta status: NOT_RUN_LOCAL_ONLY
```

Use `CLEAN_NO_NEW_CRITICAL_HIGH` only when RubberDuck base/head comparison shows no new untriaged Critical/High findings.

Use `NEW_FINDINGS_ADJUDICATED` only when all new Critical/High findings are fixed or adjudicated with evidence and no unresolved blocker remains.

Use `BLOCKED_NEW_UNRESOLVED_FINDINGS` when new Critical/High findings remain unresolved, RubberDuck cannot produce comparable base/head results, or the authorized mutation envelope prevents a needed fix.

Use `NOT_RUN_LOCAL_ONLY` only for `LOCAL_BUILD_ONLY`. Never claim "repo is clean" when pre-existing findings remain; say "the PR security delta is clean."

## Deliverable

```text
uc07/<slug>/
  AUDIT.json
  BUILD.md
  PR_READY.diff
  HEARTBEAT.json
  heartbeat-history.json
  validation-history.json
  WARN_ADJUDICATION.json
  SIGNOFF.json or AUTO_AUTHORIZATION.json
  evidence/
    worktree-safety.md
    plan-integrity.md
    test-first-application.md
    incremental-reindex.md
    github-publish.md
    repo-backed-rubberduck-validation.md
    indexed-files-coverage.md
    security-baseline-rubberduck.md
    security-pr-head-rubberduck.md
    security-delta.json
    security-delta.md
    security-fix-loop-history.json
    finding-adjudication.json
    doppelganger-gates.md
    drift-events.md
    regression-reverts.md
    command-validation.md
    final-validation.md
    tool-health.md
```
