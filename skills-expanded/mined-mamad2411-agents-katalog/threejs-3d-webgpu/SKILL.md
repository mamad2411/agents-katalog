---
name: threejs-3d-webgpu
description: Create 3D applications and content for the web using Three.js with expert knowledge of WebGPU and shaders. Use this skill when building 3D scenes, working with geometries, materials, lighting, cameras, animations, custom shaders (GLSL/WGSL), post-processing effects, or leveraging WebGPU compute capabilities via TSL (Three Shading Language). Also triggers on "three.js", "threejs", "WebGL 3D", "WebGPU", "3D scene", "3D animation", "GLTF model", "3D game", "GLSL shader", "WGSL shader", "TSL", "node material", "OrbitControls", "bloom effect", "instanced mesh", "raycasting 3D", "EffectComposer", "MeshStandardMaterial", or any request to build a 3D web experience.
---

# Three.js 3D Web Development

Three.js is a powerful JavaScript library for creating 3D graphics in the browser. It supports both WebGL and WebGPU renderers, with a node-based material system (TSL) for advanced shader development.

**Documentation**: https://threejs.org/docs/
**Examples**: https://threejs.org/examples/

## Project Setup

### Installation

```bash
npm install three
```

### Basic HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { margin: 0; }
    canvas { display: block; }
  </style>
</head>
<body>
  <script type="importmap">
    {
      "imports": {
        "three": "https://cdn.jsdelivr.net/npm/three@0.170/build/three.module.js",
        "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170/examples/jsm/"
      }
    }
  </script>
  <script type="module" src="main.js"></script>
</body>
</html>
```

## Core Concepts

### Basic Scene Setup

```javascript
import * as THREE from 'three';

// Scene - container for all objects
const scene = new THREE.Scene();

// Camera - defines view perspective
const camera = new THREE.PerspectiveCamera(
  75,                                    // FOV (degrees)
  window.innerWidth / window.innerHeight, // Aspect ratio
  0.1,                                   // Near clipping plane
  1000                                   // Far clipping plane
);
camera.position.z = 5;

// Renderer - draws the scene
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();
```

### Using WebGPU Renderer

```javascript
import * as THREE from 'three';
import WebGPURenderer from 'three/addons/renderers/webgpu/WebGPURenderer.js';
import { WebGPU } from 'three/addons/capabilities/WebGPU.js';

// Check WebGPU support
if (!WebGPU.isAvailable()) {
  document.body.appendChild(WebGPU.getErrorMessage());
  throw new Error('WebGPU not supported');
}

const renderer = new WebGPURenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// Must initialize async
await renderer.init();
```

## Geometries

### Built-in Geometries

```javascript
// Box
const boxGeometry = new THREE.BoxGeometry(1, 1, 1);

// Sphere
const sphereGeometry = new THREE.SphereGeometry(0.5, 32, 32);

// Plane
const planeGeometry = new THREE.PlaneGeometry(10, 10);

// Cylinder
const cylinderGeometry = new THREE.CylinderGeometry(0.5, 0.5, 1, 32);

// Torus
const torusGeometry = new THREE.TorusGeometry(0.5, 0.2, 16, 100);

// Torus Knot
const torusKnotGeometry = new THREE.TorusKnotGeometry(0.5, 0.15, 100, 16);
```

### Custom BufferGeometry

```javascript
const geometry = new THREE.BufferGeometry();

// Vertices (3 floats per vertex: x, y, z)
const vertices = new Float32Array([
  -1, -1, 0,
   1, -1, 0,
   1,  1, 0,
  -1,  1, 0
]);

// Indices (triangles)
const indices = new Uint16Array([0, 1, 2, 0, 2, 3]);

// UVs (2 floats per vertex: u, v)
const uvs = new Float32Array([
  0, 0,
  1, 0,
  1, 1,
  0, 1
]);

geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
geometry.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
geometry.setIndex(new THREE.BufferAttribute(indices, 1));
geometry.computeVertexNormals();
```

## Materials

### Standard Materials

```javascript
// Basic (unlit, no shadows)
const basicMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });

// Lambert (diffuse lighting)
const lambertMaterial = new THREE.MeshLambertMaterial({ color: 0x00ff00 });

