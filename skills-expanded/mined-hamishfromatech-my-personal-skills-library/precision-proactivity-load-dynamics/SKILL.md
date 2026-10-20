---
name: precision-proactivity-load-dynamics
description: Applies the Precision Proactivity study (Lepine, Kim, Mishkin & Beane, UC Santa Barbara/KAIST, arXiv:2505.10742v3, TOCHI 2026 — 34 finance professionals, 1,178 participant-subtask observations on GPT-4o) as the LOAD-DYNAMICS framework — the first transcript-based operationalization of intrinsic and extraneous cognitive load in real AI-assisted knowledge work, finding that extraneous load harms output quality ~3× more than intrinsic task complexity (β≈−0.48 vs −0.15), that load is path-dependent (within-speaker persistence β≈0.17–0.27 across turns with near-zero response-to-prompt spillover), and that model-initiated task switching is the single strongest negative predictor of quality (β≈−0.27). Use when [designing or auditing proactive AI assistants, diagnosing why AI-assisted output quality degrades across long sessions, setting interaction-design rules that constrain assistant scope expansion, or briefing teams on cognitive-load-aware AI UX]. NOT for [developer-specific flow-state design — use developer-experience-flow-state — or general cognitive-load fundamentals — use cognitive-load].
---

# Precision Proactivity: Load Dynamics in Real AI-Assisted Work

## Overview
The first framework that measures cognitive load *from transcripts* of real professionals doing real work with a real model (GPT-4o) — replacing self-report with theory-grounded computational indicators (task decomposition + Finance Knowledge Graph + rolling contextual memory). It converts "AI interactions can feel cluttered" into measurable, design-actionable dynamics.

## When to Use
- Designing proactive assistants (coding, finance, legal, research) where response scope and initiative matter
- Diagnosing session-level quality decay in AI-assisted work ("the report got worse as the chat got longer")
- Setting interaction-design rules: when should the model elaborate vs. stay in scope
- NOT for: IDE/flow engineering (use `flow-state-engineering-for-coding-tools`); CLT instruction design (use `cognitive-load`)

## Core Process / Workflow

### The measurement architecture (three layers)
1. **Intrinsic load (ICL)** = task-inherent complexity: element interactivity across subtasks, phase spread, dependency debt — grounded in a task decomposition of 101 subtasks and a domain knowledge graph.
2. **Extraneous load (EL)** = avoidable working-memory cost of compensating for conversational incoherence, operationalized as prompt-anchored subtask coherence (PSC) computed from the transcript plus three behavioral markers: **task switching** (model introduces subtasks the user didn't ask about), **information sprawl** (semantic drift beyond the prompt's conceptual neighborhood), **truncation** (user-specified subtasks dropped and re-raised).
3. **AI-generated content usage (AIGCU)** = how much model content actually lands in the final deliverable (capacitated semantic matching to the report).

### The five headline numbers
| Finding | Value |
|---|---|
| AIGCU → output quality | β ≈ +0.32–0.35 (p<.01) — using AI helps |
| Extraneous load → quality | β ≈ −0.47 to −0.49 (p<.01) — ~3× intrinsic (−0.15) |
| Task switching (model-initiated) → quality | β ≈ −0.27 (p<.01), strongest single predictor |
| Within-speaker load persistence | β ≈ 0.17 (responses) / 0.27 (prompts) across turns |
| Response-to-prompt spillover | ≈ 0 (p=0.67) — load does not flow back; trajectories self-sustain |

### The additive-not-moderating result (the subtle one)
AIGCU × EL and AIGCU × ICL interactions are consistently **null** — AI usage does not buffer load, and load does not gate the benefit of AI content. Effects are **additive and opposing**. Implication: adding more AI content cannot compensate for a cluttered interaction; you must reduce extraneous load directly.

### The expertise asymmetry (the design-critical one)
- Less experienced professionals: larger extraneous-load penalty (direct EL→quality ≈ −0.91 at −1SD experience vs −0.42 at +1SD) AND larger per-unit quality gain from AI content (b-path ≈ 0.62 vs 0.19).
- More experienced professionals: increase AI uptake *most* sharply as load rises (a-path ≈ 0.90 vs 0.31) — their schemas let them mine clutter.
- **The dissociation:** those who would benefit most from load-dampening (novices) are not the ones who ramp uptake under load (experts). Calibrate interventions by expertise, not uniformly.

### The RLHF explanation (why this keeps happening)
RLHF rewards *relevance to the current prompt* — so the model mirrors and amplifies the user's organizational structure rather than pruning it. The model never says "let's clean this up." Combined with users who don't prune in response to model output (null spillover), this creates a **self-reinforcing clutter loop**: prompt complexity accumulates, the model accommodates, no corrective signal fires on either side.

### The precision-proactivity design playbook (three levers)
1. **Detect and dampen entrenched high-load trajectories.** Treat high-load prompts as signals for structural support, not maximal elaboration. Segment, sequence, simplify — and model expertise (novices need the dampening most; experts would experience uniform simplification as itself extraneous load — the expertise-reversal effect).
2. **Constrain system-initiated scope expansion.** Maintain a *subtask focus stack*; classify candidate response content against the user's active subtask set; flag out-of-scope content; when sprawl exceeds threshold, shift from elaboration mode to boundary-signaling mode. Optionally elicit scope explicitly before generating.
3. **Structured disclosure over monolithic responses.** Separate core in-scope content from optional elaborations (expandable sections, inline annotations, branching) — depth stays available but never imposed; navigation choices double as preference signals.

## References
- Nearest neighbors: `context-switching-taxonomy-ai-assisted-work` (the interruption/friction taxonomy this quantifies), `cognitive-friction-reduction`, `cognitive-load-reduction-ai-scaffolding`, `scaffolded-cognitive-friction`, `prompt-wait-evaluate-flow-collapse`, `llms-get-lost-in-multi-turn` (the multi-turn degradation this explains cognitively), `recalibrategpt-ai-fatigue-operators-2026` (the leader-side counterpart), `adaptive-emotion-aware-developer-ux`.
- Honesty caveats: observational (not causal) design; GPT-4o-era models; single domain (financial valuation, N=34 professionals); load measures are theory-grounded proxies, not physiological measurements; no long-term longitudinal test of schema formation.

*Sources: Lepine, B., Kim, J., Mishkin, P., & Beane, M. (2026). "Precision Proactivity: Measuring Cognitive Load in Real-World AI-Assisted Work." arXiv:2505.10742v3, accepted TOCHI 2026. Study: 34 finance professionals, complex valuation task, GPT-4o, 1,178 participant-subtask observations + 1,940-utterance dynamic panel.*