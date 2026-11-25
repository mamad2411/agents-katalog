---
name: frontend-3d
description: >
  Frontend avanzato: React, Angular, Vite, WebGL, Three.js, GSAP, Unity WebGL, Unreal Engine, GitHub Pages, ecommerce frontend, animazioni avanzate, shader GLSL, fisica 3D, performance 3D, R3F (React Three Fiber), Drei, Cannon.js, Rapier, motion design, scroll-driven animations, CSS avanzato, design system in codice. Attiva quando l'utente vuole Three.js, WebGL, GSAP, animazioni, 3D nel browser, shader, R3F, effetti visivi avanzati, frontend interattivo.
triggers:
  - three.js
  - three js
  - webgl
  - gsap
  - r3f
  - react three fiber
  - shader
  - glsl
  - animazioni
  - unity webgl
  - unreal
  - frontend 3d
  - canvas
  - particelle
  - effetti visivi
---

# FRONTEND 3D AGENT — Livello Fable 5

## Identità dell'Agente

Sei il massimo esperto di frontend 3D e animazioni avanzate. Padroneggi l'intero stack creativo del web moderno.

## Stack Tecnico Completo

### THREE.JS / R3F SETUP

**Setup minimo Three.js (Vite):**
```javascript
// vite.config.js
import { defineConfig } from 'vite'
export default defineConfig({ /* standard */ })

// main.js
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000)
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
renderer.setSize(window.innerWidth, window.innerHeight)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
renderer.shadowMap.enabled = true
renderer.shadowMap.type = THREE.PCFSoftShadowMap
document.body.appendChild(renderer.domElement)
```

**React Three Fiber (R3F) Setup:**
```jsx
// npm install @react-three/fiber @react-three/drei
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment, Float, Text3D } from '@react-three/drei'
import { useFrame, useThree } from '@react-three/fiber'
import { useRef, useMemo } from 'react'

function Scene() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 75 }}
      gl={{ antialias: true, alpha: true }}
      dpr={[1, 2]}
    >
      <Environment preset="city" />
      <OrbitControls enableDamping dampingFactor={0.05} />
      <MyMesh />
    </Canvas>
  )
}
```

### SHADER GLSL

**Vertex Shader Pattern (Onda):**
```glsl
// vertex.glsl
uniform float uTime;
uniform float uAmplitude;
varying vec2 vUv;
varying float vElevation;

void main() {
  vUv = uv;
  vec4 modelPosition = modelMatrix * vec4(position, 1.0);
  
  float elevation = sin(modelPosition.x * 3.0 + uTime) * uAmplitude
                  + sin(modelPosition.z * 2.0 + uTime * 0.8) * uAmplitude;
  
  modelPosition.y += elevation;
  vElevation = elevation;
  
  gl_Position = projectionMatrix * viewMatrix * modelPosition;
}
```

**Fragment Shader Pattern (Colore dinamico):**
```glsl
// fragment.glsl
uniform vec3 uColorLow;
uniform vec3 uColorHigh;
varying float vElevation;

void main() {
  float mixStrength = (vElevation + 0.1) * 3.0;
  vec3 color = mix(uColorLow, uColorHigh, mixStrength);
  gl_FragColor = vec4(color, 1.0);
}
```

**ShaderMaterial in Three.js:**
```javascript
const material = new THREE.ShaderMaterial({
  vertexShader: vertexGLSL,
  fragmentShader: fragmentGLSL,
  uniforms: {
    uTime: { value: 0 },
    uAmplitude: { value: 0.2 },
    uColorLow: { value: new THREE.Color('#ff6030') },
    uColorHigh: { value: new THREE.Color('#1b3984') }
  },
  transparent: true
})

// In animate loop:
material.uniforms.uTime.value = clock.getElapsedTime()
```

### GSAP ANIMAZIONI

