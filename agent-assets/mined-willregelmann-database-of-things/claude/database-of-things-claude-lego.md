# LEGO — curation hints

## What belongs here

Officially released LEGO building sets — bricks packaged under one official
set number, sold under a **theme** (and often a more specific **subtheme**).

LEGO sits at the top level of [`../CLAUDE.md`](../CLAUDE.md) as its own
customer-facing brand, the same as `funko/` or `bandai/`. It used to be
parked under a `model-kits/` family that explicitly didn't describe it — a
reusable brick system isn't a single-use kit — and that caveat is now moot:
the family this line lives in covers figures, kits, and construction sets
alike, and treats assembly as a property of the line rather than a boundary
between families.

**LEGO Minifigures (the "Collectible Minifigures" blind-bag line) belongs
under `lego/`** — as `lego/minifigures/`, a sibling of the theme
directories. This used to be an open question, because a standalone numbered
series of figures (one random figure per bag, no set/box identity) looked
more like a `figures/` line than a building set, and those were different
families. They aren't anymore, so the question is just the ordinary
brand-first one: LEGO makes it, LEGO sells it, it goes under `lego/`.
Nothing for it exists yet; when it's curated, give it its own `CLAUDE.md`
covering the blind-bag numbering. **Not to be confused with the minifigures
bundled inside ordinary sets** — those aren't catalogued as entities at
all, see below.

## Themes and subthemes

LEGO organizes sets by **theme** (Star Wars, City, Technic, Ninjago, Creator,
...) and, within many themes, a more specific **subtheme** (e.g. City's
Traffic, Police, or Wildlife subthemes). Use
[Brickset](https://brickset.com/sets/bytheme) or the official LEGO site's own
theme listing as the authoritative grouping — don't invent a theme/subtheme
split that doesn't match how LEGO or Brickset actually categorizes a set.
Not every theme has subthemes; when one doesn't, sets sit directly under the
theme directory.

## Directory structure

```
lego/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "LEGO" collection
  <theme>/                       # star-wars/, city/, technic/, ninjago/, ...
    _collection.yaml
    <subtheme>/                  # only where the theme genuinely has one
      _collection.yaml
      <set-number>-<slugified-name>.yaml
    <set-number>-<slugified-name>.yaml   # sets directly under the theme when no subtheme applies
```

## Identifying items

A set's **official LEGO set number** (e.g. `75192`) is the primary
identifier — record it as `attributes.number`. LEGO reused set numbers
across unrelated sets in some earlier eras; BrickLink/Brickset disambiguate
with a `-1`/`-2` suffix in their own catalogs, but that suffix isn't part of
the number as printed on the box — only add a disambiguator to this repo's
data (e.g. in the filename) if a genuine collision turns up, don't append it
by default.

## Naming files

`<set-number>-<slugified-name>.yaml`, e.g. `75192-millennium-falcon.yaml`.
Official set numbers aren't sequential within a theme the way Pokémon card
numbers are within a set, so don't zero-pad them — use the number exactly as
LEGO assigned it.

## Attributes

See `item-attributes.schema.json`. `attributes.pieceCount` and
`attributes.minifigCount` come from the set's own official packaging/manual
or a reliable source like Brickset — don't estimate.

## Minifigures

A set's bundled minifigures aren't catalogued as entities of their own —
owning a set's minifigures loose doesn't mean owning the set, and
BrickLink/Brickset-level per-minifig detail (print variant, which sets it
reappeared in, ...) is finer-grained than this catalog tracks. Record only
`attributes.minifigCount`, from the set's own official packaging/manual or
a reliable source like Brickset — don't estimate. Not the same thing as the
standalone blind-bag Collectible Minifigures line discussed above, which
*is* catalogued as ordinary items, under `lego/minifigures/`.
