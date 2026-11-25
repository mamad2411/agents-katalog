---
name: three-live-authoring
description: >-
  Builds interactive 3D viewers, procedural Three.js scenes, AR product
  configurators, and 6DoF WebXR, Android XR, and iOS/visionOS spatial computing
  apps using <three-live> and <xr-live>. Use when creating or editing
  <three-live> or <xr-live> HTML elements, writing <script type="text/three">
  procedural scenes, configuring userData.xr spatial traits or
  userData.interactivity behavior graphs, building <div slot="spatial"> 3D HTML
  cards, or integrating native Android (Filament / Jetpack XR SceneCore) and
  iOS/visionOS (RealityKit) spatial views.
---

# Authoring 3D & Spatial Apps with `<three-live>` and `<xr-live>`

`<three-live>` and `<xr-live>` compile declarative HTML and sandboxed Three.js scripts (`<script type="text/three">`) into WebGL2/WebXR on the web, Google Filament & Jetpack XR SceneCore on Android, and Apple RealityKit & Quick Look on iOS/visionOS.

## 1. Choose the Right Component & Bundle

- **Use `<three-live>` (`three-live.min.js` or `three-live-full.min.js`)** when you need:
    -   A 3D `.glb` / `.usdz` model viewer (`<model-viewer>` drop-in
        replacement) with built-in `EXT_meshopt_compression` decoding and
        `KHR_materials_variants` (`variant-name`)
    -   A procedural Three.js scene (including 2D `Shape`/`ExtrudeGeometry`, 3D
        `SweepGeometry`/`HelixGeometry`/`LoftGeometry` sweeps, coils, and lofted
        vessels, `THREE.PatternInstancer` arrays, `THREE.CSG` Booleans, 3D
        `TextGeometry`, optional a la carte domain kits `THREE.Mechanical`,
        `THREE.Architecture`, `THREE.Industrial`, `THREE.Science`, and
        `THREE.Electronics` via `three-live-kits.min.js` or
        `three-live-kit-<domain>.min.js`, and `THREE.InstancedMesh` GPU
        instancing) with orbit controls and 1-tap mobile AR handoff (`ar`)
    -   PBR Next materials (clearcoat, transmission, dispersion, iridescence,
        sheen, volume), 5 filmic/commerce tone-mapping modes
        (`tone-mapping="neutral|aces|agx|reinhard|none"`), HDR emissive `bloom`,
        silhouette `outline`, `.hdr` environment lighting, ground contact
        shadows, multi-light depth shadow maps (`shadow-maps="auto|pcf|off"`,
        `light.castShadow`, `mesh.castShadow`, `mesh.receiveShadow`), loop-free
        `THREE.TSL` procedural node materials (`three-live-tsl.min.js` /
        `MeshStandardNodeMaterial` + `el.setMaterialUniform()`), skeletal
        animations & 2-bone/FABRIK `ik`, or 2D screen-space hotspots
        (`slot="hotspot-*"`)
- **Use `<xr-live>` (`xr-live-full.min.js`)** when you need:
    - 6DoF WebXR (`xr-mode="ar"` / `"vr"` / `"auto"`) or desktop 6DoF simulation (`xr-simulator="living-room"`)
    -   Declarative spatial manipulation traits (`grab`, `scale`, `billboard`,
        `follow`, `anchor`, `physics`, `orbit`, `handles`, `dimensions`,
        `snapTo`, `snapSocket`, `gaze`, `explode`, `navigable`, `sync`, `bloom`,
        `outline`, `ik`, `text`, `splat`, `audioEmitter`)
    - True 3D raycastable HTML/CSS spatial cards (`<div slot="spatial">`)
    -   Real-world depth occlusion & heightfield physics
        (`xr-depth="occlusion-physics"`), 25-joint hand gesture recognition
        (`xr-hands="gestures"`), spatial 3D painting (`spatial-paint`),
        depth-colliding particles (`particles`), 3D Gaussian Splats with 3D
        covariance & SH degree 1–3 (`splatUrl` / `splat`), world plane/reticle
        understanding (`world-understanding`), multimodal Gemini Live
        (`connectGeminiLive()` / `holdToAsk`), 3D CAD dimension callouts & tape
        measure (`spatial-measure`), magnetic socket/grid snapping
        (`magnetic-snap`), hands-free eye/head gaze dwell (`gaze-dwell`),
        multi-part exploded views & section clipping (`explode` /
        `section-plane`), `#xr-state` & `XRAnchor` persistence
        (`persistent-anchors`), parabolic XR locomotion (`locomotion`), or
        multi-user co-presence & WebRTC voice signaling (`shared-room` +
        `shared-room-voice`; your app owns the `RTCPeerConnection`).
