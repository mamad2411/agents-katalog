---
name: "claude-design-workflow"
description: "Build end-to-end design workflows with Claude Design for rapid UI/UX iteration"
---

# Claude Design — End-to-End Workflows

## When to activate

- Starting a new project and need a repeatable design-to-production process rather than ad hoc prompting
- A team member is new to Claude Design and needs a structured approach to avoid wasted sessions
- Switching between design contexts — startup speed, product-team consistency, design-led exploration, or marketing launch
- Existing Claude Design sessions are consuming excessive tokens without converging on a direction

## When NOT to use

- One-off throwaway prototypes with no downstream implementation — skip the workflow, prompt directly
- Projects where Figma is the source of truth and the team must approve Figma files before any development starts — use Figma's AI tools and import to Claude Code manually
- When pixel-perfect client approval mockups are required before any engineering begins — Claude Design is not a Figma replacement for that gate
- When a design direction is already locked in Claude Code — do not return to Claude Design; iterate in code

## Instructions

Four workflows covering the four most common usage contexts. Each is designed to minimize token waste and time-to-production.

---

### Workflow 1: Rapid Validation (Startup / MVP)

Goal: validated UI direction from spec to working code in under six hours, same day.

**Phase 1 — Concept (30 minutes, one session)**

Open a fresh Claude Design session. Provide:
- Target audience (one sentence)
- Core features to show (3–5 maximum)
- Brand constraints: two hex colors and a font reference (a Google Font name or a style descriptor like "geometric sans")

Prompt:

```
"Show 3 layout directions for [product type] targeting [audience]. Core features:
[feature 1], [feature 2], [feature 3]. Brand: primary [hex], accent [hex],
[font name or descriptor]. Show all 3 side by side."
```

Output: three distinct layout directions. Decision: pick the winning direction and note one or two specific elements from the others worth carrying forward (color from A, card treatment from B).

**Phase 2 — Refinement (30 minutes, same or fresh session)**

Apply the cross-direction decisions with a specific instruction:

```
"Apply [element from version A] to [layout of version B]. Keep [specific element].
Change [specific element] to [target state]."
```

Use the Tweaks panel for spacing, typography weight, and color intensity adjustments. This costs no tokens. Only prompt for structural changes that Tweaks cannot handle.

Output: single refined direction. Do not continue iterating beyond one refinement pass — perfectionism at this phase delays production without improving the final product.

**Phase 3 — Handoff to Claude Code (immediately after direction is locked)**

Export the Claude Code bundle. Hand it to Claude Code with the implementation target:

```
"Implement this Claude Design bundle as [React with Tailwind / plain HTML+CSS /
Vue with shadcn]. Match the token values exactly. Use the layout as a reference,
not a pixel-perfect spec. Flag any deviations from the design."
```

Do not return to Claude Design after this point. All UI iteration happens in Claude Code against the actual component tree.

Result: validated direction to production code, same day, under six hours.

---

### Workflow 2: Design System Foundation (Product Teams)

Goal: a reusable design system context that makes every future Claude Design session consistent and token-efficient.

**Session 0 — System Setup (2–3 hours, runs once)**

This session is high token use and runs one time. Treat it as an investment — it reduces per-feature session cost by 60–70% afterward.

Provide:
- Codebase (or a summary of the component library in use — shadcn/ui, MUI, Radix, etc.)
- 5–10 screenshots of finished product screens showing the existing visual language
- Brand guidelines document or a written summary (colors, typography, spacing principles, do-not-dos)

Prompt:

```
"Extract the design system from these product screenshots and brand guidelines.
Identify: color tokens (primary, secondary, surface, border, text hierarchy),
typography scale (size, weight, line-height per level), spacing scale,
border radius values, and shadow tokens. Output as a JSON token file and a
summary of the component conventions (card style, button variants, input style).
Then generate a test component — a feature card — using the extracted system."
```

