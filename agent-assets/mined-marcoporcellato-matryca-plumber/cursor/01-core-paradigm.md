---
description: Core paradigm rules for Logseq OG (Markdown outliner vs flat text)
globs: *
---

## Project context
This repository builds Matryca Plumber, a local-first, background AI daemon and engine that operates directly on **Logseq OG** (local, pure Markdown graph notes) file systems.

**SSOT:** full paradigm spec lives in [`docs/openspec/agent/paradigm.md`](docs/openspec/agent/paradigm.md). Pointer: [`docs/openspec/logseq-paradigm.md`](docs/openspec/logseq-paradigm.md). This rule is the Cursor summary only.

## Outliner paradigm (non-negotiable)
- Logseq OG uses **pure Markdown files**. The atomic unit is the **block**: an indented bullet point that forms a tree, not a flat document body.
- When generating or editing content, produce **hierarchical outliner text** (nested bullets). 
- **Bulleted Headings:** AI-generated sections must use `- ### Heading Title` to ensure they are foldable in the Logseq outliner.
- **Co-working assumption:** Humans and the daemon edit the **same** `.md` files concurrently. Favor diffs that preserve indentation, block order, and `id::` lines.

## Properties Rules (CRITICAL)
- **Block Properties:** Must be placed immediately after the bullet text, before any indented children. They must be indented by exactly 2 spaces relative to the parent bullet (e.g., `id:: <uuid>`, `matryca-plumber:: true`). NEVER orphan or delete existing block properties.
- **Page Properties:** Must reside in the **Absolute Frontmatter** at the top of the file (Line 0). They are raw text `key:: value` lines WITHOUT bullet dashes (`- `), separated by a blank line before the first bullet.
- **Lists:** `alias::` and `tags::` are comma-separated lists. Do not duplicate keys. Strip markdown (`#`, `[[ ]]`) from their values.

## File System & Namespaces
- **Semantic vs Physical:** In memory/content, use `/` (e.g., `[[Domain/Subdomain]]`). On disk, use Logseq's encoding: replace `/` with `___` and URL-encode reserved OS characters (e.g., `?` -> `%3F`).
- **Encoding:** ALL file read/write operations must strictly use `encoding="utf-8"`.