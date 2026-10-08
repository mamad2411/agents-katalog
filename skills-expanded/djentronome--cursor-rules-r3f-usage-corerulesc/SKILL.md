---
description: Use when adding 3D or canvas elements using react-three-fiber.
globs: 
alwaysApply: false
---
Got it. Here's a **compressed, high-signal Cursor rule** that captures **usage patterns**, **pitfalls**, and **best practices** for `@react-three/fiber`, `drei`, `zustand`, `leva`, and related tools—optimized for *always-on inclusion* in agent context.

---

### 📜 `r3f-usage-core.rule.md`

````md
# Rule: Use react-three-fiber stack for 3D game UIs

## Applies to
Any 3D or audio-reactive visualizations using Three.js in React.

## Core Stack
- `@react-three/fiber`: React renderer for Three.js
- `@react-three/drei`: Helpers (controls, text, stages)
- `zustand`: Global state management
- `leva`: Debug/tweak UI
- `three`: Only for low-level control
- `@react-three/postprocessing`: Optional visual polish

---

## ✅ Patterns

### Canvas Setup
```tsx
<Canvas camera={{ position: [0, 5, 10], fov: 50 }}>
  <ambientLight intensity={1.2} />
  <group>{/* notes, lanes, hitboxes */}</group>
</Canvas>
````

### Animating with `useFrame`

```ts
useFrame((state, delta) => {
  meshRef.current.position.y -= speed * delta
})
```

### Zustand Store (Game State)

```ts
const useStore = create(() => ({
  time: 0, bpm: 120, playing: false, setTime: (t) => set({ time: t }),
}))
```

### Leva Controls

```ts
const { bpm, offset } = useControls({ bpm: 120, offset: 0.1 })
```

---

## ⚠️ Warning Signs

* ❌ Using `useState` instead of `zustand` for timing/game state
* ❌ Mixing DOM/UI and Canvas space (e.g. `<div>` inside `<Canvas>`)
* ❌ Using raw `THREE.Scene` or imperatively mutating objects unnecessarily
* ❌ Animating with `setInterval` or requestAnimationFrame outside `useFrame`

---

## Recommended File Structure

Follow [react-component-standards.rules.mdc](mdc:.cursor/rules/react-component-standards.rules.mdc)

---

## Architecture Notes

* Use `Canvas` as the root scene wrapper, all 3D logic lives within it
* Define scrolling logic inside `useFrame`-based hooks (`useScrollSync`)
* Model state via `zustand`; react-three-fiber reads from store
* Leva is dev-only — wrap in conditionals or env flags
* Three.js objects are treated as JSX, e.g. `<mesh>` instead of `new Mesh()`
* Import helpers from `@react-three/drei` first before rolling your own

---

## Performance Tips

* Batch geometry with `InstancedMesh` if rendering many repeated objects
* Memoize materials and geometries where possible
* Minimize re-renders — avoid using React state inside `useFrame`
* Use `drei/Bounds` and `drei/PerformanceMonitor` for optimization

---

## Related Rules

* `midi-handler.rule.ts` for integrating drum input
* [bpm-sync.rules..mdc](mdc:.cursor/rules/bpm-sync.rules..mdc) for converting song time to scroll offsets