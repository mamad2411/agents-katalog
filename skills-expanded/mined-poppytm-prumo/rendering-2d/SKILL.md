# High-Performance 2D Vector & Sprite Rendering Pipeline

## 1. Purpose
Design, implement, and optimize real-time 2D graphics rendering engines (immediate-mode and retained-mode). This skill enforces dynamic quad and polygon batching, multi-texture indexing, hardware scissoring, premultiplied alpha blending, Signed Distance Field (SDF/MSDF) vector glyph rasterization, MaxRects texture atlas generation with bleed-protection gutters, and zero-allocation per-frame draw submission.

---

## 2. Use When
- Developing 2D game engines, UI rasterizers, node editors, canvas-based chart renderers, or desktop terminal UI viewers.
- Implementing dynamic sprite batchers, tilemap chunk renderers, or 2D particle systems in WebGPU, Vulkan, Metal, OpenGL, or DirectX.
- Generating and sampling texture atlases with UV coordinate packing and bleeding prevention.
- Rendering scalable resolution-independent typography using Multi-channel Signed Distance Fields (MSDF).
- Operating in mode(s): `implementation`, `design`, `testing`, `audit`.

---

## 3. Do Not Use When
- Working purely on 3D mesh rendering, PBR shaders, or Cascaded Shadow Maps (use `rendering-3d`).
- Building standard DOM-based web applications that rely on native browser HTML/CSS rendering.
- Authoring CPU-only offline image processing without hardware graphics acceleration.

---

## 4. Required Context
Before authoring or modifying 2D rendering code, verify:
- **Graphics API**: WebGPU, Vulkan, Metal, Modern OpenGL (4.3+), or Direct3D 11/12.
- **Coordinate Space Convention**: Top-Left origin $(0,0)$ (standard UI/Desktop) vs Bottom-Left origin (standard OpenGL).
- **Target Frame Budget**: 60 FPS (16.6ms) or 120 FPS (8.33ms), with maximum 2D render thread submission budget $\le 2.0\text{ ms}$.
- **Batching Thresholds**: Max vertices per batch (e.g., 65,536 vertices = 16,384 quads), max bound texture slots per draw call (typically 8, 16, or 32 depending on GPU hardware descriptor limits).

---

## 5. Procedure

```
[2D Scene / Primitive Queue]
         |
         v
[1. Viewport & Frustum Culling] -----> AABB test against 2D Camera Ortho Rect
         |
         v
[2. Z-Index & Material Sorting] -----> Sort by Layer -> Material -> Texture -> Z
         |
         v
[3. Dynamic Batching Accumulator] ---> Pack vertices into Mapped Ring Buffer
         |  (Trigger Flush on: Buffer Full, Texture Slot Exhaustion, Scissor Change)
         v
[4. GPU Draw Call Submission] -------> Bind Vertex Buffer, Index Buffer, Multi-Texture Set
         |
         v
[5. Blending & Scissor Pass] --------> Premultiplied Alpha (ONE, ONE_MINUS_SRC_ALPHA)
```

### Step 1: Orthographic Projection & Frustum Culling
1. Construct 2D Orthographic Projection Matrix:
   $$\mathbf{M}_{\text{ortho}} = \begin{bmatrix} \frac{2}{R - L} & 0 & 0 & -\frac{R + L}{R - L} \\ 0 & \frac{2}{T - B} & 0 & -\frac{T + B}{T - B} \\ 0 & 0 & -\frac{1}{Z_f - Z_n} & -\frac{Z_n}{Z_f - Z_n} \\ 0 & 0 & 0 & 1 \end{bmatrix}$$
2. Cull any sprite whose world AABB $[\mathbf{min}, \mathbf{max}]$ does not intersect the camera view rectangle prior to vertex generation.

