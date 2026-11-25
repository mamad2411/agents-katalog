---
name: lp-brief
description: "Generates a campaign-grade brief for a landing-page redesign — hypothesis, surface rhythm, section-by-section spec, asset slots, copy candidates, hand-off prompts. Internalizes lp-optimization conversion principles as evaluation rubric. Produces `.agents/mkt/lp-brief/[slug]/brief.md` ready to hand to Claude Design, a designer in Figma, or `design-brief` for per-asset spec. Not for auditing an existing page (use lp-optimization first — its output feeds this skill). Not for non-conversion pages like blogs or docs hubs (those use different rubrics). Not for spec'ing a single visual asset in isolation (use design-brief)."
argument-hint: "[page route or campaign name, e.g. '/pricing' or 'q3-launch-lp']"
allowed-tools: Read Edit Write Grep Glob Bash WebSearch WebFetch
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
  budget: deep
  estimated-cost: "$2-4"
promptSignals:
  phrases:
    - "page brief"
    - "landing page brief"
    - "redesign brief"
    - "lp brief"
    - "campaign brief"
    - "redesign /[a-z]+"
  allOf:
    - [page, brief]
    - [landing, redesign]
    - [draft, brief]
  anyOf:
    - "redesign"
    - "page-brief"
    - "lp-brief"
    - "hero section"
    - "page architecture"
    - "section spec"
  noneOf:
    - "blog post"
    - "docs page"
    - "single asset"
    - "audit"
    - "cro audit"
  minScore: 6
routing:
  intent-tags:
    - landing-page-brief
    - page-redesign-brief
    - campaign-brief
    - conversion-brief
  position: pipeline
  produces:
    - mkt/lp-brief/[slug]/brief.md
  consumes:
    - brand/BRAND.md
    - brand/DESIGN.md
    - mkt/lp-optimization.md
    - research/icp-research.md
    - research/product-context.md
    - mkt/campaign-plan.md
  requires:
    - brand/BRAND.md
    - brand/DESIGN.md
  defers-to:
    - skill: lp-optimization
      when: "page exists and the task is diagnosis, not redesign"
    - skill: design-brief
      when: "spec'ing an individual asset slot from this brief in detail (per-asset graphic-design brief)"
    - skill: brand-system
      when: "no brand identity defined yet"
    - skill: copywriting
      when: "need craft-quality headline variation work in isolation"
  parallel-with: []
  interactive: true
  estimated-complexity: heavy
---

# Landing Page Brief — Orchestrator

*Communication — Step between strategy and design. Coordinates audit anchoring, hypothesis generation, architecture, per-section specification, asset slotting, and hand-off prompt composition into a single approved brief.*

**Core Question:** "Could a designer (or Claude Design) build the right page from this brief without a single follow-up question?"

## Critical Gates — Read First

- **Do NOT generate a brief without brand artifacts.** Missing `brand/BRAND.md` or `brand/DESIGN.md` → return `NEEDS_CONTEXT`. Brief depends on tokens, voice rules, sacred elements.
- **Do NOT skip the conversion rubric.** Every section spec is gated by lp-optimization's craft rules (4-U headline, message match, CTA psychology, social proof placement, objection handling, form-field discipline). Brand-good but conversion-bad = failure.
- **Do NOT propose changing sacred elements.** Logo geometry, primary palette anchor, tagline wording, signature treatments are "do not touch" rails, not options.
- **Do NOT exceed the brief length envelope.** Useful brief is 250–500 lines. <250 = insufficient depth (designer asks follow-ups). >500 = bloat (designer skims, misses spec). Critic enforces.
- **Do NOT inline the full skill chain.** If project has a shared chain doc (e.g., `growth/page-redesigns/_prompts.md`), reference by section header; add page-specific overrides only.
- **Do NOT inject placeholder testimonials, fake logos, or pretend numbers.** If a proof asset isn't real, spec it ("Customer logo grid, 6 cells × 60px") and note "delete cell if not real" — never fabricate.

## Philosophy

Operates between strategy and design. By invocation, WHY (hypothesis) and WHO (audience) should be stable; the brief turns those into HOW (architecture + section spec + asset slots) precise enough for execution. Conversion rubric from lp-optimization is internalized — every section evaluated against the same craft rules used to audit existing pages, but applied at brief time so the page is *built* right rather than *audited* later.

