---
name: lang-hlsl
description: Modern HLSL (Shader Model 6.x), DXC compiler validation, explicit register and space bindings, and 16-byte constant buffer packing.
---

# HLSL Modern Shading Contract

## 1. Compiler Toolchain & Target Profile
- Target modern DirectX Shader Compiler (\`dxc\`) with Shader Model 6.0+ (\`vs_6_0\`, \`ps_6_0\`, \`cs_6_0\`).
- Enforce strict compilation flags: \`-WX\` (treat warnings as errors) and generate debug PDB symbols.

## 2. Resource Bindings & Memory Alignment
- Declare explicit register and space bindings for all resources: \`register(b0, space0)\`, \`register(t0, space0)\`.
- Enforce 16-byte constant buffer packing rules: pad struct members explicitly to maintain float4 boundary alignment.

## 3. Wave Intrinsics & Concurrency
- When utilizing wave intrinsics (\`WaveActiveSum\`, \`WaveReadLaneFirst\`), ensure lane-count agnosticism (do not assume 32 or 64 thread waves).\n