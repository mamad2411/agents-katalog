# Re-Ment — curation hints

## What belongs here

Re-Ment's blind-box **character figure/diorama** lines only. Re-Ment also
sells a huge catalog of non-figure novelty items under the same licenses
(erasers, magnets, mini towels, kitchen playsets, miniature food/snacks,
stationery) — those aren't standalone character figures and don't belong in
`figures` at all. When scoping a new product for curation, check
it's actually a posed character figure/diorama, not merchandise that merely
features a Pokémon on it.

## Directory structure

```
re-ment/
  CLAUDE.md
  item-attributes.schema.json  # manufacturer + pokemon attributes, inherited by everything below
  _collection.yaml               # Re-Ment itself
  <franchise>/                   # e.g. "pokemon" — only Pokémon is curated so far
    _collection.yaml
    <series>/                    # e.g. "Terrarium Collection" — an ongoing named product line
      _collection.yaml
      CLAUDE.md                  # only where the series has its own quirks worth documenting
      vol-<NN>/                  # one blind-box release
        _collection.yaml
        <slugified-pokemon-name(s)>.yaml
```

Four levels, one more than FireLink's `<game>/<series>/<figure>` (see
[`../firelink/CLAUDE.md`](../firelink/CLAUDE.md)) — Re-Ment runs many
differently-named series per franchise, and most of those series release in
numbered volumes/waves over time rather than as a single one-off set.

Series without volume numbering yet (a single release so far) still get a
`vol-01/` directory — Re-Ment's ongoing lines routinely add a second volume
later, and this keeps the structure consistent instead of needing to
retrofit nesting when that happens.

## Series names are official (unlike FireLink)

Re-Ment publishes real product names for each series — source them from
Re-Ment's own listings, not retailer inventions:
- **Current/active products**: `re-ment.co.jp/product/brand.php?c=<franchise>`
  (e.g. `?c=pokemon`)
- **Discontinued/historical products**: `re-ment.co.jp/product/discontinue.php`
  — this is the authoritative archive of *every* past release with exact
  release dates; prefer it over a retailer's "date first available," which
  sometimes reflects a reprint/restock date rather than the true original
  release.
- **Individual product pages**: `re-ment.co.jp/product/r<NNNNN>` — gives
  exact release date and price reliably, but does **not** list box contents
  as text (see Identifying rosters below).

Prefer Re-Ment's own English rendering when a product page gives one;
otherwise use the most consistent retailer English name and note the
Japanese original.

The `r<NNNNN>` in a product URL is Re-Ment's own website catalog ID, not a
number printed on the packaging — don't treat it as a public figure/product
number.

## A vol-01 record never gets a volume number in its `name`

**Re-Ment's own official title never numbers a series' first release, even
retroactively once a numbered sequel exists** — confirmed directly against
live listings, not inferred: Aqua Bottle Collection's release 1 is still
titled just "AQUA BOTTLE collection" today, years after "AQUA BOTTLE
collection2" shipped; Gemstone Collection, Pokémon Town ("ポケモンの街"),
and Starrium Series all show the identical pattern — the *second* release
is the first one to carry any number at all. Match that in `name`:

- `vol-01/_collection.yaml`'s `name` is the bare series name, with no "Vol.
  1"/"1" suffix — same as the series' own top-level `_collection.yaml`
  `name`, duplicated exactly. That's not a bug; it's how Re-Ment's own
  first release is actually titled.
- `vol-02/`, `vol-03/`, etc. get an explicit number in `name` (rendered as
  "Vol. N" in English, matching Re-Ment's own e.g. "collection2" /
  "ポケモンの街2") — Re-Ment does number these from their own first
  listing.
- This means a `vol-01` record's `name` **never needs a retroactive
  rename** when a later volume is added — Re-Ment itself never touches
  release 1's title, so neither should this catalog.

The `vol-01/` *directory* still always exists from the first release
regardless (see above) — this rule is about the entity's `name` field only,
not the directory-nesting convention.

## No printed catalog number on figures

