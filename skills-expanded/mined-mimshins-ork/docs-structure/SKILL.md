---
name: docs-structure
description: Use when writing, moving, or maintaining a document under specs/, docs/, or runbook/, and whenever one passes 200 lines. Covers the hub and chunk layout, chunk names, contents lists, relative links, and pnpm docs:check.
---

# docs-structure

## Prerequisites

- The document to change and the tree it belongs to: `specs/`, `docs/`, or
  `runbook/`. `docs/interaction-map/` keeps its own layout (its links are still
  checked).
- Node 24 for `pnpm docs:check` (no other dependency).

## Layout

A long document is a hub plus a folder of chunks:

```
specs/runtime.md                 # hub: title, intro, "## Contents"
specs/runtime/drivers.md
specs/runtime/the-port.md        # a long section: a section hub, same folder
specs/runtime/session-spec.md    # one of The port's chunks
```

- The hub keeps the original path, so links to `runtime.md` keep working.
- Chunks live in the folder named after the hub (`runtime/`), exactly one
  folder level deep.
- A section over ~280 lines becomes a **section hub**: its own file with a
  `## Contents`, its chunks its siblings in the same folder. Never create
  `runtime/the-port/`.
- ADRs (`decisions/`) and RFCs (`rfcs/`) stay atomic: one decision per file. A
  long one gets a `## Contents` list, never a chunk folder.

## Workflow

1. **Decide.** A document over 200 lines is split. At 200 or fewer it stays one
   file. Never split an ADR, an RFC, `AGENTS.md`, `CONTRIBUTING.md`, or
   `README.md`.
2. **Group.** Put sibling sections into chunks of roughly 150–250 lines. A
   chunk holds one section, or two or three adjacent short sections whose names
   read naturally together (`purpose-and-scope`).
3. **Name.** Name the chunk after what is inside, in kebab-case, with no number:
   `drivers.md`, `usage-accounting.md`. A grouped chunk joins the names.
4. **Write the chunk.** `# <section title>`, then
   `_Part of [<Hub title>](../<hub>.md)._` (a section hub's chunk points at the
   section hub: `_Part of [<Section>](./<section>.md)._`), then the body with
   every heading demoted so the chunk's H1 sits above it.
5. **Write the hub.** Keep the H1 and the intro, then `## Contents`: a nested
   list of chunk links and the headings inside them (`chunk.md#anchor`). No
   summaries. A parent lists a section hub and its direct chunks; the section
   hub lists its chunks.
6. **Rewrite links.** A link to a moved anchor points at the chunk that now holds
   it. Links inside a chunk are relative to the chunk's folder. A link without an
   anchor keeps pointing at the hub.
7. **Check.** Run `pnpm docs:check`.

## Adding or moving content later

- New section: add a chunk, list it in the hub's `## Contents`, run the check.
  Split a chunk that passes ~280 lines into a section hub.
- Cross-reference: link the chunk that owns the anchor, never the hub.
- Moving text between documents: move it, do not copy it. A hub holds no
  section body.
- Changing a heading changes its anchor: update every `#anchor` link in the same
  change; the check lists the broken ones, the interaction map's links included
  (`pnpm map:check`).

## Constraints

- Splitting is a move, not a rewrite: do not change facts or wording in the
  same change.
- One home per fact: the chunk holds the text, the hub only the contents.
- Do not rename a chunk casually: its path is a link target.
- Avoid a lone chunk under ~15 lines unless it is a standard section (Purpose,
  Scope, References); group it with a neighbour instead.

## Useful commands

```sh
pnpm docs:check
find specs docs runbook -name '*.md' -not -path 'docs/interaction-map/*' | xargs wc -l | sort -n | tail -20
```

## Expected output

The hub and chunk files in one change, every link updated, and a clean
`pnpm docs:check`.

## References

- [ADR-001](../../../decisions/ADR-001-spec-driven-development.md)
- [runbook/development/docs.md](../../../runbook/development/docs.md)
- [tools/docs/check.ts](../../../tools/docs/check.ts)
