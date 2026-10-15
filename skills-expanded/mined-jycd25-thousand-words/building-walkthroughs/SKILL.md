---
name: building-walkthroughs
description: Use when the user wants an algorithm, protocol, or procedure explained step by step — a render_gui WALKTHROUGH-mode page with Prev/Next navigation, per-step notes, and highlighted cell grids
---

# Building Walkthroughs

Typical flow, two tool calls total: load the `render_gui` schema via
ToolSearch → write the spec → call the tool once. The tool description IS
the full grammar — trust it; this skill only adds walkthrough craft. A
success reply means done: do not read the output back or re-render.

Precompute every state once; the user steps through them locally. You are
replacing a hand-written visualizer that would cost thousands of tokens with
~20 tokens per step.

## Shape of a walkthrough page

1. One intro `text` saying what the walkthrough shows.
2. One `steps` node: `bind` holds the cursor, `states` is the full
   precomputed trace, one object per discrete step.
3. One or more views reading the broadcast fields: `cells` for
   arrays/grids, computed `text` for counters, `plot` when bars fit better.

```json
[
  { "type": "text", "value": "Bubble sort — the highlighted pair is being compared." },
  { "bind": "k", "states": [
    { "arr": [5,3,8], "j": 0, "note": "Pass 1 — compare 5 & 3: out of order, swap." },
    { "arr": [3,5,8], "j": 1, "note": "Compare 5 & 8: already in order, keep." },
    { "arr": [3,5,8], "j": -2, "note": "Sorted — nothing left to swap." }
  ] },
  { "cells": "arr", "highlights": { "accent": "j", "purple": "j+1" } }
]
```

## Craft the schema doesn't spell out

- **Compute the trace honestly** — run the algorithm in your head (or on
  paper) step by step; a wrong intermediate state teaches the wrong thing.
- **Narrate the decision** in each `note` ("out of order, swap"), not the
  array contents.
- **Park highlights out of range on the final state** (e.g. `"j": -2`):
  out-of-range indices highlight nothing.
- Highlight semantics: `accent` for the primary focus, `purple` for its
  partner, `green` for settled/done, `orange` for warnings/pivots.
- 5–30 steps is the sweet spot. Below that, a static diagram may serve
  better; far above it, summarize phases instead of every micro-step.
- Without MCP registered, render from the CLI:
  `node ${CLAUDE_PLUGIN_ROOT}/scripts/render-spec.js gui spec.json out.html`