### Step 2: Dynamic Quad Batching Architecture
1. Maintain pre-allocated CPU-mapped ring buffers for quad vertices (4 vertices, 6 indices per quad: $0, 1, 2, 2, 3, 0$):
   ```cpp
   struct Vertex2D {
       float position[2];
       float uv[2];
       uint32_t color_rgba;
       float texture_index;
   };
   ```
2. Accumulate incoming quad draw commands into the mapped buffer.
3. Automatically flush the batch to the GPU when:
   - Vertex buffer capacity reaches limit ($V_{\text{max}} = 65,536$).
   - A new texture is encountered and all hardware texture slots ($N = 16$) are full.
   - The active clipping/scissor rectangle changes.
   - Blend mode switches (e.g., Alpha to Additive).

### Step 3: Texture Atlas Packing & Bleed Prevention
1. Use MaxRects bin packing algorithm to pack heterogeneous sprite textures into a power-of-two texture atlas ($2048 \times 2048$ or $4096 \times 4096$).
2. Always inject a **2-pixel duplicate gutter** around each sprite rect in the atlas. This prevents neighboring sprite pixels from bleeding into the current sprite during bilinear filtering at fractional coordinates.

### Step 4: Text Rendering with MSDF
For scalable, crisp text at arbitrary zoom levels:
- Pre-generate Multi-channel Signed Distance Field glyph atlases (RGB channels store horizontal, vertical, and diagonal distance fields).
- Evaluate glyph alpha in fragment shader using screen-space derivative antialiasing:
  ```wgsl
  let msd = textureSample(glyph_atlas, atlas_sampler, in.uv).rgb;
  let sd = max(min(msd.r, msd.g), min(max(msd.r, msd.g), msd.b));
  let screen_pixel_distance = screen_px_range * (sd - 0.5);
  let alpha = clamp(screen_pixel_distance + 0.5, 0.0, 1.0);
  ```

### Step 5: Premultiplied Alpha & Hardware Scissoring
- Enable Premultiplied Alpha blending on all transparent passes:
  - Source Factor: `ONE`
  - Destination Factor: `ONE_MINUS_SRC_ALPHA`
- Push hierarchical clipping rectangles using hardware scissoring (`setScissorRect`) rather than fragment shader discard, enabling Early-Z and tile-based raster optimizations.

---

## 6. Decision Rules & Invariants
- **RULE 1 (Zero Allocations in Render Loop)**: Never allocate heap memory (`malloc`, `vector::push_back` beyond capacity) during per-frame batch recording.
- **RULE 2 (Premultiplied Alpha Mandatory)**: All sprite textures with transparency must be stored and loaded in premultiplied alpha format to eliminate black border fringes.
- **RULE 3 (Texture Bleed Protection)**: Every atlas sprite must have at least 1 (preferably 2) gutter pixels copied from its border.
- **RULE 4 (Batching Draw Call Ceiling)**: A complex 2D scene of up to 100,000 sprites must be rendered in fewer than 25 batched GPU draw calls.

---

## 7. Evidence Required
- **Batching Efficiency Metric**: Total draw calls and vertex count recorded per frame across benchmark scene.
- **Visual Evidence**: Rendered test output verifying zero texture bleeding artifacts on fractional zoom.
- **Allocation Audit**: Proof of zero heap allocations inside the render tick loop.

---

## 8. Output Contract
- High-performance 2D renderer / batcher source code (`.cpp`, `.rs`, `.wgsl`).
- Texture atlas packer and sprite lookup manifest.
- 2D Rendering Pipeline & Profiling Report (`templates/rendering-2d-report.md`).

---

## 9. Stop Conditions
- 2D rendering passes execute with $< 20$ draw calls on test scenes.
- Zero texture bleeding on scaled sprite tests.
- Token budget exhausted.
- Blocked on external dependency.

---

## 10. Escalation Rules
- Escalate to graphics lead if platform GPU descriptor indexing limits restrict multi-texture batching below 8 textures per draw call.
- Escalate if hardware scissoring is unsupported on targeted legacy display server.
