---
name: a-frame
description: Build immersive VR and AR experiences for the web using A-Frame, the HTML-based 3D framework built on Three.js. Use this skill whenever the user is building or working on an A-Frame scene, writing A-Frame components, adding WebXR interactivity, setting up VR controllers, loading GLTF models in A-Frame, building a 360° viewer, creating a VR game, handling raycasting or gaze interactions, or asking about a-scene, a-entity, a-box, a-sky, AFRAME.registerComponent, or any other A-Frame primitive or API. Also triggers on "WebXR scene", "VR on the web", "immersive web", "A-Frame entity", "aframe component", "meta quest webxr", "VR experience HTML", or "a-frame physics".
---

# A-Frame — WebXR & Immersive 3D for the Web

A-Frame is a web framework for building virtual reality (VR) and augmented reality (AR) experiences. It wraps Three.js in an HTML-based entity-component-system (ECS) architecture so you can write `<a-box>` in markup and get a 3D scene — while still having full access to JavaScript, Three.js, and the WebXR API when you need it.

**Current stable version:** 1.7.x (CDN: `https://aframe.io/releases/1.7.1/aframe.min.js`)

**Docs:** https://aframe.io/docs/1.7.0/introduction/

---

## Quick Start

```html
<html>
  <head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
  </head>
  <body>
    <a-scene>
      <a-box position="-1 0.5 -3" rotation="0 45 0" color="#4CC3D9"></a-box>
      <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E"></a-sphere>
      <a-cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D"></a-cylinder>
      <a-plane position="0 0 -4" rotation="-90 0 0" width="4" height="4" color="#7BC8A4"></a-plane>
      <a-sky color="#ECECEC"></a-sky>
    </a-scene>
  </body>
</html>
```

No build step, no install. Drop a `<script>` tag and write HTML. Open in any browser — including on a Meta Quest — and click "Enter VR."

---

## Core Concepts

### Entity-Component-System (ECS)

A-Frame follows an ECS architecture: the building blocks are **entities** (container objects), **components** (reusable data/behavior modules), and **systems** (global managers).

- `<a-entity>` — a bare entity with no appearance or behavior until components are attached
- Components are HTML attributes: `geometry="primitive: box"`, `material="color: red"`, `light="type: point"`
- Multiple components compose into any kind of object

```html
<!-- A glowing point-light sphere -->
<a-entity
  geometry="primitive: sphere; radius: 0.5"
  material="color: white; shader: flat; emissive: #FFEEAA; emissiveIntensity: 0.8"
  light="type: point; color: white; intensity: 1.5; distance: 5"
  position="0 2 -3">
</a-entity>
```

### Primitives

Primitives are shorthand wrappers around common entity+component combos:

| Primitive | Equivalent entity components |
|---|---|
| `<a-box>` | `geometry="primitive: box"` + `material` |
| `<a-sphere>` | `geometry="primitive: sphere"` |
| `<a-plane>` | `geometry="primitive: plane"` |
| `<a-sky>` | Large inverted sphere + `material="side: back"` |
| `<a-gltf-model>` | `gltf-model` component |
| `<a-text>` | `text` component |
| `<a-camera>` | `camera` + `look-controls` + `wasd-controls` |
| `<a-cursor>` | `cursor` + `raycaster` (gaze interaction) |
| `<a-light>` | `light` component |
| `<a-sound>` | `sound` component |

---

## Scene & Assets

### Asset Management System

Preload assets in `<a-assets>` so the scene only starts rendering when everything is ready:

```html
<a-scene>
  <a-assets>
    <a-asset-item id="tree-model" src="tree.gltf"></a-asset-item>
    <img id="grass-texture" src="grass.jpg">
    <audio id="ambient-sound" src="forest.mp3" preload="auto"></audio>
  </a-assets>

  <!-- Reference assets by ID -->
  <a-gltf-model src="#tree-model" position="0 0 -5"></a-gltf-model>
  <a-plane material="src: #grass-texture" width="20" height="20" rotation="-90 0 0"></a-plane>
  <a-sound src="#ambient-sound" autoplay="true" loop="true"></a-sound>
</a-scene>
```

