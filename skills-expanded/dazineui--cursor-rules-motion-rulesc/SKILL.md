---
description: Motion system rules for AI assistants in this repository
globs: "**/*"
alwaysApply: true
---

# Motion Rules

This rule mirrors the project-level instruction layer for Cursor users.

## 1) Hard Rules (Non-Negotiable)

1. Do not write custom CSS keyframes for hero or feature-level visual motion when a project primitive can satisfy the request.
2. Do not write custom GLSL unless the user explicitly asks for custom shader work.
3. Do not use `MeshStandardMaterial` with default settings for hero-grade 3D visuals; tune materials deliberately, and prefer `MeshPhysicalMaterial` where appropriate.
4. Do not hardcode proprietary display fonts (for example: Söhne, GT America, Founders Grotesk, NB International, SF Pro where platform use is not explicit).
5. Do not use office/system display fonts (`Arial`, `Helvetica`, `Times New Roman`, `Georgia`, `Calibri`) for premium-facing hero/UI typography.
6. Always include post-processing for production-quality R3F hero scenes.
7. Always respect reduced-motion accessibility (`prefers-reduced-motion`) for any animation.
8. Do not replace primitive usage with ad-hoc inline animation code when an existing primitive covers the need.
9. Keep implementations token-aware: prefer design tokens over ad-hoc colors/timing values.

## 2) Decision Flow (When User Requests Visual Design or Motion)

Follow this sequence in order:

1. Check for `DESIGN.md` in project root and parse/derive usable color, typography, spacing, radius, and motion tokens.
2. Scan `lib/motion/*/MANIFEST.md` files and read descriptors, use-cases, presets, and constraints.
3. If a screenshot/mock reference is provided, describe visible traits first (palette, motion character, layout rhythm, visual hierarchy), then map those traits to manifest descriptors.
4. Choose the closest matching primitive (or minimal composition of primitives).
5. Configure via typed props and presets first. Pass DESIGN-driven tokens whenever possible.
6. If a primitive exists for the requested effect, import and use it. Do not reimplement inline.
7. If no primitive matches, generate new code only after proving no suitable primitive exists, and still follow this repo's aesthetic defaults and safety rules.

## 3) Aesthetic Defaults (Fallbacks When Inputs Are Ambiguous)

- Background base: `#0a0a0a` (not pure black).
- Hero motion timing: `600ms` to `900ms`.
- Micro-interaction timing: `200ms` to `300ms`.
- Easing default: `cubic-bezier(0.32, 0.72, 0, 1)` (never browser default ease for premium motion).
- Spacing system: 4px base scale.
- Radius scale: 8px, 12px, 16px, 24px.
- Display font fallback: Geist Sans.
- Monospace fallback: Geist Mono.
- Secondary fallback: Inter.

When uncertain, choose subtle, premium motion over loud, novelty animation.

## 4) Vague Prompt Routing (Ambiguous User Language)

- "Make it pop" / "Stripe-style" / "Feel premium" → `FlowGradient preset="stripe"` — wave ribbons
- "Neon" / "Glowing tubes" / "Linear-style" → `SpotlightGradient` — emissive tubes + Bloom
- "Flow field" / "Generative art" / "Organic particle streams" → `NoiseGradient`
- "Dot matrix" / "Aurora" / "Wave particles" / "AI aesthetic" → `AuroraGradient`
- "Fine lines" / "Thread texture" / "Fiber" / "Woven" → `MeshGradient`
- "Cool background" (no context) → `FlowGradient preset="stripe"` (safe default)
- "Organic sphere" / "Morphing ball" / "AI orb" → `MorphOrb` (planned)
- "Crystal" / "Glass" / "Gem" / "Refraction" → `CrystalShard` (planned)

Prefer explicit primitive mapping. When writing new primitives from scratch: real
geometry, tuned materials, custom GLSL. Never blur as the core visual ingredient.

## 5) Anti-Patterns and Explicit Prohibitions

Never produce these in this project unless explicitly requested:

1. Blanket `motion.div` fade-ins across the page as a default style.
2. `hover:scale-105` used as a substitute for designed motion systems.
3. `transition: all` for UI animation.
4. Generic spinner/pulse effects as filler "movement."
5. Plain untuned spheres/cubes as hero 3D visuals when styled primitives should be used.
6. Default Three.js tutorial lighting that yields flat gray scenes.
7. Primary display typography set to generic system fonts.
