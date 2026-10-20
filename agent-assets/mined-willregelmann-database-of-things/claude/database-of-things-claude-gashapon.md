# Gashapon — curation hints

## What belongs here

"GASHAPON" is a Bandai-owned trademark (registered in Japan, the US, the EU,
and elsewhere) for its own capsule-vending-machine toy business, running
since 1977. Only Bandai's own **character figure/diorama** capsule sets sold
under that trademark belong here — check both boundaries below before filing
something as gashapon:

- **Not Bandai's non-figure capsule products.** Bandai's gashapon lineup also
  includes food miniatures, animal replicas, stationery, and accessories with
  no character depicted — same carve-out as
  [`../../re-ment/CLAUDE.md`](../../re-ment/CLAUDE.md). A capsule toy that merely
  features a franchise's logo or a non-character object isn't a standalone
  character figure and doesn't belong in `figures` at all.
- **Not other companies' capsule toys.** "Gachapon"/"capsule toy" is a
  generic category with many manufacturers — Kitan Club, Takara Tomy A.R.T.S.,
  T-ARTS, Yell, and others all sell visually similar capsule figures, often
  stocked in the same vending banks as Bandai's. So does Bandai's own sister
  brand **Banpresto**, whose prize/arcade figures (e.g. "World Collectable
  Figure") are a separate product line, not vended from a gashapon capsule
  machine. None of these are Bandai's GASHAPON-branded product — verify the
  box/listing actually credits Bandai's Gashapon brand before filing here
  rather than assuming from visual similarity or shelf placement.

## Directory structure

```
gashapon/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # Gashapon itself
  <franchise>/                   # licensed IP depicted, or the line's own
                                  # name for a wholly original (unlicensed)
                                  # Bandai mascot/novelty character line
    _collection.yaml
    <series>/                    # one named capsule-toy release — Bandai's
                                  # own product name for that set
      _collection.yaml
      <slugified-character-name(s)>.yaml
```

Same three-tier shape as [`../../re-ment/CLAUDE.md`](../../re-ment/CLAUDE.md):
Bandai runs many independently-named gashapon series per franchise, and a
popular series routinely continues across multiple volumes/waves — nest a
`vol-<NN>/` (or the series' own official wave/part naming, if it differs)
under the series directory the same way Re-Ment does once a second release
appears, rather than flattening every wave's figures into one directory.

## Series and set names are official — verify, don't infer from a retailer

Source a set's real product name and roster from Bandai's own listings
before filing anything:
- **Japan**: [gashapon.jp](https://gashapon.jp/) is Bandai's own current
  catalog.
- **English-market releases**: [us.gashapon.jp](https://us.gashapon.jp/)
  covers the (smaller) subset localized for the US.
- [Premium Bandai](https://p-bandai.jp/) sometimes carries gashapon-adjacent
  exclusives — confirm a listing is actually GASHAPON-branded, not a
  different Bandai storefront's own product, before treating it as part of
  this line.

A retailer or aggregator listing is fine as a first-pass lead, but Bandai's
own product page is the source of truth for the release name, roster, and
date — the same bar as Re-Ment.

## Known pitfalls

- **"All N types" often hides a secret/rare variant.** A set advertised as a
  fixed count frequently ships a lower-odds "secret" (シークレット) design
  on top of the stated lineup — check the actual box art/official product
  photos for a secret callout before assuming the advertised count is
  the complete roster.
- **Recolors and reissues are common under a near-identical name.** Bandai
  frequently reissues a popular gashapon set later with new colors/finishes
  ("Vol. 2", a seasonal recolor, etc.) rather than a wholly new sculpt —
  don't assume a same-named listing found later is a duplicate of one
  already curated; check whether it's actually a distinct release before
  merging or skipping it.
- **No reliable universal per-figure catalog number.** Unlike Nendoroid,
  individual gashapon figures generally carry no printed figure number —
  identify a figure by the character(s)/subject it depicts within its
  series directory, matching
  [`../../re-ment/CLAUDE.md`](../../re-ment/CLAUDE.md)'s approach. Some series do
  print a position number on the base or in official photos (e.g. "1 of 6")
  — record it as `attributes.number` when a specific release confirms one,
  but don't assume every series has it.

## Naming and identifying figures

`name` is the character(s)/subject(s) depicted, joined with " & " for a
paired design (e.g. `Goku & Vegeta`). File slug matches:
`goku-vegeta.yaml`. `attributes.character` lists the same subjects as a
structured array, using each character's official English name.

**A series can depict the same character more than once** (different pose,
outfit, or scene) — a bare character name would collide as a filename.
Disambiguate with a short parenthetical pose/scene descriptor in both `name`
and the slug (e.g. `Goku (Kamehameha)` → `goku-kamehameha.yaml`), the same
judgment call as Re-Ment's disambiguation approach — describe what's
actually different, don't reach for a fixed vocabulary.

## Attributes

See `item-attributes.schema.json`. `attributes.brand_line` records Bandai's own
capsule-toy sub-brand for the release (e.g. "Ringcolle!", "HGIF",
"Cap-Chara", "ChibiMasters") when the listing is marketed under one — this
is a real, verifiable Bandai product distinction that directory position
(franchise-first) doesn't capture, so don't skip recording it when a
listing states it. Leave it off for a release sold as a plain "GASHAPON"
capsule toy with no further sub-brand.

## Images

Attach `image` pointing at Bandai's own official gashapon.jp (or
us.gashapon.jp) product photography once you've confirmed which photo
matches which figure, per the root
[`collections/CLAUDE.md`](../../../CLAUDE.md) image guidance. Fall back to a
retailer/marketplace photo per the project's general image-sourcing policy
only if no official photo is available.

## Dates

For a series' own `_collection.yaml`, use its first release date as listed
on Bandai's own product page. If the true original release date isn't
independently confirmable (e.g. an older set no longer listed and only
known via a reissue), leave `date` off rather than guessing — see the root
[`collections/CLAUDE.md`](../../../CLAUDE.md).
