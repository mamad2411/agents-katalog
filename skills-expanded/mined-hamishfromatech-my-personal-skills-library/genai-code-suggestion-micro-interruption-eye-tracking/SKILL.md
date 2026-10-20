---
name: genai-code-suggestion-micro-interruption-eye-tracking
description: Applies the first in-depth eye-tracking study of how developers interact with generative AI code suggestions during programming, revealing that ~50% of suggestions are ignored, 75%+ of looked-at suggestions are rejected, and each suggestion introduces a micro-interruption disrupting developer flow. Use when designing AI code suggestion UX, optimizing suggestion delivery timing, or measuring cognitive costs of AI autocomplete.
---

# Generative AI Code Suggestions & Micro-Interruption Eye-Tracking

## Source

Alakmeh, D'Angelo & Fritz — University of Zurich / Google — ICSE 2026

The first in-depth eye-tracking study examining how developers interact with generative AI code suggestions during real programming tasks. Rather than relying on self-report or telemetry-only data, this work uses high-frequency gaze data to measure exactly when, how long, and whether developers actually look at AI suggestions—and what happens to their typing flow afterward.

See `references/evidence-base.md` for full experimental setup, methodology, statistical tables, and extended analysis.

---

## Study at a Glance

| Dimension | Detail |
|---|---|
| Participants | 33 developers |
| Suggestions logged | 4,444 |
| Task | TypeScript coding in a web IDE |
| Session length | 45 minutes per participant |
| Eye tracker | EyeLink Portable Duo, 2000 Hz sampling |
| Suggestion logging | Custom Chrome extension capturing suggestion lifecycle events |
| Venue | ICSE 2026 |

---

## Key Findings

### 1. Half of All Suggestions Are Never Looked At

- **49.5% of suggestions** received zero visual attention — developers never gazed at them.
- This means the AI is generating, rendering, and presenting code that is functionally invisible roughly half the time.
- Implication: a large fraction of compute and screen real estate is spent on suggestions that have no chance of adoption.

### 2. Of Suggestions That Are Looked At, Over 75% Are Rejected

- **76.7% of looked-at suggestions are rejected.**
  - 5.5% actively rejected (explicit dismiss action).
  - 71.2% passively rejected (ignored after viewing; eventually discarded by typing or timeout).
- Only **23.3% of looked-at suggestions are accepted.**
- Combined with the 49.5% never looked at, the overall acceptance rate is very low — the majority of AI suggestion compute does not translate into adopted code.

### 3. Each Suggestion Is a Micro-Interruption

- A suggestion is visible for approximately **1.5 seconds** on average.
- When a developer does look, **dwell time is ~0.9 seconds.**
- Across a 45-minute session, developers experience **~51 micro-interruptions** — more than one per minute.
- These are not long pauses, but they are frequent enough to measurably disrupt typing flow and cognitive momentum.

### 4. Fixed Startup Cost to Read Any Suggestion

- There is a **256 ms fixed cost** to begin reading a suggestion, regardless of its length.
- After that initial parsing cost, per-character reading time stabilizes at **11.5 ms per character.**
- This means even very short suggestions impose a non-trivial cognitive entry tax before the developer can judge whether the suggestion is useful.

### 5. Deletion Rate Spikes During Micro-Interruptions

- Baseline deletion rate: **0.039 Hz** (deletions per second during normal typing).
- Deletion rate during micro-interruption windows: **0.226 Hz** — roughly **6× higher.**
- This indicates that suggestions frequently trigger rework: developers delete, rewrite, or restructure code after engaging with a suggestion, even when they ultimately reject it.

### 6. Suggestion Length Does NOT Predict Acceptance

- Accepted suggestions averaged **27.7 characters.**
- Rejected suggestions averaged **27.3 characters.**
- The difference is not statistically significant.
- Implication: making suggestions shorter or longer alone will not improve acceptance — the problem is relevance, timing, and cognitive cost, not size.

### 7. Acceptance Rate Rises Over Time

- Across task quartiles, acceptance rate climbs: **19.9% → 30.1%.**
- Developers are more receptive to suggestions toward the end of tasks and sessions, possibly as cognitive load accumulates or as the problem context becomes clearer to the AI.
- This temporal pattern is a strong signal that **when** suggestions are delivered matters as much as **what** is delivered.

---

## Suggestion Engagement Flow

```
Suggestion Shown
      │
      ├── (49.5%) Never Looked At ───────────────► Discarded (no engagement)
      │
      └── (50.5%) Looked At
                │
                ├── (23.3%) Accepted ─────────────► Adopted into code
                │
                └── (76.7%) Rejected
                          │
                          ├── (5.5%)  Actively Rejected (explicit dismiss)
                          │
                          └── (71.2%) Passively Rejected (ignored, timed out, or typed over)
```

