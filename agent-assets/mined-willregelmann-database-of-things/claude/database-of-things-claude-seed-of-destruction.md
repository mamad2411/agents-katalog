# Hellboy: Seed of Destruction — curation hints

## Directory structure

```
seed-of-destruction/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # this mini-series
  <number>-hellboy-seed-of-destruction-<number>.yaml
```

Self-contained 4-issue mini-series (March–June 1994) — the first Hellboy
story, plotted and drawn by Mike Mignola and scripted by John Byrne.
**Hellboy is not one continuously-numbered ongoing** — each subsequent
mini-series/one-shot (Wake the Devil, The Chained Coffin and Others, The
Right Hand of Doom, etc.) restarts its own numbering, so each one gets its
own sibling directory under [`hellboy/`](../_collection.yaml) rather than
being mixed into this one's 1–4 sequence. See
[`comics-and-manga/CLAUDE.md`](../../../CLAUDE.md) for the general publisher/series
shape this deviates from, and follow this directory as the worked example
for other Hellboy mini-series.

**Pre-1994 Hellboy cameos are a known gap, not yet catalogued**: a 1993
Italy-only appearance in *Dime Press* #4, a first color/named appearance in
John Byrne's *Next Men* #21 (Dec 1993), and a 4-page promo piece in *San
Diego Comic-Con Comics* #2 (Aug 1993). None of these are Hellboy-titled
books — they're cameos inside other publishers'/creators' titles — so they
don't fit cleanly under `hellboy/` and are left for a future call on how
(or whether) to model them, rather than force-fit here.

## Identifying items

Issues are identified by number within this mini-series only; `name` is
`"Hellboy: Seed of Destruction #<N>"`.

## Naming files

`<number>-hellboy-seed-of-destruction-<number>.yaml`, number **not**
zero-padded — the mini-series only ever ran 4 issues, so there's no
ordering benefit to padding (same reasoning as Monstress's per-series
digit-width judgment call, applied at the low end).

## Release dates

Dark Horse's own site gives on-sale dates as the 1st of each month,
monthly cadence March–June 1994 — used directly. Grand Comics Database
(comics.org) returned HTTP 403 on direct fetch during seeding, so dates
weren't independently cross-checked against it; treat as a lower-confidence
sourcing gap if a discrepancy ever turns up.

## Creative team

Mike Mignola (plot/pencils/cover) and John Byrne (script) are credited
across all 4 issues; Mark Chiarello colors; Barbara Kesel edits. A
`letterer` field was deliberately left out of the schema — the lettering
credit for this series wasn't cleanly sourced during seeding.

## Common pitfalls

- Don't confuse this 1994 mini-series with the 2004 movie tie-in
  materials or the "Seed of Destruction" collected-edition trade — the
  entities here are the original single issues.