-   **Add `xr-live-sim.min.js` (included in `xr-live-full.min.js`)** when the
    scene is an interactive simulation: a game, training drill, or safety
    walkthrough with a controllable character (`character`), steering agents
    (`agent`), integrity and hits (`integrity`, `hit-zones`), trigger zones
    (`zone`), spawners (`spawner`), objectives and scoring (`objective`,
    `scenario-timer`, `target-score`, `attempts`), or procedural audio cues
    (`audioCues`, `synth-audio`). Use neutral names: `integrity` (not health),
    `group` (not team).

---

## 2. Critical Rules That Prevent Broken Scenes

1.  **Declare `capabilities="..."` explicitly on `<three-live>` and
    `<xr-live>`:**
    -   All 9 capabilities (`scripts`, `network`, `remote_content`, `camera`,
        `microphone`, `sensors`, `storage`, `ai`, `external_handoff`) default to
        **off** on Web (`ThreeLiveCapabilities` on Android/iOS defaults to
        `scripts = true` and all sensitive capabilities `false`).
    -   Use `capabilities="scripts"` (or legacy `allow-client-scripts`) for pure
        procedural `<script type="text/three">`, `capabilities="viewer"` for
        remote `.glb`/`.usdz` + AR handoff, `capabilities="all"` for full
        playgrounds, or scoped tokens like
        `capabilities="scripts ai network:https@https://api.example.com"`.
        Server-hosted `script-src` requires
        `capabilities="scripts remote_content network"`.
        `three-live-cli validate <file>.html` flags missing capabilities via
        `TL401` and `TL403`.
2. **Use the pre-defined `THREE` and `scene` globals inside `<script type="text/three">`:**
   - Do **not** `import * as THREE from 'three'`, do **not** create a `new THREE.WebGLRenderer()`, and do **not** call `document.body.appendChild(...)` inside `<script type="text/three">`. The script runs inside an isolated Web Worker (or Rust Boa sandbox) with zero DOM access and populates the global `scene` directly (`scene.add(mesh)`).
3. **Never use `GLTFLoader` or `TextureLoader` inside `<script type="text/three">`:**
   - Network APIs (`fetch`, `XMLHttpRequest`) are revoked inside the procedural sandbox. Load `.glb` assets declaratively via `<three-live src="model.glb">` or `<xr-anchor src="model.glb">`.
4. **Prefer `mesh.userData.xr = { ... }` over legacy `userData.xrTraits`:**
   - The structured `userData.xr` object supports all core and extended spatial traits and exports cleanly to `.glb` (`extras.xr` + `ANDROID_xr_scenecore`) and `.usdz` (`customData.xr`).
5. **Always name interactive meshes (`mesh.name = '...'`):**
   - `meshclick` events, `selected-mesh`, `userData.xr.orbit.target`, `userData.interactivity` target references, `holdToAsk` prompts, and WebMCP `place_xr_object_at_gaze` all identify nodes by `mesh.name`.
6.  **Use loop-free `THREE.MeshStandardNodeMaterial` + `THREE.TSL` for
    procedural shaders (never `ShaderMaterial` or `TSL.Loop`):**
    -   Load `three-live-tsl.min.js` (or `three-live-full.min.js` /
        `xr-live-full.min.js`) and assign `colorNode`, `opacityNode`,
        `emissiveNode`, `roughnessNode`, `metalnessNode`, `normalScaleNode`,
        `bumpNode`, or `positionNode` using `THREE.TSL` (`uv`, `time`,
        `positionLocal`, `positionWorld`, `normalLocal`, `normalWorld`,
        `viewDirection`, `uniform(val, name)`, `fresnel`, `simplexNoise2D/3D`,
        `voronoi2D`, `checker`, `triplanar`, `hueShift`, `bumpFromHeight`,
        `remap`). Keep graphs acyclic (`<= 128` nodes, `<= 16` uniforms) and
        avoid fragment-only ops (`viewDirection`, `fresnel`, `bumpFromHeight`)
        inside `positionNode` (`TL501`–`TL504`).

---

## 3. Canonical `userData.xr` Trait Quick Reference

Attach `userData.xr` to any `THREE.Mesh` or `THREE.Group` inside `<script type="text/three">`:

