---
name: lights
description: "Set up lighting for Three.js scenes — choosing light combinations, shadows, and look. Use when configuring scene lighting, fixing flat or harsh lighting, or adding shadows."
---

# Lights

## Light Setups

| Setup                            | Result                                      |
| -------------------------------- | ------------------------------------------- |
| AmbientLight only                | Flat uniform lighting, no shadows           |
| DirectionalLight only            | Harsh contrast, pure black shadows          |
| Ambient + Directional            | Realistic outdoor lighting (sun + sky fill) |
| Ambient + PointLights/SpotLights | Indoor scenes with local light sources      |

Ambient light controls shadow appearance—without it, shadows are pure black. Even in nighttime scenes, keep enough light (e.g. AmbientLight) for the viewer to see the environment.

## Recommended Setup

Use AmbientLight + CSM (Cascading Shadow Maps). CSM replaces DirectionalLight with superior shadow quality out of the box—no need to manually configure shadow camera bounds.

A lone `DirectionalLight` has a single shadow map covering one fixed frustum: over a large outdoor map its shadows are either blurry (one map stretched across hundreds of meters) or simply missing past a short range. **For any outdoor or large scene, use CSM** — its cascades keep shadows crisp from right next to the camera out to the horizon. A lone `DirectionalLight` with a small shadow frustum on a big map is wrong.

CSM looks like a lot of setup, but it is **paste-once boilerplate** — drop this helper in unchanged, then call `createCsmSun(...)` once and `csm.update()` every frame. That is the whole cost; don't trade it for a plain `DirectionalLight`.

```typescript
import { CSM } from 'three/examples/jsm/csm/CSM.js'
import { Material, Vector3 } from 'three'

// Paste-once: an outdoor sun with cascaded shadows. Returns the csm; call csm.update() each frame.
function createCsmSun(scene, camera, renderer, lightDirection = new Vector3(-1, -2, -1), intensity = 2, maxFar = 200) {
  renderer.shadowMap.enabled = true // do NOT also set shadowMap.type = PCFSoftShadowMap with CSM

  const csm = new CSM({
    cascades: 4, lightDirection: lightDirection.clone().normalize(),
    camera, parent: scene, lightIntensity: intensity, maxFar, mode: 'practical',
  })
  csm.fade = true

  const biases = [-0.00001, -0.0001, -0.0003, -0.0006]
  const normalBiases = [0.02, 0.06, 0.16, 0.3]
  csm.lights.forEach((light, i) => {
    light.shadow.bias = biases[i] ?? -0.0006
    light.shadow.normalBias = normalBiases[i] ?? 0.3
  })

  // CSM must inject its shader into every material; do it lazily at render time.
  const done = new WeakSet<Material>()
  const original = renderer.renderBufferDirect.bind(renderer)
  renderer.renderBufferDirect = function (cam, sc, geom, material, object, group) {
    if (material && !done.has(material)) {
      done.add(material)
      const prev = material.onBeforeCompile
      csm.setupMaterial(material)
      if (material.onBeforeCompile !== prev) {
        const csmHook = material.onBeforeCompile
        material.onBeforeCompile = (...args) => { prev.apply(material, args); csmHook.apply(material, args) }
      }
    }
    return original(cam, sc, geom, material, object, group)
  }
  return csm
}
```

Use it:

```typescript
scene.add(new THREE.AmbientLight(0xffffff, 0.4)) // fill, so shadows aren't pure black
const csm = createCsmSun(scene, camera, renderer)
// in the render loop, BEFORE renderer.render(...):
csm.update()
```

Forgetting `csm.update()` is the one easy mistake — shadows then won't follow the camera.

## Intensity

- **AmbientLight**: `0.3–0.6` (fill light)
- **CSM lightIntensity**: `1–3` (sun-like, affects entire scene)
- **PointLight / SpotLight**: `1–5` with reasonable `distance` (e.g. `10–50`)

## Runtime cost: keep the light set fixed

Three.js bakes the **number** of lights (and of shadow-casting lights) into every material's shader. Adding or removing a light — or toggling a light's `castShadow` — at runtime forces a **recompile of all materials**, which stalls the frame. Spawning a light per effect (a muzzle flash, an explosion) produces a visible hitch on every shot.

- Decide the light rig once at startup and keep the count fixed.
- For muzzle flashes, explosions, and pulses, **do not add a light**. Animate the `intensity`/`color` of one pre-created, normally-dim light, or fake the glow with an emissive material or an additive sprite. If you genuinely need moving light sources, pool a few reusable ones created up front.
- The same applies to materials: changing a material's *defines* (e.g. adding/removing a map) recompiles too — prefer animating a uniform or `color`.

## Environment lighting (IBL) for a non-flat look

Ambient-only or hemisphere-only lighting looks flat and gray because nothing gives surfaces form. What reads as "a real place" is image-based fill + a sun + textured materials:

- Set `scene.environment` from an HDR (Market `environment` assets ship one) so materials pick up real image-based reflections and fill light.
- Add one directional/CSM "sun" for shape and shadows.
- Tone-map the HDR range with `renderer.toneMapping = ACESFilmicToneMapping` and exposure ~1.

Flat ambient light + solid-color (untextured) materials is exactly the "gray clay" look — fix it with IBL, a sun, and real textures (see the `materials` skill).

### The visible sky must be an equirectangular skybox, not a flat image

To show the sky behind the scene, assign the equirectangular panorama to `scene.background` **and set its mapping**, so Three.js wraps it around the world as a skybox that stays put as the camera turns:

```typescript
const sky = await new TextureLoader().loadAsync('/environment/<name>-background.webp')
sky.mapping = EquirectangularReflectionMapping // without this it renders as a flat 2D screen image
sky.colorSpace = SRGBColorSpace
scene.background = sky
```

Never parent a sky image to the camera — that pins a flat picture to the view instead of giving the world a real horizon.
