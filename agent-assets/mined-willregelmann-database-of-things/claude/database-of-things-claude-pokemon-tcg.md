# Pokémon TCG — curation hints

## Directory structure

```
pokemon-tcg/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml              # the whole "Pokémon TCG" collection
  <series>/
    _collection.yaml            # the series, e.g. "Base Series"
    <expansion>/
      _collection.yaml          # the expansion/set, e.g. "Base Set"
      <card>.yaml
```

Three levels under this category, not two: **series → expansion → card**. A
series is a group of related expansions released together under one banner
(e.g. "Base Series" contains Base Set, Jungle, Fossil; "Neo Series" contains Neo
Genesis, Neo Discovery, Neo Revelation, Neo Destiny). An expansion is a single
released set — same level a card-containing directory already occupied before
this convention existed.

**Determining a set's series**: look it up, don't guess from the name alone.
Bulbapedia's "List of Pokémon Trading Card Game expansions" groups every
expansion under its official series — use that grouping, not an invented one.

**Naming series directories**: same convention as expansions — lowercase,
hyphenated (e.g. `base-series`, `neo-series`, `ex-series`).

**Migrating an expansion that's still flat under `pokemon-tcg/`** (not yet
nested under its series): move it, don't recreate it — `git mv <expansion>/
<series>/<expansion>/`. Card `id`s, filenames, and content are untouched by the
move; only the path changes.

## Collection records

Every `_collection.yaml` in this category — category, series, and expansion
level alike — carries a `description`: a short prose blurb of context
(release history, scope, what it spans). Match the tone of existing
`_collection.yaml` files. It isn't required by the schema, but every
existing record has one — include it when adding a new series or expansion.

These records used to also carry `category: Trading Card Games`, the same
value at every level. That field has been removed everywhere — it restated
what directory position already says, which is the same reason
`collection:`/`parent_collection:` don't exist. Don't reintroduce it.

Expansions also carry `image` pointing at the set's official
logo/box art (e.g. the Pokémon TCG API's `images.logo` for that set) when one
exists. Series records usually don't get one — most series (e.g. "Original
Series") are retroactive groupings with no single official logo to point to;
don't invent one.

**Always take `image` (both card- and set-level) directly from
the API response's own `images` field — never hand-construct the URL from
a pattern.** The API's image CDN is mid-migration: older sets serve from
`images.pokemontcg.io/<setId>/<n>_hires.png` (and `<setId>/logo.png` for
set logos), but newer sets — first confirmed on Mega Evolution Series'
`me3` (Perfect Order) and `me4` (Chaos Rising), and already the case for
100% of `me2pt5` (Ascended Heroes) including cards fetched via page 1 —
serve exclusively from `images.scrydex.com/pokemon/<setId>-<n>/large`
(and `<setId>-logo/logo` for set logos) instead, with the old host
returning a 404. Two whole expansions' worth of card files (246 cards)
had to be repaired after generation because a workflow agent
reconstructed the legacy URL pattern instead of reading the fetched
JSON's actual `images.large`/`images.logo` field — verify every
`image` actually resolves (e.g. `curl -o /dev/null -w '%{http_code}'`)
before considering a set's generation complete, don't assume the pattern
that worked for one set works for the next.

## Release dates

**Series- and category-level `_collection.yaml` records also carry a
`date`, rolled up from their earliest mainline expansion** (see
[`collections/CLAUDE.md`](../../CLAUDE.md)'s general grouping-date rule) —
e.g. Original Series' `date` matches Base Set's (`1999-01-09`), and the
whole Pokémon TCG category's `date` matches its earliest series in turn.
Exclude `promos/`/`energies/` sub-lines from this rollup — they only carry
placeholder-year dates themselves (see below), so they'd distort which
expansion is genuinely "first" for the series.

Every numbered expansion's own `_collection.yaml` and every card inside it
carry the expansion's official US/English release date as `date:
"YYYY-MM-DD"` (see [`collections/CLAUDE.md`](../../CLAUDE.md) for the
general `date` field format) — one date per expansion, not per card, since
every card in a numbered expansion ships together on the same day.

**Source: the Pokémon TCG API's `/v2/sets` endpoint (`releaseDate` field),
bulk-fetched and spot-checked — not a per-set Bulbapedia lookup for every
expansion.** A single `GET https://api.pokemontcg.io/v2/sets?pageSize=300`
call returns every set's metadata at once, including `releaseDate` (as
`YYYY/MM/DD`). This is a deliberate exception to this category's usual
"verify every field against Bulbapedia" bar (see the rarity/numbering notes
above) — a release date is one objective fact, not an interpretation-prone
label like rarity, so bulk-trusting the API after spot-checking a sample is
proportionate. Confirmed via 6 independent Bulbapedia infobox checks
spanning the game's full history — Base Set (Jan 9, 1999), Team Rocket
(Apr 24, 2000), Aquapolis (Jan 15, 2003 — not October 2002, a common
misremembering), Celebrations (Oct 8, 2021), Prismatic Evolutions
(Jan 17, 2025), Perfect Order (Mar 27, 2026) — all matched the API's
`releaseDate` exactly. If a newly-added expansion's `releaseDate` looks
off, verify it against Bulbapedia's infobox before trusting it, same as any
other API field in this category.

**Map an expansion directory to its API set id via an existing card's
`image`, not by matching set names.** The id embedded in every
card's image URL is unambiguous — `images.pokemontcg.io/<setId>/<n>_hires.png`
for the legacy CDN, `images.scrydex.com/pokemon/<setId>-<n>/large` for the
newer one (see the image-sourcing note above) — where display names can
diverge from this repo's directory slugs. Look up that id in the bulk
`/v2/sets` response rather than matching on name.

**Sub-checklists folded into a parent expansion's directory (Trainer
Gallery, Shiny Vault, Galarian Gallery, Celebrations' Classic Collection —
see the numbering notes above) carry their own separate API set id, but
ship inside the same physical product as the parent set on the same day.**
Confirmed by comparing `releaseDate` across all 8 known pairs (e.g. `swsh9`
/ `swsh9tg` for Brilliant Stars/Trainer Gallery, `cel25` / `cel25c` for
Celebrations/Classic Collection) — every pair's `releaseDate` matched
exactly. Apply one date to the whole directory; don't try to split by
sub-checklist.

