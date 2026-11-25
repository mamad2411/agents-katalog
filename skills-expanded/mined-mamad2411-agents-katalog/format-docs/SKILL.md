---
name: format-docs
description: "Format and restructure markdown documents so they publish cleanly to Confluence via `orbit confluence publish`. Use this skill whenever the user wants to prepare docs for Confluence, fix markdown formatting for wiki publishing, add frontmatter to docs, restructure a docs directory, or ensure markdown files follow Confluence-friendly conventions. Also trigger when the user says things like 'format these docs', 'prepare docs for Confluence', 'fix the frontmatter', 'restructure the docs folder', 'make these docs publishable', 'clean up the markdown', or any task involving making markdown Confluence-ready — even if they just say 'format this' or 'prep for wiki' without mentioning Confluence explicitly. If the user has a docs/ directory and mentions publishing or syncing, this skill applies."
---

# Format Docs

Prepare markdown documents for clean Confluence publishing via `orbit confluence publish`. This skill analyzes and transforms markdown files — individually or as a directory tree — to follow the conventions that Confluence expects.

## When to Use

- Before running `orbit confluence publish` for the first time on a docs directory
- When adding new markdown files to an existing published docs tree
- When docs render poorly in Confluence and need structural fixes
- When migrating docs from another system (GitHub wiki, Notion export, etc.)

## Process

### 1. Assess the Scope

Determine whether the user is asking about a single file or a directory.

- **Single file**: Read it and apply the file-level checks below.
- **Directory**: List the full tree, then work through both directory-level and file-level checks.

### 2. Directory-Level Checks

If formatting a directory, verify and fix these structural issues:

**INDEX.md files** — Every directory that contains markdown files needs an `INDEX.md`. This file becomes the parent page in Confluence for all sibling `.md` files.

```
docs/
  INDEX.md              ← Required: parent page for docs/
  overview.md
  api/
    INDEX.md            ← Required: parent page for api/
    endpoints.md
```

