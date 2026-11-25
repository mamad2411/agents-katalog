---
name: forgeax-engine-debug-draw
description: >-
  ForgeAX immediate-mode debug geometry. Use when visualizing positions, colliders,
  frustums, axes, or radii without creating ECS entities.
---

# forgeax-engine-debug-draw

> debug-draw visualizes gameplay facts: `app.debugDraw.line(a, b, RED)` draws wire geometry in the final frame without ECS entities/components/systems. GPU recording and frame analysis use [`forgeax-engine-rhi-debug`](../forgeax-engine-rhi-debug/SKILL.md). Use debug-draw for demos, physics tuning, cameras, and audio radii.

## Mental model

`@forgeax/engine-debug-draw` is an immediate-mode RHI convenience layer:

- Shape calls (`line` / `sphere` / `aabb` / `frustum` / `arrow` / `axes`) accumulate vertices in CPU staging. `arrow` uses a body and four tip lines, with default `tipLength = |end-start|/10`; `axes(worldMat,length)` draws RGB arrows along local XYZ, like Bevy `gizmos.axes`.
- At frame end, `flush(encoder, view, viewProj)` uploads staging, issues one draw, and clears staging for the next frame.
- Nothing persists: omitting a shape call removes it from the next frame.
- No ECS/render-graph/shader-registry dependency; the package compiles its own WGSL and creates its PSO.

Runtime users use automatic `app.debugDraw.*`; low-level RHI scripts use `createDebugDraw(...)` and explicit `flush(...)`.

### Dependency level alongside engine-math

| Package | Dependencies | Purpose |
|:--|:--|:--|
| `engine-math` | No ForgeAX dependencies | Vec / Mat / Quat / Color / frustum reconstruction. |
| `engine-debug-draw` | rhi + math + types | Wire overlay collection and GPU flush. |
| `engine-runtime` | debug-draw (thin glue) | Attach `app.debugDraw` during createApp. |

Runtime wiring lives in `packages/render/src/debug-draw-glue.ts`; debug-draw itself does not depend on runtime, ECS, render-graph, or shader.

## Integration paths

### Runtime path (automatic, recommended)

```ts
import { createApp } from '@forgeax/engine-runtime';

const app = await createApp({ canvas });

// In any update system or hook:
app.debugDraw.line([0, 0, 0], [1, 1, 1], [1, 0, 0, 1]);   // red line
app.debugDraw.sphere([0, 0, 0], 1, [0, 1, 0, 1]);          // green sphere
app.debugDraw.aabb([-1, -1, -1], [1, 1, 1], [0, 0, 1, 1]); // blue box
app.debugDraw.frustum(cameraViewProj, [1, 1, 0, 1]);        // yellow frustum
app.debugDraw.arrow([0, 0, 0], [0, 2, 0], [1, 1, 1, 1]);    // arrow (body + head); tipLength optional
app.debugDraw.axes(transform.world, 1);                     // local frame: X=red / Y=green / Z=blue arrows

// No manual flush -- runtime appends a DebugOverlay pass to the render graph
// and draws the staged vertices every frame.
```

- `createApp` attaches `app.debugDraw` through the `debug-draw-glue.ts` hook.
- Call shapes from update systems or other code; vertices accumulate and clear automatically at frame end.
- Runtime owns the GPU overlay: `app.debugDraw` is a CPU source the Renderer takes once per frame and draws in every view; update-only or non-drawing frames discard its geometry.
- An overlay failure skips the overlay and fires one `debug-overlay-failed` error per reason (`overlay-source-failed`, `overlay-upload-failed`, `overlay-pipeline-failed`); the scene frame continues. Read `renderer.inspect().debugOverlay` for the latest outcome.

### Low-level path (custom RHI and graph)

```ts
import { createDebugDraw } from '@forgeax/engine-debug-draw';
import { createShaderModule } from '@forgeax/engine-rhi-webgpu';

const r = await createDebugDraw({ device, queue, createShaderModule });
if (!r.ok) {
  switch (r.error.code) {
    case 'pipeline-create-failed':  /* ... */
    case 'buffer-allocation-failed': /* ... */
  }
}
const dd = r.value;

// Per-frame:
dd.line([0, 0, 0], [1, 1, 1], [1, 0, 0, 1]);
// ... more shape calls ...
dd.flush(encoder, swapChainView, cameraViewProj);

// When done:
dd.destroy();
```

- Supply `device`, `queue`, and the injected WGSL compilation factory `createShaderModule` from `@forgeax/engine-rhi-webgpu`.
- Call `flush(encoder, view, viewProj)` at the end of the custom render graph or capture script.
- `destroy()` releases GPU resources; subsequent shape calls are no-ops with one console warning, and flush returns `Result.err`.

## Core API quick reference

