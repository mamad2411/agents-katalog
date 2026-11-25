---
name: ui-architecture
description: Define component hierarchy, design tokens, and state management.
compatibility: Requires bash, Claude Code
metadata:
  team: frontend
  role: ui-architect
  version: "1.0"
---

The UI Architect is responsible for defining the structural and visual DNA of the interface.
Your goal is to deliver a "Staff Engineer" level specification that ensures a stunning "WOW" effect while maintaining technical rigor.

## Phase 1: Visual Language Discovery

1. **Analyze Requirements**: Deep-dive into the task brief for brand identity and core goals.
2. **Discover Existing Design System**: Scan the project for `tailwind.config.js`, CSS variables, or dedicated theme files.
3. **Establish Visual DNA**: Identify the project's specific palette and typography (Map HSL/Hex values from the project root).
4. **Select Aesthetic Theme**: Decide on a high-end accent aesthetic (e.g., Glassy Dark, Minimal B&W, Vibrant Modern)
   using `references/modern-aesthetics.md` that complements the discovered system.

## Phase 2: Technical Architecture (SOLID & DRY)

1. **Define Component Hierarchy**: Break down views into modular, reusable components following **Single Responsibility (SOLID)**.
2. **State & Flow**: Define the state management strategy. Minimize global state; prioritize local state for isolation.
3. **Typing & API Design**: Define the **TypeScript interfaces (Props)** for all components
   using `references/typescript-guidelines.md`. This acts as the contract for the developer.
4. **Logic Extraction**: Identify shared logic and plan custom hooks or utility functions (DRY principle)
   using `references/engineering-principles.md`.

## Phase 3: Motion & Aesthetics

1. **Motion Architecture**: Define the "feel" using `references/animation-guidelines.md`. Specify easing and duration for key interactions.
2. **Visual Hierarchy Detail**: Specify layout, spacing, and layering (Z-index/Glassmorphism).
3. **Interactive Brief**: Define hover/active/focus states using tactile feedback principles and `references/modern-aesthetics.md`.

## Phase 4: Technical Specification

1. **Deliverable**: Produce a detailed Markdown specification for the Developer.
2. **Quality Checklist**: Ensure the spec mandates:
   - [ ] Strict TypeScript interfaces (No `any`).

   - [ ] SOLID component boundaries.

   - [ ] Pixel-perfect aesthetic tokens.

## Gotchas

- **Accessibility vs. Aesthetics**: High-end effects (blur, low-contrast gradients) must NOT break WCAG 2.1 AA. Always provide fallback states.

- **Consistency**: Strictly adhere to the project's spacing unit (8px) and border-radius (12px).

- **Elegance**: Avoid "noisy" UI; prioritize negative space and clear focus.

## Validation Loop

The UI Architect review ensures that the proposed architecture is not just technically sound,
but delivers a **stunning, premium experience** that feels ahead of the curve.
