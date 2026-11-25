---
name: mykg
description: Universal Knowledge Graph for accumulating and organizing knowledge from any source. Use when ingesting documents, answering questions, maintaining wiki pages, or working with project-specific knowledge bases.
---

# MyKG: Universal Knowledge Graph

An LLM-maintained personal knowledge base. The LLM incrementally builds and maintains a structured wiki of markdown files — reading sources, extracting knowledge, updating pages, and keeping everything connected.

## Setup

### 1. Initialize

```bash
# From kgskills repo
cp -r templates/kg-init/* ~/MyKG
# Or use /kg-init command
```

### 2. Configure Path

```bash
# Option A: Environment variable (add to ~/.bashrc or ~/.zshrc)
export MYKG_PATH="$HOME/MyKG"

# Option B: Config file
mkdir -p ~/.config/mykg
echo "/path/to/your/kg" > ~/.config/mykg/config
```

### 3. (Optional) Use with Obsidian

Point your Obsidian vault at the `MYKG_PATH` for graph view, backlinks, and browsing.

## Optional Skill Integrations

These companion skills from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) enhance mykg when installed.

| Skill | When to use |
|-------|-------------|
| `obsidian-markdown` | Use when creating or editing wiki pages — ensures correct wikilink syntax (`[[Page]]`), frontmatter, callouts, and embeds |
| `obsidian-cli` | Use when the KG lives in an Obsidian vault — open pages, search vault content, navigate notes directly |
| `defuddle` | Use instead of WebFetch when ingesting a URL — strips nav/clutter and returns clean markdown, saving tokens |

If these skills are loaded, prefer them over raw file edits or WebFetch for the relevant operations.

## KG Path Resolution

The skill resolves the KG path in this order:
1. `MYKG_PATH` environment variable
2. `~/.config/mykg/config` file
3. `~/.mykgrc` file
4. Common locations: `~/MyKG`, `~/Dev/Obsidian/MyKG`
5. Ask user for location

## Three Layers

```
┌─────────────────────────────────────────────┐
│              Raw Sources (immutable)         │
│  Papers, articles, transcripts, notes, URLs │
└──────────────────────┬──────────────────────┘
                       │ ingest
                       ▼
┌─────────────────────────────────────────────┐
│              Wiki (LLM-maintained)           │
│  Summaries, entity pages, concepts,         │
│  synthesis, cross-references                │
└──────────────────────┬──────────────────────┘
                       │ query
                       ▼
┌─────────────────────────────────────────────┐
│              Schema (configuration)          │
│  AGENTS.md — tells the LLM how to maintain  │
└─────────────────────────────────────────────┘
```

### Raw Sources (`raw/`)
Immutable source documents. The LLM reads from them but never modifies them. This is the source of truth.

### Wiki (`wiki/`)
LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, synthesis. The LLM owns this layer — it creates pages, updates them, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.

### Schema (`AGENTS.md`)
Tells the LLM how the wiki is structured, what conventions to follow, and what workflows to use. Co-evolve this over time.

## Structure

```
MyKG/
├── index.md              ← Catalog of all pages. START HERE.
├── log.md                ← Chronological change history.
├── AGENTS.md             ← Schema: structure, conventions, workflows.
├── Active.md             ← Current focus items and priorities.
├── raw/                  ← Source documents (immutable).
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   └── notes/
├── wiki/                 ← LLM-generated wiki pages.
│   ├── entities/         ← Pages for specific entities (people, orgs, tools).
│   ├── concepts/         ← Pages for ideas, topics, themes.
│   ├── synthesis/        ← High-level summaries and overviews.
│   └── comparisons/      ← Side-by-side analyses.
└── <Project>/            ← One subdirectory per project.
    ├── SKILL.md          ← Project-specific skill (optional).
    ├── AGENTS.md         ← Project-specific schema (optional).
    ├── raw/              ← Project sources.
    └── wiki/             ← Project wiki pages.
```

## Operations

### Ingest

Read a source, extract knowledge, integrate into the wiki:

1. Read the source document
2. Discuss key takeaways with user
3. Write a summary page in `wiki/`
4. Create/update entity pages in `wiki/entities/`
5. Create/update concept pages in `wiki/concepts/`
6. Note contradictions with existing pages
7. Update `index.md` with new pages
8. Append entry to `log.md`

A single source might touch 10-15 wiki pages. The knowledge compounds.

### Query

Search the wiki, synthesize an answer with citations:

1. Read `index.md` to find relevant pages
2. Drill into specific pages
3. Synthesize an answer
4. **Good answers can be filed back as new wiki pages** — comparisons, analyses, connections discovered during exploration. This way your queries compound too.

### Lint

Periodically health-check the wiki:

