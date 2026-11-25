---
name: reviewable-pr
description: "Prepare PRs for review: clean noisy history, improve descriptions, add reviewer guidance. Trigger: 'make easy to review', 'tidy PR', 'clean up commits', 'annotate diff'."
when_to_use: "Activate ONLY when explicitly asked to prepare a PR for review. Do NOT auto-trigger during normal coding or review tasks."
argument-hint: "[PR URL, branch, or current]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: review
  ck_mcp_tools: [ck_git_diff, ck_git_status, ck_validate, ck_review_submit, ck_finding]
  related_skills: [security-review, deep-code-quality-review]
---

# Reviewable PR

Prepare a PR so a reviewer can quickly understand intent, risk, and key files — without changing code behavior.

## Do NOT use when
- Doing normal coding or bug fixing
- Running security or quality reviews (use those skills directly)
- Making behavior changes (this skill only improves reviewability)

## Workflow

1. Resolve the PR (URL, branch, or current). Run `ck_git_diff` and `ck_git_status`.
2. Run `ck_validate` on the diff. Resolve blocked findings first — reviewability is secondary to correctness.
3. Diagnose reviewability issues against [checklist](references/pr-checklist.md):
   - Noisy/mixed-intent commit history
   - Missing or stale PR description
   - Unrelated changes mixed in
   - Mechanical changes mixed with logic
   - Missing test coverage for core change
   - Unclear reviewer entry points
4. Record issues as `ck_finding` (category `reviewability`, severity `medium`/`low`).
5. Submit plan via `ck_review_submit` (review_type: `plan`) describing what will change. **Wait for approval** before rewriting history or force-pushing.
6. Apply approved improvements. After any history rewrite, verify tree hash unchanged:
   ```
   ORIGINAL_TREE=$(git rev-parse origin/<branch>^{tree})
   # ... rewrite ...
   # Tree must match
   ```
7. Update PR description with: TL;DR, core files (3-7), mechanical files, risk callouts, context links.

## Guardrails

- Never hide behavior changes inside cleanup
- Never force-push without `ck_review_submit` approval
- If PR too large to review, recommend splitting instead of polishing
- If `ck_validate` blocked, fix those first

## Output

- `ck_finding` records for reviewability issues
- `ck_review_submit` plan (approved)
- Updated PR description with reviewer guidance
- Verified tree identity after any history changes
