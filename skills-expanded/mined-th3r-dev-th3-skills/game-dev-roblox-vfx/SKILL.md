---
name: game-dev-roblox-vfx
description: >-
  Build Roblox visual effects that look right and stay cheap: ParticleEmitter (parenting, the
  property stack, shapes, flipbooks), Beam, Trail and Highlight, a fill-rate budget, client-side
  playback driven by a server RemoteEvent, the power-ability recipe (press a key, rocks burst
  out of the ground, dust, hit applied on the server), and the anime-style look (one role per
  layer, flash/impact/residue timing, black silhouette layers, Brightness and Bloom, recolourable
  white templates, frozen-frame checks). Use WHENEVER the work is "Roblox VFX",
  "ParticleEmitter", "particles", "Emit", "flipbook", "Beam", "Trail", "Highlight", "fire", "smoke",
  "explosion", "impact", "aura", "awakening aura", "slash", "crescent", "shock ring", "impact
  frame", "black layer", "anime VFX", "recolor the effect", "effect washed out in daylight", "magic", "ability effect", "power", "skill effect", "rocks out of
  the ground", "ground slam", "shockwave", "fill rate", "overdraw", "laggy effects", "เอฟเฟกต์
  Roblox", "เอฟเฟกต์อนิเมะ", "ท่าไม้ตาย", or before adding any effect to a Roblox place.
---

# Roblox VFX

An effect is cheap to write and easy to get wrong: `Rate` and `Size` set blindly look flat and cost
fill rate. This file is the rules; property tables and recipes are in
[`references/particles.md`](references/particles.md), the ability code in
[`references/abilities.md`](references/abilities.md), the art direction in
[`references/look.md`](references/look.md). Set the project up first with
[`../roblox/SKILL.md`](../roblox/SKILL.md).

## Parenting

- Prefer an **Attachment**, and rotate it to aim. `EmissionDirection` only applies when the parent
  is a part.
- Sphere and Cylinder shapes render wrong under an Attachment. Parent those emitters to a tiny
  invisible part (`Transparency = 1`, `CanCollide`/`CanQuery`/`CanTouch` off).

## The visual stack, in order of impact

| # | Property | Rule |
|---|---|---|
| 1 | `Texture` | PNG with alpha, white or grey: colour comes from `Color`, so one template recolours. `LightEmission = 1` hides the dark areas but washes out in daylight |
| 2 | `Color` | a ColorSequence over the life, not one flat colour |
| 3 | `Size` | a NumberSequence; large = fill-rate cost |
| 4 | `Transparency` | always fade in and/or out, or particles pop |
| 5 | `Lifetime` | a range, not one number; capped at 20 s |
| 6 | `Rate` | caps ~400 desktop / ~100 mobile per emitter; reach density with 1-5 emitters, not Rate |

Then motion: `Speed`, `SpreadAngle`, `Acceleration` (gravity), `Drag` + `WindAffectsDrag`,
`VelocityInheritance`, `LockedToPart`, `TimeScale`. Shapes, flipbooks, `Orientation` and `ZOffset`:
[`references/particles.md`](references/particles.md).

## Look

How it reads matters as much as what it costs. Full guide: [`references/look.md`](references/look.md).

- **One role per emitter**: flash, rings and crescents (`VelocityPerpendicular`, the main shape),
  sparks (`VelocityParallel`), debris and smoke, a **black layer** with the same texture that
  keeps the silhouette readable in daylight.
- **Three stages**: flash up to 0.1 s, impact to 0.4 s, residue 0.5-4 s, set per emitter with the
  `EmitDelay` attribute.
- **Light**: `LightInfluence = 0`; 1-2 core layers bright enough to bloom, coloured layers at a
  moderate `Brightness`, black layers at 0. Test with the game's Bloom, in daylight.
- **Size eases out**; high `Speed` with high `Drag` makes a punch.
- **White templates, tinted per element**; tag black layers and white flashes `NoColor`.

## Budget: fill rate and overdraw

Cost is roughly `Rate × Size × opacity × overlap`. Shrink `Size` and pixel overlap before `Rate`.

- Measure: Studio **View → Stats → GPU → Fill Rate**, and **Render → Overdraw**.
- Test at the lowest and the highest quality level. Low-end devices drop flipbooks and throttle.
- `Enabled = false` only stops new particles; `:Clear()` removes the live ones.

## Replication

An emitter's state replicates; single particles do not. For a burst:

1. The **server decides that** the effect happened and fires `FireAllClients(effectId, cframe)`.
2. **Each client builds and plays** it, so it can skip or thin it by distance and quality.
3. Cooldown, range and damage stay on the server.

## Pipeline hygiene

