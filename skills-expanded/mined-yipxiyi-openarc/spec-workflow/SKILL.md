---
name: spec-workflow
description: Use when creating or updating OpenArc feature specs with acceptance criteria, compatibility decisions, and technical direction.
---

# Spec Workflow

Use this skill when behavior, acceptance criteria, compatibility, or product direction needs durable alignment before implementation. Routine work with clear behavior and validation does not need a spec.

## Goal

Create lightweight specs that keep humans and coding agents aligned without adding heavy process overhead.

Use Clarification Gate output when available. If the feature behavior, non-goals, compatibility constraints, or acceptance criteria are not clear, run `clarification-gate` before drafting the spec.

## Location

Use `docs/specs/` by default.

Recommended file names:

```txt
docs/specs/
  auth-system.md
  editor-upgrade.md
  cloud-sync.md
```

Use a stable, descriptive kebab-case slug. Do not couple the file name to a release version or rename the spec when the release version changes.

## Status Values

- Draft
- Planned
- In Progress
- Implemented
- Verified

## Release Impact

Draft and name the spec without waiting for version confirmation.

Use `version-governance` only when the proposed change is release-visible. When useful, record an optional `Release Impact` section with:

- change type
- proposed release version
- confirmation status

The release manifest, release changelog, and tags remain authoritative for the released version.

## Spec Sections

Use `templates/SPEC.template.md` as the baseline:

- Background
- Goals
- Non-Goals
- User Stories
- Requirements
- Existing System Review
- Technical Approach
- Release Impact when release-visible
- Acceptance Criteria
- Risks
- Open Questions
- Changelog

## Rules

- Keep specs concrete and implementation-facing.
- Include only sections relevant to the change. Keep implementation sequencing in `docs/plans/*` and active coordination in `docs/TASKS.md` instead of duplicating either inside the spec.
- Do not create a spec solely because a change touches multiple files.
- Separate goals from non-goals.
- Include acceptance criteria that can be verified.
- Preserve Clarification Gate decisions in Background, Goals, Non-Goals, Requirements, Risks, or Open Questions instead of creating a separate intake document by default.
- Update status and changelog after implementation.
- Do not use specs as a dumping ground for unrelated product ideas.
- Use the spec changelog for spec revisions, not as the source of truth for release versions.
