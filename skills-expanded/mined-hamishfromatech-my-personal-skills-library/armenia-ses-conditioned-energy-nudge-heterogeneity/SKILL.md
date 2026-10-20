---
name: armenia-ses-conditioned-energy-nudge-heterogeneity
description: Applies "Who Responds to Intermittent Energy Nudges? Heterogeneity by Socioeconomic Status and Female Education in Armenia" (Sargsyan, Turdaliev & van Koten, CERGE-EI WP 823, Sept 2026; Yerevan RCT, 291 households, 20-month panel) as the SES-CONDITIONED-COST-SALIENCE pattern — adding monetary cost information to peer-comparison energy reports is NOT a neutral enhancement: it flips response direction by subgroup (high-SES households show a significant +20.8 kWh differential increase under cost-added reports; tertiary-educated-female households show significant conservation; low-baseline households boomarang upward; electric-heating households conserve strongly), and effects persist into pause months for some groups only. Use when designing segmented feedback programs, auditing nudge campaigns for backfire segments, or writing heterogeneity-of-treatment-effect content. NOT for [average-treatment-effect reporting (the finding is that averages mask the structure), tax or price-policy evaluation (the intervention is information-only), or non-energy domains without re-instantiation care].
---

# SES-Conditioned Cost Salience: The Same Nudge, Opposite Directions

## Overview
Sargsyan, Turdaliev & van Koten (CERGE-EI Working Paper 823, Sept 2026) extend the Armenia/Yerevan intermittent-reporting RCT lineage with the heterogeneity analysis that turns a modest average effect into a design principle. Three arms — control, **CI** (peer consumption comparison), **CCI** (the same peer comparisons **plus monetary cost**) — across a 20-month panel with two report-delivery phases separated by an 8-month pause. Pooled treatment effects are small and insignificant; the structure is entirely in the interactions: **CCI's high-SES interaction is significantly positive during delivery (+20.8 kWh, p=0.045 ≈ 9.8% of baseline consumption)** while the CI high-SES interaction is negative — adding money flips the response for high-SES households. **Tertiary-educated-female households show consistent conservation** (all four interactions negative; strongest −31.8 kWh under CCI delivery, p=0.007 ≈ 14.9%). **Low-baseline households boomarang upward** (+30.9 kWh under CCI delivery, p=0.003 ≈ 14.5%). **Electric-heating households conserve massively** (−47.1 kWh CI, −90.0 kWh CCI during delivery ≈ 22–42% of baseline). Persistence is also heterogeneous: electric-heating effects persist into pause months; high-SES CCI increases attenuate.

