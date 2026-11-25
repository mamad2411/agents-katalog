---
name: forge
description: Generate a new dragoon skill scaffold (SKILL.md, scripts/<name>.js, test/<name>.test.js, README.md) into .dragoon/forge/<name>/ for review. dragoon does NOT auto-install forged skills. After review, copy into ~/.dragoon/skills/ and add an entry to bin/dragoon's COMMANDS map. Use to extend the pack with custom skills. Run as `node ~/.claude/skills/dragoon/skills/forge/scripts/forge.js <name>`.
version: 1.0.0
---

# /forge

Scaffold a new skill. The pack extends itself.

## When to use

- Building a custom skill for the team
- Prototyping a new dragoon command
- The user says "make a new skill", "scaffold a skill"

## Run it

```
dragoon forge MySkill --description "what it does" --apply
```

Then review the scaffold, implement the script, copy to `~/.dragoon/skills/<name>/`, and register in `bin/dragoon`.

## Safety

- Skill name must be a valid identifier (a-z, A-Z, 0-9, _)
- Output lands in a sandbox: `.dragoon/forge/<name>/`
- Never auto-installed