All assets get a `crossorigin` attribute automatically. Set a timeout with `<a-assets timeout="10000">` (default 3000ms). Listen for the `loaded` event if you need to act after all assets finish.

### Loading GLTF Models

GLTF 2.0 is A-Frame's preferred 3D model format:

```html
<!-- As primitive -->
<a-gltf-model src="url(model.gltf)" position="0 0 -3" scale="0.5 0.5 0.5"></a-gltf-model>

<!-- As component on entity -->
<a-entity gltf-model="url(model.gltf)" position="0 0 -3"></a-entity>

<!-- Or reference a preloaded asset -->
<a-gltf-model src="#my-model"></a-gltf-model>
```

Listen for the model to load before modifying its children:

```javascript
document.querySelector('a-gltf-model').addEventListener('model-loaded', function (evt) {
  var model = evt.detail.model; // THREE.Group
  console.log('Model loaded:', model);
});
```

**Tip:** Use GLB (binary GLTF) for single-file deployment. Keep models under 5MB for web performance.

---

## Writing Custom Components

All application logic belongs inside components — this keeps code modular, reusable, and testable. Define components before `<a-scene>`:

```html
<head>
  <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
  <script src="my-component.js"></script>  <!-- ← before a-scene -->
</head>
```

### Component Anatomy

```javascript
AFRAME.registerComponent('my-component', {
  // Define configurable properties
  schema: {
    color:    { type: 'color',    default: '#FF0000' },
    speed:    { type: 'number',   default: 1 },
    target:   { type: 'selector'              },   // returns an element
    enabled:  { type: 'boolean',  default: true }
  },

  // Called once when the component first attaches to an entity
  init: function () {
    // Set up state, allocate objects you'll reuse in tick()
    this.velocity = new THREE.Vector3();
    this.clock = 0;
  },

  // Called after init() and whenever data changes
  update: function (oldData) {
    var diff = AFRAME.utils.diff(oldData, this.data); // what changed
    if ('color' in diff) {
      this.el.getObject3D('mesh').material.color.set(this.data.color);
    }
  },

  // Called on every frame. Keep it lean — no garbage!
  tick: function (time, timeDelta) {
    if (!this.data.enabled) { return; }
    this.clock += timeDelta;
    // timeDelta is milliseconds since last frame
  },

  // Called when the component is removed or entity is removed
  remove: function () {
    // Clean up event listeners, cancel timers, dispose Three.js objects
  },

  // Called when entity pauses (e.g., tab hidden)
  pause: function () {},
  play: function () {}
});
```

Use the component in HTML:

```html
<a-entity my-component="color: blue; speed: 2; target: #player"></a-entity>
```

### Performance Rule for tick()

Never allocate objects inside `tick()` — create `THREE.Vector3`, `THREE.Quaternion` etc. once in `init()` and reuse them. Garbage collection pauses in VR cause visible judder:

```javascript
// ✅ Allocate once in init()
init: function () {
  this.tempVec = new THREE.Vector3();
},

tick: function () {
  // Reuse the vector
  this.tempVec.copy(this.el.object3D.position);
}

// ❌ Creates garbage every frame
tick: function () {
  var pos = new THREE.Vector3(); // Don't do this
}
```

Also bypass `setAttribute()` for per-frame transforms — write directly to `object3D`:

```javascript
// ✅ Fast path
this.el.object3D.position.x += speed * timeDelta * 0.001;
this.el.object3D.rotation.y += 0.01;

// ❌ Slow — parses strings every frame
this.el.setAttribute('position', {x: newX, y: 0, z: 0});
```

### Multiple Component Instances

Set `multiple: true` in the definition and use double-underscore IDs:

```javascript
AFRAME.registerComponent('badge', {
  multiple: true,
  schema: { label: { type: 'string' } },
  // ...
});
```

```html
<a-entity badge__score="label: Score: 100"
          badge__health="label: HP: 80">
</a-entity>
```

---

## Interactions

### Gaze / Desktop: cursor Component

For headsets without controllers (or desktop preview), attach `<a-cursor>` as a child of the camera:

```html
<a-camera>
  <a-cursor></a-cursor>
</a-camera>
```

