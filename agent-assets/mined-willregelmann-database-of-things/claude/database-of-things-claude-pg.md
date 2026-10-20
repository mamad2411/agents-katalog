# PG (Perfect Grade) — curation hints

Bandai's 1/60 flagship kit line, running since 1998 at a much slower
release cadence than MG/RG — roughly one kit a year. Flat — one directory,
one file per kit, no sub-grouping, no `variants` sub-entities, same
reasoning as [`../rg/CLAUDE.md`](../rg/CLAUDE.md).

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`**, the same MG/RG/EG exception — only
8 of 23 kits have a documented lineup number (recolors and exclusives
generally don't get one, same pattern documented across the other grades).

## Sourcing: trust the category + `PG `-prefix allpages listing, NOT the
## old "Perfect Grade" main page gallery

This is the reverse lesson from [`../eg/CLAUDE.md`](../eg/CLAUDE.md), where
the category was the unreliable source — here it's the opposite. The main
`Perfect Grade` wiki page's lineup gallery lists several kits
(`PG MSZ-006 Zeta Gundam`, `PG MS-06F Zaku II`, `PG RX-178 Gundam Mk-II`
(both AEUG and Titans versions), `PG RX-78GP01 Gundam "Zephyrantes"/Fb`,
`PG GN-0000GNHW/7SG 00 Gundam Seven Sword/G`, `PG Evangelion Unit 01`,
`PG Millennium Falcon`) that **were never released as PG at all** — Zeta
Gundam, Zaku II, and Mk-II exist as MG/RG/HGUC kits instead, Seven Sword/G
is an HG00 kit, and the other two are pure redlinks with no page. Direct
search confirms none of these are real PG products; the gallery page is
stale, not just incomplete.

The reliable method: fetch `Category:Perfect Grade` (25 members) AND
`action=query&list=allpages&apprefix=PG ` (42 titles, mostly redirects) —
resolve every candidate with `redirects=1` to collapse duplicates/aliases
to their real target page, cross-check the two lists agree. They did here,
converging on 25 real pages, 2 of which turned out `{{Canceled}}` (see
below) for 23 actually-released kits.

**A page can exist and still document a kit that was never released.**
`PG GAT-X105 Sword/Launcher Strike Gundam` and `PG MBF-P01 Gundam Astray
Gold Frame` both resolve to real pages (unlike RG's "Under Consideration"
concept kits, which had no proper page at all) but are explicitly tagged
`{{Canceled}}`/`{{Template:Canceled}}` with `Release Date = N/A` — grep
for that template, not just prose like "unreleased", before trusting a
resolved page is a real product. Other kits' own "Variants" sections
reference these two with wiki strikethrough formatting
(`<s>...</s>`) as a second confirmation signal.

**Redlinks found via "Variants" section cross-references, not filed —
deferred, same policy as MG/RG/EG's undocumented kits.** PG kit pages
carry a rich "Variants" section listing sibling releases (reissues,
region exclusives, recolors) that often link to kits with no page written
yet — 15 found this pass (Astray Red Frame Metallic Gloss Injection, MBF-
P02Kai, several Unicorn/Banshee Norn/Phenex color variants, a Trans-Am
Raiser, an Aile Strike Clear Pearl Shift Ver., etc.). Confirmed via a
`redirects=1` existence check the same way as the main candidate list —
don't assume a "Variants" mention means a sourceable page exists.

**Images**: same `imageinfo` + space/underscore normalization method as
[`../rg/CLAUDE.md`](../rg/CLAUDE.md) and [`../eg/CLAUDE.md`](../eg/CLAUDE.md)
document. All 23 kits had a usable infobox `image` this time — no
fallback-photo cases needed.

## Scale

All 23 released kits are `1/60` — no exceptions found this pass (unlike
MG, which has a handful of off-scale kits). Verify per kit anyway before
assuming this always holds, per the root gunpla `CLAUDE.md`.