| API | Form | Vertex count |
|:--|:--|:--|
| `dd.line(a, b, color)` | `a: Vec3, b: Vec3, color: ColorLike => void` | 2 |
| `dd.sphere(center, radius, color, segments?)` | `center: Vec3, radius: number, color: ColorLike, segments?: number => void` | $3 \times 2 \times \text{segments}$ (default `segments=16`: 96) |
| `dd.aabb(min, max, color)` | `min: Vec3, max: Vec3, color: ColorLike => void` | 24 (12 edges) |
| `dd.frustum(viewProj, color)` | `viewProj: Mat4, color: ColorLike => void` | 24 (12 edges) |
| `dd.flush(encoder, view, viewProj)` | `encoder: RhiCommandEncoder, view: TextureView, viewProj: Mat4 => Result<void, DebugDrawError>` | -- |
| `dd.destroy()` | `() => void` | -- |

> `ColorLike` accepts plain `[r, g, b, a?]` tuples, `Float32Array`, or branded `Color` from `@forgeax/engine-math`; no `as Vec4` assertion is needed.

### Depth mode

| Mode | Behavior |
|:--|:--|
| `'always'` (default) | Draw overlays above the scene, ignoring depth. |
| `'less-equal'` | Foreground geometry occludes the overlay using scene depth. |

`createDebugDraw({ depthMode: 'less-equal', depthFormat: 'depth24plus' })` requires `depthFormat`. Each instance compiles one PSO for its fixed depth mode. To use both modes in one frame, create two instances (AC-06 demo).

### Capacity resize + truncation

| Trigger | Behavior |
|:--|:--|
| Vertices exceed capacity but remain below `MAX_VERTEX_CAPACITY` (1M) | Double capacity and log old/new sizes once. |
| Vertices exceed `MAX_VERTEX_CAPACITY` | Flush within the limit, discard overflow, and warn at most once per frame. |

Exported constants: `INITIAL_VERTEX_CAPACITY` (1024), `MAX_VERTEX_CAPACITY` (1_000_000), `VERTEX_STRIDE_BYTES` (16).

## Error model

`DebugDrawErrorCode` is a closed union. Each member carries `.code` / `.expected` / `.hint` / `.detail`, following AGENTS.md:

| `err.code` | Trigger | Actionable `.hint` |
|:--|:--|:--|
| `'pipeline-create-failed'` | PSO or shader compilation failure | `Pipeline creation failed: <rhiError>. Check WGSL syntax, vertex layout, and depth-stencil state.` |
| `'buffer-allocation-failed'` | GPU buffer allocation failure | `Buffer allocation failed: <rhiError>. Check available device memory and buffer usage flags.` |
| `'flushed-after-destroy'` | Flush after destruction | `DebugDraw was destroyed; create a new instance via createDebugDraw().` |
| `'viewProj-required'` | Missing viewProj at flush | `Pass a viewProj Mat4 to flush(encoder, view, viewProj).` |

Handle `err.code` exhaustively without default. `packages/debug-draw/src/errors.ts` owns the complete error contract.

## Pitfalls

- **Creating ECS mesh entities instead of `dd.line()`**: debug-draw is immediate-mode and needs no component registration. Mesh entities outlive a frame, can leave stale debug geometry, and freeze engine gaps into demos.
- **Missing `createShaderModule` injection**: import the WGSL factory from `@forgeax/engine-rhi-webgpu`; without it the package cannot create its PSO.
- **Missing `depthFormat` with `less-equal`**: the PSO needs `depthStencil.format`; supply `depthFormat: 'depth24plus'` to avoid `pipeline-create-failed`.
- **Confusing debug-draw and rhi-debug**: debug-draw draws gameplay wire overlays; rhi-debug records GPU calls for frame analysis. See the package README's distinction table.
- **Expecting shape calls to throw after destroy**: they are no-ops, write no staging, and warn only once. The next flush reports `Result.err({ code: 'flushed-after-destroy' })`.
- **Forgetting flush is idempotent**: empty staging returns `ok(undefined)` without `beginRenderPass` or GPU effects. A second flush in the same frame does not redraw.
- **Excessive sphere segments**: 10,000 segments produce 60,000 vertices and may trigger a capacity warning, but do not crash the frame. Default 16 segments yields 96 vertices.

## Further reading

- Shape signatures, depth modes, capacity behavior, and errors: `packages/debug-draw/README.md`.
- Closed error union and discriminated details: `packages/debug-draw/src/errors.ts`.
- `DebugDraw` class + `createDebugDraw` factory + GPU resource lifecycle: `packages/debug-draw/src/debug-draw.ts`
- Runtime attachment and final graph pass: `packages/render/src/debug-draw-glue.ts`.
- Hello demo (5 modes: runtime / low / depth / hdrp-tonemap / empty): `apps/hello/debug-draw/src/main.ts`
- Comparison with rhi-debug: `packages/debug-draw/README.md`.
