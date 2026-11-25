---
name: md-to-html
description: Convert a Markdown file into a polished, self-contained HTML page with distinctive styling via frontend-design plugin
model: haiku
argument-hint: "<md-file-path> [output-folder] [--style=academic|report|minimal|magazine] [--theme=light|dark]"
allowed-tools: Bash, Read
---

# Markdown → Polished HTML (Template-Based)

Convert an Obsidian Markdown file into a styled HTML page using pandoc + pre-built templates. Fast (~5 seconds).

## How It Works

A Python script (`convert.py` in this skill's directory) handles everything:
1. Extracts YAML frontmatter metadata
2. Preprocesses Obsidian syntax (wikilinks, embeds, checkboxes, comments)
3. Runs pandoc for Markdown → HTML conversion
4. Injects content into a pre-built styled template
5. Client-side JS enhances critique findings into interactive cards

## Workflow

### Step 1: Resolve the file path

Resolve `$ARGUMENTS` into:
- **input_path**: first argument (required), resolved relative to vault root
- **output_dir**: second positional argument (optional)
- **--style=**: optional flag
- **--theme=**: optional flag (light or dark)

If the input path is relative, prepend the vault root (current working directory).

### Step 2: Run the converter

Run the Python script via Bash:

```bash
python3 "{SKILL_DIR}/convert.py" "{input_path}" [output_dir] [--style=X] [--theme=light|dark]
```

Where `{SKILL_DIR}` is the directory containing this SKILL.md file (use the "Base directory for this skill" path from the skill invocation header).

The script outputs a JSON line to stdout with: `input`, `output`, `style`, `title`, `has_math`, `words`.

### Step 3: Report result

Parse the JSON output and display:

```
Done.

Input:  {title} ({words} words)
Style:  {style}
Output: {output}

Open in browser: file://{absolute_output_path}
```

If the script exits with an error, display the stderr message.

## Available Styles

| Style | Aesthetic | Best For |
|-------|----------|----------|
| `academic` | Warm cream, Crimson Pro serif, parchment feel | Papers, critiques, reviews |
| `report` | Dark dashboard, Outfit sans, severity cards, sidebar TOC | Project docs, audits, critiques |
| `minimal` | Extreme negative space, Literata serif, narrow column | Long-form reading, notes |
| `magazine` | Dark editorial, Playfair Display, drop caps, gold accents | Narratives, essays, summaries |

Auto-detection picks the style from document content if `--style=` is not specified.

## Critique Enhancement

The `report` and `academic` templates include client-side JS that automatically detects critique findings (h3 elements matching `F-XX: Title`) and converts them into interactive collapsible cards with severity color-coding. No special markup needed — just standard `/critique` output.

## Requirements

- `pandoc` (installed at /opt/homebrew/bin/pandoc)
- `python3`
