---
name: bounded-delegation-developer-ai-boundaries
description: Applies the Microsoft study of 860 developers identifying 22 wanted AI systems and four cross-cutting guardrails, culminating in "bounded delegation" — developers want AI to absorb the assembly work surrounding their craft, never the craft itself, and the boundary tracks professional identity, not capability. Use when designing AI developer tools, setting agent autonomy policies, or planning team norms around what agents may and may not do.
---

# Bounded Delegation: Where Developers Draw the Line

## Overview
The largest stated-preference study of AI tooling in software (860 Microsoft developers, human-in-the-loop multi-model thematic analysis) found demand concentrated overwhelmingly on the **verification side** of the workflow — 22 wanted systems across five task categories — and found four constraints developers place on nearly every system: explicit authority scoping, provenance, uncertainty signaling, and least-privilege access. The pattern they name: **bounded delegation** — AI may absorb assembly; it may not absorb craft. Crucially, developers drew this line even for tasks they acknowledged AI could handle, which means the boundary is unlikely to move just because models improve.

## When to Use
- Scoping what an AI coding/ops agent is allowed to do in a team
- Designing tool features so developers don't route around them
- Explaining to leadership why adoption friction is principled, not obstruction
- Content: "The value of AI tooling lies in where — and how precisely — it stops"

**NOT for**: the review-production gap telemetry (use `review-production-gap-observability-2026`), the developer-side trust survey (use `sonar-state-of-code-2026`), agent-building workflow research (use `se-agent-building-practice`).

## Core Process

### 1. The 22 systems across five categories (with top wants)
- **Development (N=353)**: scoped-PR builder for tech debt (50.1% — atomic reviewable diffs, stops at authorized boundaries), embedded quality gate at authorship time (27.8%), trace-to-diff root-cause workbench (19.5% — assembles the incident "case file," proposes narrow patch + regression test), repository context graph for cross-file changes (18.4%).
- **Design & Planning (N=223)**: design-to-sprint workbench (30.5%), architecture studio (27.8% — multiple materially different architectures, never one), design trade-off analyzer (20.6%), decision context/provenance graph (19.7%), full-loop design-doc workspace (15.2%).
- **Quality & Risk (N=155)**: change-aware test generation + quality gates (44.5% — impact map from the diff), context-aware PR review assistant (23.2% — states what it checked and what it didn't), pre-merge security advisor (21.9%), compliance evidence compiler (14.2%), change risk radar (11.6%).
- **Infra & Ops (N=101)**: telemetry correlation assistant (40.6% — read-only evidence bundles, alert tuning), CI/CD blueprint builder (33.7%), maintenance backlog prioritizer (16.8%), customer-support triage (11.9%).
- **Meta-work (N=157)**: DocSync continuous documentation (45.9%), contextualized ramp-up coach (30.6%), stakeholder-communication drafting (12.7%), interactive tech-discovery board (11.7%).

### 2. The four cross-cutting guardrails (treat as design requirements)
1. **Explicit authority scoping** — operate within a declared boundary; halt when judgment is required.
2. **Provenance** — trace every output to sources; show lineage for decisions.
3. **Uncertainty signaling** — surface when evidence is missing or confidence is low; abort rather than guess.
4. **Least-privilege access** — strict boundaries around sensitive data; read-only by default in production.

### 3. The two-part boundary
- **The tooling part may move**: "AI is very bad at understanding context and throwing wrong answers with utmost confidence" — as models improve, more assembly work becomes delegable.
- **The agency part does not**: "AI should not settle the final decision ever. Because this is the part that people should be accountable for" (P774). Developers refused delegation where it would erode task identity and ownership — Hackman & Oldham's work-design prediction, not a capability assessment. Work-design theory implies treating the boundary as a durable design requirement, not a transient adoption lag.

### 4. The right-shift problem (why verification demand dominates)
AI accelerates the already-fast part (generation) and expands the slow, human-intensive parts (review, verification, incident triage). Consequences: reviewers face more code with less provenance; on-call debugs systems nobody on the team fully understands; docs drift faster than anyone can track; "workslop" forces recipients to redo work. **Design response: left-shift quality signals to the point of change** — every one of the 22 systems targets authorship time, where cost-to-fix is lowest and context is richest.

### 5. Calibration warning
Too little constraint → lost control and trust; too much → developers route around the tools entirely. Where the boundary sits varies by context and criticality — treat calibration as a priority for team-level policy, and instrument it (which guardrail trips most? where do users override?).

## References
- Pairs with `se-agent-building-practice` (how builders of agents experience the same boundaries), `review-production-gap-observability-2026` (the operational-twin evidence), `sonar-state-of-code-2026` (the trust gap at scale), `junior-senior-agency-allocation` (how agency preferences diverge by experience), `hax-perception-behavior-gap-2026` (stated vs measured divergence — pair before generalizing any stated-preference finding).
- A-Tech alignment: open source (the four guardrails are implementable in any OSS agent harness — provenance and uncertainty signaling are the differentiators), privacy (least-privilege + evidence-collection boundaries are the privacy layer of the same spec), financial freedom (build for the verification layer — that's where willingness-to-pay concentrates), practical (the guardrails are a one-page review checklist for any tool proposal).