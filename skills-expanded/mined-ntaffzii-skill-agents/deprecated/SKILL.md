---
name: deprecated
description: Retire, preserve, explain, or replace old skills without silently deleting useful history. Use when the user asks to deprecate a skill, replace a skill, audit stale skills, or understand why a skill should no longer be used.
---

# Deprecated Skill Maintenance

Use this skill when a skill is no longer recommended but should remain understandable.

## Purpose

`skills/deprecated/` keeps retired skills visible until users and workflows have moved away from them. Deprecation should explain what replaced the skill and why.

## When To Deprecate

- Another skill fully replaces it.
- The workflow is unsafe or misleading.
- The scope became too broad or unclear.
- The domain changed and the instructions are stale.
- It was an experiment that should not be promoted.

## Rules

- Do not delete a retired skill until replacements and references are clear.
- Do not leave active workflows pointing at deprecated skills.
- Keep the deprecation reason short and factual.
- Preserve useful reference material when it can be safely reused.

## Workflow

1. Identify replacement
   - Name the new skill or workflow if one exists.
   - If no replacement exists, state that clearly.

2. Move carefully
   - Move the old skill folder into `skills/deprecated/`.
   - Keep its `SKILL.md` readable.
   - Add a deprecation note near the top.

3. Update references
   - Remove it from README stable skill lists.
   - Remove it from workflow recommendations.
   - Update `data/workflows.json` or `data/tools.json` if needed.

4. Explain the reason
   - State why the skill was retired.
   - State what to use instead.
   - Preserve any useful reference links.

5. Validate
   - Run skill and workflow validation.
   - Confirm no active workflow depends on the deprecated skill.

## Deprecation Note Template

```markdown
## Deprecated

Status: Deprecated
Reason: ...
Use instead: `replacement-skill`
Date: YYYY-MM-DD
```

## Output Format

End with:

- Deprecated skill
- Replacement
- References updated
- Validation result
