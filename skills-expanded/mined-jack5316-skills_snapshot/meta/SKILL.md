---
name: meta-skill
description: Create new skills following the PAI framework guidelines from CLAUDE.md. Generates Python script templates, SKILL.md files, and guides you through the complete skill creation process.
---

# Meta Skill (/meta-skill)

Create new skills following the Personal AI Infrastructure (PAI) framework guidelines from CLAUDE.md. This skill automates the creation of Python script templates, SKILL.md documentation files, and provides comprehensive guidance through the complete skill creation workflow.

## Quick Start

```bash
# Create a new skill
python3 _scripts/meta_skill.py create my-new-skill "Brief description of my skill"

# Show the skill creation guide
python3 _scripts/meta_skill.py guide

# Show the completion checklist
python3 _scripts/meta_skill.py checklist
```

## Features

1. **Automated Template Generation** - Creates Python script and SKILL.md files following PAI conventions
2. **Interactive Guide** - Shows the complete skill creation process from CLAUDE.md
3. **Completion Checklist** - Provides a verification checklist to ensure skill quality
4. **Naming Convention Enforcement** - Automatically handles hyphenated vs snake_case naming
5. **Best Practices Built-in** - Follows all conventions from the PAI framework

## Options

### Create Command
- `skill_name`: Hyphenated skill name (e.g., my-new-skill) (required)
- `description`: Brief description of what the skill does (required)
- `--features`: List of features for the skill (optional)
- `--output-dir`: Output directory for generated files (default: vault root)

### Guide Command
- No additional options - shows the complete creation guide

### Checklist Command
- No additional options - shows the completion checklist

## Examples

```bash
# Create a basic skill
python3 _scripts/meta_skill.py create weather-digest "Fetch and summarize weather forecasts"

# Create a skill with custom features
python3 _scripts/meta_skill.py create research-assistant "AI-powered research helper" --features "Literature search" "Paper summarization" "Citation management"

# Show the creation guide
python3 _scripts/meta_skill.py guide

# Verify your skill is complete
python3 _scripts/meta_skill.py checklist
```

## Output

When creating a skill, the meta-skill generates:

- **Python script**: `_scripts/my_new_skill.py` - Fully functional template with argparse
- **Skill documentation**: `.claude/skills/my-new-skill/SKILL.md` - Complete documentation
- **Terminal output**: Summary with next steps and skills.json entry snippet

## Usage Workflow

1. **Generate template** - Use `/skill meta-skill create <name> <description>`
2. **Implement logic** - Edit the generated Python script
3. **Update documentation** - Refine the SKILL.md file
4. **Register** - Add to `.claude/skills.json`
5. **Integrate** - Run `/skill gateway --integrate <name> "description"` to see how it fits
6. **Test** - Verify everything works
7. **Verify** - Run `/skill meta-skill checklist` to confirm completeness
