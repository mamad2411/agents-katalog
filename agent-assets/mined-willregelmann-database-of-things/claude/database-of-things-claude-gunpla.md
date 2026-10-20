# Gunpla — curation hints

## What belongs here

Bandai's Gundam plastic model kits ("Gunpla") — build-it-yourself kits of
mobile suits and related vehicles from the Gundam franchise, sold under a
small set of official **grades** that fix scale, engineering complexity, and
price tier.

This is one of Bandai's own branded lines, filed at `bandai/gunpla/` like
any other (see [`../CLAUDE.md`](../CLAUDE.md)). Being an assemble-it-
yourself kit doesn't put it anywhere different — it shapes how kits are
identified, which is what the grades below are for. A buildable Gundam that
ships as part of some *other* line stays with that line rather than being
re-filed here.

## Grades

Bandai's grades, oldest-to-current (verify against
[Bandai Hobby's own site](https://global.bandai-hobby.net/) or the
[Gunpla Wiki](https://gunpla.fandom.com/) before assuming a kit's grade —
don't infer it from box size or price alone):

- **PG (Perfect Grade)** — 1/60 scale, the most detailed and complex tier.
- **MG (Master Grade)** — 1/100 scale, full inner-frame skeleton.
- **RG (Real Grade)** — 1/144 scale like HG, but with MG-level inner-frame
  engineering.
- **HG (High Grade)** — 1/144 scale, the most prolific grade by far.
- **SD (Super Deformed)** — chibi-proportioned, non-scale.
- **EG (Entry Grade)** — introduced 2020, simplified beginner kits.

## Directory structure

```
gunpla/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "Gunpla" collection
  <grade>/                       # pg/, mg/, rg/, hg/, sd/, eg/
    _collection.yaml
    <sub-line>/                  # only where the grade splits into one — see below
      _collection.yaml
      <number>-<slugified-name>.yaml
    <number>-<slugified-name>.yaml   # kits directly under the grade when it has no sub-lines
```

**HG splits into many numbering sub-lines — don't treat it as one flat
checklist.** Unlike every other grade, High Grade has shipped under dozens
of distinct sub-brands tied to a specific Gundam timeline or sub-franchise,
each with its own independent kit numbering: `HGUC` (Universal Century, the
original and largest), `HGCE` (Cosmic Era/SEED), `HGIBO` (Iron-Blooded
Orphans), `HGBF` (Build Fighters), `HGAC`/`HGAW`/`HGFC`/`HGCC` (other
timelines folded into the "HG All Gundam Project"), and several more. A
kit's number is only unique *within* its own sub-line (e.g. HGUC #191 and
HGCE #191 are unrelated kits) — nest `hg/<sub-line>/` the same way Pokémon
TCG nests `<series>/<expansion>/` (see
[`../../../trading-cards/pokemon-tcg/CLAUDE.md`](../../../trading-cards/pokemon-tcg/CLAUDE.md)),
and confirm which sub-line a kit belongs to (Gunpla Wiki or the kit's own
box art, which prints the sub-line tag) before filing it.

**SD is messier still — several unrelated numbering sub-brands, not
necessarily one sub-line per box tag.** SD Gundam has shipped as BB Senshi,
SD Gundam Cross Silhouette, SD Gundam EX-Standard, and others over the
decades, each independently numbered. Don't assume `sd/` is flat, and don't
assume the HG sub-line pattern maps cleanly onto it — check each sub-brand's
own numbering before nesting.

**RG, MG, and PG use one continuous numbering per grade** as far as
confirmed so far (no timeline-based sub-lines the way HG has) — but verify
this holds before filing a kit flatly under `rg/`, `mg/`, or `pg/`, the same
"don't assume, check" bar as everything else in this category.

## Identifying items

A kit's official number (as printed on its box and in Bandai's own catalog)
is the primary identifier, scoped to its sub-line/grade the same way a
Pokémon card's `attributes.number` is scoped to its set. Record it as
`attributes.number` (a string — some sub-lines use letter prefixes, e.g.
`HGUC 191`, `RG 01`).

## Naming files

`<number>-<slugified-name>.yaml`, number zero-padded to the sub-line's own
digit width so far (3 digits covers every sub-line confirmed to date, e.g.
`191-rx-93-nu-gundam.yaml`) — widen if a sub-line's kit count ever exceeds
999, same rule as any other numbered collection (see the root
[`collections/CLAUDE.md`](../../../CLAUDE.md)).

**MG is the documented exception** — only about half its kits have a
sourceable lineup number, so it names files `<slugified-name>.yaml` and keeps
the number in `attributes.number` where known. See
[`mg/CLAUDE.md`](mg/CLAUDE.md) before applying the rule above to a grade whose
numbering you haven't checked; "one continuous numbering per grade" holds for
MG in principle but isn't fully recoverable from public sources.

## Attributes

See `item-attributes.schema.json`. `attributes.scale` should match the grade's
standard scale (e.g. `1/144` for HG/RG, `1/100` for MG, `1/60` for PG) except
for genuinely non-scale grades (SD, and some EG releases) — verify per kit
rather than assuming the grade's typical scale always applies, since a small
number of kits deviate (e.g. some MG kits are non-standard scale for
oversized subjects).