**Celebrations' Classic Collection reprints use Celebrations' own release
date (`2021-10-08`) for every card, not each card's original historical
printing date — unlike `attributes.number`, which deliberately keeps the
ORIGINAL denominator (see the numbering note above).** Don't assume `date`
follows the same "preserve the original" logic just because `number` does
— this was a deliberate call to treat `date` as "when this physical card
was sold," not "what historical card this reprints."

**Promo lines and the Energies subset are excluded from this — they don't
have one release date to begin with.** `<series>/promos/`,
`wizards-black-star-promos/`, and `scarlet-violet-series/energies/` each
release cards individually over months or years rather than as a single
dated product, so they stay at year-only `date` precision until each card
gets its own individually-sourced date — a separate, harder task, not yet
started.

## Identifying items

Cards are identified by their **collector number within a set**, formatted as
`number/total` (e.g. `4/102`). This is the single most reliable disambiguator —
prefer it over name matching, since many cards share a name across sets (multiple
"Charizard" printings exist across dozens of sets) and even within a set via
reprints/alt-art variants.

**e-Card Series `H`-prefixed numbering**: Aquapolis and Skyridge each give
certain Rare cards a separate Holo-foil printing, numbered independently of
the main checklist as `H1`–`H32` with its own fixed denominator — e.g. `H1/H32`,
not `H1/147`. Confirm the exact printed number against Bulbapedia's card
infobox ("English card no.") rather than assuming; don't reuse the set's main
denominator for these. `attributes.number`'s pattern allows an optional
leading `H` on either side of the fraction to accommodate this.

**EX Unseen Forces' lettered Unown secret set**: this expansion's 28 secret
Unown cards are printed on their own sub-checklist, numbered `A`–`Z` then
`!` and `?`, with a fixed `/28` denominator (e.g. `G/28`, `!/28`) — entirely
independent of the main `/115` numbering. The card's actual name is just
"Unown" (verified via both the Pokémon TCG API and Bulbapedia's own article
title, e.g. "Unown (EX Unseen Forces G)") — don't append the letter to the
`name` field, it belongs only in `attributes.number`. A naive fetch of a
per-letter Bulbapedia URL can silently 404 into an empty "no text on this
page" stub rather than erroring — confirm you actually got a populated
infobox (check for the "English card no." field) before trusting a page
fetch, and prefer web-searching for the exact article title over guessing
it. `attributes.number`'s pattern allows a single `A`-`Z`/`!`/`?` character
as the numerator to accommodate this.

identifier. Confirmed cases: the "Shiny" secret sub-line that runs across
*four* Diamond & Pearl/Platinum Series sets without resetting (Stormfront
`SH1`-`SH3`, Platinum `SH4`-`SH6`, Supreme Victors `SH7`-`SH9`, Platinum:
Arceus `SH10`-`SH12`), Rising Rivals' Rotom-themed `RT1`-`RT6`, Platinum:
Arceus' `AR1`-`AR9`, the DP Black Star Promos line (`DP01`-`DP56`), and the
HGSS Black Star Promos line (`HGSS01`-`HGSS25`), all zero-padded as printed.
Verify via Bulbapedia's "English card no." field the same way as any other
numbering quirk — don't assume a denominator exists just because every other
case so far has had one, and don't assume a prefix resets to 1 in a later
set just because the set changed. `attributes.number`'s pattern allows a
bare 1-4-uppercase-letter prefix followed by digits (widened from 1-3 to
fit `HGSS01`-`HGSS25`), with no `/denominator`, to accommodate this.

**The Pokémon TCG API's `rarity` field is wrong for every bare-numbered
special-subset card checked so far.** All of `SH1`-`SH12`, `RT1`-`RT6`, and
`AR1`-`AR9` come back from the API as plain `"Rare"`, but every one
independently checked directly against Bulbapedia's own infobox (not a
search summary — fetch the raw page) is actually `Rare Holo`. This was
caught only after 3 of these cards had already been merged with the wrong
value in an earlier PR and had to be corrected after the fact. Don't trust
the API's `rarity` field for cards with this numbering pattern — verify
each subset directly against Bulbapedia before writing anything, even if
you've already verified a different subset with the same prefix pattern
in a different set.

**Fully spelled-out numbers, no digits at all**: the HeartGold & SoulSilver
Series' "Alph Lithograph" secret card — one per mainline expansion, same
name and illustrator every time, disambiguated only by which expansion
it's in — is printed with its English card number spelled out as a word:
`ONE`, `TWO`, `THREE`, `FOUR` for the four expansions in release order.
Confirmed via Bulbapedia's "English card no." field. `attributes.number`'s
pattern has a dedicated `ONE|TWO|THREE|FOUR` alternative for this rather
than a generic word-matcher, since it's a closed, known set.

**Unown cards on a set's *main* numbered checklist keep the bracket**: outside
the EX Unseen Forces secret sub-checklist above, every other Unown printing
(Neo Discovery/Revelation/Destiny, Diamond & Pearl Series, etc.) is named
`Unown [A]` — brackets included — both in the Pokémon TCG API's `name` field
and as the established convention across dozens of already-curated files.
Bulbapedia's *article title* for these drops the brackets (e.g. "Unown A
(Diamond & Pearl 65)"), but that's MediaWiki's own title-simplification, not
the printed card name — don't let a page title override a name the API
already gives you consistently. When multiple parallel agents touched Unown
cards in the same PR, some incorrectly stripped the brackets based on the
Bulbapedia title alone; keep the brackets.

