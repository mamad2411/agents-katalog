---
name: templater
description: Quickly create Obsidian templates. Create templates from built-in types (daily, meeting, project, permanent, fleeting) or generate custom templates from descriptions. Use when you want to create an Obsidian template, add a new note template, or /templater.
---

# Templater Skill (/templater)

Quickly create Obsidian note templates with YAML frontmatter and Templater syntax. Supports built-in template types and AI-generated custom templates from natural language descriptions.

## Quick Start

```bash
# List existing templates in vault
python3 _scripts/templater_skill.py list

# Create from built-in type (preview)
python3 _scripts/templater_skill.py create daily

# Create and save to Templates/
python3 _scripts/templater_skill.py create meeting --save

# Create custom template from description (AI-generated)
python3 _scripts/templater_skill.py create "Book review with quotes and rating" --save

# Show a template's content
python3 _scripts/templater_skill.py show "Daily Note"
```

## Features

1. **List** - Browse all templates in the vault's Templates folder
2. **Create from type** - Use built-in templates (daily, meeting, project, permanent, fleeting, literature, moc, experiment)
3. **Create from description** - AI generates a custom template from your description
4. **Show** - Display any template's full content
5. **Types** - List available built-in types with descriptions

## Built-in Template Types

| Type | Description |
|------|-------------|
| `daily` | Daily note with intention, tasks, learnings, and reflection |
| `meeting` | Meeting notes with attendees, agenda, decisions, action items |
| `project` | Project tracking with outcome, actions, tasks, and log |
| `permanent` | Evergreen note - one idea that stands on its own |
| `fleeting` | Quick capture for raw thoughts and inbox processing |
| `literature` | Notes from reading - quotes, summary, and connections |
| `moc` | Map of Content - hub note linking related notes |
| `experiment` | Structured log for experiments and tests |

## Options

### list
- No options - lists all templates in `Templates/`

### create
- `source`: Built-in type (e.g., daily, meeting) OR description for AI-generated template (required)
- `--name`, `-n`: Custom filename without .md
- `--save`, `-s`: Save to `Templates/` folder

### show
- `name`: Template filename without .md (supports partial match)

### types
- `--verbose`, `-v`: Show template content preview

## Examples

```bash
# List vault templates
python3 _scripts/templater_skill.py list

# Preview daily template (no save)
python3 _scripts/templater_skill.py create daily

# Create and save meeting template
python3 _scripts/templater_skill.py create meeting --save

# Create custom template with custom name
python3 _scripts/templater_skill.py create "Weekly review with wins and learnings" --name "Weekly Review" --save

# Create book notes template
python3 _scripts/templater_skill.py create "Book notes with author, key ideas, and action items"

# Show existing template
python3 _scripts/templater_skill.py show "Daily Note"

# List built-in types
python3 _scripts/templater_skill.py types
```

## Output

- **list**: Markdown list of template wikilinks
- **create**: Full template markdown (printed to terminal; saved to `Templates/` if `--save`)
- **show**: Full template content
- **types**: Table of built-in types with descriptions

## Template Conventions

All templates follow vault conventions:
- YAML frontmatter with `created` (Templater date) and `tags`
- Templater syntax: `{{date:YYYY-MM-DD}}`, `{{title}}`
- Type tags: `type/daily`, `type/project`, `type/fleeting`, etc.
- Status tags: `status/inbox`, `status/processing`, `status/evergreen`
- Task checkboxes `- [ ]` for action items
- Blockquotes `>` for section hints

## Related

- [[Prompt Template]] - For AI prompt templates
- [[Daily Note]] - Daily note template
- [[Meeting Note]] - Meeting notes template
