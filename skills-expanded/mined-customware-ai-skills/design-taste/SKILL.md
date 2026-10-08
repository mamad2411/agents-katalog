---
name: design-taste
license: MIT
compatibility: Works with any AI coding assistant that supports the Agent Skills specification. Read on every UI build.
metadata:
  author: ryan-price
  version: "0.2"
description: >
  Universal visual quality skill for every Customware build. Encodes layout philosophy,
  hierarchy, restraint, rhythm, brand theming mechanics, the template contract, BrandMark
  rendering, archetype catalog, component recipes, and aesthetic anti-patterns. Read on
  every UI build. The first task agent (mitb-initial-agent) runs the vision pass once;
  this skill is the implementation contract that turns vision into a coherent app.
  Trigger signals: any UI build, improving visual quality, aesthetic balance, polished design,
  hierarchy, restraint, taste, component design, layout principles, premium feel,
  brand theming, template contract, light-mode default, BrandMark.
---

# Design Taste Skill

## What this skill is

This skill is the visual quality bar for every build. It owns both the *taste* layer (foundations, archetypes, recipes, anti-patterns) and the *mechanics* layer (template contract, brand theming, BrandMark, light-mode mandate, header right cluster).

This skill is read by:
- **mitb-initial-agent** on the first task, after the agent has stated its vision and design tokens. design-taste is the implementation contract that turns the vision into a coherent app.
- **mitb-agent-prototype** and **mitb-agent-full-access** on subsequent tasks. The vision is already in the codebase by then; design-taste guides additions to match the existing visual language.

The first task is special — it sets the design language. Every task after that respects it. Both modes use design-taste; only the first build uses it to *establish* the system, and every later build uses it to *extend* the system.

## Reading order — fully read these before writing any tokens or components

The reference files are short and necessary. Do not skim, do not partial-read with `head`, do not skip:

1. `references/archetypes.md` — full archetype catalog, token sets, reference apps, typography pairings
2. `references/components.md` — exact recipes for every common component
3. `references/anti-patterns.md` — failure modes to scan for during and before completion
4. `references/mechanics.md` — template contract, brand theming, BrandMark, light-mode mandate, header rules

If any of these is unread when you start writing tokens, your output will drift from the system. The previous build (dental scheduler, April 2026) only read SKILL.md and partial archetypes.md and produced generic-dashboard output. Read all four references in full.

---

## A. Foundations — what good design feels like

These principles describe the qualities the build should have. They're abstract on their own; the system, patterns, and recipes that follow are how each principle gets implemented.

### 1. Visual balance

Most app screens are NOT centered hero pages. Content aligns left, scans top-to-bottom, with the focal element occupying the upper third or upper-left of the main content area. Asymmetric balance — a heavy element offset by a lighter cluster of supporting elements — reads as more sophisticated than centered symmetry, which is reserved for empty states, error pages, and onboarding.

A balanced layout has:
- **One focal point per screen.** The primary score, the day's plan, the active document, the highlighted record. One — not three.
- **Supporting elements that orbit, don't compete.** Secondary information sits to the side or below at lower visual weight (smaller, lighter, less color).
- **Negative space as a design element.** Empty space isn't unfilled — it's part of what makes the focal point feel focal.

### 2. Hierarchy

Hierarchy is how the user knows what to look at first, second, third. It's built from four levers — size, weight, color, spacing — and the rule is to use ONE, occasionally two, never four at once.

- **Size hierarchy:** primary number 32px, title 20px, supporting label 14px, metadata 12px. Four sizes total. A fifth means you're trying to differentiate something that doesn't deserve differentiation.
- **Weight hierarchy:** semibold (600) for primary numbers and headings, medium (500) for titles and emphasized labels, regular (400) for body. Three weights, used systematically.
- **Color hierarchy:** foreground (primary text), muted (secondary), subtle (tertiary). Three text colors. The brand color is reserved for action, not for hierarchy.
- **Spacing hierarchy:** larger gaps (32-40px) separate major sections; medium gaps (16-24px) separate cards within a section; small gaps (8-12px) separate elements within a card.

