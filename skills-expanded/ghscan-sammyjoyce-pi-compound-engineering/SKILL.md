---
description: Create or edit a pi skill (Agent Skills format)
---
# create-agent-skill (pi)

## Input

$ARGUMENTS

If empty, ask for:
- skill name (lowercase, hyphens)
- what it does
- when to use it

## Output

Create a directory:
- `skills/<skill-name>/SKILL.md`

With required frontmatter:

```markdown
---
name: <skill-name>
description: <what it does and when to use it>
---

# <Title>

## Setup

## Usage

## Notes
```

Use relative paths to scripts/assets inside the skill directory.
