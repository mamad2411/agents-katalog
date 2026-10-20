# HGUC (High Grade Universal Century) — curation hints

Bandai's original and largest HG sub-line, running since 1999. Flat — one
directory, one file per kit, no further nesting, no `variants`
sub-entities, same reasoning as [`../../rg/CLAUDE.md`](../../rg/CLAUDE.md).
See [`../CLAUDE.md`](../CLAUDE.md) for how this sub-line was discovered
and scoped relative to the rest of HG.

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`** — only 214 of 330 kits (65%) have a
documented lineup number, the same MG/RG/EG/PG/SD exception for the same
reason (a directory that sorts into two disjoint groups reads as a data
error). The number is still recorded as `attributes.number` wherever known.

## Scale

326 of 330 kits are `1/144`. Two are `Non-scale` (SD/chibi crossover
kits carrying the HGUC brand despite not being HGUC's usual scale — verify
per kit, don't assume). Two are recorded on their own box as `1/144` but
are actually `1/132` — Bandai's own labeling error, confirmed by the
wiki's infobox carrying both values (`1/144 (labeled)` and the true
`1/132`) — recorded as `attributes.scale: "1/132 (labeled 1/144)"` for
these two rather than picking one and silently dropping the discrepancy.

## Sourcing

Same Gunpla Wiki `allpages&apprefix=HGUC ` + `redirects=1` method as
[`../CLAUDE.md`](../CLAUDE.md) documents — 546 raw pages resolved to 330
real kits (3 more were `/Variants` navigational subpages, excluded; a
25-title sweep of links referenced from those subpages turned up no
further real kits, just redlinks already known to be missing).

**Images**: 325 kits had a usable infobox `image`; 3 more had no infobox
image but a "Stock Photos" gallery further down the page, used as a
fallback (same as every other grade in this project). 2 kits genuinely
have no image anywhere on their wiki page (`Dictus (Callisto's Light
Custom)`, `RGM-79S GM Spartan`) and stay imageless.