Trait Key                | Accepted Values                                                                                                                                                                                                                                                                                                       | Behavior
:----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------
`grab`                   | `'1-hand' \| '2-hand' \| true`                                                                                                                                                                                                                                                                                        | Enables 6DoF pinch / controller trigger grabbing (`true` defaults to `'2-hand'`).
`scale`                  | `{ min?: number, max?: number } \| true`                                                                                                                                                                                                                                                                              | Two-hand pinch-to-scale clamped to `[min, max]` (default `0.05`–`5.0`).
`billboard`              | `'capsule' \| 'cylindrical' \| 'spherical' \| true`                                                                                                                                                                                                                                                                   | Faces the active viewer camera (`'capsule'` / `'cylindrical'` yaw-only; `'spherical'` full 3D).
`follow`                 | `'head' \| 'hand-left' \| 'hand-right'` **or** `{ mode, lazy, distance, deadzoneDeg, stiffness, height, faceUser, snapOnStart }`                                                                                                                                                                                      | String values use eager spring follow; object values activate lazy follow with angular deadzone + critically damped spring.
`anchor`                 | `'floor' \| 'wall' \| 'ceiling' \| 'table' \| 'horizontal' \| 'vertical'` **or** `{ target?, id?, persist? }`                                                                                                                                                                                                         | Snaps node to detected real-world planes or simulated surfaces; `persist: true` saves user-moved transforms across reloads and `#xr-state` URLs.
`physics` / `rigidBody`  | `'dynamic' \| 'static' \| 'kinematic' \| true` **or** `{ body?, shape?: 'auto' \| 'box' \| 'sphere' \| 'cylinder', mass?, restitution?, friction?, linearDamping?, angularDamping?, gravityScale?, velocity?, angularVelocity?, lockRotation? }`                                                                      | Steps 60 Hz deterministic Sequential Impulse rigid-body physics (gravity, restitution bounce, friction, stacking, sleeping, character push, projectile knockback, and depth heightfield collisions); emits `xrcollision` and `xrsleep`.
`orbit`                  | `{ target: [x,y,z] \| 'nodeName', radius, speed, height, phase, faceCenter }`                                                                                                                                                                                                                                         | Orbits around a 3D point or named target mesh at `speed` rad/s.
`handles`                | `{ rotateAxis?: 'y' \| 'none', minScale?: number, maxScale?: number } \| true`                                                                                                                                                                                                                                        | Spawns 4 top-corner uniform-scale handles and a bottom pedestal yaw-rotation bar; emits `xr-handles-change`.
`dimensions`             | `{ unit?: 'auto' \| 'm' \| 'cm' \| 'mm' \| 'in' \| 'ft-in', axes?: Array<'x' \| 'y' \| 'z'>, color?: string, showOnSelect?: boolean } \| true`                                                                                                                                                                        | Renders live `W × H × D` bounding-box dimension guide bars and 3D vector-glyph labels (`spatial-measure`).
`snapTo`                 | `{ grid?: number \| [x,y,z], angleDeg?: number, surface?: 'none' \| 'floor' \| 'wall' \| 'ceiling' \| 'any', socketTag?: string, radius?: number } \| true`                                                                                                                                                           | Snaps grabbed meshes to matching `snapSocket` anchors (`1.25×` breakaway hysteresis), grids, surfaces, and yaw angles (`magnetic-snap`).
`snapSocket`             | `string` **or** `{ tag: string, radius?: number, alignRotation?: boolean, highlightColor?: string }`                                                                                                                                                                                                                  | Marks a node as a magnetic snap target socket with a pulsing proximity ring (`magnetic-snap`).
`gaze`                   | `{ dwellMs?: number, action?: 'select' \| 'ask', repeat?: boolean } \| true`                                                                                                                                                                                                                                          | Opts mesh into hands-free eye/head gaze dwell (`250..10000ms`, default `1200ms`), routing to `meshclick` or `gemini-live` (`gaze-dwell`).
`explode`                | `{ direction?: [x,y,z], distance?: number, layer?: number, leaderLine?: boolean } \| boolean`                                                                                                                                                                                                                         | Configures per-part explosion vector, distance, staggered `layer` (`1..10`), and dashed leader lines (`exploded-view`); `false` pins base parts.
`cutaway`                | `[x,y,z]` **or** `{ normal: [x,y,z] }`                                                                                                                                                                                                                                                                                | Dollhouse view: hides the wall from the camera while the camera is on its outward side (`cutaway="off"` disables); keep curbs/baseboards on separate meshes.
`navigable`              | `boolean \| 'walkable' \| 'blocked'`                                                                                                                                                                                                                                                                                  | Marks floor/deck meshes as valid (`'walkable'`) or blocked landing surfaces for parabolic XR teleportation (`spatial-locomotion`).
`sync`                   | `boolean`                                                                                                                                                                                                                                                                                                             | Controls whether user manipulations sync across peers in `shared-room` (defaults to `true` on grabbable nodes).
`particles`              | `{ preset: 'rain' \| 'snow' \| 'sparks' \| 'confetti', count?: number, area?: [x,y,z], speed?: number }`                                                                                                                                                                                                              | Emits up to `2,000` depth-colliding particles inside `area`.
`holdToAsk`              | `{ prompt?: string, holdMs?: number } \| true`                                                                                                                                                                                                                                                                        | Press-and-hold on the mesh starts speech recognition and queries Gemini Live; emits `xr-hold-to-ask`.
`worldUnderstanding`     | `{ planes?: boolean, meshes?: boolean, reticle?: boolean, objects?: boolean }`                                                                                                                                                                                                                                        | Enables WebXR plane/mesh detection and gaze surface reticle (`__xr_reticle__`).
`splatUrl`               | `'https://.../scene.splat'` or `'.spz'`                                                                                                                                                                                                                                                                               | Streams and depth-sorts 3D Gaussian Splats (`.splat` or Niantic `.spz` v2/v3 with 3D covariance + SH degree 1–3).
`splat`                  | `{ url: string, shDegree?: 0 \| 1 \| 2 \| 3, maxSplats?: number }`                                                                                                                                                                                                                                                    | Structured 3D Gaussian Splat trait controlling Spherical Harmonics degree (`0..3`) and splat cap.
`bloom`                  | `{ strength?: number, threshold?: number, radius?: number } \| boolean \| number`                                                                                                                                                                                                                                     | Enables HDR emissive bloom on the scene/node (`strength` in `[0, 5]`, `threshold` in `[0, 2]`, `radius` in `[0, 1]`).
`outline`                | `{ color?: string, thickness?: number } \| boolean \| string`                                                                                                                                                                                                                                                         | Renders an inverted-hull or screen-space silhouette outline (`thickness` in `[0.002, 0.25]`) around the node.
`ik`                     | `{ root: string, mid?: string, effector: string, target: string \| [x, y, z], pole?: string \| [x, y, z], solver?: 'two-bone' \| 'fabrik', iterations?: number, tolerance?: number, weight?: number }`                                                                                                                | Solves analytical 2-bone (`root` → `mid` → `effector`) or FABRIK inverse kinematics toward `target` (and optional `pole`, alias `poleTarget`).
`lod`                    | `boolean \| number[] \| { distances?: number[], ratios?: number[], levels?: Array<{ distance: number, ratio?: number, node?: string }>, cullDistance?: number, hysteresis?: number }`                                                                                                                                 | Distance-based Level-of-Detail switching with hysteresis, far-distance culling, and automatic vertex-clustering decimation (also `new THREE.LOD()`).
`text`                   | `{ text: string, size?: number, depth?: number, bevelEnabled?: boolean, bevelThickness?: number, bevelSize?: number }`                                                                                                                                                                                                | Extruded 3D vector text metadata exported to glTF `extras.xr.text` and USDZ `customData.xr`.
`audioEmitter` / `audio` | `'hum' \| 'reactor' \| 'wind' \| 'beacon' \| 'geiger' \| 'chimeLoop' \| 'machinery' \| 'water'` or `'https://.../sound.mp3'` or `{ preset?, src?, volume?, loop?, autoplay?, playOnSelect?, distanceModel?, refDistance?, maxDistance?, rolloffFactor?, coneInnerAngle?, coneOuterAngle?, coneOuterGain?, pitchHz? }` | Attaches a 3D positional and directional spatial audio emitter (`spatial-audio`), exporting `KHR_audio_emitter` and USDZ `SpatialAudio`.
`character`              | `true \| 'third-person' \| 'first-person' \| 'top-down' \| 'fixed'` **or** `{ speed, jumpVelocity, radius, height, cameraMode, clips }`                                                                                                                                                                               | (`xr-live-sim`) Keyboard, gamepad, or touch-joystick character that slides along `collidable` nodes.
`agent`                  | `'patrol' \| 'chase' \| 'flee' \| 'follow' \| 'wander'` **or** `{ mode, target, speed, sightRadius, waypoints }`                                                                                                                                                                                                      | (`xr-live-sim`) Steering agent; `target: 'user'` means the character, else the viewer.
`integrity`              | `number` **or** `{ max, group, showBar, scoreValue, contactAmount, hideOnDepleted }`                                                                                                                                                                                                                                  | (`xr-live-sim`) Takes hits from other groups; emits `xrhit` and `xrdepleted`.
`zone`                   | `'box' \| 'sphere'` **or** `{ shape, size, radius, watchGroups, color }`                                                                                                                                                                                                                                              | (`xr-live-sim`) Emits `xrzoneenter` / `xrzoneexit` for characters, agents, and integrity nodes.
`spawner`                | `'TemplateName'` **or** `{ template, intervalSec, maxActive, totalCount, spawnRadius }`                                                                                                                                                                                                                               | (`xr-live-sim`) Clones a hidden template node; emits `xrspawn`.
`objective`              | `'pickup' \| 'checkpoint' \| 'key' \| 'time-bonus' \| 'restore'` **or** `{ type, amount, order, required, radius, respawnSec }`                                                                                                                                                                                       | (`xr-live-sim`) Completed by proximity to the character, or by tap without one; `order > 0` enforces sequence.
`audioCues`              | `{ onTap?, onObjective?, onHit?, onDepleted?, onZoneEnter?, onZoneExit?, onSpawn?, onJump?, onLand? }` (cue names such as `'confirm'`, `'alarm'`)                                                                                                                                                                     | (`xr-live-sim`) Procedural cues with `synth-audio`; separate from the file-based `audio` trait.
`collidable`             | `true`                                                                                                                                                                                                                                                                                                                | (`xr-live-sim`) Wall or floor for characters and agents.
`pointerEvents`          | `'none'`                                                                                                                                                                                                                                                                                                              | Excludes the mesh from raycast picking so rays pass through to objects behind it.

