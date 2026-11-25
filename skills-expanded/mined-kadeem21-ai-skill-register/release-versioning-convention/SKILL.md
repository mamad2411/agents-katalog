---
name: release-versioning-convention
description: Define semver policy, changelog/release notes flow, tagging rules, and breaking-change handling. Use when preparing or automating releases.
---

# Release and Versioning Convention

## Goal
Make releases predictable and auditable.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Versioning policy plus release checklist and tag format.

## Verify Gate
Every release change includes version bump rationale and notes entry.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
