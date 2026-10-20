# Power Rangers Zeo — curation hints

Bandai America's toy line for the 1996 Power Rangers Zeo TV season, the
direct successor to [Mighty Morphin](../mighty-morphin/CLAUDE.md).

## Directory structure

Same shape as `mighty-morphin/` — five type-based subdirectories
(`figures-and-models/`, `zords/`, `vehicles/`, `weapons/`, `playsets/`), flat within
each. A Megazord's individual Zeo Zords/Super Zeo Zords, bundled inside one
box and never sold separately, are recorded as `attributes.zordComponents`
on the Megazord itself — see [`../CLAUDE.md`](../CLAUDE.md), "Zords a
Megazord combines from." No `../../../../../item-attributes.schema.json` of
its own; inherits the shared `power-rangers/item-attributes.schema.json`.

## Source

[grnrngr.com](https://grnrngr.com/toys/power-rangers/zeo) — same
fan-maintained archive used for Mighty Morphin, same data shape (catalog
number, release season+year, UPC, box-art photo, explicit "Unreleased"
flag for solicited-but-never-shipped items). See
[`../mighty-morphin/CLAUDE.md`](../mighty-morphin/CLAUDE.md) for the
general sourcing/identification/naming rules shared by every era in this
brand — this file only covers what's different about Zeo.

## Assortment header numbers routinely don't match any child item

More so than Mighty Morphin: most of this line's category headers (e.g.
"2506 Zeo Jet Cycles") carry a case-assortment SKU that isn't any of the
individual items filed beneath it (the real items are `2507`-`2512`). This
is normal Bandai practice here, not a one-off anomaly — the header number
only ever feeds `attributes.category`'s *name*, never an item's own
`number`, so it doesn't affect filing.

## Reused Mighty Morphin catalog numbers (repackaged tooling)

Two items in the "5.5″ Action Feature Evil Space Aliens" assortment —
`2340` "Rapid Sword Swinging Goldar" and `2462` "Air-Pumping Cannon Rito
Revolto" — reuse catalog numbers already assigned to Mighty Morphin figures
(`../mighty-morphin/figures-and-models/2340-sword-slashing-goldar.yaml` and
`2462-air-pump-cannon-rito-revolto.yaml`). Same sculpt/tooling, reissued
under Zeo-branded box art (source site's own `_2`-suffixed photos confirm
alternate packaging) — filed here as their own Zeo-line entities under
their Zeo names, since numbers are scoped per line/directory, not global
across the whole `power-rangers/` brand. Don't treat this as a duplicate to
merge or a validator problem.

## Gift-set / multi-pack items

`2669` (Auto Morphin Zeo Ranger Collection), `2676` (Special Edition Auto
Morphin Gold Team), and `2687` (Deluxe Special Edition Gold Team) are
single-UPC boxed multi-figure sets with no sub-items enumerated on the
source page — filed as `type: figure` with the set's own name, matching how
Mighty Morphin's `2222`/`2301`/`2307` gift/collector sets were handled.

## What's excluded from this line

- **Unreleased "6″ Doll Assortment"** (Katherine, Tanya, Tommy) — flagged
  unreleased on the source site, and its catalog number is itself
  unconfirmed there ("????"). Excluded per the same policy as Mighty
  Morphin's unreleased items.

## Zord Morphin Zeo Rangers — only three ever released

The "Zord Morphin Zeo Rangers" assortment (`2703`) case count of 12 reflects
multiple units of the same 3 SKUs, not 12 distinct figures — confirmed via
grnrngr.com, thetoycollectorsguide.com, and multiple independent
retailer/collector listings: only Zeo Rangers III, IV, and V (`2704`-`2706`,
already filed here) were ever released as Zord Morphin figures. No Zeo
Ranger I, II, or Gold Ranger version exists in this assortment — this line
is already complete for it, don't go looking for more.
