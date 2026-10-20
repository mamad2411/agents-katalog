# HG (High Grade) — curation hints

Like SD (see [`../sd/CLAUDE.md`](../sd/CLAUDE.md)), HG is not one line — it's
an umbrella over dozens of **independently numbered timeline sub-lines**,
confirmed via research before filing anything (see the top-level
[`../CLAUDE.md`](../CLAUDE.md)'s warning about this). Full-scope research
(2026-08-08) found roughly 20 real sub-lines totaling ~1,480 raw wiki pages
— by far the largest grade in the Gunpla family, bigger than every other
grade combined. **All confirmed sub-lines are now populated:**

```
hg/
  CLAUDE.md
  _collection.yaml
  hguc/    # High Grade Universal Century — 330 kits, the original/largest sub-line
  hggs/    # High Grade Gundam SEED (original 2002-2010s era) — 84 kits
  hgce/    # High Grade Cosmic Era (newer current-era SEED prefix) — 55 kits
  hg00/    # High Grade Gundam 00 — 74 kits
  hggto/   # High Grade Gundam The Origin (08th MS Team-Thunderbolt era) — 62 kits
  hgibo/   # High Grade Iron-Blooded Orphans — 63 kits
  hgage/   # High Grade Gundam AGE — 41 kits
  hgbf/    # High Grade Build Fighters — 38 kits
  hgac/    # High Grade After Colony (Gundam Wing) — 21 kits
  hgbd/    # High Grade Build Divers — 20 kits
  hgfc/    # High Grade Future Century (G Gundam) — 11 kits
  hgiba/   # High Grade Iron-Blooded Arms (IBO add-on weapon sets) — 11 kits
  hgbc/    # High Grade Build Custom (add-on weapon/accessory sets) — 11 kits
  hggt/    # High Grade Gundam Thunderbolt — 6 kits
  hgaw/    # High Grade After War (Gundam X) — 7 kits
  hgrg/    # High Grade Reconguista in G — 4 kits
  hggb/    # High Grade Gunpla Builders (Build Fighters precursor) — 3 kits
  hgcc/    # High Grade Correct Century (Turn A Gundam) — 1 kit
  hgm/     # High Grade Mechanics (0083 large mobile armors, 1/550 scale) — 1 kit
  hggu/    # High Grade Gundam Wing Dual Story G-Unit — 1 kit
```

~1,181 kits total. If a genuinely new HG sub-line surfaces later (a new
timeline tie-in, a newly announced prefix), research its scope the same
way documented below before scaffolding it — this list isn't necessarily
exhaustive forever, just exhaustive as of the 2026-08-08 research pass.

**HGGS and HGCE are two separate sub-lines despite both covering the
Cosmic Era/SEED timeline** — confirmed by checking their category members
directly. HGGS is the original 2002-2010s SEED-era HG line; HGCE is a
distinct, newer prefix used for current-era SEED kits (SEED Freedom-tie-in
releases, sports-team collabs, etc.). Don't merge them into one directory
just because they cover the same in-universe timeline. Likewise, HGAC
(After Colony/Wing TV series) and HGGU (the Wing "G-Unit" manga spin-off)
are two separate Gundam Wing-adjacent sub-lines with independent
numbering, not one.

**Not every HG sub-line uses the grade's standard 1/144 scale** — HGM
("High Grade Mechanics") is a distinct sub-line for oversized mobile
armors from Mobile Suit Gundam 0083, built at 1/550 to keep the kit a
manageable size. Verify scale per kit/sub-line rather than assuming
1/144, same rule as [`../../CLAUDE.md`](../../CLAUDE.md).

**A kit's `Classification` field can list a second grade/sub-line it's
also nominally "part of the lineup" of, without actually being filed
there** — HGCC's sole kit lists both "High Grade Correct Century" and
"High Grade Universal Century (Part of the lineup)" and carries a real
HGUC-style lineup number, but the page's own title and opening prose
unambiguously call it an HGCC kit, and it isn't already filed under
`hguc/`. Filed by its primary sourced prefix; don't duplicate a kit into
a second sub-line just because its `Classification` field name-drops it.

**A sub-line's directory-name prefix doesn't always spell out what its
`Classification` field actually says, and can be genuinely misleading** —
HGGB's kits are named "Beginning Gundam"/"Forever Gundam" (suggesting a
"Beginning-Forever" movie tie-in), but their own infobox
`Classification` field reads "High Grade **Gunpla Builders**", tied to a
precursor media property to Gundam Build Fighters, not a "Beginning-
Forever" movie. Always read the `Classification`/`Franchise` fields
before writing a sub-line's `_collection.yaml` description rather than
inferring the tie-in from kit names alone.