Validate the test component against a real product screenshot. Correct any extraction errors before proceeding. Once the system is correct, export the token file (JSON format) and store it at:

```
project-root/
└── design-system/
    └── tokens.json       ← from Claude Design extraction
    └── system-notes.md   ← component conventions in plain text
```

Save this session as a Claude Project so the design system context persists across all future design sessions without re-upload.

**Per-Feature Sessions (after system setup)**

Open a session in the Claude Project containing the design system. Brand and tokens are already present in context — do not re-upload.

Prompt for a new feature:

```
"Design the [feature name] screen. Users need to [primary task]. Key elements:
[list]. Follow the established design system. Use existing component patterns
where they apply."
```

Token use is 60–70% lower than a system-naive session because correction cycles are eliminated. Output will match the existing product without explicit brand enforcement in every prompt.

**Integration with Development**

Export the Claude Code bundle per feature. The token values in the bundle match the token file in `design-system/tokens.json`. If the codebase already imports those tokens (via CSS variables or a Tailwind extension), generated components will inherit correct values without manual mapping.

---

### Workflow 3: Exploration-First (Design-Led Teams)

Goal: team alignment on design direction before any engineering time is committed.

**Phase 1 — Wide Exploration (1–2 hours)**

Generate a range of directions rather than a single answer:

```
"Show 5 directions for the [page or feature] homepage hero. Each should have a
distinct visual personality — vary layout, typography weight, and color treatment.
Label them 1–5."
```

Use the Tweaks panel to blend across directions: "Apply direction 3's typography to direction 1's layout." Document findings as you go — screenshot and a brief note describing what works in each (not "I like this" but "the large type on dark background reads as authoritative, which fits the enterprise buyer").

Do not prompt repeatedly in this phase trying to reach a final answer. Exploration is the output.

**Phase 2 — Direction Validation (30 minutes)**

Select the top 2–3 directions. Share each as a URL from Claude Design. Collect stakeholder feedback in a single round — not a series of async threads. Feedback must be specific:

Acceptable feedback: "The card spacing feels tight on mobile" / "The secondary color is too similar to the primary — they're not differentiating."

Feedback to decline (return it with a clarifying question): "Make it more premium" / "It should pop more."

Apply structural feedback via prompts. Apply visual tuning feedback via the Tweaks panel. Complete this phase in one sitting.

**Phase 3 — Production Path**

After direction is validated, choose one path and do not mix them:

| Team tooling | Path |
|---|---|
| Figma as source of truth | Screenshot validated direction, recreate in Figma manually (or use Canva as a bridge for non-Figma teams) |
| Claude Code as implementation layer | Export Claude Code bundle, implement |
| Direct publish (marketing pages) | Export standalone HTML, deploy |

Do not spend additional time in Claude Design after the direction is validated. The value of this workflow is the alignment it produces — not the pixel quality of the Claude Design output.

---

### Workflow 4: Landing Page Generation (Marketing Teams / Solo Builders)

Goal: production-ready landing page in under one hour with no design background.

**Step 1 — Prepare an Input Package (5 minutes)**

Gather before opening Claude Design:
- Headline and subheadline (final copy, not placeholders)
- Three value propositions (one sentence each)
- One CTA label
- Two hex color codes (if none, use a style descriptor: "deep navy and electric cyan" or "warm off-white and forest green")
- Font preference or style descriptor ("modern geometric" / "humanist serif" / "neutral SaaS")
- Audience description (one sentence: who they are, what they care about)

**Step 2 — Single Dense Prompt**

Deliver all input in one prompt. Do not split into multiple exchanges — a single dense prompt produces a more coherent first output than iterative clarifications.

