---
name: obsidian-vault-workflow
description: "Operate across an Obsidian vault: organize notes, maintain links, normalize tags and properties, create indexes, update maps of content, and preserve vault conventions. Use when the user asks to clean, organize, connect, refactor, or maintain an Obsidian vault."
---

# Obsidian Vault Workflow

Use this skill when working across multiple notes.

## Workflow

1. Discover conventions
   - Inspect existing folder names, note titles, tags, properties, templates, and index notes.
   - Follow local style before introducing a new one.

2. Plan the change
   - Identify affected notes.
   - Preserve existing links.
   - Decide whether to create backlinks, index notes, or maps of content.

3. Edit carefully
   - Update frontmatter consistently.
   - Use wikilinks for internal relationships.
   - Keep aliases when renaming concepts.
   - Avoid breaking embedded files or block references.

4. Create navigation
   - Add index notes when a topic has multiple related notes.
   - Use sections like Overview, Notes, Projects, Questions, and Related.
   - Link both directions when a relationship is important.

5. Verify
   - Check YAML frontmatter.
   - Check changed wikilinks.
   - Check renamed or moved files have aliases or updated references.

## Rules

- Do not mass-rename notes without explicit user approval.
- Do not flatten a vault's existing structure just to make it neat.
- Prefer incremental cleanup with clear before/after behavior.
- Keep private or personal note content intact unless asked to rewrite it.

## Output Format

End with:

- Notes changed
- Links, tags, or properties updated
- Indexes or canvases created
- Validation performed
- Anything intentionally left untouched