## The Evidence Base
- **Design:** Yerevan RCT; 291 households (98 control / 97 CI / 96 CCI) randomized at household level; 5,334 household-month observations after exclusions; PCA-based SES index (9 durable-asset/dwelling inputs, validated against income at p<0.01); household + calendar-month fixed effects; household-clustered SEs.
- **Context:** post-Soviet transition economy; increasing-block tariff where crossing a threshold raises the tariff on ALL consumption; day/night tariffs; a deliberately WEIRD-complement sample (the high-income-country evidence base doesn't travel).
- **Key interactions (Table 6):** CI×high-SES delivery −15.6 (ns) vs CCI×high-SES delivery **+20.8** (p=.045); CCI×FemEdu delivery **−31.8** (p=.007); CCI×low-baseline delivery **+30.9** (p=.003); CI×high-baseline delivery −70.4 (p=.006); electric-heating cells −47.1 to −90.0 (all significant).
- **Mechanism interpretation:** cost salience is not uniform salience — for budget-constrained households the bill is a salient budget item; for high-SES households the same amount may be too small to trigger conservation, and the cost frame can change how the peer comparison is interpreted (consistency with Sudarshan 2017: monetary framing can eliminate the nudge effect).

## Core Findings (the salience-flip pattern)
1. **Cost information changes the message, not just its salience.** The CCI arm is not "CI plus a nudge" — it is a different treatment whose direction depends on who receives it. "Not a neutral add-on" is the paper's own framing and the citable rule.
2. **Average effects hide directional reversals.** The pooled CI/CCI effects are statistically null; every actionable pattern is an interaction. Segmentation is not an enhancement of nudge design — it is the design.
3. **Four targeting axes, four directions:** high-SES (flips positive under CCI), tertiary-educated female (conserves, strongest under CCI), low-baseline (boomarangs), electric-heating (conserves hugely). A one-size program would mis-serve at least two of the four.
4. **Persistence is subgroup-specific.** Pause-month decay is not uniform — conservation-oriented groups attenuate, upward-response groups also attenuate; intermittent delivery redistributes effects, not just their magnitude.

## When to Use
- Designing any segmented feedback program (energy, spend, health, adoption): build the interaction table before launch; average effects are the wrong deliverable.
- Auditing existing nudge campaigns for backfire segments — low-baseline and high-SES-under-CCI analogues are the recurring backfire profiles.
- Writing heterogeneity-of-treatment-effect or post-WEIRD evidence content: the two-games frame (average vs subgroup) generalizes.

## NOT For
- Average-treatment-effect reporting or meta-analytic pooling that assumes homogeneous effects.
- Price or tax policy evaluation — the manipulation is information design under a fixed tariff.
- Non-energy domains without re-instantiation care: the SES index, the IBT tariff, and the heating moderator are domain-structural.

## Core Process / Workflow
1. **Pre-specify the heterogeneity axes.** SES (asset-based PCA when income is noisy), decision-maker education, baseline-consumption quantiles, technology/heating moderators — the pre-registered set in the paper.
2. **Run the interaction model, not the main-effects model.** Treatment-arm × phase × subgroup; cluster at the household; interpret with magnitude + sign-consistency, not per-cell p-values alone.
3. **Treat cost salience as a design variable.** Decide *whether* to include monetary framing per segment, not globally — it flips direction for identifiable groups.
4. **Plan for pause months.** Persistence differs by subgroup; schedule intermittent delivery against the groups whose effects persist and re-touch those whose effects decay.
5. **Report distributional consequences.** Boomerang segments are a distributional finding, not a failure — the program's welfare effect is the sum of directions.

## A-Tech Alignment
- **Practical:** the four-axis targeting framework is directly reusable for any A-Tech feedback-loop product or campaign design; the "not a neutral add-on" rule is a one-line design law.
- **Behavioral honesty:** a large-N field RCT (not a lab study) that operationalizes backfire-by-segment — the evidence-based complement to the library's reactance-backfire and nudge-effectiveness families.
- **Financial freedom:** the female-education conservation result is a concrete, measurable empowerment datapoint for wealth-behavior content.

## Honesty Caveats
- 291 households, single city (Yerevan, 98.9% Armenian); transition-economy external validity unknown.
- Energy domain with an IBT tariff; the cost-salience flip depends on threshold crossing salience.
- Interaction estimates in three of four FemEdu cells are directional (imprecise); only the CCI-delivery cell is significant.
- Attrition/exclusion protocol (251 high-use + 35 missing-month exclusions) is documented but reduces the balanced panel.

## Pairs-with
`nudge-history-reactance` and `vaccination-history-contingent-reactance-backfire` (history- and status-contingent backfire — different targeting variables, same design lesson), `nudge-persistence-meta-analysis-38-experiments` and `attention-stock-nudge-scheduling` (the pause-month persistence complement), `behavioral-intervention-choice-tailoring`, `cost-salience-variety-margin`, `llm-personalized-nudge-friction-boundary`, `sudarshan-monetary-framing-null` (Sudarshan 2017 as the mechanism precedent).

## References
- Sargsyan, Y., Turdaliev, S., van Koten, S. (CERGE-EI Working Paper 823, published Sept 9, 2026; dated 24.08.2026), "Who Responds to Intermittent Energy Nudges? Heterogeneity by Socioeconomic Status and Female Education in Armenia."
- Companion: Turdaliev, Sargsyan & van Koten (2026), Environmental and Resource Economics 89(1) — the average-effect companion paper.
- Sudarshan (2017, JEBO) — nudges + monetary incentives elimination; Allcott (2011), Ayres et al. (2013) baselines.

*Created: 2026-09-17 (Cycle 28, Run 3) — A-Tech Research Division*