When two elements need to feel different in importance, change ONE lever — usually size or weight. Don't change all four. Visual noise comes from over-differentiation.

### 3. Restraint

Restraint is the signature of premium design. AI defaults toward the opposite — using brand colors everywhere, adding gradients, layering shadows, multiplying decorative elements. Each individually feels like "more polish"; together they feel like a discount template.

The single most important restraint rule: **the brand or accent color appears in roughly 8-10% of pixels — no more.** Primary buttons, the active state border, the score badge fill, maybe one or two focal accents. Body text is foreground. Icons are foreground or muted. Most surfaces are neutral.

Other restraint rules:
- **No more than one primary action per screen.** Two if absolutely necessary, with one clearly subordinate.
- **No more than one focal element per screen.** Other elements are supporting context.
- **No more than 2-3 colors in any chart.** Multi-colored bars and lines are noise.
- **No more than 4 type sizes total in the entire app.** Hard ceiling.
- **No drop shadows for elevation.** Use 1px borders. Shadows immediately read as bargain-template.

Restraint produces calm. Calm is what makes the user trust the app.

### 4. Rhythm

Rhythm is the consistent spacing and sizing pattern that makes the app feel like one designer made it. It comes from using a defined scale — radius scale, spacing scale, type scale — and never improvising values.

- **8px grid for spacing.** All spacing values are multiples of 4 (4, 8, 12, 16, 20, 24, 32, 40). Invisible to the user but felt in the regularity of the layout.
- **Generous default.** When in doubt about whether a gap should be 12px or 16px, choose 16px. AI defaults to dense layouts; override the default. Premium aesthetics breathe.
- **Consistent radius by hierarchy.** Cards use one radius, chips use another, badges use another. Same hierarchy = same radius. Don't mix.
- **Aligned baselines.** Text in the same row aligns vertically. Headings align with the icons next to them. Card content has consistent padding all around.

Rhythm is invisible when present and obvious when absent. It's what separates "looks fine" from "feels right."

### 5. Inline-first composition

This is the principle most often violated by AI builds. Cards are not the default layout primitive. They are an *exception* used when content needs emphasis, separation, repetition, or framing.

Default to inline content in the page body:
- A page title sits as text, not inside a card with a title bar
- A primary number sits as a large display element on the page, not inside a "metric card"
- A list of items can be a styled list with rows, not a grid of card tiles
- A form is field rows on the page, not a "Form" card

Use cards only when:
- **Emphasis** — this one element is the focal point and needs visual lift from its surroundings
- **Separation** — multiple unrelated content blocks need to be visually distinct
- **Repetition** — a list of equivalent things benefits from each one being self-contained
- **Framing** — a detail panel, modal, or overlay frames content for focused attention

A page that stacks one card after another for no reason — KPI card, today card, list card, secondary list card — is the dashboard reflex, and it's almost always wrong. Real apps inline most content and reserve cards for moments that actually need framing.

---

## B. System — how to encode visual language

The principles in Section A describe what the build should feel like. This section describes the mechanics.

### Core mandate: token-first, then archetype, then components

Every build follows this order:

1. **Pick or derive an archetype** based on the app's purpose, customer, and feeling
2. **Declare the complete token set** in `app.css` — colors, typography, radius, borders, elevation, spacing
3. **Build every component as a consumer of those tokens** — no hardcoded hex values, no improvised type sizes, no ad-hoc radii

This single ordering eliminates the most common AI design failures: invented colors, mixed radii, accidental new type sizes, ad-hoc status colors. The constraint produces coherence; the coherence produces taste.

### Picking the archetype

An archetype is a complete preset for the visual language — palette flavor, typography pairing, radius scale, elevation style. All archetypes share the same structural shape; they differ only in values.

