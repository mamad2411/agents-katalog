# HGGS (High Grade Gundam SEED) — curation hints

The original 2002-2010s High Grade line for the Cosmic Era/Gundam SEED
timeline — distinct from the newer HGCE prefix used for current-era SEED
kits (see [`../CLAUDE.md`](../CLAUDE.md)). Flat — one directory, one file
per kit, no further nesting, no `variants` sub-entities, same reasoning as
[`../../rg/CLAUDE.md`](../../rg/CLAUDE.md).

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`** — 76 of 84 kits (90%) have a
documented lineup number, higher coverage than HGUC but still not 100%,
so the same MG/RG/EG/PG/SD/HGUC flat-naming exception applies for
consistency.

## Sourcing

Same `allpages&apprefix=HGGS ` + `redirects=1` method as
[`../hguc/CLAUDE.md`](../hguc/CLAUDE.md) — 149 raw pages resolved to 84
real kits, no `/Variants` navigational subpages this time, no unreleased/
`{{Canceled}}` kits found. Every kit had both a `Release Date` and an
`image` in its infobox — the cleanest sourcing pass of any Gunpla
sub-line so far, no fallback-photo cases needed.

**One kit's `Scale` field was a wiki typo (`1/44` instead of `1/144`)** —
`MBF-P02 Gundam Astray Red Frame` — corrected by hand rather than
propagated; Gunpla doesn't make 1/44 scale kits, and Astray Red Frame's
other grade releases (MG, RG) are all standard scale. Worth a sanity
skim of the scale distribution before trusting it wholesale, same
lesson as HGUC's mislabeled `1/144`-vs-actual-`1/132` pair.

**One kit's `Classification` field says "High Grade Universal Century"
despite being a Cosmic Era unit** (`HGGS METEOR Unit`) — a wiki data-entry
error (likely a copy-pasted infobox template), not a real cross-grade
kit. Doesn't affect filing here since sub-line membership is determined
by the `HGGS` title prefix via `allpages`, not the `Classification`
field — but don't trust `Classification` as an authoritative signal if
ever used for something else.
