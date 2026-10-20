# Power Rangers Turbo — curation hints

Bandai America's toy line for the 1997 Power Rangers Turbo TV season
(including its "Turbo: A Power Rangers Movie" tie-in), the direct successor
to [Zeo](../zeo/CLAUDE.md).

## Directory structure

Same shape as `mighty-morphin/` and `zeo/` — five type-based subdirectories
(`figures-and-models/`, `zords/`, `vehicles/`, `weapons/`, `playsets/`), flat
within each. A Megazord's individual Turbozords/Rescue Zords, bundled
inside one box and never sold separately, are recorded as
`attributes.zordComponents` on the Megazord itself — see
[`../CLAUDE.md`](../CLAUDE.md), "Zords a Megazord combines from." No
`../../../../../item-attributes.schema.json` of its own; inherits the shared
`power-rangers/item-attributes.schema.json`.

## Source

[grnrngr.com](https://grnrngr.com/toys/power-rangers/turbo) — same archive
used for the prior two eras, same data shape. See
[`../mighty-morphin/CLAUDE.md`](../mighty-morphin/CLAUDE.md) for the
general sourcing/identification/naming rules shared by every era in this
brand — this file only covers what's different about Turbo.

## No Movie Edition variants, unlike Mighty Morphin

Despite "Turbo: A Power Rangers Movie" being a real theatrical tie-in, the
source treats Turbo as a single undifferentiated toy line — no item repeats
a catalog number for a movie-specific box-art variant the way Mighty
Morphin's `2428`/`2491`/`2492`/`2370` do. Don't go looking for a
`variant: Movie Edition` pattern here; it doesn't occur in this line.

## Shared catalog numbers are rare here

Unlike Mighty Morphin and Zeo, almost every individual figure/vehicle in
Turbo got its own unique catalog number — Bandai stopped the
one-number-per-whole-assortment blind-pack pattern seen in the earlier two
eras (e.g. Mighty Morphin's `2200` covering all five original Rangers).
Assortment header numbers still routinely don't match any child item's own
number (same as Zeo) — that's just the case-pack SKU, not a per-item
oddity.

## What's excluded from this line

- **The `1090` Turbo Rangers Trading Card Set.** Three promotional photos
  share one catalog number and UPC — it's a single trading-card product,
  not a figure/zord/vehicle/weapon/playset, so it falls outside this
  category's scope entirely (not just this line's `variant: Standard`
  scope). If Power Rangers trading cards are ever worth curating, that's a
  `trading-cards/` category of its own, not a `power-rangers/turbo/`
  entity.
- **Two unreleased 8″ villain figures**, Maligore (`2988`) and Terrorsaur
  (`2989`) — flagged unreleased on the source site, and unlike every other
  item in this line, their catalog numbers are themselves unconfirmed
  (shown as `????`, only inferable from image filenames). Excluded per the
  same policy as every other line's unreleased items — see
  [`../mighty-morphin/CLAUDE.md`](../mighty-morphin/CLAUDE.md).

## Known judgment calls

- **`3033` "Turbo Power Pack"** is a single-SKU boxed item with no contents
  listed on the source page. Filed as `type: figure` for consistency with
  the line's other unelaborated boxed sets (`2798`, `3031`), but unlike
  those two this name doesn't obviously imply figures — Mighty Morphin used
  "Power Pack" naming for store-exclusive *Zord* repacks
  (`2303`-`2306`), so this could plausibly be a Zord or weapon bundle
  instead. Revisit if a source ever turns up its actual contents.
  Same caveat, less ambiguously, for the two other unelaborated boxed sets:
  `2798` "Shifter Action Turbo Ranger Collection" and `3031` "Triple Action
  Turbo Ranger Collection" — their names strongly imply Ranger figures, so
  those two are lower-risk guesses than `3033`.
- **"Robo Racer" items are filed as `zord`, not `vehicle`**, even though
  the name and die-cast miniature version (`3076`, under "Real Metal Turbo
  Vehicles") suggest a car — the source's own category header for its
  first appearance (`2952`) is "Action Feature Turbo Zords," matching its
  in-fiction role as one of the combining Turbo Zords. `3076`'s die-cast
  miniature stays `type: vehicle` since that whole sub-line (`3074`-`3078`)
  is a small-scale replica collectible spanning both Zords and Ranger-driven
  cars indiscriminately — it's its own product category, not a scaled-down
  version of each item's own type.