- **DOMAIN.md has brand colors** → use brand colors for the palette layer; pick the archetype whose structural feel matches the customer (industrial CPQ → Enterprise; wellness clinic → Wellness; creative agency CRM → Creator). Brand colors override the archetype's palette; everything else (typography, radius, elevation) comes from the archetype.
- **No DOMAIN.md and no clear emotional cue** → use Neutral / Default. Safe choice that works for any app.
- **No DOMAIN.md but a clear cue from the task** → match the archetype to the cue. "Build me a habit tracker" → Wellness. "Dental scheduler" → Editorial-Clinical or Wellness. "Build me an expense tracker" → Finance & Trust.
- **Multiple cues** → pick the most dominant. Don't blend archetypes.

Do not invent a new archetype mid-build.

**For the full archetype catalog and encoded token sets**, read `references/archetypes.md` in full before writing the token block.

### Picking the layout shape

The dashboard layout (sidebar + KPI cards + content cards) is overused and almost always wrong unless the app is genuinely a dashboard tool. Most apps have a *primary product surface* — and that surface should be the focal element, not buried below KPI cards.

Common product surfaces by app type:
- **Calendar/scheduler** → day or week timeline IS the surface. The schedule is not "below" KPIs; it's the page.
- **Writing/notes** → the editor IS the surface
- **Pipeline/board** → the board IS the surface
- **Map/location** → the map IS the surface
- **Reading** → the article IS the surface
- **Chat/messaging** → the conversation IS the surface
- **Tracker/log** → the log entries ARE the surface
- **Form-heavy intake** → the form sequence IS the surface

When the product has a clear primary surface, that surface gets the page. Supporting context (counts, filters, related items) goes in narrow side panels or collapses into the surface itself. KPIs go above only when the user actually monitors them — not as decoration.

For full layout patterns (focal, surface-first, list-detail, form, reading, board, single-column), see `references/components.md`.

---

## C. Patterns — interactive states and microinteractions

### Every interactive element has all four states

**Default.** Resting appearance.
**Hover.** Subtle change signaling interactivity — slight background tint, slight border darken. Never a dramatic visual jump. Cursor changes to pointer.
**Active / pressed.** Slightly more pronounced than hover; signals the click is registering.
**Disabled.** Reduced opacity (60-70%), no hover effect, no cursor change. The user should immediately understand "this is here but currently unavailable."

### Every async surface has all four UI states

**Default.** Content rendered.
**Empty.** Never blank. Title ("No appointments yet"), description ("Book the first one to get started"), action button when applicable.
**Loading.** Skeletons matching the actual content shape, not generic spinners. A row skeleton is a tinted rectangle the size of a row.
**Error.** Constructive, never dead-end. Title ("Couldn't load appointments"), description ("Check your connection and try again"), action ("Retry"). Never a raw error message.

### Microinteractions

- **Hover transitions:** 150-200ms ease-out
- **Focus indicators:** visible focus ring on keyboard nav (2px outline in `--primary` with 2px offset)
- **Optimistic UI:** update immediately, roll back if the action fails
- **Button press feedback:** subtle scale or color shift on press
- **State transitions:** 150ms cross-fade or slide between sections
- **Toast entry:** slide in from bottom-right over 200ms

If a transition is noticeable as a transition, it's too long. Aim for "I didn't notice it but the app felt good."

---

## D. Component recipes

Components consume the active token set. Same recipes across all archetypes; different tokens; different visual results; always coherent.

For exact specs of all 16+ component recipes — Primary/Secondary/Tertiary Buttons, Chips, Status Badges, Rows (default/hover/selected), Cards (when appropriate), Toggles, Form Inputs, Section Headers, Empty States, Toasts, Loading Skeletons, plus the layout pattern catalog — see [`references/components.md`](references/components.md).

Read this reference whenever building any UI component or composing a screen layout.

---

## E. Anti-patterns

The 18+ failures that show up in 90% of one-shot AI builds — including the dashboard reflex, card-heavy compositions, generic SaaS purple, decorative gradients, mixed radii, fifth type sizes, invented status colors, and brand-color overuse.

See [`references/anti-patterns.md`](references/anti-patterns.md). Read at the start of the build to internalize and again before completion as a verification scan.

