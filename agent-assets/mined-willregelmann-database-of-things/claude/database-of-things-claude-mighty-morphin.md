# Mighty Morphin Power Rangers — curation hints

Bandai America's original toy line for the 1993 TV series — the first Power
Rangers toy line ever released, spanning Fall 1993 through Spring 1996.

## Directory structure

```
mighty-morphin/
  CLAUDE.md
  _collection.yaml
  figures/      # poseable Rangers, villains, dolls, talking figures, mini blind-assortment figures
  zords/        # Megazords, Thunderzords, Dragonzord, Titanus, Tor, Falconzord, Serpentera, ...
  vehicles/     # Battle Bikes, Thunder Bikes, Shark Cycles
  weapons/      # Power Morpher, Dragon Dagger, Power Cannon, Saba, Power Blaster
  playsets/     # Power Dome, Micro Morphin Playsets, Girls Carrying Case Playset
```

See [`../CLAUDE.md`](../CLAUDE.md), "Zords a Megazord combines from," for
how a Megazord's individually-named, never-sold-separately Dinozords/
Thunderzords/Shogunzords/Ninjazords are recorded.

Five type-based subdirectories, flat within each — matching an item's `type`
(`figure`/`zord`/`vehicle`/`weapon`/`playset`) to its directory. Unlike
Nendoroid's single continuous catalog, Bandai's numbering here isn't
type-segregated (a figure and a Zord can have adjacent numbers), so the
subdirectory is an editorial grouping for browsability, not a reflection of
a printed catalog section. Attributes/schema are shared with the rest of the
`power-rangers/` brand — this line has no `../../../../../item-attributes.schema.json` of its own.

## Source

[grnrngr.com](https://grnrngr.com/toys/power-rangers/mighty-morphin) is the
best available reference for this line — a fan-maintained archive giving
Bandai's own catalog number, release season, UPC, and box-art photo for
every item, including unreleased/solicited-only prototypes. It's the
authoritative source available for this line in the absence of a still-
active Bandai storefront (this line has been discontinued for decades). Its
image URLs (`grnrngr.com/toys/pictures/bandai/<code>.jpg`) are fine to use
for `image` — a fan/reference-site photo is an acceptable
fallback when no manufacturer-hosted image exists (see root
`collections/CLAUDE.md` image guidance).

## Identifying items

Items are identified by Bandai's own catalog/assortment number, e.g. `2200`.
**The number is not always unique to one item** — Bandai frequently assigned
one number to an entire blind-packed assortment (e.g. `2200` covers all
five original Rangers; `2300` covers 12 different mini figures). Treat a
shared number the same way Funko Pop's shared numbers are treated (see
[`../../../funko/pop/CLAUDE.md`](../../../funko/pop/CLAUDE.md)): file each
character/release as its own entity sharing that number, disambiguated by a
name/variant slug in the filename — don't invent a fake per-character
number that Bandai never printed.

## Naming files

`<number>-<slugified-name>.yaml`, inside the appropriate type subdirectory.
Bandai's numbers are already 4 digits, so no extra zero-padding is needed.
When a number is shared across multiple characters or re-releases, append a
name or variant slug to keep the filename unique (e.g.
`2200-jason-red-ranger.yaml`, `2428-ninja-megafalconzord-movie-edition.yaml`).

## `variant`

A handful of items reuse their common release's exact catalog number for a
different box-art release — most often a "Movie Edition" tie-in (1995's
feature film) reissuing the same toy under the same number with new
packaging (e.g. `2428` Ninja Megafalconzord, `2491` Deluxe Ninja Megazord,
`2492` Deluxe Falconzord, `2370` Girls Yellow & Pink Rangers gift set).
`attributes.variant` records this (`Standard` for the plain release). Four
store-exclusive "Special Size" Zord repacks (`2303`–`2306`, sold
exclusively through Toys "R" Us or Target) use `variant: Store Exclusive`
plus `attributes.exclusive_to` naming the retailer.

## Dates

grnrngr.com gives only a release season + year (e.g. "Fall 1994"), never an
exact date — store just the year (`date: "YYYY"`), matching the root
guidance for imprecise sourcing. A few items (the Toys "R" Us/Target
store-exclusive "Special Size" repacks, and `2307`/`2308`) have no
season/year listed at all on the source — leave `date` off entirely for
those rather than guessing.

## What's excluded from this line

- **Unreleased/solicited-only items.** grnrngr.com documents ~25 items that
  were solicited (shown in catalogs/press materials) but never actually
  released for sale — no real UPC, no shelf presence. Since DBoT catalogs
  things that exist to be collected, these aren't filed as entities here.
  If corroborating evidence later surfaces that one of these did reach
  retail in some market, re-evaluate — don't add speculatively.
- **The 2010 reissue line** (`mighty-morphin-2010` on the source site) is a
  separate Bandai product line with its own numbering; it would be a
  sibling directory (`power-rangers/mighty-morphin-2010/`) if ever curated,
  not folded into this one.

## Known source oddities

Catalog number `2488` ("8″ Evil Space Aliens" on grnrngr.com) doesn't match
any of its own listed items' numbers (`2527`/`2528`/`2529`), and two of
those three (`2528` Hornitor, `2529` Scorpitan) are also cross-listed under
`2521` "New Deluxe Evil Space Aliens" with "Deluxe"-prefixed names. These
look like the same physical releases indexed under two category headers on
the source site, not distinct products — filed once each here, under
`2521`'s "Deluxe" naming (`figures-and-models/2528-deluxe-hornitor.yaml`,
`figures-and-models/2529-deluxe-scorpitan.yaml`), with `2527` Ivan Ooze filed
separately under its own "8″ Evil Space Aliens" category since it doesn't
share this overlap. Revisit if a more authoritative source clarifies
otherwise.

## Known gap: two Toys "R" Us "Special Size Power Pack" box contents unconfirmed

`2305-special-size-mega-tigerzord.yaml` and `2308-special-size-thunder-megazord.yaml`
are both "Power Pack" boxes that visually bundle two toy windows, and by
name plausibly bundle two already-catalogued Special Size Zords each (2305:
White Tigerzord + Falconzord; 2308: Thunder Megazord + Tor) — but no source
turned up so far explicitly captions box contents by name for either, so
neither has an `attributes.zordComponents` list yet. Add one only once a
clearer box-back photo or instruction sheet confirms the exact contents.
