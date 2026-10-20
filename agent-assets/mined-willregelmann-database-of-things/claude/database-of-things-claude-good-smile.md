# Good Smile Company — curation hints

## What belongs here

Good Smile Company's character figure lines, organized one nested collection
per product line. Curated so far:

- [`nendoroid/`](nendoroid/CLAUDE.md) — poseable chibi-style figures, one
  continuous catalog number since 2006.
- [`figma/`](figma/CLAUDE.md) — highly articulated action figures (Max
  Factory, a Good Smile subsidiary listed under the Good Smile Company
  storefront), one continuous number since 2008.

Scaffolded, no items yet — each needs its own `CLAUDE.md` and
`../../../item-attributes.schema.json` before its first figure is filed (see
[`../../CLAUDE.md`](../../CLAUDE.md#scaffolding-a-new-collection)):

- `pop-up-parade/` — affordable non-articulated static figures, since 2019.
- `moderoid/` — partially pre-painted plastic model kits, since 2018.
- `nendoroid-doll/` — articulated dress-up bodies, since 2018.
- `nendoroid-more/` — accessory, face-plate and playset parts.
- `nendoroid-petit/` — half-height Nendoroids in boxed and blind-box sets.

A line's numbering is its own — a model-kit line and a dress-up doll line
share nothing with Nendoroid's flat catalog number, so don't carry one
line's identification scheme across to another when filling these in.

figma is placed here rather than under its manufacturing subsidiary Max
Factory because Good Smile Company is the customer-facing brand that presents
and sells it — the same "cut at the customer-facing brand" rule the parent
[`../CLAUDE.md`](../CLAUDE.md) documents.

## Directory structure

```
good-smile/
  CLAUDE.md
  _collection.yaml               # Good Smile Company itself
  <line>/                         # e.g. "nendoroid", "figma"
    CLAUDE.md                     # phase 2 — before the line's first item
    item-attributes.schema.json  # phase 2 — same
    _collection.yaml              # phase 1 — the scaffold
    ...                          # the line's own internal structure
```

Each line owns its numbering, attributes, and pitfalls — don't assume one
line's conventions carry to another. Nendoroid spin-off lines (Nendoroid
Doll, Nendoroid More, Nendoroid Petit) are their own lines, and are siblings
here (`good-smile/nendoroid-doll/`, ...) rather than nested inside
`nendoroid/` — see [`nendoroid/CLAUDE.md`](nendoroid/CLAUDE.md).
