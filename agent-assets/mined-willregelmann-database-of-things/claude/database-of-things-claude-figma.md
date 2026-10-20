# figma — curation hints

## Directory structure

```
figma/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "figma" line
  <number>-<slugified-name>.yaml
```

Flat — one level, no series/set nesting, same as
[`../nendoroid/CLAUDE.md`](../nendoroid/CLAUDE.md). Max Factory assigns one
continuous figma number across every franchise, so there's no natural
grouping level to insert. Don't invent one.

## Numbering: three parallel sequences

figma numbers come in three forms — record the number **exactly** as printed,
including its prefix:

- **Normal** — a bare three-digit number, e.g. `001`. The main sequence.
- **SP** (Special) — `SP` + three digits, e.g. `SP001`. Special editions,
  usually bundled with a game/manga/Blu-ray rather than sold standalone (the
  very first figma, `SP001` Haruhi Suzumiya, shipped with a PS2 game).
- **EX** (Limited) — `EX` + three digits, e.g. `EX001`. Event/limited
  editions, typically sold at Wonder Festival or as shop exclusives.

The three sequences are independent — `001`, `SP001`, and `EX001` are three
different figures. `SP`/`EX` releases are **not** spin-off product lines (see
below); they're part of figma proper, just differently numbered.

**Spin-off lines are siblings, not nested here.** figma Styles, figma+, and
figFIX are separate Max Factory/Good Smile product lines with their own
numbering — if curating one, add it as its own collection under
[`../`](../CLAUDE.md) (the Good Smile Company umbrella), not folded into this
numbering.

## Identifying items

Identify a figure by its **figma number** plus the version, since popular
characters get multiple figma across re-releases and alternate outfits (each
version is its own figma number — don't merge them). Record the source work
in `attributes.origin` (e.g. `The Melancholy of Haruhi Suzumiya`), the same
way Nendoroid does — that's the **specific work**, and it stays in
`attributes`.

**Franchise is a separate, coarser axis and always goes in top-level `tags`,
never in `attributes`** (see [`../../CLAUDE.md`](../../CLAUDE.md)). **Every
figma gets a franchise tag** — create the `tags/franchises/` entity if one
doesn't exist yet rather than leaving the figure unsearchable by franchise. A
franchise that so far appears only here still earns its tag; don't wait for it
to turn up in a second collection.

The two fields coexist deliberately and often differ: figma 003 is
`origin: Fate/stay night` under the `Fate` tag, and figma 001/002 are
`origin: The Melancholy of Haruhi Suzumiya` under the `Haruhi Suzumiya` tag —
`origin` is what distinguishes works *within* a franchise, the tag is what a
catalog-wide franchise search resolves against. Where a franchise has only one
work the two read the same (`Death Note`, `Tsukihime`); that's expected, not a
duplication to collapse.

Look up the number and metadata rather than guessing — Good Smile's own
listing (`goodsmile.info`) and [MyFigureCollection](https://myfigurecollection.net/)
are the authoritative sources; use the same source consistently within one PR
when cross-checking a batch.

## `manufacturer` is not always Max Factory

figma is a Max Factory line, but individual releases are sometimes produced
by a Good Smile partner/subsidiary (e.g. FREEing for larger-scale figma, Good
Smile Arts Shanghai) or co-branded. Verify `attributes.manufacturer` per
release against the actual credit rather than assuming Max Factory.

## `release_type`

`attributes.release_type` is enum-validated in `item-attributes.schema.json`. The
enum starts small (`Standard`, `Exclusive`, `Limited`) and is expected to
grow — it is not meant to gate curation. If a figure's real classification
isn't in the enum yet, add it as part of the same PR after confirming the
label against Good Smile's own listing or MyFigureCollection.

## Naming files

`<number>-<slugified-name>.yaml`, the normal number zero-padded to 3 digits
(e.g. `001`); `SP`/`EX` numbers keep their lowercase prefix in the filename
(e.g. `sp001-haruhi-suzumiya.yaml`, `ex001-konata-izumi-cosplay.yaml`).
Include the version in the slug where it's needed to keep a recurring
character's files distinct (e.g. `001-yuki-nagato-school-uniform.yaml`).
Three digits covers the catalog with headroom; this is a continuously growing
line, so there's no "total" to pad against.

## Common pitfalls

- Don't confuse the **figma number** with a JAN/barcode or a GSC internal
  SKU — the catalog number is the "figma ###" printed on the box.
- Alternate-version and re-sculpt releases of the same character each get
  their own figma number and their own entity file — don't merge them.
- This line has no fixed endpoint, so completeness means cross-checking
  whatever range you're curating against Good Smile's listing for that range.
