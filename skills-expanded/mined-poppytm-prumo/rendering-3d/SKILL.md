---
name: rendering-3d
description: Modern 3D real-time rendering pipelines, Forward+ and Deferred G-Buffer architectures, Cook-Torrance PBR metallic-roughness, Cascaded Shadow Maps (CSM), frustum/Hi-Z culling, and GPU resource lifecycles.
---

# 3D Real-Time Rendering & Graphics Architecture

## 1. Title and Description
**3D Real-Time Rendering & Graphics Architecture (`rendering-3d`)**
Governs the design, implementation, and optimization of real-time 3D graphics rendering pipelines across WebGPU, Vulkan, DirectX 12, and Metal. Covers Forward+ and Deferred shading architectures, Physically Based Rendering (PBR), Cascaded Shadow Maps (CSM), spatial visibility culling, GPU resource lifecycles, and frame pacing.

## 2. Purpose
Achieve high visual fidelity and robust frame pacing (16.6ms / 8.3ms budgets) while eliminating pipeline stalls, memory bandwidth saturation, shadow acne/peter-panning, and GPU synchronization deadlocks.

## 3. Prerequisites
- Target graphics API: WebGPU, Vulkan, Metal, or Direct3D 12.
- Linear algebra foundation (4x4 matrix transforms, quaternions, coordinate spaces).
- Shader compiler toolchain (Naga, DXC, or glslang).

## 4. Inputs
- 3D scene representation (meshes, materials, cameras, lights, transform hierarchies).
- Target hardware profile (integrated GPU vs discrete desktop GPU, VRAM budgets).
- Target render resolution and frame rate goals (e.g. 1080p @ 60 FPS / 1440p @ 120 FPS).

## 5. Outputs
- Implemented 3D rendering pipeline modules (render passes, pipeline state objects, buffer managers).
- Spatial visibility culling algorithms (Frustum, BVH, Hi-Z).
- PBR material shaders and shadow generation routines.
- Render performance report conforming to `templates/rendering-3d-report.md`.

## 6. Execution Steps

### Step 1: Select Rendering Architecture (Forward+ vs Deferred)
1. **Deferred Shading**:
   - Best when scene contains hundreds of dynamic lights affecting opaque geometry.
   - **Pass 1 (G-Buffer)**: Output to Multiple Render Targets (MRT):
     - RT0: Albedo RGB (sRGB, 8-bit per channel) + Material AO (8-bit).
     - RT1: World Normal (Octahedral or 16-bit float per channel).
     - RT2: Metallic (8-bit) + Roughness (8-bit) + Emissive (16-bit).
     - Depth Buffer: 24-bit or 32-bit floating point depth (`D32F`).
   - **Pass 2 (Lighting)**: Compute lighting per-pixel from G-Buffer.
   - **Limitation**: Incompatible with hardware MSAA; transparent objects must be rendered in a separate forward pass.
2. **Forward+ (Clustered Forward)**:
   - Divides the screen into an $X \times Y \times Z$ grid of frustum clusters via a compute shader.
   - Assigns dynamic lights to clusters. Forward shading pass iterates only over lights relevant to its pixel's cluster.
   - Supports hardware MSAA and handles transparent and opaque materials uniformly.

### Step 2: Implement Cook-Torrance PBR Shading
Implement the standard microfacet model with the metallic-roughness workflow:
1. **Diffuse Reflection**: Lambertian diffuse term:
   $$f_{\text{diffuse}} = \frac{c_{\text{albedo}}}{\pi} \cdot (1 - \text{metallic})$$
2. **Specular Reflection**: Cook-Torrance BRDF:
   $$f_{\text{specular}} = \frac{D(h) \cdot F(v, h) \cdot G(l, v, h)}{4 (\mathbf{n} \cdot \mathbf{l}) (\mathbf{n} \cdot \mathbf{v})}$$
   - **$D$ (Normal Distribution)**: Trowbridge-Reitz GGX.
   - **$F$ (Fresnel Term)**: Schlick's approximation with $F_0$ interpolated between $0.04$ (dielectrics) and albedo color (metals).
   - **$G$ (Geometric Shadowing)**: Smith's method with Schlick-GGX formulation.

### Step 3: Cascaded Shadow Maps (CSM)
1. Split the camera view frustum into 3 or 4 depth partitions using practical split schemes (combining logarithmic and uniform distributions).
2. For each cascade:
   - Calculate tight bounding box around the frustum partition.
   - Snap light projection matrix to texel increments to prevent "shadow shimmering" when camera translates.
3. Apply **Percentage-Closer Filtering (PCF)** with a $3 \times 3$ or $5 \times 5$ kernel to soften shadow borders.
4. Calculate normal bias and slope-scaled depth bias to eliminate shadow acne and peter-panning artifacts.

