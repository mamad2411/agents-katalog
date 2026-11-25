---
name: dev-research
description: >
  Use NotebookLM for grounded research — documentation queries, stack comparisons, session log search.
  Trigger when user needs answers FROM SPECIFIC DOCUMENTATION or FROM PAST SESSIONS:
  "по документации", "check docs", "как в Payload", "как в Next.js",
  "что мы решили про", "when did we decide", "по нашим записям",
  "спроси в нотбуке", "ask notebooklm", "query notebook",
  "загрузи доки", "load docs", "add to notebook",
  "найди в сессиях", "search sessions", "когда мы делали".
  Also for structured comparisons: "сравни X и Y по документации", "compare based on docs".
  Requires notebooklm-py. For WEB research (current info, trends), use deep-research skill instead.
---

# Dev Research Skill

Integrates NotebookLM into development workflow for grounded, citation-backed research. Uses notebooklm-py CLI for all NotebookLM interactions.

## Prerequisites
```bash
# Check if notebooklm-py is installed
which notebooklm || echo "Install: pip install 'notebooklm-py[browser]'"

# Check auth
notebooklm auth check --test
```

## Notebooks Convention

Each dev notebook follows naming: `[Project] — [Purpose]`

Examples:
- "Crypto Portal — Stack Docs" (Payload CMS, Next.js docs)
- "AI News Portal — CMS Research" (comparing CMS options)
- "Dev Sessions Archive" (all session logs for cross-project search)

## Commands

### /research TOPIC
Research a topic using NotebookLM's grounded answers.

```bash
# Check if relevant notebook exists
notebooklm list 2>/dev/null | grep -i "TOPIC"

# If not, create one
notebooklm create "Research — TOPIC"
notebooklm use <notebook_id>

# Add sources — user provides URLs, or we search
notebooklm source add "URL1"
notebooklm source add "URL2"
notebooklm source add "./local-doc.md"

# Ask questions
notebooklm ask --json "QUESTION"
```

Parse JSON response and extract:
- Answer text
- Citations with source references
- Confidence indicators

### /docs-query QUESTION
Query project documentation notebook.

```bash
# Use the project's docs notebook
notebooklm use <project-docs-notebook-id>
notebooklm ask --json "QUESTION"
```

This gives grounded answers from actual documentation, not hallucinations.

### /compare OPTION1 vs OPTION2
Create a structured comparison using NotebookLM.

```bash
notebooklm create "Comparison — OPTION1 vs OPTION2"
# Add documentation for both options
notebooklm source add "URL_OPTION1_DOCS"
notebooklm source add "URL_OPTION2_DOCS"

# Structured comparison questions
notebooklm ask --json "Compare OPTION1 and OPTION2 for: performance, DX, ecosystem, production readiness"
notebooklm ask --json "What are the main trade-offs between OPTION1 and OPTION2?"
notebooklm ask --json "Which is better for: [specific use case]?"

# Generate mind-map for visual comparison
notebooklm generate mind-map
notebooklm download mind-map ./vault/research/COMPARISON.json
```

### /load-docs PROJECT
Load current project documentation into NotebookLM.

```bash
PROJECT_NAME=$(basename $(git rev-parse --show-toplevel 2>/dev/null || pwd))
VAULT=${VAULT_PATH:-~/vault}

# Create or reuse notebook
notebooklm create "$PROJECT_NAME — Documentation"

# Add from vault
for f in "$VAULT/projects/$PROJECT_NAME/decisions/"*.md; do
  notebooklm source add "$f"
done

# Add architecture docs from project
find . -name "*.md" -maxdepth 2 | head -20 | while read f; do
  notebooklm source add "$f"
done

echo "Loaded docs for $PROJECT_NAME into NotebookLM"
```

### /archive-sessions
Upload session logs to NotebookLM for cross-project search.

```bash
VAULT=${VAULT_PATH:-~/vault}

# Use or create archive notebook
notebooklm create "Dev Sessions Archive"

# Upload recent sessions from all projects
for project_dir in "$VAULT/projects"/*/sessions/; do
  for session in $(ls -t "$project_dir"*.md 2>/dev/null | head -10); do
    notebooklm source add "$session"
  done
done
```

Now you can ask: "When did we last deal with caching issues?" across all projects.

## Output to Obsidian

All NotebookLM research outputs go to the vault:

```bash
VAULT=${VAULT_PATH:-~/vault}

# Mind maps
notebooklm download mind-map "$VAULT/research/TOPIC-mindmap.json"

# Research notes (from JSON answers)
# Parse and format as Obsidian markdown with wikilinks
```

### Formatting NotebookLM answers for Obsidian

When saving answers to vault:
1. Convert citations to wikilinks: `[1]` → `[[Source Name#passage]]`
2. Add YAML frontmatter: date, notebook, question, sources
3. Create topic files if they don't exist
4. Add backlinks from source files

Example output file:
```markdown
---
date: 2026-04-06
notebook: "Crypto Portal — Stack Docs"
question: "How does Payload CMS handle field hooks?"
sources: ["Payload CMS Docs", "Next.js Integration Guide"]
---

# How Payload CMS handles field hooks

[answer with wikilinks to sources]

## Sources
- [[Payload CMS Docs]] — field lifecycle
- [[Next.js Integration Guide]] — integration patterns
```

## Audio Briefings

Generate audio briefing for a project:

```bash
notebooklm generate audio "Brief project status and key decisions" --wait
notebooklm download audio "$VAULT/projects/$PROJECT/briefing-$(date +%Y-%m-%d).mp3"
```

Listen on phone via Obsidian Sync while commuting.

## Limitations & Notes

- Rate limit: ~50 queries/day on free Google account
- NotebookLM uses undocumented Google APIs — may break
- Browser automation requires local Chromium — won't work in Docker devcontainer
- Sources max: 300 per notebook
- Best for: documentation, comparisons, cross-source search
- NOT for: running code, real-time data, live APIs
