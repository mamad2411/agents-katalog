---
name: nudge-cross-domain-spillover-effects
description: Framework for predicting and evaluating whether a behavioral nudge in one domain produces spillover effects in unrelated domains (e.g., a waste-sorting nudge affecting water and energy use). Based on a two-year natural field experiment in Guali Town, China. Use when designing multi-outcome nudges, estimating cross-domain spillovers for cost-effectiveness analysis, assessing whether institutional context (financial incentives, social capital) will amplify or suppress spillovers, or deciding whether to combine nudges with financial incentives. NOT for single-domain nudge design where cross-domain effects are irrelevant, and NOT for mechanical complementarities that are obvious structural links.
---

# Nudge Cross-Domain Spillover Effects

## Overview

A two-year natural field experiment (Ling, Liu & Xu, Journal of Environmental Psychology, Vol. 110, March 2026) evaluated whether a HER-type social-comparison nudge for household waste sorting — the "Home Waste-Sorting Report" (HWSR) — produced cross-domain spillover effects on water, electricity, and gas consumption in Guali Town, China. The study covered 1,788 households across 14 communities, using an opt-out design with longitudinal administrative utility data (objective behavioral measures, not self-report).

The headline finding cuts against the optimistic spillover literature: **on average, the nudge had no significant cross-domain spillover effects on water, electricity, or gas use.** But this null average masks critical heterogeneity. Positive and persistent spillovers arose in specific localized institutional contexts — communities without financial incentives for waste sorting and with low social capital. In contrast, communities with financial incentives and high social capital showed **suppressed** spillovers, consistent with the "moral licensing / external justification" mechanism: when people can attribute their waste-sorting behavior to a financial reward rather than an internalized environmental value, the behavior does not generalize to other pro-environmental domains.

This skill provides a framework for (a) diagnosing whether a planned nudge will produce cross-domain spillovers, (b) assessing the institutional context that determines whether spillovers will be positive or suppressed, (c) incorporating even small spillover effects into cost-effectiveness analysis, and (d) applying the four-mechanism taxonomy (direct moral utility, mechanical complementarities, resource competition, self-related beliefs/identity) to predict the direction and magnitude of spillovers in A-Tech product contexts.

## When to Use

- Designing a nudge in one domain and wanting to predict its effects on related or unrelated behaviors (e.g., nudging code-review compliance and wondering if it spills over to documentation habits)
- Estimating the total social benefit of a nudge intervention, including cross-domain spillovers, for cost-effectiveness analysis or ROI justification
- Assessing whether combining a nudge with financial incentives will enhance or undermine cross-domain generalization
- Evaluating whether institutional context (community social capital, existing incentive structures) will amplify or suppress spillover effects
- Deciding between a standalone nudge and a bundled intervention across multiple behavioral domains
- Reviewing a behavioral intervention program that claims "compound benefits" across multiple domains from a single nudge

## NOT for

- Single-domain nudge design where cross-domain effects are genuinely irrelevant (the target behavior has no plausible adjacent domains)
- Mechanical complementarities that are obvious structural links (e.g., a nudge to install a smart thermostat mechanically reduces electricity — that is not a spillover, it is a direct effect)
- Situations where only immediate, within-domain compliance matters and long-term generalization is out of scope
- Predicting spillovers from non-nudge interventions (taxes, regulations, mandates operate through different mechanisms)

## Core Process / Workflow

### 1. Spillover Potential Diagnosis

Before designing or evaluating a nudge for cross-domain spillover potential, classify the target behavior and its candidate spillover domains:

| Spillover Type | Mechanism | Direction | Example |
|---|---|---|---|
| **Direct moral utility** | The nudge alters the actor's moral self-concept or environmental identity, which then generalizes to other pro-social/pro-environmental behaviors | Positive (if internalized) or suppressed (if externally justified) | Waste-sorting nudge → water/energy conservation because the person now sees themselves as "someone who cares about the environment" |
| **Mechanical complementarity** | The nudged behavior and the spillover behavior share a physical or structural linkage | Positive or neutral | Sorting waste → reduced packaging purchases → less garbage volume (structural, not psychological) |
| **Resource competition** | The nudged behavior consumes resources (time, money, attention) that are then unavailable for the spillover domain | Negative | Time spent sorting waste → less time for energy-efficiency behaviors |
| **Self-related beliefs / identity** | The nudge shifts self-perception or self-efficacy beliefs that carry across domains | Positive if the nudge builds self-efficacy; negative if it triggers moral licensing | Waste-sorting success → "I am capable of environmental action" → willingness to try energy conservation |

**Key insight from the study:** The direct moral utility and self-related beliefs channels are the primary pathways for cross-domain spillovers. But whether these channels activate depends entirely on the institutional context (Step 2).

### 2. Institutional Context Assessment Framework