If an `INDEX.md` is missing, create one with:
- Frontmatter (title from directory name, today's date)
- A brief intro line
- A properties report directive (see below)
- Child page tables wrapped in confluence ignore blocks

**INDEX.md structure** — Every INDEX.md must follow this pattern:

```markdown
---
title: "Section Title"
# ... full frontmatter ...
confluence_labels:
  - my-label
---

# Section Title

> Brief intro summarizing the section.

---

<!-- confluence:properties-report cql="ancestor = currentContent() AND label = 'my-label'" firstcolumn="Title" headings="Owner,Status,Version,Reviewed on" -->

<!-- confluence:ignore-start -->

## Subsection Name

| Document | Version | Summary |
|----------|---------|---------|
| [Child Page](./child-page.md) | v1.0 | Brief description |

<!-- confluence:ignore-end -->
```

Key rules for INDEX.md files:

1. **Properties report directive** — Add a `<!-- confluence:properties-report -->` directive after the intro content. This generates a dynamic table on Confluence that pulls metadata from all child pages sharing the same label. Use `ancestor = currentContent()` to scope to child pages, and match the label from `confluence_labels`.
2. **Confluence ignore blocks** — Wrap **all child page listing content** (section headings, tables, links) between `<!-- confluence:ignore-start -->` and `<!-- confluence:ignore-end -->`. This content is only visible in markdown viewers (GitHub, local); on Confluence, the properties report replaces it.
3. **Label alignment** — The `label` value in the CQL query must match one of the `confluence_labels` defined in the child pages' frontmatter. Use the same label across all siblings so the report captures them all.
4. **Report headings** — Include at minimum: `Owner,Status,Version,Reviewed on`. These must match field names in the children's `confluence_properties`.

**File naming** — Rename files that would cause URL issues:
- Use lowercase with hyphens: `api-reference.md` not `API Reference.md`
- No spaces, underscores, or special characters in filenames
- No version numbers in filenames — track versions in frontmatter instead

**Flat nesting** — Confluence page trees work best with one level of topic directories under the root. If the directory has deeply nested subdirectories (3+ levels), suggest flattening.

### 3. File-Level Checks

For each markdown file, check and fix the following. Read the [formatting reference](./references/formatting.md) for detailed rules on each item.

#### Frontmatter

Every file needs YAML frontmatter with **all standard fields** populated. Frontmatter is the single source of truth for document metadata — any metadata that exists in the frontmatter must NOT be duplicated in the document body.

**Always use the full frontmatter template:**

```yaml
---
title: API Reference
subtitle: "Reference — Project Docs v1.0"
date: "2026-03-09"
author: "Engineering Team"
confluence_ignore: false
confluence_labels:
  - api
  - reference
confluence_properties:
  - id: status
    fields:
      Owner: "Engineering Team"
      Classification: Internal
      Status: "{status:Green|Published}"
      Version: v1.0
      Reviewed on: 2026-03-05
---
```

When adding or completing frontmatter:
- Derive `title` from the first `# heading` if present, otherwise from the filename
- Set `date` to today's date
- Derive `author` from inline metadata if present, otherwise from existing sibling files or ask the user
- Derive `subtitle` from document context (e.g., `"ADR — Project v1.0"`, `"Guide — Team Docs"`)
- Suggest `confluence_labels` based on the directory name and content
- **Always include `confluence_properties`** with at minimum: `Owner`, `Classification`, `Status`, `Version`, and `Reviewed on`
- Populate property values from inline metadata found in the document body when available
- Set `confluence_ignore: false` by default. Only set to `true` when the user explicitly wants to exclude a file from Confluence publishing (previously published pages will be deleted on next sync)
- Never overwrite existing `confluence_page_id` or `confluence_url`

#### Remove Redundant Inline Metadata

After populating the frontmatter, **remove any inline metadata blocks** from the document body that duplicate information already captured in the frontmatter or `confluence_properties`. These blocks typically appear near the top of the document as bold-key/value lines or small tables.

**Patterns to detect and remove:**

```markdown
**Document Version**: 1.0
**Status**: Draft (Proposal)
**Classification**: Internal
**Last Updated**: March 7, 2026
**Author**: Engineering Team
**Owner**: Platform Team
```

Also detect and remove metadata presented as:
- Key-value lines: `Version: 1.0` or `Status: Draft`
- Small two-column tables with metadata-like headers (e.g., `| Field | Value |`)
- Blockquote metadata: `> **Version**: 1.0`

**Rules for removal:**
- Only remove metadata lines/blocks where the information is already captured in frontmatter fields or `confluence_properties` fields
- If an inline metadata block contains values not yet in frontmatter, **absorb them into frontmatter first**, then remove the block
- Preserve any surrounding content — only strip the metadata lines themselves
- If the metadata block is followed by a blank line or horizontal rule, remove the separator too to avoid orphaned whitespace

#### Heading Hierarchy

The converter skips the first `# heading` (Confluence uses the page title instead), so the document body should use `##` as the top-level section heading.

Fix these issues:
- **Multiple `#` headings** — Keep only the first one (it becomes the title). Convert subsequent `#` to `##`.
- **Heading gaps** — Don't jump from `##` to `####`. Fill in the hierarchy.
- **No `#` heading** — If the file has no `#` heading but has a `title` in frontmatter, that's fine. If it has neither, add a `#` heading derived from the filename.

#### Document Structure

Well-structured documents follow this pattern:

```markdown
# Title

> One-line summary of what this document covers.

<!-- confluence:toc-start -->

## Table of Contents

1. [Section One](#section-one)
2. [Section Two](#section-two)

<!-- confluence:toc-end -->

---

## Section One

Content...

---

## Section Two

Content...
```

Apply these structural improvements:
- **Add a TOC** if the document has 3+ sections (`##` headings). Wrap the TOC section (heading + list) with `<!-- confluence:toc-start -->` / `<!-- confluence:toc-end -->` directives so it gets replaced with the Confluence TOC macro on publish. The markdown TOC remains visible in GitHub/local renderers.
- **Add horizontal rules** (`---`) between major sections for visual separation.
- **Add a summary blockquote** after the title if the document jumps straight into content without context.

#### Cross-References

If the file is part of a directory being formatted, add a Cross-References section near the bottom linking to related sibling documents:

```markdown
## Cross-References

| Document | Relevance |
|----------|-----------|
| [Related Doc](./related-doc.md) | Brief note on why it's relevant |
```

Use relative paths so links resolve correctly both locally and in Confluence.

#### Revision History

For documents that will be actively maintained, add a revision history table at the bottom:

```markdown
## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-09 | Initial document |
```

Only add this if the document doesn't already have one.

### 4. Content Formatting

Fix markdown patterns that don't convert well to Confluence:

| Issue | Fix |
|-------|-----|
| Inline metadata blocks (`**Status**: Draft`, etc.) | Absorb into frontmatter/`confluence_properties`, then remove from body |
| Raw HTML tags | Replace with markdown equivalents |
| `<br>` tags | Use blank lines instead |
| Deeply nested lists (3+ levels) | Flatten to 2 levels max |
| Tables with multi-line cells | Split into simpler tables |
| Inline images with relative paths | Verify paths are correct relative to the file |
| GitHub-flavored alerts (`> [!NOTE]`) | Keep as-is — the converter handles these |
| MkDocs admonitions (`!!! note`) | Keep as-is — the converter handles these |

### 5. Confluence-Specific Enhancements

These are optional improvements that use Confluence features:

- **Status badges** — Use `{status:Color|Text}` syntax in property fields (e.g., `{status:Green|Published}`)
- **Confluence ignore blocks** — Wrap sections that should only appear in markdown (not Confluence) with `<!-- confluence:ignore-start -->` and `<!-- confluence:ignore-end -->`. In INDEX.md files, all child page tables must be wrapped (see Directory-Level Checks above).
- **Properties report** — Every INDEX.md must include a properties report directive. See the INDEX.md structure in Directory-Level Checks for the exact pattern.

### 6. Dry Run

After making changes, suggest the user verify with:

```bash
orbit confluence publish <directory> --space <SPACE> --parent <PAGE_ID> --dry-run -p <profile>
```

This previews what would be published without making changes.

## Rules

- Never delete content — only restructure and add metadata.
- Never overwrite `confluence_page_id` or `confluence_url` — these are managed by `orbit confluence publish`.
- Preserve existing frontmatter fields — add missing ones, don't remove existing ones.
- When in doubt about a title, derive it from the `# heading` first, then from the filename.
- Keep changes minimal — don't rewrite prose, don't reorganize sections unless the heading hierarchy is broken.
- Show the user a summary of changes before applying them to a large directory.
