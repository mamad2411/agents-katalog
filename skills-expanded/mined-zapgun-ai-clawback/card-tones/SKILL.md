---
name: card-tones
description: Render the clawback share card in BOTH tones (neg + pos) as a DESIGN render-only proof — NOT a benchmark result — so the share-card atmosphere (deep-purple LENS_CORE centre, win-only cyan corona, darkened gradients) can be eyeballed in one pass. neg uses a real run's amber regression card (purple core, no corona); pos is a SYNTHETIC fixture built only to exercise the renderer's win branch (purple core + cyan corona) — its number is fabricated, never published. Delegates to the shared preview_card.sh. Use when tweaking the share-card renderer's visuals and you want to see both tones side by side.
---

# clawback share-card tone proof

Run `.skills/card-tones/scripts/preview_card_tones.sh` from the project root.
It renders the share card in both tones so a renderer change can be eyeballed
in one pass. **Design proof only — neither card is a publishable result.**

```bash
.skills/card-tones/scripts/preview_card_tones.sh <neg-run-dir> <out-dir>
# e.g.
.skills/card-tones/scripts/preview_card_tones.sh runs/L0-headline-haiku /tmp/cardcheck
```

Writes `share_card.neg.{png,svg}` and `share_card.pos.{png,svg}` under
`<out-dir>`.

## The two cards

1. **neg** — a REAL run's amber regression card: the deep-purple core with the
   corona tone-gated OFF.
2. **pos** — a SYNTHETIC win card, built only to exercise the renderer's `pos`
   branch (purple core **plus** the faint cyan corona). It borrows the neg
   run's bare chart and carries a fabricated positive-token summary purely so
   the graph and lens-flare compose — the number is a render fixture, never a
   published metric. Staged in a temp dir and removed on exit.

## Depends on

The shared `.skills/scripts/preview_card.sh` (walks Chrome → `sips` →
SVG-only), which is the single card renderer the
[preview_card](../preview_card/SKILL.md) and [finish](../finish/SKILL.md)
skills also use.
