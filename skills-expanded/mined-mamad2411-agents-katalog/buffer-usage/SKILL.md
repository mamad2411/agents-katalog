---
name: buffer-usage
description: This skill should be used when declaring, creating, or reviewing GPU buffer resources in TortureRed — choosing between StructuredBuffer/RWStructuredBuffer, ByteAddressBuffer/RWByteAddressBuffer, typed Buffer<T>, and ConstantBuffer<T> in HLSL, or between CreateBuffer/CreateStructuredBuffer and heap types (UPLOAD/DEFAULT) on the C++ side (Sources/Graphics/GraphicsTypes.h/.cpp, GPUBuffer). Triggers on tasks such as adding a new GPU buffer resource, picking a buffer type for a new shader, reviewing DeferredLighting/DebugTextRenderer/PathTracing-style buffer usage, or debugging why a buffer doesn't reflect nicely in RenderDoc.
---

# Buffer Usage

## Overview

TortureRed uses exactly four HLSL buffer-family resource types — `StructuredBuffer<T>`/`RWStructuredBuffer<T>`, `ByteAddressBuffer`/`RWByteAddressBuffer`, typed `Buffer<T>`, and `ConstantBuffer<T>` — backed by two C++ creation helpers (`CreateBuffer`, `CreateStructuredBuffer`) and two constant-buffer binding mechanisms (root 32-bit constants, root CBV). Picking the wrong one causes silent bugs (RenderDoc showing raw hex instead of named fields, byte-offset misalignment, or wasted format-conversion opportunities) rather than compile errors.

## When this applies

- Adding a new GPU buffer resource (a C++ `GPUBuffer` + its matching HLSL declaration).
- Choosing between `StructuredBuffer`, `ByteAddressBuffer`, or typed `Buffer<T>` for a new resource.
- Choosing the CPU/GPU read-write access pattern (heap type + SRV/UAV combination).
- Uploading one-time CPU-authored initial data into a `DEFAULT`-heap buffer (staging via `ResourceUploadBatch`).
- Adding a new small per-pass constant struct, or deciding whether it needs its own root CBV.
- Debugging why a buffer shows raw bytes instead of named fields in RenderDoc/PIX.

## How to use

1. Read `references/buffer_type_conventions.md` before creating a new buffer resource — it has the full type-selection decision table and grounded TortureRed examples (`DeferredLighting`, `DebugTextRenderer`, `PathTracing`'s RTXDI integration, `Model`'s buffer/texture upload paths).
2. Decide the **element shape** first: one custom struct → `StructuredBuffer<T>` (default); one scalar/vector HLSL type mapped to a real DXGI hardware format → typed `Buffer<T>`; multiple different types/counters packed at manual byte offsets in one resource → `ByteAddressBuffer` (narrowest, last-resort case).
3. Pick the heap type (`D3D12_HEAP_TYPE_UPLOAD` vs `D3D12_HEAP_TYPE_DEFAULT` vs `D3D12_HEAP_TYPE_READBACK`) using the CPU/GPU read-write matrix in the reference doc — don't default to UPLOAD out of convenience for GPU-only data.
4. If a `DEFAULT`-heap buffer needs one-time CPU-authored initial content, bridge it through `ResourceUploadBatch::Upload()` (see `Model::UploadBuffers()`) rather than leaving the buffer on `UPLOAD` heap permanently. Route new *texture* uploads through the same `CreateBuffer()`-based staging convention where possible — `Model::UploadTextures` currently does not, and is flagged as a known inconsistency in the reference doc.
5. For a new small per-pass parameter struct, check whether it can share the existing root-constants slot (`b1`) instead of allocating a new CBV — but read the "shared slot sizing" gotcha first.
6. Always bind new buffers bindlessly (`ResourceDescriptorHeap[idx]` + an index passed via constants) — the project is moving away from fixed root-slot bindings; don't introduce new non-bindless root-SRV-by-address bindings.

## Resources

### references/

- `references/buffer_type_conventions.md` — full buffer-type selection matrix, the readability/writability (CPU/GPU read-write) matrix, GPU buffer staging via `ResourceUploadBatch`, and grounded examples from `DeferredLighting.cpp`, `DebugTextRenderer.cpp/.hlsli`, `PathTracing.cpp`'s RTXDI neighbor-offsets buffer, and `Model.cpp`'s buffer/texture upload paths.
