---
name: ingest
description: Ingest a source document into the wiki — read it, create/update wiki pages (entities, concepts, sources), update index and log.
argument-hint: '<path to source file, URL, or topic to research>'
model: opus
---

User's request: $ARGUMENTS

# Ingest Source

You are ingesting a source document into the wiki knowledge base. This is the core operation — a single source may touch 10-15 wiki pages as you extract entities, concepts, and connections.

## Vault Discovery

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/vault-discovery.md`.

Store the resolved vault path as `$VAULT`.

## Read Schema

If `$VAULT/CLAUDE.md` exists, read it. It defines vault-specific conventions that override defaults. Follow the schema's rules for everything below.

If no schema exists, follow the default conventions in `${CLAUDE_PLUGIN_ROOT}/references/page-conventions.md`.

## Parse the Source

The user provides one of:
- **A file path** — read the file directly
- **A URL** — fetch the content using `WebFetch`
- **A topic/text** — treat the argument text as the source content itself

### For files:

Read the file. If it's in a supported format (markdown, text, PDF), process it directly.

Copy the raw source to `$VAULT/raw/` if it isn't already there:
- Articles/blog posts → `$VAULT/raw/articles/<kebab-case-name>.md`
- Research papers → `$VAULT/raw/papers/<kebab-case-name>.md`
- Images/assets → `$VAULT/raw/assets/<original-name>`

### For URLs:

Use `WebFetch` to retrieve the content. Save the markdown output to `$VAULT/raw/articles/<kebab-case-name>.md`.

### For topics/text:

No raw file to save. Create pages directly from the provided content.

## Read the Index

Read `$VAULT/wiki/index.md` once. It is a flat catalog of every page — wikilinks and one-line summaries. You will use it throughout ingest to check what already exists.

Do not scan wiki folders. Do not read individual pages yet. Open a specific page only when you are about to update it — not to check whether it exists.

## Read Ingest Workflow

Read `${CLAUDE_SKILL_DIR}/references/ingest-workflow.md` for the detailed step-by-step process.

## Read Page Templates

Read `${CLAUDE_SKILL_DIR}/references/page-templates.md` for the templates to use when creating pages.

## Key Rules

1. **Raw sources are immutable** — never modify files in `raw/`. Always create new files.
2. **Update, don't duplicate** — if an entity or concept page already exists, update it with new information rather than creating a duplicate.
3. **Every page must link** — every new page must have at least one outbound wikilink. Add inbound links from related existing pages.
4. **Update the index** — add every new page to `wiki/index.md`.
5. **Log the operation** — call the log-append script; never read or edit `log.md` directly.
6. **Check for synthesis opportunities** — if the new source connects to existing knowledge in interesting ways, create a synthesis page.

## Done

After ingesting, report:

```
Ingested: <source title>

Pages created/updated:
  Sources:   <list>
  Entities:  <list>
  Concepts:  <list>
  Synthesis: <list if any>

Index updated. Log entry added.

Total wiki pages: <count>
```

Count pages with:
```bash
find "$VAULT/wiki" -name "*.md" ! -name "index.md" ! -name "log.md" | wc -l
```
