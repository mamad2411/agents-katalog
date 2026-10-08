---
name: vtj-performance
description: Optimizes Three.js rendering performance. Use when rendering large numbers of objects, optimizing frame rates, implementing streaming, or managing memory in voxel/block-based scenes.
---

# vite-threejs Performance Optimization

## Overview

Performance patterns for voxel-based Three.js applications.

**Key techniques:**
- **InstancedMesh**: Batch render thousands of similar objects
- **Occlusion culling**: Skip hidden blocks
- **Geometry sharing**: Single geometry for all blocks
- **Idle queue**: Non-blocking chunk generation

## Quick Reference

| Technique | Use When | Benefit |
|-----------|----------|---------|
| InstancedMesh | 100+ similar objects | Reduced draw calls |
| Occlusion culling | Voxel terrain | Fewer vertices processed |
| Geometry sharing | Multiple meshes same shape | Lower memory |
| Swap-and-pop | Dynamic instance removal | O(1) deletion |
| Idle queue | Background tasks | No frame drops |

## InstancedMesh Pattern

```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1)  // Shared
const material = new THREE.MeshStandardMaterial({ color: 0x888888 })
const mesh = new THREE.InstancedMesh(geometry, material, count)

mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage)

// Set instance at index
mesh.setMatrixAt(index, matrix)
mesh.instanceMatrix.needsUpdate = true
```

**Full patterns:** See [references/instanced-mesh.md](references/instanced-mesh.md)

## O(1) Instance Removal

```javascript
// Swap last instance into deleted slot
const lastIndex = mesh.count - 1
if (index < lastIndex) {
  mesh.getMatrixAt(lastIndex, tempMatrix)
  mesh.setMatrixAt(index, tempMatrix)
}
mesh.count--
mesh.instanceMatrix.needsUpdate = true
```

**Implementation details:** See [references/swap-and-pop.md](references/swap-and-pop.md)

## Occlusion Culling

Skip blocks completely surrounded by other blocks:

```javascript
if (isBlockObscured(x, y, z)) return  // Skip rendering
renderBlock(x, y, z)
```

**Algorithm:** See [references/occlusion-culling.md](references/occlusion-culling.md)

## Idle Queue

```javascript
// Schedule work without blocking main thread
idleQueue.enqueue('chunk', () => {
  chunk.generateData()
}, priority)
```

**API reference:** See [references/idle-queue.md](references/idle-queue.md)

## Memory Management

```javascript
destroy() {
  // Dispose materials
  if (Array.isArray(mesh.material)) {
    mesh.material.forEach(m => m?.dispose())
  } else {
    mesh.material?.dispose()
  }
  
  // Remove from scene
  scene.remove(mesh)
  mesh = null
}
```

**Complete patterns:** See [references/memory-management.md](references/memory-management.md)

## Common Mistakes

- ❌ Creating geometry per object
- ❌ Using `splice()` for instance removal
- ❌ Forgetting `needsUpdate = true`
- ❌ Synchronous chunk generation

**Full catalog:** See [references/common-mistakes.md](references/common-mistakes.md)

## Configuration

```javascript
export const CHUNK_CONFIG = {
  chunkWidth: 64,      // Balance draw calls vs memory
  viewDistance: 1,     // 1 = 3x3 chunk grid
  unloadPadding: 1,    // Hysteresis for unloading
}
```

**Tuning guide:** See [references/configuration.md](references/configuration.md)