Brand fidelity > aesthetic novelty. Conversion craft > visual flair. Specificity > flexibility. Designer executes, doesn't interpret.

## Inputs

| Artifact | Required? | What it provides |
|----------|-----------|------------------|
| Page route or campaign name (e.g. `/pricing`, `q3-launch-lp`) — current state if page exists (URL/screenshot/code) | **required** | Subject of the brief |
| `brand/BRAND.md` | **required** (NEEDS_CONTEXT if absent) | Voice, archetype, sacred elements, lexicon rules |
| `brand/DESIGN.md` | **required** (NEEDS_CONTEXT if absent) | Palette, typography, surface language, motion tokens |
| `.agents/mkt/lp-optimization.md` | **required for Route B** (existing-page redesign blocks without it; user can downgrade to Route A) | Audit-anchored hypothesis basis |
| `research/icp-research.md` | optional | Objections + VoC for copy candidates |
| `research/product-context.md` | optional | Product accuracy in features/proof |
| `.agents/mkt/campaign-plan.md` | optional | Traffic source, awareness stage, role in funnel |
| `.agents/targets.md` | optional | Conversion target informs CTA aggressiveness |

## Output

`.agents/mkt/lp-brief/[slug]/brief.md` — single artifact, structured per the template below.

Optional companions if the project uses them:
- `.agents/mkt/lp-brief/[slug]/handoff-claude-design.md` — verbatim prompt block for claude.ai/design
- `.agents/mkt/lp-brief/[slug]/handoff-figma.md` — design spec for human designer
- `.agents/mkt/lp-brief/[slug]/asset-slots/` — per-asset prompt artifacts (one per generative slot)

## Quality Gate

Two critics run in parallel before delivery, both binary PASS/FAIL:

- **Conversion critic** scores brief against `references/conversion-principles.md` (CP-01 → CP-13). Full rubric and gate logic in `agents/conversion-critic-agent.md`.
- **Brand-voice critic** scores sacred-element compliance, voice rules, surface language, token discipline, brief envelope (250–500 lines). Full rubric in `agents/brand-voice-critic-agent.md`.

Verdict logic: see `## Layer 5: Critic Gate` below.

## Chain Position

Previous: `lp-optimization` (optional — existing page redesign), `campaign-plan` (optional — campaign context), `brand-system` (required) | Next: `design-brief` per asset slot (optional), then implementation (Claude Design / image-gen / human designer)

**Re-run triggers:** new audit revision, BRAND.md/DESIGN.md update, ICP refresh, traffic source pivot. Increment `--rev=N`.

### Skill Deference

- **Page exists; need to know what to fix?** → `lp-optimization` first. Output (`.agents/mkt/lp-optimization.md`) feeds this skill.
- **Single visual asset spec, not whole page?** → `design-brief`.
- **No brand?** → `brand-system` first.
- **Need only headline variations?** → `copywriting`.
- **Non-LP page (blog, docs, navigation hub)?** → Out of scope. Conversion rubric doesn't apply.
- **Programmatic-SEO templates (industries/:slug, workflows/:slug, compare/:vs:)?** → **Out of scope for v1.** Targets single-purpose conversion pages (tier 1). Programmatic templates need a different rubric (template-fillability, slug-coverage, dedup) and would dilute the conversion-critic. Future skill.

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Audit-Anchor Agent | 1 (parallel) | `agents/audit-anchor-agent.md` | Pulls signals from lp-optimization audit (if exists) or gathers signals from page state and ICP |
| Brand-Anchor Agent | 1 (parallel) | `agents/brand-anchor-agent.md` | Pulls relevant tokens, sacred elements, voice rules from BRAND.md + DESIGN.md |
| Hypothesis Agent | 1.5 (after L1) | `agents/hypothesis-agent.md` | Generates 3 hypothesis candidates with 3Q rubric (Visual / Falsifiable / Unique) |
| Architecture Agent | 2 (after hypothesis approved) | `agents/architecture-agent.md` | Surface rhythm + section list + ASCII diagram + scroll velocity plan |
| Section-Spec Agent | 3 (after architecture approved) | `agents/section-spec-agent.md` | Per-section spec — copy slots, layout, motion, asset slots, conversion-checklist embed |
| Asset-Slot Agent | 3.5 (after section-spec — consumes its slot references) | `agents/asset-slot-agent.md` | Named asset slots with file paths, dimensions, formats, fallbacks, generation prompt templates |
| Hand-Off Agent | 4 (after L3) | `agents/handoff-agent.md` | Composes Claude Design / Figma / designer hand-off prompt block |
| Conversion Critic | 5 (parallel) | `agents/conversion-critic-agent.md` | Scores brief against lp-optimization rubric |
| Brand-Voice Critic | 5 (parallel) | `agents/brand-voice-critic-agent.md` | Scores brand fidelity + voice + envelope |

