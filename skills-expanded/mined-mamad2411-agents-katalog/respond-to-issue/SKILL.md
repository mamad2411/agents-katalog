---
name: respond-to-issue
description: Triage a GitHub Issue (add-cert / update-cert / add-source / evaluation) and dispatch to the right skill, ending with a draft PR or a clarifying comment.
---

# respond-to-issue

## When to use

A maintainer pastes a GitHub Issue URL or number, or an automated dispatch
hands you the Issue body. You triage and either run the matching skill or
ask the user to disambiguate.

## Process

1. **Fetch the Issue** via `gh issue view <n> --json number,title,body,labels`.
2. **Route by label**:
   - `add-cert`            → invoke `add-cert` skill with the form fields.
   - `update-cert`         → invoke `update-cert` skill with the cert id.
   - `add-source`          → invoke `add-source` skill with the agency fields.
   - `evaluation`          → produce a structured response (see below); do
                             NOT just edit the tier. Propose either a
                             `scoring_factors` change in the cert JSON or a
                             rubric change in `evaluate-roadmap-3-personas`.
   - No matching label, or multiple → comment on the Issue asking the user
                                       to pick the right template.
3. **For data-modifying actions**, after the underlying skill writes
   files:
   - `git checkout -b issue-<n>-<short-slug>`
   - Commit with a message that references the issue (`Refs #<n>`).
   - `gh pr create --fill --body "Closes #<n>"`
4. **Comment back on the Issue** with the PR URL or with the reason work
   is blocked.

## Evaluation-issue special handling

For `evaluation`-labelled issues:

- Read the user's claim and evidence.
- Re-read the cert's current `scoring_factors`.
- Decide which of these is the right fix:
  1. A new plus / minus factor with the user's evidence URL.
  2. A change to an existing factor's `weight_hint`.
  3. A rubric change in `data/tiers.json` or
     `.Codex/skills/evaluate-roadmap-3-personas/SKILL.md`.
- Open a PR with the chosen change. **Never** patch
  `evaluation.computed_tier` directly; let the next eval run reflect the
  underlying change.

## Never

- Do not close the Issue without a PR or an explanation comment.
- Do not respond by editing files on `main`.
- Do not invent fields not in `schema/certification.schema.json`.
