---
name: r3f
description: "React Three Fiber skill for declarative 3D in React. USE when building React apps with Three.js, using @react-three/fiber, drei, zustand with 3D, or the user mentions R3F, react-three, Canvas component, useFrame, useThree. Even if they just say 'React 3D' or 'declarative Three.js'. For vanilla Three.js, see threejs skill. For WebGPU/TSL, see webgpu-threejs-tsl skill."
metadata:
  author: jonathan
  version: "1.0.0"
---

# React Three Fiber (R3F) Skill

Declarative Three.js in React via `@react-three/fiber`. Everything is a component.
Drei provides batteries-included helpers. Zustand handles state without re-render hell.

## Reference Files

- `references/patterns.md` — component architecture, scroll animations, HTML overlays, instancing, post-processing
- `references/recipes.md` — product configurator, 3D portfolio, data viz, adaptive quality

---

## Quick Start

### Installation

```bash
npm install three @react-three/fiber @react-three/drei
# Optional but recommended:
npm install zustand @react-three/postprocessing
```

### Canvas Setup

```tsx
import { Canvas } from '@react-three/fiber'

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', touchAction: 'none' }}>
      <Canvas
        shadows
        dpr={[1, 2]}
        camera={{ position: [0, 2, 5], fov: 50 }}
        gl={{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping }}
        performance={{ min: 0.5 }}
      >
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[5, 5, 5]}
          intensity={1}
          castShadow
          shadow-mapSize={[2048, 2048]}
        />
        <Scene />
      </Canvas>
    </div>
  )
}
```

Key `<Canvas>` props:
- `shadows` — enables shadow maps globally
- `dpr={[1, 2]}` — clamps device pixel ratio (saves GPU on retina)
- `performance={{ min: 0.5 }}` — allows adaptive DPR to drop to 50%
- `frameloop="demand"` — only render when `invalidate()` is called (static scenes)
- `flat` — disables tone mapping (for UI-heavy scenes)

---

## Core Hooks

### useFrame — The Render Loop

**GOLDEN RULE: NEVER call setState inside useFrame. Mutate refs instead.**

Every setState triggers a React re-render. At 60fps that's 60 re-renders/second = death.

```tsx
import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

function SpinningBox() {
  const meshRef = useRef<THREE.Mesh>(null!)

  useFrame((state, delta) => {
    // GOOD — mutate ref directly
    meshRef.current.rotation.y += delta
    // Access clock, camera, mouse, etc. from state
    meshRef.current.position.y = Math.sin(state.clock.elapsedTime)
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}
```

useFrame callback args:
- `state` — full R3F state: `clock`, `camera`, `mouse`, `viewport`, `scene`, `gl`, `size`
- `delta` — time since last frame in seconds (use for frame-rate-independent movement)

Priority: `useFrame(cb, priority)` — lower runs first. Default is 0.

### useThree — Access Fiber State

Always use a selector to avoid re-renders on every frame:

```tsx
// BAD — re-renders on every state change
const state = useThree()

// GOOD — only re-renders when viewport changes
const viewport = useThree((s) => s.viewport)

// GOOD — only re-renders when size changes
const { width, height } = useThree((s) => s.size)
```

Common selectors: `camera`, `gl`, `scene`, `viewport`, `size`, `mouse`, `clock`.

### useLoader

```tsx
import { useLoader } from '@react-three/fiber'
import { TextureLoader } from 'three'

function TexturedMesh() {
  const texture = useLoader(TextureLoader, '/textures/wood.jpg')
  return (
    <mesh>
      <planeGeometry args={[4, 4]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  )
}
```

Prefer drei's `useTexture` or `useGLTF` — they handle caching and preloading.

---

## Drei Essentials

Drei (`@react-three/drei`) is the standard helper library. Import only what you use.

### Controls

```tsx
import { OrbitControls } from '@react-three/drei'

<OrbitControls
  enableDamping
  dampingFactor={0.05}
  maxPolarAngle={Math.PI / 2}  // prevent flipping below ground
  minDistance={2}
  maxDistance={10}
/>
```

### Environment & Lighting

```tsx
import { Environment } from '@react-three/drei'

// Preset HDR environments (no extra files needed)
<Environment preset="city" background blur={0.5} />
// Presets: apartment, city, dawn, forest, lobby, night, park, studio, sunset, warehouse
```