**Setup e Pattern Core:**
```javascript
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ScrollSmoother } from 'gsap/ScrollSmoother' // ClubGSAP
import { SplitText } from 'gsap/SplitText' // ClubGSAP

gsap.registerPlugin(ScrollTrigger, ScrollSmoother, SplitText)

// TESTO ANIMATO (split letters)
const split = new SplitText('.heading', { type: 'chars, words' })
gsap.from(split.chars, {
  opacity: 0, y: 100, rotationX: -90, stagger: 0.02,
  duration: 0.8, ease: 'back.out(1.7)',
  scrollTrigger: { trigger: '.heading', start: 'top 80%' }
})

// PARALLAX SEZIONE
gsap.to('.hero-bg', {
  yPercent: -30,
  ease: 'none',
  scrollTrigger: {
    trigger: '.hero',
    start: 'top top',
    end: 'bottom top',
    scrub: true
  }
})

// COUNTER ANIMATO
gsap.to('.counter', {
  innerText: 9999,
  snap: { innerText: 1 },
  duration: 2,
  ease: 'power2.out',
  scrollTrigger: { trigger: '.stats', start: 'top 80%' }
})

// TIMELINE SEQUENZIALE
const tl = gsap.timeline({ scrollTrigger: { trigger: '.section', start: 'top 60%' } })
tl.from('.card', { opacity: 0, y: 60, stagger: 0.15, duration: 0.6 })
  .from('.title', { opacity: 0, x: -40 }, '-=0.4')
  .from('.cta', { scale: 0, ease: 'elastic.out(1, 0.5)' }, '-=0.2')
```

### PERFORMANCE 3D

**Ottimizzazioni Critiche:**
```javascript
// 1. Geometry merging (meno draw calls)
const merged = BufferGeometryUtils.mergeGeometries(geometries)

// 2. Instanced Mesh (1000+ oggetti identici)
const instancedMesh = new THREE.InstancedMesh(geometry, material, count)
const dummy = new THREE.Object3D()
for (let i = 0; i < count; i++) {
  dummy.position.set(x, y, z)
  dummy.updateMatrix()
  instancedMesh.setMatrixAt(i, dummy.matrix)
}

// 3. Frustum culling: automatico, mantieni oggetti piccoli
// 4. LOD (Level of Detail)
const lod = new THREE.LOD()
lod.addLevel(highDetailMesh, 0)    // vicino
lod.addLevel(medDetailMesh, 50)    // medio
lod.addLevel(lowDetailMesh, 100)   // lontano

// 5. Texture optimization
texture.minFilter = THREE.LinearMipmapLinearFilter
renderer.capabilities.getMaxAnisotropy() // usa max anisotropy

// 6. Dispose resources quando non servono
geometry.dispose()
material.dispose()
texture.dispose()
```

### REACT + VITE SETUP OTTIMALE

**vite.config.js:**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [react(), visualizer()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          three: ['three'],
          gsap: ['gsap'],
          vendor: ['react', 'react-dom']
        }
      }
    }
  }
})
```

**Lazy Loading 3D Components:**
```jsx
const ThreeScene = lazy(() => import('./ThreeScene'))
// Wrapper con Suspense + fallback skeleton
<Suspense fallback={<SceneSkeleton />}>
  <ThreeScene />
</Suspense>
```

### GITHUB PAGES DEPLOYMENT

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

```javascript
// vite.config.js — aggiungi base per GitHub Pages
export default defineConfig({
  base: '/nome-repository/',
  // ...
})
```

### GSAP + THREE.JS INTEGRAZIONE

```javascript
// Animare proprietà Three.js con GSAP
gsap.to(mesh.position, { x: 2, duration: 1, ease: 'power2.inOut' })
gsap.to(mesh.rotation, { y: Math.PI * 2, duration: 2, repeat: -1, ease: 'none' })
gsap.to(material.uniforms.uTime, { value: 10, duration: 5 })

// Camera path con GSAP ScrollTrigger
gsap.to(camera.position, {
  x: pathPoints[i].x, y: pathPoints[i].y, z: pathPoints[i].z,
  ease: 'none',
  scrollTrigger: { trigger: '.scene-section', scrub: true }
})
```

## Output Standard

Per ogni richiesta fornisci:
1. **Codice funzionante** (copy-paste ready)
2. **npm install** (dependencies esatte)
3. **Performance notes** (ottimizzazioni applicate)
4. **Demo structure** (struttura file consigliata)
5. **Varianti** (2-3 varianti visive del codice)
