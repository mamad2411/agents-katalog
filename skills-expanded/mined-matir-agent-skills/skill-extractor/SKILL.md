---
name: skill-extractor
description: Extracts reusable knowledge and project-specific patterns from work sessions to create new skills. Used to preserve non-obvious solutions and debugging techniques.
allowed-tools:
- Read
- Write
- Glob
- Grep
- WebSearch
- AskUserQuestion
metadata:
  version: 0.2.0
  category: meta
---
# Skill Extractor

## Quick Start
```bash
# Extract learning from the current session with a hint
/skill-extractor the cyclic data DoS fix

# Extract and save to the project directory
/skill-extractor --project
```

## Workflow
1. **Search**: Check existing user and project skills for overlaps or updates.
2. **Identify**: Summarize the problem solved, non-obvious insight, and triggers.
3. **Assess**: Evaluate against quality criteria (reusable, non-trivial, verified).
4. **Detail**: Gather skill name, scope (user/project), and perform research if needed.
5. **Generate**: Create the skill file following the standard template.
6. **Validate**: Run a final checklist for triggers and behavioral guidance.
7. **Save**: Persist the skill to `~/.claude/skills/` or `.claude/skills/`.

## Rules & Constraints
- **Judgment Over Facts**: Prefer teaching how to solve problems over documenting static data.
- **Specific Triggers**: Every skill MUST have identifiable error messages or symptoms.
- **Explicit Confirmation**: Always ask for user confirmation before proceeding with extraction.
- **Why over What**: Documentation MUST explain the trade-offs and rationale, not just steps.
- **Veracity**: Only extract solutions that have been empirically verified as working.

## When to Use
- Solved a non-obvious problem or discovered a non-trivial workaround.
- Identified a project-specific pattern worth preserving for future sessions.
- Found a debugging technique that addresses specific, identifiable symptoms.

## When NOT to Use
- Simple documentation lookups or trivial fixes (typos, obvious bugs).
- One-off configurations or unverified experimental solutions.
- Knowledge already well-documented in official sources.

## References
- [Skill Manual](references/skill-extractor-manual.md)
- [Quality Guide](references/quality-guide.md)
- [Skill Template](references/skill-template.md)
