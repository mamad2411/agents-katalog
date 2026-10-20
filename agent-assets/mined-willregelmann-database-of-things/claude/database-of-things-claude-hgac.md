# HGAC (High Grade After Colony) — curation hints

Covers mobile suits from *New Mobile Report Gundam Wing* at 1/144 scale.
Flat — one directory, one file per kit, no further nesting, no
`variants` sub-entities, same reasoning as
[`../../rg/CLAUDE.md`](../../rg/CLAUDE.md).

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`** — only 10 of 21 kits (48%) have a
documented lineup number, same flat-naming exception as every other
sub-line so far.

## Sourcing

Same `allpages&apprefix=HGAC ` + `redirects=1` method as
[`../hguc/CLAUDE.md`](../hguc/CLAUDE.md) — 36 raw pages resolved to 21
real targets, no `/Variants` navigational subpages. One kit
(`XXXG-01S Shenlong Gundam`) hit a false-positive "unreleased" keyword
match — its own Notes & Trivia section describes the kit's *history* as
a long-running fandom "unreleased kit" meme before it finally shipped in
2022 (confirmed real by its own `Lineup no.`/`Release Date` fields) —
another reminder to check the page's own infobox data, not just a bare
keyword hit, same lesson as HG00's `{{Canceled}}` false positives.

**Scale**: same `1/144`-labeled-but-actually-`1/132` quirk as HGUC, on
`OZ-06MS Leo` — recorded as `attributes.scale: "1/132 (labeled 1/144)"`.
One kit (`WMS-03 Maganac 36-piece Set`, a bulk multi-unit Premium Bandai
exclusive) had no `Scale` field in its infobox at all — inferred `1/144`
from the base `WMS-03 Maganac` kit it's explicitly a bulk variant of,
rather than leaving it blank.

**Images**: all 21 kits had a usable infobox `image` — no fallback
photos needed.
