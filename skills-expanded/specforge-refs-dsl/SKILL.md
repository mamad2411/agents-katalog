---
name: specforge-refs-dsl
description: "Write ref external reference declarations in .spec files. `ref` is one of the five structural keywords of the core grammar, available in every project whatever extensions it loads. Covers the one-line form (ref gh.issue:42 \"Title\"), the block form with metadata, and naming declared refs in an entity's refs list or in prose. Use when linking entities of any domain to outside resources: issues, tickets, designs, SOPs, documents."
---

# SpecForge Refs DSL

> **Structural, not from an extension.** `ref` is one of the five keywords the core grammar knows (`spec`, `ref`,
> `use`, `define`, `defaults`), so it works in every project. The `refs` *field* on an entity exists only when that
> entity's extension declares it -- check with `specforge infer-guide <kind>`.

A `ref` is a typed link to something outside the graph: an issue, a ticket, a design frame, a procedure document.
It becomes a node; entities point at it.

## Block Syntax

### One-Line Declaration (most common)

```spec
ref gh.issue:42 "Track login timeout bug"
ref jira.epic:PROJ-123 "Q2 auth overhaul"
ref docs.sop:QA-017 "Batch release procedure"
```

### Block Form (for metadata)

```spec
ref gh.issue:99 "Performance regression in search" {
  labels   ["performance", "search"]
  priority high
}
```

### Naming a ref from an entity

```spec
ref gh.issue:42 "Track login timeout bug"

behavior fix_login_timeout "Fix Login Timeout" {
  category command
  contract """
    A login MUST complete or fail within 5 seconds.
    See [gh.issue:42] for the original report.
  """
  refs [gh.issue:42]

  verify unit "a stalled identity provider fails the login after 5 seconds"
}
```

An item of a `refs` list must be a declared `ref` (otherwise E003). A `[gh.issue:42]` inside prose is text for
readers and editors; it creates no edge.

## ID Pattern

```
scheme.kind:identifier
```

- `scheme` -- the source (`gh`, `jira`, `figma`, `docs`)
- `kind` -- the resource type within it (`issue`, `pr`, `epic`, `frame`, `sop`)
- `identifier` -- the locator (`42`, `PROJ-123`, `abc123`)

All three parts are required: `mermaid:user-flow` (no kind) does not parse.

## Providers (what is and is not built)

`specforge.json` can list `providers`, and an extension can register a ref scheme. Today that registers the scheme
only: there is no host reader yet, so SpecForge does not fetch, sync or check the linked resource. A ref is a typed,
named link -- not a live connection to GitHub, Jira or any other system. `specforge providers` lists what is
configured.

## Relationships

| From | Field | Meaning |
|------|-------|---------|
| any entity whose kind declares `refs` | `refs` | the entity links to this resource (`links_to` edge) |

Refs are leaf nodes: they reference nothing.

## Writing Rules

1. **Use scheme IDs, not raw URLs** -- `gh.issue:42`, not `https://github.com/...`.
2. **Declare once, reference many times** -- one `ref` per resource, named from every entity that needs it.
3. **Ref IDs are unique** -- one declaration per `scheme.kind:identifier`.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E001 | core | The ID is not `scheme.kind:identifier`. |
| E002 | core | The same ref declared twice. |
| E003 | core | A `refs` item names no declared ref. |
| W012 | core | A ref nothing points at. |
| I005 | core | A scheme no configured provider registers. |

## What NOT to Do

- Do not use refs for links between entities of the graph -- reference the entity's ID directly
- Do not name an undeclared ref in a `refs` list -- declare it first (E003)
- Do not claim a ref is synced with the outside tool -- providers have no reader yet
- Do not put the kind in the identifier -- `gh.issue:42`, not `gh:issue-42`
