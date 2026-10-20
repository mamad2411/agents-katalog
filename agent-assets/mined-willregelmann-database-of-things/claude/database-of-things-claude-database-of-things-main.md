# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

Database of Things (DBoT) is a minimal, git-driven database of collectibles —
curated by agents and humans through GitHub pull requests.

**Mission**: Build the most comprehensive collectibles database on the Internet.

**Source of truth**: [`collections/`](collections/) — one YAML file per item,
organized into directories by category. There's no database to write to;
curation *is* opening a pull request.

**Core philosophy**:
- **Collectibles, not products** — the entity is the individual thing someone
  owns (a card, a figure, an issue), deduplicated on physical uniqueness
  rather than on UPC or packaging. See
  [`collections/CLAUDE.md`](collections/CLAUDE.md#collectibles-not-products)
- Minimal metadata by design — focus on coverage over exhaustive detail
- Source attribution via `image`, an authoritative link for each item's photo/logo
- Curation guidance travels with the data: each category carries its own
  `CLAUDE.md` and `item-attributes.schema.json` right next to its entity files

**Not optimizing for**:
- Exhaustive metadata (that's what source links are for)
- Real-time market data (we're a catalog, not a marketplace)

**Curation model**: the catalog is meant to grow and self-correct primarily
through AI agents web-searching for collectible data and opening PRs, not
through a human driving every addition. Curation currently happens by
directly editing entity files and validating by hand (see "Adding or
editing an entry" below) — no dedicated curation/audit tooling is wired up
at the moment.

## Repository structure

```
collections/                  # the data — see collections/README.md
  trading-cards/
    pokemon-tcg/
      CLAUDE.md               # naming conventions, verification, pitfalls
      item-attributes.schema.json  # JSON Schema for item attributes, enforced by CI
      original-series/
        base-set/
          004-charizard.yaml
          ...
tags/                          # cross-cutting tag entities — see
                               # docs/primitives/TAG.md
  franchises/
    pokemon.yaml
    ...
tools/collections-validate/   # CI validator: schema conformance, UUID
                               # uniqueness, required-file presence
docs/                          # design docs
```

## Entity file format

One YAML file per entity (`collections/<category>/.../<item>.yaml`):

```yaml
id: 3f4334f3-6a41-45fb-a1c1-dcf44566491e   # stable, generated once, never reused
name: Charizard
type: card
date: "1999-01-09"
attributes:
  number: "4/102"
  rarity: Rare Holo
  illustrator: Mitsuhiro Arita
image: https://images.pokemontcg.io/base1/4_hires.png
```

- `attributes` is validated against the collection's `item-attributes.schema.json`;
  top-level fields (`id`, `name`, `type`) are structural and validated the
  same way everywhere.
- **No `collection:`/`parent_collection:` field.** An entity's parent is
  whatever directory it's in — the validator rejects these fields if it finds
  them.
- Every collection directory (top-level or nested) needs its own
  `_collection.yaml` — the entity record for the collection/set itself.
- `CLAUDE.md` and `item-attributes.schema.json` are only required where a directory's
  conventions differ from its parent's — a nested set normally inherits both
  from its category.

See [`collections/README.md`](collections/README.md) for the full format and
[`collections/trading-cards/pokemon-tcg/CLAUDE.md`](collections/trading-cards/pokemon-tcg/CLAUDE.md) for a
worked example.

## Naming files

`collections/<category>/.../<slugified-name>.yaml` — lowercase, hyphenated.

When a collection has canonical numbering (a collector number, catalog
number, issue number, etc.), **prefix the slug with that number**, zero-padded
to the collection's total digit width — e.g. `004-charizard.yaml` for card
`4/102`. This keeps directory listings in canonical order instead of
alphabetical order. Collections without canonical numbering just use
`<slugified-name>.yaml`.

The category `CLAUDE.md` documents the specifics (which field is canonical,
how to slugify, disambiguation rules) — see
[`collections/trading-cards/pokemon-tcg/CLAUDE.md`](collections/trading-cards/pokemon-tcg/CLAUDE.md) for a
worked example.

## Adding or editing an entry

Add or edit entity files directly (see "Entity file format" and "Naming
files" above), then validate before opening a PR:

```bash
cd tools/collections-validate
npm install   # first time only
npm run validate
```

CI runs this validator on every PR that touches `collections/**`.

## Curation workflow

1. Branch, add or edit entity files, update `CLAUDE.md`/template if a
   collection's conventions changed.
2. Open a PR. CI validates schema conformance, UUID uniqueness/format, and
   required files.

## Reference documentation

- **Collections format**: [`collections/README.md`](collections/README.md)
- **Category-specific curation**: `collections/<category>/CLAUDE.md`
- **Core data-model primitives**: [`docs/primitives/`](docs/primitives/)
  (`COLLECTION.md`, `ITEM.md`, `TAG.md`)
