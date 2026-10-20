# Magic: The Gathering — curation hints

This category is freshly scaffolded — structure and conventions below are a
starting point, not yet battle-tested against real curation the way
[`pokemon-tcg/CLAUDE.md`](../pokemon-tcg/CLAUDE.md) is. Expect this file to
grow the same way: confirm facts against an authoritative source as you go,
and record what you learn (including corrections to guidance below) rather
than trusting it blindly.

## Directory structure

```
magic-the-gathering/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml                # the whole "Magic: The Gathering" collection
  <block>/                        # only for sets released as part of an official block
    _collection.yaml              # the block, e.g. "Ravnica Block"
    <set>/
      _collection.yaml            # the expansion/set, e.g. "Ravnica: City of Guilds"
      <card>.yaml
  <set>/                          # standalone sets (no block), nested directly here
    _collection.yaml
    <card>.yaml
```

Mirrors Pokémon TCG's series → expansion → card split, but only where it
actually applies: Wizards organized Magic into official blocks from the
early years through the Ixalan block (2017-18), then dropped the block
structure starting with Dominaria (2018) — sets since then stand alone
directly under `magic-the-gathering/`. **Not every set from the block era was
part of a block either** — supplemental products (Chronicles, the Portal
line, Deckmasters, anthologies, etc.) released standalone even during those
years. Determine block membership from an authoritative source (Wikipedia's
"List of Magic: The Gathering sets", or Scryfall's own set-type/block
metadata) rather than guessing from release-year proximity — same discipline
as Pokémon TCG's "look it up, don't guess from the name alone" rule for
series membership.

**Core sets are not blocks, despite what Scryfall's API response looks
like at a glance.** Scryfall's `/sets/<code>` response tags every core set
(Alpha, Beta, Unlimited, Revised, 4th–10th Edition, M10–M15, etc.) with
`"block": "Core Set"` and a `block_code`, but that's Scryfall's own
UI-grouping label, not a real Wizards-designated block — confirmed on
Alpha/Beta, where `block_code` is literally just the set's own code
(`"lea"`/`"leb"`) rather than pointing at a shared block-defining set the
way real blocks do (e.g. Ravnica block's `block_code` is `"rav"` on all
three of its member sets). Wikipedia's set list also keeps "Core sets" in
their own table, separate from every expansion-block table. Treat core
sets as standalone — filed directly under `magic-the-gathering/`, e.g.
`limited-edition-alpha/`, `limited-edition-beta/` — not nested in a
`core-set/` block directory.

**Naming block/set directories**: lowercase, hyphenated, same convention as
everywhere else (e.g. `ravnica-block`, `ravnica-city-of-guilds`).

## Data source

**Scryfall's API (`api.scryfall.com`) is this category's equivalent of the
Pokémon TCG API** — bulk set/card metadata, including collector number,
rarity, colors, mana cost, type line, illustrator, and card images.
`/sets` lists every set (`code`, `name`, `released_at`, `card_count`,
`set_type`, `block`); `/cards/search?q=set:<code>` or the bulk-data exports
return full checklists. Cross-check against Gatherer (Wizards' own official
card database) when Scryfall looks inconsistent, the same way Pokémon TCG
curation falls back to Bulbapedia when the Pokémon TCG API looks wrong —
Scryfall is a convenient bulk source, not infallible.