// Phong (specular highlights)
const phongMaterial = new THREE.MeshPhongMaterial({
  color: 0x0000ff,
  shininess: 100
});

// Standard (PBR - physically based)
const standardMaterial = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  metalness: 0.5,
  roughness: 0.5
});

// Physical (advanced PBR)
const physicalMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xffffff,
  metalness: 0.0,
  roughness: 0.1,
  transmission: 1.0,  // Glass-like
  thickness: 0.5,
  clearcoat: 1.0,
  clearcoatRoughness: 0.1
});
```

### Material Properties

```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  map: texture,              // Diffuse/albedo map
  normalMap: normalTexture,  // Normal map
  roughnessMap: roughTex,    // Roughness map
  metalnessMap: metalTex,    // Metalness map
  aoMap: aoTexture,          // Ambient occlusion
  emissive: 0x000000,        // Emissive color
  emissiveMap: emissiveTex,  // Emissive map
  envMap: envTexture,        // Environment map
  transparent: true,
  opacity: 0.5,
  side: THREE.DoubleSide,    // Render both sides
  wireframe: false
});
```

## Meshes and Objects

```javascript
// Create mesh (geometry + material)
const mesh = new THREE.Mesh(geometry, material);

// Transform
mesh.position.set(0, 1, 0);
mesh.rotation.set(0, Math.PI / 4, 0);
mesh.scale.set(2, 2, 2);

// Add to scene
scene.add(mesh);

// Groups
const group = new THREE.Group();
group.add(mesh1);
group.add(mesh2);
scene.add(group);
```

### Instanced Mesh (Performance)

```javascript
const count = 1000;
const mesh = new THREE.InstancedMesh(geometry, material, count);

const matrix = new THREE.Matrix4();
const position = new THREE.Vector3();
const rotation = new THREE.Euler();
const quaternion = new THREE.Quaternion();
const scale = new THREE.Vector3(1, 1, 1);

for (let i = 0; i < count; i++) {
  position.set(Math.random() * 10 - 5, Math.random() * 10, Math.random() * 10 - 5);
  rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
  quaternion.setFromEuler(rotation);
  matrix.compose(position, quaternion, scale);
  mesh.setMatrixAt(i, matrix);
}
mesh.instanceMatrix.needsUpdate = true;
scene.add(mesh);
```

## Lighting

```javascript
// Ambient (uniform light everywhere)
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

// Directional (sun-like, parallel rays)
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 5);
directionalLight.castShadow = true;
scene.add(directionalLight);

// Point (omni-directional from a point)
const pointLight = new THREE.PointLight(0xffffff, 1, 100);
pointLight.position.set(0, 5, 0);
scene.add(pointLight);

// Spot (cone of light)
const spotLight = new THREE.SpotLight(0xffffff, 1);
spotLight.position.set(0, 10, 0);
spotLight.angle = Math.PI / 6;
spotLight.penumbra = 0.2;
spotLight.castShadow = true;
scene.add(spotLight);

// Hemisphere (sky + ground colors)
const hemiLight = new THREE.HemisphereLight(0x87ceeb, 0x3d5c35, 0.6);
scene.add(hemiLight);

// RectArea (soft box light)
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
RectAreaLightUniformsLib.init();
const rectLight = new THREE.RectAreaLight(0xffffff, 5, 4, 2);
rectLight.position.set(0, 5, 0);
scene.add(rectLight);
```

### Shadows

```javascript
// Enable shadows on renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Light casts shadows
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
directionalLight.shadow.camera.near = 0.5;
directionalLight.shadow.camera.far = 50;
directionalLight.shadow.camera.left = -10;
directionalLight.shadow.camera.right = 10;
directionalLight.shadow.camera.top = 10;
directionalLight.shadow.camera.bottom = -10;

// Objects cast and receive shadows
mesh.castShadow = true;
mesh.receiveShadow = true;
floor.receiveShadow = true;
```

## Cameras

```javascript
// Perspective (realistic 3D)
const perspectiveCamera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);

// Orthographic (no perspective distortion)
const frustumSize = 10;
const orthographicCamera = new THREE.OrthographicCamera(
  -frustumSize * aspect / 2,
  frustumSize * aspect / 2,
  frustumSize / 2,
  -frustumSize / 2,
  0.1,
  1000
);
```

### Camera Controls

```javascript
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 2;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI / 2; // Limit vertical rotation

