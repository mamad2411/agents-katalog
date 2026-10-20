# HGI-BA (High Grade Iron-Blooded Arms) — curation hints

A High Grade prefix for **add-on weapon/option parts sets** tied to Mobile
Suit Gundam: Iron-Blooded Orphans — not mobile-suit kits themselves (those
are [`../hgibo/CLAUDE.md`](../hgibo/CLAUDE.md), a separate sub-line with
its own numbering). Each set bundles weapon runners with a small "Mobile
Worker" companion figure. Still a legitimate item per
[`../../../../CLAUDE.md`](../../../../CLAUDE.md) — it's sold as its own
boxed, JAN'd HG-classified kit (`Classification = High Grade IRON-BLOODED
ARMS` in its own infobox), not a component of some other kit. Flat — one
directory, one file per kit, no further nesting, no `variants`
sub-entities, same reasoning as
[`../../rg/CLAUDE.md`](../../rg/CLAUDE.md).

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`** — 10 of 11 kits have a documented
lineup number (one, the Gundam Ace magazine bonus add-on kit, has none),
same MG/RG/EG/PG/SD/HG*-flat-naming exception.

## Sourcing

Same `allpages&apprefix=HGI-BA ` + `redirects=1` method as
[`../hguc/CLAUDE.md`](../hguc/CLAUDE.md) — 12 raw pages resolved to 11
real unique kits, no unreleased/`{{Canceled}}` kits found.

**One kit's infobox metadata is a verbatim copy-paste from a sibling kit's
page, not its own data** — `HGI-BA Mobile Suit Option Set 7`'s infobox
(`Lineup no. = 06`, `Release Date = November 12, 2016`, same `Price` and
`JAN/ISBN`) is byte-identical to `Mobile Suit Option Set 6 & HD Mobile
Worker`'s infobox, even though the two pages list entirely different
included parts and have distinct box-art image files (`MS-Option-Set-6-
boxart.jpg` vs `MS-Option-Set-7-boxart.jpg`) — a real, distinct kit with a
wiki editor's copy-paste error, not a duplicate to exclude. Corrected
`number` to `07` (matching the title, box art filename, and the 1-9
sequence) but left `date` unset rather than propagate a release date
known to be wrong — a genuine, documented gap, not a parsing bug.

**Images**: 11 of 11 kits had a usable infobox `image`, all verified HTTP
200.