The cursor emits `mouseenter`, `mouseleave`, `mousedown`, `mouseup`, `click`, and `fusing` (gaze timer) on intersected entities. Handle them with a component or the community `event-set` component:

```html
<script src="https://unpkg.com/aframe-event-set-component@5.x.x/dist/aframe-event-set-component.min.js"></script>

<a-box color="#4CC3D9"
       event-set__enter="_event: mouseenter; color: #8FF7FF"
       event-set__leave="_event: mouseleave; color: #4CC3D9">
</a-box>
```

### Handling Events in JavaScript

Put interaction logic in components — don't scatter it in `<script>` blocks:

```javascript
AFRAME.registerComponent('highlight-on-hover', {
  schema: { hoverColor: { default: 'yellow' } },
  init: function () {
    var el = this.el;
    var defaultColor = el.getAttribute('material').color;
    var hoverColor   = this.data.hoverColor;

    el.addEventListener('mouseenter', function () {
      el.setAttribute('material', 'color', hoverColor);
    });
    el.addEventListener('mouseleave', function () {
      el.setAttribute('material', 'color', defaultColor);
    });
  }
});
```

### Raycaster

Raycasting drives most interactions. Configure which objects a raycaster tests against to avoid performance issues:

```html
<!-- Cursor only tests entities with class="interactive" -->
<a-camera>
  <a-cursor raycaster="objects: .interactive"></a-cursor>
</a-camera>

<a-box class="interactive" position="0 1 -3"></a-box>
```

### VR Controllers

**3DoF (rotation only — Oculus Go):**
```html
<a-entity oculus-go-controls></a-entity>
```

**6DoF (full positional — Meta Quest, HTC Vive):**
```html
<!-- Vive -->
<a-entity vive-controls="hand: left"></a-entity>
<a-entity vive-controls="hand: right"></a-entity>

<!-- Meta Quest / Oculus Touch -->
<a-entity meta-touch-controls="hand: left"></a-entity>
<a-entity meta-touch-controls="hand: right"></a-entity>

<!-- Cross-platform abstraction (recommended for all 6DoF) -->
<a-entity hand-controls="hand: left"></a-entity>
<a-entity hand-controls="hand: right"></a-entity>
```

**Laser pointer interactions (attach to controller, not camera):**
```html
<a-entity hand-controls="hand: right"
          laser-controls
          raycaster="objects: .interactive; far: 5">
</a-entity>
```

**Listening to controller button events:**
```javascript
AFRAME.registerComponent('trigger-listener', {
  init: function () {
    this.el.addEventListener('triggerdown', this.onTrigger.bind(this));
  },
  onTrigger: function (evt) {
    console.log('Trigger pressed!', evt);
  }
});
```

Common button events: `triggerdown/up`, `gripdown/up`, `menudown/up`, `thumbstickdown/up`, `xbuttondown/up`, `ybuttondown/up`, `abuttondown/up`, `bbuttondown/up`.

### Room-Scale Grab Interactions

Use the community `super-hands` library for grab, stretch, and drag-drop without rolling your own:

```html
<script src="https://cdn.jsdelivr.net/npm/super-hands@^3.0.3/dist/super-hands.min.js"></script>

<a-entity hand-controls="hand: right"
          super-hands
          sphere-collider="objects: .grabbable">
</a-entity>

<a-box class="grabbable" grabbable position="0 1 -1"></a-box>
```

---

## Accessing Three.js

A-Frame is built on Three.js. Every entity's Three.js object is available via `el.object3D`:

```javascript
// Get the THREE.Object3D of an entity
var obj = document.querySelector('#my-entity').object3D;

// Manipulate directly
obj.position.set(1, 2, -3);
obj.rotation.y = Math.PI / 4;
obj.scale.setScalar(1.5);
obj.visible = false;

// Get the Three.js mesh specifically
var mesh = el.getObject3D('mesh');   // returns THREE.Mesh or undefined

// Set a custom Three.js object on the entity
el.setObject3D('myMesh', new THREE.Mesh(geometry, material));
el.removeObject3D('myMesh');

// Access the Three.js scene and renderer
var scene = document.querySelector('a-scene').object3D;  // THREE.Scene
var renderer = document.querySelector('a-scene').renderer; // THREE.WebGLRenderer
```

