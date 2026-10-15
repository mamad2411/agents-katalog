---
name: vulkan-bindless
description: Vulkan bindless rendering architecture with vertex pulling, uber shaders, and draw indirect. Use when implementing rendering pipelines, writing shaders, setting up descriptor sets, optimizing draw calls, or when the user asks about vertex buffers, materials, pipeline management, or GPU-driven rendering.
---

# Vulkan Bindless Rendering Architecture

You are an expert in modern Vulkan bindless rendering for game engines. When helping with rendering code, follow these principles strictly.

## Core Philosophy

**Treat the GPU as a raw compute device. Upload all data into massive flat storage buffers. One pipeline, one descriptor set, one draw call for the entire scene.**

Discard the traditional model of per-object vertex buffers, per-material descriptor sets, and per-entity draw calls. Instead:

- All vertex data → one giant Storage Buffer (SSBO)
- All per-object data → one giant Storage Buffer
- All draw commands → one Indirect Draw Buffer
- One Uber Shader handles all materials via branching
- One `vkCmdDrawIndirect` renders the entire scene

## Vertex Pulling

Do NOT create separate vertex buffer layouts for different meshes. Place ALL vertex data into one flat SSBO. The vertex shader fetches its own data using `gl_VertexIndex`:

```glsl
struct Vertex {
    vec3 position;
    float padding1;
    vec3 normal;
    float padding2;
    vec2 uv;
    vec2 padding3;
};

layout(std140, set = 0, binding = 0) readonly buffer VertexBuffer {
    Vertex vertices[];
};

void main() {
    Vertex v = vertices[gl_VertexIndex];
    // ...
}
```

This sidesteps the entire VkVertexInputState API. No vertex attribute descriptions, no binding descriptions, no per-mesh vertex buffer binds.

## Bindless Object Data

All per-object parameters (transforms, material IDs) go into a single SSBO. The shader indexes it via `gl_InstanceIndex`:

```glsl
struct ObjectData {
    mat4 transform;
    uint material_idx;
    uint padding;
};

layout(std140, set = 0, binding = 1) readonly buffer ObjectBuffer {
    ObjectData objects[];
};

void main() {
    ObjectData obj = objects[gl_InstanceIndex];
    gl_Position = obj.transform * vec4(v.position, 1.0);
}
```

Any CPU lane can write to the mapped ObjectBuffer lock-free at its computed offset.

## The Uber Shader

One shader, one pipeline, handles ALL materials via a switch on `material_idx`:

```glsl
void main() {
    uint mat_idx = objects[gl_InstanceIndex].material_idx;
    switch(mat_idx) {
        case MAT_MATTE:    final_color = compute_matte();    break;
        case MAT_METALLIC: final_color = compute_metallic(); break;
        case MAT_EMISSIVE: final_color = compute_emissive(); break;
    }
}
```

**Why branching is fine here**: Every pixel on a given object evaluates to the same branch. All threads in the warp take the same path. Zero thread divergence penalty. The cost of a single conditional instruction is irrelevant compared to eliminating pipeline swaps.

## Draw Indirect

Stop issuing one draw call per entity. Instead:

1. CPU lanes fill an indirect buffer with `VkDrawIndirectCommand` entries in parallel
2. Each entry specifies:
   - `vertexCount`: number of vertices for this mesh
   - `firstVertex`: offset into the giant VertexBuffer where this mesh starts → this becomes `gl_VertexIndex`
   - `firstInstance`: set to the entity's index → this becomes `gl_InstanceIndex`, the key into the ObjectBuffer
   - `instanceCount`: 1
3. Lane 0 submits ONE `vkCmdDrawIndirect` that renders everything

```
// In the go-narrow phase:
vk.CmdDrawIndirect(cmd, indirect_buffer, 0, active_entity_count, size_of(VkDrawIndirectCommand))
```

## Descriptor Set Layout

Radically simplified — one global set for the entire pass:

- **Binding 0** (Storage Buffer): Giant VertexBuffer — all geometry for the level
- **Binding 1** (Storage Buffer): Giant ObjectBuffer — per-object transforms and material IDs
- **Binding 2** (Optional): Bindless texture array — `sampler2D textures[]`, indexed by material

No per-object descriptor sets. No per-material descriptor sets. One bind, one draw.

## CPU-Side Buffer Management

- Allocate VertexBuffer, ObjectBuffer, and IndirectDrawBuffer at startup as large Vulkan buffers
- Keep ObjectBuffer and IndirectDrawBuffer **persistently mapped** to CPU memory
- Every frame, CPU lanes write directly into the mapped memory at non-overlapping offsets (lock-free)
- Static geometry (VertexBuffer) is uploaded once via staging buffer at level load

## Rules When Writing Rendering Code

- Never create per-mesh vertex buffer objects — put everything in the global VertexBuffer
- Never create per-object or per-material descriptor sets — use one global set
- Never swap pipelines for different materials — use the Uber Shader switch
- Never issue individual draw calls per entity — use Draw Indirect
- Use `firstInstance` in indirect commands to pass the entity index to the shader
- Use `firstVertex` to point into the correct region of the global VertexBuffer
- Keep dynamic buffers persistently mapped — never map/unmap per frame

## Anti-Patterns (Never Do This)

- Never use VkVertexInputState with attribute/binding descriptions — pull vertices from SSBO
- Never bind/unbind descriptor sets per object — bind once globally
- Never sort draw calls by material on CPU — let the Uber Shader handle it
- Never create multiple graphics pipelines for different materials
- Never call vkCmdDraw in a loop per entity — use vkCmdDrawIndirect once
