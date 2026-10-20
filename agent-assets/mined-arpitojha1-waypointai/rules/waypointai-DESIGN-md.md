# Waypoint — Design Reference
> flat void canvas, cream type, one neon accent per opportunity type

**Theme:** dark

Waypoint is a product UI, not a marketing site — so this adapts the flat-dark/neon-glow language you liked (GSAP's site) but drops everything that only makes sense on a landing page: the 224px hero, the two-column tool-showcase blocks, the promotional banner. What carries over: a near-black canvas, cream-white type, zero shadows/elevation, pill-shaped interactive elements, hairline dividers for rhythm, and — the important part — **color as the organizing system**. GSAP gave each plugin its own accent hue; Waypoint gives each **opportunity type** its own accent hue, and each **step status** its own accent hue. A user should be able to tell a job from a hackathon from a GitHub issue by color alone, at a glance, before reading a word.

Working name: **Waypoint**. Swap freely.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Void Black | `#0e100f` | `--color-void-black` | Page canvas, card surfaces — the dark stage everything else glows against |
| Cream Glow | `#fffce1` | `--color-cream-glow` | Primary text, borders, icon strokes — softer than pure white |
| Olive Stone | `#42433d` | `--color-olive-stone` | Hairline dividers, muted borders, low-emphasis structure |
| Ash Gray | `#7c7c6f` | `--color-ash-gray` | Metadata, timestamps, pending-step state, helper text |
| **Issue Green** | `#0ae448` → `#abff84` gradient | `--color-issue-green` | GitHub issue opportunities. Also doubles as "step done" — reads naturally as GitHub's own green, and as completion. |
| **Job Blue** | `#00bae2` | `--color-job-blue` | Job posting opportunities (Arbeitnow). Technical/precise read, fits skill-gap-diff framing. |
| **Hackathon Orange** | `#ff8709` | `--color-hackathon-orange` | Hackathon opportunities (Devpost). Time-boxed, urgent, matches deadline pressure. |
| Reject Red | `#ff5c5c` | `--color-reject-red` | Step rejected state, delete/destructive actions. Not present in the GSAP palette — added because the app needs a real negative-state color the source system didn't. |
| Memify Violet | `#9d95ff` | `--color-memify-violet` | Reserved exclusively for the "adapted by memory" signal — badges, glow outline on a step that Cognee's `improve`/`memify` reordered. Never used for anything else, so it stays legible as a distinct event. |

One accent per card, one accent per badge. Don't mix Job Blue and Hackathon Orange on the same element.

## Tokens — Typography

Two faces, not one — GSAP's Mori is proprietary and its 224px hero scale doesn't apply to a dashboard. Dropped the hero/display sizes entirely; kept the tight tracking discipline.

**UI Sans** — `Inter Tight` (or Geist Sans). Body copy, nav, card titles, buttons. Weight 400 default, 600 reserved for emphasis and active states, same restraint as the source system.
**Mono** — `Geist Mono` or `JetBrains Mono`. Repo names, deadlines, JD skill tags, `$ cognee.improve()` style technical metadata — a deliberate nod to "raw primitives" that also gives the GitHub-issue and job-JD content its own visual register distinct from prose.

### Type Scale

| Role | Size | Line Height | Weight | Token |
|------|------|-------------|--------|-------|
| caption | 13px | 1.4 | 400 | `--text-caption` |
| meta-mono | 13px | 1.4 | 400 (mono) | `--text-meta-mono` |
| body-sm | 15px | 1.4 | 400 | `--text-body-sm` |
| body | 17px | 1.4 | 400 | `--text-body` |
| card-title | 20px | 1.2 | 600 | `--text-card-title` |
| section-heading | 28px | 1.15 | 400 | `--text-section-heading` |
| page-heading | 36px | 1.1 | 400 | `--text-page-heading` |

## Tokens — Spacing & Shapes

**Base unit:** 4px · **Density:** comfortable, tightening slightly for the roadmap checklist (data-dense screen)

| Element | Radius |
|---|---|
| tags / badges | 100px |
| cards | 8px |
| buttons | 100px |
| checkbox (StepItem) | 6px — the one deliberate break from full-pill, so "done" reads as a checkbox, not a toggle |

Zero shadows, same as the source. Depth comes from 1px Cream/accent borders and color contrast only.

## Components

### OpportunityCard
Void Black surface, 1px Olive Stone border, 8px radius. Top-left: type badge — pill, 1px border in the type's accent color, accent-colored text, mono font (`ISSUE` / `JOB` / `HACKATHON`). Title in card-title weight 600. Deadline/metadata row in Ash Gray, mono. No shadow, no hover-lift — on hover, border shifts from Olive Stone to the type accent at full opacity. Click → RoadmapPage.

### RoadmapView / StepItem
Checklist layout, one StepItem per row. Pending: 6px-radius empty checkbox, Cream Glow border, Ash Gray text. Done: checkbox fills Issue Green, title gets a subtle strikethrough-free "completed" treatment (color shift, not strikethrough — strikethrough reads as dismissed, not accomplished). Rejected: checkbox shows an X in Reject Red, title dims to Ash Gray at reduced opacity. Resource links render as small mono-font pill tags below the step description.

### Memify Badge
Small pill, 1px Memify Violet border, Memify Violet text, mono, reads `adapted`. Appears next to any step whose order or content changed as a result of `cognee.improve()`. On first appearance after a feedback action, the step's container gets a brief outline pulse in Memify Violet (see emil-design-eng skill for the actual motion spec) — this is the single most important visual moment in the demo, so it should never look like a generic list re-sort.

### BYOKPanel
Modal on Void Black, 1px Cream Glow border, 8px radius. Input field for OpenRouter key, mono font. Status row shows a colored dot (Issue Green = key active, Ash Gray = using default Anthropic key). "Use Default" toggle as a pill switch, not a checkbox.

### Feedback Toast
Bottom-anchored pill, Void Black fill, 1px Memify Violet border when reporting a memify event ("Roadmap adapted"), Cream Glow border otherwise. Mono text, auto-dismiss.

### Nav
Minimal horizontal bar, Nav Pills same as source system — inline text links, no container, Cream Glow, weight 600 for active route. BYOK status indicator (colored dot) lives in the nav, right-aligned.

### Hairline Divider
1px solid Olive Stone, full content width. Used between opportunity list sections and above the roadmap footer — same restrained rhythm role as the source system, no need to change it.

## Do's and Don'ts

### Do
- Keep one accent color per card/badge — type accents (Job Blue, Hackathon Orange, Issue Green) never mix on a single element
- Reserve Memify Violet exclusively for memory-adaptation signals — the moment it means anything else, the demo's key visual cue loses meaning
- Use mono font for anything technical or data-like (deadlines, repo names, skill tags, resource links) to visually separate "system output" from "prose"
- Keep the canvas flat — no shadows, no elevation, separation via 1px borders only, same as the source system
- Use full-pill radius for buttons/badges, 8px for cards, and the one deliberate 6px exception for the StepItem checkbox

### Don't
- Don't port over the 224px hero scale, the two-column tool-showcase card, or the promotional banner — those are landing-page patterns this app doesn't have a use for
- Don't introduce a second violet, orange, blue, or green — the palette is intentionally scarce so each opportunity type stays instantly identifiable
- Don't use strikethrough for completed steps — it reads as "cancelled," not "accomplished"; use color/fill state instead
- Don't animate the memify reorder with a default CSS transition — it's the demo centerpiece and gets the emil-design-eng pass, not a default

## Quick Start — CSS Custom Properties

```css
:root {
  /* Colors */
  --color-void-black: #0e100f;
  --color-cream-glow: #fffce1;
  --color-olive-stone: #42433d;
  --color-ash-gray: #7c7c6f;
  --color-issue-green: #0ae448;
  --gradient-issue-green: linear-gradient(114.41deg, #0ae448 20.74%, #abff84 65.5%);
  --color-job-blue: #00bae2;
  --color-hackathon-orange: #ff8709;
  --color-reject-red: #ff5c5c;
  --color-memify-violet: #9d95ff;

  /* Typography */
  --font-ui: 'Inter Tight', ui-sans-serif, system-ui, sans-serif;
  --font-mono: 'Geist Mono', 'JetBrains Mono', ui-monospace, monospace;

  --text-caption: 13px;
  --text-meta-mono: 13px;
  --text-body-sm: 15px;
  --text-body: 17px;
  --text-card-title: 20px;
  --text-section-heading: 28px;
  --text-page-heading: 36px;

  /* Spacing */
  --spacing-unit: 4px;
  --spacing-8: 8px;
  --spacing-16: 16px;
  --spacing-24: 24px;
  --spacing-32: 32px;

  /* Radius */
  --radius-checkbox: 6px;
  --radius-card: 8px;
  --radius-pill: 100px;

  /* Surfaces */
  --surface-canvas: #0e100f;
}
```

### Tailwind v4

```css
@theme {
  --color-void-black: #0e100f;
  --color-cream-glow: #fffce1;
  --color-olive-stone: #42433d;
  --color-ash-gray: #7c7c6f;
  --color-issue-green: #0ae448;
  --color-job-blue: #00bae2;
  --color-hackathon-orange: #ff8709;
  --color-reject-red: #ff5c5c;
  --color-memify-violet: #9d95ff;

  --font-ui: 'Inter Tight', ui-sans-serif, system-ui, sans-serif;
  --font-mono: 'Geist Mono', 'JetBrains Mono', ui-monospace, monospace;

  --radius-checkbox: 6px;
  --radius-card: 8px;
  --radius-pill: 100px;
}
```