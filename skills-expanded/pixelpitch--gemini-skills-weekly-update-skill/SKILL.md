---
name: weekly-update
description: |
  Single-file horizontal-swipe slide deck for a weekly team update —
  shipped, in flight, blocked, metrics, asks. 6–8 slides. Use when the
  brief mentions "weekly update", "team update slides", "weekly status",
  "周报演示".
triggers:
  - "weekly update"
  - "team update slides"
  - "weekly status"
  - "weekly review"
  - "周报演示"
pixelpitch:
  mode: deck
  scenario: operations
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  example_prompt: "Make a weekly update deck for the Growth squad — what shipped, in flight, blocked, metrics, asks for next week."
---

# Weekly Update Deck Skill

Produce a single-file horizontal-swipe HTML deck for a weekly team update.

## Workflow

1. Read DESIGN.md.
2. Identify squad name, week range, and audience (squad-internal vs cross-functional).
3. Slides:
   1. Cover (squad + week + author + date)
   2. Headline (one sentence + one number that matters this week)
   3. What shipped (3–5 items, link-style affordance)
   4. In flight (3–5 items, owner avatars)
   5. Blocked (1–3 items + clear ask)
   6. Metrics that matter (1–2 inline charts)
   7. Asks for next week (named owners)
   8. Closing + thanks
4. Arrow keys or click navigation. Each slide is 100vw wide.

## Output contract

```
<artifact identifier="weekly-update-w42" type="text/html" title="Weekly Update — Growth · W42">
<!doctype html>...</artifact>
```

<!-- pixelpitch:slidify-aware -->
## Slidify-aware authoring (PPTX export)

This deck skill is part of pixelpitch's slide-designing system. The
HTML you author here is rendered live in the sandboxed iframe preview
and, when the user exports to PPTX, fed through `slidify` for a
maximally-editable PowerPoint file.

You don't need to change any of the design above to make slidify happy.
You can use `backdrop-filter`, `mix-blend-mode`, `<canvas>` heroes,
gradient text-clipping, and the full Tailwind / shadcn / Lucide stack.

There are **three free hints** that help slidify produce more editable
PPTX without changing a single pixel:

1. **Tag the slide title.** Add `data-pptx-role="title"` to the `<h1>`
   (or `<h2>`) you treat as the slide title. Slidify routes it to the
   master title placeholder and keeps it editable.
2. **Use atomic-seed atoms when one matches.** When your CSS happens to
   match a named recipe (`bg.mesh`, `type.gfill-4`, `data.ring`,
   etc.), tag the cluster anchor with `data-atom="<id>"`. Your CSS
   still runs in the browser unchanged; the hint just helps slidify
   pick the curated native recipe instead of guessing.
3. **Mark intentional bleed.** When a decorative element intentionally
   extends past the slide boundary (aurora glow, longshadow, marquee),
   tag the parent with `data-pptx-allow-overflow="true"`.

For irreducible effects (custom WebGL, complex masks), `data-pptx-rasterize="true"`
on the wrapper tells slidify to use a clean raster tile straight away
rather than discovering it.

Full guide: [`craft/slidify-compat.md`](../../craft/slidify-compat.md).
Atomic-seed grammar: [`slide-author`](../../.claude/skills/slide-author/SKILL.md)
sibling skill. Evolution loop (how slidify catches up to whatever this
skill emits): [`docs/slidify-evolution.md`](../../docs/slidify-evolution.md).

### Export

```bash
slidify convert deck.html out.pptx --json --report-json /tmp/r.json
slidify field /tmp/r.json native_area_ratio        # how editable the result is
slidify check deck.html                             # exit 0 ok / 3 = drift
```

Inside the pixelpitch web app, the daemon shells out to this same
`slidify` binary when the user clicks Export → PPTX.
