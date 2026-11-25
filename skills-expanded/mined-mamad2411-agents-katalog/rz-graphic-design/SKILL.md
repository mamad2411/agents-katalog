---
name: rz-graphic-design
description: >
  Use when producing visual assets: social media graphics, LinkedIn post images, slides, diagrams, infographics, architecture diagrams, framework visualizations, speaker one-sheets, or brand-consistent imagery. Also for visualizing the five-step context generation process, RAG vs Context Layer comparisons, or building talk decks. Skip for product or UI design (use rz-product-design).
---

# Graphic Design — Riché Zamor

You produce visual assets that reinforce Riché's "Neural Architect" brand identity. Every visual should feel like it came from the same system: technical, precise, dark-themed, and architecturally structured.

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited below are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). Doc ownership, canonical constants (thesis label, channels, cadence, North Star), and the Decision-of-Record log. Honor it; flag drift.
2. **Your sections of the Corpus** at `Projects > RZ Claude Skills > Corpus`:
   - `brand-system` → page `357ac0ea-4f65-8163-b0a9-c51f37062fc0` (identity, presentation, social, diagrams)
   - `ux-principles` → page `357ac0ea-4f65-8180-a1cf-f97ce0f3e11d` (visual hierarchy, typography, color, spacing)
   - `content-system` → page `357ac0ea-4f65-8160-8762-eddfa6307d47` (when graphic ties to a specific post format)
   - `voice` → page `357ac0ea-4f65-8194-ae1e-e5147adad60c` (when overlay copy is needed)

Each Corpus directory page lists its child entries. Fetch only the specific entries you need.

## Quick Reference

| Operation | What you produce | Anchor in corpus |
|---|---|---|
| Social graphic (LinkedIn, X) | 1200x627 / 1080x1080 / 1600x900 image, dark bg, mobile readable | `corpus/brand-system/social/` |
| Diagram (5-step, RAG vs CL, flywheel) | SVG node-and-edge structure, transformation visible | `corpus/brand-system/diagrams/` |
| Talk slide deck | One idea per slide, dark bg, code/architecture anchors | `corpus/brand-system/presentation/` |
| Color or type spec lookup | Hex codes, accent rule, font pairing | `corpus/brand-system/identity/palette.yaml`, `typography-rules.md` |
| Anti-pattern check | Reject pastels, neon, glowing brains, stock photos | `color-anti-patterns.md`, `imagery-anti-patterns.md` |

## Load from corpus

**Brand visual identity** — `corpus/brand-system/identity/`:
- `neural-architect-overview.md` — the theme: technical, precise, dark, architecturally structured
- `palette.yaml` — programmatic palette lookup
- `color-palette.md` — backgrounds (#0a0a0a–#1a1a1a, #2a2a2a), text (#f5f5f5, #a0a0a0)
- `accent-colors.md` — one per project from electric blue / emerald green / amber
- `color-anti-patterns.md` — never pastels, decorative gradients, neon
- `typography-rules.md` — Inter / system sans for body, JetBrains Mono / Fira Code for technical
- `imagery-style.md` — architectural, structural, systems-oriented; node-and-edge diagrams
- `imagery-anti-patterns.md` — never stock photos of people pointing, robots, glowing brains, circuit boards
- `logo-feel.md` — IDE icon or developer-tool logo aesthetic

**Diagram templates** — `corpus/brand-system/diagrams/`:
- `five-step-context-flow.md` — 5 stages, transformation visible at each, NOT a passive pipeline
- `rag-vs-context-layer-comparison.md` — side-by-side; the gap between is the visual argument
- `context-quality-framework.md` — freshness × consistency × completeness × goal-alignment (radar / 2x2 / cards)
- `flywheel-diagrams.md` — circular reinforcing loops; pairs with growth flywheel

**Presentation design** — `corpus/brand-system/presentation/`:
- `one-idea-per-slide.md`, `minimal-text-max-impact.md`, `dark-bg-high-contrast.md`
- `code-and-architecture-anchors.md`, `no-bullet-walls.md`
- `talk-structure-template.md` — 6-step arc: opening moment → problem → thesis → evidence → framework → close

**Social media graphics** — `corpus/brand-system/social/`:
- `aspect-ratios.md` — LinkedIn 1200x627 or 1080x1080, X 1600x900
- `mobile-thumbnail-readability.md` — text overlays readable at 375px
- `non-templated-feel.md` — brand-consistent but not Canva-default
- `diagrams-over-abstract.md` — substance over decoration
- `corner-treatment.md` — slight border radius (4-8px), never fully rounded
- `attribution-placement.md` — Riché's name/handle subtly in corner

**Implementation** — `corpus/brand-system/implementation/`:
- `svg-for-diagrams.md`, `css-tailwind-layouts.md`, `react-interactive.md`, `2x-export-retina.md`

**Cross-medium principles** — `corpus/brand-system/principles/`:
- `medium-determines-spec.md` — when medium isn't specified, ask first
- `consistent-visual-language.md` — same colors, type scale, spacing rhythm across all outputs

## How to apply

1. Load `palette.yaml` for color lookups; load specific identity entries for application rules.
2. For diagrams, pull the matching template entry — don't invent structures.
3. For talks, use `talk-structure-template.md` to scaffold; pair with `corpus/content-system/format-talk-abstract.md` for content.
4. For social, the aspect ratio + mobile readability + non-templated rules apply universally.
5. When the medium isn't specified, ask first — medium determines spec.

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Glowing brain or robot imagery | Reads as generic AI stock content, breaks Neural Architect feel | Use node-and-edge diagrams from `corpus/brand-system/diagrams/`, structural visuals only |
| Stock photos of people pointing at screens | Generic, decorative, not substantive | Replace with diagrams or code anchors per `imagery-anti-patterns.md` |
| Pastel or neon accent colors | Violates dark theme and the one-accent-per-project rule | Pick one of electric blue, emerald green, or amber from `accent-colors.md` |
| Decorative gradients or rainbow palettes | AI Slop signal, dilutes brand precision | Solid backgrounds in #0a0a0a to #2a2a2a range, no gradients |
| Text overlay unreadable at 375px width | Mobile users (majority of feed) cannot parse the graphic | Test thumbnail at phone size, follow `mobile-thumbnail-readability.md` |
| Canva default templates with stock icons | Reads as templated, not branded | Apply `non-templated-feel.md`, custom layout, IDE-style aesthetic |

## Cross-skill connections

**Upstream (reads from these for canonical knowledge):**
- `rz-copywriting`. Voice and hook patterns for any text overlays in graphics. Corpus path: `corpus/voice/`.
- `rz-product-design`. UX color, contrast, and typography rules to apply when graphics live inside a product surface. Corpus path: `corpus/ux-principles/`.

**Downstream (hands off to these for execution):**
- `rz-website-audit`. Fires this skill when D5 (OG image consistency) flags missing or off-brand share images.
- `rz-draft-content`. Invokes this skill in step 8 to generate content graphics that pair with a draft post or article.
