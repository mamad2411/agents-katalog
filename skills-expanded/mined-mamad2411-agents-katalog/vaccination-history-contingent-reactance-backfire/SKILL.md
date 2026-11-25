---
name: vaccination-history-contingent-reactance-backfire
description: Applies the community- and web-based randomized trial of electronic nudges for influenza-vaccination willingness among older Chinese adults (Yang, Hu, Huang, Wang, Zhang, Jiang, Pang, Fu, Chen & Guo, Peking University; npj Digital Medicine, published Aug 18, 2026; N=2,167, eight parallel arms, seven nudge methods + control, Lanzhou New Area Gansu) as the HISTORY-CONTINGENT-REACTANCE-BACKFIRE pattern — the first published evidence that nudges applied to already-behaved recipients reduce willingness (psychological reactance), while video nudges lift willingness mainly in the unvaccinated and side-effect-worried. Use when [designing multi-segment nudge programs, auditing nudge campaigns for backfire segments, deciding when NOT to nudge, or tailoring intervention delivery by behavioral history]. NOT for [nudge scheduling/attention stocks (use the scheduling skill), nudge persistence decomposition, or single-audience default nudges].
---

# Vaccination-History-Contingent Reactance Backfire

## Overview
The npj Digital Medicine trial (Yang et al., Peking University, published Aug 18, 2026) randomized **2,167 older adults (60+) in Lanzhou New Area, Gansu** across **eight parallel arms** — seven nudge methods plus control — through 80 family-doctor teams' household surveys on a web platform. Headline willingness was **19.20%**. The finding that matters: **nudge effectiveness is contingent on vaccination history** — a video nudge significantly increased willingness among the **unvaccinated** (especially those worried about side effects), while **for previously vaccinated participants, most nudge methods were negatively associated with willingness**, with stronger negative effects in those **without prior influenza experience**. The authors' interpretation: indiscriminate application to already-behaved recipients paradoxically reduces willingness **through psychological reactance**. This is the library's first field-grade demonstration of segment-conditional backfire — nudges that help the intended audience can hurt the already-convinced — and it sharpens the existing nudge-effectiveness skepticism into a design rule: **history is a targeting variable, and "do not nudge" is a valid arm.**

## The Evidence Base
- **Yang et al., npj Digital Medicine (Aug 18, 2026):** N=2,167; 7 community health service centers; 80 family doctor teams (≥20 household surveys each; 183-524 subjects per center); online randomization to 8 arms; baseline willingness 19.20%; video nudges increase willingness in unvaccinated participants, particularly side-effect-worried; previously vaccinated show negative associations with most nudge methods; those without prior influenza experience show stronger negative effects; authors name reactance as the mechanism.
- **Same-window comparators (below-bar but contextually useful):** the **NUDGE-FLU pooled analysis** (Jensen et al., Clinical Infectious Diseases, Sept 2, 2026 — 1,181,254 participants across two nationwide Danish trials; letters raised uptake +2.79pp overall and +4.12pp among immunosuppressed; +11.7pp in younger chronic-condition adults, +13.3pp immunosuppressed) and the **Kaiser Colorado flu nudge RCT** (NCT07372950, ~100K target, completion Sept 2026 — text-message framing trial, results pending). The Danish letters show *unconditional* letter nudges work broadly; the Chinese trial shows *conditional* backfire in a segment — the contrast is the lesson.
- **Library context:** `nudge-history-reactance` holds the theory; this trial supplies the field-grade, history-contingent instantiation.

## Core Findings (the pattern)
1. **History is a targeting variable.** The same nudge helps unvaccinated recipients and hurts previously vaccinated ones — segmentation by behavioral history is not optimization garnish, it is the difference between lift and backfire.
2. **"Do not nudge" is a valid arm.** A multi-segment program needs an explicit no-nudge segment for the already-behaved; contact itself can be the harm.
3. **Reactance is the named mechanism, not an interpretation garnish.** Already-behaved recipients read the nudge as pressure; the negative effect is strongest in those without prior influenza experience — i.e., those whose good behavior is least internally motivated.
4. **Video (modality) matters where the barrier is emotional.** The video nudge worked on the side-effect-worried unvaccinated — modality choice should track the *barrier type* (emotional vs informational), not just the audience.
5. **Scale contrast with the Danish letters.** 1.18M-participant letter programs show unconditional lift across chronic-disease populations; the Chinese trial shows segment-conditional backfire in older adults — nudge universality claims must now survive a history-contingency check.

