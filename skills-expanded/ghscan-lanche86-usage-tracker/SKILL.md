---
description: Generate a skill from detected usage patterns
argument-hint: "[pattern-id or 'suggest' for recommendations]"
---

The user wants to generate a skill from their usage patterns.

## Process

1. **If no argument provided or argument is "suggest":**
   Run the analyzer to get skill suggestions:
   ```bash
   python3 -c "
   import sys
   sys.path.insert(0, '$HOME/.claude/plugins/marketplaces/usage-tracker-marketplace/scripts')
   from analyzer import suggest_skills
   import json

   suggestions = suggest_skills()
   print(json.dumps(suggestions, indent=2))
   "
   ```

   Present the suggestions to the user and ask which one they want to generate.

2. **If a pattern is specified:**
   Use the skill-generator agent to:
   - Analyze the specific pattern
   - Design an appropriate skill
   - Generate the SKILL.md content
   - Ask user to confirm the location (personal `~/.claude/skills/` or project `.claude/skills/`)
   - Write the skill file

3. **Skill Creation:**
   - Create the skill directory: `~/.claude/skills/[skill-name]/`
   - Write `SKILL.md` with proper frontmatter
   - Confirm creation to user

## Example Interaction

User: `/usage-tracker:generate-skill suggest`
-> Show top 5 skill suggestions with descriptions

User: `/usage-tracker:generate-skill fix-tests`
-> Generate a skill based on the "fix tests" pattern