// Update in animation loop
function animate() {
  controls.update();
  renderer.render(scene, camera);
}
```

## Textures

```javascript
const textureLoader = new THREE.TextureLoader();

// Load texture
const texture = textureLoader.load('texture.jpg', (tex) => {
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(4, 4);
  tex.colorSpace = THREE.SRGBColorSpace;
});

// Cube texture (skybox/environment)
const cubeTextureLoader = new THREE.CubeTextureLoader();
const envMap = cubeTextureLoader.load([
  'px.jpg', 'nx.jpg',  // positive/negative X
  'py.jpg', 'ny.jpg',  // positive/negative Y
  'pz.jpg', 'nz.jpg'   // positive/negative Z
]);
scene.background = envMap;
scene.environment = envMap;
```

## Loading 3D Models

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

gltfLoader.load('model.glb', (gltf) => {
  const model = gltf.scene;
  
  // Enable shadows for all meshes
  model.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });
  
  scene.add(model);
  
  // Handle animations
  if (gltf.animations.length > 0) {
    const mixer = new THREE.AnimationMixer(model);
    const action = mixer.clipAction(gltf.animations[0]);
    action.play();
  }
});
```

## Animation

### Animation Loop with Clock

```javascript
const clock = new THREE.Clock();

function animate() {
  const delta = clock.getDelta();
  const elapsed = clock.getElapsedTime();
  
  // Rotate mesh
  mesh.rotation.y += delta;
  
  // Update animation mixer
  mixer?.update(delta);
  
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

### Tween Animation

```javascript
import gsap from 'gsap';

// Animate position
gsap.to(mesh.position, {
  x: 5,
  y: 2,
  duration: 2,
  ease: 'power2.inOut'
});

// Animate material
gsap.to(mesh.material, {
  opacity: 0,
  duration: 1
});
```

## Custom Shaders (WebGL/GLSL)

### ShaderMaterial

```javascript
const shaderMaterial = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color(0xff0000) },
    uTexture: { value: texture }
  },
  vertexShader: `
    uniform float uTime;
    varying vec2 vUv;
    varying vec3 vNormal;
    
    void main() {
      vUv = uv;
      vNormal = normalize(normalMatrix * normal);
      
      vec3 pos = position;
      pos.z += sin(pos.x * 5.0 + uTime) * 0.1;
      
      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform vec3 uColor;
    uniform sampler2D uTexture;
    
    varying vec2 vUv;
    varying vec3 vNormal;
    
    void main() {
      vec4 texColor = texture2D(uTexture, vUv);
      vec3 light = normalize(vec3(1.0, 1.0, 1.0));
      float diffuse = max(dot(vNormal, light), 0.0);
      
      gl_FragColor = vec4(texColor.rgb * uColor * diffuse, 1.0);
    }
  `,
  transparent: true
});

// Update uniform in animation loop
function animate() {
  shaderMaterial.uniforms.uTime.value = clock.getElapsedTime();
}
```

## TSL - Three Shading Language (WebGPU)

TSL is a JavaScript-based shader system for WebGPU that compiles to WGSL.

### Basic TSL Material

```javascript
import { MeshStandardNodeMaterial } from 'three/webgpu';
import { color, uv, sin, time, texture, normalMap } from 'three/tsl';

const material = new MeshStandardNodeMaterial();

// Animated color
material.colorNode = color(0xff0000).mul(sin(time).mul(0.5).add(0.5));

// Custom UV distortion
const distortedUV = uv().add(sin(uv().mul(10).add(time)).mul(0.02));
material.colorNode = texture(myTexture, distortedUV);
```

### TSL Vertex Displacement

```javascript
import { 
  MeshStandardNodeMaterial, 
  positionLocal, 
  normalLocal,
  sin, 
  time, 
  float 
} from 'three/tsl';

const material = new MeshStandardNodeMaterial();

// Displacement along normal
const displacement = sin(positionLocal.x.mul(10).add(time)).mul(0.1);
material.positionNode = positionLocal.add(normalLocal.mul(displacement));
```

### TSL Custom Functions

```javascript
import { 
  Fn, 
  vec3, 
  float, 
  sin, 
  cos, 
  time,
  uv 
} from 'three/tsl';

