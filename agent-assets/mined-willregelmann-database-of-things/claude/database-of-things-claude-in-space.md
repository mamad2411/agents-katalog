# Power Rangers In Space — curation hints

Bandai America's toy line for the 1998 Power Rangers In Space TV season,
the direct successor to [Turbo](../turbo/CLAUDE.md).

## Directory structure

Same shape as the other eras — five type-based subdirectories (`figures-and-models/`,
`zords/`, `vehicles/`, `weapons/`, `playsets/`), flat within each. A
Megazord's individual pieces, bundled inside one box and never sold
separately, are recorded as `attributes.zordComponents` on the Megazord
itself — see [`../CLAUDE.md`](../CLAUDE.md), "Zords a Megazord combines
from." No `../../../../../item-attributes.schema.json` of its own; inherits
the shared `power-rangers/item-attributes.schema.json`.

## Source

[grnrngr.com](https://grnrngr.com/toys/power-rangers/in-space) — same
archive used for the prior eras, same data shape. See
[`../mighty-morphin/CLAUDE.md`](../mighty-morphin/CLAUDE.md) for the
general sourcing/identification/naming rules shared by every era in this
brand — this file only covers what's different about In Space.

## Excluded: literal carryover relistings from Turbo, not new products

Two catalog numbers on the In Space page — `3040` "Astro Galaxy Navigator"
and `3047` "Deluxe Double Morphing Rescue Megazord" — carry the **exact
same UPC** as `../turbo/weapons/3040-turbo-navigator.yaml` and
`../turbo/zords/3047-deluxe-double-morphing-rescue-megazord.yaml`
respectively (3047 even keeps the identical name). These read as the same
physical retail product still being sold/catalogued during the In Space
merchandising window, not new 1998 tooling — excluded from this line rather
than filed as duplicate entities. This is a different situation from Zeo's
catalog-number reuse (`2340`/`2462`), where the reused number pointed to a
*different* box-art/name and got filed as its own entity — the test is
whether the UPC and product are actually the same (exclude) or just the
number was recycled for something new (file it).

## Shared numbers here are packaging-variant sharing, not blind-assortment sharing

Unlike Mighty Morphin/Zeo's "one number for the whole team," In Space only
reuses a number/UPC across rows in two narrow cases:
- **`3200` Digizord** — three rows are just different-colored photos of one
  electronic handheld toy, not distinct characters. Filed as a **single**
  entity rather than three.
- **`3248` Astro Team Packs** — three rows share one UPC but each pairs a
  *different* Ranger with a *different* Zord (Red+Megazord, Black+Mega
  Tank, Blue+Megaship) — genuinely distinct box contents. Filed as three
  separate entities, same disambiguation approach as every other shared-
  number case in this brand.

## Missing photos are a real gap, not a placeholder to use

Four of the five "5″ Astro Power Rangers" figures (`3211`-`3214`) show a
site-side "Photo Needed" crowdsourcing placeholder instead of real product
photography — these are confirmed released items with real UPCs (not
unreleased), just without a sourced image yet. Filed without
`image` rather than link the placeholder graphic; add the real
photo later if one turns up. `3215` (Pink) has a real photo and is filed
normally.

## Known gap: Astro Delta Megazord box contents unconfirmed

`3253-astro-delta-megazord.yaml` — its box photo reads as a single
pre-posed figure like its non-combining siblings, but a secondary
toy-identification database categorizes it as a "Combiner" and lists an
included instructions sheet, which doesn't fit that reading. No
`attributes.zordComponents` was added for it pending a clearer source
(box-back photo, instruction sheet, or review) confirming which is correct.

## Heroes Of Space sub-line released outside the nominal 1998 season

`3291`-`3293` and their `3310` triple-pack bundle (NASA Apollo-astronaut
cross-promotional figures) shipped **Spring 1999**, a year after the rest
of the line — still real, released products catalogued under Bandai's In
Space page, just dated `1999` individually rather than `1998` like
everything else here. Included on the same basis as Mighty Morphin's
Spring 1996 tail-end waves (Battle Borgs, Alien Rangers): still part of the
line's real release history even though it trails the show's original air
year.

## What's excluded from this line

- **The `1035` Trading Card Set** (`1036`-`1038`) — out of category scope,
  same as Turbo's `1090`.
- **`3040`/`3047` carryover relistings** — see above.
- **Unreleased items**, two confidence tiers: `3134` Spiral Saber has a
  confirmed catalog number and UPC but never shipped; `3182` Jumbo Mega
  Voyager and the three `3255` "Grip Fighters" (Astro Megazord Shuttle,
  Delta Megaship, Red Galaxy Glider) are unreleased *and* their catalog
  numbers are themselves unconfirmed (site shows `????`). All excluded per
  the standard unreleased-item policy.

## Known judgment call

`3200` Digizord doesn't cleanly fit `figure`/`zord`/`vehicle`/`weapon`/
`playset` — it's an electronic handheld/virtual-pet-style gaming novelty,
not a poseable figure. Filed as `type: figure` for lack of a better fit;
revisit if this pattern recurs enough in later eras to warrant its own
type.
