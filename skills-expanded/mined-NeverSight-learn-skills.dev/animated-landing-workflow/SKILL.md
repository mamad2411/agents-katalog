---
name: animated-landing-workflow
description: Applied workflow skill for producing Awwwards-caliber animated landing pages using Claude Design as the orchestrator, with motionsites.ai (animated backgrounds), higgsfield.io or Kling 3 (AI animation generation), Dribbble (component inspiration), shots.so (animation showcase/video edit), and land-book (landing page templates) as the accelerator toolchain. Use when the user asks to design, prototype, animate, or ship a landing page with motion — from bare idea to code-ready handoff. Orchestrates on top of the three design-system skills in this stack (extract-design-system, design-system-patterns, awesome-design-systems) and hands off to existing animation-code skills (awwwards-animations, modern-web-design) for implementation.
---

# Animated Landing Workflow

## Purpose

This skill encodes a **reproducible pipeline for producing top-tier animated landing pages**, sourced from a tutorial by [Viktor Oddy (@viktoroddy on X)](https://x.com/viktoroddy/status/2045492112054165813), published shortly after Anthropic launched [Claude Design](https://claude.ai/design) on 2026-04-17. Claude Design is the orchestrator; five accelerator tools feed it inspiration, animated backgrounds, AI-generated animation previews, component references, showcase assets, and full-page templates.

It is **not** a code-pattern skill. For GSAP / Framer Motion / Anime.js / Lenis code, defer to the `awwwards-animations` skill. This skill owns the **pre-code orchestration layer**: how to move from a blank brief to a vetted visual prototype ready for Claude Code to implement.

## Where it fits in the stack

This is the fourth skill in the `design-system-stack` repo. The stack's four tiers:

1. **PRIMARY — how to extract:** `extract-design-system` (tokens + primitives from an existing site)
2. **PRIMARY — how to build:** `design-system-patterns` (token hierarchy, theming, variants, pipelines)
3. **COMPLEMENTARY — catalog:** `awesome-design-systems` (185 shipped systems indexed by feature flag)
4. **APPLIED WORKFLOW — this skill:** pre-code orchestration for animated landings

This skill **uses** the other three. During the workflow, it calls on `awesome-design-systems` for precedent lookups, `design-system-patterns` for token-and-variant decisions, and `extract-design-system` if the landing needs to inherit an existing brand's primitives.

## The toolchain — at a glance

| Tool | Role | When to use |
|---|---|---|
| **[Claude Design](https://claude.ai/design)** | Orchestrator. Generates prototypes, wireframes, code-powered previews; exports Canva/PDF/PPTX/standalone HTML; reads your codebase + design files; bundles a handoff for Claude Code. Powered by Claude Opus 4.7. Available on Pro/Max/Team/Enterprise. | Always — this is the central surface. Everything else feeds it or ships from it. |
| **[motionsites.ai](https://motionsites.ai)** | Animated background library — ready-made animated backgrounds you export and hand to an LLM to generate the equivalent code for your own site. | Hero sections, full-bleed backgrounds, section dividers — anywhere you want motion behind content. |
| **[higgsfield.io](https://higgsfield.io)** | AI-driven animation generation. Quickly previews how animations will feel on the page. Alternative: **Kling 3** (see `references/tool-inventory.md`). Similar in spirit to wavespeed-style preview tools. | Exploring animation style options before committing to a GSAP/Motion implementation. |
| **[Dribbble](https://dribbble.com)** | Component-level design inspiration — buttons, stat cards, data widgets, micro-interactions. | Mining specific component patterns (a button treatment, a stats tile) rather than whole pages. |
| **[shots.so](https://shots.so)** | Browser-based video editor with high-end "liquid-crystal" showcase templates. Wraps animations in polished frames/backgrounds for portfolio shots and client deliverables. | Presenting completed animations — demo videos, pitch decks, Twitter/X post embeds. |
| **[land-book](https://land-book.com)** | Curated gallery of full landing-page templates. | Starting skeletons — layout, section order, typography scale, overall composition. |

**Note on URLs:** exact domains reflect the tutorial at time of capture (2026-04-20). Verify each on first use — AI/design tools rebrand frequently.

## The pipeline — 6 stages

Full detail in `references/workflow-pipeline.md`. High-level:

1. **Inspiration & framing** — pull layout references from `land-book`, component references from `Dribbble`, animated-background candidates from `motionsites.ai`. Capture 3–5 references per axis. Run precedent lookups through `awesome-design-systems` for industry-matched design systems.
2. **Asset generation** — export chosen `motionsites` background → feed to an LLM (Claude) to generate the equivalent self-hosted implementation. Preview candidate hero/section animations in `higgsfield.io` (or Kling 3) to validate style.
3. **Token & architecture decisions** — consult `design-system-patterns` for the token hierarchy, theming, and variant system. **Animation timing and easing are tokens too** — express them as CSS custom properties (`--duration-*`, `--ease-*`) so motion feel can be tuned in one place rather than hunted across components. Consult `extract-design-system` if inheriting an existing brand.
4. **Visual prototype in Claude Design** — at `claude.ai/design`, assemble the landing from references, prompts, and uploaded assets. Iterate with inline comments + adjustment knobs (spacing, color, layout).
5. **Handoff to Claude Code** — Claude Design packages a handoff bundle; pass it to Claude Code with one instruction. Delegate animation implementation to the `awwwards-animations` skill (GSAP / Motion / Lenis patterns).
6. **Showcase & ship** — use `shots.so` to produce a demo reel of the finished animation for portfolio / pitch / social. Ship the code.

## When to use this skill

Load this skill for any of these user intents:

- **"Help me build an animated landing page."**
- **"Design a hero section with a moving background."**
- **"Turn this Dribbble shot into a live landing page."**
- **"Recreate this motionsites.ai background in code."**
- **"Use Claude Design to prototype X, then hand it off to Claude Code."**
- **"I need an Awwwards-caliber landing for {product}."**
- **"Prepare a showcase reel of my finished landing animation."**

## Reference routing table

| Question | File | Contains |
|---|---|---|
| Deep dive on each tool — alternatives, pricing tier, export formats, caveats | `references/tool-inventory.md` | 6 tools, each with purpose, inputs/outputs, alternatives, failure modes |
| Step-by-step from blank brief to shipped code | `references/workflow-pipeline.md` | Full 6-stage pipeline with per-stage checklists and prompts |
| Claude Design → Claude Code handoff mechanics | `references/handoff-to-code.md` | What a "handoff bundle" contains, how to phrase the Claude Code prompt, where the `awwwards-animations` skill plugs in |

## How this skill behaves in-conversation

- When the user names one of the 6 tools, load `references/tool-inventory.md` before answering.
- When the user asks for a "workflow" or "how do I go from X to Y," load `references/workflow-pipeline.md`.
- When the user says "hand off" / "Claude Design" / "Claude Code bundle," load `references/handoff-to-code.md`.
- Always cite the originator of the workflow: [Viktor Oddy (@viktoroddy)](https://x.com/viktoroddy/status/2045492112054165813).
- Always defer to `awwwards-animations` (if installed) for the actual animation code — this skill stops at handoff.

## Caveats & honesty

- **Tool accuracy lives at the tutorial's capture date (2026-04-20).** URLs and UI flows change. If a domain 404s, note it and search for the current equivalent rather than guessing.
- **Claude Design access:** Pro / Max / Team / Enterprise. Enterprise orgs have it off by default (admin toggle). If the user is on Free, this workflow partially degrades — skip Stage 4, use a different prototyping surface (v0, Figma), keep everything else.
- **Claude Design model:** Opus 4.7 as of launch (2026-04-17). Version may drift.
- **Credit upstream when teaching the workflow.** The pipeline isn't mine or the user's — it's Viktor Oddy's. Attribution is part of the skill.
- **This skill does NOT generate animation code.** For GSAP / Motion / Lenis / Anime.js code patterns, the caller should also have `awwwards-animations` installed and should defer to it at Stage 5.

## Sources

- Workflow: [Viktor Oddy (@viktoroddy), X post 2045492112054165813](https://x.com/viktoroddy/status/2045492112054165813) (captured 2026-04-20)
- Claude Design: [Anthropic Labs announcement, 2026-04-17](https://www.anthropic.com/news/claude-design-anthropic-labs) · entry point: [claude.ai/design](https://claude.ai/design)