### Loading 3D Models

```tsx
import { useGLTF } from '@react-three/drei'

function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} />
}

// Preload outside component
useGLTF.preload('/models/robot.glb')
```

For editable models, use `useGLTF` + clone or gltfjsx to generate typed components.

### HTML Overlays

```tsx
import { Html } from '@react-three/drei'

<mesh position={[0, 2, 0]}>
  <sphereGeometry />
  <meshStandardMaterial />
  <Html
    center
    distanceFactor={10}
    occlude
    style={{ pointerEvents: 'none', userSelect: 'none' }}
  >
    <div className="label">Hello 3D</div>
  </Html>
</mesh>
```

### Text

```tsx
import { Text } from '@react-three/drei'

<Text
  fontSize={0.5}
  color="white"
  anchorX="center"
  anchorY="middle"
  font="/fonts/Inter-Bold.woff"
>
  Hello World
</Text>
```

### Other Must-Know Drei Components

| Component | Use Case |
|-----------|----------|
| `Float` | Gentle floating animation |
| `MeshReflectorMaterial` | Reflective floors |
| `ContactShadows` | Soft ground shadows (cheaper than shadow maps) |
| `Sparkles` | Particle sparkle effect |
| `useProgress` | Loading progress for Suspense |
| `Preload` | Preload all useLoader assets |
| `AdaptiveDpr` | Auto-adjust DPR based on performance |
| `AdaptiveEvents` | Throttle pointer events under load |
| `BakeShadows` | Bake shadows once (static scenes) |
| `PerformanceMonitor` | Track FPS and trigger quality changes |
| `ScrollControls` | Scroll-driven 3D animations |
| `PresentationControls` | Drag-to-rotate for product views |
| `MeshTransmissionMaterial` | Glass/refractive materials |
| `Center` | Auto-center geometry |

---

## Zustand for 3D State

Zustand is the recommended state manager for R3F. It lives outside React's render cycle.

### Store Setup

```ts
import { create } from 'zustand'

interface GameStore {
  score: number
  color: string
  setColor: (c: string) => void
  increment: () => void
}

const useGameStore = create<GameStore>((set) => ({
  score: 0,
  color: '#ff6600',
  setColor: (color) => set({ color }),
  increment: () => set((s) => ({ score: s.score + 1 })),
}))
```

### Selective Subscriptions (Prevent Re-renders)

```tsx
// GOOD — only re-renders when color changes
const color = useGameStore((s) => s.color)

// BAD — re-renders on ANY store change
const store = useGameStore()
```

### Reading State in useFrame (Zero Re-renders)

```tsx
useFrame(() => {
  // getState() reads without subscribing — no re-renders ever
  const { score } = useGameStore.getState()
  meshRef.current.scale.setScalar(1 + score * 0.1)
})
```

### Transient Subscriptions

```tsx
useEffect(() => {
  const unsub = useGameStore.subscribe(
    (state) => state.color,
    (color) => {
      // Runs only when color changes, bypasses React entirely
      meshRef.current.material.color.set(color)
    }
  )
  return unsub
}, [])
```

---

## Performance Rules

### 1. Never setState in useFrame
Already said it. Saying it again. Mutate refs.

### 2. Memoize Geometry and Materials

```tsx
// BAD — creates new geometry every render
<mesh>
  <boxGeometry args={[1, 1, 1]} />
</mesh>

// GOOD — reuse with useMemo
const geometry = useMemo(() => new THREE.BoxGeometry(1, 1, 1), [])
const material = useMemo(() => new THREE.MeshStandardMaterial({ color: 'red' }), [])

<mesh geometry={geometry} material={material} />
```

Note: R3F auto-caches declarative `<boxGeometry />` with same args, so this mainly matters for complex/custom geometries.

### 3. React.memo for Static Components

```tsx
const StaticProp = React.memo(function StaticProp() {
  return (
    <mesh position={[0, 0, 0]}>
      <boxGeometry />
      <meshStandardMaterial color="gray" />
    </mesh>
  )
})
```

### 4. Instancing for Repeated Objects

