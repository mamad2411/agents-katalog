---
name: mobile-product-brief
description: Turn an early mobile app idea, feature request, or product concept into an actionable, assumption-aware product brief for UX and UI design. Use when Codex needs to clarify target users, problem, jobs, value proposition, activation, core loop, MVP scope, constraints, risks, success signals, or handoff requirements before mobile flows, wireframes, UI, prototyping, or implementation.
---

# Mobile Product Brief

Convert ambiguous product intent into a bounded design contract. Preserve uncertainty: separate user-provided facts, external evidence, assumptions, hypotheses, and product decisions.

## Choose the brief mode

- **Create**: produce a new brief from an idea or rough request.
- **Refine**: resolve contradictions and missing decisions in an existing brief.
- **Feature**: define a feature inside an existing product without rewriting the whole product strategy.

Do not perform competitive UI analysis in this skill. When references or screenshots drive the request, use `analyze-mobile-ui` first and cite its output as evidence.

## Collect the minimum input

Establish when available:

- Product idea or requested change.
- Target users and situation.
- Desired user outcome.
- Target platforms and devices.
- Business, legal, privacy, technical, time, or brand constraints.
- Existing evidence, product context, and explicit non-goals.

Proceed with partial input when a reversible assumption can preserve momentum. Ask only when a missing choice would materially change the product, audience, safety boundary, or scope. Record every assumption that remains.

## Follow the workflow

### 1. Build the source ledger

Assign stable IDs to user statements, existing documents, research, and prior analyses. Classify each important input as:

- `fact`: directly stated by the user or supported by a cited source.
- `assumption`: plausible but unverified condition used to proceed.
- `hypothesis`: testable belief about user behavior or product value.
- `decision`: chosen product direction and its owner or rationale.

Do not turn a user request into a market fact. Do not invent demand, demographics, conversion, retention, or competitor performance.

### 2. Frame the problem and audience

Write the problem as a user situation, friction, and consequence. Define a primary audience narrow enough to design for, then list secondary or excluded audiences only when useful.

Read [references/product-framing.md](references/product-framing.md) for framing tests and anti-patterns.

### 3. Define jobs and outcomes

Capture functional, emotional, and social jobs only when relevant. Express desired outcomes without prescribing a feature. Distinguish the user's outcome from the buyer's or business outcome.

### 4. State the value proposition and principles

Write one falsifiable value proposition:

```text
For [primary user] in [situation], [product] helps [progress] by [mechanism], unlike [current alternative], while [important boundary].
```

Add three to five design principles. Each principle must change a product or UX decision; reject slogans such as “simple,” “delightful,” or “seamless” without consequences.

### 5. Bound the product mechanism

Define:

- Entry point and trigger.
- Activation moment in observable user terms.
- Core loop as ordered action and feedback.
- Accumulated value and return trigger.
- MVP capabilities required for that loop.
- Explicit non-goals and later ideas.

Keep the MVP as the smallest coherent value loop, not the smallest screen count.

### 6. Specify constraints and trust boundaries

Cover applicable platform, accessibility, privacy, permission, sensitive-data, moderation, child-safety, financial, medical, legal, localization, connectivity, and operational constraints.

For iOS and Android, describe outcome parity separately from implementation parity. Do not assume widgets, background work, permissions, navigation, or system surfaces behave identically.

### 7. Record risks and hypotheses

For each material risk or hypothesis, state:

- What is uncertain.
- Why it matters.
- Earliest low-cost validation method.
- Decision or threshold the result will inform.

Prioritize tests that can invalidate the core value or safety model before visual refinement.

### 8. Define success and guardrails

Use observable success signals tied to user progress and product health. Mark numeric targets `TBD` unless supplied or derived from credible evidence. Include guardrail signals for harm, confusion, privacy, or exclusion where relevant.

Do not replace an outcome with vanity metrics such as downloads, page views, or raw session time.

### 9. Create the UX handoff

List:

- Primary scenarios and actors.
- Required entry, happy-path, empty, error, offline, permission, destructive, and recovery states.
- Objects and their important lifecycle states.
- Platform integrations and known differences.
- Open decisions that block UX architecture.
- Acceptance signals a reviewer can observe.

This handoff defines what `mobile-ux-architect` must solve without prescribing screen layouts.

### 10. Produce and validate the brief

When files are requested or this skill is part of a design workflow, create:

- `product-brief.md` using [assets/product-brief-template.md](assets/product-brief-template.md).
- `product-brief.json` using [assets/product-brief-template.json](assets/product-brief-template.json) and [references/product-brief-schema.md](references/product-brief-schema.md).

Run `python3 scripts/validate_product_brief.py <path-to-product-brief.json>` and fix every error before delivery. Treat warnings as review prompts.

When responding only in conversation, keep the same section order but avoid unnecessary files.

## Enforce the output contract

Include, in order:

1. Brief summary and confidence.
2. Source ledger and assumptions.
3. Problem, audience, and jobs.
4. Value proposition and principles.
5. Activation, core loop, MVP scope, and non-goals.
6. Constraints and trust boundaries.
7. Risks, hypotheses, and validation plan.
8. Success signals and guardrails.
9. UX handoff and open decisions.

## Run the quality gate

Read [references/product-brief-rubric.md](references/product-brief-rubric.md) and revise any blocking failure before completing.

Do not finish until:

- Facts, assumptions, hypotheses, and decisions remain distinct.
- The audience and situation are specific enough to design for.
- Activation and the core loop are observable.
- MVP scope contains a coherent value loop and explicit non-goals.
- Sensitive data, permissions, failure, and platform constraints are addressed when relevant.
- Success signals measure user progress and include applicable guardrails.
- The UX handoff names required states without prematurely drawing screens.