The study's central contribution is demonstrating that the **same nudge** produces positive spillovers in some communities and suppressed spillovers in others, depending on two institutional context variables. Apply this 2×2 assessment before predicting spillover direction:

| | **Low Social Capital** | **High Social Capital** |
|---|---|---|
| **No Financial Incentives** | **Positive spillovers (observed)** — the nudge fills a behavioral vacuum; without external rewards or strong social norms, the nudge's moral utility alteration internalizes deeply and generalizes | Ambiguous — strong social norms may substitute for the nudge's identity effect, reducing marginal spillover potential |
| **Financial Incentives Present** | Ambiguous — financial incentives may partially crowd out internalization, but low social capital means fewer alternative normative pressures | **Suppressed spillovers (observed)** — external justification dominates; actors attribute their behavior to the financial reward rather than internalized values, preventing cross-domain generalization |

**Diagnostic questions for any deployment context:**

1. **Are there financial incentives for the target behavior?** If yes, expect the external justification mechanism to suppress cross-domain spillovers. The actor's internal narrative becomes "I do this because I get paid," not "I do this because I am an environmentally responsible person."
2. **Is social capital high or low in the target community?** High social capital (dense networks, strong trust, established norms) can either substitute for the nudge's identity-building effect (reducing marginal spillovers) or reinforce it (amplifying spillovers). The study found that high social capital combined with financial incentives produced the strongest suppression.
3. **Is the nudge the primary behavioral prompt, or does it compete with other interventions?** When the nudge is the sole intervention (no incentives, weak existing norms), it has the most room to build the moral identity that drives spillovers. When it is layered onto existing incentives and norms, its identity-building capacity is diluted.
4. **What is the actor's likely causal attribution?** If actors will attribute their behavior to the nudge or incentive (external), spillovers will be suppressed. If they will attribute it to their own values (internal), spillovers are possible.

### 3. Spillover Measurement Design

The study demonstrates a gold-standard measurement approach for cross-domain spillovers. Replicate these design features:

- **Opt-out design:** Rather than opt-in (which selects motivated participants and biases spillover estimates upward), use opt-out — all households receive the HWSR unless they actively decline. This preserves external validity.
- **Longitudinal administrative data:** Use objective, time-stamped utility records (water, electricity, gas meter readings) rather than self-report. Self-report of spillover behaviors is especially vulnerable to social desirability and demand characteristics.
- **Pre-treatment baseline period:** Establish consumption baselines before the nudge to control for pre-existing differences across communities.
- **Community-level heterogeneity analysis:** Do not rely on the pooled average alone. Decompose effects by community-level institutional context (incentives, social capital) to reveal the heterogeneity that the null average conceals.
- **Persistence measurement:** Track spillover domains across the full treatment period (two years in this study) and beyond to distinguish temporary from persistent spillovers.

### 4. Cost-Effectiveness Incorporation of Spillovers

Even small cross-domain spillovers can substantially affect the cost-effectiveness calculation for a nudge intervention:

1. **Estimate the direct effect** of the nudge on the target domain (e.g., waste-sorting compliance).
2. **Estimate the spillover effect** on adjacent domains (water, electricity, gas), even if small. The study found that spillovers, where present, were modest in absolute terms but meaningful relative to the nudge's marginal cost (which is near zero for a social-comparison report).
3. **Monetize all domains** using a common metric (e.g., CO2 equivalent, monetary value of resource savings).
4. **Sum the direct + spillover benefits** and compare to the nudge's total cost. A nudge whose direct effect alone is marginally cost-effective can become clearly cost-effective when even small positive spillovers are included.
5. **Subtract negative spillovers** (resource competition effects) where applicable. If the nudged behavior consumes time or money that crowds out other pro-environmental behaviors, this offsets part of the direct benefit.

**Critical caveat:** Only incorporate positive spillovers into the cost-effectiveness case if the institutional context assessment (Step 2) predicts that spillovers will actually arise in the deployment context. Do not assume positive spillovers by default — the study's null average is the correct prior in the absence of context-specific evidence.

### 5. Financial Incentive Compatibility Check

Before combining a nudge with financial incentives, run the compatibility check:

| Check | Question | If Yes… | If No… |
|---|---|---|---|
| **Attribution crowding** | Will the incentive cause actors to attribute their behavior to the reward rather than to their own values? | Expect suppressed cross-domain spillovers. The incentive may boost the target behavior but at the cost of generalization. | Spillovers are more likely; the nudge's identity-building mechanism is intact. |
| **Incentive magnitude** | Is the incentive large enough to be the dominant motive? | Strong suppression of spillovers expected. The external justification overwhelms internal attribution. | Moderate or ambiguous effect on spillovers. |
| **Incentive framing** | Can the incentive be framed as affirming existing values rather than purchasing behavior? | Some spillover preservation possible. Framing matters: "reward for your environmental commitment" vs "payment for sorting waste." | Standard extrinsic framing; expect full suppression. |
| **Incentive removal plan** | Will the incentive be removed after a period? | If behavior persists post-removal, internalization may have occurred despite the incentive. Monitor post-incentive spillover domains. | N/A. |

