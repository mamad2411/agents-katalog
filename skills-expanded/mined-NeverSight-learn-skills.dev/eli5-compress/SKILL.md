---
name: eli5-compress
description: >
  Compress natural language memory files (CLAUDE.md, todos, preferences) into simple, plain language
  to save input tokens. Simplifies jargon-heavy text while preserving all technical substance,
  code, URLs, and structure. Compressed version overwrites the original file.
  Human-readable backup saved as FILE.original.md.
  Trigger: /eli5-compress <filepath> or "compress memory file"
---

# ELI5 Compress

## Purpose

Compress natural language files (CLAUDE.md, todos, preferences) into plain, simple language to reduce input tokens. Simplifies and shrinks — not just truncation. Compressed version overwrites original. Human-readable backup saved as `<filename>.original.md`.

## Trigger

`/eli5-compress <filepath>` or when user asks to compress/simplify a memory file.

## Process

1. This SKILL.md lives alongside `scripts/` in the same directory. Find that directory.

2. Run:
   ```
   cd <directory_containing_this_SKILL.md> && python3 -m scripts <absolute_filepath>
   ```

3. The CLI will:
   - detect file type (no tokens)
   - call Claude to simplify and compress
   - validate output (no tokens)
   - if errors: cherry-pick fix with Claude (targeted fixes only, no recompression)
   - retry up to 2 times

4. Return result to user

## Compression Rules

### Remove
- Filler: just, really, basically, actually, simply, essentially, generally
- Pleasantries: "sure", "certainly", "of course", "happy to", "I'd recommend"
- Hedging: "it might be worth", "you could consider", "it would be good to"
- Redundant phrasing: "in order to" → "to", "make sure to" → "ensure", "the reason is because" → "because"
- Overly formal language: "ensure that" → "make sure", "utilize" → "use"
- Connective fluff: "however", "furthermore", "additionally", "in addition"

### Simplify
- Rewrite jargon-heavy sentences into plain equivalents
- Use everyday words where possible
- Keep meaning intact — just say it more simply

### Preserve EXACTLY (never modify)
- Code blocks (fenced ``` and indented)
- Inline code (`backtick content`)
- URLs and links (full URLs, markdown links)
- File paths (`/src/components/...`, `./config.yaml`)
- Commands (`npm install`, `git commit`, `docker build`)
- Technical terms (library names, API names, protocols, algorithms)
- Proper nouns (project names, people, companies)
- Dates, version numbers, numeric values
- Environment variables (`$HOME`, `NODE_ENV`)

### Preserve Structure
- All markdown headings (keep exact heading text, simplify body below)
- Bullet point hierarchy (keep nesting level)
- Numbered lists (keep numbering)
- Tables (simplify cell text, keep structure)
- Frontmatter/YAML headers in markdown files

### Compress
- Use short synonyms: "big" not "extensive", "fix" not "implement a solution for", "use" not "utilize"
- Fragments OK: "Run tests before commit" not "You should always run tests before committing"
- Drop "you should", "make sure to", "remember to" — just state the action
- Merge redundant bullets that say the same thing differently
- Keep one example where multiple examples show the same pattern

CRITICAL RULE:
Anything inside ``` ... ``` must be copied EXACTLY.
Do not:
- remove comments
- remove spacing
- reorder lines
- shorten commands
- simplify anything

Inline code (`...`) must be preserved EXACTLY.
Do not modify anything inside backticks.

If file contains code blocks:
- Treat code blocks as read-only regions
- Only compress text outside them
- Do not merge sections around code

## Pattern

Original:
> You should always make sure to run the test suite before pushing any changes to the main branch. This is important because it helps catch bugs early and prevents broken builds from being deployed to production.

Simplified:
> Run tests before pushing to main. Catches bugs early and stops broken builds from reaching production.

Original:
> Ensure that database connection pooling is configured with appropriate timeout parameters to prevent resource exhaustion under high concurrency scenarios.

Simplified:
> Set up database connection pool with good timeouts so it doesn't run out of connections when busy.

## Boundaries

- ONLY compress natural language files (.md, .txt, .markdown, .rst, extensionless)
- NEVER modify: .py, .js, .ts, .json, .yaml, .yml, .toml, .env, .lock, .css, .html, .xml, .sql, .sh
- If file has mixed content (prose + code), compress ONLY the prose sections
- If unsure whether something is code or prose, leave it unchanged
- Original file is backed up as FILE.original.md before overwriting
- Never compress FILE.original.md (skip it)
