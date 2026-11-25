---
name: obsidian-markdown
description: Create and edit Obsidian flavored Markdown notes with wikilinks, embeds, callouts, properties, tags, comments, highlights, footnotes, Mermaid, and Obsidian-specific syntax. Use when working with Obsidian .md notes, vault content, wikilinks, callouts, frontmatter, tags, or embeds.
---

# Obsidian Markdown

Use this skill to create valid Obsidian notes.

## Workflow

1. Add properties
   - Put YAML frontmatter at the top when the note needs metadata.
   - Use `title`, `tags`, `aliases`, `status`, `date`, or project-specific properties when appropriate.

2. Structure the note
   - Use standard Markdown headings and lists.
   - Keep headings linkable and specific.
   - Use task checkboxes for actionable items.

3. Link the vault
   - Use `[[Note Name]]` for internal notes.
   - Use `[[Note Name|Display Text]]` when the note title is not natural in prose.
   - Use normal Markdown links only for external URLs.

4. Add Obsidian syntax when useful
   - Embeds: `![[Note Name]]`, `![[image.png|300]]`
   - Callouts: `> [!note]`, `> [!warning] Custom Title`
   - Tags: `#tag` or `#nested/tag`
   - Comments: `%% hidden comment %%`
   - Highlights: `==highlighted text==`

5. Verify
   - Check frontmatter is valid YAML.
   - Check wikilinks point to intended note names.
   - Check callout syntax has `>` on each line.

## Common Patterns

```markdown
---
title: Project Alpha
tags:
  - project
  - active
status: in-progress
---

# Project Alpha

Related: [[Project Index]]

> [!important] Decision
> Use the existing sync pipeline for the first release.

## Tasks

- [ ] Confirm owner
- [ ] Draft implementation plan
```

## Rules

- Prefer wikilinks for vault-internal references.
- Do not use external URL syntax for internal notes.
- Keep tags lowercase unless the vault already uses another convention.

## Output Format

End with:

- Notes created or changed
- Properties, tags, and links added
- Obsidian syntax used
- Validation performed
