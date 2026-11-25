---
name: wire-art
description: Draw Genex's canvas illustrations (loading, empty and being-made states) in its wireframe language - beam-scanned solids, flat marks extruded with depth, real tool logos - and explore them as rendered variants before code. Use when a surface needs a drawing, an icon with depth or a "making" state.
---

# Wire art

Genex draws its illustrations on canvas in one wireframe language: the empty states
(`ui/WireArt.tsx`, `ui/wire-computer.ts`), the welcome (`onboarding/ArtCanvas.tsx`) and the
Assets making cards (`making-shapes.ts`, `making-art.ts`, `panels/MakingArt.tsx`). Reuse those
modules before writing new geometry. The owner chose this language; keep it, don't restyle it.

## The look

- **Lines, not pictures.** Edges in a theme colour (an accent and ink mix, read from CSS),
  dimmed with depth, plus a faint nonzero fill of the faces for body. No gradients, no shadows,
  no photos, no emoji.
- **Small subjects.** A subject takes about half of its area and never crosses its edges or the
  card's chips and label. Prove the bounds in a unit test over every moment of the loop.
- **Real forms.** Solids are recognisable: a body scan of a person (level contours, believable
  proportions), the Utah teapot, cobblestones on a tilted plane for a texture. Offer several
  takes of a figure; the first one is rarely right.
- **Marks with depth.** A flat icon (image, video, sound, a vendor mark) is extruded into a few
  slices, brightest at the front, swaying slowly on its vertical axis: 2D with 3D. Keep it
  simple and rounded: an image is a rounded-corner picture, a video a rounded play shape, a
  sound a few waves. Vendor marks keep their own paths, unaltered.
- **One motion that means something.** A beam sweeps up and down the subject: below it is
  built, above it stays faint but visible. Waiting, failed or finished states are grey and
  still. Everything holds a still frame under Reduce Motion, when hidden, inert or off screen.
- **Tools by their logos.** Name the tool doing the work by its own mark on a small dark tile
  and its short name; never a borrowed mark for a plugin that ships none.

## Building one

1. Geometry is pure and deterministic: a function of `t` (seconds) that returns line segments
   and polygons in the art's own pixel box, with no DOM. Same `t`, same frame; `NaN` still draws.
2. Paint in alpha buckets (one stroke per bucket), glow only the brightest buckets with a small
   blur scaled to the backing store, and size the backing store to the shown size so canvas
   zoom stays sharp.
3. Loop at 30 fps through the `MakingArt`/`WireArt` loop: it already pauses for hidden documents,
   intersection, inert ancestors, `data-motion="rest"` and Reduce Motion. A rest frame never
   changes pose on a repaint.
4. Test in `tests/conformance/`: bounds at every moment, size, still frames, determinism.

## Designing one

Explore on the Design canvas before code: render several real variants per round (the actual
canvas drawing, not a sketch), publish every round to the canvas the owner is looking at, take
their notes, and implement only after they approve. Then check the rendered app in both themes
under `docs/agent/design.md`.