Use `<instancedMesh>` for hundreds+ of similar objects. See `references/patterns.md`.

### 5. Adaptive Quality

```tsx
import { AdaptiveDpr, PerformanceMonitor } from '@react-three/drei'

<Canvas dpr={[1, 2]} performance={{ min: 0.5 }}>
  <AdaptiveDpr pixelated />
  <PerformanceMonitor
    onIncline={() => setQuality('high')}
    onDecline={() => setQuality('low')}
  />
  {/* ... */}
</Canvas>
```

### 6. frameloop="demand" for Static Scenes

```tsx
import { useThree } from '@react-three/fiber'

<Canvas frameloop="demand">
  <StaticScene />
</Canvas>

// Call invalidate() when something changes
function InteractiveObject() {
  const invalidate = useThree((s) => s.invalidate)
  return (
    <mesh onClick={() => { /* change something */ invalidate() }}>
      {/* ... */}
    </mesh>
  )
}
```

---

## Mobile Configuration

### Device Detection & Quality Tiers

```tsx
import { useMemo } from 'react'

function useDeviceTier() {
  return useMemo(() => {
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
    const gpu = (navigator as any).gpu
    const cores = navigator.hardwareConcurrency || 4

    if (isMobile && cores <= 4) return 'low'
    if (isMobile) return 'medium'
    if (cores >= 8) return 'high'
    return 'medium'
  }, [])
}

function App() {
  const tier = useDeviceTier()

  const config = {
    low:    { dpr: [1, 1],   shadows: false, envMapIntensity: 0.5 },
    medium: { dpr: [1, 1.5], shadows: true,  envMapIntensity: 0.8 },
    high:   { dpr: [1, 2],   shadows: true,  envMapIntensity: 1.0 },
  }[tier]

  return (
    <Canvas
      shadows={config.shadows}
      dpr={config.dpr as [number, number]}
    >
      <Scene envMapIntensity={config.envMapIntensity} />
      <AdaptiveDpr pixelated />
    </Canvas>
  )
}
```

### Required CSS

```css
/* Container must have explicit size */
.canvas-container {
  width: 100vw;
  height: 100vh;
  touch-action: none;    /* prevents browser gestures interfering with 3D controls */
  overflow: hidden;
  position: fixed;       /* or absolute — prevents scroll bounce */
  top: 0;
  left: 0;
}

/* Alternative: inline on parent div */
/* <div style={{ width: '100vw', height: '100vh', touchAction: 'none' }}> */
```

---

## Common Patterns Quick Reference

### Events

```tsx
<mesh
  onClick={(e) => { e.stopPropagation(); /* handle click */ }}
  onPointerOver={(e) => { document.body.style.cursor = 'pointer' }}
  onPointerOut={(e) => { document.body.style.cursor = 'auto' }}
>
```

R3F events are raycasted — they hit the first mesh and propagate. Always `stopPropagation()` if needed.

### Suspense for Loading

```tsx
import { Suspense } from 'react'
import { useProgress, Html } from '@react-three/drei'

function Loader() {
  const { progress } = useProgress()
  return <Html center>{progress.toFixed(0)}%</Html>
}

<Canvas>
  <Suspense fallback={<Loader />}>
    <Model url="/model.glb" />
  </Suspense>
</Canvas>
```

### Disposing Resources

R3F auto-disposes geometries, materials, and textures when components unmount.
For manual control: `<mesh dispose={null}>` to prevent auto-dispose (shared resources).

### TypeScript

```tsx
import { ThreeElements } from '@react-three/fiber'

// Extend JSX for custom elements
type MeshProps = ThreeElements['mesh']

function Box(props: MeshProps) {
  const ref = useRef<THREE.Mesh>(null!)
  return <mesh ref={ref} {...props} />
}
```

---

## Package Versions (as of 2025)

| Package | Version | Notes |
|---------|---------|-------|
| `@react-three/fiber` | 8.x | Stable, React 18+ |
| `@react-three/drei` | 9.x | Helpers |
| `@react-three/postprocessing` | 2.x | Effects |
| `three` | 0.160+ | Keep in sync with R3F peer dep |
| `zustand` | 4.x / 5.x | State management |

Always check R3F changelog when upgrading Three.js — breaking changes in Three often need R3F patches.