---

## Routing Logic

### Route A: Fresh LP (no existing page)

```
Step 0 → L1 (audit-anchor ∥ brand-anchor) → L1.5 (hypothesis) → ★ Gate 1
       → L2 (architecture) → ★ Gate 2
       → L3 (section-spec) → L3.5 (asset-slot) → L4 (handoff)
       → L5 (conversion-critic ∥ brand-voice-critic) → critic merge → ★ Gate 3
       → write brief.md + handoff/* + asset-slots/* to .agents/mkt/lp-brief/[slug]/
```

Per-layer details, contracts, and references are in the layer sections below.

### Route B: Existing LP redesign (audit-anchored — audit REQUIRED)

Existing page redesign. **Requires `.agents/mkt/lp-optimization.md`.** If absent, Step 0 blocks; user runs lp-optimization first or explicitly downgrades to Route A.

Same dispatch as Route A, but Layer 1 audit-anchor-agent reads the audit. Hypothesis anchored in audit findings ("rev N → rev N+1: what changed and why"). Architecture and section spec address audit failure modes explicitly. "What Changed from rev N-1" section becomes mandatory.

### Route C: Re-run with `--rev=N`

```
1. Read prior brief at .agents/mkt/lp-brief/[slug]/v[N-1]/brief.md
2. Read fresh inputs (new audit, new ICP)
3. Run Layer 1 — diff prior brief against fresh inputs
4. Hypothesis-agent receives "what's new since rev N-1" context
5. Continue Route A/B from Layer 1.5
6. Save new brief at .agents/mkt/lp-brief/[slug]/v[N]/brief.md, preserve prior versions
```

---

## Pre-Dispatch

This skill has **hard gates** before any cold-start questioning — brand artifacts and audit availability gate routing. Cold-start questions are bundled after gates pass. Approval Gates 1/2/3 (mid-flow user reviews) are separate from Pre-Dispatch and happen after Layer 1.5 / Layer 2 / Layer 5. Full Pre-Dispatch protocol pattern: `meta-skills/references/pre-dispatch-protocol.md`.

### Hard gates (before any questioning)

1. **Brand artifacts.** `brand/BRAND.md` AND `brand/DESIGN.md` must be present. If either missing → return **NEEDS_CONTEXT**, recommend `brand-system`. If either >60 days stale, warn and ask before proceeding.
2. **Audit availability gate (existing-page redesign).** `.agents/mkt/lp-optimization.md` present? If yes → Route B. Page exists but no audit → Route B **blocked**; offer: (a) run `lp-optimization` first then re-invoke (recommended), or (b) explicitly downgrade to Route A. Never silently treat existing-page redesign as Route A — guessing what's broken when you could measure it is a quality failure.
3. No existing page (greenfield) → Route A.

If hard gates pass, proceed to Pre-Dispatch flows.

### Needed dimensions
- Page identity — route + name (always supplied as input — not asked)
- Tier — conversion-primary (hero LP, /pricing, /services) or conversion-secondary (/about, /story). Programmatic out of scope.
- Hypothesis intent — what's the redesign trying to prove?
- Goal — leads / signups / purchases / demos
- Route (A or B) — already resolved by hard gates above

### Read order
1. Pipeline: `brand/BRAND.md`, `brand/DESIGN.md` (both confirmed by hard gate). `.agents/mkt/lp-optimization.md` if Route B. `research/icp-research.md`, `research/product-context.md`, `.agents/mkt/campaign-plan.md`, `.agents/targets.md` (all optional, read when present).
2. Experience: `.agents/experience/goals.md` for prior hypothesis/goal context. `.agents/experience/audience.md` for ICP fallback if no `icp-research.md`.

### Warm Start (page identity supplied + goal/hypothesis derivable)

