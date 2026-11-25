---
name: threejs-gpu-butterflies
description: Adds butterflies to a three.js meadow as one instanced draw call flown entirely in the vertex shader — each insect keeps a home flower, wanders out on two slow loops with a bobbing flight line, turns to face its own path derivative, beats its wings fast in the air and fans them slowly when it comes down to rest, with wing shape, dark border, pale dots and veins painted procedurally in the fragment shader; they fold away at night and in rain. Use when a nature scene feels static, when asked for butterflies, moths, ambient insects, small flying life, "make the meadow feel alive", or cheap ambient creatures with no per-frame CPU cost and no textures.
---

# GPU butterflies over a meadow

A flower meadow with wind in it still reads as a painting until something small crosses it on its own business.
Eighteen butterflies do that for one draw call and one shader program, with **nothing updated per frame on the
CPU**: position, heading and wing beat are all functions of time and a per-instance seed.

Stack: three.js `InstancedBufferGeometry` + `ShaderMaterial` (r150+), a shared `uTime` uniform. Works in R3F as a
`<mesh>` with the same geometry and material; no `useFrame` needed beyond the one that advances `uTime`.

## When to use

- A daytime meadow, garden or bank that already has flowers to anchor them to.
- You want ambient life but the frame budget is spent.
- Not for hero creatures seen close up for long: there is no body detail and no lighting response beyond a flap
  flicker.

## Paste-ready prompt

> Add `{{count: ~18, 8 on low-end devices}}` butterflies over `{{the flower meadow}}` in `{{entry file}}` as a
> single instanced mesh flown in the vertex shader: each has a home on a flower (collect positions while
> scattering the flowers), wanders within 1–2.6 m of it on two summed slow sine loops with a bobbing height,
> faces along its own path, beats its wings quickly in flight and comes down to rest on the flower now and then,
> fanning them slowly. Paint the wing in the fragment shader (two ellipses for fore and hind wing, dark border,
> pale dots, faint veins) in `{{4–5 tints}}`. Fade them out at night and in rain, hide them from the ambient
> occlusion and depth pre-passes, and cast no shadows.

## Implementation (`references/butterflies.js`)

### Geometry
- Three quads in one geometry: left wing, right wing (root on the body line along **x**, reaching out along ±z,
  `uv.y` = root → tip), and a thin dark body quad flagged with `uv.x = -1`.
- Storybook scale: wing 0.088 m out × 0.085 m along the body. True-to-life (3 cm) wings vanish at 5 m.
- Instanced attributes: `aHome` (xyz + seed in w), `aTint` (rgb). Homes are flower positions + 0.26–0.36 m, picked
  from flowers within 17 m of where the visitor stands.

### Flight, in the vertex shader
- Per-instance clock: `t = uTime·(.8 + .4·fract(s·3.7)) + s·50` — different speeds and phases, so no two are in step.
- `path(t, s)`: radius `R = 1.1 + 1.5·fract(s·7.31)`; x/z are two summed sines at unrelated rates
  (`.23` & `.71`, `.19` & `.63`); height `.5 + .32·sin(.37t) + .05·sin(6.3t)` — the fast term is the bob.
  A little `uWind` drift on top.
- **Resting:** `rest = smoothstep(.5, .86, sin(t·.13 + s·40))`; `mix(path, vec3(0), rest)` brings it down onto the
  home flower for a few seconds every ~48 s, each on its own schedule.
- **Heading** from the path itself: `d = path(t + .12) − path(t)`, `yaw = atan(d.z, d.x)`. No stored velocity.
- **Wings:** flap angle `a = mix(.2 + 1.05·sin(uTime·(11 + 4s)), .95 + .4·sin(uTime·1.7), rest)`; both wings lift
  about the body line: `p = vec3(p.x, |p.z|·sin a, p.z·cos a)`. Then rotate by yaw and add home + path.
- `uShow` scales the whole insect; ease it toward `(1 − night)·(1 − min(1, rain·3))` and hide the mesh under .02.

### The wing, in the fragment shader
- Silhouette = union of two ellipses in wing UV: the fore wing rotated ~20° forward, the hind wing shorter and
  behind; `discard` outside. Opaque + `discard` means depth writes and no sorting.
- `margin = smoothstep(-.17, -.03, d)` darkens toward the edge to 22 % of the tint; pale dots ride the border;
  faint veins from `sin(atan(p.x, p.y)·26)`; a lighter patch near the body.
- Unlit: `col · (.8 + .2·cos a)` so the wing flickers as it beats. In an HDR composer this needs no tone-mapping
  include.

## Pitfalls

- **Use two clocks for the wing beat.** Multiplying one time by a rate that depends on `rest` makes the phase jump
  whenever `rest` changes; mix the *results* of a fast sine and a slow sine instead.
- **Hide it from override-material passes.** An AO normal pass or depth pre-pass renders with its own material,
  which knows nothing of the vertex shader: every instance collapses to the geometry's origin and prints a dark
  speck there. Add the mesh to whatever list those passes hide.
- `frustumCulled = false` — the geometry's bounds are a 10 cm quad at the origin.
- Collect flower positions **without** drawing extra random numbers in the scatter loop, or every flower in the
  meadow moves. Give the butterflies their own seeded generator.
- A wide dark border (`-.3 … -.06`) with white wings reads as a grey blob at distance; keep the border thin.
- Storybook flowers are scaled up 1.5–2.6×; match the insects to them, not to nature.

## Verify

- Point a 30° lens at one home from 1.5 m: wing shape, border and dots readable; it comes down to rest and lifts
  off again.
- From the scene's opening view: movement visible over the flowers but never drawing the eye from the hero.
- Switch to night and to rain: they shrink away within a few seconds and return after.
- `renderer.info`: +1 draw call, +1 program. No dark speck at the world origin with AO on.

## References

- `references/butterflies.js` — geometry, instanced attributes, both shaders, and the show/hide step.

## Related skills

threejs-procedural-vegetation (the flowers they live on) · threejs-night-lights-lanterns (fireflies take over at
night) · threejs-webgl-rain-effect · threejs-fish-school-boids · threejs-postprocessing-anime-grade
