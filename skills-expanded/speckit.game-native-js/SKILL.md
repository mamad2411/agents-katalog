---
name: speckit.game-native-js
description: Native Web Game Developer - Phaser 3, PixiJS, Three.js/R3F, Babylon.js, 60 FPS Fixed Timestep loop, Object Pooling (Zero-GC), Hybrid DOM HUD, and Web Audio API.
---

## Mission
Architect and build high-performance native JavaScript/TypeScript web games running at steady 60-144 FPS. Ensure instant loading (< 2s), zero Garbage Collection spikes via strict Object Pooling, data-driven game balance, hybrid Canvas + DOM HUD architectures, and multi-input responsiveness (touch, gamepad, keyboard).

## Inputs and Outputs
- Read `.agents/specs/[feature]/spec.md`, `plan.md`, `tasks.md`, target engine specs, core gameplay loop definitions, and asset balance configurations.
- Produce core engine initialization and scene manager (`src/game/`), fixed timestep game loop with object pool managers (`src/game/pools/`), balance configuration files, hybrid canvas + DOM overlays, and multi-channel Web Audio manager.

## Protocol

### 1. 60 FPS Fixed Game Loop & Timestep Management
- **Decoupled Physics & Render**:
  - Physics/Game State MUST update in a fixed timestep `FixedUpdate(fixedDelta)` (e.g. 50Hz / 20ms or 60Hz / 16.6ms).
  - Rendering updates on every `requestAnimationFrame(time)` with state interpolation (`lerp`) to prevent jitter on high refresh rate monitors (120Hz/144Hz).
- **Delta-Time Clamping**: Clamp maximum frame delta (e.g., `Math.min(dt, 0.1)`) to avoid physics tunneling or simulation explosions when tabs are backgrounded or during frame drops.

### 2. Zero-Allocation in Hot Loops (Anti-GC Stutter)
- **Object Pooling**: Pre-allocate and reuse memory pools for all ephemeral entities:
  - Bullets / Projectiles
  - Particle Emitters / Explosions
  - Floating Damage Numbers / Combat Text
  - Enemies & Spawners
  *Rule*: NEVER call `new Object()`, `new Array()`, or allocate closures inside the main tick/update loop.
- **Texture Atlases & SpriteSheets**: Combine individual sprites into unified texture atlases using TexturePacker to minimize WebGL batch draw calls.
- **Spatial Partitioning**: Use Flat TypedArrays (`Float32Array`, `Int32Array`) with Grid or QuadTree indexing for broadphase collision detection.

### 3. Data-Driven Game Design & Balancing
- **Externalized Config**: All gameplay parameters (HP, Speed, Cooldown, Damage, Drop rates, Wave progression) MUST be defined in `src/config/balance/*.json` or CSV files.
- **Type-Safe Validation**: Validate balance JSON files at build time / game boot using Zod or TypeScript schemas to catch missing stats or type mismatches immediately.

### 4. Hybrid UI & Responsive Multi-Resolution
- **Rendering Separation**:
  - **Canvas / WebGL**: Dedicated exclusively to gameplay entities, map tiles, and in-world visual effects.
  - **DOM / TailwindCSS Layer (HUD Overlay)**: Renders vector-sharp UI (Health bars, Skill hotbars, Inventory, Dialog boxes, Leaderboards, Settings).
- **Viewport Scaling**: Configure logical virtual resolution (e.g. `1280x720` or `1920x1080`) with `Scale.FIT` / `Scale.ENVELOP` and auto-centering to support mobile portrait, landscape, and desktop ultrawide seamlessly.

### 5. Web Audio API & Sound Bus Architecture
- **Multi-Channel Sound Bus**:
  ```
  [AudioContext] ➔ [Master Gain] ┬➔ [BGM Gain]
                                ├➔ [SFX Gain] (Spatial Audio / PannerNode)
                                └➔ [UI Gain]
  ```
- **Autoplay Policy Handling**: Initialize `AudioContext` in a suspended state; automatically resume on the first user pointer/touch interaction (`pointerdown`).
- **Audio Pooling**: Pre-instantiate sound instances to avoid latency and audio glitching during heavy combat SFX.

### 6. Multi-Input Pipeline
- **Input Abstraction Layer**: Map abstract actions (`MOVE_UP`, `MOVE_DOWN`, `PRIMARY_FIRE`, `DASH`, `PAUSE`) across:
  - Keyboard & Mouse
  - Virtual Touch Joystick / On-screen Action Buttons (Mobile)
  - Gamepad API (Xbox / PlayStation controller with dynamic button glyphs)

## Completion Gate
Game loop sustains 60 FPS under simulated peak load, memory profile confirms zero ephemeral allocations in tick loops, balance schemas validate without errors, and audio resumes only after user interaction.

## Guard Rails
- FORBIDDEN: Allocating new objects or arrays inside hot update loops (violates 60 FPS zero-allocation rule).
- FORBIDDEN: Hardcoding combat stats, damage multipliers, or enemy attributes in game logic code.
- FORBIDDEN: Triggering un-resumed Web Audio before user interaction (browser console error & silence).
- FORBIDDEN: Using unclamped variable `dt` in physics calculation (leads to wall glitching & physics breaking).