---

## F. Mechanics

The non-optional mechanics inherited from the deprecated frontend-design skill: template contract, brand theming CSS variable mapping, BrandMark component pattern with onError fallback, light-mode-in-both-places mandate, header right cluster (role switcher + theme toggle + user menu), currency formatting, scope boundaries.

These rules are mandatory. Skipping any of them is a failed build even when tokens and components are perfect.

See [`references/mechanics.md`](references/mechanics.md). Read before writing the token block AND before building the layout shell.

---

## G. Build order

The agent MUST follow this order. Do not start building components before the token block is complete.

1. **Read all four references in full.** Do not skim. archetypes, components, anti-patterns, mechanics.
2. **Pick the archetype.** Match to the task description, DOMAIN.md (if present), and any vision the upstream agent stated. Note the choice in a code comment at the top of `app.css`: `/* design-taste archetype: Wellness & Health */`
3. **Identify the primary product surface.** What IS this app? Calendar timeline? Writing canvas? Board? Pipeline? Map? Reading layout? The answer determines the layout shape — see Section B and `references/components.md`.
4. **Write the complete token block to `app.css`.** All token categories declared as CSS variables under `:root`. No exceptions. No "I'll add elevation later." Use `references/mechanics.md` for the brand theming variable mapping.
5. **Set light mode in BOTH places.** `app.css` AND the JavaScript ThemeProvider default. Failure to do this means the app ships in dark mode regardless of tokens. Most-skipped step.
6. **Build the layout shell using the Template Contract.** Sidebar (if applicable), header, main content area. Use `--surface-stage` for the page background, `--surface-navigation` for the sidebar. Header gets the BrandMark + company name on the left and the right cluster on the right. NO hardcoded colors anywhere — every value comes from a token.
7. **Build the primary product surface.** Whatever the surface is for this app — that's the focal element. Inline it on the page. Do NOT wrap it in a "card" unless the surface itself benefits from card framing (rare).
8. **Build supporting elements.** Side panels, secondary surfaces, navigation rows. Apply the recipes in `references/components.md` exactly. Inline content into the page body before reaching for cards.
9. **Build interactive states.** Every interactive element has hover, active, selected, disabled. Every async surface has loading, error, empty.
10. **Add microinteractions.** Hover transitions, focus indicators, optimistic UI, button press feedback, toast animations.
11. **Anti-pattern scan.** Open `references/anti-patterns.md`. Walk each item. Fix any violations.
12. **Side-by-side check (iterative builds only — not first build).** Compare the new screen to the closest existing peer screen. Match radius, typography, spacing, badge style, button shape. The existing app's visual language overrides this skill's defaults — match the existing.

---

## H. Verification

Before completion, run through this checklist:

1. **Token block complete.** Every token category declared in `app.css`. No hardcoded hex values anywhere except inside the token block.
2. **Archetype consistent.** Every component pulls from the declared tokens. No off-archetype values.
3. **Light mode in both places.** `app.css` AND ThemeProvider default. App ships in light mode.
4. **Brand colors mapped if present in DOMAIN.md.** `accent` → `--primary`; `dark` (lightened) → `--sidebar`; `light` → `--background`. Per `references/mechanics.md`.
5. **BrandMark used everywhere a logo appears.** No bare `<img>` tags.
6. **Primary surface is the focal element.** Not a card buried below KPIs.
7. **Inline-first composition.** Cards used only for emphasis, separation, repetition, or framing — not as the default layout primitive.
8. **Hierarchy clear.** Each screen has one focal point. Supporting elements are visually subordinate.
9. **Restraint visible.** Brand color used in <10% of pixels. No more than one primary action per screen. No drop shadows.
10. **Rhythm consistent.** All spacing on the 4/8 scale. Same hierarchy = same radius. Aligned baselines.
11. **All four states present** for every interactive element (default/hover/active/disabled) and every async surface (default/loading/empty/error).
12. **Anti-pattern scan clean.** All items in `references/anti-patterns.md` checked. No violations.
13. **Header right cluster correct.** Role switcher (prototype phase) + theme toggle + user menu. User menu has placeholder Log out + "Demo mode" hint per mechanics.
14. **Side-by-side check passed (iterative builds).** New screen visually matches existing peer screen.

