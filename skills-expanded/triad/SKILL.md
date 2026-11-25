---
name: Triad Derivations
slug: triad-derive
description: Derived outputs computed from the VISION/SPEC/BUILDING triangle — roadmap, drift, status, changelog, pitch, debt, onboard
category: operations
complexity: complex
version: "1.0.0"
author: "id8Labs"
triggers:
  - "roadmap"
  - "drift"
  - "changelog"
  - "pitch"
  - "debt"
  - "onboard"
tags:
  - triad
  - documentation
  - operations
  - derivation
---

# Triad Derivations — Computed Outputs from the Triangle

The Triad (VISION.md, SPEC.md, BUILDING.md) is a normalized data store. These commands are **views** — computed fresh from the three source documents every time. Nothing is cached. Nothing goes stale.

## Core Principle

Every derived output is a function of deltas between the three documents:

```
VISION - SPEC           = gap (what doesn't exist yet)
SPEC - BUILDING         = undocumented work (exists but not journaled)
BUILDING -> VISION      = trajectory (converging or drifting?)
BUILDING velocity       = momentum (what ships fast vs. slow)
```

The three documents dictate priority, order, and urgency. No human maintains a separate roadmap or status page. The triangle produces them.

---

## Command: `/roadmap`

**Function:** `f(VISION, SPEC, BUILDING)` — Prioritized list of what to build next.

### Algorithm

1. **Read all three documents** into context.
2. **Extract the gap:** Every VISION pillar marked UNREALIZED or PARTIAL that has no matching SPEC capability = roadmap item.
3. **Score each item for priority** using three signals:

   | Signal | Source | Weight | How to Extract |
   |--------|--------|--------|----------------|
   | **Dependency depth** | VISION | High | Does this pillar unblock other pillars? Are other pillars described as depending on it? Foundational items score higher. |
   | **Momentum** | BUILDING | Medium | How many recent BUILDING entries reference or point toward this item? Recent activity = active energy = higher priority. |
   | **Distance from done** | SPEC | Medium | For PARTIAL items: how much capability already exists? Items closer to done (higher partial %) are cheaper to finish = higher priority. |
   | **Recency signal** | BUILDING | Low | When was this last mentioned in BUILDING? Stale items (no mention in 30+ days) deprioritize unless they're foundational. |

4. **Sort by composite score** (dependency > momentum > distance > recency).
5. **Group into tiers:**
   - **Now** — highest priority, has momentum, foundational
   - **Next** — medium priority, dependencies met, no active blockers
   - **Later** — low priority, blocked by other items, or no momentum signal

### Output Format

```
ROADMAP — [PROJECT] — [DATE]
Derived from: VISION.md (evolved [date]) + SPEC.md (reconciled [date]) + BUILDING.md

Distance: [X]% ([N]/[M] pillars realized)

--- NOW ---
1. [Pillar/Item] — [why it's first: dependency + momentum signals]
   Gap: [what VISION says] vs [what SPEC has]
   Momentum: [BUILDING references]
   Effort estimate: [small/medium/large based on gap size]

2. ...

--- NEXT ---
3. ...

--- LATER ---
5. ...

BLOCKED:
- [Item] — blocked by [dependency]. Unblocks when [condition].
```

6. **Do NOT create a file.** This is ephemeral output. If Eddie wants it saved, he'll say so.

### Priority Override

If Eddie says "roadmap for [specific pillar]", zoom into that pillar's sub-items using SPEC capabilities as the granularity level.

---

## Command: `/drift`

**Function:** `f(VISION, BUILDING)` — Are we building toward the vision or wandering?

### Algorithm

1. **Read VISION.md and BUILDING.md.**
2. **Forward mapping:** For each VISION pillar, scan BUILDING for entries that advance it. Count momentum per pillar.
3. **Reverse mapping:** For each BUILDING entry (last 30 days), check if it maps to ANY VISION pillar. Entries that don't map = potential scope creep.
4. **Neglect detection:** VISION pillars with ZERO BUILDING momentum in 30+ days = neglected priorities.
5. **Contradiction detection:** BUILDING entries that move in a direction the Anti-Vision warns against.

### Output Format

```
DRIFT ANALYSIS — [PROJECT] — [DATE]

TRAJECTORY: [CONVERGING / DRIFTING / DIVERGING]

Pillar Momentum (last 30 days):
  [Pillar 1]: [N] BUILDING entries — [STRONG/MODERATE/NONE]
  [Pillar 2]: [N] BUILDING entries — [STRONG/MODERATE/NONE]
  ...

Scope Creep Candidates:
  [BUILDING entry] — does not map to any VISION pillar
  ...

Neglected Priorities:
  [Pillar] — no BUILDING momentum in [N] days
  ...

Anti-Vision Warnings:
  [BUILDING entry] — may conflict with Anti-Vision: "[quote]"
  ...

Recommendation: [1-2 sentences on what to do]
```

---

## Command: `/changelog`

**Function:** `f(BUILDING, SPEC)` — What shipped recently.

### Algorithm

1. **Read BUILDING.md and SPEC.md.**
2. **Extract recent BUILDING entries** (default: since last SPEC reconciliation date, or last 14 days if no date found).
3. **Cross-reference with SPEC capabilities** to classify each entry:
   - **New capability** — BUILDING entry describes something now in SPEC that wasn't before
   - **Enhancement** — BUILDING entry improves an existing SPEC capability
   - **Fix** — BUILDING entry fixes a bug or issue
   - **Architecture** — BUILDING entry changes infrastructure/stack
   - **Internal** — BUILDING entry doesn't change user-facing capabilities
