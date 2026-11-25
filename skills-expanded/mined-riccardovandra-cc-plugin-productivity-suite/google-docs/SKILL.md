---
name: google-docs
description: Create and update Google Docs from markdown files. Convert local markdown to cloud documents with formatting preserved. Use when user asks to create a Google Doc, convert markdown to Google Docs, or update an existing doc.
---

# Google Docs Skill

Create and update Google Docs from markdown files with formatting preserved.

## Quick Start

```bash
# Create new Google Doc from markdown
uv run scripts/create.py document.md --title "My Document"

# Create in specific folder
uv run scripts/create.py report.md --title "Q4 Report" --folder "Reports"

# Update existing doc
uv run scripts/update.py changes.md --doc-id "1abc123..."
```

## Available Operations

| Operation | Module | Script | Description |
|-----------|--------|--------|-------------|
| Create | [CREATE.md](modules/CREATE.md) | `create.py` | Create new Google Doc from markdown |
| Update | [UPDATE.md](modules/UPDATE.md) | `update.py` | Update existing Google Doc |

## First-Time Setup

This skill uses the shared Google OAuth integration:

```bash
uv run ~/.claude/plugins/cache/riccardovandra/cc-plugin-productivity-suite/integrations/google/scripts/oauth_setup.py --add-scope documents --add-scope drive
```

See the plugin README for full setup instructions.

## Supported Markdown Features

| Markdown | Google Docs Result |
|----------|-------------------|
| `# H1` | Title/Heading 1 |
| `## H2` | Heading 2 |
| `### H3` | Heading 3 |
| `#### H4` | Heading 4 |
| `**bold**` | Bold text |
| `*italic*` | Italic text |
| `- bullet` | Bullet list |
| `1. numbered` | Numbered list |
| `` `code` `` | Monospace text |
| Tables | Native Google Docs tables (bold header) |
| Code blocks | Monospace paragraphs with gray background |

## Activation Triggers

- "create google doc", "make a google doc"
- "convert to google docs", "export to google docs"
- "update google doc", "sync to google doc"
- "markdown to google docs"

## Output

Scripts output the Google Doc URL for easy access:
```
Created: https://docs.google.com/document/d/1abc.../edit
```
