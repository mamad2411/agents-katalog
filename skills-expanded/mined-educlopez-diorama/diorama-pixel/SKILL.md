---
name: diorama-pixel
description: 'Build animated pixel-art miniatures: a small isometric place drawn at low resolution and enlarged crisp, with ordered dithering on every surface, procedural planks, thatch, paving, grass and water, a ground that dissolves into the white page, soft cast shadows and tiny people with a looping action. One self-contained HTML file with no dependency (no three.js, no WebGL): a software renderer on a 2D canvas, about 50 KB. Use it whenever someone asks for a pixel-art scene, a retro or 16-bit isometric vignette, a dithered illustration, or a cozy little place in pixels for a landing page, a blog post or a card. For vector UI illustrations, line art and empty states use the diorama skill; for detailed Three.js worlds with articulated people and four finishes use diorama-worlds.'
license: MIT
compatibility: Written for Claude Code; runs in any agent that reads skills. Needs Node.js 20+ for the build and checks, and Chrome or Chromium for the look.
metadata:
  opencode/slash: "true"
---

# Diorama Pixel: a pixel-art miniature that moves

You are making one small place, a stall, a pier, a garden plot or a doorway, seen from a fixed isometric camera and drawn as pixel art: the whole frame is rendered at 320 x 240 and enlarged with nearest-neighbour pixels, every surface is quantized to a short ramp of muted colours through an 8 x 8 Bayer matrix, the materials carry procedural texture (plank lines, thatch streaks, stones, stippled grass, blotchy water), the ground's edge dissolves into the white page, the sun throws soft shadows, and one or two tiny people do one clear thing in a loop. The three scenes in `examples/` are the bar, and they are in the format you will write.

This skill is one of three. `diorama` draws vector SVG illustrations (UI scenes, line art, empty states, themes); `diorama-worlds` renders detailed Three.js worlds with articulated people and four finishes. Use this one when the person wants pixels, dithering, a retro or 16-bit feel, or a pixel scene that must stay small and dependency-free.

You write one thing: the scene, a `.js` file. The kernel (`kit/pixel.js`) and the page (`kit/page.html`) are fixed. Never edit them, never paste a changed copy, and never write again what the kernel gives you (the camera, the light, shadows, textures, dithering, the ground, a person rig, trees and bushes, a clock that sleeps offscreen, the pointer).

Every file named below is in this skill's folder. Write the scene and the built page in the person's working directory, and run the scripts from there by their path in this folder.

## 1. Concept

Write the concept in one line before any code:

> **Name.** The place and what is in it. The one action a person does, and what else moves. What the pointer and a tap do.

Pick a place with a story and a use: a market stall, a jetty, a bakery door, an allotment, a bus stop, a rooftop garden. One action carries the scene (tying a bouquet, fishing, watering, kneading), with anticipation and a pause, and two or three quiet loops around it (cloth, water, leaves, a flag). Then write the parts list in four lines: **ground** (zones: grass, paving, water, sand, soil, a path), **structure** (what stands: a stall, a shed, a fence), **people** (who, where, facing where, doing what), **life** (what sways, bobs or shimmers). A scene runs to 10–25 objects. If the list reads thin, the scene will too.

Offer two or three concepts when there is someone to ask, and wait. If there is nobody to ask, take the one with the strongest still frame and say which.

## 2. Build

1. Read `references/art-direction.md`: palette, materials, dithering, the ground edge, the scale of people, what makes a frame read as a pixel miniature rather than a blurry render.
2. Read `references/scene-api.md`: every primitive, material, helper and the tick contract. Do not read `kit/pixel.js` below its index comment.
3. Read the nearest example: `examples/flower-stall.js` (paving and grass, a striped awning, two people, a pennant), `examples/pier.js` (water and a shore, a seated person with a rod, a boat, a thatched shed) or `examples/allotment.js` (soil, a brick path, raised beds, a gardener watering, a scarecrow).
4. Write `<name>.js`: one `Pixel.scene({ … })` with `name`, `title`, `means` (one sentence, at most 140 characters), `hint` (what to hover, what to tap), `duration`, `still`, `ground`, optional `materials`, `build(P)` returning `parts` (with `parts.hot`, each hot group named) and `tick(ctx)` posing everything from `ctx.t` / `ctx.q`.
5. Build: `node <skill>/scripts/build.mjs <name>.js` writes `pixel-<name>.html`, one self-contained page with no network request.

