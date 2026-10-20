---

name: leeway-creative-rendering-engineering

description: High-end digital design/front-end graphics capability hub combining motion physics, PBR/BRDF lighting, Oklab colorimetry, Bézier/vector continuity, GPU frame budgets, VRAM, accessibility, visual design and frontend implementation.

license: MIT

metadata:

  authority: Creator/Human Authority > LeeWay Standards

  mode: creative-rendering-engineering

  sun: skills/leeway-mathematical-sun/SKILL.md

---

# LeeWay Creative Rendering Engineering

## Motion

Use physically meaningful spring/damping models where appropriate: m x'' + c x' + k x = 0, omega_0=sqrt(k/m), zeta=c/(2 sqrt(mk)). Target damping is design-context dependent; do not universally claim zeta=0.85 or 1.0 is optimal without interaction evidence.

## PBR

Use physically based BRDF components such as Cook-Torrance/GGX/Fresnel/Smith where the renderer/material model calls for them. Preserve normalized normals and energy constraints appropriate to the material model; do not reduce all physically valid materials to a naive kd+ks=1 equality.

## Color

Perform perceptual comparisons in an appropriate space such as Oklab/OKLCH while preserving the actual accessibility contrast standard and gamut constraints required by the product. Perceptual delta and WCAG contrast are separate measurements.

## Vector geometry

Cubic Bézier B(t)=(1-t)^3 P0+3(1-t)^2 t P1+3(1-t)t^2 P2+t^3 P3. Measure tangent/curvature continuity at joins. C2 and G2 are related but not identical; preserve which continuity class is actually required.

## Hardware

Measure CPU preparation, GPU render/compute, synchronization, upload, compositor and frame timing against the target refresh interval. Track VRAM/resource budgets from actual formats, dimensions, mip levels, samples, buffers and residency evidence.

## Composition

Combine design-suite, frontend/UI, accessibility, WebGPU/graphics, performance, testing, observability, device/hardware, Veritas and Mathematical Sun metrics. A visual skill never suppresses performance/accessibility/security evidence.