**Prefixed-fraction subsets (`RC*`, `SV*`, ...)**: unlike every bare-prefix
subset (no fraction at all — see below), some subsets ARE printed with a
fraction, but the *denominator* is also prefixed, not the set's main
total: `RC1/RC25`, not `RC1/113`. Confirmed via Bulbapedia's raw wikitext
(`cardno=RC1/RC25`, `cardno=SV1/SV94`). Known cases so far: Legendary
Treasures' and Generations' separate "Radiant Collection"s (`RC25` and
`RC32` respectively — the denominator isn't fixed, check each set) and
Hidden Fates' "Shiny Vault" (`SV94`, folded into the `hidden-fates/`
directory alongside Hidden Fates' own numbered checklist — Shiny Vault is
not a separate expansion, Bulbapedia treats it as part of Hidden Fates).
`attributes.number`'s pattern allows any 0-2-uppercase-letter prefix on
either side of the fraction rather than an enumerated list of known
prefixes, since a new one has shown up in each of the last few series.
**Zero-pad the numeral in the filename to the collection's own width**,
same as any other numbered set (e.g. `rc01`-`rc25`, not `rc1`-`rc25`) —
Legendary Treasures originally shipped with `rc1`-`rc9` unpadded, which
sorted after `rc25` in a directory listing; fixed alongside the
Generations addition that caught it. **Many more prefixed-fraction
sub-checklists have since turned up, all folded into their parent
expansion's directory the same way, not a separate expansion**: Shining
Fates has its own separate `SV*` "Shiny Vault" (`SV001/SV122` — note the
3-digit zero-padded numerator, unlike Hidden Fates' unpadded `SV1/SV94`;
these are two unrelated Shiny Vaults with different widths, check each
one), Brilliant Stars/Astral Radiance/Lost Origin/Silver Tempest each
have a `TG*` "Trainer Gallery" (`TG01/TG30`, confirmed via Bulbapedia's
own card-list template `ennum=` field rather than conflicting
third-party listings — some showed `TG01/30`, only the primary source
resolved it), and Crown Zenith has a `GG*` "Galarian Gallery"
(`GG01/GG70`).

**Celebrations' "Classic Collection" is numbered like nothing else in
this category — each card's `attributes.number` reflects its ORIGINAL
historical printing, not anything specific to Celebrations.** These 25
cards are reprints of iconic cards spanning the entire history of the
TCG (Base Set's Charizard, Neo Revelation's Shining Magikarp, EX-era
Gold Star Umbreon, Sword & Shield's own Tapu Lele-GX, etc.), and the
Pokémon Company deliberately kept each card's original collector number
and denominator as a homage — so `Charizard`'s number here is `4/102`
(Base Set's own numbering), not `4/25` or `4/CC25`. Do not invent a
Celebrations-specific denominator. The full 25-card table (number,
original source expansion, name) is authoritative from Bulbapedia's own
`Celebrations (TCG)` setlist page, not the API (which also mislabels the
rarity — see above) — re-derive it from that page's raw wikitext rather
than the API's bare numbers if this needs redoing. Multiple cards
legitimately share the same numerator (four different cards are all
`15/<something>`, one per original expansion) since they're independent
historical references — filenames stay unique via the name slug, same
as any other reprint, but ALSO need a way to avoid colliding with the
main Celebrations set's own `1-25` numbering in the same directory (e.g.
a `cc-` filename prefix, since — unlike RC/TG/GG/SV — this subset's
`attributes.number` itself carries no distinguishing prefix to reuse).

**BW Black Star Promos has a genuine printed inconsistency — don't
normalize it.** Cards are numbered `BW01`-`BW101` (2 digits), except
Reshiram and Zekrom, which are printed `BW004`/`BW005` (3 digits) — this
is confirmed as the actual printed number by multiple independent
commercial listings, not an API typo. Use each card's number exactly as
the API gives it; don't zero-pad the whole line to a uniform width.

**Kalos Starter Set has no rarity symbol on any card — omit the field,
don't guess.** All 39 cards return `rarity: null` from the API, and
Bulbapedia's raw wikitext confirms it: no `rarity=` parameter at all in
the template call (unlike a genuinely-uncredited-illustrator case, where
the card still has other rarity data). This is a real starter/beginner
product without rarity tiers, not a data gap. Same treatment as omitting
`illustrator` when uncredited: leave `attributes.rarity` out of the file
entirely rather than inventing a value.

**"Yellow A Alternate cards" are a separate, later collection — exclude
them from the mainline expansion they appear to belong to.** Starting
around Flashfire, several XY-era sets contain extra cards with a letter
suffix on their number (e.g. `88a`, `98a`/`98b`). These look like
alternate-art secret rares of the base numbered card, but Bulbapedia's
raw wikitext shows their `expansion=` parameter is literally `Yellow A
Alternate cards`, not the set they're numbered alongside (confirmed on 2
cards from 2 different sets) — a distinct reprint line, first released
during the *Sun & Moon* era via the Mega Powers Collection, that reuses
XY-era card numbers with a letter appended and a yellow "A" symbol to
keep them format-legal only alongside their original printing. **Do not
generate files for these letter-suffixed cards as part of a mainline XY
expansion** — they're out of scope until "Yellow A Alternate cards" gets
curated as its own collection. This also explains an API metadata
inconsistency: most sets' `total` field already excludes these cards, but
not consistently (Ancient Origins' `total: 100` excludes its one `75a`
card, while other sets' `total` appears to include theirs) — don't trust
the set-level `total` field for your generation target; count printed +
genuine secret rares (digits only, no letter suffix) yourself instead.

## Verifying a set is complete

A set's total card count is public and fixed (encoded in every card's
`attributes.number` field, e.g. `.../102`). To check completeness:
1. Read any card's `attributes.number` field to get the set total.
2. Confirm that many distinct numbers 1..N exist as entity files in the set
   directory.
3. Cross-reference the full checklist against an authoritative source (Bulbapedia,
   Pokémon TCG API, or Serebii) rather than assuming — some sets have secret rares
   numbered above the printed total (e.g. `103/102`).

**The API sometimes invents a sequential number for a card that isn't
printed with one at all — don't trust `attributes.number` blindly for
trailing basic Energy cards.** Sun & Moon's API data includes 9 basic
Energy cards (one of each type, including Fairy) at what look like
numbers 164-172, beyond its documented 163-card checklist. Bulbapedia's
own compiled printing history for these explicitly calls this a Sun &
Moon-era Basic Energy print "**unnumbered**" — the physical card carries
no collector number at all, and the API's sequential numbering is its own
invention for database bookkeeping, not something to reproduce. Excluded
these 9 from `sun-moon/` for exactly that reason (a card's number is this
category's primary identifier — don't fabricate one). This appears to be
a one-off tied to this specific print event, not a recurring pattern —
every other Sun & Moon-era set's genuine numeric-card count matched its
independently-documented community checklist exactly with no similar
excess, so don't assume it recurs without checking.

