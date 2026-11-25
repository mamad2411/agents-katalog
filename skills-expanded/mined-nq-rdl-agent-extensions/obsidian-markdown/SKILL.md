---
name: obsidian-markdown
license: CC-BY-4.0
description: >-
  Create and edit Obsidian notes in Obsidian Flavored Markdown: wikilinks,
  embeds, callouts, block references, properties, tags, and %% comments. Use
  whenever the user mentions Obsidian, an Obsidian note or vault, or works on
  .md files in a vault (a .obsidian/ folder) or with wikilinks, embeds, or
  callouts. Frontmatter or tags in a README or docs site are not, by
  themselves, an Obsidian signal.
compatibility: >-
  Obsidian 1.9+ for property handling as written: plural tags, aliases and
  cssclasses as lists (singular tag/alias/cssclass deprecated in 1.4, removed
  in 1.9). Syntax checked against obsidian-help commit bc5b4f2 on 2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Obsidian Flavored Markdown Skill

Create and edit valid Obsidian Flavored Markdown. Obsidian extends CommonMark and GFM with wikilinks, embeds, callouts, properties, comments, and other syntax. This skill covers only Obsidian-specific extensions -- standard Markdown (headings, bold, italic, lists, quotes, code blocks, tables) is assumed knowledge.

When exact syntax matters and could differ from the tested source, verify it against the canonical docs at https://help.obsidian.md.

## Workflow: Creating an Obsidian Note

1. **Add frontmatter** with properties (tags, aliases, plus any custom properties) at the top of the file. The file name is the note title and link target; a `title:` property is an ordinary custom property. See [PROPERTIES.rst](references/PROPERTIES.rst) for all property types.
2. **Write content** using standard Markdown for structure, plus Obsidian-specific syntax below.
3. **Link related notes** using wikilinks (`[[Note]]`) for internal vault connections, or standard Markdown links for external URLs.
4. **Embed content** from other notes, images, or PDFs using the `![[embed]]` syntax. See [EMBEDS.rst](references/EMBEDS.rst) for all embed types.
5. **Add callouts** for highlighted information using `> [!type]` syntax. See [CALLOUTS.rst](references/CALLOUTS.rst) for all callout types.
6. **Verify** the note renders correctly in Obsidian's reading view.

## Vault Gotchas

- **Follow the vault's link style.** Obsidian writes `[[wikilinks]]` by default, but a vault can turn off *Use [[Wikilinks]]* and use Markdown links. Match what the vault's notes already use. A Markdown internal link needs URL encoding: `[Plan](Q3%20Plan.md)`.
- **Ambiguous names:** if two notes share a name, link with the folder path from the vault root: `[[Projects/Plan]]`.
- **Pipes inside tables:** escape the `|` of an alias or image size: `[[Note\|Alias]]`, `![[chart.png\|200]]`.
- **Links in properties** must be quoted: `related: "[[Other Note]]"`, and list items `- "[[Other Note]]"`.
- **Tags in properties** are a YAML list without `#` (in YAML, `#` starts a comment).
- **Title:** the file name is the note title and link target; renaming the file (with *Automatically update internal links* on) updates links.

## Internal Links (Wikilinks)

```markdown
[[Note Name]]                          Link to note
[[Note Name|Display Text]]             Custom display text
[[Note Name#Heading]]                  Link to heading
[[Note Name#^block-id]]                Link to block
[[#Heading in same note]]              Same-note heading link
```

Define a block ID by appending `^block-id` to any paragraph:

```markdown
This paragraph can be linked to. ^my-block-id
```

For lists, quotes, callouts, and tables, place the block ID on a separate line with a blank line before and after it. Block IDs may contain only Latin letters, numbers, and dashes.

```markdown
> A quote block

^quote-id
```

## Embeds

Prefix any wikilink with `!` to embed its content inline:

```markdown
![[Note Name]]                         Embed full note
![[Note Name#Heading]]                 Embed section
![[image.png]]                         Embed image
![[image.png|300]]                     Embed image with width
![[document.pdf#page=3]]               Embed PDF page
```

See [EMBEDS.rst](references/EMBEDS.rst) for audio, video, search embeds, and external images.

## Callouts

```markdown
> [!note]
> Basic callout.

> [!warning] Custom Title
> Callout with a custom title.

> [!faq]- Collapsed by default
> Foldable callout (- collapsed, + expanded).
```

Common types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`.

See [CALLOUTS.rst](references/CALLOUTS.rst) for the full list with aliases, nesting, and custom CSS callouts.

## Properties (Frontmatter)

```yaml
---
date: 2024-01-15
tags:
  - project
  - active
aliases:
  - Alternative Name
cssclasses:
  - custom-class
---
```

Default properties: `tags` (searchable labels), `aliases` (alternative note names for link suggestions), `cssclasses` (CSS classes for styling). Any other name, such as `date` or `title`, is a custom property; `title` does not change the note title, which is the file name.

See [PROPERTIES.rst](references/PROPERTIES.rst) for all property types, tag syntax rules, and advanced usage.

## Tags

```markdown
#tag                    Inline tag
#nested/tag             Nested tag with hierarchy
```

Tags can contain letters, numbers, underscores, hyphens, forward slashes, and common Unicode characters including emoji, but no spaces. A tag must contain at least one non-numeric character: `#1984` is invalid, `#y1984` is valid. Tags can also be defined in frontmatter under the `tags` property.

## Comments

```markdown
This is visible %%but this is hidden%% text.

%%
This entire block is hidden in reading view.
%%
```

Comments are visible only in Editing view.

## Obsidian-Specific Formatting

```markdown
==Highlighted text==                   Highlight syntax
```

## Math and Diagrams

Math uses `$…$` inline and `$$…$$` blocks (MathJax); diagrams use fenced
`mermaid` code blocks. To link Mermaid nodes to Obsidian notes, add `class NodeName internal-link;`. Quote note names that contain special characters (`class "⨳ special character" internal-link`). These links do not appear in Graph view.

## Footnotes

```markdown
Text with a footnote[^1].

[^1]: Footnote content.

Inline footnote.^[This is inline.]
```

Inline footnotes render only in Reading view, not in Live Preview.

## Complete Example

````markdown
---
date: 2024-01-15
tags:
  - project
  - active
status: in-progress
---

# Project Alpha

This project aims to [[improve workflow]] using modern techniques.

> [!important] Key Deadline
> The first milestone is due on ==January 30th==.

## Tasks

- [x] Initial planning
- [ ] Development phase
  - [ ] Backend implementation
  - [ ] Frontend design

## Notes

The algorithm uses $O(n \log n)$ sorting. See [[Algorithm Notes#Sorting]] for details.

![[Architecture Diagram.png|600]]

Reviewed in [[Meeting Notes 2024-01-10#Decisions]].
````

## References

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Internal links](https://help.obsidian.md/links)
- [Embed files](https://help.obsidian.md/embeds)
- [Callouts](https://help.obsidian.md/callouts)
- [Properties](https://help.obsidian.md/properties)