---

## Scene Configuration

### Camera
```html
<!-- Default camera with look/WASD controls -->
<a-camera position="0 1.6 0"></a-camera>

<!-- Fixed camera, no controls -->
<a-entity camera="active: true" look-controls="enabled: false" position="0 1 5"></a-entity>
```

### Lighting

A-Frame adds default hemisphere + directional lights. Override them:

```html
<a-scene light="defaultLightsEnabled: false">
  <a-light type="ambient" color="#888"></a-light>
  <a-light type="directional" color="white" intensity="1" position="-1 2 1"></a-light>
  <a-light type="point" color="orange" intensity="2" distance="10" position="0 3 0"></a-light>
  <a-light type="spot" angle="45" penumbra="0.3" position="0 5 0" target="#target"></a-light>
</a-scene>
```

### Fog

```html
<a-scene fog="type: exponential; color: #AAC; density: 0.05"></a-scene>
```

### Environment (community component)

The `aframe-environment-component` generates a full procedural environment in one attribute:

```html
<script src="https://unpkg.com/aframe-environment-component/dist/aframe-environment-component.min.js"></script>
<a-entity environment="preset: forest; groundColor: #445; fog: 0.8"></a-entity>
```

Presets: `none`, `default`, `contact`, `egypt`, `checkerboard`, `forest`, `goaland`, `yavapai`, `goldmine`, `threetowers`, `poison`, `arches`, `tron`, `japan`, `dream`, `volcano`, `starry`, `osiris`.

---

## VR / AR (WebXR)

### Enabling VR

VR is automatic — `<a-scene>` renders an "Enter VR" button on WebXR-capable browsers. To configure:

```html
<a-scene webxr="requiredFeatures: local-floor; optionalFeatures: bounded-floor, hand-tracking">
</a-scene>
```

### AR (Augmented Reality)

Enable AR mode with passthrough:

```html
<a-scene webxr="referenceSpaceType: local-floor; optionalFeatures: hit-test, dom-overlay">
  <!-- Use hide-on-enter-ar to hide VR-only objects in AR mode -->
  <a-sky color="#ECECEC" hide-on-enter-ar></a-sky>

  <!-- Use ar-hit-test for placing objects on real surfaces -->
  <a-entity ar-hit-test></a-entity>
</a-scene>
```

### Detecting XR Mode in Components

```javascript
// Check if in VR
this.el.sceneEl.is('vr-mode');  // → boolean

// Listen for mode changes
this.el.sceneEl.addEventListener('enter-vr', function () { /* ... */ });
this.el.sceneEl.addEventListener('exit-vr',  function () { /* ... */ });
```

---

## Community Components (Ecosystem)

Install via CDN before `<a-scene>`:

```html
<script src="https://unpkg.com/package-name/dist/package-name.min.js"></script>
```

Some essential community components:

| Component | Package | Use |
|---|---|---|
| Environment | `aframe-environment-component` | Procedural skyboxes & ground |
| Physics | `@c-frame/aframe-physics-system` | Rigid body / collision |
| Particle system | `@c-frame/aframe-particle-system-component` | Rain, fire, snow |
| Super hands | `super-hands` | Grab/stretch/throw for 6DoF |
| Extras | `aframe-extras` | Locomotion, movement controls, ocean |
| Event set | `aframe-event-set-component` | Declarative event handlers |
| State | `aframe-state-component` | Redux-like state management |
| Networked | `networked-aframe` | Multiplayer |

