# EG (Entry Grade) — curation hints

Bandai's simplified, tool-free beginner kit line. Two disjoint generations,
not one continuous line: a 2011 Asia-exclusive launch (4 kits) and a 2020
worldwide relaunch (30 kits, still active) — the two share no numbering and
several kit names repeat across them (both eras have their own "RX-78-2
Gundam" and "GAT-X105 Strike Gundam"). Flat — one directory, both
generations together, no `<generation>/` nesting (a deliberate call, see
below) — and no `variants` sub-entities, same reasoning as
[`../rg/CLAUDE.md`](../rg/CLAUDE.md).

## Naming files: no number prefix, year-disambiguate only real collisions

**Files are `<slugified-name>.yaml`**, same MG/RG exception — EG's coverage
is even thinner: only 9 of 34 kits have a documented lineup number (the
2011 line used plain `01`-`04`; the 2020 line uses its own `EX-0`/`EX1`/...
scheme that doesn't continue cleanly, and most kits — recolors, event
exclusives — have none at all, per the same pattern documented in
`../mg/CLAUDE.md`).

Kept flat rather than nested by generation (`eg/2011/`, `eg/2020/`) —
considered, given how cleanly the generations split, but Will's call was to
match MG/RG's flat precedent. This means exactly two name collisions need a
year disambiguator that Bandai's own box art doesn't print: the 2011 and
2020 "RX-78-2 Gundam" are `rx-78-2-gundam-2011.yaml`/`rx-78-2-gundam-2020.yaml`
(`name: RX-78-2 Gundam (2011)`/`(2020)`), same treatment for "GAT-X105
Strike Gundam". Every other kit keeps its bare name — don't add a year
parenthetical to a kit that doesn't actually collide with one from the
other generation.

## Not a Gundam-only line — more so than MG or RG

Same "Entry Grade" brand, same `Classification = Entry Grade` infobox
field, covers Doraemon, My Hero Academia (Izuku Midoriya), Kamen Rider
(Zero-One, Saber), and Detective Conan (Edogawa Conan) kits alongside
Gundam ones — a wider non-Gundam footprint than MG's single Kamen Rider
kit. The wiki's own lineup gallery lists further Dragon Ball, Ultraman,
Naruto, and Kirby kits with no page written yet (see "Known gap" below) —
expect this list to grow across even more franchises.

## Cross-grade and multi-item bundle products stay one item

A few EG products bundle in non-EG content or multiple distinct figures
under one box/JAN — filed as a single item each, matching how
[`../rg/CLAUDE.md`](../rg/CLAUDE.md) keeps RG's own cross-grade Akatsuki +
Zeus Silhouette bundle as one entity:

- `EG (2020) Edogawa Conan (MS-06S Zaku II Color) & HGUC MS-06S Zaku II
  (Shuuichi Akai Color)` bundles an EG figure with an unrelated HGUC kit.
- The two "Mini Gunpla" bath-toy crossovers (`Strike Gundam (Deactive
  Mode) & Mini Gunpla GOOhN.../ZnO...`) bundle an EG Strike Gundam with
  non-Gunpla "Mini Gunpla" creature figures, sold under Bandai's separate
  "Surprised Egg Dramatic Bath" novelty line.

`attributes.scale` on these records each component's scale inline (e.g.
`"1/144 (Zaku II); Non-scale (Conan Edogawa)"`) since a single enum-style
value can't represent a mixed-scale product honestly.

## Sourcing

Same [Gunpla Wiki](https://gunpla.fandom.com/) MediaWiki-API method as
[`../rg/CLAUDE.md`](../rg/CLAUDE.md) and [`../mg/CLAUDE.md`](../mg/CLAUDE.md)
document — but **`Category:Entry Grade` is NOT a complete kit list here,
unlike MG's and RG's categories.** It returned only 16 of the line's 34
real kit pages; the missing 18 (including the flagship 2020 `RX-78-2
Gundam` and `GAT-X105 Strike Gundam` base kits) simply aren't tagged into
the category. **Use the `Entry Grade/2020` lineup gallery page instead**
(`action=query&prop=revisions&titles=Entry Grade/2020`) — its `link=`
gallery parameters are the authoritative list, cross-referenced against
the category rather than trusting either alone. That page is itself
tagged `{{WorkInProgress}}` — re-check it for kits added since this pass
before assuming it's exhaustive either.

**Verify every linked title actually resolves to a page before trusting
it** — of the 51 unique titles found across the category + gallery, 2 were
gallery link-title typos missing the "(2020)" year marker (same page
already reachable via its category-listed title), 1 was a `#REDIRECT`
stub whose target must be fetched separately, and the remainder (15 kits —
7-Eleven-color Strike variants, Kirby, Naruto Uzumaki/Sasuke, both Dragon
Ball Super Saiyan God kits, both Ultraman kits, several more RX-78-2
recolors) are genuine redlinks with no page and no infobox data at all —
**left un-filed rather than guessed at**, the same "defer, don't
fabricate" policy MG/RG apply to missing dates. Revisit once the wiki
documents them.

**Images**: same `imageinfo` resolution + space/underscore normalization
as `../rg/CLAUDE.md` documents. One kit (`RX-78-2［US］ Gundam (American
Type)`) has a blank infobox `image` field — no packaging photo exists yet
— but its page's own "Stock Photos" gallery has product renders; used the
first one as a documented fallback rather than leaving the item imageless.

## Not everything shown is released — checked, none found this pass

Same check as `../rg/CLAUDE.md` (search full wikitext for "Under
Consideration"/rumor/cancelled markers) — clean this time, all 34 filed
kits are confirmed released.
