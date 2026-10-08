---
description: "Scaffold a new Claude Code skill using the skill-factory"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash(python3 skills/skill-factory/scripts/*.py:*)
  - Bash(python3 scripts/*.py:*)
---

# /new-skill — Create a New Skill

You have been asked to create a new skill: **$1**

## Process

Follow the skill-factory skill workflow exactly:

### Phase 1: Capture Intent

Ask the user these questions before proceeding:
1. What should this skill enable Claude to do?
2. Is this Track 1 (small/surgical) or Track 2 (multi-step)?
3. What triggers it? (user phrases, contexts)
4. What is the expected output format?
5. Are there PTC opportunities? (grepping, formatting, validation)

Wait for answers before continuing.

### Phase 2: Scaffold

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/skill-factory/scripts/scaffold_skill.py \
  --name "$1" --track <1_or_2_based_on_answers>
```

### Phase 3: Draft SKILL.md

Read `docs/templates/skill-template.md` for structure reference.

Edit the scaffolded SKILL.md to fill in:
- Frontmatter with trigger phrases in description
- Process steps in imperative form
- 2-3 concrete examples
- Anti-patterns
- PTC script references

### Phase 4: Create PTC Scripts

If PTC opportunities were identified, create scripts in `skills/$1/scripts/`.
Follow patterns in `docs/ptc-guide.md`.

### Phase 5: Test

Test the new skill by simulating 2-3 realistic prompts.

### Phase 6: Log

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/progress.py append "Created new skill: $1"
```
