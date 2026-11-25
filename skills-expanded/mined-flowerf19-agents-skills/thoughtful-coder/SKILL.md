---
name: thoughtful-coder
description: Implements approved code changes with clean cutover, zero Tier 1 lint/type errors, and exported Tier 2 runtime verification artifacts. Use when asked to implement a feature, fix a confirmed bug, refactor code, or execute an approved plan. Do not use for discussion, planning, or review-only requests.
license: MIT
---

# Thoughtful coder

Deliver the approved behavior, a focused diff, and a verified Tier 1 + Tier 2 artifacts bundle.

Edit only inside approved implementation scope (see [AGENTS.md](../AGENTS.md) for permission, clean-cutover, comment-ban, and business-rule policies).

## Step 1: Before editing

1. Keep pre-existing changes separate from this task.
2. Check the Feature Map (if present; see [templates/feature-map.md](../templates/feature-map.md)) and trace the affected flow to its callers.
3. For bugs, verify or capture a **Reproduction Artifact** as concrete "before" proof. Resolve blocking questions before coding.
4. Confirm required **Verification Artifacts** (Tier 1 commands + Tier 2 live runtime flow and output paths) before editing.

## Step 2: Make the change

1. Make the smallest complete change following working project patterns and existing module boundaries.
2. **Clean cutover:** Migrate all affected callers, tests, config, and docs and delete superseded paths in the same task.
3. **Obey Tier 1 constraints:** On any lint, compiler, or typecheck failure, fix the root cause instead of silencing rules or adding workaround comments.
4. Keep validation, security, and explicit errors intact; leave unrelated cleanup and unneeded dependencies out of the diff.

## Step 3: Mandatory verification loop

1. **Tier 1 Gate (0 errors):** Run typecheck, compiler, linter, and applicable repo checks ([check-no-weakened-tests.sh](../scripts/checks/check-no-weakened-tests.sh), [check-file-boundaries.sh](../scripts/checks/check-file-boundaries.sh)). All must exit `0`.
2. **Tier 2 Runtime Verification:** Run tests **and** exercise the real product flow (CLI, live HTTP/API, browser/CDP/Playwright, or live integration). For bugs, show the repro fails before and passes after.
3. **Export Verification Artifacts:** Save real outputs/traces/captures to `.agents/artifacts` (or the task dir), fill `manifest.md` from [templates/verification-artifacts.md](../templates/verification-artifacts.md), and validate with [check-artifacts.sh](../scripts/checks/check-artifacts.sh).

Fix root causes on any failure and rerun. Report checks that cannot run as outstanding.

## Step 4: Review and finish

1. Hand off the diff, affected interfaces, and validated Verification Artifacts path for review.
2. Verify review findings before editing; fix valid in-scope issues and rerun Step 3.
3. Update the Feature Map and directly affected docs; mark an existing approved plan `done` only when verified.

Report exact changed files, commands, Verification Artifacts path, review status, and open gaps.
