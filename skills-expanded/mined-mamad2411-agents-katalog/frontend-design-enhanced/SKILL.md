---
name: frontend-design-enhanced
description: Design and implement distinctive, production-ready frontend interfaces for the web. Use when building, redesigning, or polishing components, pages, dashboards, landing pages, design systems, or UI code (HTML/CSS/JS/TS/React/Vue/Tailwind) that must be beautiful, usable, responsive, accessible, and feel deliberately designed rather than generic.
compatibility: Best in coding agents that can inspect and edit existing frontend files and follow local framework conventions. Avoid introducing new dependencies unless they are clearly justified.
license: MIT
metadata:
  author: Skill Atlas
  version: "0.1.0"
  homepage: https://skillatlas.sh/
---

# Frontend Design

Create real, working frontend experiences with a clear point of view. Distinctive is the goal, but the interface must still help the user complete tasks quickly and confidently. When the codebase already has a design language, extend it intelligently instead of forcing a disconnected redesign.

## Use this skill when

- The user wants a page, component, view, landing page, dashboard, form flow, design system, or frontend refactor.
- The user wants HTML/CSS/JS, TypeScript, React, Vue, Svelte, Next.js, Tailwind, or similar UI code.
- The user wants an existing UI reviewed, restyled, or made more polished, usable, responsive, or accessible.
- The request is primarily about visible interface design and implementation, not backend logic.

## Do not use this skill when

- The task is purely backend, API, database, infrastructure, or CLI with no meaningful UI surface.
- The user only wants branding strategy or copywriting without interface work.

## Core stance

- Make the design memorable, not merely fashionable.
- Put task clarity first: hierarchy, affordance, and readability beat decoration.
- Honor real-world constraints: existing brand, framework, performance budget, accessibility requirements, and team conventions.
- One signature element is stronger than five disconnected tricks.
- If the brief is vague, make decisive assumptions and state them briefly.

## Workflow

### 1) Read the problem and the codebase

Before changing anything, extract:

- **Purpose**: what the screen must help a person do.
- **Primary actions**: the key clicks, decisions, inputs, and success path.
- **Audience**: skill level, device mix, and context of use.
- **Constraints**: framework, styling system, performance budget, accessibility target, brand rules, localization, dark/light mode, and technical limits.
- **Content shape**: real data types, long labels, empty states, loading states, failure states, permissions, destructive actions, and edge cases.
- **Existing system**: current tokens, spacing, typography, components, utilities, icon style, and motion language.
- **Reference cues**: screenshots, wireframes, existing brand materials, or nearby product surfaces.

If you are refining an existing product, inspect nearby components and styles first. Reuse the product's own primitives unless the user asked for a redesign.

### 2) Choose the mode

Pick one mode explicitly:

- **New system**: greenfield UI or major redesign.
- **Extension**: a new surface inside an existing design system.
- **Polish**: improve clarity, rhythm, affordances, and visual quality without changing the product's core identity.

### 3) Write a visual brief before coding

Commit to one strong direction rather than blending everything together. Examples: ultra-minimal, editorial, brutalist, playful, industrial, luxe, retro-futuristic, organic, art deco, lo-fi zine, soft/pastel.

Before you code, write 3-5 bullets covering:

- aesthetic direction
- density (airy vs compact)
- palette strategy
- type strategy
- signature element
- motion character

Example:

> Dark industrial dashboard; compact grid; condensed serif display + restrained sans; graphite + acid-lime accent; data panels with scanline texture; 140ms snap transitions.

Also define a **restraint rule**: what you will intentionally avoid so the design stays coherent.

### 4) Build the information hierarchy

Make the interface readable at a glance:

- establish a dominant headline or anchor
- make the primary action unmistakable
- group related content clearly
- design for scanning before reading
- remove decorative clutter that competes with task completion

When building workflows, reduce friction first. When building marketing pages, create narrative pace. When building dashboards, optimize for fast interpretation and dense clarity.

### 5) Build a visual system, not isolated styles

Use tokens or theme variables for all repeat values.

**Typography**

- Choose typography that carries the concept. Avoid default-feeling display choices unless the existing brand requires them.
- Pair expressive display typography with a calmer body face, or create distinction through weight, width, case, and spacing if custom fonts are constrained.
- Use intentional hierarchy:
  - headline `line-height`: ~1.0-1.2
  - subhead/section titles: ~1.2-1.35
  - body: ~1.5-1.7
- Use slight tracking for uppercase labels. Use `clamp()` for fluid scale.

**Color**

- Use a tight palette: 1-2 neutrals, 1 dominant accent, semantic colors only where needed.
- Concentrate accent color where action or emphasis matters.
- Ensure accessible contrast, including on hover, focus, and disabled states.
- Prefer decisive color stories over timid multi-accent palettes.

**Layout and space**