Common when invoked from a campaign-plan that already declared the page's role:

```
Hard gates passed: brand artifacts present, [Route A | Route B with audit].
Found:
- page → "[route, tier]"
- goal → "[from experience/goals.md or campaign context]"
- hypothesis seed → "[from prior brief if rev > 1, or audit if Route B]"

Anything to override, or proceed to Layer 1?
```

### Cold Start (no campaign context, no prior rev, fresh hypothesis)

```
lp-brief produces a campaign-grade redesign brief — hypothesis, surface rhythm,
section spec, asset slots, hand-off prompts. Before I dispatch, I need:

1. **Page route + tier** — e.g., "/pricing, conversion-primary" or
   "/about, conversion-secondary". (Programmatic templates out of scope.)
2. **Hypothesis intent** — what's this redesign trying to prove or fix?
   One sentence. (Examples: "show pricing above the fold drives more
   trial starts" / "add objection-handling to address scaling concerns".)
3. **Goal** — what does the redesigned page need to do? Generate leads,
   drive trial signups, drive purchases, book demos, or other?
4. **Route confirmation** — [A: greenfield, no existing page] or
   [B: existing-page redesign with audit at .agents/mkt/lp-optimization.md].

Answer 1-4 in one response. I'll confirm and dispatch Layer 1.
```

### Write-back

After cold-start answers, append to experience/:

| Question | File | Key |
|---|---|---|
| 1. Page route + tier | (not persisted — page-specific, not stable cross-skill) |
| 2. Hypothesis intent | `goals.md` | `Goals — page hypothesis: [route]` |
| 3. Goal | `goals.md` | `Goals — page conversion goal: [route]` |
| 4. Route | (resolved by hard gates, not persisted) |

### Project-Specific Workflows

This skill **does not ship a default skill-chain doc.** Two paths:

1. **Project has one** (e.g., `growth/page-redesigns/_prompts.md`) — read once at orchestrator level. Brief REFERENCES by section header; never inline-duplicate. Add page-specific overrides only.
2. **Project does not** — brief generates a per-page chain inline: "Skill Chain" section listing downstream skills/prompts (`design-brief` per asset slot, `copywriting` for headline polish, `humanize` for AI-flavored copy). Page-scoped only — no project-level default created.

Rationale: project-level default locks teams into our chain. Per-page is correct because the chain depends on generative slots, copy polish needs, and asset rendering — all page-specific.

### Context to Pass to All Agents

After Pre-Dispatch resolves:
1. **Page identity** — route, name, current state (URL/screenshot/code if exists)
2. **Tier** — conversion-primary or conversion-secondary
3. **Audit signals** — from lp-optimization.md if Route B
4. **Brand digest** — palette, type, motion, sacred, voice rules (from brand-anchor after L1)
5. **Audience digest** — top 3 ICP objections, top 5 VoC phrases, awareness stage (from audit-anchor after L1)
6. **Campaign context** — traffic source, awareness stage, conversion target

---

## Dispatch Protocol

### How to spawn a sub-agent

1. Read agent instruction file — include FULL content in Agent prompt
2. Append context (digest excerpts, prior layer outputs, asset slot list, etc.)
3. Resolve all file paths to absolute (rooted at skill directory)
4. Pass upstream artifacts by content — orchestrator reads `.agents/mkt/lp-optimization.md`, `research/icp-research.md`, etc. FIRST and includes excerpts; sub-agents don't read these directly
5. If critic feedback exists, append with `## Critic Feedback — Address Every Point`

### Single-agent fallback

If multi-agent dispatch is unavailable, execute layers sequentially. Approval gates remain — single-agent mode does not bypass user gates.

---

## Layer 1: Parallel Foundation

| Agent | Pass These Inputs | Reference Files |
|-------|-------------------|-----------------|
| Audit-Anchor Agent | page identity + tier + lp-optimization.md (if present) + ICP | — |
| Brand-Anchor Agent | full BRAND.md + DESIGN.md + page identity | — |

Wait for both — outputs feed Layer 1.5.

---

## Layer 1.5: Hypothesis

| Agent | Pass These Inputs | Reference Files |
|-------|-------------------|-----------------|
| Hypothesis Agent | audit digest + brand digest + page tier + campaign context | `references/hypothesis-rubric.md`, `references/conversion-principles.md` |

