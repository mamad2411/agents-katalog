---
name: phaser-gamedev
description: "Build 2D browser games with Phaser 3 (JS/TS): scenes (Boot/Menu/Game/UI), sprites/animations, input, Arcade/Matter physics, tilemaps (Tiled), asset loading, and performance patterns. Use for prompts like 'Phaser scene', 'Arcade physics', 'tilemap', 'Phaser 3 game architecture'."
---

# Phaser Game Development

Build fast, polished 2D browser games using Phaser 3’s scene-based architecture and physics systems.

## Philosophy: Games as Living Systems

Games are not static UIs—they are **dynamic systems** where entities interact, state evolves, and player input drives everything.

**Before building, ask**:
- What **scenes** does this game need? (Boot, Menu, Game, Pause, GameOver, UI overlay)
- What are the **core entities** and how do they interact?
- What **state** must persist across scenes (and what must not)?
- What **physics** model fits? (Arcade for speed, Matter for realism)
- What **input methods** will players use? (keyboard/gamepad/touch)

**Core principles**:
1. **Scene-first architecture**: Organize code around scene lifecycle and transitions.
2. **Composition over inheritance**: Build entities from sprite/body/controllers, not deep class trees.
3. **Physics-aware design**: Choose collision model early; don’t retrofit physics late.
4. **Asset pipeline discipline**: Preload everything; reference by keys; keep loading deterministic.
5. **Frame-rate independence**: Use `delta` for motion and timers; avoid frame counting.

## Workflow: Build the Spine First

- Define the minimal playable loop (movement + win/lose + restart) before content/polish.
- Decide scene graph and transitions (including UI overlay scene if needed).
- Choose physics system early:
  - **Arcade** for most games (platformers/top-down/shooters).
  - **Matter** for realistic collision/constraints/ragdolls.
  - **None** for non-physics scenes (menus, VN, card games).
- Implement a reliable asset-loading path (Boot scene), then scale out content.
- Add debug toggles/profiling early so performance doesn’t become a late surprise.

## Use References (Progressive Disclosure)

- `references/core-patterns.md`: config, scene lifecycle, objects, input, animations, asset loading, project structure.
- `references/arcade-physics.md`: Arcade physics deep dive (including pooling patterns).
- `references/tilemaps.md`: Tiled tilemap workflows, collision setup, object layers.
- `references/performance.md`: optimization strategies (pooling, batching, culling, camera, texture atlases).
- `references/spritesheets-nineslice.md`: spritesheet loading (spacing/margin), nine-slice UI panels, asset inspection protocol.

## Anti-Patterns to Avoid

❌ **Global state soup**: Storing game state on `window` or module globals  
Why bad: scene transitions become fragile; debugging becomes chaotic  
Better: scene data, registries, or a dedicated state manager

❌ **Loading in `create()`**: Loading assets in `create()` instead of `preload()`  
Why bad: assets may not be ready when referenced  
Better: load in `preload()`; use a Boot scene for all assets

❌ **Frame-dependent logic**: Using frame count instead of `delta`  
Why bad: game speed varies with frame rate  
Better: scale by `(delta / 1000)` for consistent movement/timers

❌ **Physics overkill**: Using Matter for simple platformer collisions  
Why bad: unnecessary complexity + perf cost  
Better: Arcade covers most 2D collision needs

❌ **Monolithic scenes**: One giant scene with all game logic  
Why bad: hard to extend; UI/menus/pause become hacks  
Better: separate gameplay vs UI overlay vs menus

❌ **Magic numbers everywhere**: Hardcoded tuning values scattered in code  
Why bad: balancing becomes painful; changes cause regressions  
Better: config objects/constants and centralized tuning

❌ **No pooling for spammy objects**: Creating/destroying bullets/particles constantly
Why bad: GC spikes → stutters
Better: object pooling with groups + `setActive(false)` / `setVisible(false)`

❌ **Assuming spritesheet frame dimensions**: Using guessed frame sizes without verifying source asset
Why bad: wrong dimensions cause silent frame corruption; off-by-pixels compounds into broken visuals
Better: open asset file, measure frames, calculate with spacing/margin, verify math adds up

❌ **Ignoring spritesheet spacing**: Not specifying `spacing` for gapped spritesheets
Why bad: frames shift progressively; later frames read wrong pixel regions
Better: check source asset for gaps between frames; use `spacing: N` in loader config

❌ **Hardcoding nine-slice colors**: Using single background color for all UI panel variants
Why bad: transparent frame edges reveal wrong color for different asset color schemes
Better: per-asset background color config; sample from center frame (frame 4)

❌ **Nine-slice with padded frames**: Treating the full frame as the slice region when the art is centered/padded inside each tile
Why bad: edge tiles contribute interior fill, showing up as opaque “side bars” inside the panel
Better: trim tiles to their effective content bounds (alpha bbox) and composite/cache a texture; add ~1px overlap + disable smoothing to avoid seams

❌ **Scaling discontinuous UI art**: Scaling a cropped banner/ribbon row that contains internal transparent gaps
Why bad: the transparent gutters scale too, making the UI look “broken” or segmented
Better: slice into left/center/right (or similar), stretch only the center, and stitch into a cached texture at the target size

## Variation Guidance

Outputs should vary based on:
- **Genre** (platformer vs top-down vs shmup changes physics/input/camera)
- **Target platform** (mobile touch, desktop keyboard, gamepad support)
- **Art style** (pixel art scaling vs HD smoothing; atlas usage)
- **Performance envelope** (many sprites → pooling/culling; few sprites → simpler code)
- **Team size / complexity** (prototype vs production architecture)

Avoid converging on:
- One “default” resolution and scale mode
- Always defaulting to Arcade (or always defaulting to Matter)
- Copy-pasting boilerplate without adapting to the game’s needs

## Remember

Phaser gives powerful primitives—scenes, sprites, physics, input—but **architecture is your responsibility**.

Think in systems: define the scenes, define the entities, define their interactions—then implement.

**Codex is capable of building complete, polished Phaser games. These guidelines illuminate the path—they don't fence it.**
