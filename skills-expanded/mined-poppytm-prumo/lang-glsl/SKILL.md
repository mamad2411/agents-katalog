---
name: lang-glsl
description: GLSL shader robustness, glslangValidator compilation in CI, explicit precision qualifiers, branching optimization, and uniform buffer layout.
---

# GLSL Shader Robustness Contract

## 1. Compilation & CI Validation
- All shaders must be compiled and validated in CI using \`glslangValidator\` or \`glslc\` with warnings treated as errors.
- Specify explicit shader stages (\`.vert\`, \`.frag\`, \`.comp\`) and targeted version (\`#version 450\` or \`#version 300 es\`).

## 2. Numerical Stability & Bounds Safety
- Declare explicit precision qualifiers (\`precision highp float;\` or per-variable) to ensure consistency across mobile and desktop GPUs.
- Protect against numerical instability: guard divisions with \`max(denom, 1e-6)\`, clamp dot products to \`[0.0, 1.0]\`, and avoid negative square roots.
- All array lookups must use statically bounded or clamped indices to prevent GPU memory corruption.

## 3. Uniform & Interface Layouts
- Use explicit uniform buffer layouts (\`layout(std140, set = 0, binding = 0)\`).
- Minimize dynamic branching in fragment execution to prevent warp divergence.\n