## 3. Check

1. `node <skill>/scripts/validate.mjs <name>.js pixel-<name>.html`: the declaration, the clock, self-containment, no URLs, the kernel byte for byte, the size budget and the pointer. Fix every `FAIL`.
2. `npm ci --ignore-scripts --prefix <skill>` once, then `node <skill>/scripts/look.mjs <name>.js <outdir>`. It opens the page in headless Chromium with the network blocked and writes `<name>-look.json`, the still, four moments of the loop, the hover, the press and a mobile view, and checks fill, motion, the loop seam, picking, hover, press, reduced motion, frame cost and mobile overflow. Frame cost is judged against the scene's frame budget (41.7 ms at 24 fps); `--throttle 4` looks at it on a CPU four times slower, as a CI runner or a phone. `CHROME_PATH` selects a browser; otherwise it uses an installed Chrome or Chromium.
3. **Open the PNGs and look.** Passing checks do not make a picture. Ask of the still: does the action read at this size (hands, the tool, the thing being worked on)? Is anyone hidden behind a post or a roof? Does every surface show its material? Does the ground fade into the page on every side, with nothing cut by the frame? Are the shadows on the ground where the sun says? Then fix the scene, not the kernel, and look again.

Do not hand over a page the validator rejects. Do not claim the look is done if you did not open the images. Without a browser, say so plainly and hand over with the look unverified.

## 4. Hand over

Give `pixel-<name>.html` the way the person asked (the file, or an artifact if you can publish one). Then, one line each: the concept; the still second and why; the size (about 50 KB, no dependency); how to embed it (`references/scene-api.md`, "Embedding": a `<canvas>`, the kernel and the scene in two `<script>` tags and `Pixel.mount`, or the React component there); anything you could not verify.

## 5. Adjust

When the person asks for a change, edit only `<name>.js`, build, validate and look again.

## What goes wrong

| If you catch yourself | Do this instead |
| --- | --- |
| reaching for three.js, WebGL or an image file | there is none: the kernel rasterizes solids on a 2D canvas; use `P.box`, `P.cyl`, `P.ball`, `P.wedge`, `P.line` |
| writing `requestAnimationFrame`, `setTimeout` or `Math.random` | pose everything from `ctx.t` / `ctx.q` in `tick`; use `P.hash(i, j)` for variety that stays put |
| `position.x += speed * dt` | a position from `P.phase(t, period)`, so the still frame and the loop seam are exact |
| a person hidden behind a counter, a post or a roof | move them, lower the counter, raise the roof: the camera is fixed and they are the story |
| arms that read as one blob with the body | a pose with the forearms out (`P.pose(p, 'work' / 'hold')`), the hands holding something with a colour of its own |
| a tree as one big ball | `P.tree` and `P.bush`: clusters of round-shaded leaf clumps |
| a flat colour on a big surface | a textured material: `'wood'`, `'thatch'`, `'stone'`, `'paving'`, `'leaf'`, `'cloth'`, or a ramp with `tex` |
| a hard edge where the ground ends | the ground is `ground: { rx, rz, wobble, fade }`: it already dissolves; never add a slab or a plinth |
| a scene wider than its ground | keep everything inside `rx` and `rz`; the frame fits the ground |
| more than 480 px of internal width | 320 x 240 is the look; more pixels look like a render, not pixel art |
| editing `kit/pixel.js` to make a scene work | the scene is wrong; change the scene |

## References

- `references/scene-api.md`: the declaration, `P` (primitives, materials, people, poses, trees, noise), the tick context and the pointer, the runtime and embedding.
- `references/art-direction.md`: palette and ramps, materials and textures, dithering, the ground edge, light and shadow, people at pixel scale, composition.