Output: 3 candidates, each scored 3Q (Visual / Falsifiable / Uniquely Ours).

---

## Approval Gate 1 — Hypothesis Selection

**STOP.** Present 3 hypothesis candidates:

```
## Hypothesis Candidates

### A. [Title]
**Claim:** [single sentence — falsifiable]
**3Q score:** Visual [Y/N] / Falsifiable [Y/N] / Unique [Y/N] = N/3
**Why this:** [argument tied to audit findings or audience signals]
**Risk:** [main concern]

### B. [Title]
[same structure]

### C. [Title]
[same structure]

**Pick one (A/B/C), revise, or kill all.**
```

User responses:
- "A" / "B" / "C" → proceed to Layer 2 with that hypothesis
- "Revise X" → re-dispatch hypothesis-agent with feedback
- "None of these" → ask one clarifying question, regenerate
- "Stop" → save candidates, exit BLOCKED

---

## Layer 2: Architecture

| Agent | Pass These Inputs | Reference Files |
|-------|-------------------|-----------------|
| Architecture Agent | approved hypothesis + brand digest + audit digest + tier | `references/surface-rhythm.md`, `references/section-templates.md` |

Output: surface rhythm plan + section list + ASCII diagram + scroll velocity notes (where eye accelerates/decelerates/pauses).

---

## Approval Gate 2 — Architecture Approval

**STOP.** Present architecture:

```
## Page Architecture — [Hypothesis Title]

### Surface Rhythm
[3–5 line description of scroll experience: fast/slow/pause beats]

### Section List
1. Hero — [purpose + key message]
2. [section name] — [purpose]
...

### ASCII Page Diagram
[Visual schematic of section stacking, asset positioning, scroll velocity]

### Scroll Velocity Plan
[Where the eye accelerates / decelerates / pauses, tied to conversion gates]

**Approve, revise, or reject.**
```

User responses:
- "Approve" → proceed to Layer 3
- "Revise X" → re-dispatch architecture-agent with feedback (max 1 revise cycle here)
- "Reject" → return to Layer 1.5 to pick a different hypothesis OR exit BLOCKED

---

## Layer 3: Section Spec (then Asset Slots in 3.5)

| Agent | Pass These Inputs | Reference Files |
|-------|-------------------|-----------------|
| Section-Spec Agent | architecture + audit digest + brand digest + ICP objections + VoC | `references/section-templates.md`, `references/conversion-principles.md`, `references/failure-modes.md` |

## Layer 3.5: Asset Slots (after section-spec)

| Agent | Pass These Inputs | Reference Files |
|-------|-------------------|-----------------|
| Asset-Slot Agent | architecture + section-spec output (canonical source of slot IDs) + brand digest | `marketing-skills/skills/design-brief/references/asset-types.md` |

Asset-slot-agent runs **after** section-spec because slot IDs originate in section-spec's per-section asset references. Parallel execution guarantees ID drift.

---

## Layer 4: Hand-Off Composition

| Agent | Pass These Inputs | Reference Files |
|-------|-------------------|-----------------|
| Hand-Off Agent | full assembled brief (architecture + section spec + asset slots) + target tool (Claude Design / Figma / designer) | `references/handoff-formats.md` |

Output: hand-off prompt block, ready to paste into target tool.

---

## Layer 5: Critic Gate (parallel)

| Agent | Pass These Inputs | Reference Files |
|-------|-------------------|-----------------|
| Conversion Critic | full brief | `references/conversion-principles.md`, `references/section-templates.md` |
| Brand-Voice Critic | full brief + brand digest | `references/failure-modes.md` |

Both run in parallel. Orchestrator merges reports.

**Verdict logic** (max 2 cycles total). Critics return binary PASS/FAIL; NOTEs are advisory and don't change the verdict.

| Cycle 1 outcome | Action |
|-----------------|--------|
| Both PASS | DONE — write brief |
| Mixed or both FAIL | Re-dispatch each agent named in failing critics' Failures Summary `fix direction` field. (Critics emit per-FAIL routing — orchestrator does not hardcode it.) Combine feedback per receiving agent. Cycle 2. |

| Cycle 2 outcome | Action |
|-----------------|--------|
| Both PASS | DONE — write brief |
| Either or both FAIL | DONE_WITH_CONCERNS — write brief with all FAIL notes pinned at **top** of `brief.md` under `## Concerns` above body. Critic scores in frontmatter. User sees failing reports at Approval Gate 3 and decides: ship, revise manually, or kill. |

