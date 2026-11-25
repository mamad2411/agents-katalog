# design/frontend — skill payload

> Machine-readable contract: [`../frontend-design.manifest.json`](../frontend-design.manifest.json).

## What this skill does

Generates React + Tailwind component code from a structured screen brief
(sections, copy, call-to-action). Output is TSX files keyed by component
name, ready to drop into a Next.js app under `app/` or `components/`.

Honours an optional `tokens` input (output of `design/theme-factory`) so
colours, type scale, spacing and radii flow through the generated code.

## When to use it

- You need a presentable landing page or internal-tool screen quickly.
- The visual style is set (you have tokens or a Tailwind config) and you
  just need scaffolded structure.

## When **not** to use it

- The work is a *design exploration* — generate variations in Figma
  first, then come back to scaffold the winner.
- The component must integrate with a non-React stack — output is React
  only.

## Determinism and risk

Determinism: **medium** — semantic structure is stable; class names and
copy phrasing vary. Risk: **low** — code only, reviewed before merge.

## How it composes

Most useful immediately downstream of `design/theme-factory` (token
input) and immediately upstream of `dev/webapp-testing` (smoke-test the
rendered screen in a real browser).