**A short prefix can be an add-on weapon/accessory-set sub-line, not
mobile-suit kits** — both HGI-BA ("Iron-Blooded Arms") and HGBC ("Build
Custom") bundle weapon runners or display accessories rather than full
mobile suits, each with its own numbering distinct from any mobile-suit
sub-line. Still filed the same way as any other sub-line (own directory,
own numbering) — each set is sold as its own boxed, JAN'd, HG-classified
kit, not a component of some other kit. Don't assume a sub-line is out of
scope just because its contents aren't a full mobile suit; check the
`Classification` field and box-art description. HGRG is a related but
distinct case: not weapon sets, but equipment-pack add-ons for one base
kit whose own base release wasn't found under this prefix (likely filed
under another grade) — still a legitimate, independently-numbered
sub-line by the same logic.

## Sourcing: verify the wiki category name, it's rarely the short prefix

`Category:HGUC`, `Category:HG00`, etc. **do not exist** — the wiki
categorizes by spelled-out name (`Category:High Grade Universal Century`,
`Category:High Grade Gundam 00`, ...). The `allpages&apprefix=<PREFIX> `
method (same as every other grade) is the reliable way to enumerate a
sub-line's real kit pages by the prefix that actually appears in kit
titles — **always resolve with `redirects=1`** before trusting a raw
count; HGUC's 546 raw pages resolved to 330 real unique kits, HGGS's 149
resolved to 84. A sub-line's redirect dedup ratio varies widely — HGFC's
26 raw resolved to only 11 real kits (58% dedup, mostly from in-fiction
alias titles and spelling-variant pairs, not `/Variants` pages), while
HGBC's 11 raw resolved to all 11 real (0% dedup), and HGCC's 3 raw
(two are alternate-title redirects) resolved to just 1 real kit.