---

## 4. Progressive Disclosure References

Read these reference files when you need detailed schemas, copy-pasteable recipes, or debugging steps:

-   **[`references/xr-traits-and-plugins.md`](references/xr-traits-and-plugins.md)**:
    Complete attribute tables, clamping ranges, DOM events,
    `userData.interactivity` (`KHR_interactivity`) actions, all 15 spatial
    plugin controllers, the 6 `xr-live-sim` simulation plugins, Gemini Live API,
    and WebMCP tool schemas.
-   **[`references/recipes.md`](references/recipes.md)**: 10 production-ready,
    copy-pasteable code templates (E-commerce configurator, Physics ballpit &
    spatial HTML UI, manipulation handles & lazy HUD, Gemini Live + World
    Understanding, Spatial Paint + Particles + Gaussian Splats, Native
    Android/iOS integration, CAD Exploded View + Measure + Gaze Dwell, Magnetic
    Snapping + Persistent `#xr-state` + Locomotion, Multi-User `shared-room`
    Co-Presence, and an `xr-live-sim` training drill).
-   **[`references/debugging-and-csp.md`](references/debugging-and-csp.md)**:
    Diagnosing blank scenes, inspecting `THREE.getAuthorWarnings()`, running
    closed-loop `three-live-cli validate --json` / `render --view=quad` /
    `sim --json` checks (`TL100–TL402`), configuring Worker/iframe sandboxes &
    `connect-src wss:` under strict CSP / Trusted Types, and verifying bundle
    budgets.