DONE_WITH_CONCERNS is the floor. No silent FAIL outputs — every critic concern visible in the artifact.

**Per-FAIL routing comes from critics, not this table.** Each FAIL includes `fix direction` naming the responsible agent (section-spec for copy/structure/checklist, asset-slot for asset, handoff for hand-off-only, brand-anchor for digest correction). Orchestrator follows that direction; do not assume failure-class → agent mappings.

---

## Approval Gate 3 — Final Brief Acceptance

**STOP.** Present the full brief + critic merge.

```
## Brief: [Page Slug] [rev N if applicable]

[Brief preview: hypothesis title, section count, asset slot count, hand-off target]

## Critics
- **Conversion:** [PASS / DONE_WITH_CONCERNS / FAIL] — [score]
- **Brand-voice:** [PASS / DONE_WITH_CONCERNS / FAIL] — [score]

[Concerns to monitor, if any]

**Approve, request revisions, or reject.**
```

User responses:
- "Approve" → write brief to `.agents/mkt/lp-brief/[slug]/brief.md` (with version subfolder if rev), status DONE
- "Revise X" → re-dispatch named layer with feedback (1 cycle)
- "Reject" → save as `.agents/mkt/lp-brief/[slug]/rejected.md`, exit BLOCKED

---

## Artifact Template — `.agents/mkt/lp-brief/[slug]/brief.md`

