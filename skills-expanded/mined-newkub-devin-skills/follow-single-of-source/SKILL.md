---
name: follow-single-of-source
description: Single source of truth — one canonical definition, everything else references it, no duplication
argument-hint: "[topic-or-file]"
related:
  - follow-best-practice
  - update-devin-global-skills
  - new-skills
  - idea-merge
  - refactor
  - use-lib-effective
  - review-devin-global-harness
  - update-references
  - update-config
---

## Goal

Enforce single source of truth — every piece of data/definition/config/catalog has exactly one canonical location; everywhere else references or derives from it, never copies the content

## Scope

Use when creating/editing skills, docs, config, or data that could become duplicated:

- skill content — the canonical catalog/dispatch table lives in one place (e.g. `deep-review-codebase/SKILL.md`)
- config values — defined once then injected/imported (env, tokens, versions)
- docs — frequently changing facts (counts, versions, commands) have a single source
- data/schema — one model definition derives types/forms/validation
- reuse existing internal code before writing new (DRY) → `/use-lib-effective` `### 5`

## Execute

### 1. Identify Candidate

> Goal: find where the same data appears in multiple places

1. Look for duplicated content: numbers (counts, versions), dispatch tables, lists, rules
2. If the same data lives in ≥2 places → it's an SSOT candidate
3. Decide which one is canonical — usually the most authoritative or most detailed location

### 2. Establish Canonical Source

> Goal: designate one authoritative source

1. Pick the canonical location — a single file/section/variable
2. Move the full content to the canonical place
3. Everywhere else keeps only a reference — `> Canonical X lives at <path>` — or derives via script/import

### 3. Wire References

> Goal: consumers point back to the canonical, no copying

1. Replace duplicate content with a pointer + the short context needed
2. If a count/list must appear in multiple places → derive it from a command (`git ls-files`, script) instead of hardcoding
3. Run `/update-references` if files moved

### 4. Guard Drift

> Goal: prevent drift from now on

1. Add a sync note at the canonical — "if you change this, also update X" — when derived copies are necessary
2. If it can be derived → write a check script (`check-*`) to verify consistency
3. Record the canonical in `AGENTS.md` or conventions if it's repo-wide

## Rules

- One canonical per fact — never two authoritative places at once
- reference ≠ copy — derived locations store only a pointer or generated content
- If duplication is truly required (e.g. performance/embedding) → add a drift check or sync note
- Always edit the canonical; never edit a derived copy directly
- Use `/follow-best-practice` if needed
- Use `/update-devin-global-skills` if needed
- Use `/new-skills` if needed
- Use `/idea-merge` if needed
- Use `/refactor` if needed
- Use `/review-devin-global-harness` if needed
- Use `/update-config` if needed


## Expected Outcome

- Every fact has a single source — one edit propagates correctly
- No drift between copies
- The canonical path is clearly stated in docs/conventions
