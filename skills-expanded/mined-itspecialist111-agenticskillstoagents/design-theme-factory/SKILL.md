# design/theme-factory — skill payload

> Machine-readable contract: [`../theme-factory.manifest.json`](../theme-factory.manifest.json).

## What this skill does

Generates a coherent UI theme as design tokens (colour ramp, type scale,
spacing, radii) from a minimal brief: brand name, vibe words, primary
colour. Output is a JSON document compatible with the design-tokens
community spec, plus a preview swatch.

The tokens are framework-agnostic; downstream skills (or humans) map
them into Tailwind, MUI, CSS variables, or design-system source.

## When to use it

- You're starting a new product/internal-tool and need a defensible
  visual baseline in minutes.
- You have a brand colour and want a full ramp + complements that pass
  contrast checks.

## When **not** to use it

- The product already has a design system — don't fork it.
- The brand needs human design judgement (consumer-facing, regulated) —
  treat this as a starting point only.

## Determinism and risk

Determinism: **medium** — minor variations between runs. Risk: **low**.

## How it composes

Direct upstream of `design/frontend` (consumes its tokens) and
`design/canvas` (uses its palette).
