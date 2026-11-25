# Register Skill

> Use for: adding a new skill and keeping the registry in sync in one step.

```
@skills/README.md @skills/REGISTRY.md
@skills/SKILL-TEMPLATE.md

Create a new skill called "[skill-name]" that handles requests to [describe the task
in user words].

1. Read SKILL-TEMPLATE.md and REGISTRY.md first.
2. Create skills/[skill-name]/SKILL.md following the template:
   - Description written in the USER's words (this is what matching keys off)
   - Numbered procedure steps, each with a one-line "why"
   - Verification section (how to know it worked)
   - Conventions specific to this skill
   - One worked example
3. Register it: add a row to the Trigger table in REGISTRY.md
   (Skill / Trigger / What it produces / Typical commands).

Constraints:
- Don't invent commands — use real ones from AGENTS.md.
- Keep the trigger narrow enough not to fire on unrelated tasks.
- Match the style of existing skills in skills/ (both are worked examples).
```

**Rules:** skills are for repeatable multi-step procedures. If it's < 3 steps → it's a prompt,
not a skill. If it's project conventions → it belongs in AGENTS.md. If in doubt, don't make a skill.