| Concern | Rule |
|---|---|
| LOD / culling | skip or halve effects past ~100-300 studs from `workspace.CurrentCamera`; check at play time, not per frame |
| Preload | `ContentProvider:PreloadAsync` the flipbook atlases and key textures before the first use |
| Cleanup | a one-shot clone is destroyed after its longest `Lifetime.Max` (`Debris` or `task.delay`); never leave disabled emitters in `workspace` |
| Reparenting | `Enabled = false` and `:Clear()` first |
| Pooling | reset `Rate`, `Lifetime`, `Size`, `Transparency`, `Color` to the template before reuse |
| Templates | clone, never mutate: a shared emitter changed mid-burst breaks the next burst |

## Beam, Trail, Highlight

| Class | What it is | Key properties |
|---|---|---|
| Beam | textured ribbon between two Attachments (laser, energy, rope) | `Texture`, `TextureMode`, `TextureLength`, `TextureSpeed`, `Color`, `Transparency` (sequence along it), `Width0`/`Width1`, `CurveSize0`/`CurveSize1`, `FaceCamera`, `LightEmission`, `ZOffset` |
| Trail | ribbon left behind two Attachments on a moving part (sword, projectile) | `Color`, `Transparency`, `Texture`, `TextureMode`, `Lifetime`, `MinLength`, `MaxLength`, `WidthScale`, `FaceCamera`, `LightEmission` |
| Highlight | outline + fill on an instance (target, selected, powered up) | `FillColor`/`FillTransparency`, `OutlineColor`/`OutlineTransparency`, `DepthMode` (`AlwaysOnTop` or `Occluded`). **255 per client**; disabled ones count |

## Ability recipe: "press a key, rocks burst out of the ground"

From the DevForum thread: put the part underground and move it up. The thread's `BodyVelocity` is
legacy: use a `LinearVelocity` (or another constraint) for a part that must collide, or a
`TweenService` CFrame tween for a purely visual rise (the default here).

1. **Client** reads the key (`UserInputService`, ignore `gameProcessedEvent`) and fires a
   `RemoteEvent` with the ability id only.
2. **Server** checks the type, the per-player cooldown, that the character is alive, and range,
   then applies the hit itself (`GetPartBoundsInRadius`, `TakeDamage`).
3. **Server** calls `FireAllClients(abilityId, root.CFrame)`.
4. **Client VFX factory** builds the effect from a frozen definition and plays it:
   - rocks cloned below ground at `root.CFrame * CFrame.new(0, -h, -dist)`, in an arc;
   - a `TweenService` rise (anchored, `CanCollide = false`, visual copies only);
   - a `ParticleEmitter` burst for dust;
   - hold, then sink or fade, then destroy (`Debris` or `task.delay`).

Code: [`references/abilities.md`](references/abilities.md). Never use `BodyVelocity`,
`BodyPosition` or the other legacy BodyMovers, the global `wait`/`spawn`/`delay` (use `task.*`), or
`Humanoid:LoadAnimation`.

## Check

A visual change is not done until it was run and looked at, with the MCP setup from
[`../roblox/SKILL.md`](../roblox/SKILL.md):

1. `start_stop_play`, then trigger the effect (`user_keyboard_input`).
2. `screen_capture` at the **lowest** and the **highest** quality level. Capture lags ~1-2 s, so
   for a burst freeze it first (`TimeScale = 0` on every emitter) at the flash, the impact and the
   residue ([`references/look.md`](references/look.md)). Look in daylight and with one other tint.
3. `get_console_output`: no errors or warnings from the effect's code.
4. The Fill Rate stat while it plays.
5. `start_stop_play` to stop.

A check that could not run (Studio closed, MCP off, no key press possible) is **NOT ASSESSED**,
never a pass.

## Where it fits

| Folder | Holds |
|---|---|
| `src/shared/` | the frozen definitions table (`VfxDefinitions`); no `game` |
| `src/client/` | the factory, the effect classes, the input and the `OnClientEvent` hook |
| `src/server/` | the one Script: cooldown, range, hit, `FireAllClients` |

Templates (emitters, the rock part) live under `ReplicatedStorage.VfxTemplates`, made in Studio.
Luau style, classes and the review checklist:
[`../roblox/references/luau.md`](../roblox/references/luau.md).

## Credits

Adapted from [nonlooped/roblox-suite@fc1c3dd](https://github.com/nonlooped/roblox-suite/tree/fc1c3dd26fef67ee4d7b6e20b1299b44fc6101ae/roblox-vfx)
(MIT, © 2026 nonlooped) and the DevForum thread
[Roblox VFX and power abilities](https://devforum.roblox.com/t/roblox-vfx-and-power-abilities/1537223).
The look is based on lef's **Roblox VFX Design** guide,
[Wongsakorn-krub/SKILL_AI_VFXROBLOX@7d42130](https://github.com/Wongsakorn-krub/SKILL_AI_VFXROBLOX/tree/7d4213017038899d895374cf0f59801fc957af84)
(no licence stated: linked and restated, not copied).
