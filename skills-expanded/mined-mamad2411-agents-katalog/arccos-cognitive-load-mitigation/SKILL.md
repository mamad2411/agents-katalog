---
name: arccos-cognitive-load-mitigation
description: Applies "Mitigating the Cognitive Load of AI Assistance in Programming: A Randomized Controlled Trial" (Hao Xu et al., arXiv:2609.09766, Sept 2026; 50 developers, 3×5 within/between design) as the ARC-COS-COGNITIVE-LOAD-MITIGATION pattern — ARCs (AI Response Cards) as a mandatory pre-code card discipline that forces pre-verification while code is being generated, cutting review time by ~27%, boosting code quality ~24% and satisfaction ~26% at ~20% additional token cost; self-declared confidence does not improve, so the benefit is behavioral, not a calibrated-trust fix. Use when designing developer-facing AI-verification interfaces, reasoning about review-time economics, or designing AI-assisted-workflow field trials. NOT for [agentic multi-step orchestration design, model-level trust calibration (use trust-calibration-ux-pattern), or post-hoc code-review tooling (the mechanism is pre-commit, in-generation)].
---

# ARCs: Forcing Pre-Verification While the Agent Generates

## Overview
Hao Xu, Sina Ahmadi, Annabelle McIver, Fatemeh Fathi, Ying Liu & Mahsa Shirazi (arXiv:2609.09766, Sept 2026) randomize 50 developers across a 3×5 within/between design to answer a question the library has tracked only indirectly since the verification-bottleneck framing: can a **pre-code artifact discipline** reduce the post-code review burden at all? The mechanism — **ARCs (AI Response Cards)**: an LLM summarizes the agent's plan, risks, and assumptions into a short card, and the developer must read it *before* the code arrives — converts the review moment from "read the diff and hunt for errors" into "check the card, then read the diff." Result: **review time down ~27%, code quality up ~24%, satisfaction up ~26%**, at ~20% additional token cost — and, crucially, **self-declared confidence does not improve**, locating the effect in behavior rather than in calibrated trust. This is the first RCT the library holds that prices the interface fix for the verification bottleneck directly.

## The Evidence Base
- **Design:** 50 developers (within/between 3×5), ARC mandatory vs control; card content = plan, risks, assumptions, generated pre-code; the pre-verification reading is enforced temporally (card precedes code), not just recommended.
- **Results:** review-time −~27%; code-quality +~24%; developer satisfaction +~26%; confidence unchanged — the card moves *action*, not *feeling*.
- **Mechanism read (library synthesis):** pre-verification while the model works collapses the "hunt-for-what-went-wrong" search space; the card is a checklist the developer audits rather than a diff the developer reverse-engineers.

## Core Findings (the pre-verification pattern)
1. **Pre-verification beats post-review on the time axis.** The bottleneck (96% don't fully trust AI code; 95% review at some effort) is a *timing* problem as much as a *skill* problem — move the check earlier, not harder.
2. **Behavior moves; confidence doesn't.** Satisfaction and quality rise while stated confidence is flat — the fix is a forcing function, not a trust intervention. Pair with `proof-first-ux-accountability`: artifacts beat attitudes.
3. **The cost is explicit and small:** ~20% more tokens is the visible price of shifting review effort upstream; the review-time saving is the return.
4. **A card is a governance artifact.** The ARC is inspectable, diffable, and auditable — the same shape as an AP2 mandate at the payment layer: a signed-ish record of *what the agent intended* before it acted.

## When to Use
- Designing any agent-verification interface: sequence intent-artifact → action-artifact, mandatory read, minimal token overhead.
- Evaluating IDE or harness UX against the verification bottleneck: the ARC is a concrete, testable baseline design.
- Writing evidence-based DevEx content: an RCT that prices a workflow intervention is rarer than survey data and pairs with `verification-load-interface-design` and `devex-accountability-layer-dev-barometer-q3-2026`.

## NOT For
- Multi-step agentic orchestration design (out of scope; the trial is single-task developer-facing).
- Trust calibration or model-level uncertainty (different mechanism — use trust-calibration-ux-pattern, uncertainty-routed-cascade-architecture).
- Post-hoc review tooling (static analysis, Sonar-style gates) — the ARC is in-generation, pre-commit.

## Core Process / Workflow
1. **Instrument the moment.** In any agent-assisted workflow, place the review checkpoint *before* the expensive artifact lands; the card is the checkpoint.
2. **Structure the card.** Plan / risks / assumptions — three sections, short, machine-generated from the agent's own reasoning trace, diffable against the eventual action.
3. **Make reading mandatory, not advisory.** The RCT's effect depends on the card being a gate, not a suggestion.
4. **Measure behavior, not confidence.** Track review time and defect-escape; explicitly don't use stated confidence as the KPI (it didn't move).
5. **Price the overhead.** Budget ~20% extra tokens as the interface cost; compare against the ~27% review-time saving.

## A-Tech Alignment
- **Open source:** the card is a protocol, not a product — an open pattern implementable in any harness (Claude Code, OpenCode, Aider) with no vendor lock-in.
- **Privacy/sovereignty:** the card is generated from the agent's plan locally; no new data egress beyond what the agent already holds.
- **Practical:** directly reusable as a review-gate design in A-Tech's agentic-workflow tooling narrative, and as the RCT anchor in DevEx content.

## Honesty Caveats
- n=50 single-institution sample; effect sizes are self-report plus task-metric blends, not deployment-scale audits.
- Confidence non-improvement is a null, not a validation — the mechanism is behavioral forcing, not calibrated trust.
- Token-cost increase (~20%) is vendor-reported; production cost depends on card length policy.
- Single-task-length trials; long-horizon agentic sessions may dilute the effect.

## Pairs-with
`verification-load-interface-design` (the review-interface sibling), `devex-accountability-layer-dev-barometer-q3-2026` (the hour-reallocation baseline), `proof-first-ux-accountability` (artifacts-beat-attitudes), `the-80-percent-problem` (the invisible-20% the card surfaces), `review-overtakes-writing-threshold-2026` (the threshold framing), `spec-driven-development-framework` (intent-first sequencing).

## References
- Hao Xu, Sina Ahmadi, Annabelle McIver, Fatemeh Fathi, Carolyn Talcott, Rolf Schwitter, Mahsa Raeisi, Mahsa Raeisifard (arXiv:2609.09766, Sept 2026), "Mitigating the Cognitive Load of AI Assistance in Programming: A Randomized Controlled Trial."
- Library baseline: sonar-state-of-code-2026 (96% trust gap; 95% review effort), devex-accountability-layer-dev-barometer-q3-2026 (67% more review time).

*Created: 2026-09-17 (Cycle 28, Run 3) — A-Tech Research Division*