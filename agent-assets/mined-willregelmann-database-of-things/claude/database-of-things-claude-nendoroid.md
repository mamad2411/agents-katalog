# Nendoroid — curation hints

## Directory structure

```
nendoroid/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "Nendoroid" line
  <number>-<slugified-name>.yaml
```

Flat — one level, no series/set nesting. Unlike a trading card game, Nendoroid
doesn't release in discrete numbered sets; Good Smile assigns one continuous
catalog number across every franchise, so there's no natural grouping level
to insert. Don't invent one.

**Spin-off lines are siblings, not nested items.** Nendoroid Doll, Nendoroid
More, and Nendoroid Petit are separate Good Smile product lines with their
own numbering — they don't belong in this directory. Each now exists as its
own collection under `../` (the Good Smile Company umbrella), a sibling of
`nendoroid/`: `good-smile/nendoroid-doll/`, `good-smile/nendoroid-more/`,
`good-smile/nendoroid-petit/`. File a spin-off's items there rather than
folding them into this numbering.

## Collection records

The `_collection.yaml` at this level carries `description` beyond the
baseline `id`/`name`/`type` — a short blurb of scope (what the line is, when
it started). Not required by the schema, but match the tone of the existing
record.

## Identifying items

Figures are identified by their **official Nendoroid No.**, e.g. `1200`.
Numbers aren't always bare integers — variant releases use a letter suffix
(e.g. `245b`) or a `-DX` deluxe-version suffix (e.g. `970-DX`); use the number
exactly as Good Smile printed it, don't normalize it away. Prefer the number
over name matching — many characters get multiple Nendoroids across different
versions/re-releases, and the number is the reliable disambiguator.

**Source work vs. franchise — two fields, not one.** Record the specific work
a figure comes from in `attributes.origin` (e.g.
`origin: The Melancholy of Haruhi Suzumiya`). Record its **franchise** in
top-level `tags`, never in `attributes` (see
[`../../../CLAUDE.md`](../../../CLAUDE.md)). **Every Nendoroid gets a franchise
tag** — since this line is one flat sequence spanning every franchise Good
Smile has ever licensed, the tag is the *only* thing that makes a figure
findable by franchise; nothing about its directory position or catalog number
carries that. Create the `tags/franchises/` entity if one doesn't exist yet
rather than leaving the figure untagged, even when the franchise appears
nowhere else in the catalog yet.

The two fields legitimately differ where a franchise spans several works —
Nendoroids 002/003/005 are `origin: Fate/stay night` under the `Fate` tag,
009/010 are `origin: The Melancholy of Haruhi Suzumiya` under the
`Haruhi Suzumiya` tag. Where a franchise has only one work they read the same
(`Death Note`, `Nitro Wars`); that's expected, not a duplication to collapse.

Look up the number and metadata rather than guessing — Good Smile's own
listing pages (`goodsmile.info/en/nendoroid<range>`) and
[MyFigureCollection](https://myfigurecollection.net/) are the authoritative
sources; use the same source consistently within one PR when cross-checking a
batch.

## Naming files

`<number>-<slugified-name>.yaml`, number zero-padded to 4 digits (e.g.
`0004`), including any letter/`-DX` suffix in the slug portion if needed for
uniqueness (e.g. `0245b-...`). Four digits covers the catalog with headroom;
this is a continuously growing line, unlike a fixed-size card set, so there's
no "total" to pad against — 4 digits is a judgment call based on current
volume (catalog is past #3000 as of 2026), not a canonical width.

## `release_type`

`attributes.release_type` is enum-validated in `item-attributes.schema.json`. The
enum starts small (`Standard`, `Exclusive`, `Limited`) and is expected to
grow — it is not meant to gate curation. If a figure's real release
classification isn't in the enum yet (e.g. a specific convention-exclusive
label), add it as part of the same PR: confirm the label against Good
Smile's own listing or MyFigureCollection, then add it to the `enum` array
alongside the figure file(s) that need it.

## Common pitfalls

- Don't confuse the **Nendoroid No.** with a JAN/product barcode or a
  manufacturer SKU — the catalog number is what appears on the box as
  "Nendoroid No. ###".
- `manufacturer` isn't always "Good Smile Company" — some releases are
  co-branded or produced under a different Good Smile subsidiary/partner
  (e.g. Phat Company, Good Smile Arts Shanghai). Check the actual credit,
  don't assume.
- Variant/re-release versions (e.g. a "2.0" re-sculpt, a con-exclusive color
  edition) get their own Nendoroid No. and their own entity file — don't
  merge multiple releases of the same character into one file.
- This line has no fixed endpoint, so there's no "verify the set is
  complete" step the way a card set has — completeness here just means
  cross-checking whatever range you're curating against Good Smile's listing
  pages for that range.
