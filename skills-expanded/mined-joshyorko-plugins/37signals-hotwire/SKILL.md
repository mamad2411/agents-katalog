---
name: 37signals-hotwire
description: Use when designing, implementing, or reviewing Rails UI with Hotwire, Turbo, Stimulus, or server rendering.
---
## Source Grounding

Community-maintained and 37signals-inspired, not official Basecamp guidance.
Read `../../references/caveats.md`; installed Rails, Turbo, and Stimulus
versions win.

# 37signals Hotwire

Use this when the main question is frontend interaction shape inside a Rails app.
Bias toward useful HTML from the server, small Stimulus controllers, and fewer
client-side concepts until the product proves it needs more.

## Workflow

1. Start with the server-rendered screen and the user action.
2. Decide whether Turbo Drive, Frames, Streams, morphing, or plain HTML is enough.
3. Add Stimulus only for local DOM behavior the server should not own.
4. Keep authorization, validation, rendering, and persistence on the server unless
   the app already has a stronger frontend contract.
5. Check loading, empty, validation, permission, and stale-content states.

## Recipes

Use `../../references/recipes/hotwire-turbo.md` and
`../../references/recipes/hotwire-stimulus.md`. Pull in
`product-empty-states.md` and `product-copy.md` for screen-level decisions.

## Do Not Use For

- Generic UI critique without Rails/Hotwire: use `$37signals-product-design`.
- Full Rails feature sequencing: use `$37signals-rails-implement`.
- A requested non-Rails frontend architecture review: use the target repo's
  frontend conventions first, then explain tradeoffs.

## Output

Return the simplest Hotwire shape, accepted client-side complexity, recipes
used, and browser states that need verification.
