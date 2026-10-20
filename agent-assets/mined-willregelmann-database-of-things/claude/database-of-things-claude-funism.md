# Funism — curation hints

## What belongs here

Funism's standalone character figures — blind-box designs and premium
statues alike — across **every** franchise/IP it produces, not just one.
Unlike Re-Ment (scoped to Pokémon only because that's the sole franchise
where Re-Ment sells actual figures), Funism's entire catalog is figures, so
this category is intentionally brand-scoped like Funko Pop!: licensed lines
(Pokémon, My Little Pony, Care Bears, Naruto, Neon Genesis Evangelion) and
original IP (Butterbear, Maltese, MOMO Bunny, Luo Xiaohei, Alexander the Fat
Tiger) are all in scope — only some may actually be curated at any given
time.

Non-figure merchandise carrying a Funism license (apparel, stationery,
homeware) is out of scope, same reasoning as Re-Ment.

## Directory structure

```
funism/
  CLAUDE.md
  item-attributes.schema.json  # manufacturer + character attributes, inherited by everything below
  _collection.yaml               # Funism itself
  <franchise>/                   # e.g. "pokemon", "my-little-pony", "care-bears", "butterbear"
    _collection.yaml
    <series>/                    # e.g. "Palmsize Wonders", "Adventure! Eevee", "Twinkmont"
      _collection.yaml
      CLAUDE.md                  # only where a series has its own quirks worth documenting
      vol-<NN>/                  # one blind-box release — only for blind-box series
        _collection.yaml
        <slugified-character-name(s)>.yaml
      <slugified-character-name>.yaml   # premium/statue series: each release stands alone, no vol- nesting
```

Two product formats coexist under one brand, and they nest differently:

- **Blind-box series** (e.g. Palmsize Wonders, Adventure! Eevee) release in
  numbered waves of several blind-wrapped designs, one guaranteed per full
  carton — same shape as [`../re-ment/CLAUDE.md`](../re-ment/CLAUDE.md).
  These get `vol-<NN>/` nesting under the series directory, one file per
  design inside. Follow Re-Ment's convention of still creating `vol-01/` for
  a series with only one release so far, since Funism's blind-box lines
  routinely add later waves.
- **Premium/statue series** (e.g. Twinkmont, Prime Figure Series) sell each
  release as its own named, non-blind product — no box roster to unbox. File
  these directly in the series directory, no `vol-NN` level.

Confirm which shape a series actually is (check whether a listing describes
it as a blind box / mystery design vs. a single named product) before
picking the nesting — don't assume from the series name alone.

## No printed catalog number on figures

Like Re-Ment, individual figures carry no manufacturer catalog number.
Identify a figure by the character(s) it depicts, scoped to its series (and
volume, if blind-box).

## Naming and identifying figures

`name` is the character(s) depicted, joined with " & " for a paired/scene
design (e.g. `Pikachu & Mareep`). File slug matches:
`pikachu-mareep.yaml`. `attributes.characters` lists the same names as a
structured array.

A series can repeat a character across different poses/scenes (common in
blind-box lines) — a bare character name would collide as a filename.
Disambiguate with a short parenthetical pose/scene descriptor in both `name`
and the slug (e.g. `Eevee (Sleeping)` → `eevee-sleeping.yaml`), same pattern
as Re-Ment.

## Identifying rosters — verify, don't trust a checklist blindly

Funism's own site (funismglobal.com, organized by franchise under
`/collections/<franchise>`) is the primary source for series names and
listings. Cross-reference against fan/retailer listings (Otaku Collectives,
NekoStop, BigBadToyStore, Galactic Toys, X-Playground, Target, eBay,
StockX) when the official site doesn't confirm a full box roster or release
date — but treat retailer-invented series names and auto-translated
character names with the same skepticism documented in
[`../re-ment/CLAUDE.md`](../re-ment/CLAUDE.md#identifying-rosters--verify-against-the-actual-photos):
confirm each character against product photos, not just a text listing.

## Dates

Prefer an official Funism release date when the site gives one. Where only
a retailer's "date first available" exists, treat it as approximate (it can
reflect a restock rather than the original release) — leave `date` off
rather than guessing, per the root [`collections/CLAUDE.md`](../../../CLAUDE.md).

## Images

Use Funism's own product photography (funismglobal.com) as the authoritative
source once a photo is confirmed to match the figure. Fall back to a
retailer/marketplace photo per the project's general image-sourcing policy
when no official photo is available — don't leave `image` off if a
reasonable source exists.

## Common pitfalls

- Don't assume every series is blind-box — Funism's premium/statue lines
  (Twinkmont, Prime Figure Series, Home Collection) sell named, non-random
  releases; check before picking `vol-NN` nesting.
- Don't treat `manufacturer` as always literally "Funism" without checking
  — original-IP lines and some licensed collaborations may credit
  differently; verify per series rather than assuming.
- This category, like Funko Pop! and Re-Ment, has no fixed endpoint —
  completeness just means cross-checking whatever franchise/series you're
  curating against Funism's own listing for it.
