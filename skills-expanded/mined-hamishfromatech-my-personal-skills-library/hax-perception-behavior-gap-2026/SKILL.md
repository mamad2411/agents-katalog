---
name: hax-perception-behavior-gap-2026
description: Applies the JetBrains HAX mixed-method study (800 developers, two years of telemetry) on how AI redistributes developer workflows invisibly. Use when measuring AI coding tool impact, designing developer surveys vs telemetry, interpreting self-report divergence, or planning DevEx measurement programs.
---

# HAX Perception-Behavior Gap 2026

## Overview

JetBrains' Human-AI Experience (HAX) team presented at ICSE 2026 (Rio de Janeiro) a mixed-method study of AI-assisted developer workflows: **two years of IDE telemetry from 800 developers** (151,904,543 logged events; 400 AI users vs 400 non-users, devices active from Oct 2022 — ChatGPT's release — through Oct 2024), triangulated with a 62-developer survey and follow-up interviews.

Headline: **AI redistributes and reshapes developers' workflows in ways that often elude their own perceptions.** Several major behavioral shifts were invisible (or inverted) in self-reports.

## Methodology (why this study is trustworthy)

- Telemetry only counts action events — no code content. Dimensions proxy-mapped: typed characters (productivity), debugging-session starts (code quality), delete/undo actions (editing), external paste events without in-IDE copy (reuse), IDE window activations (context switching).
- Mixed-method design compensates blind spots: logs show *that* workflows change but not why; self-reports explain motivation but are biased and miss subtle shifts.
- Limitation acknowledged: chosen proxies are imperfect; goal is pattern detection over time, not causal effects.

## The Five Dimensions — Perception vs Behavior

| Dimension | Telemetry (behavior) | Survey/interview (perception) | Aligned? |
|---|---|---|---|
| **Productivity** | AI users +~600 typed chars/month vs +75 for non-users; gap grew over 2 years | >80% report productivity increase; >50% less coding time | **Aligned** |
| **Code quality** | No significant change in debugging starts for AI users | ~47% say quality slightly/significantly increased | **Diverged** (perception positive, behavior flat) |
| **Code editing** | AI users +~100 deletions/month vs +7 for non-users (significant) | Half report *no* change in editing behavior | **Inverted** (major behavior change, no perception) |
| **Code reuse** | AI users higher external-paste baseline; no large change over time | ~33% increase / 20% decrease / 44% no change | Roughly aligned (both flat) |
| **Context switching** | AI users +~6 IDE activations/month; non-users −7 | No clear pattern; "I stopped switching contexts, saving a few seconds every time I would have googled something" | **Diverged** (behavior up, perception "less switching") |

## The Core Lessons

1. **The editing inversion is the signal**: AI makes code dramatically more iterative (deletions/undo up ~14× faster than non-users) while developers report feeling no change. Curation work — accepting, reworking, deciding what stays — has become a large, invisible workload.
2. **Quality perception is not quality behavior**: developers *feel* quality improved while their debugging behavior is unchanged. Trust feelings are not quality evidence. ("I triple-check it, and even then, I still feel a bit uneasy.")
3. **Context switching is re-shaped, not reduced**: in-IDE AI doesn't eliminate context hops; it trades googling-seconds for dialogue-management fragmentation — a different interruption pattern, not fewer interruptions.
4. **Perceived vs actual productivity**: echoes prior findings (developers perceived Copilot productivity gains "despite the data showing otherwise"; another study: perceived +20% completion speed, actually 19% slower). Belief outpaces measurement in both directions.

## Practical Applications

### For measurement programs
- Never rely on self-report alone: pair surveys with telemetry (event counts, not content) for the five workflow dimensions.
- Instrument deletions/undo and review-time explicitly — the highest-divergence, most-invisible signals.
- Treat "productivity" claims as perception data; validate against delivery metrics before budget decisions.

### For tool design
- Make curation work visible: dashboards/surfaces showing how much accepted AI output gets reworked — surfacing the editing inversion turns invisible toil into manageable process.
- Design for the dialogue-fragmentation reality: AI interfaces should reduce, not merely relocate, interruptions.

### For leaders
- 84% feel faster; the HAX study is the mechanism behind why you should still measure: feelings, quality perception, editing burden, and attention fragmentation all diverge from behavior.
- The four GitKraken moves pair naturally: baseline before scaling; maturity ladder; compare tools; instrument agents. HAX supplies the evidence that self-reports (the 33% leaning on them) are structurally unreliable.

## A-Tech Values Alignment

- **Open-source AI**: JetBrains published the method openly at ICSE; findings apply directly to open-source agentic tooling (Aider, Cline, OpenHands) where telemetry habits are weaker.
- **Data privacy**: The study is a privacy-preserving telemetry model — event counts, not code content; explicit data-collection policy; the right pattern for any org instrumenting AI workflows.
- **Financial freedom**: Prevents wasted AI-spend renewals based on sentiment; identifies the hidden curation cost that doesn't appear in any vendor's marketing.
- **Practical implementation**: Five-dimension measurement template immediately applicable; mixed-method blueprint reproducible at any org scale.

## Related Skills

- `developer-experience-and-flow/plan-limit-cognitive-thirst-trap/` — the metering psychology layer (cycle 12); HAX supplies the behavioral evidence that perception diverges from consumption
- `developer-experience-and-flow/` category: `devex-ai-era-measurement-framework/`, `devexcompass-*` (120+ metric navigation), `core-peripheral-developer-agent-usage/`, `agentic-coding-production-characterization/`
- `behavioral-psychology-and-nudging/automation-bias-trust-calibration-nudge/` — trust perception vs calibrated trust
- `ai-agents-and-workflows/` verification-bottleneck skills — the editing inversion is curation/verification load
