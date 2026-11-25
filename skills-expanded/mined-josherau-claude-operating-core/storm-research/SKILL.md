---
name: storm-research
description: Use when researching any topic, question, market, company, technology, or decision — before writing reports or proposals, making business or investment decisions, preparing for negotiations, interviews, or presentations, or learning a new field. This is the default research method for all research tasks. Skip only for single-fact lookups, or when the user explicitly asks for a quick answer or names a different method.
---

# STORM Research

## Overview

Multi-perspective research method adapted from Stanford's STORM (Shao et al., NAACL 2024, github.com/stanford-oval/storm). Core principle: **one query returns the majority view; five grounded perspectives plus a contradiction map returns understanding.** The STORM paper reports ~25% better organization and ~10% broader coverage from multi-perspective question asking versus its single-pass baseline.

**The Iron Rule: every perspective must be grounded in real retrieval.** Persona-prompting without sources is five flavors of one model's blind spots hallucinating in harmony. Each perspective's claims come from actual searches (WebSearch, WebFetch, or whatever search MCPs you have wired up) with sources noted. No search → no claim.

## The Four Phases

Run all four, in order. Do not stop after Phase 1 or 3.

### Phase 1 — Multi-Perspective Scan
Pick 5 perspectives suited to the topic. Default set:

| Perspective | Asks |
|---|---|
| Practitioner | What actually happens day-to-day? What breaks in reality? |
| Skeptic | What's overhyped or wrong? What could fail? |
| Economist | Who profits? What incentives shape the claims? |
| Historian | Has this pattern happened before? How did it end? |
| Academic | What does the actual evidence/data say? |

Swap perspectives when the topic demands (e.g. regulator, customer, competitor, clinician). For each: generate that persona's 2-3 sharpest questions, then **search to answer them**. Note the source for each finding.

### Phase 2 — Contradiction Map
Find where the perspectives fight and why. Rules of evidence:
- All 5 agree → probably true.
- Perspectives conflict → the real understanding lives here; name the disagreement and the reason (incentive, timeframe, evidence quality).
- Nobody addressed it → you found a gap; say so explicitly.

### Phase 3 — Synthesis
One briefing: what's established (with sources), the named contradictions, reliability ranking of major claims, and a **specific recommended action** — not a summary that hedges everything.

### Phase 4 — Peer Review
Adversarially grade your own output: strongest claim, weakest claim, likely source bias, missing perspective, and a confidence score per key conclusion. The original STORM pipeline has no self-critique step, so this phase is our addition — and it is not optional. (And per the review-panel rule: Phase 4 is still self-critique — the finished deliverable gets an independent reviewer too.)

## Scaling

| Mode | When | How |
|---|---|---|
| Quick | Casual question, minutes matter | 3 perspectives, ~5 searches, all inline |
| Standard (default) | Most research requests | 5 perspectives, 8-15 searches, inline or 2-3 parallel subagents |
| Deep | "Thorough/comprehensive/audit" | One subagent per perspective in parallel, then synthesize; consider a dedicated deep-research harness if you run one |

## Output Shape

Deliver: **Briefing** (synthesis + recommended action) → **Contradiction map** → **Perspective findings with sources** → **Peer review with confidence scores**. Briefing first — the reader gets the answer before the apparatus.

## Common Mistakes

- **Answering from training data with persona flavoring.** The perspectives structure the questions; retrieval answers them.
- **Perspectives that converge.** If the skeptic sounds like the academic, you picked lazy personas — force genuine disagreement in framing.
- **Skipping Phase 2.** The contradiction map is the step that separates this from a book report.
- **Skipping Phase 4 to save time.** 60 seconds of self-critique is the method's error bar.
