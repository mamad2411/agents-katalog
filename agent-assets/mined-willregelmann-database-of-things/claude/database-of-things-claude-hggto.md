# HGGTO (High Grade Gundam The Origin) — curation hints

Covers mobile suits from the *Mobile Suit Gundam: The Origin* manga/OVA
prequel at 1/144 scale (the "GTO" abbreviation is for "Gundam The
Origin," not "08th MS Team" or "Thunderbolt" as their era might suggest —
verify what a prefix actually stands for from the infobox
`Classification` field rather than guessing from raw category size
alone). Flat — one directory, one file per kit, no further nesting, no
`variants` sub-entities, same reasoning as
[`../../rg/CLAUDE.md`](../../rg/CLAUDE.md).

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`** — only 26 of 62 kits (42%) have a
documented lineup number, same flat-naming exception as every other
sub-line so far.

## Sourcing

Same `allpages&apprefix=HGGTO ` + `redirects=1` method as
[`../hguc/CLAUDE.md`](../hguc/CLAUDE.md) — 124 raw pages resolved to 64
real targets, 2 of which were `/Variants` navigational subpages
(excluded; their links surfaced no additional kits). No unreleased/
canceled kits found.

**Images**: 60 of 62 kits had a usable infobox `image`; 2 more had no
infobox image but a "Stock Photos" gallery further down the page, used
as a fallback (same as every other grade). All 62 resolved successfully
on verification, though one took a couple of retries due to a transient
CDN 503 — confirmed the file genuinely exists via the wiki's own
`imageinfo` API before retrying rather than assuming it was broken.

**Dates**: 34 of 62 have one; 28 defer to a "See below" per-kit section,
the highest proportion of any HG sub-line populated so far but the same
established gap-not-a-bug pattern.
