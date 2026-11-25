---
name: yolo-verify
description: Use to check a feature's work against its success_criteria and record the result. Produces verification.md and, on pass, the YOLO-Verified trailer. Triggers on "verify this", "does it meet the criteria", or as the verify step of yolo-feature.
---

# yolo-verify

Decide, with evidence, whether the work satisfies the brief's `success_criteria`.

## Inputs
- `workspace/features/<slug>/brief.md` (`success_criteria`), the diff `git diff <base_branch>...feature/<slug>` (three-dot — only what the branch introduced; see `.claude/yolo/conventions.md`), and `plan.md` `lint_commands`/`test_commands`.

## Procedure
1. Run the recorded `lint_commands` and `test_commands`. Capture pass/fail and key output.
2. For EACH criterion in `success_criteria`, gather concrete evidence (a passing test, an observed behavior, a code reference). Mark it met/unmet.
3. Write `workspace/features/<slug>/verification.md`: one section per criterion with its evidence, plus the lint/test results.

## Outcome
- **All criteria met** → commit the verification file with the trailer:
  `git add workspace/features/<slug>/verification.md && git commit -m "yolo: verify <slug>" --trailer "YOLO-Verified: true"`
- **Any criterion unmet** → write the file recording what failed, do NOT write the trailer, and report the gap so execution can resume. A feature is never "done" without `YOLO-Verified: true` (`.claude/yolo/conventions.md`). The execute→verify loop is **bounded** (`.claude/yolo/conventions.md` *The two gates*); after repeated failure the caller should stop and escalate to the human rather than re-running, since that signals the plan or criteria need rethinking.

## Constraints
- The only file you write is `verification.md`. You do not edit code.
- Verification is semantic (criteria), distinct from CI (mechanical) — yolo-finish handles CI.
