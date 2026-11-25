---
name: notion-specification
description: Write or maintain a specification in a Notion documentation space. Covers the workspace coordinates to record, the tool-level traps that silently destroy content, and where the house style lives. Triggers - "write a spec for X", "document X in Notion", "update the X specification", "add a variables database", "promote this draft to Specifications", "why did my Notion database disappear".
---

# Notion specifications

**Style, structure and process belong in a style-guide page inside the space itself. Fetch it before
writing or editing anything.** A guide in Notion is readable by every team rather than only one repo, and
it should cover research order, page shape, prose rules, ownership, formatting, variables, metadata,
lifecycle and review. If the space has no guide yet, the skeleton below is the fallback.

This file carries only what that page cannot: the identifiers, the exact tool calls, and the repo-local
tooling. A line that would read identically for every team belongs in Notion alone.

**Preview before writing, whether or not the connector will let you write.** A page other teams read is a
shared surface, and a write reaches it with no review step of its own, so a draft or a revision is shown as
an HTML preview and authorised by its owner before anything lands. The `notion-preview` skill owns that
rendering, the Previous / Proposed / Diff review switch, and both routes into Notion. Read this file for
what a page says, that one for how it is shown and handed over.

Connector write access can be revoked and restored without notice, so check it with `get_tool_access`
rather than assuming either state. Availability changes the route, never the review gate.

## Workspace coordinates

Record these once per workspace. Page ids are 32 hex characters; data-source ids are the dashed UUID from
the `collection://` URL that `notion-fetch` returns for a database.

| Thing | ID |
|---|---|
| Documentation hub | `<page-id>` |
| Style guide | `<page-id>` |
| Specifications data source | `<data-source-id>` |
| Specifications database page | `<page-id>` |
| Specification template (registered default) | `<page-id>` |
| Proposals data source (if any) | `<data-source-id>` |

Keep the filled table out of any public repository — a copy of this skill under the project's own
`.claude/skills/` or the project `CLAUDE.md` is the right home. List two or three well-shaped
specifications as worked examples alongside it; imitating a live page teaches house style faster than a
rule list.

## Section skeleton

Enough to produce a correctly-shaped page if the guide is unreachable. Every section reads: heading →
permanent italic tagline → `<details>` prompt → `---` → content.

```
Lead paragraph, then table of contents
Background
Behaviour by version and product
Architecture
  Variables · Communication · Storage · Configuration
Testing and Assurance
Open decisions
```

## Changing a page

Held by `notion-editing`, and by `notion-database` for a schema, a view or a registry row. The traps they
carry bite whatever is being edited, and anyone changing a registry or a releases database never reaches a
specification skill.

## Repo-local tooling

- **Diagrams**: render every Mermaid block through `mmdc` before publishing. Notion clips long node
  labels. Where the layout has to be chosen rather than computed, or the figure is meant to be clicked, it
  becomes an HTML block instead — see the `notion-diagram` skill.
- **Scratch files**: a directory outside the repo, never under `.claude/`.
