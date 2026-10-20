# Bluey Mini Figures — curation hints

## Format

Hard-plastic, highly poseable figures roughly 1" tall — distinct from the
soft flocked Fuzzies (see [`../fuzzies/CLAUDE.md`](../fuzzies/CLAUDE.md)) and
from the larger 2.5-3" Poseable Figures (see
[`../poseable-figures/CLAUDE.md`](../poseable-figures/CLAUDE.md)). Sold as
blind-bag mystery figures, either as a Single Pack or a Figure Case of 16.

## "S" labels are release waves, not a global number

Moose Toys labels each release wave with an `S`-prefixed code (`S6`, `S11`,
`S12`, `S13`, `S14`, `S15`, ...). **These are internal product-release wave
labels, not TV show seasons and not a sequential collector number** — don't
treat them as `attributes.number`. Record the wave as `attributes.series`
(e.g. `"S11"`), and don't assume the numbering is continuous or that gaps
(e.g. no S7-S10 confirmed) indicate missing curation — verify each wave
against an official listing before assuming it exists.

## Identifying figures

No printed catalog number exists on an individual figure. Identify by
character name within its release wave — the core roster confirmed so far is
Bluey, Bingo, Chilli, Bandit, Muffin, Socks, and the two grandparents
(Rita/"Granny Bingo" and Janet/"Granny Bluey"), but blind-bag waves
frequently add costume/pose variants of the same character — disambiguate
with a short descriptor the same way Re-Ment does (see
[`../../../re-ment/CLAUDE.md`](../../../re-ment/CLAUDE.md)).

## Naming files

`<slugified-character>[-variant-descriptor].yaml`, nested under its
`series/<wave>/` directory (e.g. `series/s11/bluey.yaml`).