---

## I. v0.2 scope, what changed since v0.1, and known gaps

### What changed

- **Absorbed mechanics from frontend-design** (now disabled). Template Contract, BrandMark, brand theming variable mapping, light-mode mandate, header right cluster, currency formatting — all live in `references/mechanics.md`. design-taste is now the single source of truth for visual mechanics + taste.
- **Added inline-first composition principle (Section A.5).** Cards are an exception, not the default. Replaces the v0.1 assumption that cards are the primary layout primitive.
- **Added "identify the primary product surface" step in build order.** This was the gap that produced the generic-dashboard dental scheduler in the April 2026 validation. Now an explicit step before token-write.
- **Added reference apps and optional typography pairings to archetypes** (in `references/archetypes.md`). Each archetype names 2-3 real apps as North Stars and may declare an optional display font pairing.
- **Added Editorial-Clinical archetype** for medical/professional/document-heavy contexts (Marigold-style — Fraunces + Inter, soft mint, generous whitespace, broadsheet feel).
- **Strengthened the read directive.** All four references must be read in full before writing tokens. The April 2026 validation showed that partial reads (`head -150` on archetypes.md) lose critical information.
- **Removed VISION.md hooks.** The first task agent (mitb-initial-agent) runs the vision pass once as an inline planning note, not as a separate file. design-taste consumes whatever vision exists in the agent's context; subsequent builds match the existing codebase.
- **Removed Generic Layout Fallback references.** design-taste's archetype model replaces it.

### Encoded in v0.2

- 3 archetypes (Neutral / Default + Wellness & Health + Editorial-Clinical)
- 16+ component recipes
- 18+ anti-patterns including new card-overuse and generic-dashboard items
- Layout pattern catalog (focal, surface-first, list-detail, form, reading, board, single-column)
- 4 interactive states + 4 async UI states + 6 microinteraction guidelines
- Mechanics: Template Contract, BrandMark, brand theming, light-mode mandate, header right cluster, currency

### Pending

- 7 additional archetypes (Productivity & Focus, Finance & Trust, Creator & Social, Lifestyle & Travel, Education & Knowledge, Utility & Tools, Reading & Content, Enterprise & Professional)
- Edge components (date picker, multi-step wizards, complex modals, data tables, calendars, kanban boards)
- Animation specifics for transitions beyond microinteractions
- Detailed responsive breakpoint behavior
- Dark mode (deferred — get light mode reliable first)

### Validation plan

1. Re-run the dental scheduler build with v0.2 (Editorial-Clinical archetype). Compare to Marigold reference.
2. Run an existing-vertical build (e.g., HB Material Handling CPQ) using the Default archetype with brand colors from DOMAIN.md overriding the palette. Compare against current quality.
3. Identify gaps. Update to v0.3.

---

## How this fits the skill stack

| Skill | Reads when | What it provides |
|---|---|---|
| **design-taste** | **Always** | **Visual quality + mechanics — foundations, archetypes, recipes, anti-patterns, template contract, brand theming, BrandMark, light-mode mandate** |
| `domain-context` | Always | Business terminology, entities, statuses, stakeholders |
| `cpq-builder` | When task is CPQ-shaped | CPQ-specific section structure, quote document, RBAC patterns |
| `trades-builder` | When task is trades-shaped | Trades-specific section structure, job summary, payment flow |
| `crm-builder` | When task is CRM-shaped | Entity model, pipeline view, list/detail patterns |
| `erp-builder` | When task is ERP-shaped | Inventory model, purchase order flow |

design-taste and domain-context are read on every build. Verticals are additive when one fits. For builds with no vertical, design-taste + domain-context are sufficient — there is no Generic Layout Fallback; the chosen archetype IS the design system.
