---
name: belief-profile-targeting-rct
description: Use when designing targeted behavioral interventions for job seekers or other heterogeneous populations, diagnosing which behavioral friction binds different segments, choosing between information provision vs aspiration-setting vs effort encouragement, or avoiding iatrogenic nudges.
---

# Belief-Profile Targeting: Same Nudge, Different Search Problem

**Source:** Crépon, Frot & Gaillac (CREST / France Travail / U. Geneva), "Targeting Support Using Job Seekers' Biases: A Randomized Experiment," arXiv:2608.16849 (Aug 2026; companion paper Crépon et al. 2025). Pre-registered (AEARCTR-0012218). N=52,465 French job seekers in an RCT with France Travail; belief-profile classification (pessimists/optimists) via ML prediction on prior survey waves; two intervention arms (occupational recommendation vs motivational recommendation) crossed with bias groups.

## Core Insight: Friction Type → Intervention Type

The study formalizes what most nudge design gets wrong: **people facing different frictions need different interventions, and delivering the wrong one is iatrogenic** (a nudge that works for one group reduces outcomes for another).

| Friction | Binding constraint | Right intervention | Wrong intervention |
|---|---|---|---|
| Attention allocation | Where to search | Occupational recommendations (diversify) | Motivational messages (misdirect) |
| Low aspiration / effort | How hard to try, what to aim for | Motivational messages (effort norm + wage benchmark) | Occupational diversification (adds noise to a constrained search) |

**Mechanism split (this is the transferable part):** interventions work through different channels, and you can test which one you're operating:
- **Attention activation** — the intervention lowers the cognitive threshold for acting on an existing belief (no belief change required; "learning through noticing").
- **Aspiration shift** — the intervention raises a reference point (what peers aim for), shifting effort/reservation wages without changing beliefs about the world.
- **Belief updating** — actual revision of perceived probabilities. **Most information interventions do NOT operate through this channel**, despite everyone assuming they do.

## Key Empirical Results (for calibration)

- Occupational recommendations: worked for optimists (belief-profile group) on the intended margin; on **pessimists, they worked "off-target"** — increased spontaneous applications (+90%) with lower job quality (more fixed-term contracts), not through the recommended path.
- Motivational recommendation: **+2.2pp reemployment at 12 months** for pessimists, concentrated in the low-effort subgroup (+2.9pp) and the low-reservation-wage subgroup (+5.3pp probability of a job above baseline wage); raised reservation wages 1.9% overall, 2.4% among those below the disclosed benchmark.
- **Beliefs barely moved in either arm** despite large behavioral responses — the mechanisms were attention/aspiration, not belief correction. This is the sharpest evidence against "information → belief change → behavior" as the default model.

## Design Rules (transferable)

1. **Diagnose before you nudge.** Map which friction binds each segment (attention vs aspiration vs capability) before choosing intervention type.
2. **Match the nudge to the friction, not to the population average.** A message that helps segment A can hurt segment B (psychological reactance, misdirection, wasted attention).
3. **Report both the intended-margin effect and the off-target spillover.** "It worked" is meaningless without knowing through which margin it worked.
4. **Design for iatrogenic risk.** In the RCT, delivering an occupational recommendation to a pessimist would have *worsened* job quality; the paper explicitly warns against giving motivational content to optimists.

## Application Beyond Job Search

- **Content/marketing:** choose message type by the reader's actual friction (don't send motivational content to someone who needs a decision shortcut).
- **Behavior-change products:** segment by binding constraint, not by demographics; measure off-target effects, not just the primary endpoint.
- **AI assistants/nudging systems:** the architecture applies directly — an intent-scoring agent should classify the user's binding friction (e.g., information gap vs motivation gap vs execution gap) before choosing its intervention style. Pairs with `intent-assistant-attention-steering` and `llm-iterative-nudge-personalization`.

## Cross-Links

- `engagement-gated-nudge-effectiveness-2026` — timing/engagement gates; this skill adds the *friction-type* gate
- `nudge-effectiveness-reality-check` — null-result literature this strengthens
- `mecha-nudges-for-machines` — machine-side analog (what friction binds an agent?)
- `llm-iterative-nudge-personalization` — same France/behavioral-economics lineage, personalization layer

## A-Tech Fit

- **Practical implementation:** a diagnostic-first template for any A-Tech client doing behavior-change or retention work — audit friction type before writing the intervention.
- **Financial freedom:** directly quantified ROI for the right intervention (2.2pp reemployment; ~200 extra reemployments at near-zero marginal cost from a message).
- **Open source:** the belief-profile classification method (ML prediction of bias from administrative + survey data) is replicable with open tooling.
- **Privacy:** uses administrative + survey data with IRB oversight; a caution for anyone replicating: belief prediction is sensitive — treat as consent-gated, not default.