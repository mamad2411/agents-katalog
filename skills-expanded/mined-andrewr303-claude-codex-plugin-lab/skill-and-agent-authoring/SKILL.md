---
name: skill-and-agent-authoring
description: Use when creating or improving Codex skills, plugins, agent instructions, workflow docs, harnesses, or reusable AI operating procedures.
---

# Skill And Agent Authoring

Reusable instructions should be small, placed at the right layer, and validated.

## Placement Logic

- Always-on rule: short entry in `AGENTS.md` or equivalent.
- Repeated workflow: skill.
- Hard stop: deterministic script, hook, or test when possible.
- Artifact procedure: artifact-specific skill or template.
- Repo-specific knowledge: repo docs/wiki, not global instructions.

## Skill Quality Bar

- Clear trigger in frontmatter description.
- One job per skill.
- Concrete steps with pass/fail checks.
- No unsupported tool names unless a compatibility map is included.
- No fake mandates that cannot be enforced.
- References are relative and actually exist.
- Avoid instruction bloat and duplicated rules.

## Plugin Quality Bar

- Valid `.codex-plugin/plugin.json`.
- No TODO placeholders.
- Real assets for declared icon/logo paths.
- Marketplace entry only through the plugin-creator flow.
- Validator run before handoff.
- README explains what the plugin does and how to test it.

## Review Questions

- What behavior will this instruction improve?
- What failure mode does it prevent?
- Is prose enough, or should this be a check?
- Could it conflict with existing repo instructions?
- How will future agents know it worked?