**Always take `image` directly from the API response's own
image field** (Scryfall's `image_uris.large` or, for double-faced cards,
each face's own `image_uris`) — never hand-construct the URL from a
pattern, same rule as Pokémon TCG.

## Identifying items

Cards are identified by their **collector number within a set**,
`attributes.number` — the same primary-disambiguator role collector number
plays in Pokémon TCG, since names repeat across printings/reprints. Stored
as `attributes.number: "<n>/<total>"`, same fraction format as Pokémon TCG,
using Scryfall's `collector_number` as `<n>`.

**Confirmed: Limited Edition Alpha and Beta print no collector number on
the card at all** — this era predates the convention entirely (Wizards
started printing numbers on cards later in the mid-1990s). Scryfall still
assigns each card a `collector_number` (1-295 for Alpha, 1-302 for Beta,
alphabetical-ish by color pile, basic lands last) for database bookkeeping,
and this assigned number is the de facto standard identifier used
throughout the hobby (TCGplayer, EDHRec, price guides, Scryfall's own UI
all reference "Alpha #232" etc.) even though it's not physically printed —
adopted it here for exactly that reason. **When curating a later set,
verify whether that set's cards print a real number before assuming
Alpha/Beta's "not printed, use Scryfall's" precedent carries forward** —
don't assume every pre-modern set behaves the same way without checking.

## Naming files

`<number>-<slugified-name>.yaml`, number zero-padded to the set's total
digit width — same convention as Pokémon TCG. Reprints of the same name
within a set (e.g. multiple basic Forest arts) get disambiguated by number,
which is already unique.

## Rarity

`attributes.rarity` is enum-validated in `item-attributes.schema.json`. The enum
starts small (`Common`, `Uncommon`, `Rare`, `Mythic`, `Special`, `Bonus`,
`Land`) and is expected to grow the same way Pokémon TCG's did — it's not
meant to gate curation. Values are title-cased from Scryfall's own
lowercase `rarity` field (`common`/`uncommon`/`rare`/`mythic`/`special`/
`bonus`).

**Confirmed: basic lands in Alpha/Beta are `rarity: common`, same as any
other common** — Scryfall does not give them a distinct "land" rarity
tier, so the `Land` enum value went unused for this era. It's left in the
schema speculatively for a later era where it might apply (some very old
or special-product basic lands are sometimes described as having no real
rarity at all) — **verify against Scryfall before ever using it, and
remove it from the enum if no set ever turns out to need it**, don't treat
its presence as confirmation it's a real value.

If a real rarity value isn't in the enum yet, add it to
`item-attributes.schema.json` in the same PR that adds the card needing it,
confirmed against Scryfall or Gatherer first — don't invent a label or
force a near-miss existing value to avoid the schema edit. `Mythic` did
not exist until 2008 (Shards of Alara) — don't expect it before then.

## Colors

`attributes.colors` is an array of `W`/`U`/`B`/`R`/`G`, sourced from
Scryfall's `colors` field. **Confirmed convention: omit the key entirely
for colorless cards** (artifacts, lands) rather than writing `colors: []`
— matches this repo's general minimal-metadata philosophy of leaving
inapplicable fields out rather than writing an empty/null placeholder.

For double-faced, split, or other multi-face cards, this hasn't been
decided yet — resolve it (front face's colors? union of both faces?
Scryfall's own top-level `colors` vs. per-face `card_faces[].colors`?)
when the first such card is actually curated, and document the decision
here.

## Common pitfalls (initial — expand as real curation surfaces more)

- **Foil vs. non-foil is a finish, not a separate print**, in most sets —
  same collector number, don't create separate card files for it. Some
  products do print foil-only cards with their own distinct collector
  number (promotional and some set-booster exclusives); those genuinely are
  separate cards.
- **Alternate-art/showcase/borderless/extended-art variants** of the same
  card within a modern set typically get their own separate collector
  number — treat each as its own card file, same disambiguation-by-number
  approach as Pokémon TCG reprints within a set.
- **Double-faced cards** (transform, modal DFC, meld) print two faces on one
  physical card. Model as a single card entity, not two — but the `name`
  and `attributes` convention for capturing both faces (Scryfall itself
  joins them as `"Front Name // Back Name"`) isn't decided yet; resolve it
  when the first one is curated.
- **Basic lands** (Forest, Island, Mountain, Plains, Swamp, and colorless
  Wastes) are reprinted with new art across nearly every set, often with
  several numbered variants in the same set — high file count, low
  per-card novelty. **When a set's basic lands are genuinely part of its
  own official numbered checklist** (confirmed for Alpha: 10 land cards
  among its 295; Beta: 15 among its 302 — each art variant gets its own
  collector number same as any other card), generate them along with the
  rest of the set; they're not an optional extra, the checklist isn't
  complete without them. This is different from a set *reusing* an
  earlier set's land art without assigning its own numbers — that
  scenario hasn't come up yet, resolve it if/when it does.
- **Un-sets** (Unglued, Unhinged, Unstable, Unfinity), **Secret Lair
  Drops**, **Universes Beyond** crossovers, and other silver-bordered or
  not-Standard-legal products are real Wizards products but don't
  necessarily follow mainline set numbering/rarity conventions — scope each
  as its own decision when first encountered rather than assuming the
  mainline pattern applies.
- **Promo cards** (prerelease, buy-a-box, judge promos, FNM promos, etc.)
  aren't part of any numbered set — same treatment as Pokémon TCG's promo
  lines: their own top-level `promos/`-style collection, not folded into
  the nearest numbered set.

## Verifying a set is complete

Same approach as Pokémon TCG: a set's total card count is public and fixed
(Scryfall's `/sets` entry gives `card_count`). Confirm that many distinct
numbers exist as entity files, then cross-reference the checklist against
Scryfall and/or Gatherer rather than assuming — some sets have secret/bonus
cards numbered above the printed total, same pattern as Pokémon TCG secret
rares.