Unlike Nendoroid, individual figures carry no manufacturer number. Identify
a figure by the Pokémon it depicts, within its volume directory — matching
[`../firelink/CLAUDE.md`](../firelink/CLAUDE.md)'s approach.

## Box contents

Each release is typically an outer carton of 6 individually blind-wrapped
figures ("全6種類" = "all 6 types"), one guaranteed of each design per full
carton. The count varies by series/volume (some are 4, 7, or 8) — verify the
actual count per volume rather than assuming 6.

## Identifying rosters — verify against the actual photos

A Re-Ment product page's **text** never lists which Pokémon are in the box —
that information only exists in the page's photo gallery (a "N/6"-labeled
image set, `data-original="../data/photo/product/t/<id>.jpg"` in the page
HTML). Cross-reference a retailer/fan checklist for a first-pass roster, but
**always verify each pairing against the actual gallery photo** before
filing:

- **Gallery image order does not reliably match a checklist's listed
  order.** Match by visual content, not position, before attaching an image
  URL to a figure file.
- **Japanese→English Pokémon name mistranslation is common** from automated
  tools and even some retailer listings. Confirmed mistakes caught while
  curating Terrarium Collection: シェルダー is Shellder, not Cloyster;
  ヌマクロー is Marshtomp, not Palpitoad; ソーナンス is Wobbuffet, not
  Wynaut; ココドラ is Aron, not Roggenrola; マグマラシ is Quilava, not
  Slugma; キレイハナ is Bellossom, not Vileplume; オオタチ is Furret, not
  Bibarel; ピジョン is Pidgeotto, not Pidgeot. Cross-check any Japanese
  name against [Bulbapedia's "List of Japanese Pokémon
  names"](https://bulbapedia.bulbagarden.net/wiki/List_of_Japanese_Pok%C3%A9mon_names)
  rather than trusting a single auto-translated source.
- **Many designs depict two Pokémon together** (e.g. "Pikachu & Mareep").
  Don't assume a design is solo from a quick glance — a small second figure
  is easy to miss in a low-res thumbnail.

## Naming and identifying figures

`name` is the Pokémon depicted, joined with " & " for a paired design (e.g.
`Pikachu & Mareep`). File slug matches: `pikachu-mareep.yaml`.
`attributes.pokemon` lists the same species as a structured array. Use each
Pokémon's official English species name.

**A volume can feature the same species more than once** (e.g. a "napping"
Piplup design and a separate "tumbling" Piplup design in the same box) — a
bare species name would collide as a filename. Disambiguate with a short
parenthetical pose/scene descriptor in both `name` and the slug (e.g.
`Piplup (Napping)` → `piplup-napping.yaml`). This is a judgment call each
time, not a fixed vocabulary — describe what's actually different about the
pose/scene.

## Images

Attach `image` pointing directly at the verified Re-Ment gallery
photo (`https://www.re-ment.co.jp/data/photo/product/t/<id>.jpg`) once
you've confirmed which photo matches which figure — these are Re-Ment's own
official product photography, an authoritative source per the root
[`collections/CLAUDE.md`](../../../CLAUDE.md) logo/image guidance.

**Some older volumes never got an individual per-figure gallery** — Re-Ment's
page for that product has only a single box-art photo instead of a "N/6"
gallery (confirmed by checking the Wayback Machine's earliest snapshot, not
just the current live page). When that's genuinely the case: use that one
official box-art photo as `image` for every figure in the volume
(still authoritative Re-Ment photography, just shared rather than 1:1) rather
than inventing per-figure crops, or fall back to a retailer/marketplace photo
per the project's general image-sourcing policy if even that's unavailable —
don't leave `image` off if a reasonable source exists. If truly no clean
photo can be found for a specific figure after a real search, it's fine to
omit `image` for just that figure rather than reuse an unrelated or
low-confidence image.

## Dates

For a series' own `_collection.yaml`, use its first volume's release date
(sourced from the discontinue-products archive when available). For a
currently-active series with no discontinued predecessor, the true original
release date may not be independently confirmable yet — leave `date` off
rather than guessing (see root `collections/CLAUDE.md`).