- Orphan pages (no inbound links)
- Stale claims superseded by newer sources
- Important concepts mentioned but lacking their own page
- Missing cross-references
- Contradictions between pages
- Data gaps that could be filled with a web search

## Two-Tier Skill System

### Universal Skill (this file)
- KG structure and conventions
- Navigation and search workflows
- Standard operations (ingest, query, lint)
- Cross-project references

### Project Skills (`<Project>/SKILL.md`)
- Domain-specific page types and conventions
- Custom ingestion workflows
- Domain terminology and knowledge
- Project-specific formatting rules

When working on a project, both skills are available:
```
Universal SKILL (always loaded)
    ↓
Project SKILL (loaded when working on that project)
    ↓
Wiki Content (entities, concepts, synthesis)
```

## When to Use

**Use when:**
1. Ingesting a new source → extract and integrate
2. Answering questions → search wiki first
3. Exploring a topic → read wiki pages, follow links
4. Maintaining the wiki → lint, update, cross-reference
5. Starting a new domain → create project with custom SKILL.md

**Don't use for:**
- Code implementation details (project AGENTS.md)
- Ephemeral conversation context (chat history)

## Workflow

### Ingesting a Source
1. Place source in `raw/` (or provide URL/file)
2. Read the source, discuss key takeaways
3. Create/update wiki pages (entities, concepts, synthesis)
4. Update `index.md`
5. Append to `log.md`

### Querying the Wiki
1. Read `index.md` to find relevant pages
2. Read specific pages
3. Synthesize answer with citations (`[[Page Name]]`)
4. Optionally save answer as new wiki page

### Creating a New Project
1. Copy project template: `cp -r project-templates/init "$KG_PATH/ProjectName"`
2. Edit `<Project>/SKILL.md` with domain-specific instructions
3. Edit `<Project>/AGENTS.md` with project schema
4. Update root `index.md`
5. Append to `log.md`

### Linting the Wiki
1. Check for orphan pages
2. Find contradictions between pages
3. Identify missing cross-references
4. Flag stale claims
5. Suggest new sources to investigate

## Page Types

| Type | Location | Content |
|------|----------|---------|
| Entity | `wiki/entities/` | People, organizations, tools, places |
| Concept | `wiki/concepts/` | Ideas, topics, themes, frameworks |
| Synthesis | `wiki/synthesis/` | High-level summaries, overviews |
| Comparison | `wiki/comparisons/` | Side-by-side analyses, trade-offs |
| Source Summary | `wiki/` | Summary of a single source |

## Conventions

### Wikilinks
- `[[Page Name]]` - internal link
- `[[Page Name#Section]]` - deep link
- `[[Page Name|Display Text]]` - alias
- `[[Project/wiki/Page]]` - cross-project link

### Frontmatter
```yaml
---
tags:
  - category
  - subcategory
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/article-name.md
related:
  - [[Related Page]]
---
```

### File Naming
- Lowercase with hyphens: `entity-name.md`
- Wiki pages in appropriate subdirectory
- Raw sources preserve original name or slug

### Status Values
- `draft` - Work in progress
- `in-progress` - Actively being updated
- `complete` - Finished

## Key Files

| File | Purpose |
|------|---------|
| `index.md` | Catalog of all pages - READ FIRST |
| `log.md` | Chronological change history |
| `Active.md` | Current focus items and priorities |
| `AGENTS.md` | Full schema and conventions |
| `raw/` | Immutable source documents |
| `wiki/` | LLM-generated knowledge pages |

## Index Format

`index.md` is content-oriented. Catalog of everything with links and one-line summaries. Organized by category. The LLM reads it first to find relevant pages.

```markdown
## Entities
| Page | Summary | Sources |
|------|---------|---------|
| [[entities/some-person]] | Researcher specializing in X | 3 |

## Concepts
| Page | Summary | Sources |
|------|---------|---------|
| [[concept/topic]] | Overview of topic Y | 5 |
```

## Log Format

`log.md` is chronological. Append-only record of what happened. Consistent prefixes make it parseable:

```markdown
## [2026-04-07] ingest | Article Title
- Added entity pages: X, Y
- Updated concept: Z
- New contradiction noted: A vs B

## [2026-04-06] query | What is X?
- Answer filed as [[concepts/X explained]]
```

Parse with: `grep "^## \[" log.md | tail -5`

## Cross-Project References

Projects can reference each other:
```markdown
Related: [[OtherProject/wiki/concepts/Topic]]
Contradicts: [[OtherProject/wiki/entities/Entity]]
```

## Maintenance

After each session:
1. Update `log.md` with changes
2. Update `index.md` for new pages
3. Update `Active.md` if priorities changed

Periodically:
1. Run `/kg-lint` to find orphans and contradictions
2. Review synthesis pages for completeness
3. Archive stale content