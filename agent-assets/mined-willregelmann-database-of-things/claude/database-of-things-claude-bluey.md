# Bluey — curation hints

## What belongs here

Moose Toys' official *Bluey* toy lines (BBC Studios/Ludo Studio). Moose Toys
has held the global master toy license since 2019 — verify
`attributes.manufacturer` as **Moose Toys Pty Ltd** unless a specific product
says otherwise.

Curate each Bluey toy line whole, per the `figures-and-models/` family rule (see
[`../../CLAUDE.md`](../../CLAUDE.md)): a line's figures **and** its companion
vehicles, playsets, and accessories all belong — a Bluey 4WD or the Heeler
House is in scope, not excluded for being a vehicle or a playset. The
sub-lines below are Bluey's distinct figure *formats*; when a format ships
vehicles/playsets/locations, curate them alongside its figures rather than
dropping them.

Out of scope, same as anywhere in `figures-and-models/`:

- **Plush** — curated in the [`plush/`](../../../plush/CLAUDE.md) family, not
  here.
- **Non-toy merchandise** — apparel, stationery, homeware.
- **Board games** (5-in-1, Bingo's Bingo, Shadowlands) and **Mash'ems**
  (squishy-fidget novelties) — these are separate product lines, not part of a
  Bluey figure/toy line. If ever curated they'd be their own line, not folded
  into the figure sub-lines below.

## Directory structure

```
bluey/
  CLAUDE.md
  item-attributes.schema.json  # generic fallback; each sub-line overrides it
  _collection.yaml               # the whole Bluey figures collection
  fuzzies/                       # soft flocked mini figures, blind-bag
    CLAUDE.md
    item-attributes.schema.json
    _collection.yaml
  mini-figures/                  # hard plastic ~1" figures, blind-bag
    CLAUDE.md
    item-attributes.schema.json
    _collection.yaml
  poseable-figures/               # 2.5-3" articulated figures, multi-pack/single-pack
    CLAUDE.md
    item-attributes.schema.json
    _collection.yaml
```

Each sub-line is its own top-level collection here, the same reasoning as
Nendoroid vs Figma vs Funko Pop under [`../../CLAUDE.md`](../../CLAUDE.md) — Fuzzies,
Mini Figures, and (Standard) Poseable Figures are different products with
different scale, material, and packaging, not variants of one line.

## No official global numbering

None of Bluey's figure formats print a global catalog/collector number the
way e.g. Funko Pop's "Pop! No." does. Identify figures by character name plus
their pack/series name — see each sub-line's own `CLAUDE.md` for its specific
identification approach and known pitfalls before filing anything.

## Manufacturer

`attributes.manufacturer` is `Moose Toys Pty Ltd` across every sub-line
unless a specific release credits a different legal entity — check the
package/listing rather than assuming.
