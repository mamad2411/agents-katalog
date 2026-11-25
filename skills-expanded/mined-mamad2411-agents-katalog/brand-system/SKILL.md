---
name: brand-system
description: "Builds brand identity systems as two artifacts — BRAND.md (story, voice, positioning, archetype) and DESIGN.md (AI-readable design system with palettes, tokens, components, motion). Not for writing marketing copy (use content-create) or mapping user flows (use user-flow). For campaign planning, see imc-plan. For audience research, see icp-research."
argument-hint: "[product or brand to design]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "6.0.0"
  budget: deep
  estimated-cost: "$2-5"
promptSignals:
  phrases:
    - "brand identity"
    - "brand voice"
    - "design system"
    - "brand guidelines"
    - "visual identity"
    - "brand book"
  allOf:
    - [brand, identity]
    - [design, system]
  anyOf:
    - "brand"
    - "voice"
    - "typography"
    - "color system"
    - "design tokens"
    - "logo"
  noneOf:
    - "landing page audit"
    - "conversion rate"
  minScore: 6
routing:
  intent-tags:
    - brand-identity
    - design-tokens
    - visual-system
    - color-system
    - typography-system
    - brand-voice
  position: pipeline
  produces:
    - brand/BRAND.md
    - brand/DESIGN.md  # Route B (full) only. Quick Brand (Route A) produces BRAND.md only.
  consumes:
    - product-context.md
  requires: []
  defers-to:
    - skill: user-flow
      when: "need screen mapping, not brand identity"
    - skill: copywriting
      when: "need copy craft, not brand voice definition"
  parallel-with:
    - imc-plan
  interactive: false
  estimated-complexity: heavy
---

## ⚠ v6 Breaking Change

Output moved from `.agents/design/brand-system.md` → `brand/BRAND.md` + `brand/DESIGN.md`.

**Downstream consumers to update:**
- `product-skills/user-flow` — consumes `design/brand-system.md` → update to `brand/DESIGN.md`
- `product-skills/technical-writer` — consumes `.agents/design/brand-system.md` → update to `brand/BRAND.md` (voice/terminology) and `brand/DESIGN.md` (tokens)
- Root `README.md` artifact table → update path

**Duration scale change:** Timings shifted from (100, 200, 300, 500)ms to (75, 150, 250, 400, 600)ms with a new `--duration-emphasis` tier. Brands built on v5 will have different motion timing.

**Quick Brand (Route A)** produces `brand/BRAND.md` only. DESIGN.md requires the full Route B pipeline.

---

# Brand Identity & Design System — Orchestrator

*Design — Step 1 of 2. Coordinates specialized agents to transform product artifacts into a complete brand narrative and AI-readable design system.*

**Core Question:** "Does every visual decision trace back to who we are?"

## Critical Gates — Read First

- **Do NOT choose colors or fonts before strategy.** Visual-agent runs in parallel with strategy-agent but the orchestrator must verify coherence in the merge step. Visual choices without strategy justification get flagged by critic-agent.
- **Do NOT dispatch Layer 2 before Layer 1 completes.** Token-architect-agent needs visual-agent output. Component-token-agent needs token-architect-agent output. The chain is strict.
- **Do NOT skip the critic's cross-element coherence check.** Radius must map to archetype. Typography must match personality. Color must align with brand emotion. The critic checks the matrix that no individual agent can see.
- **Stale upstream data (>30 days) produces generic archetypes.** Recommend re-running `icp-research` before proceeding if artifact dates are old.
- **BRAND.md is prose, DESIGN.md is specification.** BRAND.md reads like a brand book — narrative, story, voice. DESIGN.md reads like an API reference — tables, formulas, exact values. Never mix the registers.