```markdown
---
skill: lp-brief
version: 1
date: [today]
status: [done | done_with_concerns | blocked | needs_context]
page_route: [/pricing | /services | etc.]
tier: [primary | secondary]
rev: [N — what revision this is]
hypothesis_title: [from approved hypothesis]
target_handoff: [claude-design | figma | designer]
brand_anchors:
  primary_color: [hex with token name]
  primary_type: [font, weight]
  surface: [paper / matte / glass-if-DESIGN.md-permits]
sacred_respected: [list]
critic_scores:
  conversion: [N/M]
  brand_voice: [N/M]
shared_skill_chain: [path to project's _prompts.md if referenced]
---

# Landing-Page Brief: [Title]

**Page:** [route + name]
**Tier:** [primary / secondary]
**Rev:** [N — what changed from rev N-1, if applicable]
**Hand-off target:** [Claude Design / Figma / designer]

## Concerns (only present if status = done_with_concerns)

> Pinned at top so downstream operators see them before reading the brief body.
>
> **Conversion critic:** [score / verdict] — [each FAIL bullet, verbatim from critic]
> **Brand-voice critic:** [score / verdict] — [each FAIL bullet, verbatim from critic]
>
> Decide before execution: ship as-is, revise manually, or kill.

## IMC Context

[1–3 lines: where this page sits in the campaign, traffic source, awareness stage, role in funnel.]

## Hypothesis (Approved)

**Claim:** [single sentence — falsifiable]
**3Q score:** Visual [Y/N] / Falsifiable [Y/N] / Unique [Y/N]
**Why this:** [argument tied to audit findings or audience signals]
**What we're betting:** [the falsifiable bet — what success looks like, what failure looks like]

## What Changed from rev N-1 (if rev > 1)

[Bullet list — only present if --rev=N. Tied to audit findings or new ICP signals.]

## Page Architecture

### Surface Rhythm

[3–5 lines: how the page reads at scroll speed. Fast / slow / pause beats.]

### Section List

1. **Hero** — [purpose + headline pull]
2. **[Section name]** — [purpose]
...
N. **CTA Block** — [purpose]

### ASCII Diagram

```
┌─────────────────────────────────────┐
│  HERO    [headline]    [hero CTA]   │  ← 100vh, low velocity
├─────────────────────────────────────┤
│  VALUE PROP — 3 columns             │
├─────────────────────────────────────┤
│  SOCIAL PROOF — logo grid + quote   │
├─────────────────────────────────────┤
│  ...                                 │
└─────────────────────────────────────┘
```

### Scroll Velocity Plan

| Section | Velocity | Why |
|---------|----------|-----|
| Hero | Slow / pause | First-impression gate |
| Value prop | Medium | Argument scan |
| Social proof | Slow | Decision moment |
| Features | Fast | Detail layer |
| Objection | Slow | Decision blocker |
| CTA | Pause | Action moment |

## Section-by-Section Spec

### 1. Hero

**Purpose:** [first-impression conversion gate]

**Headline candidates (3, 4-U scored):**
1. "[copy]" — Useful: Y, Unique: Y, Urgent: Y, Ultra-specific: Y → 4/4
2. "[copy]" — 3/4
3. "[copy]" — 4/4
**Recommended:** #[N] — [why]

**Subhead:** "[copy]"

**Hero CTA:** "[copy]" — primary, action verb + outcome, first-person

**Visual:** [reference to asset slot — see Asset Slots section]

**Layout:**
- Heading: [type token, size]
- Subhead: [type token, size]
- CTA position: [above-fold, button style, contrast pair]
- Background: [hex / asset slot]

**Motion:** [duration token from DESIGN.md if applicable; static otherwise]

**Conversion checklist (gates):**
- [ ] 4-U ≥ 3/4
- [ ] Message match to traffic source
- [ ] Above-fold value clear in 3 seconds
- [ ] Primary CTA visible without scroll
- [ ] Trust signal within scroll-distance (logo grid below or testimonial widget)
- [ ] Voice rules: no forbidden vocab

### 2. [Next Section]

[Same structure: purpose, copy candidates with rubric, visual, layout, motion, conversion checklist.]

[Continue per section...]

## Asset Slots

| Slot | Section | Dimensions | Format | File path | Fallback | Generation prompt |
|------|---------|-----------|--------|-----------|----------|-------------------|
| Hero image | Hero | 1920×1080 | WebP | `growth/[slug]/hero.webp` | solid #004700 | [link to prompt template, see asset-slots/] |
| Logo grid | Social proof | 6 cells × 60px | SVG | `growth/[slug]/logos.svg` | "delete cell if not real" | — |
| Founder portrait | Story | 600×600 | WebP | `growth/[slug]/founder.webp` | spot illustration | [link if generative] |

**Generation prompts** for asset slots that use generative AI live at `.agents/mkt/lp-brief/[slug]/asset-slots/[slot-name].prompt.md`. Each is written by `design-brief` against the slot's spec — the prompt is the actionable handoff to an image-generation tool.

## What NOT to Do

- [Sacred element 1 — verbatim "do not touch" line]
- [Sacred element 2]
- [Page-specific failure mode — e.g., "do not use stock-photo office imagery; ICP rejects it"]
- [Voice violations — e.g., "no leverage / unlock / seamlessly anywhere"]

## Hand-Off

### To: [Claude Design / Figma / designer]

**Prompt block (paste verbatim):**

```
[Hand-off prompt composed by handoff-agent — concrete enough to execute without follow-up]
```

### Pre-flight Checklist

- [ ] All copy in brief is final (or marked "candidate — pick one")
- [ ] All asset slots have file paths and fallbacks
- [ ] All sacred elements listed under What NOT to Do
- [ ] Critic scores both ≥ pass threshold
- [ ] Shared skill chain referenced (if project uses one) — not duplicated

## Skill Chain

**If project has a shared chain doc:** "See `growth/page-redesigns/_prompts.md` § Phase A — Hero Build" (etc.). List only page-specific overrides under each referenced phase.

**If project does not:** generate a per-page chain inline — list the downstream skills/prompts in execution order, each with one-line scope:

1. `design-brief` — spec hero asset (slot: `hero-image`), then run image-gen against the produced prompt at `asset-slots/hero-image.prompt.md`
2. `copywriting` — polish 3 headline candidates against 4-U + voice
3. [implementation step — Claude Design / Figma / designer]
4. `humanize` — final pass on any AI-generated body copy
5. [post-launch] re-run `lp-optimization` 30d after launch → next rev

Page-scoped only. No project-level default is created.

## Launch Plan

[3–5 lines: when, traffic ramp, instrumentation (UTMs, events to fire), success criteria from hypothesis.]

## Results (filled post-launch)

[Empty until launched. After: actual metrics, hypothesis verdict, what to take into rev N+1.]

## Why This Works (sanity check)

[2–4 lines: the brief's load-bearing arguments — why this hero/this architecture/this CTA hierarchy lands the hypothesis.]
```

> Re-run with `--rev=N`: write to `.agents/mkt/lp-brief/[slug]/v[N]/brief.md`, preserve prior versions.

