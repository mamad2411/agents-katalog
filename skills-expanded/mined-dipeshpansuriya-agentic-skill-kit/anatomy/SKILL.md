---
name: anatomy
description: "Use when the user wants an idea explained as a live isometric machine drawing (HTML, SVG, or React). Not for ordinary diagrams (use archify) or marketing pages (use web-design)."
user-invocable: true
---

# Anatomy — idea as a working machine

This file is the whole skill. Do not fetch another owner's GitHub tree.

Build in the **code root** (Node 22+). No API keys. Source the user owns: a Node build script and the page it writes, or React geometry modules. Long session on purpose: invent, build, zoom every joint, then hand over.

## The object is the explanation

Do not draw boxes, arrows and labels. Invent a real machine whose working *is* the idea.

| Idea | Object |
|---|---|
| Cache key that skips work when nothing changed | Pin-tumbler lock: plug turns only when every pin matches |
| Message queue | Marble run: hoppers produce, a lane waits, drums consume |
| DNS resolution | Pneumatic tubes: capsule visits root, TLD, then the name |

Two failures: stacked plates (too abstract) or one bland slab (too flat). Fix: many small, precise, purposeful parts.

## Size before geometry

- **Figure** — one mechanism, 40–80 parts. Build it.
- **Hero** — dense object, 80–150 parts. Say 2–4 hours, then build unless he asked for quick.
- **Epic** — a plant or vehicle. Do not start; propose a Hero and wait for go.

## Workflow

1. Collect real numbers (sizes, counts, rates). Drive readout and motion from one small model.
2. Name the machine in one sentence: what moves, what that motion means.
3. Parts list ≥40, grouped: base, structure, mechanism, controls, subject (the one lit part). Each part sits on another.
4. World units ~1 px of the real thing. Camera azimuth ~45°, elevation ~30°. Centre the figure; it fills ~55–65% of a card.
5. Solids, not wireframes. Paint back-to-front. Tone: base `lo`, structure `mid`, subject `hi`, one accent `lit`.
6. Card: title, hint, live readout. Words stay off the drawing.
7. Calm motion (pointer + keyboard). Reduced-motion still.
8. Verify: desktop + phone (390 wide); every junction at 4×; no line that ends in empty air; nothing passing through anything.

## How to ask

```
/anatomy explain how [the mechanism] works, interactive
```

Copy-ready: Raptor on a test stand; message queue as a marble run; tokamak; CNC plasma cutter; DNS as pneumatic tubes; mechanical watch. Say HTML, SVG, or React; light or dark.

It draws machines, instruments, tools and furniture — not people or maps. Archify stays the architecture-diagram tool.

The developer builds it; it goes through normal review if it ships in a product repo.