## Inputs Required
- Product description or PRD (what the product does, who it serves)
- Target audience profile (demographics, psychographics, context of use)
- Competitive context (who else serves this audience, how they're positioned)

## Output — Two Files

The skill produces two complementary files, each serving a different audience:

### `BRAND.md` — Brand Narrative & Voice
**Audience:** Founders, marketers, copywriters, designers making brand decisions.
**Register:** Prose. Reads like a brand book — narrative, story, voice examples.
**Contains:** Origin story, naming, purpose/mission/vision, values, positioning, archetype, personality traits, emotional journey, voice chart, tone spectrum, messaging architecture, brand mark, product-specific brand sections, digital touchpoints.

### `DESIGN.md` — AI-Readable Design System
**Audience:** AI coding agents, frontend engineers, design system consumers.
**Register:** Specification. Tables, formulas, exact values. An AI agent should be able to read this file and produce on-brand UI without any other context.
**Contains:** Visual atmosphere, complete color palettes per theme, typography rules, component stylings, layout principles, shadows & elevation, iconography, imagery direction, motion & animation, accessibility, do's and don'ts.

**Output location:** `brand/BRAND.md` and `brand/DESIGN.md` in the project directory. Additionally, visual brand guideline artboards if Paper MCP is available.

### Agent-to-File Routing

| Agent Output | → BRAND.md | → DESIGN.md |
|-------------|-----------|------------|
| Strategy Agent | Origin story, naming, purpose/mission/vision, values, positioning, competitive landscape, product-specific sections, digital touchpoints | — |
| Personality Agent | Archetype, personality traits, emotional journey map | — |
| Voice Agent | Voice attributes (Do/Don't), tone range (3 contexts), tagline | — |
| Visual Agent | Brand mark / logo system | Visual atmosphere, color system, per-theme palettes, typography, imagery, iconography, surface & material language, shadow system, z-index, do's and don'ts |
| Token Architect Agent | — | Primitive scales, semantic token map, spacing, radius |
| Component Token Agent | — | Component specs, product-specific components, motion tokens, named animations |
| Accessibility Agent | — | Contrast audit, touch targets, focus states, dark mode, color independence, motion safety |

## Quality Gate
Before delivering, the **critic agent** verifies both files:

**BRAND.md checks:**
- [ ] Origin story and naming have cultural/etymological depth — not just "we named it X"
- [ ] Values have real tradeoffs (not generic "innovation, quality, integrity")
- [ ] Voice attributes have Do/Don't examples using real brand contexts (not hypothetical)
- [ ] Tone range covers 3 key contexts with clear shift across the range
- [ ] Tagline scored with V/F/U (minimum 6/9), passes competitor swap test
- [ ] No copywriting scope creep (no boilerplate, pillars, elevator pitch, tagline variants)
- [ ] Emotional journey is touchpoint-level with design/interaction triggers (not copy triggers)
- [ ] Brand mark described with enough detail to commission or generate
- [ ] Digital touchpoints scoped to visual expression (not verbal)
- [ ] Prose quality: reads like a brand book, not fill-in-the-blank templates

**DESIGN.md checks:**
- [ ] AI-readable header summarizes key decisions (archetype, metaphor, fonts, primary color)
- [ ] Complete color palette tables for every theme (not just primary + neutrals)
- [ ] All semantic tokens have values for every theme
- [ ] Every token pair meets WCAG AA contrast (4.5:1 normal text, 3:1 large/UI)
- [ ] Background/foreground convention used consistently (`bg-primary text-primary-foreground`)
- [ ] One global `--radius` value — archetype-justified
- [ ] Surface/material language documented with CSS formulas
- [ ] Shadow system with multiple elevation levels
- [ ] Named animations with physics values (spring stiffness, damping, mass)
- [ ] Do's and Don'ts section with concrete rules

**Cross-file coherence:**
- [ ] Cross-element coherence: radius maps to archetype, type personality matches archetype, color emotion aligns with brand personality, imagery direction reflects the archetype's visual world
- [ ] Voice tone in BRAND.md matches the visual atmosphere described in DESIGN.md
- [ ] AI slop check: run `references/ai-slop-detection.md` — 0-1 clean, 2-3 review, 4+ regeneration

**Reference quality bar:** Compare output against the annotated quality guides in `references/example-brand.md` and `references/example-design.md`. Every section should match the "good" pattern and avoid the "bad" pattern described in those guides. Use the overall quality tests in example-design.md (copy-paste test, blind build test, competitor swap test, implementation gap test) as final validation.

## Chain Position
Previous: `icp-research` (product context) | Next: `imc-plan`, `copywriting`, `content-create`

**Re-run triggers:** After major product pivots, when entering new markets, after significant audience shifts, or annually for brand refresh.

**Related skills (non-chain):** `icp-research` (audience data for brand strategy), `content-create` (consumes voice guidelines), `humanize` (uses voice adjectives)

### Skill Deference
- **Need audience research first?** Run `icp-research` (from marketing-skills) — brand strategy without audience research produces generic archetypes.
- **Need user flows after brand?** Run `user-flow` next — it consumes design tokens and component context.
- **Need marketing copy?** Run `content-create` or `copywriting` — they consume voice guidelines.

---

## Agent Manifest

| Agent | Layer | File | Routes to | Focus |
|-------|-------|------|-----------|-------|
| Strategy Agent | 1 (parallel) | `agents/strategy-agent.md` | BRAND.md | Purpose, mission, vision, values, positioning, competitive landscape, **brand narrative (origin/naming), product-specific sections, digital touchpoints** |
| Personality Agent | 1 (parallel) | `agents/personality-agent.md` | BRAND.md | Jungian archetype (70/30 blend), personality traits, **touchpoint-level emotional journey** |
| Voice Agent | 1 (parallel) | `agents/voice-agent.md` | BRAND.md | Voice attributes (Do/Don't), tone range (3 key contexts), primary tagline with V/F/U score |
| Visual Agent | 1 (parallel) | `agents/visual-agent.md` | Both | Logo → BRAND.md. **Visual atmosphere, color system, per-theme palettes, typography, imagery, surface & material language, shadow system, z-index, do's and don'ts** → DESIGN.md |
| Token Architect Agent | 2 (sequential) | `agents/token-architect-agent.md` | DESIGN.md | 3-layer W3C token system, semantic map, radius-to-archetype, **per-theme token tables** |
| Component Token Agent | 2 (sequential) | `agents/component-token-agent.md` | DESIGN.md | Button 6 variants, input specs, card specs, **product-specific components, named animations with physics values**, motion tokens |
| Accessibility Agent | 2 (sequential) | `agents/accessibility-agent.md` | DESIGN.md | WCAG AA contrast, touch targets, dark mode audit, focus states |
| Critic Agent | 2 (final) | `agents/critic-agent.md` | Both | Cross-element coherence, **BRAND.md narrative quality, DESIGN.md AI-readability**, PASS/FAIL |

### Shared References (read by multiple agents)
- `references/brand-archetypes.md` — 12 Jungian archetypes with visual/verbal mappings
- `references/brand-voice.md` — Voice frameworks, tone dimensions, messaging architecture
- `references/visual-identity.md` — Logo systems, imagery, iconography, graphic elements
- `references/color-emotion.md` — Color psychology, OKLCH values, audience palettes
- `references/typography-psychology.md` — Font personality mappings and pairing rules
- `references/token-architecture.md` — Three-layer token system, semantic token map
- `references/token-templates.md` — Primitive scales, radius-archetype mapping, mapping example
- `references/component-tokens.md` — Component token map, button/input/card specs, motion tokens
- `references/component-patterns.md` — Extended UI component patterns with token consumption maps
- `references/implementation-rules.md` — Accessibility baseline, dark mode rules, brand applications
- `references/artboard-generation.md` — Paper MCP artboard specs and workflow
- `references/paper-artboard-templates.md` — Paper MCP HTML/CSS templates
- `references/ai-slop-detection.md` — AI-generated design anti-patterns checklist

### Quality-Bar Reference Examples
- `references/example-brand.md` — Annotated quality guide: good vs bad excerpts for every BRAND.md section
- `references/example-design.md` — Annotated quality guide: good vs bad excerpts for every DESIGN.md section

---

## Routing Logic

### Mode Selection

Ask: *"Full brand system or quick brand for MVP?"*

### Route A: Quick Brand (MVP)
**When:** MVP, early-stage, need to ship fast with basic brand foundations.

```
1. Pre-dispatch: Gather context (Step 0)
2. LAYER 1 — Dispatch IN PARALLEL:
   - strategy-agent (purpose, values, positioning)
   - visual-agent (color + typography only — logo deferred)
3. Dispatch: critic-agent (coherence check — strategy-to-visual only)
4. If FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
5. Deliver Quick Brand artifact
```

**Quick Brand scope:** Purpose/mission/vision, core values, positioning, primary color + neutrals, display + body font, basic type hierarchy. Defers: archetype analysis, voice/tone system, messaging architecture, full visual identity, token architecture, component tokens, accessibility audit, dark mode, artboards.

**Quick Brand output includes a note:** "Run full brand-system when ready to build the design system."

### Route B: Full Brand System
**When:** Established product, full rebrand, comprehensive guidelines needed.

```
1. Pre-dispatch: Gather context (Step 0)
2. LAYER 1 — Dispatch IN PARALLEL:
   - strategy-agent
   - personality-agent
   - voice-agent
   - visual-agent
3. MERGE: Assemble Layer 1 outputs into brand identity sections
4. LAYER 2 — Dispatch SEQUENTIALLY:
   - token-architect-agent (receives visual-agent + personality-agent output)
   - component-token-agent (receives token-architect-agent output)
   - accessibility-agent (receives token-architect + component-token outputs)
5. Dispatch: critic-agent (receives complete brand system)
6. If FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
7. Artboard generation (Step 9 — if Paper MCP available)
8. Deliver artifact
```

---

## Step 0: Pre-Dispatch Context Gathering

### Product Context Check
Check for `.agents/product-context.md` and `.agents/mkt/icp-research.md`. If `date` fields are older than 30 days, **warn the user** and recommend re-running upstream skills. Tip: `/navigate status` (from meta-skills) gives a single-pass freshness report across all upstream artifacts.

### Required Inputs — Interview If Missing
- Product description or PRD
- Target audience profile
- Competitive context

### Strongly Recommended
- Existing brand assets (logos, colors, fonts, past guidelines)
- Founder/team values and origin story
- Key differentiators

### Helpful
- Admired brands (aspirational and anti-aspirational)
- Market positioning intent (premium, accessible, disruptive, trusted)

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `.agents/product-context.md` | icp-research (from `hungv47/marketing-skills`) | Product positioning, audience, and voice adjectives — grounds brand strategy in audience research |
| `.agents/mkt/icp-research.md` | icp-research (from `hungv47/marketing-skills`) | Audience personas, pain profiles, and VoC quotes — brand strategy without audience research produces generic archetypes |

**Strongly recommended:** Run `icp-research` (from marketing-skills) first if audience research hasn't been done.

### Context to Pass to All Agents
1. **Product:** description, audience, competitive landscape
2. **Existing assets:** any logos, colors, fonts, guidelines to preserve or evolve
3. **Positioning intent:** premium, accessible, disruptive, trusted
4. **Upstream artifacts:** excerpts from product-context.md and icp-research.md if available

Missing product details are not guessable — interview for them.

---

## Dispatch Protocol

### How to spawn a sub-agent

1. **Read** the agent instruction file — include its FULL content in the Agent prompt
2. **Append** the context (product, audience, competitive landscape, existing assets) after the instructions
3. **Resolve file paths to absolute**: replace relative paths with absolute paths rooted at this skill's directory
4. **Pass upstream artifacts by content**: the orchestrator reads `.agents/` files FIRST, then includes relevant excerpts in context. Sub-agents should NOT read artifact files directly.
5. If **feedback** exists (from critic FAIL), append with header "## Critic Feedback — Address Every Point"

### Conventions

- **Source citation:** When stating facts about brand psychology, color theory, or archetype effectiveness, cite the source. If from a web search, include the URL. If a fact cannot be attributed, flag it as `[UNVERIFIED]`.
- **Context loaded:** When producing the artifact, include which upstream artifacts were read and their versions/dates in the artifact body. This creates an audit trail for downstream skills.

### Single-agent fallback

If multi-agent dispatch is unavailable, execute each agent's instructions sequentially in-context:
- Layer 1: define strategy, select archetype, write voice chart, design visual identity
- Layer 2: build token architecture, map component tokens, audit accessibility
- Final: evaluate with critic rubric, check cross-element coherence

---

## Layer 1: Parallel Foundation

Spawn **IN PARALLEL**:

| Agent | Instruction File | Pass These Inputs | Reference Files |
|-------|-----------------|-------------------|-----------------|
| Strategy Agent | `agents/strategy-agent.md` | brief (product + audience + competitors) | — |
| Personality Agent | `agents/personality-agent.md` | brief (product + audience) | `references/brand-archetypes.md` |
| Voice Agent | `agents/voice-agent.md` | brief (product + audience) | `references/brand-voice.md` |
| Visual Agent | `agents/visual-agent.md` | brief (product + audience + existing assets) | `references/color-emotion.md`, `references/typography-psychology.md`, `references/visual-identity.md` |

Wait for all to complete. Their outputs feed the merge step and Layer 2.

---

## Merge Step — Two-File Assembly

Before assembling, read `references/artifact-templates.md` for the complete section structure, field specifications, and ordering for both files.

After Layer 1 completes, assemble outputs into **two separate files** simultaneously:

### BRAND.md Assembly (from Layer 1)

| Section | Owner Agent | Notes |
|---------|-----------|-------|
| The Origin Story | Strategy Agent | Narrative prose, not bullet points |
| The Name | Strategy Agent | Etymology, meaning, cultural context |
| Purpose, Mission & Vision | Strategy Agent | — |
| Core Values | Strategy Agent | "X over Y" format with real tradeoffs |
| Brand Positioning | Strategy Agent | Positioning statement, value prop, what we are/aren't |
| Brand Archetype | Personality Agent | 70/30 blend with "in action" section |
| Personality Traits | Personality Agent | "Trait, but not extreme" table |
| Emotional Journey Map | Personality Agent | Touchpoint-by-touchpoint, not before/during/after |
| Brand Voice DNA | Voice Agent | Voice attributes (Do/Don't) + tone range (3 contexts) + tagline |
| The Brand Mark | Visual Agent (logo section) | Visual description, variations, color combos, rules |
| [Product-Specific Sections] | Strategy Agent | Differentiators, pricing as brand, parent brand relationship |
| Digital Touchpoints | Strategy Agent | How brand expresses at each surface |

### DESIGN.md Assembly (starts from Layer 1, completed by Layer 2)

| Section | Owner Agent | Notes |
|---------|-----------|-------|
| AI-Readable Header | Orchestrator synthesis | Archetype, visual metaphor, fonts, primary color |
| 1. Visual Theme & Atmosphere | Visual Agent | Mood, density, metaphor — prose introduction |
| 2. Color Palette & Roles | Visual Agent + Token Architect | Primary colors, semantic, per-theme palettes, neutrals, distribution rules |
| 3. Typography Rules | Visual Agent | Font stack, type scale, typography rules |
| 4. Component Stylings | Component Token Agent | Product-specific core components + standard components |
| 5. Layout Principles | Token Architect Agent | Spacing scale, border radius |
| 6. Shadows & Elevation | Visual Agent + Component Token | Shadow scale, z-index scale |
| 7. Iconography | Visual Agent | System icons, product-specific icons |
| 8. Imagery & Visual Direction | Visual Agent | Photography, brand devices |
| 9. Motion & Animation | Component Token Agent | Principles, duration scale, easing, named animations, motion safety |
| 10. Accessibility | Accessibility Agent | Contrast, focus, touch targets, color independence |
| 11. Do's and Don'ts | Visual Agent | Concrete rules synthesized from all decisions |

**Coherence check before Layer 2:** Verify that the archetype selected by personality-agent aligns with the visual choices made by visual-agent. If they contradict (e.g., Caregiver archetype with sharp/aggressive typography), resolve before dispatching Layer 2.

---

## Layer 2: Sequential Chain

Dispatch **ONE AT A TIME, IN ORDER**:

| Step | Agent | Instruction File | Receives |
|------|-------|-----------------|----------|
| 1 | Token Architect Agent | `agents/token-architect-agent.md` | Visual-agent output (colors, fonts, **complete theme palettes**) + personality-agent output (archetype for radius) |
| 2 | Component Token Agent | `agents/component-token-agent.md` | Token-architect-agent output (semantic token map) |
| 3 | Accessibility Agent | `agents/accessibility-agent.md` | Token-architect + component-token outputs |
| 4 | Critic Agent | `agents/critic-agent.md` | Complete assembled brand system (both BRAND.md and DESIGN.md) |

**Palette ownership rule:** Visual-agent is authoritative for color choices and theme palette values. Token-architect-agent systematizes those values into the three-layer architecture (primitive → semantic → component) and adds any missing infrastructure tokens (`--popover`, `--popover-foreground`). If values conflict, visual-agent wins.

---

## Critic Gate

- **PASS:** Deliver the artifact. Proceed to artboard generation (Step 9) if Paper MCP available.
- **FAIL:** Re-dispatch named agent(s) with critic feedback. Max 2 rewrite cycles. After 2 failures, deliver with critic annotations and flag to user.

---

## Step 9: Visual Artboard Generation (Paper MCP)

Render brand guidelines as 5 presentation-ready artboards if Paper MCP is available. Reference `references/artboard-generation.md` for complete specs, workflow, and prerequisites.

After generating artboards, run the AI slop detection checklist (`references/ai-slop-detection.md`). Artboards are the highest-risk output for AI default patterns.

Artboards: Color Palette | Typography System | Spacing & Tokens | UI Style Principles | Logo System

Skip this step if Paper MCP tools are unavailable.

---

## Artifact Templates

Save to `brand/BRAND.md` and `brand/DESIGN.md` in the project directory. Create the `brand/` directory if it doesn't exist. Also create `brand/logo/`, `brand/font/`, and `brand/inspiration/` subdirectories with `.gitkeep` files for future assets.

On re-run: rename existing artifacts to `BRAND.v[N].md` / `DESIGN.v[N].md` and create new with incremented version.

**Full templates:** See [references/artifact-templates.md](references/artifact-templates.md) for the complete BRAND.md and DESIGN.md templates with all sections and field specifications.

**Template summary:**

**BRAND.md** (11 sections): Origin Story → Name → Purpose/Mission/Vision → Core Values ("X over Y" format) → Brand Positioning → Brand Archetype (Primary 70% + Secondary 30%) → Personality Traits → Emotional Journey Map → Brand Voice DNA (attributes + tone range + tagline with V/F/U scoring) → Brand Mark (logo system) → Digital Touchpoints.

**DESIGN.md** (11 sections): Visual Theme & Atmosphere → Color Palette & Roles (OKLCH, themes, neutral scale, 60/30/10) → Typography Rules (font stack, type scale) → Component Stylings (core component + cards + buttons + inputs) → Layout Principles (spacing, radius) → Shadows & Elevation (z-index) → Iconography → Imagery & Visual Direction → Motion & Animation (duration, easing, spring physics) → Accessibility (contrast, focus, touch targets) → Do's and Don'ts.

**Quality-bar examples:** [references/example-brand.md](references/example-brand.md) and [references/example-design.md](references/example-design.md) show the complete output at the expected quality level.

---

## Worked Example (Condensed) — Route B: Full Brand System

**Input**: FinLit — a personal finance app for young professionals (22-30), positioned against intimidating banking apps.

### Step 0: Pre-Dispatch
Product: personal finance app. Audience: young professionals 22-30. Competitors: traditional banking apps (Mint, bank mobile apps).

### Layer 1: Parallel Foundation
All 4 agents dispatched in parallel:
- **Strategy agent** returns: Origin story ("born from a founder's shame spiral at 24"), name ("FinLit — financial literacy, shortened to feel casual"), purpose "make finance empowering, not shameful." Positioning: "the only finance app that feels like a supportive friend." Values: transparency over comfort, simplicity over completeness, progress over perfection. Digital touchpoints mapped across 6 surfaces. Product-specific: "Streak System as brand expression" section.
- **Personality agent** returns: Caregiver (70%) + Explorer (30%). Traits: encouraging but not patronizing, clear but not dumbed-down, warm but not saccharine. Emotional journey: 8-touchpoint map (first encounter → app store → onboarding → first budget → daily check → missed goal → annual review → telling a friend).
- **Voice agent** returns: Voice DNA with 3 attributes (straight-talking, encouraging, honest) with real-context Do/Don't examples. Tone range across 3 contexts (marketing: inviting + confident, product UI: minimal + clear, errors: calm + honest). Tagline: "Money, minus the shame." V:3 F:2 U:3 = 8/9.
- **Visual agent** returns: **For BRAND.md:** Logo system (4 variations, color combos, rules). **For DESIGN.md:** Visual atmosphere ("warm kitchen table, not bank lobby"). Primary warm teal `oklch(0.65 0.15 180)` / `#2cbaa0`. Complete light + dark theme palettes (18 tokens each). Neutral base: Stone. Display: Plus Jakarta Sans. Body: Inter. Shadow system (5 levels). Surface material: soft matte (no glass). Imagery: real people, natural light, warm tones. Do's and Don'ts (12 items each).

### Merge — Two Files
**BRAND.md assembled** from strategy (origin/name/purpose/values/positioning/touchpoints) + personality (archetype/traits/journey) + voice (voice DNA/tone range/tagline) + visual (logo only).
**DESIGN.md started** from visual (atmosphere/colors/typography/shadows/imagery/do's-don'ts). AI-readable header generated.

Coherence check: Caregiver archetype aligns with warm teal (trust + growth), humanist-leaning typography (approachable), 0.5rem radius (soft). PASS — proceed to Layer 2.

### Layer 2: Sequential Chain
All outputs go to DESIGN.md:
- **Token architect** returns: Stone 50-950 neutral scale, teal 50-950 primary scale, `--radius: 0.5rem`, 19 semantic tokens with light + dark values. Spacing scale.
- **Component token** returns: 6 button variants mapped to semantic tokens, input specs with blur validation, card specs. Product-specific: "Budget Card" component with progress ring. Named animations: `progress-fill` (spring, stiffness 180), `goal-celebrate` (confetti, 600ms). Motion tokens (75-500ms).
- **Accessibility** returns: All token pairs pass 4.5:1. Dark mode surface hierarchy (stone.950 → stone.900 → stone.800). Primary shifts to teal.400 in dark mode. Touch targets ≥44px.
- **Critic** returns: PASS on both files. BRAND.md narrative quality strong, emotional journey touchpoint-level. DESIGN.md AI-readable, all themes complete. Cross-element coherence verified. AI slop score: 1 item (clean).

### Deliver
`brand/BRAND.md` and `brand/DESIGN.md` saved.

---

## Worked Example (Condensed) — Route A: Quick Brand

**Input**: TaskFlow — a new project management tool, pre-MVP, needs basic brand to start building.

### Step 0: Pre-Dispatch
Product: project management tool. Audience: small team leads. Quick Brand selected.

### Layer 1: Parallel (reduced)
- **Strategy agent** returns: Purpose, values (clarity over complexity, speed over ceremony), positioning. Origin story deferred.
- **Visual agent** returns: Primary blue `oklch(0.623 0.214 259)` / `#3b82f6`. Neutral: Slate. Display: Inter. Body: Inter.

### Critic (reduced)
Checks strategy-to-visual coherence only. PASS.

### Deliver
Quick Brand artifact saved as single `brand/BRAND.md` with note: "Run full brand-system when ready to produce DESIGN.md."

**Quick Brand produces BRAND.md only.** DESIGN.md requires the full Route B pipeline (token architect, component tokens, accessibility audit).

---

## Anti-Patterns

**Aesthetics without strategy** — Picking colors or fonts because they "look nice" without tracing back to archetype and positioning. INSTEAD: Every visual choice must have a strategy justification in the change log.

**Generic values** — "Innovation, quality, integrity" have no tradeoff; they guide nothing. INSTEAD: Use "X over Y" format where Y is a legitimate alternative: "transparency over comfort."

**Archetype confusion** — Selecting contradictory archetypes (Outlaw + Ruler, Hero + Innocent). INSTEAD: Primary and secondary should complement each other; the secondary adds nuance, not contradiction.

**Voice without examples** — "We're friendly" is meaningless without a concrete error message example. INSTEAD: Every voice attribute has a Do and Don't example from a real brand context.

**Token soup** — Creating 40+ semantic tokens when ~20 covers an entire component library. INSTEAD: Keep the semantic layer tight. If you're inventing `--subtle-muted-foreground-alt`, the system is too granular.

**Skipping semantic layer** — Components referencing primitives (`oklch(0.546...)`) instead of semantic tokens (`var(--primary)`). INSTEAD: Always reference semantic tokens. The three-layer chain is Primitive -> Semantic -> Component.

**Mismatched bg/fg pairs** — `bg-primary text-primary` is wrong; use `bg-primary text-primary-foreground`. INSTEAD: Every semantic color role is a pair. Base = background. `-foreground` = text on that surface.

**Dark mode as inversion** — Simply swapping black/white produces unusable surfaces. INSTEAD: Deliberate surface hierarchy (background -> card -> popover), reduced saturation, shifted primary lightness.

**Dispatching all agents for Quick Brand** — Route A exists for MVPs. INSTEAD: Quick Brand uses only strategy + visual + critic. No archetype analysis, no tokens, no components.

---

## Agent Files

### Sub-Agent Instructions (agents/)
- [agents/strategy-agent.md](agents/strategy-agent.md) — Purpose, mission, vision, values, positioning
- [agents/personality-agent.md](agents/personality-agent.md) — Jungian archetype blend, personality traits, emotional journey
- [agents/voice-agent.md](agents/voice-agent.md) — Voice chart, tone spectrum, messaging architecture
- [agents/visual-agent.md](agents/visual-agent.md) — Logo, color system, typography, imagery
- [agents/token-architect-agent.md](agents/token-architect-agent.md) — 3-layer W3C token system, semantic map
- [agents/component-token-agent.md](agents/component-token-agent.md) — Button variants, input/card specs, motion tokens
- [agents/accessibility-agent.md](agents/accessibility-agent.md) — WCAG AA, dark mode, touch targets, focus states
- [agents/critic-agent.md](agents/critic-agent.md) — Cross-element coherence, PASS/FAIL

### Shared References (references/)
- [references/brand-archetypes.md](references/brand-archetypes.md) — 12 Jungian archetypes with visual and verbal mappings
- [references/brand-voice.md](references/brand-voice.md) — Voice frameworks, tone dimensions, messaging architecture
- [references/visual-identity.md](references/visual-identity.md) — Logo systems, imagery direction, iconography, graphic elements
- [references/token-architecture.md](references/token-architecture.md) — Three-layer token system, semantic token map, neutral presets
- [references/token-templates.md](references/token-templates.md) — Primitive scales, semantic token map, radius-archetype mapping, mapping example
- [references/component-tokens.md](references/component-tokens.md) — Component token map, button/input/card specs, motion tokens
- [references/implementation-rules.md](references/implementation-rules.md) — Accessibility baseline, dark mode rules, brand applications
- [references/artboard-generation.md](references/artboard-generation.md) — Paper MCP artboard specs and workflow
- [references/typography-psychology.md](references/typography-psychology.md) — Font personality mappings and pairing rules
- [references/color-emotion.md](references/color-emotion.md) — Color psychology, OKLCH values, audience palettes
- [references/component-patterns.md](references/component-patterns.md) — Extended UI component patterns with token consumption maps
- [references/paper-artboard-templates.md](references/paper-artboard-templates.md) — Paper MCP HTML/CSS templates
- [references/ai-slop-detection.md](references/ai-slop-detection.md) — AI-generated design anti-patterns checklist
- [references/artifact-templates.md](references/artifact-templates.md) — Complete BRAND.md and DESIGN.md output templates with all sections and field specifications

### Quality-Bar Reference Examples (references/)
- [references/example-brand.md](references/example-brand.md) — Worked example: Conquistador BRAND.md (narrative brand book at quality bar)
- [references/example-design.md](references/example-design.md) — Worked example: Conquistador DESIGN.md (AI-readable design system at quality bar)