### Step 4: Spatial Visibility Acceleration & Culling
1. **Frustum Culling**: Extract 6 clipping planes from the combined View-Projection matrix:
   $$\text{Plane}: A x + B y + C z + D = 0$$
   Test mesh Axis-Aligned Bounding Boxes (AABB) against all 6 planes. Reject objects completely outside any plane before dispatching draw calls.
2. **Hierarchical Z-Buffer (Hi-Z) Occlusion Culling**:
   - Downsample previous frame depth buffer into a mipmapped pyramid.
   - In compute shader, project object bounding boxes and test against the corresponding Hi-Z depth mip. Discard occluded geometry.

### Step 5: GPU Resource Lifecycles & Synchronization
1. **Double / Triple Buffering**:
   - Maintain $N$ frames in flight (typically 2 or 3) with per-frame uniform buffers and command allocators.
   - Synchronize with CPU fences (`vkWaitForFences`, WebGPU queue submission) to prevent overwriting GPU resources while a previous frame is in flight.
2. **Image Layout Transitions & Memory Barriers**:
   - Explicitly transition render targets (e.g. from `COLOR_ATTACHMENT` to `SHADER_READ_ONLY`) before sampling in subsequent passes.

## 7. Verification
```bash
# 1. Verify graphics tests
cargo test -p renderer_core

# 2. Shader compilation check for 3D passes
naga src/shaders/*.wgsl
```

## 8. Fallbacks & Failure Recovery
| Failure Class | Root Cause | Deterministic Remediation |
|---|---|---|
| Shadow Shimmering / Crawling | Shadow camera projection moves continuously with sub-pixel offsets | Snap shadow camera origin to texel grid: `world_pos = floor(world_pos / texel_size) * texel_size`. |
| Shadow Acne (Surface Artifacts) | Self-shadowing from depth precision limitations | Add slope-scaled depth bias and normal offset bias in shadow shader. |
| GPU Pipeline Stall (0 FPS Drops) | CPU blocking on `vkQueueWaitIdle` or synchronous buffer readback | Use non-blocking double-buffered staging buffers and query fences asynchronously. |
| Inverted Normal Lighting | Tangent space handedness flipped in model importer | Ensure bitangent calculation accounts for UV winding: `bitangent = cross(normal, tangent) * tangent.w`. |

## 9. Constraints
- **Zero synchronous CPU-GPU readbacks in render loops**: Never call blocking readback functions during rendering.
- **Strict G-Buffer bit-budget**: Keep G-Buffer thickness under 128 bits per pixel to preserve mobile/integrated GPU bandwidth.
- **Always frustum cull**: Never issue draw calls for the entire scene without frustum testing.

## 10. Examples

### Anti-Pattern: Unculled Immediate Draw with Hardcoded Shading
```cpp
// BAD: Draws every object without culling, ad-hoc Phong lighting, blocking CPU wait
void BadRenderScene(Camera camera, std::vector<Mesh> meshes) {
    for (auto& mesh : meshes) {
        // ERROR: No frustum test! Submits 500,000 off-screen triangles to GPU!
        mesh.Draw(); 
    }
    glFinish(); // ERROR: Blocks CPU until GPU idle! Destroys parallelism!
}
```

### Idiomatic Pattern: Frustum Culling & Structured PBR Draw List
```cpp
// GOOD: AABB Frustum test, batched draw list generation, decoupled synchronization
struct Frustum {
    Plane planes[6];

    bool IntersectsAABB(const AABB& box) const {
        for (int i = 0; i < 6; ++i) {
            // Find positive vertex along plane normal
            Vec3 p = box.min;
            if (planes[i].normal.x >= 0) p.x = box.max.x;
            if (planes[i].normal.y >= 0) p.y = box.max.y;
            if (planes[i].normal.z >= 0) p.z = box.max.z;

            if (planes[i].DistanceTo(p) < 0) {
                return false; // Box is outside frustum
            }
        }
        return true;
    }
};

void BuildRenderQueue(const Frustum& frustum, const std::vector<RenderObject>& scene, RenderQueue& outQueue) {
    outQueue.opaqueDraws.clear();
    outQueue.opaqueDraws.reserve(scene.size());

    for (const auto& obj : scene) {
        if (!frustum.IntersectsAABB(obj.worldBounds)) {
            continue; // Culled! Zero GPU overhead
        }

        outQueue.opaqueDraws.push_back({
            .meshBuffer = obj.meshBuffer,
            .materialUniforms = obj.materialHandle,
            .modelMatrix = obj.transform
        });
    }
}
```