// Define custom function
const wave = Fn(([amplitude, frequency, offset]) => {
  return sin(uv().x.mul(frequency).add(time).add(offset)).mul(amplitude);
});

// Use in material
const waveResult = wave(float(0.1), float(10), float(0));
material.positionNode = positionLocal.add(vec3(0, waveResult, 0));
```

### TSL Compute Shaders

```javascript
import { WebGPURenderer } from 'three/webgpu';
import { 
  compute, 
  storage, 
  instanceIndex, 
  float, 
  vec3,
  sin,
  time 
} from 'three/tsl';

// Create storage buffer
const count = 1000;
const positionBuffer = new THREE.StorageBufferAttribute(
  new Float32Array(count * 3), 3
);

// Define compute shader
const computeShader = Fn(() => {
  const index = instanceIndex;
  const x = float(index).mod(10).sub(5);
  const z = float(index).div(10).floor().sub(5);
  const y = sin(x.add(time)).mul(0.5);
  
  storage(positionBuffer, 'vec3', index).assign(vec3(x, y, z));
});

// Create compute node
const computeNode = computeShader().compute(count);

// Execute in render loop
await renderer.computeAsync(computeNode);
```

## Post-Processing

### EffectComposer (WebGL)

```javascript
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const composer = new EffectComposer(renderer);

// Render the scene
composer.addPass(new RenderPass(scene, camera));

// Bloom effect
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,  // strength
  0.4,  // radius
  0.85  // threshold
);
composer.addPass(bloomPass);

// Output (handles color space)
composer.addPass(new OutputPass());

// Render with composer
function animate() {
  composer.render();
}
```

### PostProcessing (WebGPU)

```javascript
import { PostProcessing } from 'three/webgpu';
import { bloom, pass } from 'three/tsl';

const postProcessing = new PostProcessing(renderer);
const scenePass = pass(scene, camera);

// Add bloom
postProcessing.outputNode = bloom(scenePass, {
  strength: 1.5,
  radius: 0.4,
  threshold: 0.85
});

// Render
function animate() {
  postProcessing.render();
}
```

## Performance Optimization

### Instancing

```javascript
// Use InstancedMesh for many identical objects
const mesh = new THREE.InstancedMesh(geometry, material, 10000);
```

### Level of Detail (LOD)

```javascript
const lod = new THREE.LOD();

// High detail (close)
lod.addLevel(highDetailMesh, 0);

// Medium detail
lod.addLevel(mediumDetailMesh, 50);

// Low detail (far)
lod.addLevel(lowDetailMesh, 100);

scene.add(lod);
```

### Batched Mesh

```javascript
const batchedMesh = new THREE.BatchedMesh(maxGeometries, maxVertices, maxIndices);

// Add geometries
const geomId = batchedMesh.addGeometry(geometry);

// Add instances
const instanceId = batchedMesh.addInstance(geomId);
batchedMesh.setMatrixAt(instanceId, matrix);
```

### Dispose Resources

```javascript
// Clean up when removing objects
geometry.dispose();
material.dispose();
texture.dispose();
renderer.dispose();
```

## Responsive Handling

```javascript
function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener('resize', onWindowResize);
```

## Raycasting (Mouse Interaction)

```javascript
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseClick(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children, true);
  
  if (intersects.length > 0) {
    const object = intersects[0].object;
    console.log('Clicked:', object);
  }
}

