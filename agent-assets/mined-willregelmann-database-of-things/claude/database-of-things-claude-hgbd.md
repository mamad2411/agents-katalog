# HGBD (High Grade Build Divers) — curation hints

The High Grade prefix tying into the Gundam Build Divers anime and its
in-fiction virtual Gunpla-battling premise. Flat — one directory, one file
per kit, no further nesting, no `variants` sub-entities, same reasoning as
[`../../rg/CLAUDE.md`](../../rg/CLAUDE.md).

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`** — only 18 of 20 kits (90%) have a
documented lineup number, same MG/RG/EG/PG/SD/HG*-flat-naming exception.

## Sourcing

Same `allpages&apprefix=HGBD ` + `redirects=1` method as
[`../hguc/CLAUDE.md`](../hguc/CLAUDE.md) — 30 raw pages resolved to 20 real
kits, no `/Variants` navigational subpages, no unreleased/`{{Canceled}}`
kits found — the cleanest scope pass of any HG sub-line so far (every
candidate title resolved to a real, released kit).

**A second wiki-image placeholder filename found: `Gunpla-Wiki-No-Image-
Available.jpg`.** One kit (`GN-0000DVR/A Gundam 00 Diver Ace (Gold Plated
Ver.)`, a campaign-prize kit) had this literal placeholder string in its
infobox `image=` field instead of a real filename — a sibling pattern to
HGUC's plain `No-Image-Available.jpg` (see
[`../CLAUDE.md`](../CLAUDE.md)). Neither is a real file on the wiki; treat
any `image=` value containing "No-Image-Available" as empty and fall back
to the page's Stock Photos gallery (which had one for this kit).

**An infobox `Release Date` can be an outright typo contradicted by the
page's own prose** — `GNX-803OG Ogre GN-X`'s infobox said `May 19, 2015`,
but the article's own opening sentence says "is a 1/144 scale kit released
in **2018**" (consistent with every other HGBD kit — the line didn't exist
before 2018, tying into the anime that aired that year). Corrected to
2018-05-19 (kept the day/month, fixed the obviously-wrong year) rather than
propagated. A sanity check against the surrounding prose, not just the
infobox field, catches errors a plain field extraction would miss.

**Two kits deferred their `Release Date` to a page section instead of
stating it in the infobox** (`[[...#Availability|See below]]` /
`[[...#Release Dates|See below]]`), same pattern as
[`../hgibo/CLAUDE.md`](../hgibo/CLAUDE.md) — resolved by reading the
referenced section by hand: `PEN-01M Momokapool (Ver. Zaishin)`'s
Availability section gave an exact event window (August 11 – September 2,
2018 at Gundam Docks Hong Kong III), recorded as its start date
(2018-08-11); `RMS-099BC Build Γ Gundam`'s Release Dates section gave
"January 2020 (First Batch)", recorded as 2020-01. A third kit (`Gundam 00
Diver Ace (Gold Plated Ver.)`) had no Release Date field at all, but its
own prose said "released in 2018" — recorded at year precision, the most
the source supports.

**Images**: 20 of 20 kits resolved to a usable filename via the infobox
image field or Stock Photos fallback; all verified HTTP 200.
