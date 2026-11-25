---
name: example-skill
description: A starter template demonstrating the SKILL.md format. Duplicate this folder to create your own custom skills.
---

# Example Skill

This is a minimal custom skill intended to demonstrate the Context Engine skill format.

## Triggers
- do something
- example task

## Instructions

When the user asks to "do something" or triggers this skill, follow these steps:

1. Acknowledge the skill was matched.
2. Explain that this is a template skill.
3. Point the user to the `skills/` directory to create their own.

## Notes

- Skills are discovered automatically by the server when placed in the `skills/` directory.
- Each skill must have a `SKILL.md` file at its root.
- YAML frontmatter (`name`, `description`) is optional but recommended for better dashboard display.