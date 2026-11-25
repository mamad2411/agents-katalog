---
name: social-learning-ecology-diffusion
description: Applies Veltri & Acerbi (Behavioural Public Policy, Sept 2 2026, open access, agent-based model of 400 agents, 150 steps, 100 paired replications, code on OSF) — an identical seeding campaign stalls under conformist majorities, drifts under prestige-biased and random copying, and cascades under payoff-biased learning; four canonical social-learning strategies (conformist / prestige-biased / payoff-biased / random) become a diagnostic layer that predicts whether any intervention, launch, or community behavior will spread. Use when [planning a launch or growth campaign whose success depends on peer copying, diagnosing why an identical initiative worked in one community and stalled in another, designing behavior-change products or documentation-encouragement campaigns, or briefing on why intervention effect sizes are modest at scale]. NOT for [individual-level choice-architecture design — use nudge-theory-choice-architecture — or content-calendar tactics with no social-diffusion component].
---

# Social-Learning Ecology: Why Identical Interventions Stall, Drift, or Cascade

## The problem with evaluating interventions as private transactions

Behavioural interventions almost never land on isolated individuals. They land in communities where people watch, discuss, and copy one another — and whether an intervention takes off can depend **less on its content than on how the people around it learn from each other**. Veltri & Acerbi's open-access paper in Behavioural Public Policy (Sept 2, 2026) formalizes this with a deliberately minimal agent-based model: a population of 400 simulated individuals repeatedly deciding whether to adopt a behavior by observing others. Every simulation compares two identical worlds: a control arm seeded at 5% adoption and a treatment arm seeded to 25%. The seeding is the *entire* intervention; everything after comes from social learning.

The measured gap between the two arms over time — the "lift" — meets four different fates depending on one variable nobody controls in a field deployment: **what kind of copiers the population is made of**.

## The four canonical social-learning strategies

Decades of cultural-evolution research show people deploy rules of thumb about when and whom to imitate:

| Strategy | Rule | In the model |
|---|---|---|
| **Conformist** | Copy whatever the majority does — a behavior must feel common before joining | **Stalls.** Even 25% adoption sits below the majority threshold; both arms collapse back to zero and the campaign leaves no trace |
| **Prestige-biased** | Copy high-status or respected individuals | **Drifts, slowly.** Preserves a solid gap — *provided prestige actually tracks who benefits from the behavior* |
| **Payoff-biased** | Copy whoever seems to be doing well | **Cascades** — in both arms, saturating the whole system |
| **Random copiers** | Imitate a randomly encountered peer | **Drifts.** No directional force; the head start largely persists and is the arm that preserves the largest residual advantage |

## The findings that rewrite evaluation practice

**1. Real populations are mixtures, and mixtures matter.** No community is all-conformist or all-payoff-chaser. Simulating mixed ecologies (one rule at 70%, others sharing 30%) produces the sharpest result: **conformist-dominant mixtures still stall even when followed ten times longer** — a 30% minority of other learners cannot push the population across the majority threshold. Payoff-dominant mixtures saturate in both arms. In between: prestige-dominant mixtures climb to high adoption in both arms leaving only modest final lift (93% vs 90%); random-dominant mixtures preserve the largest residual advantage (78% vs 69%) though the control gradually catches up.

**2. The payoff trap: success erases its own evidence.** In payoff-driven ecologies the intervention clearly *works* — the treated population reaches high adoption much sooner — but because the behavior is visibly rewarding, the control arm eventually catches up. Measure at the endpoint and the trial reports a null. The intervention **changed the timing of diffusion rather than its eventual reach**, and an evaluation that only looks at the endpoint cannot tell the difference. This is a direct mechanism-level explanation for why scaled intervention effects (government nudge units, workplace AI adoption) look smaller than the academic literature promised.

**3. There is a sweet spot.** Final lift peaks when roughly **20% of the population is payoff-biased** — large enough to move the system, small enough not to saturate it — and collapses again by 30%. The measured "effect" of an intervention is largest where the social system leaves it room to matter: conformist populations near a tipping point, or payoff signals that are weak or noisy.

## Design rules (diagnose the learning ecology before choosing the seed)

- **Conformist-heavy settings:** diagnose local adoption thresholds; either seed *above* the threshold or change what people perceive the majority to be doing (perceived-majority framing is itself a design surface).
- **Prestige-relevant settings:** recruit demonstrators who are credible *in the eyes of the community* — not generic influencers; prestige must track who benefits.
- **Payoff-driven settings:** make good outcomes visible and attributable; expect early acceleration rather than a permanent gap, and measure at matched *time-since-seeding*, not matched calendar end.
- **Weakly structured settings:** broad seeding beats narrow targeting.
- **Ethics:** amplifying prestige or payoff cues means deciding whose status gets amplified — apply the transparency norms of the boosting tradition.

## Applications for A-Tech and open source

- **Open-source adoption campaigns:** a tool launch seeding 25% of a community where the majority copies only when things feel mainstream will read as a failure at week 12 even though nothing was wrong. Diagnose the ecology first; consider threshold-targeting (see the stem-cell donation dropout nudge for commitment-moment targeting) or visible-payoff showcases (real adoption numbers, testimonials) when the audience is payoff-biased.
- **Behavior-change products:** the same intervention shipped to two cohorts can legitimately produce stall vs cascade — instrument *who learns from whom*, not just aggregate retention.
- **Content strategy:** word-of-mouth for videos/newsletters follows the same four rules; a launch that "worked in one niche and not another" is usually a learning-ecology mismatch, not a content-quality difference.
- **Evaluation honesty:** for any growth or behavior experiment, pre-register *when* you measure and whether you expect timing-vs-reach effects (the payoff trap).

## Honest caveats

- Proof-of-concept model, deliberately stylized — not a calibrated forecast. Parameters (400 agents, 150 steps) chosen for tractability.
- The four strategies are canonical simplifications; real learners blend rules and rules may vary by domain within one person.
- No empirical calibration of the payoff-noise distributions; the 20%-payoff-biased sweet spot is a model result, not a measured constant.
- Cultural-evolution framing is contested by some social psychologists; treat as a meso-level design layer between individual choice architecture and system-level change (the authors' own i-frame/s-frame positioning).

## Pairs with

`nudge-persistence-technology-adoption` (both explain why scaled effects look smaller than trials: persistence channel vs diffusion-timing), `nudge-effectiveness-reality-check` (the scale-fidelity gap this helps explain), `engagement-gated-nudge-effectiveness-2026` (individual-level gate; this adds the population-level gate), `community-open-source-flywheel` skills, `stem-cell-donation-dropout-nudge` (commitment-moment targeting as the conformist-threshold tool), `ai-assistance-distributional-inversion` (who benefits from universal AI access — this skill adds *whether* adoption even spreads to them).

## A-Tech alignment

- **Open source:** model code openly available on OSF — the diagnostic simulation is reproducible and the four-strategy taxonomy is directly teachable.
- **Privacy:** behavioral targeting for diffusion must stay aggregate/perceived-majority-level; no individual learning-style profiling without consent (flagged as an ethics rule above).
- **Financial freedom:** explains why community-led growth (cheap, slow, prestige-and-payoff dependent) outperforms paid acquisition in payoff-visible domains — and why measuring at the wrong horizon makes good strategies look bad.
- **Practical:** one diagnostic question ("what kind of copiers is this community?") reframes launch planning, campaign evaluation, and community-design reviews.