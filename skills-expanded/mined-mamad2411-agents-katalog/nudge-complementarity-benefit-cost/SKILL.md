---
name: nudge-complementarity-benefit-cost
description: Applies the Yokohama natural field experiments (Nishihata, Kobayashi & Ishikawa, RIETI Discussion Paper 26-E-023, March 2026) on nudging automatic debit registration for property tax — where a benefit-enhancing nudge (flyer) and a cost-reducing nudge (owner code) each moved adoption 2.7–2.8pp alone but 8.8pp together (super-additive), while a cosmetic envelope redesign moved nothing — as the decision rule for pairing nudges. Use when [designing multi-component onboarding or adoption nudges for developer tools or AI products, deciding whether to bundle a motivation message with a friction reducer, diagnosing why a nudge campaign underperformed its sum-of-parts forecast, or setting A/B test budgets across nudge components]. NOT for [payment collection policy design or tax policy per se, manipulative engagement-farming, or single-component microcopy tweaks where complementarity is irrelevant].
---

# Nudge Complementarity: Benefit × Cost Pairing

## Overview
Two natural field experiments in Yokohama (2020, 2021; N=3,184 and N=7,621 new property taxpayers) tested nudges to adopt automatic debit for tax payments — a behavior with persistent returns (pay once, never decide again) and no repeated-reminder cost. The striking result is structural: a benefit-enhancing nudge and a cost-reducing nudge are SUPER-ADDITIVE (8.8pp combined vs 2.7 + 2.8pp separately), while a cosmetic redesign (nudge envelope) did nothing. Most nudge bundles in the literature are tested additively; this is field evidence that the right PAIRING beats the right message.

## The Evidence Base
- **Nishihata, Kobayashi & Ishikawa** — "Nudging Automatic Debit for Property Tax: Evidence from two natural field experiments," RIETI DP 26-E-023, March 2026. With Behavioural Insights Team cooperation; Yokohama City, Japan (new property taxpayers).
- **Exp 1 (n=3,184):** nudge flyer + owner code vs standard flyer vs no mail. Combined intervention: +8.8pp adoption (1% level). Standard flyer alone +7.3pp vs no mail.
- **Exp 2 (n=7,621) — the factorial that isolates components:** nudge flyer alone +2.7pp; owner code alone +2.8pp; nudge envelope ≈ 0 (ns). Combined exceeds the sum of parts — complementarity confirmed.
- **No downstream effect:** adoption rose but on-time payment rates did NOT improve within the observation window (baseline delinquency low; or the nudge converted already-compliant taxpayers — selection caveat).
- **Theoretical frame (authors' own):** a benefit-enhancing intervention raises perceived benefits by εᵦ; a cost-reducing one lowers perceived costs by ε𝒸. Application is a threshold rule: apply iff B − C > 0. If the density of latent utility is DECREASING around the decision threshold (true when baseline take-up is low, here ~8.4%), the cross-partial ∂²Pr/∂εᵦ∂ε𝒸 > 0 — complementarity emerges from the shape of the population near the threshold, even when components enter additively in utility.
- **Mechanism reading:** the flyer raises perceived benefit ("avoid penalty," deadline salience); the owner code removes a real procedural cost (no need to hunt for the code from prior mail). When either is absent, the marginal impact of the other is limited; both together move people across the threshold. Complementarity is most likely when baseline take-up is LOW (mass of the distribution sits left of the threshold).

## Core Findings (the three laws)
1. **Pair a benefit nudge with a cost nudge.** Motivation alone moves the willing-but-frustrated; friction removal alone moves the already-motivated; together they cross thresholds neither crosses alone. Expect super-additivity when baseline adoption is low.
2. **Cosmetic nudge ≈ 0 when open-rate is already high.** Official tax mailings are opened regardless of envelope design — decoration can't act on attention that isn't the binding constraint. Diagnose which constraint binds before spending design budget.
3. **Adoption ≠ outcome improvement.** Take-up of the persistent-convenience nudge did not improve on-time payment within the window — because it mostly converted already-compliant taxpayers. Measure the downstream outcome, not just the adoption metric; know who your nudge actually converts.

## When to Use
- Onboarding flows for developer tools / AI products (docs link + quickstart = benefit + cost pairing).
- Diagnosing flat A/B results: was the benefit message wasted on a friction-bound population, or the friction fix wasted on an attention-bound one?
- Planning multi-arm experiments: factorial designs over benefit × cost components beat sequential single-arm tests.
- Any "persistent decision" nudge (autopay, auto-update, default settings, recurring backups).

## NOT For
- One-shot persuasion where no persistent behavior is at stake.
- Situations with high baseline adoption (complementarity condition fails — mass of distribution right of threshold).
- Envelope/cosmetic spend when open-rates are already high.

## Core Process / Workflow
1. **Diagnose the binding constraint first.** Is the audience benefit-aware but friction-blocked, or friction-free but unconvinced? Survey or funnel data: open rates (attention), completion rates (friction), benefit-belief measures.
2. **Design the factorial.** Arms: control / benefit-only / cost-removal-only / benefit+cost-removal. The interaction term is the deliverable — the sum-of-parts is a hypothesis, not a plan.
3. **Apply the complementarity screen.** If baseline take-up < ~10%, expect super-additivity and budget accordingly; if high, components act additively and bundling buys little.
4. **Instrument the true outcome.** Track the downstream behavior (on-time payment analog: retention, renewal, deployment), not just registration.
5. **Watch the selection caveat.** Rising adoption can be a compositional shift (new adopters were already compliant) rather than outcome improvement; segment outcomes by prior behavior.
6. **Pre-commit the stop rule.** If the interaction term is null after adequate power, ship the single most cost-effective component — don't bundle for bundling's sake.

## A-Tech Alignment
- **Open source:** replicable via any A/B tooling; the factorial design is the open science pattern.
- **Privacy:** neutral here — flagged as N/A to avoid a fake alignment claim.
- **Financial freedom:** automatic debit = the Kiyosaki "pay yourself first" pattern in tax administration; the same complementarity applies to auto-invest defaults and AI-subscription vs owned-silicon decisions.
- **Practical:** the benefit×cost factorial template is a one-page experiment design any product team can run Monday morning; the "diagnose-then-pair" rule kills budget-wasting cosmetic A/B tests.

## References
- Pairs with: `engagement-gated-nudge-effectiveness-2026` (the ITT-vs-complier gate), `belief-profile-targeting-rct` (friction-type → intervention-type matching — the diagnostic layer this study's factorial verifies), `nudge-effectiveness-reality-check` (small-effects calibration), `reminder-wtp-information-penalty` (what happens when you bundle the WRONG thing — content into a nudge), `implementation-intentions-trust-ladder` (persistent-decision design).