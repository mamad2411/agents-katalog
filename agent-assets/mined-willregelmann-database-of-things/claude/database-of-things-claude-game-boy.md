# Game Boy — curation hints

**Status: all 499 North American-released licensed Game Boy titles are
catalogued**, per Wikipedia's "List of Game Boy games" NA column (see
Sourcing below). Japan- and PAL-exclusive titles, unlicensed releases, and
Game Boy Color games are out of scope for this directory — see Scope.

## Scope

Original Game Boy (DMG) releases only. **Game Boy Color is a separate
platform**, not a variant of this one — it has its own hardware, its own
product code prefix, and its own cartridge shape, distinct from DMG carts
even for a title playable on both. See
[`../game-boy-color/CLAUDE.md`](../game-boy-color/CLAUDE.md) — don't fold
GBC-format cartridges in here, including "Dual Mode" ones that also run on
original Game Boy hardware; that backward-compatibility is a cartridge
attribute over there, not a reason to split it between the two platform
directories.

## Directory structure

```
game-boy/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "Game Boy" platform
  <slugified-name>.yaml
```

Flat, no sub-grouping — Game Boy games don't have an equivalent to a card
set or a numbered catalog line; each release is independent.

## Identifying items

Nintendo cartridges/boxes carry an official product code (format
`DMG-<code>-<region>`, e.g. `DMG-AREE` for a US release) — verify the exact
code per game against the actual box/cartridge or a reliable database (not
memory) before treating it as a schema field; it may be worth adding a
`catalog_number` attribute once the first real batch confirms the format
holds consistently. Region matters: the same game can have different codes
and sometimes different content across US/EU/JP releases — don't assume
one region's data applies to another without checking.

## Naming files

`<slugified-name>.yaml` — no canonical numbering exists across the
platform's library, so no zero-padded number prefix (per the root
`CLAUDE.md`'s naming rule for collections without canonical numbering).
Disambiguate same-named re-releases/reprints by adding a region or edition
qualifier to the slug if needed once that situation actually arises.

## Sourcing (North American releases)

**Two-source method, adopted after the PR #193 rejection below** — a single
source wasn't enough to avoid the region/publisher and shared-title traps
reliably:

1. **Primary: Wikipedia's ["List of Game Boy games"](https://en.wikipedia.org/wiki/List_of_Game_Boy_games)**
   article — one sortable table, ~1,043 games, with **separate date columns
   per region** (Japan/North America/PAL) and the publisher shown per-region
   in the same row (`Interplay <sup>NA/EU</sup><br/>Imagineer <sup>JP</sup>`,
   "Unreleased" marked explicitly where a region never got it). Filter to
   rows where the NA column isn't "Unreleased". Fetch via
   `en.wikipedia.org/w/api.php?action=parse&page=List_of_Game_Boy_games&prop=wikitext`
   and parse the wikitext table directly — reading date and publisher
   *together* out of the same row is what structurally prevents the
   region-pairing error, rather than cross-matching two separately-sourced
   fields by hand.
