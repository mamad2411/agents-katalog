# Funko Pop! — curation hints

## Directory structure

```
pop/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "Funko Pop!" product line
  <pop-line>/
    _collection.yaml             # the Pop! line, e.g. "Movies", "Marvel", "Star Wars"
    <number>-<slugified-name>.yaml
```

Two levels, not flat like Nendoroid — Funko resets numbering independently
within each **Pop! line**, the category printed on the box directly beneath
the "Pop!" wordmark (`Movies`, `Television`, `Animation`, `Marvel`, `Star
Wars`, `Disney`, `Rocks`, `Games`, `Heroes`, `Icons`, `Ad Icons`, `Sports`,
`Retro Toys`, `Harry Potter`, `Horror`, `Anime`, and more). A number is only
unique within its line, not globally — two figures in two different lines
can share the same number.

**Determining a figure's line**: use the category actually printed on the
box, not the character's source franchise — a figure's *franchise* (e.g.
"The Office", "Breaking Bad") is usually narrower than its *line* (e.g.
"Television"), and one line spans many unrelated franchises. Record the
franchise separately via the top-level `tags` field, referencing a
`tags/franchises/` entity by id (e.g. "The Office") — see
[`collections/CLAUDE.md`](../../../CLAUDE.md#tags) — not as an `attributes`
field; the directory captures the line only.

**Naming line directories**: lowercase, hyphenated, matching the printed
category name (e.g. `movies`, `animation`, `marvel`, `star-wars`, `disney`,
`television`, `rocks`).

**Sub-formats are separate sibling lines under `figures-and-models/`, not
nested here.** Pop! Rides (vehicle + figure), Pop! Town (figure + buildable
diorama piece), Pop! Moments (multi-figure scene), and Pop! Albums (figure +
album-cover box art) are distinct Funko product formats with their own
separate numbering and box conventions — same relationship as Nendoroid
Doll/More/Petit to plain Nendoroid (see
[`../../good-smile/nendoroid/CLAUDE.md`](../../good-smile/nendoroid/CLAUDE.md)).
If curating one, add it as its own sibling line under `funko/` (e.g.
`figures-and-models/funko/pop-rides/`), not folded into this directory's
numbering.

## Collection records

The top-level `_collection.yaml` carries `description` beyond the baseline
`id`/`name`/`type`. Give each `<pop-line>/_collection.yaml` a short
`description` too — match the tone of existing records elsewhere in this
category.

## Identifying items

Figures are identified by their **Pop! No.**, printed on the box's window
sticker — e.g. `421`. This number is scoped to the figure's *line* only (see
above), not global — always confirm which line a number belongs to before
treating it as a unique identifier.

**Variants (chase, glow-in-the-dark, flocked, metallic, diamond glitter,
blacklight, etc.) usually share the exact same Pop! No. as the common
release they vary from** — Funko distinguishes them with a sticker/label on
the box, not a different number. Unlike Nendoroid, the number alone is NOT a
reliable uniqueness key — always check whether a release is a variant of an
already-filed number before assuming a number is unclaimed. When it is,
file it as a `variants` sub-entity on the common release's item (see
[`../../../../docs/primitives/ITEM.md`](../../../../docs/primitives/ITEM.md),
"Variants") rather than a second top-level file, giving the variant its own
`attributes.variant` (see below) since that's the field actually differing
from the parent.

**Retailer- and convention-exclusive releases (SDCC, NYCC, Hot Topic,
GameStop, Target, Walmart, Funko Shop, etc.) may reuse an existing common
figure's number, or may be assigned their own new number entirely — this
isn't consistent, so verify each one individually rather than assuming
either pattern.** Record the exclusivity via `attributes.exclusive_to`.

Look up the number and metadata rather than guessing — Funko's own site
(funko.com) and fan databases like [HobbyDB / Pop Price
Guide](https://www.hobbydb.com/home/funko) and [Pop's
Today](https://pops.today/) are the best sources; cross-reference more than
one where possible. PopPriceGuide.com merged into hobbyDB in 2023, so older
links to it may redirect.

## Naming files

`<number>-<slugified-name>.yaml`, number zero-padded to 4 digits (e.g.
`0421`), inside its line's directory. Since numbers reset per line, this
only needs to be unique within the line, not across the whole collection. A
variant sharing its base release's number lives inside that same file's
`variants` array, not a filename of its own.

## `variant`

`attributes.variant` is enum-validated in `item-attributes.schema.json`. The enum
starts small (`Common`, `Chase`, `Flocked`, `Glow in the Dark`, `Metallic`,
`Diamond Collection`) and is expected to grow — it is not meant to gate
curation. If a figure's real variant type isn't in the enum yet, add it as
part of the same PR: confirm the label against Funko's own listing or a fan
database, then add it to the `enum` array alongside the figure file(s) that
need it.

## Common pitfalls

- Don't confuse the **Pop! No.** with a UPC/barcode or Funko's internal SKU
  — the number that matters is the one printed as the figure's catalog
  number for its line.
- Don't treat a Pop! No. as globally unique across lines — always check
  which line before filing (see Identifying items above).
- Don't assume a chase/variant gets its own number — verify each case, and
  don't create a second top-level file for one that shares its common
  release's number; add it as a `variants` entry on the existing file
  instead (see Identifying items above).
- `manufacturer` is generally "Funko, LLC", but check for co-branded or
  licensed sub-lines that credit differently.
- This line (like Nendoroid) has no fixed endpoint per line — completeness
  here just means cross-checking whatever range you're curating against
  Funko's or a fan database's listing for that line.
