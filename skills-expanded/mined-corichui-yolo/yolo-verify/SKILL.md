---
name: yolo-verify
description: Use to check a feature branch against its brief's success_criteria and record the result. Writes verification.md and, on a full pass, commits it with the YOLO-Verified trailer. Triggers on "verify this feature", "does it meet the criteria", "yolo verify".
---

# yolo-verify

Decide, with evidence, whether `feature/<slug>` satisfies its brief. Rules:
`../../yolo/conventions.md`.

## Inputs
- `workspace/features/<slug>/brief.md` → `success_criteria`.
- The branch's own changes: `git diff <base>...feature/<slug>` (three-dot).
- The project's lint and test commands. Find them in `package.json` scripts, a `Makefile`,
  `justfile`, `pyproject.toml` or CI config. If there are none, say so; don't invent any.

## Procedure
1. Check out `feature/<slug>` and make sure the working tree is clean.
2. Run the lint and test commands. Record pass/fail and the key output.
3. For each criterion, gather concrete evidence: a passing test, an observed behavior, a
   code reference. Mark it met or unmet. A criterion you couldn't actually check is unmet.
4. Write `workspace/features/<slug>/verification.md`: one section per criterion with its
   evidence, then the lint/test results.

## Outcome
- **All met**: commit only that file, with the trailer, as the branch tip:
  `git add workspace/features/<slug>/verification.md && git commit -m "yolo: verify <slug>" --trailer "YOLO-Verified: true"`.
  Status reads `verified` until the branch is merged. Any later commit on the branch makes
  the verification stale; re-run this skill before merging.
- **Any unmet**: still write `verification.md` (it records the gap), commit it **without**
  the trailer, and report what failed.

## Constraints
- Writes only `verification.md`. Never edits code to make a criterion pass.
