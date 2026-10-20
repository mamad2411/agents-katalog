# Game Boy Color — curation hints

**Status: all North American-released licensed Game Boy Color titles are
catalogued**, per Wikipedia's "List of Game Boy Color games" NA column (see
Sourcing below).

## Scope

Games released on **Game Boy Color-format cartridges** — its own hardware
generation, its own product-code prefix (`CGB-`), and its own physical
cartridge shape, distinct from the original Game Boy's DMG-format carts
even when a title is playable on both. This is a different axis from
"which hardware can run it": a GBC cartridge comes in two classes —

- **"Dual Mode" cartridges** — molded in black plastic, boxes labeled
  "Compatible with Game Boy," playable on original monochrome Game Boy
  hardware as well as Game Boy Color (many also support Super Game Boy
  peripheral features).
- **Game Boy Color-exclusive cartridges** — molded in clear plastic,
  boxes labeled "Only for Game Boy Color," won't run on original Game Boy
  hardware at all.

Both classes are cartridges sold and shelved as *Game Boy Color* product —
they belong here, in `game-boy-color/`, not split between here and
[`../game-boy/`](../game-boy/CLAUDE.md) by technical backward-compatibility.
`../game-boy/` covers the separate, non-overlapping library of original
DMG-format cartridges only. Recorded via `attributes.compatible_with_game_boy`
(see Attributes below) rather than as a directory split.

## Directory structure

```
game-boy-color/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "Game Boy Color" platform
  <slugified-name>.yaml
```

Flat, no sub-grouping — same reasoning as `../game-boy/CLAUDE.md`.

## Attributes

