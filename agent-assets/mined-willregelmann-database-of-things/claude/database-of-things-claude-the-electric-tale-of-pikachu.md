# The Electric Tale of Pikachu — curation hints

## Directory structure

```
the-electric-tale-of-pikachu/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole 4-volume series
  <number>-<slugified-title>.yaml
```

Flat — a complete, closed series: 4 volumes, no arcs/sub-series to split
out.

## Publisher / licensor

Original Japanese serialization: Shogakukan, in *CoroCoro Comic* (April
1997 – December 1999), collected into 4 Japanese tankōbon (1997–2000). Sole
English-language licensor: Viz Media — no relicense has occurred, unlike
series that get picked up by a new publisher on reprint.

**Only the English Viz volumes are modeled here**, matching this family's
en/US-market convention (see
[`comics-and-manga/CLAUDE.md`](../../CLAUDE.md)) — Japanese volumes/ISBNs
aren't cataloged as separate entities.

## Known pitfall: this was originally released as single comic-book issues

Before the 4 paperback volumes modeled here existed, Viz released this
series in English as **16 individual monthly comic-book issues**
(November 1998 – February 2000), grouped into four same-named runs that
each became one of the eventual paperback volumes: *The Electric Tale of
Pikachu* #1–4, *Pikachu Shocks Back* #1–4, *Electric Pikachu Boogaloo*
#1–4, *Surf's Up, Pikachu* #1–4. Issue #1 was the best-selling comic in the
US at the time (over 1 million copies).

**Those individual issues are not modeled as separate entities.** This
family's chosen primary collectible unit is the tankōbon/paperback volume
(see [`comics-and-manga/CLAUDE.md`](../../CLAUDE.md)), and each paperback
volume's title already matches one of the four issue-runs it collects — so
don't add issue-level entities alongside the volumes, and don't confuse the
1998–2000 single-issue release dates with each volume's own (later)
paperback release date below.

## Identifying items

Each volume has its own distinct title — not just "Volume N" — so `name` is
that title (e.g. `Pikachu Shocks Back`), and `attributes.number` carries the
1–4 sequence.

## Creator credit

Toshihiro Ono wrote and illustrated the entire series himself — there's no
separate writer/artist split to track, so `attributes.creator` is a single
field rather than the writer/artist pair some other comics/manga series
use. Consistent across all 4 volumes; the series is complete, so this won't
change.

## Naming files

`<number>-<slugified-title>.yaml`, number un-padded (1–4 — a fixed,
4-volume series needs no zero-padding).

## Dates

Each volume's `date` is Viz's own English paperback release date (not the
1998–2000 single-issue dates, and not the earlier Japanese tankōbon date —
see "Known pitfall" above). Source: Bulbapedia's volume list, cross-checked
against Viz's own solicitation history.