--------------------------------------------------------------------------------

## 5. Closed-Loop CLI Verification (`three-live-cli`)

Always verify authored `.js`, `.html`, or `.glb` scenes headlessly using
`three-live-cli`:

1.  **Validate & Spatial Lint:** `three-live-cli validate scene.js --json` — fix
    all `TL100–TL402` errors and spatial warnings (`inFrustum`,
    `screenCoveragePct`, `grounded`, broken target references) before rendering.
2.  **Render 4-Up Quad Contact Sheet:** `three-live-cli render scene.js -o
    preview.png --view=quad --grid --annotations` — inspect perspective camera
    framing (`CAMERA`), front/right elevation (`FRONT`, `RIGHT`), and top-down
    layout (`TOP`) with `1 m` gridlines and AABB labels.
3.  **Match a Reference (when given a photo, mockup, sketch, or blueprint):**
    `three-live-cli render scene.js -o compare.png --reference=ref.jpg
    --view=camera` (or `--view=front|right|top` for blueprints) — iterate until
    `silhouetteIou >= 0.85` and `|aspectError| < 0.05` when `silhouetteReliable`
    is true, otherwise compare the aligned OVERLAY panel.
4.  **Simulate Interactivity & Temporal Motion:** `three-live-cli render
    scene.js -o anim.png --frames=4 --duration=2.0 --trigger-select=<node>` or
    `three-live-cli sim scene.js --duration=5.0 --actions='[...]' --json`. For
    games, play the level closed-loop with
    `three-live-cli gym reset scene.js --session ep.json` and
    `three-live-cli gym step --session ep.json --actions='[...]'` (or the
    `three_live_gym_*` MCP tools) to check it is winnable.