## Naming files

`<number>-<slugified-name>.yaml`, number zero-padded to the set's total digit
width, e.g. `004-charizard.yaml` for card `4/102` in a 102-card set. Reprints
of the same name within a set get disambiguated by number, which is already
unique.

## Rarity

`attributes.rarity` is enum-validated in `item-attributes.schema.json`. The enum
starts small (`Common`, `Uncommon`, `Rare`, `Rare Holo`, `Rare Holo ex`) and is
expected to grow — it is not meant to gate curation. If a card's real rarity
tier isn't in the enum yet, add it as part of the same PR: confirm the exact
label against an authoritative source (Bulbapedia, Pokémon TCG API, or
Serebii), then add that label to the `enum` array in `item-attributes.schema.json`
alongside the card file(s) that need it. Don't invent a label, and don't
reuse a near-miss enum value to dodge a schema edit (e.g. filing a `Rare Holo
GX` card as `Rare Holo ex`).

**`Rare Holo ex` is lowercase, and — despite an earlier note here predicting
otherwise — it's the SAME enum value for both the 2003-2007 `Pokémon-ex`
mechanic and the 2011+ `Pokémon-EX` mechanic.** The card's `name` field
still shows the real difference (space-separated lowercase `Chansey ex` vs.
hyphenated capitalized `Shaymin-EX`), and Bulbapedia's own card template
has a separate `class=EX` field to track the mechanic distinction — but the
`rarity` template parameter itself is `Rare Holo ex` (lowercase) for both,
confirmed via raw wikitext (`action=raw`, not rendered HTML/icon alt text,
which can be ambiguous when a page lists multiple printings) on 4
independent BW-era cards across 2 sets. The Pokémon TCG API instead returns
`"Rare Holo EX"` (capitalized) for these BW-era cards — don't trust that;
map it to the existing `Rare Holo ex` value, not a new one. Full-art
BW-era `-EX` reprints are a genuinely different, separate rarity: see
`Rare Ultra` below.

**Word order and case both matter, and existing precedent isn't automatically
correct.** Two rarity values in this enum were wrong before being
re-verified against Bulbapedia: `Holo Rare` (should be `Rare Holo` — reversed
word order) and `Rare Holo EX` (should be `Rare Holo ex` — wrong case). Both
went unnoticed through several PRs because "it's already in the enum" was
read as settled instead of re-verified — and a third value, `Rare Holo ☆`,
that looked equally suspect on the same pass turned out to already be
correct (confirmed independently on two cards from different sets). The
lesson isn't "assume existing values are wrong" — it's that *neither*
assumption (precedent is right / precedent is suspect) substitutes for
actually checking. If you're about to reuse an enum value instead of
confirming it fresh, verify it against Bulbapedia anyway.

