---
name: skill-governance
description: Govern a growing Codex skill pack: evaluate external skills, prevent duplicate or conflicting skills, version skill changes, track sources, define skill tiers, retire weak skills, and maintain trigger quality. Use when adding, reviewing, merging, pruning, distributing, or upgrading skills.
---

# Skill Governance

## Purpose

Keep the skill system useful as it grows.

More skills are not automatically better. A good skill pack is discoverable, non-overlapping, safe, triggerable, and maintained.

## Skill Tiers

- `Core`: routing, project context, project maintenance, project evolution, docs, governance.
- `Professional`: domain skills used often in project development, such as frontend, backend, API, database, Tauri, UI, testing, security.
- `Specialized`: narrow workflow skills, such as Figma, PostgreSQL, release packaging, migration, QA.
- `Optional`: rare, experimental, or project-specific skills.

For production-grade project development, `project-assistant`, `project-sync-audit`, `docs-index-maintainer`, and `production-readiness-pro` are Core/Workflow skills because they protect continuity, handoff quality, and release confidence.

## Evaluation Checklist

Before adding a skill, assess:
- Clear trigger.
- Real repeated use case.
- Non-overlap with existing skills.
- Concise procedural body.
- Safe instructions.
- License/source compatibility.
- Maintenance cost.
- Verification or output contract.
- Fits one tier.
- Whether it improves production readiness, project memory, or domain execution enough to justify routing complexity.

## Frontmatter Standard

Every `SKILL.md` must have:

```yaml
---
name: short-hyphen-name
description: What the skill does and exactly when to use it.
---
```

Description must include trigger terms. Do not hide trigger rules only in the body.

## Body Standard

Prefer these sections:
- `Purpose`
- `Workflow`
- `Required Checks` or `Checklist`
- `Avoid`
- `Output`

Keep skills procedural. Avoid long essays.

## Merge Rules

- If a new skill only adds a checklist to an existing skill, merge it.
- If it has a distinct trigger and workflow, create a new skill.
- If it is domain-specific but rare, mark it optional.
- If it conflicts with project rules or safety rules, do not import it directly.
- If two skills compete for the same trigger, clarify descriptions or merge.

Production skill rule:
- General domain skills hold baseline rules.
- `*-pro` skills hold production-grade workflows and deeper checklists.
- If a baseline skill repeats a `*-pro` workflow, keep the baseline short and reference the pro skill.

## Versioning

Track significant changes in `MANIFEST.md`:
- Added skill.
- Renamed skill.
- Merged skill.
- Deprecated skill.
- Source inspiration.
- Reason for change.
- Prompt version compatibility.

## Pruning

Deprecate or merge skills that:
- Rarely trigger.
- Duplicate another skill.
- Cause routing confusion.
- Are too broad to guide action.
- Contain outdated or unsafe instructions.

## Distribution

For sharing to another computer:
- Include the full prompt file.
- Include the complete skill folder.
- Include installation notes.
- Include the manifest.
- Keep generated zip versioned.

## Output

Provide recommendation:

```markdown
判断：Add | Merge | Adapt | Skip | Deprecate

理由：
- ...

影响：
- ...
```
