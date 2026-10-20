# Elden Ring: The Road to the Erdtree — curation hints

## Directory structure

```
elden-ring-the-road-to-the-erdtree/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole ongoing series
  <number>-elden-ring-the-road-to-the-erdtree-vol-<number>.yaml
```

Flat, continuous numbering — no arcs/sub-series.

## Not to be confused with other Elden Ring manga

There are at least two other, distinct official Elden Ring manga series —
*Elden Ring: Become Lord* (a completed 2-volume full-color webcomic, no
English release found) and *Elden Ring: Distant Tales Between* (a newer
NPC-focused anthology series, English release from Yen Press starting
September 2026). **Neither is part of this series' numbering, and neither
is modeled here yet** — don't fold their volumes into this directory if
adding them later; give each its own directory under whichever publisher
holds its English license (`yen-press/` for *Distant Tales Between*).

## Publisher / licensor

Original Japanese serialization: Kadokawa, on the ComicWalker/Comic Hu
platform, since September 4, 2022. English-language licensor: Yen Press —
the only licensor so far (unlike The Electric Tale of Pikachu, this series
hasn't been relicensed, but it's ongoing — re-check this note if that ever
changes).

**Only the English Yen Press volumes are modeled here**, per this family's
en/US-market convention (see
[`comics-and-manga/CLAUDE.md`](../../CLAUDE.md)). As of this
writing the Japanese release is ahead of the English one — don't assume
they're in lockstep; confirm each volume's English release has actually
happened (not just been solicited/announced) before adding it. Volume 9
(announced English release: July 28, 2026) is not yet added for exactly
this reason as of 2026-07-19.

## Identifying items

Volumes carry no individual subtitle — just "Vol. N" — so `name` is
`"Elden Ring: The Road to the Erdtree, Vol. <N>"`, matching Yen Press' own
title format, and `attributes.number` carries the sequence number.

## Creator credits

Story and art: Nikiichi Tobita, based on FromSoftware, Inc.'s original
work — consistent across all volumes so far. **Letterer is not constant**:
Phil Christie lettered Vol. 1–3, Greg Deng took over from Vol. 4 onward
(Vol. 5 credits both). Confirm the letterer per volume from Yen Press'
own product page rather than assuming it carries over — this already
changed once. Translator (John Neal) has been constant throughout.

## Naming files

`<number>-elden-ring-the-road-to-the-erdtree-vol-<number>.yaml`, number
zero-padded to 2 digits — an ongoing series already at 8 volumes; 2 digits
is a judgment call based on current volume count, not a canonical width
(same reasoning as Monstress's issue numbering).

## Dates

Each volume's `date` is Yen Press' own English release date, sourced from
that volume's individual product page on yenpress.com (the series listing
page doesn't show per-volume dates) — not the earlier Japanese
serialization/tankōbon date.