- Work from a consistent spacing scale such as `4, 8, 12, 16, 24, 32, 48, 64`.
- Use a real grid, or deliberate asymmetry that still reads clearly.
- Create energy with contrast in scale: tiny labels against large headlines, compressed dense tables against generous margins, and other intentional shifts.
- Avoid default centered-everything compositions unless the concept truly calls for it.

**Depth and atmosphere**

- Never stop at flat white plus default black.
- Add depth that matches the concept: subtle gradients, grain, borders, patterning, layered surfaces, ambient shadows, blur, print textures, or controlled glow.
- Decorative effects must reinforce the concept and never reduce legibility.

**Motion**

- Micro-interactions: ~100-150ms
- Panels, modals, and state changes: ~200-300ms
- Orchestrated entrances: ~400-600ms
- Use `ease-out` for entrances and `ease-in-out` for state changes.
- Prefer one well-choreographed reveal over many random animations.
- Always respect `prefers-reduced-motion`.

### 6) Implement like a product designer who also ships

- Use semantic HTML and meaningful component structure.
- Keep component APIs small and understandable.
- Follow the framework's conventions instead of fighting them.
- Prefer co-located styles and shared tokens over scattered one-off overrides.
- Avoid magic numbers. If a value repeats, promote it to a token.
- Do not introduce major UI libraries or animation dependencies for minor stylistic gains unless the user asked for them or the payoff is substantial.

Framework-specific guidance:

- **Tailwind**: use CSS variables, shared utility patterns, and extracted components or classes for recurring patterns; avoid walls of arbitrary values.
- **React/Vue/Svelte**: keep components composable, state flows clear, and props intentional.
- **Plain HTML/CSS/JS**: make the code clean enough to drop into a real project, not a demo-only snippet.

### 7) Handle real product states

Every important surface should account for:

- hover, focus, active, and disabled states
- loading with layout stability
- empty state with a useful next step
- error state with a recovery path
- success or confirmation states when relevant
- validation feedback for forms
- text overflow, long labels, and small screens

Use realistic copy and data shapes whenever possible. Avoid lorem ipsum unless the user asks for placeholders.

### 8) Make it responsive and accessible by default

- Start mobile-first.
- No horizontal scroll at 320px.
- Use fluid type and responsive containers.
- Provide visible, high-contrast focus styles.
- Ensure full keyboard navigation.
- Use labels for form fields and accessible names for icon-only controls.
- Use ARIA only when native semantics are insufficient.
- Preserve readability at zoom and with long text.
- Support reduced motion and color/contrast needs.

### 9) QA the result before you stop

Check:

- Does the design have a clear identity?
- Does the primary action stand out immediately?
- Would this still feel good with real, messy content?
- Is it consistent with the existing product if one already exists?
- Is it usable without a mouse?
- Does it still work on a narrow mobile viewport?
- Could this belong to any brand? If yes, revise.
- Does anything feel like a copied trend rather than an intentional choice?

Revise until the answer is yes.

## Surface-specific heuristics

### Landing pages and marketing

- Build a clear narrative arc, not a template stack.
- Make the hero distinctive, but let proof, differentiation, and CTA rhythm carry the page.
- Avoid the default `hero -> three cards -> testimonials -> CTA` skeleton unless the user explicitly asks for it.

### Dashboards and data-heavy apps

- Optimize for scan speed, density, comparison, and filter clarity.
- Use hierarchy and spacing to separate control surfaces from data surfaces.
- Make tables, charts, filters, and cards feel related, not like unrelated widgets.

### Forms and workflow UIs

- Reduce cognitive load.
- Show progress, consequences, and validation clearly.
- Make destructive actions unmistakable and reversible where possible.

### Design-system work and component libraries

- Solve for consistency, extensibility, and state coverage.
- Prefer a few strong primitives over many almost-duplicate components.

## Avoid generic output

Do not default to:

- Inter, Roboto, Arial, Space Grotesk, Poppins, or generic system fonts as the **display** voice unless the product already uses them or constraints require them
- purple or blue gradients on white
- shallow startup palettes
- default browser form controls
- generic glassmorphism or neumorphism as the whole concept
- cookie-cutter section stacks and evenly weighted card grids
- decorative motion with no functional purpose

Always include at least one memorable signature element that fits the context. Good options include a striking typographic treatment, an unusual but usable grid, a distinctive border language, a controlled texture system, a strong color-positioning strategy, or a single standout interaction pattern.

## Response format

When you answer the user, structure the work like this unless they asked for something different:

1. brief assumptions or context
2. visual brief (3-5 bullets)
3. implementation notes or what changed
4. complete code or concrete edits
5. short QA and polish notes

If the user asks for direct edits to an existing file, keep the commentary brief and ship the implementation.

## Standard

Safe is forgettable. Trend-chasing is forgettable. Ship frontend work that feels considered, specific, usable, and ready to live in a real product.
