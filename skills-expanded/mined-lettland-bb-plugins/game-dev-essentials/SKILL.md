---
name: game-dev-essentials
description: Use when designing engine-agnostic game systems — ECS vs OOP, state machines vs behavior trees, fixed timestep, asset pipelines, physics, audio.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [godot, gdscript]
---

# Game Dev Essentials (Engine-Agnostic)

**Iron Law: fixed timestep for physics, variable for render. State machines for any non-trivial entity state. Pool what you spawn often.**

## ECS vs OOP

|                | ECS                                                      | OOP / scene-tree                         |
| -------------- | -------------------------------------------------------- | ---------------------------------------- |
| Identity       | Bare ID                                                  | Object / node                            |
| State          | Components (plain data) on entity                        | Fields on object                         |
| Behavior       | Systems iterate component queries                        | Methods on object                        |
| Cache locality | High (component arrays)                                  | Low (heap-scattered)                     |
| Composition    | Add `Stunned` → entity is stunned                        | Subclass or mixin                        |
| Best for       | 1000+ similar entities (bullets, swarms, RTS, particles) | Bosses, varied logic, scene-tree engines |

**Rule of thumb:** 1000+ similar entities → consider ECS. Otherwise scenes/objects.

**Hybrid wins for most projects:** 99% scenes, one hot system array-based — 10,000 bullets as packed arrays, not nodes:

```pseudo
positions:  PackedVector2Array
velocities: PackedVector2Array
lifetimes:  PackedFloat32Array

_physics_process(delta):
    for i in positions.size():
        positions[i] += velocities[i] * delta
        lifetimes[i] -= delta
    cull_expired()
```

## State machines

Implicit state (`is_attacking`, `can_jump`) goes bad fast — make it explicit. One `current_state`, clear transitions; invalid combinations become _impossible_.

```pseudo
current_state.physics_update(delta)

transition_to(new_state):
    current_state.exit()
    current_state = new_state
    current_state.enter()
```

**HSM** (hierarchical) when states share logic — `Grounded` parent handles "fall off ledge" for `Idle / Walking / Running`; children handle specific input.

### FSM vs Behavior Tree

|                      | FSM                                  | Behavior Tree                        |
| -------------------- | ------------------------------------ | ------------------------------------ |
| Mental model         | "I'm in mode X"                      | "I'm doing task X"                   |
| Best for             | Character controllers, UI, animation | Complex AI decisions                 |
| Reactive transitions | Excellent (event-driven)             | Periodic ticks                       |
| Plug-and-play        | Medium                               | High (subtrees as Lego)              |
| Debugging            | Easy (one state)                     | Harder (cursor walks tree each tick) |

FSM for **what something IS**; BT for **what something DOES**. Combine: FSM for `alive/dead/spawning`, BT for the alive-state AI.

## Game loop — fixed vs variable timestep

**Variable** (delta varies per frame): non-deterministic; 144 Hz vs 30 Hz see different worlds; 200ms spike → tunneling; breaks multiplayer/replay/rollback.

**Fixed** (constant rate, e.g., 60 Hz): deterministic, multiplayer-safe.

**Rule:** gameplay (movement, AI, physics) → fixed step. Visual-only (camera smoothing, UI tweens, particle drift) → variable.

### Accumulator (custom engines — Glenn Fiedler's "Fix Your Timestep")

```pseudo
accumulator = 0
loop:
    accumulator += now() - last_time
    while accumulator >= FIXED_DT:
        simulate(FIXED_DT)
        accumulator -= FIXED_DT
    alpha = accumulator / FIXED_DT
    render(alpha)              # interpolate prev → current
```

**Interpolation** for 60 Hz physics on 144 Hz display: store prev + current positions, render at `lerp(prev, current, alpha)`. Most engines do this when enabled.

**Spiral of death:** frame > `FIXED_DT × N` → next frame needs N+1 → freeze. Mitigate: cap accumulator; pause on huge spikes (loading, alt-tab); profile the slow frame.

### Frame budgets

| Target FPS | Budget  |
| ---------- | ------- |
| 30         | 33.3 ms |
| 60         | 16.6 ms |
| 120        | 8.3 ms  |
| 144        | 6.9 ms  |

## Asset pipelines

