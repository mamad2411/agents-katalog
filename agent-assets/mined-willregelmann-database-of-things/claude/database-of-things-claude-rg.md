# RG (Real Grade) — curation hints

Bandai's 1/144 Real Grade kit line, running continuously since 2010. Flat —
one directory, one file per kit, no sub-grouping, no `variants` sub-entities
(see below). Everything else follows [`../CLAUDE.md`](../CLAUDE.md) except
the deviations below.

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`, not `<number>-<slugified-name>.yaml`** —
the same deviation [`../mg/CLAUDE.md`](../mg/CLAUDE.md) documents for Master
Grade, for the same reason: **only 40 of 114 RG kits have a documented
lineup number** (event exclusives, P-Bandai-only releases, and alternate
finishes of an already-numbered kit are typically sold without one).
Prefixing the numbered fraction and not the rest would sort into two
disjoint groups. The number is still recorded as `attributes.number`
wherever known.

## No `variants` — recolors and exclusives are full items

A same-mold recolor or event/P-Bandai exclusive of an already-numbered kit
(e.g. GN-001 Gundam Exia → "Extra Finish Ver.", "Trans-Am Mode (Clear
Ver.)") could read as a `variants` sub-entity candidate under
[`../../../CLAUDE.md`](../../../CLAUDE.md)'s print-treatment rule — same
underlying mold, no number of its own. **Deliberately not used here**: MG
already has the identical situation (its own Exia recolors — Clear Color
Ver., Trans-Am Mode Gloss Injection Ver., etc. — none carry
`attributes.number` either) filed as full top-level items, and RG follows
that precedent for consistency within one product line rather than modeling
the same real-world kit two different ways across grades. Revisit
line-wide (not just here) before introducing `variants` to Gunpla.

## Not every kit shown at an expo shipped — check before filing

Three designs unveiled at Gunpla Expo World Tour 2012 (MS-07B Gouf, RGM-79
GM, RX-79[G] Gundam Ground Type) are explicitly flagged on Gunpla Wiki as
`{{Under Consideration}}` / "yet to be developed/produced" — concept art
and test-shot photos only, never a released product. Excluded from this
directory for that reason; a page with no `Release Date` at all (not even
a "See below" deferral) and only a "Test Patterns" or concept-art image is
a signal to check for this before filing, not just a data gap.

## Not a Gundam-only line

Same as MG: RG has shipped Neon Genesis Evangelion kits (`Scale = Non`,
i.e. `attributes.scale: Non-scale`) and two King of Braves GaoGaiGar kits
(GaoGaiGar, GoldyMarg) under the Real Grade brand. Don't filter candidates
by whether they're mobile suits.

## Excluded: multi-kit anniversary bundles

Two category pages — "Gunpla 40th Memorial Set" and "1/144 Mobile Suit
Gundam SEED 20th Anniversary MS Set (Metallic)" — repackage reissues of
already-existing, separately-numbered kits (spanning multiple grades in
one box) as one commemorative product. Per
[`../../../CLAUDE.md`](../../../CLAUDE.md)'s "collectibles, not products"
rule, a retail bundle of already-catalogued items isn't itself a new
collectible — excluded, not filed.

## Dates

72 of 114 kits have a sourced release date. **42 have none**, for the same
reason MG's gap exists: Gunpla Wiki defers them to a per-kit "Release
Dates" section rather than the infobox's `Release Date` field. Left unset
rather than guessed — filling them means parsing that section per kit, a
worthwhile follow-up (same status as MG's equivalent gap).

## Sourcing

[Gunpla Wiki](https://gunpla.fandom.com/) via its MediaWiki API, same
method and traps as [`../mg/CLAUDE.md`](../mg/CLAUDE.md) documents
(HTTP 402 on rendered pages but not the API; `Plamo_Infobox` vs.
`Plamo Infobox` vs. `Gunpla_Infobox` template-name variance; brace-match
the infobox rather than a lazy regex). Use `Category:Real Grade` for the
authoritative kit list (122 members as of this writing; subtract the grade
page itself plus its two navigational subpages, `Real Grade/Exclusives`
and `Real Grade/Special Editions`, to get the real kit count).

**Images**: every RG kit page's infobox carries an `image` field pointing
to a box-art photo, resolved to a permanent `static.wikia.nocookie.net` URL
via the API's `imageinfo` endpoint (`action=query&titles=File:<name>&
prop=imageinfo&iiprop=url`) — batch up to ~40 titles per call. **Normalize
spaces to underscores before matching a resolved filename back to its kit**
— the API's returned page title always uses spaces, but a kit's infobox
`image =` value is copied verbatim from the wikitext and is inconsistently
space- or underscore-separated; a naive exact-string lookup silently drops
matches for the underscore-written ones (13 of 114 on the first pass here).
This is a lower sourcing bar than a `_collection.yaml` logo (see
[`../../../../CLAUDE.md`](../../../../CLAUDE.md)'s "Logos" section and
[`../CLAUDE.md`](../CLAUDE.md)'s grade-logo note) — acceptable for an
item photo the same way a retailer/marketplace photo is a documented
fallback, not acceptable for a collection-level logo.
