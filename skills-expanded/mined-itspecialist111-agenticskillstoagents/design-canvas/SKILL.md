# design/canvas — skill payload

> Machine-readable contract: [`../canvas-design.manifest.json`](../canvas-design.manifest.json).

## What this skill does

Renders a one-canvas visual (poster, social card, hero image, conference
slide) from a structured brief: background colour or image, headline,
body copy, optional imagery placement, palette. Emits SVG (source) and
PNG (preview).

## When to use it

- You need a single graphic — a launch announcement, an internal poster,
  a social card.
- The brief is closed (you know the copy and rough layout); you want
  consistent output without designer time.

## When **not** to use it

- The output is a multi-slide deck — use `office/pptx-toolkit`.
- The output is a *brand system* (logo, typeface, full guidelines) —
  this is a render, not a brand exercise.
- The visual needs to be editable in Figma — emit a `frontend-design`
  React preview or hand off to a designer.

## Determinism and risk

Determinism: **medium** — small style variations are possible.
Risk: **low** — visual output only.

## How it composes

Often downstream of `design/theme-factory` (uses its palette + type
scale) and `content/research-writer` (uses its headline / body copy).
