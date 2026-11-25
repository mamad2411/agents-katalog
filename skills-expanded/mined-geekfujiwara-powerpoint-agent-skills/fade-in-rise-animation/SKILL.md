---
name: fade-in-rise-animation
description: "Add a gentle automatic fade-in and upward entrance to selected PowerPoint content, staggered by position while keeping titles fixed. Use for sequential reveal or subtle motion. フェードイン、下からの入場、順次表示アニメーションに使用。"
license: MIT
---

# Fade-in Rise Animation

## Intended effect

- Start automatically on slide entry, without a click.
- Fade in over about 250 ms and rise over about 500 ms, starting together.
- Initial vertical offset: approximately 3.889% of slide height below the final
  position. The final position and slide layout must not change.
- Stagger eligible objects across **seven** delay levels: 0, 100, 200, 300,
  400, 500, and 600 ms.
- Keep titles, other placeholders, backgrounds, footers, and decorative elements
  fixed. Identify title roles from the layout and content, not the name "Title".

## Procedure

1. Confirm target slide numbers and direction: top-to-bottom by default, or
   left-to-right for flows/columns. Do not animate cover/divider slides unless
   specifically requested. Offer a fade-only or no-motion option when appropriate.
2. Inspect existing animations, triggers, builds, and media timing. Preserve them.
   If the requested effect requires replacing them, explain what would be lost
   and obtain explicit approval before replacing timing on those slides.
3. Use the supported PowerPoint animation tools when available. Do not assume
   a local Python runtime, slide XML access, or a particular internal tool exists.
   If the feature is unsupported, explain the limitation and give manual settings;
   do not pretend the effect was applied.
4. Select only substantive content objects. Keep a meaningful group as one object
   unless the user requests individual reveals. Avoid changing chart builds,
   SmartArt, media, or interactive elements unless supported and approved.
5. Compute each eligible object's delay from its top or left coordinate:
   `round((position - min)/(max - min) * 6) * 100 ms`.
   If all positions are equal, use zero delay. Break ties in reading order.
   Treat the eligible objects within the same card as one timing unit, using the
   card's top or left coordinate; give them the same delay. Stagger cards by
   position so their animations overlap.
6. Apply both effects concurrently for each object with the computed delay.
   Preserve the final geometry, editability, reading order, and existing transitions.
   If a faster effect is requested, durations and spacing can be adjusted, for
   example to a 150 ms fade, a 300 ms rise, and 120 ms between delay levels.
7. Play the edited slides in slide-show mode. Check automatic start, concurrent
   effects, timing, fixed titles, no unexpected clicks, and final placement.
   A static preview cannot verify animation playback. If playback is unavailable,
   report the effect as unverified, not as fully tested.

## Low-level editing boundary

If OOXML editing is explicitly available and necessary, work on a copy, preserve
unrelated timing and relationships, use valid unique timing IDs and target shape
IDs, and validate the package before opening it. Do not blindly replace `p:timing`
or reuse hard-coded slide numbers. A preset ID alone does not prove correct playback.

When OOXML editing meets that boundary, the established combination is:

- Fade: `presetID="10"` with `animEffect filter="fade"`.
- Rise: a separate motion path with `presetID="42"`, `presetClass="path"`,
  `decel="100000"`, and `animMotion origin="layout"`, using
  `path="M 0 0.03889 L 0 0 "` and `rCtr y="-1944"`.
- Use `withEffect` for both effects at the same calculated delay. Place the first
  effect in an `onBegin` container with zero delay so it starts automatically.
- For shapes containing text, use `grpId="0"` for the fade and `grpId="1"` for
  the motion. Add corresponding entries to `bldLst`:
  `<p:bldP spid=".." grpId="0" animBg="1"/>` and
  `<p:bldP spid=".." grpId="1" animBg="1"/>`, using the actual shape ID.
  Images and lines do not need `bldP` entries.
