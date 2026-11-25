# Prompt: Improve Existing Skill

> Authoritative prompt: `quan-skills:prompts/improve-skill.md`
> Related doc: `quan-skills:docs/skill-authoring.md`

Refine and improve an existing Codex skill.

## Authoritative Source

Skill anatomy and quality expectations:
`quan-skills:docs/skill-authoring.md`

## Context

- Skill to improve: `skills/{skill_name}/SKILL.md`
- Issue or improvement area: `{improvement_area}`

## Steps

1. Read the current SKILL.md
2. Read `quan-skills:docs/skill-authoring.md` for required anatomy
3. Identify problems: unclear triggers, missing workflow steps, vague instructions, missing verification
4. Check if `references/` docs need updates
5. Apply fixes:
   - Clarify "Use This Skill" triggers
   - Ensure workflow steps are actionable and ordered
   - Add "Do not..." constraints to prevent scope creep
   - Verify Pre-Read Order and Verification sections
   - Remove fluff — keep concrete instructions only
6. Commit: `skill({skill_name}): {brief_description}`