4. **Generate changelog** grouped by type, most impactful first.

### Output Format

```
CHANGELOG — [PROJECT] — [DATE RANGE]
Derived from: BUILDING.md entries since [start date]

### New
- [Capability]: [what it does, why it matters]

### Enhanced
- [Capability]: [what changed]

### Fixed
- [Issue]: [what was wrong, what was fixed]

### Architecture
- [Change]: [what moved, why]

### Internal
- [Change]: [context]
```

---

## Command: `/pitch`

**Function:** `f(VISION, SPEC)` — Investor/user-facing narrative.

### Algorithm

1. **Read VISION.md and SPEC.md.**
2. **Extract:**
   - Soul statement (VISION) = the story hook
   - Realized pillars (VISION) = proof points
   - Key capabilities (SPEC) = what works today
   - User Truth (VISION) = who this serves
   - Distance metric = progress signal
3. **Compose a narrative** that weaves vision with evidence:
   - Hook: the problem (from Soul)
   - Proof: what already works (from SPEC capabilities mapped to realized pillars)
   - Direction: where it's going (from unrealized pillars, framed as opportunity)
   - Traction: metrics from SPEC if available (users, capabilities, integrations)

### Output Format

A flowing narrative paragraph structure (NOT bullet points). Suitable for:
- Investor pitch deck "product" slide
- Landing page hero copy
- Cold email product summary
- Grant application product description

Present two versions:
1. **Short** (3-4 sentences) — elevator pitch
2. **Full** (2-3 paragraphs) — detailed narrative

---

## Command: `/debt`

**Function:** `f(SPEC, VISION, BUILDING)` — Technical and product debt.

### Algorithm

1. **Read all three documents.**
2. **Contradiction scan (SPEC vs VISION):**
   - SPEC capabilities that don't serve any VISION pillar = potential bloat
   - SPEC architecture choices that BUILDING describes as workarounds = tech debt
   - SPEC boundaries that contradict VISION edges = scope misalignment
3. **Workaround scan (BUILDING):**
   - BUILDING entries that describe workarounds, hacks, "for now" solutions, or deferred decisions
   - Cross-reference with SPEC to see if they're still present
4. **Orphan scan (SPEC):**
   - SPEC capabilities with no VISION justification (no pillar serves them)
   - These are features that exist but shouldn't, or whose purpose was never articulated
5. **Stale scan:**
   - SPEC capabilities not mentioned in BUILDING for 60+ days = potentially abandoned code

### Output Format

```
DEBT REPORT — [PROJECT] — [DATE]

PRODUCT DEBT (features that shouldn't exist or conflict with vision):
- [Capability] — exists in SPEC but serves no VISION pillar
  Risk: [what happens if you keep it / cost of removal]

TECHNICAL DEBT (workarounds still in place):
- [Item] — BUILDING says "[quote]", still present in SPEC
  Fix: [what the proper solution would be]

SCOPE MISALIGNMENT:
- [SPEC boundary] conflicts with [VISION edge]

ORPHANED CAPABILITIES:
- [Capability] — no BUILDING momentum, no VISION justification
  Recommendation: [remove / justify / investigate]

Debt Score: [LOW / MEDIUM / HIGH] based on count and severity
```

---

## Command: `/onboard`

**Function:** `f(BUILDING, SPEC)` — New contributor orientation.

### Algorithm

1. **Read BUILDING.md and SPEC.md.**
2. **Extract from SPEC:**
   - Identity (what this product is)
   - Architecture contract (stack, data model, integrations)
   - Key capabilities (what it does)
   - Boundaries (what it doesn't do)
3. **Extract from BUILDING:**
   - Major architectural decisions and WHY they were made
   - Key pivots or direction changes
   - Known gotchas or "we tried X but Y" entries
4. **Compose an onboarding guide** that answers:
   - What is this? (SPEC identity)
   - What does it do? (SPEC capabilities, grouped)
   - How is it built? (SPEC architecture)
   - Why is it built this way? (BUILDING decisions)
   - What should I know before touching this? (BUILDING gotchas + SPEC boundaries)

### Output Format

```
ONBOARDING — [PROJECT]
Generated [DATE] from SPEC.md + BUILDING.md

## What This Is
[2-3 sentences from SPEC identity]

## What It Does
[Grouped capabilities from SPEC]

## How It's Built
[Architecture table from SPEC + key decisions from BUILDING]

## Why It's Built This Way
[Top 3-5 architectural decisions from BUILDING with rationale]

## Before You Touch This
[Gotchas, known issues, things that look wrong but are intentional]

## What's Off-Limits
[Boundaries from SPEC + Anti-Vision from VISION if available]
```

---

## Shared Rules (All Commands)

1. **Always read all three documents first.** Even if a command only uses two, having the third in context improves accuracy.
2. **Never create persistent files.** These are ephemeral computed outputs. Present them in conversation. Eddie saves what he wants.
3. **Detect project automatically** from current directory, or accept `--project <name>` flag.
4. **If any document is missing,** say which one and offer to create it via `/reconcile init`.
5. **Date awareness:** Convert all relative references to absolute dates. "Recently" means last 14 days. "Stale" means 30+ days.
6. **Voice matching:** Read BUILDING.md first to match the project's voice and tone.
7. **No brackets.** These outputs are polished, not templates.
8. **Respect the pipeline.** If the project uses ID8Pipeline stages, reference the current stage in outputs where relevant.
