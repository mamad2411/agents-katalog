# Tags — curation hints

> **License:** tag entities here are released into the public domain under
> CC0 1.0 alongside the rest of the catalog data — see
> [`../LICENSE-DATA`](../LICENSE-DATA) and [`../DISCLAIMER.md`](../DISCLAIMER.md).

`tags/` is a sibling of `collections/`, not a part of it — a tag is a
cross-cutting label that can apply to entities anywhere across the whole
catalog, so it doesn't belong inside any one domain family or category. See
[`docs/primitives/TAG.md`](../docs/primitives/TAG.md) for the full
reference, and [`collections/CLAUDE.md`](../collections/CLAUDE.md)'s
"Tags" section for how an item or collection actually references one.

## Directory structure

```
tags/
  CLAUDE.md
  item-attributes.schema.json  # standard schema, shared by every namespace
  <namespace>/                  # e.g. franchises/
    _collection.yaml            # the namespace's own record
    <slug>.yaml                 # one tag entity per file
```

Structurally, `tags/` mirrors `collections/`: a namespace directory is the
same kind of node a domain family or category is (its own `_collection.yaml`,
inherited `CLAUDE.md`/`item-attributes.schema.json`), and an individual tag is a
leaf entity the same way a card or a set is. The validator applies the same
rules to both trees.

Only one namespace exists so far: `franchises/`, for franchise/IP tags (see
[`franchises/_collection.yaml`](franchises/_collection.yaml)). Add a new
namespace directory only when a genuinely different kind of cross-cutting
grouping shows up (e.g. a seasonal/exclusive-release status) — don't
subdivide `franchises/` itself or invent a namespace speculatively.

## Tag entities

A tag is `id`/`name`/`type: tag`, nothing more, for now — **one standard
schema for every namespace**, no per-namespace `attributes`. `name` is the
tag's proper display form (`Pokémon`, not `pokemon`; `Assassin's Creed`, not
`assassins-creed`) — get the punctuation, accents, and casing right, since
this is the only place that display form is recorded at all.

```yaml
id: 175817b0-ba6b-49ca-90a9-f0777b4149e4
name: Pokémon
type: tag
```

**Quote `name` in YAML whenever it contains a colon, apostrophe, or comma**
— `name: Magic: The Gathering` is a real parse error (a bare `: ` inside an
unquoted scalar is read as a second mapping key), not just a style
preference. Use a double-quoted string in exactly those cases:
`name: "Magic: The Gathering"`.

## Naming files

`<slugified-name>.yaml` — same slugification as everywhere else in this
format (lowercase, hyphenated). This is purely for human browsability,
though — a `tags:` field elsewhere never references this filename, only
the tag's `id` (see below).

## Referencing a tag

An item or collection's top-level `tags` field is an array of tag `id`s, not
strings — see [`collections/CLAUDE.md`](../collections/CLAUDE.md), "Tags,"
for the full referencing rules (duplicates forbidden, referential integrity,
etc.). Adding a new tag to an entity means: find its `id` under `tags/` if
it already exists, or create the entity file first if it doesn't — there's
no freeform ad hoc tagging anymore.