2. **Secondary/cross-check: the Nintendo Fandom wiki**
   (`nintendo.fandom.com`), same MediaWiki-API access pattern used for
   Gunpla Wiki elsewhere in this repo (raw `api.php`, browser User-Agent, no
   login needed — rendered pages 402 but the API doesn't). Gives an
   independent developer/publisher/date check plus box art (no equivalent on
   Wikipedia's table). Verified against **date/dev/pub
   conflict-resolution policy**: Wikipedia's value wins on disagreement (it
   already read date+publisher together per-region, which is the safer
   read); a genuine conflict still gets the item filed with Wikipedia's
   value, with the conflict itself noted below rather than silently
   resolved or silently dropped.

**Fandom cross-referencing traps, found piloting 25 games this way (all
resolved in the pipeline, not just noted for next time):**

- **A same-titled Fandom article can silently be about a completely
  different, unrelated game** — looking up "The Amazing Spider-Man" landed
  on an article about the 2012 Wii/3DS movie tie-in, not the 1990 LJN Game
  Boy game; the correct page exists at the disambiguated title `The Amazing
  Spider-Man (Game Boy)`. This is the cross-reference-side twin of the
  shared-title trap below — don't trust a direct title match without
  checking the resolved page's own system/date data actually includes a
  Game Boy entry; fall back to `"<title> (Game Boy)"` or a `list=search`
  query when it doesn't.
- **Many Fandom infoboxes cover several platforms in one article** (NES,
  SNES, Game Boy, Virtual Console re-releases, ...), with `system1`,
  `system2`, `system3`... each carrying its own `systemN = <platform name>`
  label and `systemN<REGION>` date fields. **Match on the slot whose
  `systemN` label actually says "Game Boy"** (excluding "Game Boy Color"/
  "Game Boy Advance") — never assume `system1` is the right one; it's
  whichever platform the article lists first, often the original NES
  release for a multi-platform port.
- **A `<gallery>` block's `|` (filename**`|`**caption) reads as a false field
  boundary to a naive top-level-pipe field splitter** — treat `<gallery>` /
  `</gallery>` as depth-changing tokens the same way `{{`/`}}` and `[[`/`]]`
  already are, or the image field silently truncates and later fields shift
  by one.
- **A gallery's per-image caption can be a region tag ("NA"/"JP"/"EU") on a
  single-platform article, or a platform tag ("NES"/"SNES"/"Game Boy") on a
  multi-platform one — check for a platform tag that explicitly rules an
  image out before falling back to filename heuristics.** A same-titled
  image can be tagged with both a platform AND a region in its filename
  (`"... (NES) (NA).jpg"`) — a naive `"(NA)" in filename` check will
  wrongly accept an NES box just because it also happens to carry a region
  marker.
- **An untagged single (non-gallery) `image =` field on a multi-platform
  article is only safe to use when Game Boy is listed first (`system1`)** —
  otherwise it's conventionally the *first-listed* platform's box art (often
  the original NES release), not Game Boy's, even with no gallery to
  disambiguate. `Alfred Chicken`'s single image was explicitly captioned
  "North American NES box art" despite the article also covering a Game Boy
  release — caught by checking the `caption` field, not just the filename.
  When Game Boy isn't `system1` and the caption doesn't explicitly confirm
  Game Boy, leave the item imageless rather than risk a wrong-platform
  photo (5 of the 25-game pilot batch landed here as genuine, documented
  gaps — not a parsing bug).

**At full-library scale (499 games total), roughly a quarter of games had
some Wikipedia/Fandom disagreement on developer, publisher, or exact
release date.** All filed with Wikipedia's value per the policy above,
without exception — that rate is too high to document individually (it
would bury the guidance in this file under noise), so a handful of
representative examples are kept below instead of an exhaustive log:

- *Alleyway*: NA release date. Wikipedia: August 1, 1989. Fandom: August 11,
  1989. Filed as `1989-08-01`.
- *Adventure Island* (NA title for the Game Boy game also known in Japan as
  *Takahashi Meijin no Bōken Jima II*): developer. Wikipedia: Hudson Soft.
  Fandom's closest matching article (`Adventure Island II`, a combined
  NES+GB+VC article) credits Now Production instead — but that credit may
  actually belong to the *next* game in the series (*Adventure Island II:
  Aliens in Paradise*, Japan's *...III*), which Wikipedia independently
  also credits to Now Production. Filed as Hudson Soft; this whole
  franchise's Western/Japanese sequel-numbering is confusing across
  sources and deserves extra care rather than pattern-matching on title
  similarity alone.
- *Arcade Classic No. 3: Galaga / Galaxian*: developer. Wikipedia: Namco.
  Fandom: TOSE (with Namco credited only as the Japan-region *publisher*,
  not developer). Filed as Namco.
- **Most publisher disagreements turned out to be the two sources using
  different corporate granularity for the same real company, not an actual
  factual dispute** — e.g. "Malibu Games" (Wikipedia) vs. "Malibu
  Interactive"/"Black Pearl Software" (Fandom, an imprint/parent of the
  same publisher), or "Asmik Corporation of America" vs. "Asmik Ace" (US
  arm vs. Japanese parent). Filed with Wikipedia's name either way per
  policy; worth knowing before assuming every flagged conflict reflects
  real uncertainty about who actually published a game.
