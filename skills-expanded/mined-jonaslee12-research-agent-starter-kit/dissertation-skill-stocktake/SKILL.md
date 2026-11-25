---
name: dissertation-skill-stocktake
description: Audit dissertation project skills for trigger clarity, overlap, stale content, missing safety gates, maintenance value, and merge/keep/improve/retire decisions.
---

# Dissertation Skill Stocktake

Use this skill to review `.agents/skills/` as a maintainable system, especially after migrations, new workflow rules, or signs of overlap between skills.

## Purpose

Adapt ECC skill-stocktake to this dissertation project. The goal is not to count skills; it is to keep each skill useful, scoped, and non-overlapping.

## Modes

| Mode | Use When | Scope |
|---|---|---|
| Quick Scan | after recent skill edits | changed or newly created skills |
| Full Stocktake | periodic system review | all `.agents/skills/*/SKILL.md` |
| Targeted Review | user names a problem area | only relevant skills |

## Checklist

For each skill, check:

- frontmatter has correct `name` and `description`
- trigger is clear
- scope is not too broad
- content does not duplicate another skill
- safety rules are present where needed
- source-first and document-quality gates are referenced when relevant
- skill fits Production Window, Maintenance Window, or both
- no obsolete external-tool assumptions
- no instruction to install/run unknown tools without confirmation

## Verdicts

Use:

- `Keep`: useful and clear
- `Improve`: useful but needs specific changes
- `Merge into X`: overlapping content should move into another skill
- `Retire`: no unique value or unsafe/stale
- `Split`: one skill covers too many unrelated tasks

## Output Format

```text
Skill stocktake:

| Skill | Verdict | Reason | Action |
|---|---|---|---|
| ... | Keep/Improve/Merge/Retire/Split | ... | ... |

Priority fixes:
1. ...
```

## Guardrails

- Do not delete or archive skills without explicit user confirmation.
- Do not rewrite many skills unless the stocktake identifies a concrete defect.
- For merge/retire recommendations, name the target skill that covers the same work.
- Update `research-wiki/TASK_STATE.md` after implemented skill changes.