Find components: [npm search (aframe-component tag)](https://www.npmjs.com/search?q=keywords:aframe-component), [A-Frame Wiki Component Directory](https://aframe.wiki/en/#!pages/component-directory.md)

---

## Events & DOM APIs

A-Frame entities behave like DOM elements:

```javascript
// Query
var box  = document.querySelector('#my-box');
var hits = document.querySelectorAll('[enemy]:not([dead])');

// Get/set components
box.getAttribute('material');           // → {color: '#4CC3D9', ...}
box.setAttribute('material', 'color', 'red');
box.removeAttribute('physics');

// Create / remove entities
var sphere = document.createElement('a-sphere');
sphere.setAttribute('radius', '0.5');
sphere.setAttribute('position', '1 1 -3');
document.querySelector('a-scene').appendChild(sphere);

// Custom events
box.emit('explode', { damage: 10 }, true); // bubbles=true
box.addEventListener('explode', function (evt) {
  console.log(evt.detail.damage);
});
```

---

## Animations

The built-in `animation` component handles most needs:

```html
<a-box color="red"
       animation="property: rotation; to: 0 360 0; loop: true; dur: 3000; easing: linear">
</a-box>

<!-- Chain animations with begin events -->
<a-sphere
  animation__scale="property: scale; to: 2 2 2; dur: 500; startEvents: scale-up"
  animation__fade="property: material.opacity; from: 1; to: 0; dur: 500; startEvents: fade-out">
</a-sphere>
```

Trigger animations from JS:
```javascript
sphere.emit('scale-up');
sphere.emit('fade-out');
```

Animatable properties: `position`, `rotation`, `scale`, `material.color`, `material.opacity`, `geometry.radius`, and any numeric/color component property.

---

## Dev Tools

### Visual Inspector

Press `Ctrl+Alt+I` (or `Ctrl+Option+I`) in any A-Frame scene to open the built-in visual inspector and tweak entity properties in real time.

### Stats HUD

Add `stats` to `<a-scene>` to monitor FPS, draw calls, geometries, and vertices:

```html
<a-scene stats></a-scene>
```

---

## Common Patterns

### Following a Target Entity

```javascript
AFRAME.registerComponent('follow', {
  schema: {
    target: { type: 'selector' },
    speed:  { type: 'number', default: 2 }
  },
  init: function () {
    this.direction = new THREE.Vector3(); // reuse, no GC
  },
  tick: function (time, timeDelta) {
    var target  = this.data.target.object3D.position;
    var current = this.el.object3D.position;
    this.direction.copy(target).sub(current);
    var dist = this.direction.length();
    if (dist < 0.1) { return; }
    this.direction.normalize().multiplyScalar(this.data.speed * timeDelta * 0.001);
    current.add(this.direction);
  }
});
```

### Object Pooling for Dynamic Entities

Creating/destroying entities is expensive. Pre-create a pool and toggle visibility:

```html
<a-scene pool="mixin: bullet; size: 30"></a-scene>
```

Or use `el.sceneEl.components.pool.requestEntity()` / `.returnEntity(entity)` from the `pool` component.

### Cross-Entity Communication

Emit events rather than coupling components directly:

```javascript
// Emitter component
this.el.emit('score-changed', { points: 10 });

// Listener in another component
document.querySelector('#scoreboard').addEventListener('score-changed', function (evt) {
  updateScore(evt.detail.points);
});
```

---

## Best Practices

- **Put all code in components.** No global `<script>` logic that queries the DOM at load time — wait for the `loaded` or `componentinitialized` event instead.
- **Keep tick() GC-free.** Allocate `THREE.Vector3`, arrays, and objects in `init()`; reuse them in `tick()`.
- **Bypass setAttribute() for fast-changing transforms.** Write to `el.object3D.position/rotation/scale` directly.
- **Use `<a-assets>` for everything.** Never reference asset URLs inline if you need preloading or caching.
- **Prefer GLTF over OBJ.** GLTF 2.0 has built-in PBR materials, animations, and loads faster.
- **Scope raycasters.** Always set `raycaster="objects: .someClass"` — testing all scene objects on every frame is very expensive.
- **Use the stats component** (`<a-scene stats>`) to catch draw call and FPS regressions early.
- **Think in ECS, not inheritance.** Compose behavior from small single-purpose components rather than one large monolithic component.

For deeper performance optimization (instancing, geometry merging, material simplification, tick handler bypasses), see the **a-frame-optimization** skill.

---

## Related Skills

### a-frame-optimization
The sister skill to this one, covering everything about making A-Frame scenes fast: draw call reduction, geometry merging, GPU instancing, asset LOD, material simplification, and how to profile with the stats HUD. Once you've built something with this skill, use a-frame-optimization when it needs to run at a steady 72–90fps in a headset.

**Use a-frame-optimization when:** the scene is built but frame rate is dropping, draw calls are high, or you need it to run on a standalone headset like Meta Quest.

### threejs-3d-webgpu
A-Frame's renderer is Three.js — anything you can do in plain Three.js you can do inside an A-Frame component via `this.el.object3D`, `el.sceneEl.renderer`, and `el.setObject3D()`. Use the threejs-3d-webgpu skill when you need custom geometry, advanced shaders (WGSL/GLSL), custom post-processing, TSL node materials, or precise control that goes beyond what A-Frame's built-in components expose.

**Use threejs-3d-webgpu alongside this skill when:** writing a component that creates custom Three.js geometry or materials, or when you need WebGPU, EffectComposer post-processing, or custom render passes.

### game-math
VR and 3D scenes constantly require vector math, matrix transforms, quaternion rotations, and spatial queries. The game-math skill provides the mathematical foundations for anything that involves moving objects in 3D space, computing directions or distances, rotating around arbitrary axes, or implementing camera-relative movement.

**Use game-math alongside this skill when:** implementing movement systems, camera rigs, aiming/targeting, 3D UI placement, or any component manipulating `object3D` transforms.

### physics
Physics simulation in A-Frame is handled via community components like `@c-frame/aframe-physics-system` (Cannon.js) or `aframe-physx`. The physics skill covers the underlying math — Newtonian mechanics, rigid bodies, collision response, spring systems, and numerical integration — so you can understand or extend physics components rather than just using them as a black box.

**Use physics alongside this skill when:** building throw/grab mechanics, ragdolls, vehicle simulations, or any component that needs custom force application or collision callbacks.

### animation-specialist
A-Frame's `animation` component covers basic property tweens. For more complex sequenced animations — staggered reveals, chained state transitions, spring dynamics, or animation tied to controller input — the animation-specialist skill covers the underlying techniques and tools (easing curves, lerp vs. slerp, timeline orchestration).

**Use animation-specialist alongside this skill when:** building cutscenes, animated UI panels, or controller-driven animations that go beyond what the `animation` attribute supports.

### trigonometry
Circular orbits, oscillation, rotation around a pivot, angular velocity, angles between vectors — all of it comes up constantly in 3D scene programming. The trigonometry skill covers the math that underpins spatial movement in A-Frame components.

**Use trigonometry alongside this skill when:** making objects orbit, bob, pulse, spin around a non-origin pivot, or when computing angles for aiming or camera look-at behavior.

### geometry
Collision detection, bounding volumes, raycasting math, point-in-mesh tests, and plane/line intersections are the geometric foundations of VR interaction. The geometry skill covers these spatial algorithms so you can reason about what's actually happening inside A-Frame's raycaster and collider components.

**Use geometry alongside this skill when:** building custom collision systems, computing intersection points, implementing object snapping, or creating procedural geometry in a component.

### accessibility-patterns
WebXR accessibility is still evolving, but VR experiences embedded in web pages still need to consider users who can't enter VR mode, provide non-VR fallback experiences, and handle caption/subtitle panels inside the scene. The accessibility-patterns skill covers WCAG considerations and semantic HTML practices for the 2D shell around the A-Frame scene.

**Use accessibility-patterns alongside this skill when:** building the page that hosts the A-Frame scene, adding in-scene UI panels with text, or creating experiences that need both VR and non-VR accessible modes.

### web-visual-effects
For post-processing effects (bloom, depth-of-field, chromatic aberration) applied to an A-Frame scene, you'll need to reach into the Three.js renderer layer via an A-Frame system or component. The web-visual-effects skill covers EffectComposer, WebGL shader techniques, and GPU-accelerated visual effects.

**Use web-visual-effects alongside this skill when:** adding cinematic post-processing to an A-Frame scene or implementing custom GLSL shaders in an A-Frame component.

### frontend-design
A-Frame experiences are embedded in HTML pages that need loading screens, UI chrome, onboarding flows, settings panels, and responsive design for users who aren't in VR. The frontend-design skill covers everything outside the `<a-scene>` tag.

**Use frontend-design alongside this skill when:** designing the web page shell, creating an in-browser UI for non-VR users, or building a UI overlay that appears above the A-Frame canvas.
