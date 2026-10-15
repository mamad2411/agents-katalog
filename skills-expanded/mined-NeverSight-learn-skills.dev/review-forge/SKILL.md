---
name: review-forge
description: Use when orchestrating a code review workflow across multiple LLMs or agents, synthesizing review findings, producing checklist-driven fix scopes, applying selected fixes, running regression tests, independently verifying fixes, updating review status, or keeping code review process artifacts isolated under code_review/.
---

# Review Forge

Review Forge runs a conservative, auditable branch review workflow:

1. Inspect the target diff and project context.
2. Collect one or more independent review passes.
3. Synthesize common findings into a human-controlled checklist.
4. Fix only checked and confirmed items.
5. Run focused and regression tests after every fix batch.
6. Verify fixes independently when possible.
7. Update machine-readable status and localized report labels.
8. Keep all workflow artifacts isolated from product code.

## Modes

- `review-only`: create reviewer reports and a synthesized summary checklist. Do not modify product code.
- `review-and-fix`: read checked summary items, confirm the selected scope, implement only those items, run tests, and update status.
- `review-verify`: verify fixed items with an independent perspective, rerun or inspect tests, and update verification status.

If the user does not specify a mode, infer the safest mode from the request. When ambiguous, default to `review-only`.

## Inputs

Resolve or ask for these inputs before doing work:

- `target`: branch, commit range, pull request, or current working tree.
- `base`: comparison branch or ref. If omitted, infer it using the default diff rules below.
- `artifact_dir`: default `code_review/`.
- `mode`: `review-only`, `review-and-fix`, or `review-verify`.
- `report_language`: default `auto`, meaning follow the user's prompt language. Explicit values such as `en`, `zh-CN`, or `ja` are allowed.
- `auto_fix_allowed`: default `false` unless the user explicitly asks to fix.
- `reviewer_count` or `reviewer_perspectives`: optional.
- `test_command`: optional override for validation.

## Default Diff Rules

When the user does not specify a target or base, infer the review scope in this order:

1. If the working tree or index has uncommitted changes, review the uncommitted diff.
   - Inspect both unstaged and staged changes.
   - Treat this as `target: working tree`.
   - No base branch is required unless additional context is needed.
2. If there are no uncommitted changes, review the current `HEAD` against `main`.
   - Prefer a merge-base comparison such as `main...HEAD` when supported.
   - If `main` does not exist, try `master...HEAD`.
3. If neither `main` nor `master` exists, inspect branch tracking metadata or PR metadata when available.
4. Ask the user for `base` only when no reasonable comparison ref can be inferred.

Explicit user-provided PRs, branches, commit ranges, or base refs always override these defaults.

## Required Initial Inspection

Before producing artifacts or modifying code, inspect:

- repo status and uncommitted changes;
- target diff against the chosen base;
- existing `code_review/` artifacts;
- `.gitignore` for `code_review/`;
- package, build, and test configuration;
- project-specific instructions for tests, lint, typecheck, or CI.

Never revert unrelated user changes. If `code_review/` is not ignored, recommend adding it to `.gitignore`, but do not edit `.gitignore` unless the user asks.

## Artifact Names

Write workflow files under `artifact_dir`:

- `CODE_REVIEW_<reviewer>_<timestamp>.md`
- `REVIEW_SUMMARY_<timestamp>.md`
- `FIX_PLAN_<timestamp>.md`
- `VERIFY_REPORT_<timestamp>.md`
- `STATUS_<timestamp>.md`

Use the templates in `assets/templates/` unless the repository already has a stronger local convention.

## Review Collection

For multi-reviewer workflows, use distinct perspectives such as:

- correctness and edge cases;
- security and data safety;
- tests and regression risk;
- maintainability and architecture;
- product or UX behavior when relevant.

Use subagents or multiple LLM passes only when the host supports them and the user has explicitly authorized multi-agent work. Otherwise, perform sequential review passes yourself and label the perspective used.

Each finding must include severity, evidence, affected files, risk, and a concrete suggested fix. Avoid vague style preferences unless they affect maintainability or user-facing behavior.

## Summary Checklist

Synthesize reviewer reports into one summary:

- merge duplicate findings;
- preserve meaningful disagreement;
- record reviewer agreement count;
- include suggested tests;
- use checkboxes for human fix approval.

Checkbox semantics are stable:

- unchecked: not approved for fixing;
- checked: approved for fixing.

Do not fix unchecked issues opportunistically.

## Fix Rules

In `review-and-fix` mode:

1. Read the latest or specified `REVIEW_SUMMARY`.
2. Select only checked items whose status allows fixing.
3. Confirm the fix scope unless the user already explicitly approved it.
4. Create or update a `FIX_PLAN`.
5. Modify only the files needed for selected items.
6. Run tests.
7. Update `STATUS` and, when appropriate, the summary status fields.

If a checked item reveals a larger issue, stop and ask before expanding scope.

## Test Rules

Tests are mandatory after fixes unless impossible.

Run validation in this order:

1. The narrowest relevant test for the touched behavior, when discoverable.
2. Typecheck, lint, or build checks relevant to the touched files.
3. The broader project regression command when discoverable and reasonably scoped.

If tests cannot be run, record:

- status enum `test_blocked`;
- the command that should have run;
- the blocking reason;
- residual risk.

If tests fail, do not claim the item is fixed or verified. Mark affected items `verification_failed` or `partially_fixed`, record the failing command, and summarize the failure.

## Verification Rules

In `review-verify` mode:

- verify from a perspective independent of the fixer when possible;
- check whether each selected issue was actually addressed;
- rerun or inspect test evidence;
- look for regressions caused by the fix;
- update status only when evidence supports it.

Verification requires either passing test evidence or a clear `test_blocked` explanation.

## Language Policy

Write skill instructions, template field names, and machine-readable status enums in English.

Generated prose reports should use `report_language`:

- `auto`: follow the user's prompt language;
- explicit language values: write prose in that language;
- keep status enums in English even inside localized reports.

Status display labels may be localized.

## Status Enums

Use these exact machine-readable status values:

- `open`
- `approved_for_fix`
- `fixed`
- `partially_fixed`
- `wont_fix`
- `risk_accepted`
- `verified`
- `verification_failed`
- `test_blocked`

Each status entry should include both:

- `status`: one enum above;
- `status_label`: localized human-readable label, for example `Fixed ✅` or `已修复 ✅`.

## Completion Criteria

A Review Forge workflow is complete only when:

- review artifacts are under `artifact_dir`;
- checked items are the only fixed items;
- test evidence or `test_blocked` rationale is recorded after fixes;
- verification status does not overclaim;
- process artifacts remain isolated from product code.