## A-Tech Application Matrix

| A-Tech Product | Application |
|---|---|
| **A-Coder** | A nudge to improve code-review compliance (social comparison: "your review rate is below your team's average") could spill over to documentation habits, test-writing, or PR description quality. Apply the institutional context assessment: if the team already has financial incentives (bonuses tied to review metrics), expect suppressed spillovers — developers attribute their review behavior to the bonus, not to professional identity. If no incentives and low team cohesion, spillovers to adjacent coding habits are more likely. Measure using longitudinal git analytics (objective behavioral data), not self-report. |
| **Be Practical** | A learning-completion nudge (social comparison of module progress) could spill over to practice-exercise completion, community participation, or portfolio project quality. Check for competing incentives (certificates, gamification badges) that may crowd out internalization. Frame nudges around learner identity ("learners like you who complete modules tend to build more projects") rather than external rewards to preserve the moral utility channel. |
| **Builder's Club** | A contribution nudge (social comparison of open-source commit frequency) could spill over to documentation contributions, issue triage, or mentorship. The community's social capital is the key moderator: a tight-knit community with strong norms and no financial incentives is the highest-spillover context. A community with paid bounties and weak social ties is the lowest. Use the 2×2 institutional context framework to predict which Builder's Club sub-communities will see spillovers and which will not. |
| **Content / Channel strategy** | When evaluating whether a single nudge-based video (e.g., a social-comparison energy report explainer) can drive cross-domain interest (open-source tools, privacy habits, financial freedom content), apply the spillover framework. The nudge (video) operates on environmental identity; whether that generalizes to open-source adoption or privacy behavior depends on whether the audience attributes their interest to the video (external) or to their own values (internal). Avoid claiming compound cross-domain benefits without context-specific evidence. |

## Anti-Patterns

- **The "spillovers are guaranteed" trap:** Assuming that a successful nudge in one domain will automatically produce positive effects in adjacent domains. The study's null average is the correct prior.
- **The "financial incentives always help" trap:** Layering financial incentives onto a nudge to boost the target behavior, unaware that this suppresses the cross-domain generalization that drives long-term, multi-domain impact.
- **The "pooled average is the real effect" trap:** Reporting only the average cross-domain effect and concluding "no spillovers," when community-level heterogeneity reveals substantial positive spillovers in specific contexts.
- **The "self-report spillover" trap:** Measuring cross-domain spillovers with self-report surveys rather than objective behavioral data. Self-report of spillover behavior is doubly vulnerable to demand characteristics because participants know the nudge's intent.
- **The "ignore small spillovers" trap:** Dismissing small cross-domain effects as negligible when they may substantially shift the cost-effectiveness calculation, especially for low-cost nudge interventions.
- **The "mechanical spillover misclassification" trap:** Counting a mechanical complementarity (structural linkage) as a psychological spillover. If the effect is structural, it does not depend on institutional context and does not require the moral utility mechanism.

## Cross-References

| Skill | Relationship |
|---|---|
| `nudge-persistence-technology-adoption` | Complementary — covers whether a nudge's effects persist over time; this skill covers whether a nudge's effects generalize across domains. Persistence and spillover are the two key dimensions of nudge impact beyond the immediate target behavior. |
| `nudge-effectiveness-reality-check` | Foundational — provides the bias-corrected baseline for nudge effect sizes; this skill extends to the cross-domain question of whether effects spread beyond the target domain. |
| `behavior-change-synthesis-2026` | Umbrella — this study is one input into the broader 2026 behavior change evidence synthesis. |
| `nudge-second-order-meta-analysis-publication-bias` | Methodological kin — both address the gap between published and true nudge effects; the null spillover average in this study is consistent with the bias-corrected near-zero average effect in the meta-analysis. |
| `nudge-transparency-disclosure-effectiveness` | Adjacent — transparency about the nudge's purpose may affect the attribution mechanism that drives (or suppresses) cross-domain spillovers. |

## References

- See [references/evidence-base.md](references/evidence-base.md) for the full study extraction: design, methodology, results by domain and community type, the four-mechanism taxonomy, limitations, and A-Tech alignment details.
**UPDATE pointer:** the Guali Town utility-telemetry spillover test (Ling, Liu & Xu, JEP vol. 110, March 2026 — no average spillovers to water/electricity/gas despite +27–34% target effects; positive persistent spillovers only in low-incentive, low-social-capital communities) is extracted in [addendum-guali-spillover-jep-2026.md](addendum-guali-spillover-jep-2026.md).