window.addEventListener('click', onMouseClick);
```

## Quick Reference

### Common Classes

| Class | Purpose |
|-------|---------|
| `Scene` | Container for all 3D objects |
| `PerspectiveCamera` | Standard 3D camera |
| `WebGLRenderer` | WebGL rendering |
| `WebGPURenderer` | WebGPU rendering |
| `Mesh` | Geometry + Material |
| `Group` | Container for objects |
| `BufferGeometry` | Vertex data |
| `MeshStandardMaterial` | PBR material |
| `ShaderMaterial` | Custom GLSL shaders |
| `NodeMaterial` | TSL-based materials |

### Common Addons

| Addon | Import Path |
|-------|-------------|
| OrbitControls | `three/addons/controls/OrbitControls.js` |
| GLTFLoader | `three/addons/loaders/GLTFLoader.js` |
| DRACOLoader | `three/addons/loaders/DRACOLoader.js` |
| RGBELoader | `three/addons/loaders/RGBELoader.js` |
| EffectComposer | `three/addons/postprocessing/EffectComposer.js` |
| WebGPURenderer | `three/addons/renderers/webgpu/WebGPURenderer.js` |

### TSL Functions

| Function | Purpose |
|----------|---------|
| `color()` | Create color node |
| `uv()` | UV coordinates |
| `time` | Elapsed time |
| `sin()`, `cos()` | Trigonometry |
| `texture()` | Sample texture |
| `positionLocal` | Vertex position |
| `normalLocal` | Vertex normal |
| `Fn()` | Define custom function |
| `compute()` | Create compute shader |

## Related Skills

### game-math
Vectors, matrices, quaternions, coordinate systems, camera projection, and kinematics — the full mathematical toolkit that Three.js uses under the hood. Understanding `Vector3`, `Matrix4`, `Quaternion`, and `Euler` is essential for non-trivial Three.js work.

**Use alongside this skill when:** you need to manually compose transforms, build a custom camera rig, work with frustum math, or understand the math behind something Three.js is doing internally.

### trigonometry
Radians, sin/cos/atan2, circular motion, oscillations, spherical coordinates, and rotation matrices. Three.js animations and procedural geometry almost always involve trig.

**Use alongside this skill when:** the scene has objects orbiting a point, wave-based vertex displacement, `sin(time)` oscillations, or converting between spherical and Cartesian coordinates for camera placement.

### physics
Numerical integration, force accumulation, rigid body dynamics, spring systems, soft bodies (PBD), and SPH fluids — framed as time-stepped simulation loops that map naturally onto Three.js `clock.getDelta()` render loops.

**Use alongside this skill when:** the Three.js scene needs physics simulation (falling objects, cloth, fluid, constraints) via Rapier, Cannon-es, or Ammo.js, or when you're implementing custom physics directly.

### animation-specialist
Broad motion design: easing curves, spring dynamics, keyframe choreography, timeline sequencing, and the math behind smooth motion.

**Use alongside this skill when:** the Three.js scene has complex choreographed animation sequences, character rigs, or needs easing/spring behaviour beyond basic `clock.getDelta()` integration. Use **instead of** this skill when the user needs 2D DOM animation and Three.js isn't involved.

### gsap
Professional JavaScript animation — tweens, timelines, Flip, Observer, and ScrollTrigger. Three.js + GSAP is a common and powerful pairing: GSAP drives object positions/rotations/uniforms while Three.js renders them.

**Use alongside this skill when:** Three.js camera moves, object reveals, or shader uniform transitions need precise easing, sequencing, or scroll-based control that `requestAnimationFrame` alone doesn't provide.

### gsap-scrolltrigger
Scroll-driven animation using GSAP ScrollTrigger — pinning, scrubbing, parallax, snap points. Often used to drive Three.js scene state as the user scrolls through a page.

**Use alongside this skill when:** the Three.js canvas is embedded in a scroll-driven storytelling page and scene state (camera position, object visibility, shader uniforms) should be tied to scroll progress.

### web-visual-effects
GPU-accelerated visual effects at the raw WebGL/WebGPU level — custom GLSL/WGSL shaders, compute pipelines, particle systems, and post-processing without the Three.js abstraction layer.

**Use instead of this skill when:** the effect requires direct WebGPU compute pipeline control that Three.js TSL doesn't expose, or when bundle size matters and Three.js is too heavy for the use case.

### p5js-creative-coding
Generative and creative coding using p5.js — 2D canvas drawing, Perlin noise, interactive sketches, and particle systems without a 3D scene graph.

**Use instead of this skill when:** the user wants a 2D generative art sketch or interactive canvas experience and doesn't need a 3D scene graph, model loading, or WebGPU compute.

### frontend-design
Creative direction and polished interface implementation — layout, typography, colour, and component design as a unified whole.

**Use before this skill when:** the Three.js canvas needs to live inside a well-designed web page and the overall layout, colour palette, and UI haven't been established yet.