---

## Design Implications

These are the concrete, evidence-backed design principles the study supports:

### Reduce Suggestion Volume
Given that nearly half of suggestions are never looked at and over three-quarters of the rest are rejected, the default strategy of continuously streaming suggestions imposes costs (cognitive interruption, screen clutter, compute) that far outweigh the adoption benefit. Systems should suppress or batch suggestions, only surfacing them when confidence and context are high.

### Temporal Awareness
Acceptance rate rises across task quartiles (19.9% → 30.1%). Suggestion systems should be temporally adaptive — reducing frequency early in a task when developers are still building a mental model, and increasing availability as the task matures and context stabilizes.

### Context-Adaptive Suggestion Style
Because length does not affect acceptance, the lever is not "shorter vs. longer" but "right fit for the moment." Systems should adapt suggestion granularity (single line, block, full function) to the current editing context rather than using a one-size-fits-all default.

### Alternative Presentation Formats
Inline ghost text forces a micro-interruption every time it appears. Alternatives worth exploring:
- **Collapsible previews** — suggestions hidden until explicitly expanded.
- **Overlay popovers** — appear on demand, not on every keystroke.
- **Side panels** — a dedicated suggestion surface that does not occlude the active editing region.
- **Deferred delivery** — queue suggestions and surface them at natural pause points (e.g., end of statement, save event).

---

## A-Tech Alignment

This skill aligns with the A-Tech ethos across four pillars:

- **Open Source**: The study provides a replication package and dataset, enabling independent verification and extension. Eye-tracking analysis code and the Chrome extension logging harness are available for community use.
- **Data Privacy**: The methodology uses local eye-tracking hardware and local data collection. The design principles it supports (local suggestion timing, local context adaptation) are compatible with privacy-preserving, on-device AI assistance.
- **Financial Freedom**: By reducing wasted suggestions and minimizing micro-interruptions, developers reclaim flow time — a direct efficiency and economic benefit for independent developers and small teams who cannot afford compute waste or attention fragmentation.
- **Practical Implementation**: The design implications are concrete and actionable — temporal gating, volume reduction, alternative presentation formats — not abstract theory. They can be implemented in existing open-source IDE extensions and editor plugins.

---

## Cross-References

- `ai-suggestion-micro-interruption-eye-tracking` — the generalized skill on AI-driven micro-interruptions measured via eye tracking (broader than code suggestions).
- `productivity-experience-paradox-ai-coding` — the paradox that AI coding tools can simultaneously increase output metrics while degrading developer experience and flow.
- `cognitive-load-reduction-for-ide` — techniques for reducing cognitive load in integrated development environments, including suggestion management, UI decluttering, and attention-aware interfaces.

---

## When to Use This Skill

Use this skill when:
- Designing or evaluating AI code suggestion UX (autocomplete, ghost text, inline completions).
- Deciding suggestion delivery timing, frequency, or presentation format.
- Measuring or arguing about the cognitive cost of AI autocomplete tools.
- Building open-source IDE extensions or editor plugins that include AI suggestions.
- Comparing generative AI suggestions against traditional autocomplete on cost-of-attention grounds.
- Writing content, talks, or analyses on developer experience with AI coding tools.

---

## Quick-Reference Statistics

| Metric | Value |
|---|---|
| Suggestions never looked at | 49.5% |
| Looked-at suggestions rejected | 76.7% |
| — Actively rejected | 5.5% |
| — Passively rejected | 71.2% |
| Looked-at suggestions accepted | 23.3% |
| Avg. suggestion visible time | ~1.5 s |
| Avg. dwell time (when looked at) | ~0.9 s |
| Micro-interruptions per session | ~51 (>1/min) |
| Fixed startup cost to read | 256 ms |
| Per-character reading cost | 11.5 ms/char |
| Deletion rate during micro-interruption | 0.226 Hz |
| Baseline deletion rate | 0.039 Hz |
| Deletion rate multiplier | ~6× |
| Avg. length — accepted | 27.7 chars |
| Avg. length — rejected | 27.3 chars |
| Acceptance rate by quartile | 19.9% → 30.1% |

---

## Evidence Base

For the full experimental setup, eye-tracking methodology details, statistical results tables, suggestion engagement flow analysis, temporal analysis, extended design implications, and comparison with traditional autocomplete studies, see:

→ [`references/evidence-base.md`](references/evidence-base.md)