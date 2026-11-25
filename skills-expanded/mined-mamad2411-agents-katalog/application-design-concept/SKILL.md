---
name: application-design-concept
description: Develop design concepts, visual identities, and design systems for digital products with genuine point-of-view and craft. Use this skill whenever the user asks for a design concept, visual direction, design system, brand language, mood, vibe, aesthetic direction, theme, design tokens, style guide, art direction, or visual identity — anything upstream of writing UI components. Also use when a request to "design" something is ambiguous between concept and implementation; clarify intent, then anchor the work conceptually before any pixels appear. This skill exists specifically to counter AI-generated design slop and produce work with a human point of view.
---

# Design Concept

A skill for developing design concepts, visual identities, and design systems that have a point of view — not generic AI aesthetics dressed up with gradients.

## What this skill is for

Use this skill when the work is upstream of components. The user wants:

- A **concept / direction** for a product they haven't visualized yet
- A **design system** — tokens, principles, components, voice
- A **visual identity** for a product or feature
- A **mood / vibe / aesthetic** that other deliverables will derive from
- A **style guide or theme spec** a developer will implement

If the user just wants a single beautiful screen built RIGHT NOW, prefer the `frontend-design` skill. This skill is about the upstream thinking and the system — not the artifact. The two compose well: develop a concept here, then implement against that concept with `frontend-design`.

## Why this skill exists

AI design defaults to a recognizable palette of safe choices: Inter typeface, soft purple-to-blue gradients, glassmorphism, 12px radius on everything, three-card grids, "Modern. Minimal. Clean." copy. Output is technically competent and emotionally vacant. It looks designed but means nothing.

Human design — even minimal human design — carries traces of intent: a chosen material, a referenced era, a deliberate imperfection, a specific cultural register. The design says something. It commits.

This skill exists to make agents commit.

## The core principle: concept before pixels

Move through stages in order. Each stage produces a written artifact the next stage builds on. **Do not jump ahead.** Skipping the brief is how you end up with another purple-gradient dashboard.

```
1. Brief        → who, what, why, what feeling
2. Position     → the one idea, the lineage, what we reject
3. System       → tokens, components, voice, motion
4. Audit        → human-touch check, anti-slop sweep
5. Showcase     → optional: prove it with one artifact
```

---

## Stage 1: Brief — understand before deciding

Before any aesthetic choice, get clarity on:

- **What is this thing?** Function in one sentence. "A meditation app" is not enough — "a meditation app for people who already meditate and find consumer apps condescending" is enough.
- **Who uses it?** A specific person in a specific situation, not "users."
- **What emotional state are they in when they open it?** Anxious, bored, grieving, excited, distracted. The state shapes everything that follows.
- **What's the brand truth?** If existing: what's already real about it? If new: what's the founding belief — the thing the founders would die on a hill for?
- **What's the one feeling someone should leave with?** One word. Force the choice.
- **What does this replace?** The alternative reveals what the design must be _against_.

If the user hasn't given enough material to answer these, ASK before proceeding. A good brief is worth ten rounds of iteration. Don't infer in silence.

When the brief is clear, write it up using the structure in `references/concept-brief-template.md`. The brief is a deliverable — the user should be able to read it and say "yes, that's what I meant."

---

## Stage 2: Position — commit to one idea

This is the stage agents are most tempted to skip. Don't.

Pick **one** of these as the anchor for the whole design:

- **A metaphor** — "this app is a hotel concierge," "this dashboard is a control tower," "this profile is a museum vitrine." The metaphor governs material, hierarchy, language.
- **A cultural lineage** — Swiss editorial, Japanese stationery, mid-century industrial, Memphis, vernacular signage, terminal/CLI, broadsheet newspaper, technical manual, zine, museum wall text. See `references/aesthetic-lineages.md` for a working list and what each one _actually means_ beyond the name.
- **A material** — paper, glass, concrete, fabric, metal, ink, light, plastic. Materials carry physics: weight, edge, transparency, how they age. Choose one and let it govern.
- **A constraint** — "no images," "monochrome," "everything is a list," "type-only." Constraints generate character faster than freedom does.

Then write three sentences:

1. **What this design IS** — the anchor stated plainly.
2. **What this design IS NOT** — three to five things you reject. Be specific. "Not a dashboard" / "not Stripe-clean" / "not Material Design" / "not minimalist for its own sake."
3. **The one detail someone will remember** — what is the unforgettable thing? A single moment, mark, or move.

A position you can't summarize this tightly isn't a position yet. Push back on yourself until it fits.

**Avoid these positioning failures:**

- "Modern, minimalist, clean" — these are non-positions. Every product says this. They commit to nothing.
- "Inspired by Apple / Stripe / Linear" — naming a tech company instead of an actual aesthetic tradition is how AI slop happens. Reach further back.
- Multiple anchors — "Swiss editorial AND Memphis AND brutalist" is just chaos. Pick one.

---

## Stage 3: System — derive everything from the position

Now and only now, translate the position into a system. The test for every choice: **does it follow from the position, or am I picking what I always pick?**

### Typography

Pick a _type pairing_ that argues for the position, not against it. A position of "technical manual" with Playfair Display is a contradiction. A position of "editorial gravity" with Inter is a wasted opportunity.

- Choose two faces with a real relationship — contrast (display + serif body) or kinship (two cuts from one foundry).
- Specify the weights, sizes, line-heights, and letter-spacing as a system, not per-element ad hoc.
- Avoid the AI defaults: Inter, Roboto, Arial, Open Sans, Helvetica Neue, Space Grotesk. They are not bad fonts; they are exhausted ones. Reach for something with a face.
- If you don't know fonts deeply, name the _quality_ you want and let the user or a designer pick the specific face: "wants a humanist sans with warmth in the lowercase" is more useful than naming a font you half-remember.