`developer`, `publisher`, same as Game Boy (no `genre` — dropped from that
platform's schema per curator preference, not reintroduced here).
`compatible_with_game_boy` (boolean) records the Dual Mode vs.
Color-exclusive cartridge class described above — sourced directly from
Wikipedia's own "Dual Mode" column, not inferred.

`catalog_number` (the `CGB-<code>-<region>` product code) remains
deferred, same unresolved-source situation as Game Boy.

## Naming files

`<slugified-name>.yaml` — no canonical numbering, same as Game Boy.

## Sourcing (North American releases)

Same two-source method as [`../game-boy/CLAUDE.md`](../game-boy/CLAUDE.md)
(Wikipedia primary, Nintendo Fandom wiki cross-check, Wikipedia's value
wins on disagreement) — but the Wikipedia table itself has a **meaningfully
different structure** from the Game Boy list, worth knowing before reusing
the GB parsing scripts verbatim:

- **Publisher is a single flat field for most rows**, not per-region
  `<sup>`-tagged like the GB table defaults to — but per-region tagging
  *does* still show up on a real minority of rows (e.g.
  `[[Infogrames]] <sup>NA</sup><br />[[Capcom]]<sup>JP</sup>`), so the
  per-region-tag extraction logic is still needed, just triggers less
  often.
- **Release date comes from a single `{{Vgrtbl|...}}` template** per row,
  not three separate date columns — its arguments alternate
  `region-spec, date, region-spec, date, ...`, where `region-spec` can be
  a comma-separated list covering multiple regions at once
  (`{{Vgrtbl|NA, EU|1999-08}}`) or split individually
  (`{{Vgrtbl|EU|1999-12-17|NA|2000-03-24|JP|2001-03-30}}`). A trailing
  empty argument from a stray `|` before `}}` is common — filter empty
  args before pairing them up.
- **A "Dual Mode" column** (`{{Yes}}`/`{{No}}`) is real, sourceable data
  worth its own attribute (see above) — this platform is the first
  Nintendo handheld in this catalog where cartridge compatibility class is
  a first-class, wiki-documented fact rather than something to infer.
- **Alternate per-region titles are joined by a bare `•` bullet in
  addition to `<br/>`** (e.g. `''Three Lions'' <sup>EU</sup>''•Alexi
  Lala's International Soccer <sup>NA</sup>`) — a title parser that only
  splits on `<br/>` will treat the whole bullet-joined string as one
  segment, see it contains an EU tag, and skip the NA alt-title entirely
  along with it. Split on `•` too.
- **Wikitext tag casing is inconsistent** — this table mixes `<sup>` and
  `<SUP>`, `<br/>` and `<BR />`. Every regex touching these tags needs
  `re.IGNORECASE`, not just the ones that happened to hit a lowercase
  example first. Caught two different real titles broken this way
  (`Metal Walker`, and a `<BR />`-using row) before fixing all tag-regexes
  uniformly rather than patching each casing variant as found.
- **A generic `<[^>]+>` tag-only strip silently glues two `<br/>`-joined
  values together with no separator** — `"[[Capcom]]<br/>M4 Ltd."` became
  `"CapcomM4 Ltd."` this way (a real co-developer credit,
  *Resident Evil Gaiden*). Convert `<br/>` to a real separator (`", "`)
  before the final tag strip, then trim any stray leading/trailing comma
  left over when the `<br/>` was actually the first or last thing in the
  cell (a title cell's trailing `<BR />` before its bullet-joined
  alt-title, once split apart, leaves nothing after it to separate).

**At full-library scale (443 NA games), roughly 31% had some Wikipedia/
Fandom disagreement on developer, publisher, or date** — filed with
Wikipedia's value throughout, same policy as Game Boy, and not logged
individually for the same reason (the pattern is what's useful, not an
exhaustive per-title list). Same shape of findings as Game Boy: most
publisher/developer differences are corporate-naming variance for the
same real company, a minority are genuine unresolved disagreements between
the two secondary sources.

**Fandom cross-referencing found one new image-selection trap beyond
Game Boy's list**: a single (non-gallery) `image =` field can be
explicitly labeled for the **wrong region**, not just the wrong platform
— `Aliens: Thanatos Encounter`'s sole image was
`File:Aliens Thanatos Encounter Box Art EU.jpg`, a real European box shot
with no NA alternative on the page at all. The original Game Boy
disqualification logic only checked for a wrong *platform* tag (NES/SNES/
etc.); it didn't check for an explicit EU/JP/PAL marker on an otherwise
platform-correct image. Caught 13 wrong-region images this way before
adding the check — treat an explicit non-NA region marker in a filename or
label as disqualifying, the same as a wrong-platform one, even when no
competing NA-tagged option exists to prefer instead.

**Two more parsing bugs, both from patterns not seen on Game Boy:**

- **`image = [[File:X.jpg|250px]]`** — a full wikilink with a size
  parameter, not a bare filename. The generic wikilink-cleanup regex
  (built for `[[Page|Display Text]]` links, which correctly keeps the
  *last* pipe-segment) grabs `"250px"` instead of the filename here.
  Detect the `[[File:...|...]]` / `[[Image:...|...]]` pattern specifically
  and pull the filename directly rather than running it through the
  generic display-text cleaner.
- **A tag entity's own `name` needs the same YAML-escaping as any other
  field** — creating ~150 new franchise tags in bulk for this platform's
  library wrote `name: Atlantis: The Lost Empire` unquoted for 17 of them
  (any name containing `:`, `&`, an apostrophe, etc.), which is a genuine
  YAML parse error (an unquoted `: ` mid-scalar reads as a second mapping
  key), caught by the validator crashing outright rather than reporting a
  clean error list. Apply the same `yaml_escape` used for item fields to
  tag names too when generating them programmatically.

**A bare numeric title is a schema violation, not just a style question**
— `1942`'s `name: 1942` (unquoted) parses as a YAML integer, which fails
`item.schema.json`'s `name` string-type check outright. `yaml_escape` now
quotes anything that parses as a number or a YAML reserved word (`true`/
`false`/`null`/`yes`/`no`), not just strings containing punctuation —
worth carrying forward to any future platform, since a numeral-only title
is common enough in gaming (`1942`, `720°`, `NHL 2000`-style titles are
fine since they're not *purely* numeric, but a bare year or number alone
isn't rare).

**Franchise tagging**: 312 of 443 games (70%) matched an existing or
newly-created franchise tag — much higher coverage than Game Boy's pass,
partly because many GBC titles are direct sequels/ports of already-tagged
Game Boy franchises (reusing those tags directly) and partly because this
pass added ~150 more new tags for licensed movie/TV/toy-brand tie-ins and
recognizable game franchises not yet seen in the catalog. Same exclusions
as Game Boy: real-world sports leagues/athletes/vehicle brands, and
Microsoft/Midway-style compilations of someone else's classic games.
