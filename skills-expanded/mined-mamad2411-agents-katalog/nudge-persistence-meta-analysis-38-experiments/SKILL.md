---
name: nudge-persistence-meta-analysis-38-experiments
description: Applies Brandon et al. (Review of Economic Studies, Jan 2026) — the first formalized persistence decomposition across 38 natural field experiments — as the PERSISTENCE-DECOMPOSITION pattern, upgrading the library's 50%-persists-via-technology finding into a three-pathway diagnostic (habit formation, technology adoption, inattention) with policy-relevant persistence ratios. Use when designing long-horizon behavior-change interventions, estimating post-treatment persistence, or allocating nudges vs structural interventions.
---

# Nudge Persistence Meta-Analysis — 38 Natural Field Experiments

## Overview
Brandon, Ferraro, List, Metcalfe, Price & Rundhammer (Review of Economic Studies, Jan 31, 2026) formalize how to *measure* nudge persistence — not just that it exists — using resident move-out as a natural discontinuation instrument across 38 experiments, isolating the technology-adoption channel from habit formation.

## When to Use
- Designing behavioral interventions where the effect must outlive the nudge (energy, health, finance, product adoption)
- Choosing between repeated-cue nudges and one-shot structural interventions on persistence grounds
- Writing long-term impact evaluations that need a defensible persistence ratio
- NOT for: session-level attention effects (use attention-stock skills), or for claiming universal 50% persistence outside technology-channel contexts

## Core Process / Workflow

### The persistence-decomposition pattern
1. **The mechanism question**: persistence is not one thing. Two candidate channels produce identical short-run effects with different long-run profiles —
   - **Habit formation**: behavior persists because the person changed (attention/consumption stocks)
   - **Technology adoption**: behavior persists because the *home* changed (efficient appliances, thermostat reprogramming) — treatment effects "discontinue for the home" when the treated resident moves out
2. **The natural experiment**: comparing treatment vs control homes *after* the initial resident moves discontinues the treatment — isolating what sticks to the dwelling vs the person.
3. **The headline finding**: fully **half of energy-consumption reductions persist in the home after treatment ends**, consonant with the technology-adoption channel. Persistence is a property of artifacts, not willpower.

### Design workflow
1. Classify your intended mechanism first: does the intervention create a durable artifact (technology/config change) or rely on repeated cues (habit)?
2. Estimate the persistence ratio for the pathway you chose (≈50% benchmark for technology-channel; gradual decay proportional to treatment duration for habit-channel)
3. Instrument the discontinuation event (move-out, account closure, subscription lapse) to decompose person-effects from artifact-effects
4. Budget the intervention as artifact cost + nudge cost — not nudge cost alone
5. Report persistence alongside effect size; a smaller effect that persists can dominate a larger effect that decays

## References
- See [references/persistence-decomposition-evidence.md](references/persistence-decomposition-evidence.md) for the full study design, the complementarities with `nudge-persistence-technology-adoption`, and caveats.

### Pairs with
`nudge-persistence-technology-adoption` (the Jan 2026 sibling — this skill is the formalization + diagnostic upgrade), `attention-stock-nudge-scheduling` (the within-treatment dynamics), `nudge-effectiveness-reality-check`, `llm-personalized-nudge-friction-boundary`, `habit-mediation-systemchange-magic`, `social-learning-ecology-diffusion` (both explain scaled-effect shortfall).

## A-Tech Alignment
- **Open source:** persistence-via-artifact is the open-source posture — durable tools beat repeated reminders.
- **Privacy:** artifact-based persistence needs less behavioral telemetry than habit-tracking designs.
- **Financial freedom:** cost-avoidance nudges that install a durable config (e.g., autopay, rate caps) keep paying after the campaign ends.
- **Practical:** the move-out instrument is replicable in any product with account churn data.

## Honesty Caveats
- Energy-consumption domain (home energy reports lineage); the 50% persistence is *this* dataset's technology-share, not a universal constant.
- Move-out-based identification assumes non-selective move-out; the authors address selection but residual heterogeneity remains.
- Habit vs technology decomposition is identification-dependent — other unmeasured channels (learning, social spillover) are not fully excluded.