# Bluey Fuzzies — curation hints

## Format

Soft, flocked-texture mini figures, roughly 1-2" tall — distinct from the
hard-plastic Mini Figures line (see
[`../mini-figures/CLAUDE.md`](../mini-figures/CLAUDE.md)). Sold as blind-bag
collectibles across several pack types:

- Single Pack (1 figure, blind)
- Surprise 2-Pack (2 figures, blind)
- Episode Pack (themed to a specific show episode, includes an
  episode-exclusive figure)
- Friends & Family Pack
- Deluxe Figure Pack (6 named figures + 2 blind mystery figures)
- Advent Calendar (24 daily figures)

Record the pack type as `attributes.pack_type`.

## Series 1 is an 80-figure collection — don't fabricate numbers

Series 1 comprises 80 figures total, tracked via an official Collector's
Guide (checklist) included in every pack and downloadable from bluey.tv.
**The guide's specific figure-to-number assignments are not reliably
published outside the physical/PDF guide itself** — don't invent or guess a
1-80 number for a figure. Only record `attributes.number` when you can
confirm it directly against the official Collector's Guide (or an equally
authoritative source); otherwise leave it off rather than guessing, per the
root [`collections/CLAUDE.md`](../../../../CLAUDE.md) approach to unconfirmed
precision.

## Naming and identifying figures

Identify by character name plus, where applicable, the episode/pack theme
that distinguishes a repeated character across releases (same disambiguation
approach as Re-Ment — see
[`../../../re-ment/CLAUDE.md`](../../../re-ment/CLAUDE.md) for the pattern). File
name is the slugified character (+ theme where needed), e.g. `bluey.yaml`,
`bluey-the-beach.yaml`.
