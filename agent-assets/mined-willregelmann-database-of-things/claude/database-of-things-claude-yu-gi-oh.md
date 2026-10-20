# Yu-Gi-Oh! TCG — curation hints

A playable trading card game, published by Konami. This directory covers the
**English-language TCG only** — see Scope below.

## Directory structure

```
yu-gi-oh/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole Yu-Gi-Oh! TCG
  <slugified-set-name>/           # one set, e.g. legend-of-blue-eyes-white-dragon
    _collection.yaml
    <number>-<slugified-card-name>.yaml   # flat, when only one printing is maintained
    <printing>/                   # only when a set has genuinely distinct
      _collection.yaml            # printings actually being maintained —
      <number>-<slugified-card-name>.yaml # see Printings are separate entities
```

**No series tier above the set — sets sit directly under the game, as in
[`../magic-the-gathering/`](../magic-the-gathering/), rather than under
Pokémon's series → expansion → card.** (The tier *below* the set is the
printing, which is a different thing — see Printings are separate entities.)
Yu-Gi-Oh! does use the word "Series," but it
means something else: an **OCG card-layout era** (Series 1, 2, 3 …), a design
period defined by how cards were printed, not a Konami grouping of TCG set
releases. There is no marketing tier above the set the way Pokémon has
"Scarlet & Violet Series." Don't invent one — see
[`../../CLAUDE.md`](../../CLAUDE.md#tree-shape).

**This means ~339 set directories at one level, and that's accepted.** It
exceeds the 100-nested-collections guideline in
[`../../CLAUDE.md`](../../CLAUDE.md), which is explicitly "a prompt to look
for a real missing grouping level, not a hard ceiling to engineer around when
no natural one exists." Here none exists.

The tempting non-answer is **set type** — grouping sets as Booster Packs,
Structure Decks, Starter Decks, Duel Terminal, Legendary Collections and
promos, the way Yugipedia's own category tree does. **Don't.** That's a
*product* axis: it describes the sealed package cards were distributed in,
not the cards. DBoT catalogues collectibles, and the collectible here is the
card — a booster pack is how you got it. The set prefix is printed on the
card itself; "came in a Structure Deck" isn't. If set type ever needs
recording, it belongs on the set's own record, not as a directory tier.

## Scope

**English TCG only.** The Japanese-market **OCG** is a genuinely different
game — different card pool, different legality, different release schedule —
and Konami runs the two separately.

**The OCG's placement is an open decision, deliberately deferred.** If it's
ever curated it belongs under *this* brand rather than a new top-level
`yu-gi-oh-ocg/`, which would split the brand (see
[`../../CLAUDE.md`](../../CLAUDE.md#tree-shape)). That means introducing a
`tcg/` + `ocg/` tier here and moving every existing set down one level. Make
that call **before** filing OCG cards, not after — it's cheap now and a
several-hundred-directory migration later.

## Identifying cards

A card's identity is its printed **Card Number**, bottom-right on the card:

```
LOB-EN001
 |   |  └── position in the set, zero-padded
 |   └───── region/language code
 └───────── set prefix
```

Record the **full printed code** in `attributes.number` (`"LOB-EN001"`), not
just the position — it's what's on the card and what collectors quote.

**Two traps here, both verified against Yugipedia's own set data:**

- **The set prefix is not constant across languages.** Legend of Blue Eyes
  White Dragon is `LOB-EN` in English, `LOB-G` in German and `LOB-E` in the
  early European run — but **`LDD`** in French, Italian and Spanish, and
  **`LDB`** in Portuguese. A prefix identifies a set *within a region*, not
  globally. Don't assume the English code generalises, and don't "correct" a
  non-English code to match it.
- **Early North American cards carry no region code at all.** The 2002–2004
  print runs are numbered `LOB-001`, not `LOB-EN001`; the unified `-EN`
  convention arrives later (Legend of Blue Eyes' English-prefixed run is
  dated 2004-12-01, against 2002-03-08 for its North American debut). Record
  what's actually printed on the card being catalogued rather than
  normalising to the modern form.

Special-position codes exist too — `-ENSP1` for Sneak Preview and `-ENSE1`
for Special Edition cards — so the position segment isn't always three
digits. The schema pattern is deliberately permissive about this.

### Printings are separate entities

**Each printing of a set is its own nested collection, and its cards are their
own entities.** This follows directly from
[`../../CLAUDE.md`](../../CLAUDE.md#collectibles-not-products): the printed
card number differs between printings, so the objects are physically distinct,
and the catalog deduplicates on physical uniqueness rather than on product
identity.

**Only one printing per set is currently maintained — Worldwide English
(`LOB-EN` prefix) for Legend of Blue Eyes, filed flat directly under the set
directory, no printing-level subdirectory.** This is a deliberate scope
decision, not an oversight: Legend of Blue Eyes was issued in four distinct
English printings (North American, European, Oceanic, Worldwide English),
but that regional split is essentially unique to this one transitional-era
set — once Konami settled into the unified `-EN` convention Worldwide
English represents, virtually every other Yu-Gi-Oh set only ever had a
single English printing. Maintaining just Worldwide English, flat, keeps
this one already-curated set consistent with how the ~338 other uncurated
sets will naturally be filed, rather than carrying a four-way split that's a
special case of exactly one set.

**A printing-level subdirectory is for when a set has multiple printings
genuinely being maintained side by side — not a mandatory tier.** Earlier
guidance here said every set gets one "so the shape stays uniform," even
with only one printing; that's been reversed. Go flat (cards directly under
the set directory) by default, and only introduce `<printing>/`
subdirectories if a set's other printings are actually filed alongside each
other.

The other three printings of Legend of Blue Eyes (North American, European,
Oceanic) were curated and then removed to enact this scope decision —
recoverable from git history, not the live catalog. Their data is worth
recording here in case a future Yu-Gi-Oh-focused curation pass wants to
reinstate them alongside Worldwide English (at which point all four would
move under printing subdirectories together, including Worldwide English):

| printing | prefix | released | cards |
|---|---|---|---|
| North American (removed) | `LOB-` | 2002-03-08 | 126 |
| European (removed) | `LOB-E` | 2002-12 | **103** |
| Oceanic (removed) | `LOB-A` | 2003-09 | 126 |
| Worldwide English (maintained, flat) | `LOB-EN` | 2004-12-01 | 126 |

The European printing being **103 cards rather than 126** was the clearest
demonstration that these aren't relabelled copies of one another — it was a
materially different set. Printed names differed too: the North American
printing had "Trial of Hell" and "Red-eyes B. Dragon" where Worldwide English
has "Trial of Nightmare" and "Red-Eyes B. Dragon".

If printings beyond Worldwide English are ever reinstated: name a printing
directory for its **region**, not its prefix — `north-american/`, not
`lob/`. Non-English printings (German, French, Italian, Spanish, Portuguese)
are out of scope per Scope above.

**`attributes.total_cards` belongs wherever the cards actually are** — on the
set record when filed flat (as Legend of Blue Eyes is now), on each printing
record when a set has genuinely distinct printings nested underneath it.

### Editions

**An edition is a printing axis too, not a card attribute.** A 1st Edition
card and an Unlimited card are physically distinguishable, so by the same rule
they're separate entities. Splitting an edition means introducing printing
subdirectories under the set even for a currently-flat one — e.g.
`worldwide-english-1st-edition/`, `worldwide-english-unlimited/` — rather
than one card carrying an `edition` field.

**Not yet applied, because the data isn't there.** Yugipedia's set lists carry
only `number; name; rarity`, and its card pages carry no per-printing edition
data either. Watch out for one false friend: a card page's `Unlimited` value
sits in `tcg_speed_duel_status`, which is **banlist** status — how many copies
may be played — not print edition. Don't wire that up by mistake. Edition
appears only in prose on set pages.

The printings filed so far are therefore edition-agnostic. Splitting them
needs a source documenting which editions each regional printing actually had
— a collector database or Konami print-run record. Until one is found, don't
guess, and **don't add an `edition` attribute as a stand-in**: that would
encode the axis in the wrong place and have to be unpicked across every filed
card later.

## Naming files

`<number>-<slugified-card-name>.yaml`, using **only the position digits** of
the card number, zero-padded to the set's width — `001-blue-eyes-white-dragon.yaml`
for `LOB-EN001`. The set prefix and region already come from directory
position and `attributes.number`, so repeating them in the filename adds
nothing and would sort identically anyway.

**Sets can start at `000`.** Legend of Blue Eyes runs `LOB-000` (Tri-Horned
Dragon) through `LOB-125` — 126 cards, zero-based. Don't assume a set's
numbering starts at 001, and don't renumber a `000` card to make the range
look conventional; `total_cards` and the highest number legitimately differ
by one in these sets.

Set directories use the plain slugified set name, no prefix —
`legend-of-blue-eyes-white-dragon/`, not `lob-legend-of-blue-eyes-white-dragon/`.
Yu-Gi-Oh! sets have no canonical ordering number, and sorting by prefix code
would order the directory neither alphabetically nor chronologically.

## Rarity

`attributes.rarity` is enum-validated. Yu-Gi-Oh!'s rarity ladder is unusually
long and still growing — Yugipedia lists 78 rarity pages across TCG and OCG.
The enum here covers the TCG ones and, like
[`../../figures-and-models/good-smile/nendoroid/CLAUDE.md`](../../figures-and-models/good-smile/nendoroid/CLAUDE.md)'s
`release_type`, **is expected to grow and is not meant to gate curation**. If
a card's real printed rarity isn't listed, confirm it against Yugipedia and
add it to the enum in the same PR as the card.

Expect that to happen early and often: Yugipedia's `Category:Rarities` pages
are *not* a complete list of the labels its set lists actually use. **Super
Short Print** appears throughout Legend of Blue Eyes but has no category page
of its own — it was missed on the first pass of this enum and added from the
set data. Trust the set list over the category tree.

Don't record OCG-only rarities (Millennium, Kaiba Corporation, Rush/Over Rush
variants) — they don't appear on TCG cards.

## Edition

There is **no `edition` attribute** — see Editions above. 1st Edition,
Unlimited and Limited Edition are printing-level distinctions, so they belong
as sibling printing collections once the data exists to split them, not as a
field on a card.

Note edition is a TCG/Korean-OCG concept in the first place: Japanese,
Japanese-Asian and Chinese OCG cards carry no edition marking at all. Another
reason the OCG needs its own conventions if it's ever curated.

## Sourcing

**[Yugipedia](https://yugipedia.com/) is the authoritative source**, but it
returns **HTTP 403 to plain web-fetch tools**. Its MediaWiki API is not
blocked — reach it with `curl` and a browser user-agent, the same technique
[`../../plush/squishmallows/CLAUDE.md`](../../plush/squishmallows/CLAUDE.md)
documents for Fandom:

```bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
# a set's structured data — prefixes, per-region release dates, cover card
curl -s -A "$UA" "https://yugipedia.com/api.php?action=parse&page=Legend%20of%20Blue%20Eyes%20White%20Dragon&prop=wikitext&format=json"
# every set of a given type
curl -s -A "$UA" "https://yugipedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:TCG_Booster_Packs&cmlimit=500&format=json"
```

A set page's infobox carries `en_prefix`, every regional prefix, and a
`*_release_date` per region as machine-parseable fields — far more reliable
than scraping the rendered page or synthesising from search snippets.

**The card list is not on the set page.** It lives in its own namespace
(`Set Card Lists`, id 3006), one page per set *per region*, titled
`Set Card Lists:<Set Name> (TCG-<REGION>)`:

```bash
# find the regional list pages for a set
curl -s -A "$UA" "https://yugipedia.com/api.php?action=query&list=allpages&apprefix=Legend%20of%20Blue&apnamespace=3006&aplimit=50&format=json"
# fetch one
curl -s -A "$UA" "https://yugipedia.com/api.php?action=parse&page=Set%20Card%20Lists%3ALegend%20of%20Blue%20Eyes%20White%20Dragon%20(TCG-NA)&prop=wikitext&format=json"
```

Rows sit inside a `{{Set list|region=…|` template, semicolon-delimited as
`number; name; rarity` — one parse gives a whole set's number → name → rarity
mapping:

```
LOB-000; Tri-Horned Dragon; Secret Rare
LOB-001; Blue-Eyes White Dragon; Ultra Rare
```

**Pick the region page that matches what you're cataloguing** — `TCG-NA` and
`TCG-EN` are separate pages with different numbering, which is the
region-prefix trap above showing up directly in the source.

A row may carry an inline `//description::` note, most often recording that a
card was printed under a different name in this set than the one it's known
by now (`LOB-012` is "Trial of Nightmare", printed as "Trial of Hell" until
the 2002 Collectors Tins). **Use the name as printed in the set being
catalogued**, and note the rename in the card's own record rather than
silently filing it under its modern name.

## Common pitfalls

- **Use the region-appropriate prefix**, not the English one — see
  Identifying cards above (`LDD`/`LDB`, not `LOB`, for several languages).
- **Don't normalise early `LOB-001`-style numbers to `LOB-EN001`.**
- **Don't assume numbering starts at 001** — see Naming files above.
- **A card's printed name can differ from the name it's known by today.**
  File it as printed in the set being catalogued.
- **A card reprinted in a later set is a separate entity file** under that
  set, with that set's own number — not a variant folded into the original.
  Heavily-reprinted staples appear in dozens of sets, each a legitimate
  separate collectible.
- **`date`**: use the release date for the region being catalogued. A set's
  North American, European and Australian dates can differ by 18 months (see
  Legend of Blue Eyes: 2002-03, 2002-12, 2003-09). Don't merge them.
- **Don't record gameplay data** — card type, Attribute, Level, ATK/DEF,
  effect text. That's rules data, not what identifies the collectible, and
  the catalog stays minimal by design (see the root
  [`../../../CLAUDE.md`](../../../CLAUDE.md)).
- **No illustrator field.** Unlike Pokémon TCG, Yu-Gi-Oh! cards don't credit
  their artist on the card.

## Logo

`_collection.yaml` uses the English **Yu-Gi-Oh!** wordmark — the red-brushstroke
lockup carried on TCG packaging — from Wikimedia Commons.

This is the [`../../CLAUDE.md`](../../CLAUDE.md) carve-out, not a violation of
it. That file bars pointing a *merchandise line* at the logo of a franchise
it's merely licensed from, and contrasts it with "the Pokémon TCG collection,
whose logo is correct precisely because that collection *is* the Pokémon TCG,
not a product based on it." Yu-Gi-Oh! is the same case: the card game isn't a
product spun off from the brand, it's what the brand denotes. A general
Yu-Gi-Oh! wordmark is this entity's own mark.

Use the English wordmark rather than the Japanese 遊戯王 manga logo, which is
the manga's, not the game's.
