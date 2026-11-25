---
name: threejs-temporal-surfaces
description: Build screen-space temporal surface effects in Three.js. Use for full-resolution touch-history ping-pong, frost and thaw masks, reduced-resolution separable blur, static crystalline structure targets, and two-scale normal-map refraction.
---

# Temporal Surfaces

Use render-target state when the effect depends on history. Do not fake accumulation with a time-only procedural mask.

## Pipeline

```text
screen-space touch source
  → ping-pong state update
  → reduced-resolution scene blur
  → static structure textures
  → frost composite
  → normal/refraction output
```

Read [references/ping-pong-accumulation.md](references/ping-pong-accumulation.md)
for an exact frost pass graph, pointer-history channels, blur and refraction
coupling, and implementation defects that must be corrected.

Read the
[touch-history frost implementation](https://github.com/scottstts/Threejs-Awesome-Graphics-Agent-Skills/blob/31bf12e7b76b76a2650735e02d554a04fb2d2f8b/skills/threejs-temporal-surfaces/examples/touch-history-frost/frost-surface-effect.js) for the
previous/deposit/next state transition, reduced blur, static structures,
frost-mask composition, and two-scale refraction.

## Rules

- Separate persistent state from static noise and scene color.
- Preserve separate visible-mask and tilt-response channels.
- Use half-float for this history path unless a measured lower format is equivalent.
- Convert per-frame history decay to frame-rate-independent decay.
- Run the two-pass scene blur at reduced resolution.
- Pre-render static procedural textures once.
- Define and test resize/reset behavior for both history targets and static targets.
- Do not route world footprints, object-UV paint, or simulation-plane wetness here; this skill is screen-space.

## Routing boundary

Use `$threejs-procedural-vfx` for world- or object-space residue, particles, and
dissolves. Use `$threejs-precipitation-surfaces` for rain wetness, puddles,
snow accumulation, and weather-surface coupling. This skill owns screen-space
persistent history and its composite.


Source: Scott Sun, MIT. Adapted by LumosLab: example assets remain linked to pinned upstream source; skill instructions and references are bundled. See [LICENSE](LICENSE).
