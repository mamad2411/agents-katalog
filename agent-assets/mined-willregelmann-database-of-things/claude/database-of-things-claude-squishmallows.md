# Squishmallows — curation hints

## Directory structure

```
squishmallows/
  CLAUDE.md                      # applies to every line below
  item-attributes.schema.json
  _collection.yaml               # the Squishmallows *brand*
  original-squishmallows/         # the standard line
    _collection.yaml
    <number>-<slugified-name>.yaml
  squish-a-longs/                 # a sub-line, its own numbering
    _collection.yaml
```

**This directory is the brand tier; items live in a line below it, never
here.** Jazwares' own name for the standard line is *Original Squishmallows*,
which is what `original-squishmallows/` holds — everything carrying an
ordinary Collector Number. Everything below about identification, naming and
sourcing describes that line; the brand tier itself holds no items.

Within `original-squishmallows/` the shape is flat — no series/set nesting.
Squishmallows are released under a
single continuous **Collector Number** sequence spanning every species and
every licensed collab (Pokémon, Disney, Marvel, Harry Potter, Sanrio, and
more), the same way Nendoroid uses one continuous number across franchises —
see [`../../figures-and-models/good-smile/nendoroid/CLAUDE.md`](../../figures-and-models/good-smile/nendoroid/CLAUDE.md)
for the analogous shape. Record the licensed franchise via the top-level
`tags` field, referencing a `tags/franchises/` entity by id (e.g. Pokémon)
— see [`../../CLAUDE.md`](../../CLAUDE.md#tags) — not as a directory split
or an `attributes` field.

**Sub-formats with their own restarting numbering are sibling lines beside
`original-squishmallows/`, not extra numbers in its sequence.** Squishmallows
has several distinct product formats that each keep their *own* Collector
Number sequence starting back at 1 — confirmed examples are **Fuzz-A-Mallows**
and **Squish-Doos**. Squishville (~2" minis) and Micromallows (~2.5"
blind-bag minis) are also distinct sub-brands with their own scale and
packaging, not just a size variant of the standard line. **Squish-A-Longs**
(1" Mini-Squish, numbered by its own Series) is scaffolded at
[`squish-a-longs/`](squish-a-longs/) — note it's squeezable *plastic*, not
plush, and stays under this brand anyway, because a brand is curated whole
(see [`../../CLAUDE.md`](../../CLAUDE.md#tree-shape)).

If curating one of these, add it as `squishmallows/<sub-line>/` — **not** a
hyphenated sibling under `plush/`, which would split the Squishmallows brand
across the category's top level, and **not** nested inside
`original-squishmallows/`, which is a peer line rather than a parent. The
restarting numbering is why it's a separate collection; it isn't a reason to
file it away from its brand.

Squishmallows' own "Rarity Scale" (Rare, Ultra Rare, Special Edition, Select
Series, Check-In Series, Founders Edition) is a tag-color/distribution
classification, not a numbering restart by itself — record it via
`attributes.rarity`, not a directory split.

**Check-In Series is a mixed bag — verified against ~46 characters across
every venue squad (Canada's Wonderland, Carowinds, Cedar Point, Kings
Island, SDCC) via the Fandom wiki's own character infoboxes.** Most
Check-In-tagged characters carry perfectly ordinary numbers in this
directory's own continuous sequence (Joe #2881, Toro #2671, Odion #1705,
Aaron #2608, Stacy #299, etc.) — file these here with `attributes.rarity:
Check-In Series`, same as any other rarity tag, no restart involved. A
secondary source (squishlovers.com) claims the whole line restarts its own
numbering, but that only holds for a real, distinct minority: a handful of
characters carry a genuinely separate `SCI #N`-style number instead of (or
alongside) their normal one — Connor's SDCC 2022 variant (`SCI #10`),
Behemoth (`SCI #23`), Leviathan (`SCI #24`), and three using an
inconsistent `SCI12 #N` variant of the format (Yukon Striker `#25`,
Guardian `#28`, The Fly `#29`). No confirmed starting point (`SCI #1`) or
complete list exists for this subset, and most Cedar Point/Kings Island
characters have no documented number at all yet — too thin to scaffold a
sibling collection on. **Don't file an item under a bare `SCI #N` number in
this directory** (it isn't part of this sequence) — if you find one, note
it and hold off rather than guessing where it belongs; this is a real but
still-open sourcing gap, not a settled sub-line the way Fuzz-A-Mallows and
Squish-Doos are.

## Manufacturer

Squishmallows launched in 2017 under **Kelly Toys Holdings, LLC**
("Kellytoy"); **Jazwares, LLC** partnered with Kelly Toys in 2019 and
acquired it outright in April 2020. Use whichever manufacturer name is
actually printed on the item's hangtag/box (`attributes.manufacturer`) rather
than defaulting to one — pre-2020 releases generally credit Kelly Toys,
later releases credit Jazwares. Don't assume; check the actual credit.

## Identifying items

Figures are identified by their **Collector Number**, printed on the hangtag
alongside a size code, e.g. a tag reading `S5 #1366-2` is size 5", Collector
Number 1366, second released version/colorway of that number. Use the bare
Collector Number (without the size prefix) as `attributes.number`. A
dash-suffixed version (`-2`, `-3`, ...) is the *same* base character and
Collector Number, just a different print/colorway — file it as a `variants`
sub-entity on that item (`id`/`name` only — name it by the actual colorway if
known, otherwise `2nd Version`/`3rd Version`) rather than a second top-level
file — see
[`../../../docs/primitives/ITEM.md`](../../../docs/primitives/ITEM.md),
"Variants."

**Collector Number is not globally unique across all of Squishmallows** —
only within this directory's scope (the standard line + licensed collabs).
Fuzz-A-Mallows and Squish-Doos each restart their own sequence, and a
minority of Check-In Series items carry a separate `SCI #N`-style number
too (see above) — always confirm which sub-line a number belongs to before
treating it as this directory's own.

Licensed characters (Pokémon, Disney, Sanrio, etc.) don't get a
**Squishdate** (the MM.DD.YYYY design-finalization date Kellytoy/Jazwares
prints for characters they created) or the personality-blurb bio that
standard-line characters get — don't treat a missing Squishdate as an error
for a licensed item.

Look up the number and metadata rather than guessing — the [Squishmallows
Wiki](https://squishmallowsquad.fandom.com/) (Collector Number List, Master
List) and [SquadApp](https://squadapp.app/) are the closest equivalents to
Funko's HobbyDB/Pop Price Guide; cross-reference more than one where
possible, since neither is as consistently authoritative as a
manufacturer-run database.

## Bulk sourcing (numbers 21-3205 filed this way)

Fetching `squishmallowsquad.fandom.com` through a generic web-fetch tool or
plain web search is unreliable — the site blocks or 402s many automated
fetches, and falling back to search-snippet synthesis produces confidently
wrong, self-contradictory answers (verified by trying it — see
[[project_squishmallows_curation]] in curator memory for specifics). What
actually works: `curl` with a browser user-agent against the Fandom wiki's
own MediaWiki API, which isn't blocked. Two calls matter:

- The **Collector Number List** page's raw wikitext (`action=parse&page=Collector_Number_List&prop=wikitext`)
  gives the full number→name mapping in one fetch (goes past 3200 as of this
  writing) — this page cites itself to the official "Collector's Guide and
  Trading Cards," so it's a reasonably authoritative primary source on its
  own, not just wiki-editor guesswork.
- Individual character pages can be **batch-fetched 50 at a time**
  (`action=query&prop=revisions&rvprop=content&rvslots=main&titles=A|B|C...&redirects=1`),
  which turns thousands of would-be one-by-one fetches into ~50 requests.
  Each page's `{{Squishmallow_Infobox|...}}` (or `{{Squishmallow Infobox}}`
  — both spellings exist) carries `type=` (species), `collector_number=`,
  `squishdate=`, and `year=` as machine-parseable fields.

**Confirmation policy actually used at this scale**: trust the List page's
name+number pairing by default (it's already a named, cited source). Only
skip a number if the individual character page's own `collector_number=`
field states a *different* number than the List assigned it (a real,
specific conflict — e.g. two characters' own pages both claiming the same
number) — don't skip merely because the individual page lacks the field
entirely; that's "unconfirmed by a second source," not "contradicted."
Requiring independent double-confirmation for every single entry (the
standard used for the first ~48 numbers, filed by hand) doesn't scale past a
few dozen items and left too much on the table — most of the catalog only
has the List page to go on, and it's reliable often enough (>97% agreement
where a second source exists) to trust by default.

For the **name**, prefer the bio's bolded name (e.g. resolves "Cam" over the
List's own display text "Cameron") but fall back to the List's display text
when the bio's markup doesn't parse cleanly (occasionally a bio splits the
bolded name across a wikilink, e.g. `'''JSK the''' [[Cat|'''Cat''']]`) — the
List text is usually clean even when the bio isn't. If neither is clean,
skip the number rather than filing a mangled name.

## Naming files

`<number>-<slugified-name>.yaml`, number zero-padded to 5 digits (e.g.
`01366`). Five digits is a judgment call based on current catalog volume
(Collector Numbers are already past 1,000 as of 2024, and the line is
growing faster than Funko Pop or Nendoroid did at a comparable age) — not a
canonical width, since this is a continuously growing line with no fixed
endpoint. Use the full printed name for the slug (e.g. `hans-the-hedgehog`,
not just `hans`) — Squishmallow names routinely repeat the first name across
unrelated species (see Common pitfalls). A version suffix on the tag (e.g.
the `-2` in `S5 #1366-2`) doesn't get its own file — see "Identifying
items" above.

## Sizes

Unlike Funko's variant suffix or Nendoroid's `-DX` suffix, a size difference
does **not** get its own Collector Number — the same character is typically
sold in several simultaneous sizes (a tag might read `S8`, `S16`, etc. across
different physical products, all sharing one number) with no single size
being more "canonical" than another. Don't try to force one size into
`attributes.size` for a general character entry — leave it off unless you're
cataloguing a specific release where the size is itself the distinguishing
fact (e.g. a retailer-exclusive size, like a 24" Costco-only release).

## `rarity`

`attributes.rarity` is enum-validated in `item-attributes.schema.json`. The enum
starts with Jazwares' own published tiers (`Rare`, `Ultra Rare`, `Special
Edition`, `Select Series`, `Founders Edition`) and is expected to grow — it
is not meant to gate curation, and a standard common release simply omits
the field rather than needing a `Common` value. If a real rarity/distribution
label isn't in the enum yet, confirm it against Jazwares' Rarity Scale page
or a fan database, then add it to the `enum` array alongside the item(s)
that need it.

## Common pitfalls

- Don't confuse the **Collector Number** with a UPC/barcode or a retailer's
  internal SKU — the number that matters is the one printed on the hangtag
  next to the size code.
- **Duplicate first names across unrelated species are common** (Squishmallow
  names are drawn from a shared pool independent of species) — always key
  identification off the full name + Collector Number, never the first name
  alone.
- Don't conflate **Squishdate** (design-finalization date) with the item's
  actual release/manufacture date — if populating the top-level `date`
  field, use a real sourced release date per [`../../CLAUDE.md`](../../CLAUDE.md),
  not the Squishdate.
- `manufacturer` isn't always "Jazwares, LLC" — check whether the item
  predates the 2020 acquisition (see Manufacturer above).
- Retailer exclusivity (Target, Walmart, Costco, Amazon, BoxLunch, Claire's,
  Cracker Barrel, Kohl's, and more) isn't centrally documented anywhere
  official — record it via `attributes.exclusive_to` when a source confirms
  it, but don't assume a release is exclusive just because you can't find it
  elsewhere.
- This line has no fixed endpoint, so there's no "verify the set is
  complete" step the way a card set has — completeness here just means
  cross-checking whatever range you're curating against the Squishmallows
  Wiki or SquadApp for that range.
- The Squishmallows Wiki's own per-character pages don't always agree with
  its Collector Number List page — when they actively conflict (both claim
  a different number for the same character, or two characters claim the
  same number), skip it rather than guessing which is right. See "Bulk
  sourcing" above for when a *missing* field (as opposed to conflicting one)
  is fine to proceed on. A gap in the sequence (e.g. a missing number
  between two filed ones) means "not yet verified or a real numbering gap
  the wiki marks '???'," not "doesn't exist."
- As of this writing, numbers 1-3205 have been swept once (chronological,
  bulk-sourced per above) with the following still open: numbers where the
  List and a character's own page actively conflict (skipped), a handful of
  pages that don't fetch cleanly or lack the standard infobox, and 3 pages
  where neither the bio nor the List gave a cleanly parseable name. Treat
  any number in this range that isn't filed as one of these known gaps, not
  as unswept territory — re-verifying them means resolving the specific
  conflict/parse failure, not re-researching from scratch. Numbers past
  ~3205 (the List's current end) are genuinely new territory as the catalog
  keeps growing.
