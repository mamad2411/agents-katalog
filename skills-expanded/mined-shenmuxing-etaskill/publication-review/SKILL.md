---
name: publication-review
description: Review MetaSkill skills before publication for privacy, public-safe examples, frontmatter and folder standards, truthful capability claims, and resource consistency. Use before moving a skill into skill-examples, publishing a skill, importing a local skill into MetaSkill, or responding to requests for public-readiness review.
---

# Publication Review

## Overview

Use this skill to decide whether a MetaSkill skill is ready to publish. It combines a deterministic script pass with a manual contract review.

## Workflow

1. Identify the target skill directory.
   - Review the candidate's `SKILL.md`, `agents/openai.yaml`, directly referenced resources, and any scripts it promises to use.
   - If the target is a collection-level README or root doc, review only the publication-facing claims in that file.
2. Run the lightweight checker when Python is available:

```powershell
uv run python .\publication-review\scripts\review_skill.py <path-to-skill>
```

3. Read `references/publication-checklist.md` and apply the manual checks that scripts cannot prove.
4. Report blockers first, then warnings, then the exact files reviewed.
5. Do not mark a skill public-ready if its trigger description promises automation, semantic judgment, external integrations, or generated artifacts that are not implemented by included resources or clearly marked as manual.

## Review Focus

- Privacy: no private paths, accounts, service identifiers, unpublished content, personal notes, or operational logs.
- Structure: `SKILL.md` frontmatter follows the system `skill-creator` validator; folder names use lowercase hyphen-case; optional directories are used by the skill.
- Contract truthfulness: every promised behavior is implemented, delegated to included scripts/resources, or explicitly labeled as manual or optional.
- Public examples: examples use generic fixtures such as `example-skill`, `sample-project`, or `private-workspace`.
- Metadata: `agents/openai.yaml`, when present, matches the skill body and does not introduce unsupported claims.

## Output

Use this shape for final review notes:

```text
Blockers
- <file>: <issue and required fix>

Warnings
- <file>: <risk or cleanup suggestion>

Reviewed
- <files and commands actually checked>
```
