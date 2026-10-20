# MG (Master Grade) — curation hints

Bandai's 1/100 Master Grade kit line, running continuously since 1995. Flat —
one directory, one file per kit, no sub-grouping. Everything else follows
[`../CLAUDE.md`](../CLAUDE.md) except the two deviations below.

## Naming files: no number prefix

**Files are `<slugified-name>.yaml`, not `<number>-<slugified-name>.yaml`** —
the one place this line departs from its parent.

`../CLAUDE.md` makes a kit's official number the primary identifier and
zero-pads it into the filename, which works for HGUC and RG. MG can't follow
it: **only about half of MG kits have a documented lineup number** (154 of 285
as catalogued). Prefixing the numbered half and not the rest would produce a
directory that sorts in two disjoint groups and reads as a data error rather
than a real gap.

The number is still recorded as `attributes.number` wherever it's known, so
nothing is lost — it just doesn't drive the filename. See
[`../../../../CLAUDE.md`](../../../../CLAUDE.md), which allows
`<slugified-name>.yaml` for collections without canonical numbering.

**Don't source the missing numbers from Dalong.net.** Its "M###" catalog is
the only bulk MG numbering easily found, and it does not match Bandai's own:
its M100 is Strike Noir, while Turn A Gundam — independently marketed as MG
#100 — doesn't appear in its M001–M226 list at all. Using it would silently
corrupt both `attributes.number` and any filename derived from it.

## Scale: verify, don't assume

MG is a 1/100 line and 280 of 285 kits are 1/100 — but **the exceptions are
real**, so take `attributes.scale` from the kit rather than the grade:

- `1/144` — RGM-79 GM (1999), ZGMF-X12A Testament Gundam, and the Ver. 2.0
  Shin Matsunaga Zaku II
- `1/8` — MG Figure-rise Kamen Rider 1

That last one is also the reminder that **MG is not a Gundam-only line.**
Bandai has used the Master Grade brand for other properties, so don't filter
candidates by whether they're mobile suits. Expansion and add-on kits
(weapon packs, unit upgrades sold separately) carry the MG brand too and
belong here.

## Dates

199 of 285 kits have a sourced release date, at whatever precision the wiki
gives — full date, month, or year. **86 have none**, because Gunpla Wiki
defers those to a per-kit "Release Dates" section rather than an infobox
field. Those carry no `date` rather than a guessed one; filling them means
parsing that section per kit, which is a worthwhile follow-up.

## Sourcing

[Gunpla Wiki](https://gunpla.fandom.com/) is the working source, with two
traps worth knowing before you start.

**Its rendered pages return HTTP 402, but its MediaWiki API doesn't.** Use
`curl` with a browser user-agent — the same technique
[`../../../../plush/squishmallows/CLAUDE.md`](../../../../plush/squishmallows/CLAUDE.md)
documents for other Fandom wikis. A previous audit pass concluded this wiki
was unreachable because it tested the page rather than the API.

```bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
# the authoritative kit list
curl -s -A "$UA" "https://gunpla.fandom.com/api.php?action=query&list=categorymembers&cmtitle=Category:Master%20Grade&cmlimit=500&cmnamespace=0&format=json"
# kit pages, 25 at a time
curl -s -A "$UA" "https://gunpla.fandom.com/api.php?action=query&prop=revisions&rvprop=content&rvslots=main&format=json&titles=A|B|C"
```

**Use `Category:Master Grade`, not the Master Grade page's Lineup gallery.**
The gallery looks like the obvious list and isn't: several of its links are
red links to pages that don't exist, some omit the `(year)` disambiguator the
real page title carries, and **Ver.Ka and MGEX kits appear twice** — once in
their release-year tab and again in a dedicated section further down. Parsing
it section-blind yields 251 entries for 225 distinct kits. The category is
clean and complete (286 pages).

**The infobox template name varies.** Kit pages use `Plamo Infobox`,
`Plamo_Infobox` *or* `Gunpla_Infobox`, and matching only one form silently
drops a third of the line. Fields worth reading: `Lineup no.`, `Scale`,
`Release Date`, `Classification`, `Franchise`, `Price`, `JAN/ISBN`. Parse with
brace matching rather than a non-greedy regex — the infobox contains nested
templates and links, and a lazy `.+?}}` truncates it.

## Images

283 of 285 kits carry `image`, backfilled from the same Gunpla Wiki
infoboxes as everything else here — resolved via the `imageinfo` API
endpoint and normalized for the space/underscore inconsistency documented
in [`../rg/CLAUDE.md`](../rg/CLAUDE.md). 7 kits had no infobox `image` at
all but did have a "Stock Photos" gallery further down the page; used the
first stock photo as a documented fallback rather than leaving them
imageless, same as [`../eg/CLAUDE.md`](../eg/CLAUDE.md)'s American Type
kit. **Two kits have no image anywhere on their page and stay
imageless**: `Bazooka for Aile Strike Gundam` (empty gallery entirely) and
`RX-78-2 Gundam (10th Anniversary Model)` (both Packaging and Stock
Photos galleries present but empty).

**One real kit is still missing from this directory, found while
resolving images, not yet filed**: `MG MBF-02+EW454F Strike Rouge +
Ootori (Ver. RM)` (Lineup no. 173) exists on the wiki with real data but
uses a fourth infobox template spelling this repo hasn't accounted for —
`{{Template:Plamo Infobox|...}}`, the literal `Template:` namespace
prefix inside the braces, distinct from the `Plamo Infobox` /
`Plamo_Infobox` / `Gunpla_Infobox` variants already documented above.
Worth filing as its own follow-up.

## Not yet recorded

`Price` and `JAN/ISBN` are available on most kit pages and aren't captured —
`attributes` here is deliberately minimal (see the root
[`CLAUDE.md`](../../../../../CLAUDE.md), "minimal metadata by design"). Add
them only if there's a real use for them, not because the source has them.
