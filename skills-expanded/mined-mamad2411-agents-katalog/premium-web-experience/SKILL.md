---
name: premium-web-experience
description: Orchestrator for building a complete premium, award-level website or landing page — picks the direction, then routes to the right design, motion, 3D and review skills in this kit and enforces performance/accessibility budgets. Use at the START of any new website, landing page, portfolio or redesign, or when the user asks for something "premium", "Awwwards-level", "high-end", or "not generic".
---

# Premium Web Experience (orchestrator)

Written for this agent-kit. This skill does not replace the specialist skills — it decides which ones to load and in what order, so they don't fight each other.

## Step 0 — Blueprint first

If `docs/PROJECT_PLAN.md` doesn't exist yet, run `project-blueprint` (sitemap, sections, interlinks, build order) and get approval. The design/motion choices below go into its "Design decisions" section, and the build then follows its step-by-step loop — never the whole site at once.

## Step 1 — Brief (ask if missing, max 3 questions)

Audience, primary goal/CTA, brand assets (logo, colors, fonts), tone (e.g. calm/editorial, bold/tech, playful), must-have sections, stack (Next.js/React/Vite/plain HTML).

## Step 2 — Choose ONE visual direction

| Direction | Load |
|---|---|
| Anti-generic, modern default | `design-taste-frontend` |
| Soft, expensive, agency look | `high-end-visual-design` |
| Clean editorial / Notion-like | `minimalist-ui` |
| Raw, grid, terminal, data-heavy | `industrial-brutalist-ui` |
| Match a known brand's language | `awesome-design-md` (pick a reference DESIGN.md) |
| Need a searchable palette/font/style database | `ui-ux-pro-max` |
| Existing site to upgrade | `redesign-existing-projects` (audit first) |

Never load two direction skills at once — they have conflicting rules. `ui-ux-pro-max` and `awesome-design-md` are reference data and can be combined with one direction.

Image-generation skills (`imagegen-frontend-web/-mobile`, `brandkit`, `image-to-code`) and `stitch-design-taste` are parked in `.claude/skills-extra/` — they need an image-generation tool. Use them only if the user moves them back into `skills/`.

## Step 3 — Motion layer (only what the story needs)

| Need | Load |
|---|---|
| Component micro-interactions | `premium-interaction-craft` + `motion-framer` (React) |
| Timelines, text reveals, SVG | `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-react` |
| Scroll narrative / pinning | `scroll-storytelling` + `gsap-scrolltrigger` |
| Smooth scroll feel | `lenis-smooth-scroll` |
| Lightweight JS animation without GSAP | `animejs` |
| Always when animating a lot | `gsap-performance` |

## Step 4 — 3D / WebGL layer (optional, must justify)

`threejs-webgl` (vanilla), `react-three-fiber` (React), `shader-glsl` (custom shaders / gradients), `particle-system`. For 3D + scroll: drive the camera/uniforms from a `gsap-scrolltrigger` timeline inside the render loop. Ready-made pieces: see `ui-component-sources`.

Rules: 3D must support the message. Provide a static poster fallback, lazy-load the canvas below the fold, pause rendering when off-screen or tab hidden, cap DPR at 2 (1.5 on mobile).

## Step 5 — Build

- Load `full-output-enforcement` for large generations so nothing is left as a placeholder.
- React/Next.js: follow `react-best-practices` and `composition-patterns`.
- Components: prefer an existing library from `ui-component-sources` over hand-rolling complex primitives.

## Step 6 — Budgets (non-negotiable)

- Lighthouse (mobile) Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95 on the main page.
- Core Web Vitals: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.
- Initial JS for a landing page: aim ≤ 200KB gzipped (3D libs lazy-loaded).
- Hero image/video optimised (AVIF/WebP, correct `sizes`, poster for video, `fetchpriority="high"` on the LCP image only).

## Step 7 — Review before calling it done

1. `web-design-guidelines` (Vercel's UI rules) on changed files.
2. `checklist-design` audit/critique on the rendered page.
3. The `post-code-cleanup` skill, then `.claude/checklists/website-quality.md` and `after-coding.md`.
4. If Reticle is set up: `reticle-verify-ui-change` on the main flows.