```
"Build a landing page for [company]. Audience: [description — who they are,
what they care about]. Headline: '[headline]'. Subheadline: '[subheadline]'.
Value props: [prop 1] / [prop 2] / [prop 3]. CTA: '[label]'. Brand: primary
[hex or descriptor], secondary [hex or descriptor], [font style].

Section order: hero (headline + subheadline + CTA), features (3-column, value props),
social proof (logo strip or testimonial), final CTA (full-width, high contrast).

Aesthetic: [one concrete reference — e.g., 'Linear.app's dark precision' or
'Stripe's clean density' or 'Notion's approachable minimalism']. Not generic SaaS,
not card-heavy, not stock-photo hero."
```

The aesthetic reference at the end is high-leverage. A concrete reference produces more distinctive output than abstract adjectives.

**Step 3 — Tweaks Review (10–15 minutes)**

Before prompting again, use the Tweaks panel to adjust:
- Typography weight (bolder headlines often improve hierarchy without a full reprompt)
- Whitespace and section padding
- Color intensity and contrast
- Section order (drag to reorder without token cost)

This step is free — it costs no tokens and often resolves 40–60% of visual issues that would otherwise require a prompt.

**Step 4 — One Targeted Prompt Round (5 minutes)**

Address only structural issues that Tweaks cannot fix. Be specific:

```
"The hero CTA button is too small relative to the headline. Make it full-width
on mobile and 240px wide on desktop. Keep all other elements unchanged."
```

Accept 80–90% perfect output. Do not chase perfection in Claude Design — the last 10% is faster to fix in Claude Code or directly in the exported HTML.

**Step 5 — Export and Deploy**

Choose one export path:

| Deployment target | Export | Notes |
|---|---|---|
| Shopify / WordPress / ClickFunnels | Standalone HTML | Self-contained CSS, no build step, drop directly into a page builder's HTML block |
| Custom CMS or dynamic content | Claude Code bundle | Implement in Claude Code; wire dynamic fields to CMS data |
| Collaborative polish before publish | Canva export | For teams that need non-developer editing before launch |
| Direct file deploy (S3, Netlify Drop) | Standalone HTML | Works without any build tooling |

Result: production landing page, 45–60 minutes, no design background required.

## Example

A solo SaaS founder is launching a waitlist page for an AI code review tool. They have final copy, no designer, and a conference demo in four hours.

**Input package:**

- Headline: "Code review that thinks like a senior engineer"
- Subheadline: "AI-powered review that catches logic errors, not just style."
- Value props: "Integrates with GitHub in 60 seconds" / "Explains why, not just what" / "Zero configuration, works on any stack"
- CTA: "Join the waitlist"
- Brand: primary #1C1C2E, accent #6EE7B7, font: "clean geometric sans"
- Audience: "mid-level engineers at startups who are frustrated by shallow PR review from teammates"

**Step 2 prompt:**

```
"Build a landing page for Revue, an AI code review tool. Audience: mid-level
engineers at startups frustrated by shallow PR review. Headline: 'Code review
that thinks like a senior engineer'. Subheadline: 'AI-powered review that catches
logic errors, not just style.' Value props: 'Integrates with GitHub in 60 seconds'
/ 'Explains why, not just what' / 'Zero configuration, works on any stack'.
CTA: 'Join the waitlist'. Brand: primary #1C1C2E, accent #6EE7B7, geometric sans.

Section order: hero, features (3-column), waitlist form (email input + CTA),
minimal footer.

Aesthetic: Linear.app's dark precision. Not card-heavy, not stock-photo hero,
not generic SaaS purple."
```

**Step 3 — Tweaks decisions:**

- Increased headline font weight from regular to bold (improved hierarchy immediately)
- Reduced section padding — the default had too much air between hero and features
- Shifted accent color intensity down 10% — the default #6EE7B7 was too saturated against the dark background

**Step 4 — One prompt:**

```
"The waitlist form section needs a subtle divider from the features section above it.
Add a thin horizontal rule in #2E2E42. Keep everything else as-is."
```

**Export decision:** standalone HTML. The founder is using Netlify Drop — drag the file, live in 30 seconds. No CMS needed; the waitlist form action will point to a Mailchimp embed URL added manually to the HTML after export.