## When to Use
- Designing multi-segment nudge or notification programs (vaccination, renewals, onboarding, feature adoption, savings behaviors): assign the already-behaved segment a no-nudge arm.
- Auditing campaigns for backfire: any program that nudges *everyone* is now presumptively mis-targeted.
- Tailoring modality to barrier type (video for emotional barriers, framing for informational ones).
- Writing on nudge ethics/limits: this is the cleanest field evidence that nudging is not neutral contact.

## NOT For
- Nudge timing/cadence design (use `attention-stock-nudge-scheduling` — different mechanism, within-treatment dynamics).
- Nudge persistence (use `nudge-persistence-meta-analysis-38-experiments` — post-treatment artifact effects).
- General reactance theory (use `nudge-history-reactance` — the theoretical sibling).

## Core Process / Workflow
1. **Segment by behavioral history first.** Classify the audience by prior behavior (did it / didn't do it) before choosing any intervention.
2. **Assign the no-nudge arm explicitly.** For the already-behaved segment, the default is *no contact*, not a different message.
3. **Match modality to barrier.** Video/relational formats where the barrier is emotional (fear, mistrust); framing/information where it is cognitive.
4. **Pre-register backfire checks.** Any multi-segment nudge program should include a history-interaction hypothesis in its evaluation plan — the npj trial's design is the template.
5. **Watch for the strongest-backfire profile.** Recipients whose compliance is least internally motivated (no prior issue experience, no intrinsic drive) show the sharpest negative effect — treat that profile as the do-not-contact list.

## A-Tech Alignment
- **Behavioral-psychology rigor:** extends the library's nudge-skepticism arc with the first history-contingent backfire evidence — the honest-position backbone for A-Tech's content.
- **Privacy/trust:** reinforces the consent-first posture — nudging people who already consented behaves like pressure, not help; the same logic governs notification design in A-Tech products.
- **Practical:** a three-step targeting rule (segment by history → no-nudge arm → modality-to-barrier) directly implementable in any A-Tech product or campaign.

## Honesty Caveats
- Willingness ≠ vaccination (stated intention, not observed uptake; the trial is community/web-based, not clinic-verified).
- Single country (China), single population (60+), single behavior (influenza) — reactance-backfire generality is inferred, not demonstrated across domains.
- "Most nudge methods" negatively associated — per-method breakdowns beyond the video-nudge result are not itemized in the abstract.
- The Danish NUDGE-FLU pooled analysis shows positive unconditional effects in different populations — the two studies are not a controlled comparison; population and channel differ.
- Below-bar items (Kaiser Colorado framing trial pending) are context, not evidence.

## Pairs-with
`nudge-history-reactance` (the theoretical sibling — this is its first field-grade history-contingent demonstration), `attention-stock-nudge-scheduling` (the timing counterpart: when to nudge vs whether to nudge), `nudge-persistence-meta-analysis-38-experiments` (post-treatment effects), `behavioral-intervention-choice-tailoring` (tailoring by preference; this is tailoring by history), `digital-nudges-nag-whatsapp-backfire` (the messaging-backfire precedent), `social-media-warning-labels-youth`.

## References
- Yang, F., Hu, B., Huang, N., Wang, W., Zhang, S., Jiang, Q., Pang, Y., Fu, M., Chen, C. & Guo, J. "An online randomized trial of electronic nudges for influenza vaccination willingness among older Chinese adults." npj Digital Medicine, published Aug 18, 2026. (Peking University; Beijing Natural Science Foundation L242145.)
- Jensen, A.M.R. et al. "Electronic Nudges to Increase Influenza Vaccination in Immunosuppressed Adults Across the Age Spectrum: A Pooled Analysis of 2 Nationwide Randomized Trials." Clinical Infectious Diseases 83(2):321-330, published Sept 2, 2026 (NUDGE-FLU-2 + NUDGE-FLU-CHRONIC; N=1,181,254).
- Kaiser Permanente Colorado flu nudge RCT (NCT07372950), completion Sept 2026 — results pending.

*Created: 2026-09-17 (Cycle 28) — A-Tech Research Division*