**The API routinely drops the `Rare Holo` prefix from compound rarities.**
Confirmed so far: the API's `"Rare Prime"` should be `Rare Holo Prime`
(HeartGold & SoulSilver Series' Pokémon Prime mechanic), and its bare
`"LEGEND"` should be `Rare Holo LEGEND` (the same series' two-card LEGEND
Pokémon) — both verified independently on two cards each. This is the same
failure mode as `Rare Holo EX`/`Rare Holo ex`, just via omission instead of
casing: when the API gives a short/bare rarity string, check whether
Bulbapedia's actual infobox has a longer `Rare Holo <modifier>` form before
trusting the short one.

**`Rare Ultra`** (Black & White Series onward): the full-art secret-style
reprint of an already-numbered `-EX` Pokémon within the same set (e.g.
Entei-EX prints at both `13/108` as `Rare Holo ex` and again later in the
same set's numbering as `Rare Ultra`) — not a beyond-total secret rare,
still within the printed range. Matches the API's own casing; confirmed
via raw wikitext on 2 cards across 2 sets.

**`Rare Ace`** (Boundaries Crossed onward): "ACE SPEC" Trainer/Item cards
(max 1 per deck). Title case, NOT the API's all-caps `"Rare ACE"` —
confirmed via raw wikitext on 2 cards across 2 sets.

**`Rare BREAK`** (BREAKthrough onward): "BREAK Evolution" Pokémon (named
`<Pokémon> BREAK` in-game). Matches the API's casing exactly — confirmed
via raw wikitext on 2 cards across 2 sets, no correction needed.

**A single card's raw wikitext can itself be stale — cross-check against
the Rarity overview page's prose when they disagree.** Individual
Pokémon-GX cards' `{{rar|}}` template parameter often literally reads
`Ultra-Rare Rare` (confirmed on 2 different cards' base Sun & Moon-era
printings), which looks like a genuine value but isn't the intended one:
the Rarity overview page's own maintained prose states outright "Their
rarity is rare Holo GX." Individual card infoboxes aren't always kept in
sync with what a rarity is *supposed* to be called; when a raw-wikitext
value looks inconsistent with how the same rarity reads elsewhere (e.g.
via the API, or via other cards of the same mechanic), check the Rarity
overview page's dedicated prose for that mechanic before trusting a
single card's template value. Two independent raw-wikitext checks
verifies a value is *used*, not that it's *correct* — Bulbapedia is
maintained by editors, not machine-consistent.

**`Rare Holo GX`** (Sun & Moon onward): Pokémon-GX cards, including "Tag
Team" GX from Team Up onward. Matches the API's casing — confirmed via
the Rarity overview page's prose (see above), not just individual card
infoboxes, which are unreliable for this one specifically.

**`Rare Rainbow`** (Sun & Moon onward): secret "Rainbow Rare" full-art
reprints, mostly of Pokémon-GX. Matches the API exactly — confirmed via
raw wikitext.

**`Rare Prism Star`** (Ultra Prism onward): "Prism Star" (◇) cards, max 1
per deck. Matches the API and the Rarity overview page's prose exactly.

**`Rare Shining`** (Shining Legends only): a 2017 one-set revival of the
"Shining Pokémon" concept, but a GENUINELY DIFFERENT rarity from the
1999-2002 Neo Series' `Shining Holofoil` — don't conflate them just
because both eras name the cards "Shining <Pokémon>". Confirmed via raw
wikitext on 2 cards.

**`Rare Shiny` / `Rare Shiny GX`** (Hidden Fates' Shiny Vault only):
non-GX and GX secret reprints in the `SV1/SV94` sub-checklist. Matches
the API exactly — confirmed via raw wikitext on multiple cards. Also
genuinely different from both `Shining Holofoil` and `Rare Shining` —
three visually/conceptually similar but textually distinct "shiny
Pokémon" rarities now exist in this enum across three different eras;
don't collapse them into one just because they sound alike.

**`Rare Holo V` / `Rare Holo VMAX` / `Rare Holo VSTAR`** (Sword & Shield
onward): Pokémon V, VMAX, and VSTAR mechanics. All three match the API's
casing exactly — confirmed via the Rarity overview page's own prose
("Their rarity is holo rare V/VMAX/VSTAR"), not just individual card
infoboxes (see the GX lesson above about why that matters).

**`Amazing Rare`** (Vivid Voltage onward) and **`Radiant Rare`** (Astral
Radiance onward): "Amazing Pokémon" and "Radiant Pokémon" mechanics.
Both match the API's casing exactly — confirmed via the Rarity overview
page's prose.

**`Trainer Gallery Rare Holo`**: cards in a "Trainer Gallery" (Brilliant
Stars onward) or "Galarian Gallery" (Crown Zenith) sub-checklist — both
use this SAME rarity value, there's no separate "Galarian Gallery" rarity
despite the different subset name. Matches the API exactly — confirmed
via the existence of Bulbapedia's own `Category:Trainer Gallery Rare Holo
cards` page (a curated category is as authoritative as prose for
confirming a value is real, when the Rarity overview page itself doesn't
cover a mechanic in prose).

**`Rare Classic`** (Celebrations' Classic Collection only): the API calls
this rarity `"Classic Collection"`, but Bulbapedia's own `Celebrations
(TCG)` expansion page — which maintains the authoritative card-by-card
setlist table for this specific subset — explicitly lists every one of
its 25 cards as `Rare Classic`. Trust the expansion's own setlist page
over the API string here. See the numbering note below — this subset's
`attributes.number` values are unlike anything else in this category.

**Scarlet & Violet Series (2023 onward) replaced the whole rarity-tier
vocabulary — none of the SWSH-era `Rare Holo <mechanic>` values apply,
even to physically holographic cards.** Nine new enum values, all
confirmed via Bulbapedia's Rarity overview page prose:
`Double Rare` (two stars, Pokémon ex — note this is a visually distinct
white-art mechanic from both the 2003-2007 `ex` and 2011+ `EX` eras
sharing the `Rare Holo ex` value, but SV's `ex` gets its own new rarity
name, not reused), `Ultra Rare` (two silver stars, full-art ex/Supporter
— textually distinct from the older `Rare Ultra`, don't conflate them),
`Illustration Rare` (one gold star, full-art non-ex), `Special
Illustration Rare` (two gold stars), `Hyper Rare` (three gold stars,
gold-bordered secret rares), `ACE SPEC Rare` (pink star, 1-per-deck —
textually distinct from the older title-case `Rare Ace`), `Shiny Rare`
and `Shiny Ultra Rare` (Paldean Fates' Shiny Vault subset only, hollow
gold star / two hollow gold stars), and `Black White Rare` (monochrome
foil, verified via web search rather than the Rarity page itself since
it's new enough not to be documented there yet — at least 4 cards exist
across the whole series so far: Zekrom ex in Black Bolt, Reshiram ex in
White Flare, and a Victini secret promo in each set (#171 in Black Bolt,
#172 in White Flare) — don't assume this count is exhaustive, it's grown
before).

**SV era needs no sub-checklist folding at all — a real simplification
vs. SWSH.** Every mainline set's card numbers are plain `<n>/<printed
total>`, contiguous, with zero letter prefixes anywhere — confirmed by
checking every set's live number strings are 100% numeric. Even the two
sets whose SWSH-era analogues had special sub-checklist prefixes
(`151`, echoing Champion's Path; `Paldean Fates`, echoing Shining Fates)
just use plain numbering with secret rares past the printed total —
Paldean Fates' Shiny Vault-equivalent tail (cards past #91, rarity
`Shiny Rare`/`Shiny Ultra Rare`) is NOT given an `SV`-style prefix this
time, don't assume the SWSH pattern recurs without checking.

**`Scarlet & Violet Energies` (API id `sve`) is a genuine cross-product
support line, not part of any single expansion.** Bare numbers `001`
through `024` with NO denominator at all (unlike every mainline SV set),
released in three batches alongside three different expansions. Gets
its own top-level directory, `scarlet-violet-series/energies/`, a
sibling of `promos/` — not folded into `scarlet-violet/`.

**`SVP` (SV Black Star Promos) has the same live-API completeness gap
as the SWSH promo line — verify against the API's OWN set metadata,
don't trust it blindly either.** The `/v2/sets` endpoint's `printedTotal`
figure for `svp` is stale, but the live `/v2/cards` query is also
missing several real numbers relative to Bulbapedia's own SVP category
page. Same policy as the SWSH gap: catalogue what the API actually
returns, document the specific missing numbers as a future task, don't
fabricate entries from secondary sources.

**Prismatic Evolutions (`sv8pt5`), Shrouded Fable (`sv6pt5`), Stellar
Crown (`sv7`), Surging Sparks (`sv8`), and `sve` (Scarlet & Violet
Energies) all have null `artist` on every card in the live Pokémon TCG
API — but that's a gap in that one API, not a real data gap. Don't stop
at the API and default to omitting the field.** Fan card databases carry
these credits independently of `api.pokemontcg.io`: pkmncards.com's
per-card pages (`https://pkmncards.com/card/<slug>/`) print an
`illus. <a href=".../artist/...">NAME</a>` block sourced from the
physical card, and spot-checks against Limitless
(`limitlesstcg.com/cards/<code>/<n>`) agreed on every card checked.
Bulk-sourced illustrator this way for all five sets/subsets — every
`/set/<slug>/` listing page links every card in the set, so the whole
checklist is fetchable without per-card guessing. 100% coverage on four
of them; Surging Sparks has one genuine remaining gap (see below).

**pkmncards.com sometimes prints the literal string `n/a` in the
illustrator slot instead of omitting the block — treat that as "not
credited," never write it into `attributes.illustrator` as if it were a
real name.** Hit this on a handful of Trainer/Energy cards across the sets
above (confirmed: 2 cards in Shrouded Fable, 2 in Surging Sparks, all of
`sve`'s live listing) plus 3 cards in Perfect Order (see below) — omit
`illustrator` for these, same as any other genuinely uncredited card.

**When a card comes up genuinely uncredited on every web source checked,
read the card's own image before giving up.** Surging Sparks' `246/252`
("Lisia's Appeal") had no illustrator on pokemontcg.io *or* pkmncards.com
— but every physically-printed non-Energy card carries its own credit as
small `Illus. <name>` text near the bottom border, above the copyright
line, independent of any third-party database. Fetching the card's own
`image` URL and reading that line directly gave `Illus.
Nobusawa/Mochipuyo` — a two-artist collaborative credit, matching the
`/`-joined format already used elsewhere in this category (e.g. `Ken
Sugimori/Yusuke Ohmura`). This is a fallback for the rare single-card
gap that survives multiple bulk sources, not a routine step — Energy
cards in particular often don't print an individual credit line at all,
so don't expect it to close the Energy-card gaps documented above.

Surging Sparks also has 7 cards whose illustrator was already
hand-sourced before pkmncards was used as a bulk source — the parallel
"ex" prints of Milotic ex (Double Rare, Ultra Rare, Special Illustration
Rare) and Pikachu ex (those three plus Hyper Rare). pkmncards
independently agrees with all 7 existing credits.

**Mega Evolution Series (2025 onward) mostly continues the Scarlet &
Violet star-tier system — `Common` through `Special Illustration Rare`
carry over unchanged — but adds two genuinely new top-tier values for
the returning Mega Evolution / "M Pokémon ex" mechanic**, confirmed via
Bulbapedia's Rarity page: `Mega Hyper Rare` (gold-star-with-black-border,
effectively replaces plain `Hyper Rare` for this era — none of this
series' live data contains a bare `"Hyper Rare"` string at all, don't
reuse the SV-era value) and `Mega Attack Rare` (pastel star, the
standard-art secret-rare print of a Mega Pokémon ex). **The API returns
`Mega Attack Rare` as the raw string `"MEGA_ATTACK_RARE"`
(SCREAMING_SNAKE_CASE) — the only rarity in this whole category that
doesn't come back human-readable — map it explicitly, don't pass it
through.**

**Ascended Heroes (`me2pt5`) has a genuine bulk-list pagination bug in
the live API, not a real data gap — don't just trust `totalCount`.**
`/v2/cards?q=set.id:me2pt5&pageSize=250&page=2` returns 45 cards that
are exact duplicates of page 1's records instead of the true tail, so a
naive paginate-and-merge silently caps out at 250 unique cards even
though the set's own metadata says `total: 295`. Confirmed real,
distinct cards exist through `me2pt5-295` by fetching individual card
IDs (`/v2/cards/me2pt5-<n>`) — `me2pt5-296` returns nothing, so 295 is
the true ceiling. When a page-2 fetch returns cards you already have
(check by ID, not just count), fall back to per-ID fetching for the
missing range rather than accepting a truncated merge.

**`me1` (Mega Evolution) and `me3` (Perfect Order) have null `artist` on
every single card in the live API — the same API-only gap as the Scarlet
& Violet Series sets above, not a real data gap.** Sourced from
pkmncards.com the same way: 188/188 for Mega Evolution, 121/124 for
Perfect Order. Perfect Order's three exceptions — `86/88`, `87/88`,
`88/88` (its Grass/Fighting/Psychic-type Basic Energy reprints) — come
back `n/a` on pkmncards too and are genuinely uncredited; leave
`illustrator` omitted for just those three.

**The Mega Evolution-era promo line (`mega-evolution-series/promos/`,
"MEP Black Star Promos") is catalogued, sourced from Bulbapedia's own
checklist page rather than the API** (`MEP_Black_Star_Promos_(TCG)`,
plus individual card pages) since the Pokémon TCG API has no `mep`-style
set id. Numbered `001`-`110` with no printed denominator (three-digit
zero-padded, e.g. `mep030-mega-charizard-y-ex.yaml`), plus one unnumbered
jumbo promo ("Pikachu at the Museum", filed without a number prefix or
`attributes.number` at all). An ongoing, still-active line, not a closed
checklist — like other promo lines in this category, cards stay at
year-only `date` precision until each gets its own individually-sourced
date.

## Pokémon type

`attributes.type` (the Pokémon's energy type — `Fire`, `Water`, etc.) only
applies to Pokémon-supertype cards; Trainer, Supporter, Item, Stadium, and
Energy cards never get one, and that's correct, not a gap. Source it from
the same live Pokémon TCG API already used for `number`/`rarity`/`date` —
its `types` field maps directly onto this schema's 11-value enum with no
translation needed (unlike `rarity`'s messy era-specific casing/wording
history), and it's a `supertype: "Pokémon"` check away from correctly
skipping every non-Pokémon card.

**Backfilled catalog-wide: 17,004 of 20,121 cards carry it — every
Pokémon-supertype card in the catalog.** The remaining 3,117 are all
genuinely non-Pokémon (Trainers, Energies). Sourced via a bulk
per-directory fetch (`/v2/cards?q=set.id:<id>&pageSize=250`, paginated
past 250), not a per-card lookup — cheaper than the illustrator backfill
by roughly two orders of magnitude in request count. Zero cards found
with more than one value in `types`, despite the schema modeling it as an
array. The two subsets the bulk API method couldn't reach (Mega
Evolution-era promos, Celebrations' Classic Collection — 111 + 25 cards)
were closed out separately by reading each card's own `image` directly —
see below.

**Format**: a block sequence, indented 2 spaces deeper than the `type:`
key itself (matching this repo's convention for any other array-valued
attribute, e.g. `attributes.zordComponents` elsewhere in the catalog) —
`yaml.safe_dump` does NOT produce this indentation by default, it aligns
list items with their parent key, so don't trust a naive dump without
checking the output:

```yaml
attributes:
  number: "4/102"
  rarity: Rare Holo
  illustrator: Mitsuhiro Arita
  type:
    - Fire
```

**Historical "Dragon" Pokémon are typed by their base element, not
`Dragon`, and the API is right about it — confirmed against the physical
card, not just trusted blindly.** Dragon wasn't an energy type with its
own icon until Scarlet & Violet Series' Dragon Vault-style usage; Neo
Revelation-era "Dragon" Pokémon (e.g. Kingdra, `19/64`) print a single
ordinary type icon on the physical card (Kingdra's is Water), matching the
API's `types: ["Water"]` exactly — verified by fetching the card's own
`image` and inspecting the printed icon directly, not assumed. Don't
second-guess the API on this without similarly checking a physical card
first.

**A set's own directory can fold in a sub-checklist that lives under a
SEPARATE API set id — fetching only the main checklist's id silently
misses it entirely, with no error to signal the gap.** Trainer Gallery
(Brilliant Stars `swsh9tg`, Astral Radiance `swsh10tg`, Lost Origin
`swsh11tg`, Silver Tempest `swsh12tg`), Galarian Gallery (Crown Zenith
`swsh12pt5gg`), and the Shiny Vault subsets (Shining Fates `swsh45sv`,
Hidden Fates `sma` — this one doesn't even follow the `<parent>sv` naming
pattern the others do, don't guess it) each need their own `set.id:`
query merged into the same directory's card pool before matching by
number. Discover an unmapped sub-checklist's id the same way this file
already documents for mapping a directory to its main set id: from one of
its own card's `image` URL.

**The live API can return two different cards with the same `number`
value within one set — a genuine upstream data bug, not a sourcing
mistake on this repo's part.** Confirmed on Black Bolt (`zsv10pt5`):
`zsv10pt5-80` ("Antique Cover Fossil", a Trainer card, correctly filed
here as `80/86`) comes back from the API with `number: "60"` instead of
`"80"`, colliding with the real `zsv10pt5-60` ("Escavalier", a Pokémon).
A naive last-write-wins number→card lookup can silently drop the real
Pokémon's data (if the non-Pokémon entry overwrites it) with no error
raised. When two API cards collide on the same number: if exactly one is
`supertype: "Pokémon"`, keep that one — the other one(s) didn't need
`type` written anyway, so nothing is lost. If two or more colliding
entries are BOTH Pokémon, there is no safe automatic resolution — exclude
that number from the lookup and leave it for manual sourcing rather than
guessing which one owns the data. (This backfill hit exactly one such
collision across the entire catalog, resolved via the single-Pokémon
rule; zero cases needed manual exclusion.)

**Celebrations' Classic Collection (`cc-*.yaml` files) must be
hard-excluded from any number-based lookup — this isn't a numbering
format quirk like the ones above, it's numbers borrowed wholesale from
OTHER, unrelated expansions** (see the Numbering section's note on this
subset). `cc-04-charizard.yaml`'s `4/102` is Base Set's own numbering,
reused as homage — not card 4 of Celebrations' own 25-card checklist. A
first attempt at this backfill matched these files by numerator against
Celebrations' own API data (`cel25`) anyway and wrote real, wrong data:
Charizard came back typed `Water`, Blastoise came back `Fire`, and four
unrelated cards (Claydol, a Trainer card, Rocket's Zapdos, Venusaur — all
coincidentally sitting at position `15` in their own original sets) all
received the identical `Psychic` value from one bad match. Caught by a
numerator-collision audit run across the *entire* catalog after the fact
(the only collisions found anywhere were these 25 files), reverted to a
byte-identical pre-touch state. **Resolved properly afterward by reading
each of the 22 Pokémon cards' own `image` directly, one at a time** — no
bulk shortcut exists for this subset since each card's number doesn't
belong to any one fetchable set. Caught a real trap doing it this way:
`cc-93-gardevoir-ex` ("Gardevoir ex δ", a Delta Species card) is typed
`Fire` on the actual printed card, not `Psychic` as Gardevoir's normal
game typing would suggest — Delta Species cards deliberately carry
off-type energy as their whole gimmick, so don't infer a Classic
Collection card's type from the Pokémon's usual typing, always read the
specific printing.

**The Mega Evolution-era promo line (`mega-evolution-series/promos/`) has
no `api.pokemontcg.io` set id at all**, same reason its other fields are
Bulbapedia-sourced (see the Numbering section). Of its 111 cards, 78 were
covered by pkmncards.com (which indexes this line under
`mega-evolution-promos` despite the missing official API id — same
`class="color" title="Color"` markup pattern used for illustrator
credits, just a different field). The remaining 32 (plus the one
unnumbered jumbo promo) were resolved by reading each card's own `image`
directly.

## Variants

A card's distinct physical print treatments (1st Edition, Shadowless,
Unlimited, Reverse Holo) are recorded as top-level `variants` sub-entities
(see `/schemas/item.schema.json`), not as an `attributes` field — each
treatment is its own physically distinct printing of the card, which is
exactly what the `variants` primitive models. Give each one just `id` and
`name`; every other field (`number`, `rarity`, `illustrator`, `image`, …) is
inherited from the parent card and shouldn't be repeated. This is a different
concept from `attributes.rarity`, which describes the card's slot/mechanic,
not its print run.

```yaml
variants:
  - id: <generated-uuid>
    name: 1st Edition
  - id: <generated-uuid>
    name: Shadowless
  - id: <generated-uuid>
    name: Unlimited
```

There's no schema enum enforcing the label set (a `variants[].name` is a free
string, unlike `attributes.rarity`) — treat the four names below as the
convention regardless, and confirm against a source before introducing a new
one rather than inventing one.

**The four names split into two families with genuinely different sourcing
rules — don't use one family's method for the other.**

- **`Reverse Holo`**: reliably sourceable from the Pokémon TCG API's
  `tcgplayer.prices` object. A card whose response includes a
  `reverseHolofoil` key (alongside `normal`/`holofoil`) has a confirmed
  reverse holo print — TCGplayer bulk-prices reverse holos even for
  otherwise-worthless commons, so the key's presence is a trustworthy
  per-card signal, not just a chase-card one. Introduced with Legendary
  Collection (May 24, 2002) — the first set to give every card in its
  checklist a parallel reverse-holo print (see that set's own
  `_collection.yaml`) — and standard for effectively every set since,
  though not every card in every later set gets one (some full-art/secret
  rares don't) — check each card's own `tcgplayer.prices` keys, don't
  assume a blanket rule holds past Legendary Collection.

  **Legendary Collection itself has a small confirmed gap in this signal —
  don't let it override the set's own documented rule.** Its live API data
  is missing the `reverseHolofoil` price key for exactly 2 of 110 cards
  (`88/110` Psyduck, `93/110` Slowpoke), even though third-party listings
  (GoCollect, PriceCharting, PSA pop reports) confirm reverse holo prints
  of both exist — a TCGplayer pricing gap for these two specific commons,
  not a real printing absence. Since Legendary Collection's own rule is
  "every card in the checklist gets a reverse holo parallel, no
  exceptions" (see its `_collection.yaml` description), this set is filed
  as `Reverse Holo` on all 110 cards uniformly rather than per-card API
  lookup — unlike later sets, where the per-card check is the rule, not
  the exception.
- **`1st Edition` / `Shadowless` / `Unlimited`**: WOTC-era (1999–2003)
  print-run distinction. **Do NOT use the API's `tcgplayer.prices` keys for
  these** — unlike `reverseHolofoil`, TCGplayer doesn't separately
  price-track `1stEditionNormal`/`1stEditionHolofoil` for most low-value
  vintage commons even though the physical variant exists, so absence of
  the key means "not priced," not "doesn't exist." Source this trio from
  set-level collecting history (Bulbapedia's set article, or a dedicated
  vintage-collecting reference) instead, and expect it to apply uniformly
  across a whole set's checklist rather than needing a per-card lookup.

**Base Set's Machamp (`008-machamp.yaml`, `8/102`) is the one confirmed
exception to "every Base Set card got all three treatments."** It was
commercially printed ONLY as 1st Edition (holofoil) in the regular booster
set — no Shadowless or Unlimited print exists outside of it. The sole
non-1st-edition Machamp is a non-holo print exclusive to the separate
"Trainer Deck A" 2-Player Starter Set product (red-bordered, pre-release
League exclusive) — a different product entirely, not part of this
checklist — confirmed via Bulbapedia. `variants` for this one card is a
single `1st Edition` entry only; every other Base Set card gets all three
(`1st Edition`, `Shadowless`, `Unlimited`).

## Third-party data sources can disagree — verify glyphs, not just facts

The Pokémon TCG API (`api.pokemontcg.io`) is a convenient bulk source for
card lists (name, number, rarity, illustrator, image), but it isn't
authoritative for exact typography. Confirmed case: the "Gold Star" Pokémon
of the EX Series (e.g. `Mudkip ★`) come back from the API with `★` (U+2605
BLACK STAR), but the actual printed card and Bulbapedia's own article title
use `☆` (U+2606 WHITE STAR) — `Mudkip ☆`. Use the API for bulk data, but
when a name contains a symbol (stars, gender signs, Greek letters), confirm
the exact codepoint against Bulbapedia's page title or infobox before
writing the entity file — don't assume the API's rendering is correct.

## Common pitfalls

- Don't confuse a set's *TCG expansion name* with its *physical product name*
  (booster box vs. theme deck exclusives) — the set directory should represent the
  expansion, not a retail SKU.
- Don't confuse *series* with *expansion* — a series (e.g. "Base Series") is
  never a directory that directly contains cards; only an expansion is.
- Promo cards are not part of any numbered set — they belong in a `promos`
  collection, not shoehorned into the nearest numbered set. **Whether that
  `promos` collection is scoped to a series depends on whether the promo
  line itself was scoped that way at the time.** From the Nintendo era
  onward, promo lines are explicitly tied to one series — often via a
  number prefix (e.g. "Mega Evolution Promos" uses `MEP`, distinct from
  every other series' promo prefix) — and that promo line lives at
  `<series>/promos/`, a sibling of that series' expansions. But the
  earliest promo line, the **Wizards Black Star Promos** (1999–2003, #1–53),
  predates that convention entirely: Wizards never reset or re-scoped the
  numbering by series, so cards from the Original Series, Neo Series, and
  e-Card Series eras are interleaved in one continuous run. Don't split it
  across series directories to force-fit the later convention — file it as
  its own top-level collection, `pokemon-tcg/wizards-black-star-promos/`,
  a sibling of `original-series/` rather than nested inside it. Whichever
  form a `promos` collection takes, treat it like any other expansion-level
  directory: it needs its own `_collection.yaml` and contains card files
  directly (promo numbering is promo-specific, not tied to any expansion).
- **The Pokémon TCG API's own `/v2/cards` endpoint can silently omit real,
  documented cards even while its own set object admits the gap.** The
  SWSH Black Star Promos (`swshp/promos/`) run `SWSH001`-`SWSH307`, but the
  live `/v2/cards?q=set.id:swshp` query returns only 304 records — missing
  `SWSH299` (Jirachi V), `SWSH300` (Unown V), and `SWSH301` (Lugia V)
  entirely. The set's own metadata (`printedTotal: 307` vs. `total: 304`)
  flags the discrepancy, and Bulbapedia's raw-wikitext checklist plus
  independent retail listings confirm all three are real printed cards
  (tied to the Jirachi V Box and the Crown Zenith Special Collection—Unown
  V & Lugia V, both January 2023). Don't fabricate entries for a gap like
  this without the same sourcing rigor (image URL, illustrator, exact
  name) used for every other card — left unfiled as a documented future
  task rather than guessed at. **This recurs, not a one-off**: the SV
  Black Star Promos (`svp/promos/`) has the same pattern — runs
  `SVP001`-`SVP207` but the live API returns only 200 records, missing
  `SVP175`, `SVP176`, `SVP190`-`SVP192`, and `SVP204`-`SVP205`. Same
  policy: catalogue what's live, document the gap, don't fabricate.
