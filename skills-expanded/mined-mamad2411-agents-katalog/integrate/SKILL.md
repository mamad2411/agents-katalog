---
name: integrate-skill
description: Add new skill to framework — location, metadata, testing, documentation
triggers: [new skill, add skill, integrate skill, create skill, extend framework]
---

# SKILL: Integrate Skill

## File Structure

```
skills/[skill-name]/
├── SKILL.md           ← the skill file (required)
├── examples/          ← optional: code examples
│   ├── example1.py
│   └── example2.py
└── tests/             ← optional: test suite
    └── test_skill.py
```

## Skill File Template

```yaml
---
name: [skill-name]
description: [One sentence of what it does]
triggers: [keywords, that, activate, this, skill]
---

# SKILL: [Name]

## Purpose
[Why this skill exists]

## Core Pattern
[What you're trying to achieve]

## Complete Example
[Full, runnable example]

## Quality checks
- [ ] [requirement 1]
- [ ] [requirement 2]
```

## Testing the Skill

```bash
# Is the file valid YAML?
python3 -c "import yaml; yaml.safe_load(open('SKILL.md'))"

# Does it have all sections?
grep "^# " SKILL.md | grep -E "Purpose|Pattern|Example|Quality"

# Are code examples runnable?
# Copy each code block and verify it works
```

## Documentation

Add to THE_BIBLE.md:
```markdown
## [Skill Category]

- **[skill-name]**: [description]
  File: `skills/[skill-name]/SKILL.md`
  Use when: [when to use this skill]
  Related: [related skills]
```

## Quality checks
- [ ] Skill file created in skills/[name]/SKILL.md
- [ ] YAML frontmatter valid
- [ ] Triggers defined (keywords for activation)
- [ ] Purpose section clear
- [ ] Complete working example included
- [ ] Quality checks section present
- [ ] Added to THE_BIBLE.md index
- [ ] File not empty (minimum 500 lines)