---

## Worked Examples

See `references/examples.md` — three end-to-end walkthroughs (Route A fresh LP, Route B audit-anchored redesign, Route C `--rev=N` with mixed-critic verdict).

---

## Anti-Patterns

**Skipping audit when page exists** — Route A on an existing page wastes the rev signal. INSTEAD: run lp-optimization first, anchor the hypothesis in real findings.

**Generic hypothesis** — "This page should convert better." Not falsifiable. INSTEAD: "Engineering managers reject /pricing because they perceive overkill for small teams; segmenting proof by team size lifts conversion."

**Inlining the shared skill chain** — Duplicating the project's `_prompts.md` content into every brief. INSTEAD: reference by section header, add page-specific overrides only.

**Stale or fake proof** — Logo grid from 2023, testimonials with no source, "Trusted by 1000+ teams" with no link. INSTEAD: "delete cell if not real" — every proof element has a verifiable source.

**Ignoring sacred elements** — Brief proposes new logo treatment for "freshness." Auto-FAIL. INSTEAD: sacred elements are rails. Inside-the-rails creativity only.

**No objection handling** — Brief has hero, features, CTA — no rebuttal of the audience's stated objections. ICP research lists them; the brief must address the top 1–2.

**Brief too short** — Under 250 lines. Designer asks 5 follow-up questions. INSTEAD: spec everything: every section, every slot, every fallback.

**Brief too long** — Over 500 lines. Designer skims; misses critical spec. INSTEAD: cite shared chain instead of duplicating; cap section spec at the conversion-checklist gates.

**Hero copy violating voice** — "Unlock seamless leverage" passes 4-U but fails brand. The brand-voice critic catches this before delivery.

---

## Completion Status Protocol

- **DONE** — both critics PASS (cycle 1 or 2), brief approved, artifacts written
- **DONE_WITH_CONCERNS** — after 2 cycles, ≥1 critic still FAIL or mixed; concerns pinned at top of brief.md AND in frontmatter. User sees both reports at Approval Gate 3 and ships consciously.
- **BLOCKED** — user rejected at a gate, Route B audit missing without explicit downgrade, or required input missing mid-flow
- **NEEDS_CONTEXT** — BRAND.md or DESIGN.md missing; cannot proceed

---

## Agent Files

### Sub-Agent Instructions (agents/)

- [agents/audit-anchor-agent.md](agents/audit-anchor-agent.md) — Audit signal pull
- [agents/brand-anchor-agent.md](agents/brand-anchor-agent.md) — Token + sacred + voice digest
- [agents/hypothesis-agent.md](agents/hypothesis-agent.md) — 3 hypothesis candidates with 3Q
- [agents/architecture-agent.md](agents/architecture-agent.md) — Surface rhythm + section list
- [agents/section-spec-agent.md](agents/section-spec-agent.md) — Per-section spec
- [agents/asset-slot-agent.md](agents/asset-slot-agent.md) — Named asset slots with prompts
- [agents/handoff-agent.md](agents/handoff-agent.md) — Tool-specific hand-off
- [agents/conversion-critic-agent.md](agents/conversion-critic-agent.md) — lp-optimization rubric
- [agents/brand-voice-critic-agent.md](agents/brand-voice-critic-agent.md) — Brand fidelity + voice + envelope

### Shared References (references/)

- [references/conversion-principles.md](references/conversion-principles.md) — Curated from lp-optimization (4-U, above-fold, CTA, message-match, objection handling, social proof); cites lp-optimization references
- [references/surface-rhythm.md](references/surface-rhythm.md) — Page-architecture patterns (scroll velocity, section beats, breathing room)
- [references/section-templates.md](references/section-templates.md) — Hero, value prop, social proof, features, objection, FAQ, CTA — each with conversion-checklist
- [references/hypothesis-rubric.md](references/hypothesis-rubric.md) — 3Q scoring (Visual / Falsifiable / Uniquely Ours)
- [references/handoff-formats.md](references/handoff-formats.md) — Claude Design / Pencil MCP / Figma spec hand-off patterns
- [references/failure-modes.md](references/failure-modes.md) — Page-level failures (thin hero, weak CTA, no objection handling, brief bloat)
- [references/examples.md](references/examples.md) — Worked LP-brief examples
