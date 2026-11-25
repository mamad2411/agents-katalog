---
name: thermal-finger-trail
description: Build an interactive heat-camera field that a finger or cursor smears like wet paint — a WebGL fragment shader with a domain-warped thermal blob, a seven-stop heat ramp, a velocity-carrying pointer trail, and a press ripple. Use when the user wants a thermal/heatmap effect, a "finger through paint" or smudge interaction, a living gradient that reacts to touch, a trackpad/touch-surface hero, or the Clicker disc effect. Also use for any reactive shader field driven by a pointer trail.
---

# Thermal Finger Trail

Use this skill to build a surface that looks like a thermal camera and responds to touch like wet paint: drag a finger across it and the heat field is dragged along with it, then slowly heals. Press, and a ripple pushes the colour outward and briefly heats it.

It comes from Clicker's trackpad disc (an iPhone app that turns the phone into a trackpad). On the site, the disc *is* the product: the place your finger goes.

![Clicker's thermal disc, mid-smear](assets/thermal-finger-trail-reference.png)

The complete working version is `references/thermal-finger-trail.html`: one file, no build step, with a DialKit tuning panel. Start from it rather than from scratch.

## When it fits

- A touch or pointer surface that should feel physical: a trackpad, a canvas, a hero object people want to play with.
- A brand that can carry a heat-camera palette (teal → green → yellow → orange → red).
- One focal object on a dark ground. It's a show-piece, not a background behind body copy: the field is busy and the contrast shifts constantly.

Don't put text over it, and don't run it full-screen on a page that also needs to scroll smoothly on low-end phones without the DPR cap below.

## How it works

Everything is one fragment shader on a single full-canvas triangle. There are no textures, no render targets and no feedback buffers: the "memory" of the finger is a short list of points passed in as uniforms each frame.

1. **The field.** Fractal noise (`fbm`, 5 octaves) warps the coordinates, and a second fbm, fed by the first, warps them again ("warp the warp"). That gives curling, fluid flow. A slow *melt* cycle (6 s) swells the warp and slumps the shape downward, then recovers.
2. **The blob.** In the warped space, a soft blob breathes between round and a touch tall or wide: a polar wobble of two low-frequency sines. Distance from its edge gives two values: `mask` (inside or outside) and `inside` (how deep).
3. **Heat.** Heat is a number from 0 to 1. Outside the blob it's a warm, noisy background (0.34–0.66, never white, never dark). Inside, it ramps from a cool core (0.20) to a hot rim (0.64). A hard contour is cut where green meets yellow, so the core reads crisp.
4. **Colour.** `thermal(heat)` maps heat through seven stops with `smoothstep` blends at 0, .12, .30, .45, .60, .78 and 1. Heat is capped at 0.75, so the field tops out at orange or red and never blows out to white.
5. **The finger.** JavaScript keeps the last 24 points of the pointer's path. Each holds a position, its **velocity** (the step from the previous point) and an **age** that fades from 1 to 0 over 1.6 s. In the shader, every point within reach pushes the coordinates along its own velocity:

   ```glsl
   vec2 disp = vec2(0.0);
   for (int i = 0; i < 24; i++) {
     float age = uTrailA[i];
     if (age <= 0.001) continue;
     disp += uTrail[i].zw * smoothstep(uRadius, 0.0, length(uv - uTrail[i].xy)) * age;
   }
   vec2 fuv = uv + disp * 9.0 + clickRipple;   // everything after this samples fuv
   ```

   That one line is the effect. The field is sampled from *where the finger came from*, so the colour appears dragged along the path, and it relaxes back as each point ages out.
6. **The press.** A ring expands from the press point for 0.9 s. It shoves coordinates outward (`clickD`) and adds heat along the ring, so the field blooms toward its own warm colours.
7. **The edge.** By default the blob's silhouette is razor-crisp. On an irregular cadence (two detuned sines), a soft blur front sweeps across the disc from a slowly rotating direction, then recedes. On top sit a thin specular rim inside the edge and a warm halo just outside it.

The JavaScript is small. Ease a *head* toward the raw pointer (30% per frame), so the trail is smooth even when pointer events are sparse. Lay a new trail point only after the head has moved a set distance (1% of the field), not on a timer. Upload the 24 points and their ages every frame.

```js
head.x += (target.x - head.x) * 0.3;
head.y += (target.y - head.y) * 0.3;
const [gx, gy] = toField(head.x, head.y);           // centred, y up, x scaled by aspect
const last = trail[trail.length - 1];
if (!last || Math.hypot(gx - last.x, gy - last.y) > 0.01)
  trail.push({ x: gx, y: gy, vx: last ? gx - last.x : 0, vy: last ? gy - last.y : 0, born: t });
while (trail.length && t - trail[0].born > 1.6) trail.shift();
```

## Tuning

Every constant is a control in the reference file's DialKit panel. These are the original values:

| Control | Default | What it does |
|---|---|---|
| `smudge` | 9 | How far the trail drags the field. Higher means more paint-like. Above about 14, fast strokes tear holes. |
| `radius` | 0.17 | Reach of each trail point, in field units (the field is about 1 wide). |
| `follow` | 0.3 | How fast the head eases to the finger per frame. Lower gives lazier, smoother strokes. |
| `spacing` | 0.01 | Distance before a new point is laid. Smaller means more, shorter steps. |
| `life` | 1.6 s | How long a stroke keeps pulling before the field heals. |
| `points` | 24 | Trail length. The shader's array holds 24. |
| `flow` | 0.26 | Speed of the noise flow. |
| `meltSeconds` | 6 | Length of one slump-and-recover cycle. |
| `warp` | 1 | Strength of the curling warp (0 gives a still, smooth blob). |
| `blob` | 0.37 | Radius of the hot blob. |
| `blurWash` | on | The soft blur front that sweeps across. Off keeps the edge crisp. |
| `heatCap` | 0.75 | The hottest the field gets. 0.75 stops at orange or red; 1 allows white-hot. |
| `ripple` / `bloom` / `duration` | 0.18 / 0.55 / 0.9 s | The press: outward shove, added heat, and how long the ring lives. |
| `rim` / `halo` | 0.6 / 0.45 | The crisp inner rim and the warm outer fringe. |
| Palette | 7 colours | The ramp: cold, deep, green, yellow, orange, red, white. Swap these for a brand's heat ramp. |

To retheme it, change the palette, not the heat values. The shape of the field comes from the heat numbers, and the colours are only a lookup.

## Porting

- **Vanilla / any framework.** Lift `FS`, the trail code and the uniform upload from the reference file. Nothing in it is framework-specific.
- **React / Next.js.** Use a client component. Create the context in `useEffect` on a canvas ref, keep the trail and head in refs (not state), and run the loop with `requestAnimationFrame`. Clean up the rAF, the listeners and the `IntersectionObserver` on unmount. The DialKit panel becomes `useDialKit(name, config)` from `dialkit` (React).
- **Three.js / R3F.** Use a `ShaderMaterial` on a plane, with the same uniforms. Update `uTrail` (an array of `Vector4`) and `uTrailA` in `useFrame`. With R3F, the pointer comes from the mesh's `onPointerMove` UV: convert it to the shader's centred, y-up, aspect-scaled space.

## Get these right

- **Field coordinates.** The shader's `uv` is centred, y up, with x multiplied by the aspect ratio. Convert pointer positions the same way, `[(x/W − 0.5)·(W/H), 0.5 − y/H]`, or the trail lands in the wrong place on anything that isn't square.
- **Sample by distance, not time.** Sampling on a timer bunches points when the finger is slow and spaces them out when it's fast. Velocity is the step between points, so evenly spaced samples give even smears.
- **Ease the head.** Raw pointer events arrive unevenly, especially from touch and synthetic drags. Without the ease, fast strokes make one huge velocity step, and that tears a hard-edged hole in the field.
- **GLSL ES 1.0 loop bounds** must be constants. Keep the array at 24 and switch unused points off with age 0.
- **Cost.** About 30 noise evaluations per pixel. Cap the device pixel ratio at 2 for a disc and about 1.25 for full-bleed, and pause the loop when the field is offscreen (`IntersectionObserver`) or the tab is hidden.
- **Touch.** Put `touch-action: none` on the surface so a drag paints instead of scrolling the page. Use pointer events, so one code path covers mouse, pen and touch.
- **Reduced motion.** Freeze the clock at a good-looking moment. The field then holds still and only the finger moves it, and the loop runs only while it's being touched.
- **No WebGL.** Fall back to a static radial gradient in the same palette.

## Making it yours

- Swap the palette for a brand's own ramp. Keep it running from dark to light, so heat reads as brightness.
- Change the *subject*. The blob is one shape. The same trail displacement works on any field the shader paints: a logo's distance field, a photo sampled as a texture, or type rendered into a texture.
- For a smaller focal object, put it inside a circle. A canvas with `border-radius: 50%` gives a crisp mask without any shader work.