- A few disagreements looked like genuinely different companies with no
  obvious naming-variant explanation (*Chase H.Q.*: Bits Studios vs. Taito;
  *Crystal Quest*: NovaLogic vs. Data East) — these are real, unresolved
  conflicts between the two sources, not corporate-name noise, and a third
  source would be needed to actually settle them.

**Two more small sourcing bugs found and fixed scaling from the 25-game
pilot to the full library:**

- **A wiki-authored filename typo can defeat a case-sensitive `File:`
  prefix check** — one infobox's `image =` field read `FIle:Hook (GB)
  (NA).jpg` (capital I), which a naive `if not filename.startswith('File:')`
  check doesn't catch, producing a doubled `File:FIle:...` lookup that
  fails. Strip any case-insensitive `file:` prefix before re-adding it
  canonically.
- **An infobox's stated filename extension doesn't always match the
  actually-uploaded file** — `NBA Jam`'s infobox named `NBA Jam (GB)
  (NA).png`, but the real file on the wiki is a `.jpg`. Caught by the
  `imageinfo` lookup failing, resolved by searching the wiki directly for
  the game's file rather than assuming the infobox text is authoritative
  about its own asset's extension.
- **A superscript or accented Unicode character in a title can be silently
  dropped by a naive `[^a-z0-9]` slugify strip** — the pilot batch's own
  `Alien³` produced `alien.yaml` instead of `alien-3.yaml` this way (fixed
  by hand at the time). Fixed properly for the full library via
  `unicodedata.normalize('NFKD', s)` + dropping combining marks before the
  ASCII strip, which correctly folds `é→e`, `³→3`, `ō→o`, etc. instead of
  eating the character entirely.

**Franchise tagging at full-library scale**: matched titles against
`tags/franchises/` by keyword, reusing existing tags where they already
existed (`batman`, `mortal-kombat`, `pac-man`, `power-rangers`,
`spider-man`, `star-wars`, `street-fighter`, `contra`, plus the pilot's own
`alien`/`predator`/`the-addams-family`/`aladdin`/`animaniacs`/
`adventure-island`/`rocky-and-bullwinkle`), and creating ~110 new ones for
recognizable licensed IP and flagship game franchises not yet tagged
anywhere in the catalog (movie/TV tie-ins, wrestling promotions, and
multi-entry game series like *Mega Man*, *Kirby*, *Tetris*, *Castlevania*).
**Deliberately left untagged**: real-world sports leagues/athletes (Madden,
FIFA, NHL, PGA Tour, NBA Jam, Tecmo Bowl — not fictional IP in the
collectible-franchise sense), and Nintendo's own "Arcade Classic"-style
compilations of public-domain-adjacent classic arcade games (repackaging,
not itself a franchise being collected — same call as the pilot's
untagged Arcade Classic No. 1-4).

## Common pitfalls

- Don't conflate developer and publisher — many Game Boy titles were
  developed by one studio and published by another (or a different
  publisher per region).
- **Never pair a region's release `date` with another region's publisher.**
  The `date` and `publisher` on one record must describe the *same* release.
  A batch of 141 additions was rejected for exactly this (PR #193): *Harvest
  Moon GB* was filed with the Japanese date (Dec 1997) next to
  `publisher: Natsume Inc.`, who published only the North American release
  eight months later, so the record asserted something that never happened.
  Pick one release, and let its region determine both fields.
- **A shared title is not evidence of a shared game.** Western Game Boy
  releases were routinely built by relicensing or reskinning an unrelated
  Japanese cart, so an earlier JP entry with "the same" name is often a
  different product — not an earlier release of this one. Same PR conflated
  two that way (*Double Dragon II*, *F1 Pole Position*). Confirm the two are
  actually the same game before treating the earlier date as this record's
  first release.
- Compilation carts (multiple games on one cartridge) and multiplayer/
  peripheral-bundled releases (e.g. requiring a Game Link Cable accessory)
  need a curation decision before filing — check whether an existing
  precedent applies rather than guessing.
