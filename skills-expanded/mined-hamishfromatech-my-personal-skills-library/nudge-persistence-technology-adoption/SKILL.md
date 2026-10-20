---
name: nudge-persistence-technology-adoption
description: Framework for designing nudges whose effects persist after the nudge stops, by triggering durable technology adoption rather than fragile habit formation. Use when designing behavioral interventions for long-term impact, evaluating nudge persistence, choosing between technology-adoption and habit-formation pathways, or predicting whether a nudge's effects will survive treatment cessation. NOT for one-shot nudge design or short-term behavior change without a persistence requirement.
---

# Nudge Persistence: Technology Adoption vs Habit Formation

## Overview
A landmark study of 38 natural field experiments (Brandon, Ferraro, List, Metcalfe, Price & Rundhammer, Review of Economic Studies 2026) reveals that fully half of energy-consumption reductions from a widely deployed social-comparison nudge persist after the nudge ends — and this persistence is driven by technology adoption (e.g., energy-efficient appliances, thermostat reprogramming), not by habit formation. This decomposition has profound implications for designing nudges intended to create lasting change.

## When to Use
- Designing nudges where post-treatment persistence is a requirement (health, sustainability, finance)
- Evaluating whether an existing nudge's effects will survive treatment cessation
- Choosing between "install a durable technology" and "repeat the cue" intervention pathways
- Estimating long-term social impact of behavioral interventions
- Designing A-Tech product features that aim for durable behavior change (onboarding, adoption nudges)
- NOT for one-shot nudge design where only immediate compliance matters
- NOT for nudges where the treatment cannot be discontinued (no persistence question)

## Core Process / Workflow

### 1. Persistence Diagnosis
Before designing a nudge, classify the target behavior on the persistence spectrum:

| Pathway | Mechanism | Persistence after nudge ends | Example |
|---|---|---|---|
| **Technology adoption** | Nudge triggers purchase/installation of a durable artifact that changes the default operating state | High — the technology remains after the nudge stops | Buying LED bulbs, installing smart thermostat, enabling auto-enroll |
| **Habit formation** | Nudge creates a cue-routine-reward loop that sustains behavior through repetition | Low–moderate — decays gradually, proportional to treatment duration | Turning off lights, shorter showers |
| **Pure attention** | Nudge only raises salience at the moment of choice | Near-zero — vanishes when the nudge is removed | Default formatting, one-time reminders |

### 2. Technology-Adoption Nudge Design
To maximize persistence, design the nudge to trigger a durable technology or configuration change:

1. **Identify a durable artifact** the target behavior depends on (device, setting, enrollment, structural change)
2. **Make the nudge lower the activation energy** for acquiring/configuring that artifact (friction reduction, social proof of adoption, default enrollment)
3. **Time the nudge to a transition window** (move-in, onboarding, renewal) when the cost of change is lowest and the benefit horizon is longest
4. **Measure the artifact installation rate**, not just the immediate behavior change — the artifact is the persistence carrier

### 3. Persistence Estimation
Use the Brandon et al. findings as a benchmark:
- Expect ~50% of the treatment effect to persist if the behavior has a technology-adoption channel
- Persistence is "consonant with" the technology-adoption channel: when the initial resident moves out (discontinuing treatment for the home), the persistent portion remains in the home, not with the person
- For pure habit-formation channels, expect gradual decay proportional to treatment duration (longer treatment → slower decay)

### 4. Research Design for Persistence
To measure persistence cleanly:
- Discontinue treatment for a subset of treated units (resident move-out is a natural discontinuation)
- Compare post-treatment behavior of discontinued units to never-treated controls
- Decompose the persistent effect: is it because a durable technology remains, or because a habit was formed?
- Isolate the technology channel by comparing homes where the resident changed vs. homes where the resident stayed

## References
- See [references/nudge-persistence-evidence-base.md](references/nudge-persistence-evidence-base.md) for the full evidence base, including the Brandon et al. (2026) study design, the Becker-Murphy rational addiction framework, and implications for intervention design.