### Color

Build a palette, not a swatch wall.

- Start from one anchor color tied to the position. Everything else relates to it.
- Specify roles, not just values: surface, surface-raised, ink, ink-soft, accent, accent-pressed, warning, warning-soft. A token without a role is decoration.
- Constrain. Most beautiful systems use 5–8 distinct colors total, with carefully tuned shades. AI slop comes from undisciplined palettes — fifteen grays, three blues, a teal, a "brand purple."
- Test the palette in dark mode if relevant. Dark mode is not "invert the lightness" — it's a separate system that has to be designed.

### Spacing & rhythm

- Pick a base unit (4px, 8px, sometimes a typographic em). Build the spacing scale on it.
- Decide the rhythm — tight and dense (editorial, technical), generous (luxury, contemplative), or syncopated (editorial-with-attitude). Don't default to "comfortable."
- Specify a small set of radius values — and prefer a single radius across the system unless you have a reason for more. "Different radius on different components" is almost always slop.

### Motion

- Define motion as a system: durations, easings, what gets animated and what doesn't.
- Most slop animation is decorative — things that wiggle for no reason. Animate to communicate state, not to entertain.
- Pick a motion _character_ — crisp and fast, weighty and slow, springy, mechanical. The character should match the position.

### Voice & tone

This is where AI design fails hardest. Generic, friendly, focus-grouped microcopy is the audio equivalent of a purple gradient.

- Specify a voice with concrete contrasts: "we say X, never Y." E.g. "we say 'last seen 4 minutes ago,' never 'just now ✨'."
- Provide examples for empty states, error states, success states, confirmation dialogs. These are where voice lives.
- Match the voice to the brief. A grief support product and a fantasy football product cannot share microcopy patterns.

### Components

Don't enumerate every component upfront. Define the **vocabulary** — the patterns from which components derive — and a few keystone components in detail (typically: the primary button, an input, a card or list row, a navigation pattern, an empty state).

Document each component with: anatomy, states, behavior, and the _reason_ it looks the way it does. Reasons matter — they're how the system survives contact with new screens.

For the full structure, see `references/design-system-spec.md`.

---

## Stage 4: Audit — the human-touch check

Before declaring done, run two passes.

### The anti-slop sweep

Open `references/anti-slop-checklist.md` and walk it. Each item is a tell — a thing that signals AI design. Either remove the tell or make it deliberate (i.e., justify it in writing as part of the position).

This is not optional. Most slop survives because nobody looked for it.

### The human-touch check

Ask, plainly:

1. **Could a human designer who saw only the output say "I made this"?** Not "this is competent" — "this is _mine_." If not, the design has no fingerprints. Add some.
2. **Does at least one choice trade off something?** Real design rejects. If every choice is "and also," the design has no spine.
3. **Is there one detail that wouldn't survive a committee?** A type choice that's a little weird, a layout move that's a little risky, a color that's a little uncomfortable. If every choice is safe, the result will be invisible.
4. **Is the position legible from the output alone?** Show someone the deliverable without the brief. Can they reconstruct what the design is _about_? If not, the position didn't make it into the pixels.
5. **Does the voice survive in the empty states?** Empty states are where voice dies first. Re-read them.

If any answer is no, return to Stage 2 or 3. Don't paper over it with more decoration.

---

## Stage 5: Showcase — optional, prove it works

If the user wants visual proof, build ONE artifact that demonstrates the system in action. Not five — one. The discipline of choosing the most representative screen forces the system to be coherent.

Hand off to the `frontend-design` skill for the actual implementation. Pass it the position document and the design system spec — that's what makes it implementation rather than fresh invention.

---

## Output formats

Default output is markdown documents (concept brief + design system spec) plus, if relevant, a single proof artifact. Use `references/concept-brief-template.md` and `references/design-system-spec.md` as starting structures — adapt them; don't fill them in robotically.

If the user asks for design tokens in code form (CSS variables, JSON, Tailwind config, Style Dictionary), produce them — but only after the system is documented, so the tokens have meaning attached.

If the user asks for a Figma-ready spec, structure the document with: tokens table, type scale table, spacing scale, component anatomies. Designers can import that quickly.

---

## When the user pushes for a quick aesthetic

A common situation: the user says "just give me a vibe, I don't need all this." Two responses depending on context:

- **If the deliverable is genuinely small** (a single landing page, a one-off poster), compress: do a one-paragraph brief, a one-sentence position, and skip straight to the system. But still do them in order.
- **If the deliverable is larger** (a product, an app, a brand), gently push back: "I can give you a vibe in 30 seconds, but it'll be the same vibe everyone else gets. Want to spend 5 minutes on the brief so it's actually yours?" Most users say yes when asked.

Never silently skip the brief. Silent skipping is how slop happens.

---

## Reference files

Load these when you reach the relevant stage. Don't load all of them upfront.

- `references/concept-brief-template.md` — Structure for the brief and position document. Load at Stage 1–2.
- `references/aesthetic-lineages.md` — Working list of design traditions, what each one means, and how to draw on them without cosplay. Load at Stage 2 when picking a position.
- `references/anti-slop-checklist.md` — Concrete tells of AI design and how to avoid each. Load at Stage 4.
- `references/design-system-spec.md` — Structure for documenting tokens, components, voice. Load at Stage 3.

---

## A final note on craft

The reason AI design slops is that the model has read a million Dribbble shots and zero design briefs. It pattern-matches surface and skips substance. This skill's whole job is to invert that — to force substance first, surface last.

When done well, the output should feel like it was _for_ this product and no other. That's the bar. Anything less is slop wearing a nicer font.