**MediaWiki's anonymous API caps `titles=` at 50 values per call** — chunk
at 20 (same as every other grade's fetch script) rather than requesting
all of a sub-line's titles in one call; a raw multi-title `curl` without
chunking silently returns a `toomanyvalues` error instead of data.

**Watch for `/Variants` navigational subpages** — a kit's own
`<title>/Variants` subpage (e.g. `HGUC RX-0 Unicorn Gundam (Destroy
Mode)/Variants`) is a list page linking to sibling releases, not a
product itself; it resolves as a "real" page under `redirects=1` but has
no infobox and must be excluded from the item set. Also a good place to
cross-reference for kits missing from the main `allpages` sweep — HGUC's
did surface 25 additional candidate titles this way, though all turned
out to be either duplicates already captured or genuine redlinks (kits
referenced but with no page written yet), not real gaps. Not every
sub-line has these — HGGS had none.

**Not every `/`-subpage is a `/Variants` list page, though — some are real
kits filed as subpages of their base kit's title.** HGGT had two
(`<base>/ONA Ver.`, `<base>/Bandit Flower Ver.`), each with a full
infobox, own `Release Date`, and own `image` — genuine distinct releases,
not navigational pages. The discriminator is always infobox presence, not
the `/` in the title. Renamed these to a parenthetical form for the `name`
field (matching every other bracketed-variant naming in this project)
since the wiki's own parenthetical alternate title for the same page was
just a redirect alias, not a separate missing kit.

**A malformed infobox `image =` value can be a full `[[File:...|thumb]]`
wikilink instead of a bare filename** — one HGUC kit
(`RX-78-3 Gundam + MS-09RS Rick Dom`) had this, and the standard
`[[...|X]]`-strips-to-`X` cleanup used everywhere else in this project
silently extracted the literal word "thumb" instead of the filename.
Worth a sanity check (does the resolved "filename" look like a real
image filename?) rather than assuming every infobox follows the plain
`image = Some-File.jpg` format.

**A second wiki-image placeholder filename exists**:
`Gunpla-Wiki-No-Image-Available.jpg` (HGBD), a sibling to the plain
`No-Image-Available.jpg` seen on HGUC — both are literal placeholder
strings the wiki uses in place of a real filename, not real files. Treat
any `image=` value containing "No-Image-Available" as empty and fall back
to the page's Stock Photos gallery.

**An infobox `image` filename can carry the wrong sub-line prefix without
being wrong** — HGAW's `GX-9900-DV Gundam X Divider` uses a file named
`HGUC-Gundam-X-Divider-box.jpg`, just a wiki upload-naming inconsistency;
the page's own title and category are unambiguously HGAW. Trust the
page's title/category over an inconsistent asset filename.

**Unreleased-kit markers vary per sub-line — grep for more than one
pattern.** On top of `{{Canceled}}`/`{{Template:Canceled}}` (see
[`../pg/CLAUDE.md`](../pg/CLAUDE.md)) and "Under Consideration" (see
[`../rg/CLAUDE.md`](../rg/CLAUDE.md)), HGCE turned up a third:
`{{PollsDoesNotGuarantee}}`, marking a fan-census poll result that was
never actually produced. None of these pages have a usable infobox, which
is what naturally excludes them from a parse pass keyed on infobox
presence — but don't assume "has no infobox" is itself sufficient
evidence something's unreleased without checking why it's missing one.

**A bare keyword hit for "unreleased"/"canceled" is very often a false
positive — always verify against the page's own infobox, never trust the
keyword alone.** Recurred on PG, HG00, HGAC, and HGFC: the match was
boilerplate Variants-section prose about a *different*, unrelated kit
(often a different grade entirely), not a marker on the page in question.

**A sub-line's own infobox `Scale`, `Classification`, and `Release Date`
fields can have outright typos/copy-paste errors, or a date can be typed
into the wrong field entirely.** HGGS had one kit labeled `1/44` (should
be `1/144`, no such Gunpla scale exists) and another labeled
`Classification = High Grade Universal Century` despite being a Cosmic
Era unit (a copy-pasted infobox, not a real cross-grade kit) — see
`hggs/CLAUDE.md`. HGBD's `GNX-803OG Ogre GN-X` infobox said `Release Date
= May 19, 2015`, flatly contradicted by the article's own opening prose
("released in 2018") — corrected by hand. HGI-BA's `Mobile Suit Option
Set 7` had an entire infobox (lineup no., date, price, JAN) copy-pasted
byte-for-byte from a sibling kit's page despite distinct box art and
contents — left the date unset rather than propagate a known-wrong value.
HGBC's `Diver Ace Unit` had a blank `Release Date =` but the actual date
sitting in the unrelated `Need paint? =` field instead — recovered by
reading the misplaced field. Skim for obviously-wrong outliers, check
adjacent fields for a misplaced value, and cross-check against
surrounding prose before trusting a bulk field extraction wholesale.

**When reusing a prior sub-line's scripts by prefix substitution, verify
the string-slice offsets got updated too** — copying `hgcc/build_draft.py`
to `hgm/` via a blind text substitution (`HGCC`→`HGM`) left a stale
`n[5:]` slice sized for the 5-character `"HGCC "` prefix instead of the
4-character `"HGM "`, silently truncating the first real character off
every kit name until caught by eyeballing the draft output. Always
re-check a copied script's hardcoded lengths/offsets against the new
prefix's actual length, not just its text.

Every other convention (flat directory per sub-line, `<slugified-name>.yaml`
no number prefix, no `variants` sub-entities, unreleased/`{{Canceled}}`
kit checks) follows [`../rg/CLAUDE.md`](../rg/CLAUDE.md),
[`../eg/CLAUDE.md`](../eg/CLAUDE.md), [`../pg/CLAUDE.md`](../pg/CLAUDE.md),
and [`../sd/CLAUDE.md`](../sd/CLAUDE.md) — see each sub-line's own
`CLAUDE.md` for its specific numbers and quirks.