| Concern          | Rule                                                                                           |
| ---------------- | ---------------------------------------------------------------------------------------------- |
| Source of truth  | Commit source files + import settings. Gitignore engine cache.                                 |
| Texture filter   | Pixel art → Nearest. HD → Linear.                                                              |
| 3D textures      | Always VRAM Compressed (4-8× smaller). Uncompressed only for precision (normal/height).        |
| Mipmaps          | On for 3D + 2D viewed at varying distance. Off for fixed-size pixel sprites.                   |
| Atlases          | Many small static sprites together → big win. Unique large sprites → no benefit.               |
| 3D models        | `.glb` (single binary). Apply scale in modeling tool, export at 1.0. Generate LODs.            |
| Audio            | `.wav` for short SFX (< 1s, fully loaded). `.ogg` for music + long ambient + voice (streamed). |
| Build size       | Texture compression is the biggest lever. 4K uncompressed = 64 MB VRAM; BC7 = 16 MB.           |
| VCS for binaries | `git lfs track "*.png" "*.glb" "*.wav" "*.ogg"`. `git lfs lock` for `.psd` / `.blend`.         |

## Physics

| Body                     | Moves how?              | Affected by physics?       | Use for                          |
| ------------------------ | ----------------------- | -------------------------- | -------------------------------- |
| `Static`                 | Doesn't                 | No                         | Walls, floors, level geometry    |
| `Rigid`                  | Engine simulates        | Yes                        | Crates, debris, ragdolls         |
| `Character`              | You move via code       | No (you handle collisions) | Player, AI                       |
| `Animatable` / kinematic | You move; pushes rigids | No                         | Platforms, doors, elevators      |
| `Area` / trigger         | Optional                | No collision response      | Trigger zones, hitboxes, pickups |

**Pick the least powerful body that does the job.** Rigid for a player feels floaty; Character for a falling crate wastes code.

### Shapes + layers

- **Dynamic bodies use convex shapes; static can use concave (trimesh).**
- **Circle/Sphere** — projectiles; **Capsule** — characters (no stair catches); **Box** — crates; **Convex polygon** — irregular dynamic; **Concave** — exact mesh, static only.

**Collision layers + masks:** `layer` = what THIS body IS; `mask` = what it LOOKS FOR. Name them in project settings. Player projectile mask = `world + enemy` (ignores player). Clean, fast, no `if body == self.owner: continue` hacks.

**CCD for fast objects:** bullets tunnel through thin walls between ticks. Enable CCD on rigid bodies; use raycasts for hitscan; thicker colliders (1-pixel walls invite tunneling).

## Audio — bus architecture

```
Master                          (final output, ~0 dB)
├── Music             -6 dB
├── SFX               -3 dB     (UI / Player / World / Enemy children)
├── Voice             -3 dB
└── Ambient           -9 dB
```

Player gets Music / SFX / Voice sliders → map to bus volumes. Master peaks ~-6 to -3 dB; Limiter on Master against clipping.

- **Pool players** for concurrent sounds (10 enemies hit at once).
- **Spatial 3D** needs a listener (usually the camera). 2D auto-attenuates by distance.
- **Ducking:** dialog plays → music drops (compressor sidechain or manual tween).
- **Layered music:** base loop + stems that fade in based on game state.

## Anti-patterns

- Variable timestep for physics
- Per-frame allocations in hot loops (`var x = []` every frame → GC death)
- Manual collision math instead of physics engine
- Cargo-cult ECS in a 30-entity puzzle game
- Fat components with methods and dependencies (those are just objects)
- Boolean spaghetti instead of state machines
- Movement in `_process` (frame-rate-dependent)
- Hard-coded `1/60` in calculations (breaks when physics rate changes)
- Mega-switch in `_process` for 15 states
- One mega-collider for a complex level
- Bullet velocity in pixels/frame, not units/sec
- One `AudioStreamPlayer` for everything (calls restart each other)
- Loading WAV for music → RAM bloat (use OGG)
- Same SFX every time → ear fatigue (pitch-vary ±5%, swap 3-4 variants)
- Committing engine import cache to git

## Hand-off

For Godot-specific scenes, signals, exports, 2D/3D/UI: `Skill(godot)`. For networked games: `Skill(godot)`. For GDScript fundamentals: `Skill(gdscript)`. For hot-path optimization, pooling, profiling: `Skill(gdscript)`.
