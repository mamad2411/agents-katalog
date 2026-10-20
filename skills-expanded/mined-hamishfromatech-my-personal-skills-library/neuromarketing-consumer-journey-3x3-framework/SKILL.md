---
name: neuromarketing-consumer-journey-3x3-framework
description: Apply the 3×3 neuromarketing typology (decision-making stages × affective/behavioral/cognitive components) and the cross-modal tool-interaction framework from the 2025 Frontiers systematic review. Maps stage-specific neural correlates to the full consumer journey (pre-purchase, purchase, post-purchase) and pairs each stage with the right neurometric and non-neurometric tools. Use when designing a neuromarketing measurement plan across the entire customer journey, selecting which neuro/physiological tools to combine at each stage, identifying under-explored research gaps, or building a privacy-first, behavioral-signal-based version of the framework for A-Tech products.
---

# Neuromarketing Consumer Journey: The 3×3 Framework

## Overview

A 2025 systematic review (PRISMA, 109 peer-reviewed studies, Frontiers in Neuroergonomics) by Gupta, Kapoor, and Verma is the first review to examine **actual behavior** — not proxy or self-reported intent — across all stages of consumer decision-making using both neurometric and non-neurometric tools. It resolves the field's definitional ambiguity, proposes an integrated conceptual framework, and introduces a **3×3 typology** that maps decision-making stages to the affective, behavioral, and cognitive components of attitude.

The review's central contribution: neuromarketing has historically over-concentrated on the **pre-purchase** stage. The purchase and post-purchase phases — where satisfaction, loyalty, and advocacy actually form — remain under-explored because they are hard to measure in controlled lab settings. The framework provides a roadmap for closing that gap, including which cross-modal tool combinations work at each stage.

## When to Use

- Designing a neuromarketing measurement plan that spans the entire customer journey (not just ads/awareness)
- Selecting which neurometric (EEG, fMRI, fNIRS, MEG) and non-neurometric (eye-tracking, GSR, facial coding, HRV, implicit response tests) tools to combine at each decision stage
- Identifying under-researched areas in your neuromarketing program (the typology shows where the field itself is thin)
- Building a privacy-first, behavioral-signal-based adaptation of the framework for A-Coder, Be Practical, or Builder's Club
- Evaluating neuromarketing vendors against an established research framework
- Planning cross-cultural or naturalistic (in-the-wild) neuromarketing studies

NOT for:
- The conceptual distinction between basic/translational/applied neuromarketing (see `neuromarketing-three-layer-discipline`)
- The bibliometric landscape of the field (see `neuromarketing-research-landscape-2026`)
- Practical campaign-level operating model (see `neuromarketing-2026-practical-operating-model`)
- Ethical persuasion defense (see `dark-psychology-neuromarketing-autonomy-defense`)

## Standardized Definition

> Neuromarketing is an interdisciplinary area which applies neuroscience and cognitive neuroscience to business. It is about creating brain-friendly content or communication which helps understand how consumers react at a non-conscious level in real time, based on brain operating principles, and the responses can be measured by various neuro-metric or non-neuro-metric techniques.

This definition resolves prior ambiguity by anchoring neuromarketing to **brain-friendly content/communication** and **real-time non-conscious reaction** measurable by both neuro and non-neuro tools.

## The Three Decision Phases

The consumer journey collapses five classical stages into three phases:

| Phase | Classical Stages | Key Question |
|-------|-----------------|--------------|
| **Pre-purchase** | Need recognition, information search, evaluation of alternatives | How do consumers form awareness, interest, and preference? |
| **Purchase** | Choice / buying decision | What triggers the actual transaction? |
| **Post-purchase** | Post-choice evaluation | What drives satisfaction, loyalty, advocacy, regret? |

Most existing neuromarketing research sits in the pre-purchase column. The purchase and post-purchase columns are the frontier.

## The 3×3 Typology

```
                 |  Affective (A)  |  Behavioral (B)  |  Cognitive (C)
-----------------+------------------+------------------+------------------
 Pre-purchase    |  Well-studied    |  Moderate        |  Well-studied
 Purchase        |  Under-studied   |  Under-studied   |  Under-studied
 Post-purchase   |  Under-studied   |  Under-studied   |  Moderate
```

- **Affective (A):** Emotional valence and arousal — feelings the stimulus produces.
- **Behavioral (B):** Observable actions — gaze, clicks, reaction time, actual purchase.
- **Cognitive (C):** Attention, memory, reasoning, cognitive load, value computation.

The dark cells (purchase row, post-purchase affective/behavioral) are the field's biggest gaps and therefore the highest-leverage areas for differentiated neuromarketing work.

### Why the Purchase and Post-Purchase Stages Are Under-Studied

1. **Low ecological validity of labs.** fMRI/EEG settings cannot replicate real retail pressure, time constraints, and social cues.
2. **Post-purchase emotions develop over time.** Satisfaction, loyalty, and regret are slow constructs that controlled experiments miss.
3. **Real-time capture is hard.** The moment of transaction is dynamic; portable/wearable tools are only now becoming viable.

**Implication for A-Tech:** Because these stages are under-studied, building privacy-first behavioral-signal measurement at the purchase and post-purchase stages is a genuine differentiator — not a crowded field.

## Stage-Specific Neural Correlates

### Pre-Purchase

| Sub-stage | Key Brain Regions / Signals | What They Indicate | Primary Tools |
|-----------|----------------------------|--------------------|---------------|
| Need recognition | Ventral striatum (reward anticipation), amygdala (emotional relevance) | Reward anticipation drives early brand preference; "organic" labels activate ventral striatum | fMRI, EEG |
| Information search | Prefrontal cortex (logical assessment), amygdala (emotional/brand value) | Cognitive vs emotional evaluation split | EEG (P300, LPP), fMRI |
| Evaluation of alternatives | Stratum (reward integration of price + benefit) | Integration of emotional and cognitive inputs during comparison | EEG, fMRI, eye-tracking |

**Privacy-first adaptation:** Replace lab fMRI with behavioral proxies — dwell time on comparison pages, scroll-back patterns, tab-switching frequency, query refinement sequences. These correlate with the prefrontal/amygdala split (deliberation vs emotional pull) without any biometric capture.

### Purchase

| Sub-stage | Key Signals | What They Indicate | Primary Tools |
|-----------|-------------|--------------------|---------------|
| Point of sale | Attention shifts, emotional arousal, decision urgency | Immediate contextual triggers (payment options, wait times, social cues) | Portable EEG, GSR, eye-tracking, HRV |
| Willingness to pay | Reward-related striatal activity | Price-value integration at the moment of choice | fMRI, IRT |

**The core gap:** Most research uses self-reported purchase intent, which suffers from the intention-behavior gap. Actual purchase behavior is rarely measured with neural tools. Portable/wearable devices and VR-simulated shopping are the emerging methods.

**Privacy-first adaptation:** For A-Coder (purchase = install/upgrade/subscribe), measure the behavioral signature of the decision moment — time-to-subscribe after feature discovery, pause-before-pay patterns, plan-tier comparison depth — as proxies for arousal and cognitive effort at the point of sale.

### Post-Purchase

| Sub-stage | Key Signals | What They Indicate | Primary Tools |
|-----------|-------------|--------------------|---------------|
| Satisfaction | Ventral striatum (reward/pleasure), prefrontal cortex (value fulfillment) | Reward realization vs expectation | fMRI |
| Regret / dissonance | Error-related negativity (ERN) | Post-purchase regret or dissatisfaction | EEG |
| Arousal / cognitive load | Pupil dilation changes | Emotional intensity of the post-purchase experience | Pupillometry |

**The core gap:** Post-purchase is the least studied phase yet drives loyalty, repurchase, and advocacy — the highest-value retention outcomes. Storytelling has been shown to shift post-purchase decision-making (Hamelin et al. 2020), but neural measurement of long-term satisfaction is rare.

**Privacy-first adaptation:** For Be Practical and Builder's Club, post-purchase = post-completion / post-contribution. Measure satisfaction proxies: return-to-platform latency, session length after completion, unsolicited sharing behavior, review/rating submission speed. These map to the ventral-striatum/ERN satisfaction-regret axis without biometrics.

## Cross-Modal Tool Interaction Framework

The review's key methodological insight: no single tool captures the full picture. The strength of neuromarketing is **cross-modal triangulation** — combining tools so each compensates for the others' blind spots.

| Tool | Strength | Blind Spot | Best Paired With |
|------|----------|-----------|------------------|
| fMRI | Deep spatial resolution, subcortical reward regions | Low temporal resolution, expensive, lab-only | EEG (temporal), eye-tracking (attention) |
| EEG | Sub-millisecond temporal resolution, ERPs (P300, LPP, ERN) | Limited spatial depth, lab-bound | GSR (arousal), eye-tracking (attention), facial coding (valence) |
| Eye-tracking | Visual attention, fixation, pupil dilation (arousal) | Cannot reveal valence or cognitive content | EEG (neural), GSR (arousal), facial coding (valence) |
| GSR / EDA | Emotional arousal intensity | Cannot reveal valence quality | Facial coding (valence), EEG (cognitive load) |
| Facial Action Coding | Emotional valence | Cannot assess arousal intensity | GSR (arousal), HRV (autonomic) |
| HRV | Autonomic arousal, attention vs stress, flow | Not suitable for still images | EEG, GSR for video/stimuli |
| Implicit Response Tests (IRT/IAT) | Unconscious attitudes below 500ms threshold | Conscious deliberation | EEG, eye-tracking |
| fNIRS | Prefrontal cortex activation (price, risk, selection) | Limited to cortical surface | Eye-tracking, EEG |
| Pupillometry | Emotional arousal + cognitive load | Valence | EEG, facial coding |
| MEG | Deep cortical activity, good temporal resolution | Expensive, rare | EEG, fMRI |

### The Pairing Logic

- **Valence without arousal** (facial coding alone) misses intensity.
- **Arousal without valence** (GSR alone) misses whether the emotion is positive or negative.
- **Neural without attention** (EEG alone) misses what the person actually looked at.
- **Self-report without any of the above** captures only post-hoc, socially-desirable, cognitively-biased accounts.

The review found that most high-quality studies use a **hybrid approach** combining neuro + non-neuro + traditional (questionnaire/IAT) techniques.

## Measurement Indicator Matrix

Which tools measure which constructs at which stage:

| Construct | Pre-purchase tools | Purchase tools | Post-purchase tools |
|-----------|-------------------|----------------|---------------------|
| Attention | fMRI, EEG, ET, GSR, FEA, IRT | EEG, ET, GSR, FEA, IRT | EEG, ET |
| Engagement | fMRI, EEG, ET, GSR, FEA, IRT | EEG, ET, GSR, FEA, IRT | fMRI, EEG |
| Cognitive load | fMRI, EEG, ET, GSR, FEA, IRT | fMRI, EEG, ET, GSR, FEA, IRT | EEG, ET |
| Emotion valence | fMRI, EEG, ET, GSR, FEA, IRT | fMRI, EEG, ET, GSR, FEA, IRT | EEG, ET, GSR, FEA |
| Emotion arousal | fMRI, EEG, ET, GSR, FEA, IRT | fMRI, EEG, ET, GSR, FEA, IRT | EEG, ET, GSR |
| Preference | fMRI, EEG, ET, GSR, FEA, IRT | fMRI, EEG, ET, GSR, IRT | fMRI, EEG, ET |
| Memory | fMRI, EEG, ET, GSR, FEA, IRT | fMRI, EEG, ET, GSR, FEA | fMRI, EEG, ET |

Note the post-purchase column is the thinnest — confirming the research gap.

## Seminal Theories Mapped to Stages

The review maps established theories to stages and attitude components. Key ones for A-Tech application:

| Theory | Stage Relevance | A-Tech Application |
|--------|----------------|---------------------|
| Dual-process theory (Kahneman System 1/2) | All stages; System 1 dominates | A-Coder's "feel" of the IDE should be System-1 fast; onboarding can leverage System-2 deliberation |
| SOR (Stimulus-Organism-Response) | Pre-purchase, purchase | UI stimulus → internal state → behavior (subscribe, contribute) |
| Elaboration Likelihood Model (ELM) | Pre-purchase | Central vs peripheral routes for technical vs emotional messaging |
| Somatic marker hypothesis (Damasio) | Post-purchase | Emotional markers from prior outcomes guide future repurchase/return |
| Flow theory | Purchase, post-purchase | Be Practical chapter completion flow drives post-purchase satisfaction |
| Prospect theory | Evaluation | Loss framing in plan comparisons |

## Privacy-First Behavioral-Signal Adaptation (A-Tech Native)

A-Tech's values prohibit biometric surveillance. The framework adapts by mapping neural constructs to **observable behavioral signals** collected locally:

| Neural Construct | Lab Tool | Privacy-First Behavioral Proxy (A-Tech) |
|------------------|---------|------------------------------------------|
| Attention | Eye-tracking | Gaze-equivalent: scroll depth, hover duration, element interaction order |
| Arousal | GSR, HRV | Typing cadence variance, click velocity, pause-before-action patterns |
| Cognitive load | EEG (P300, ERN) | Error recovery time, backtracking frequency, help-query rate, session fragmentation |
| Valence | Facial coding | Sentiment of in-product text input, tone of community posts, thumbs/feedback speed |
| Memory / recall | EEG, IRT | Return-to-feature latency, unprompted reuse, recall without onboarding prompts |
| Preference | fMRI, IRT | Plan-comparison depth, feature-activation order, upgrade vs downgrade patterns |
| Post-purchase satisfaction | Ventral striatum, ERN | Return-to-platform latency after purchase, session length post-conversion, voluntary rating/review |

All proxies are computed on-device from interaction telemetry the user already generates. No biometric sensors, no third-party data sharing. This is the privacy-first translation of the 3×3 framework.

## A-Tech Product Applications

### A-Coder

- **Pre-purchase (trial/evaluation):** Measure onboarding flow completion, feature-discovery order, and comparison-page dwell as proxies for the prefrontal/amygdala deliberation-emotion split. Optimize the evaluation experience for low cognitive load (simplify the comparison matrix).
- **Purchase (subscribe/upgrade):** Measure time-to-subscribe after feature discovery and pause-before-pay patterns as proxies for purchase-stage arousal and cognitive effort. Reduce the intention-behavior gap by minimizing friction at the decision moment.
- **Post-purchase (retention):** Track return-to-platform latency, session length post-conversion, and voluntary advocacy (stars, shares, community posts) as proxies for ventral-striatum satisfaction and ERN regret. The post-purchase stage is A-Coder's biggest opportunity because it is the field's biggest gap.

### Be Practical

- **Pre-purchase (enrollment):** Map the SOR pathway — course preview (stimulus) → curiosity/relief (organism) → enroll (response). Use the ELM central route for technical chapters, peripheral route for motivational content.
- **Purchase (enrollment decision):** Measure the decision moment — plan comparison depth and time-to-enroll — as purchase-stage signals.
- **Post-purchase (completion & advocacy):** Flow-theory-driven completion produces post-purchase satisfaction. Track completion rate, post-completion session length, and unsolicited sharing as satisfaction proxies. Storytelling (open-loop storytelling skill) shifts post-purchase decision-making per Hamelin et al.

### Builder's Club

- **Pre-purchase (join/explore):** Community discovery and evaluation map to the need-recognition and evaluation stages. Measure exploration depth and contribution-intent signals.
- **Purchase (contribute/first commit):** The first contribution is the "purchase" moment. Measure time-to-first-contribution and pause-before-commit patterns.
- **Post-purchase (retained contributor):** Unprompted contribution tracking (from the rapid-habit-transition-switch skill) is the post-purchase behavioral signature. The community flywheel is a post-purchase loyalty engine.

## Future Research Directions (from the review)

1. **Multi-modal integration** — combine fMRI + EEG + eye-tracking for holistic stage coverage.
2. **Machine learning on multimodal data** — deep learning on neural + gaze + facial signals for preference prediction.
3. **Unconscious process exploration** — IATs alongside neural measurement to reveal hidden drivers.
4. **Naturalistic settings** — portable/wearable EEG, mobile eye-tracking, HRV monitors for real-world validity.
5. **Under-explored areas** — social marketing (health, sustainability, climate), cross-cultural validation, post-purchase loyalty neural mechanisms.

A-Tech's privacy-first behavioral-signal approach addresses directions 3–5 simultaneously: it captures unconscious behavior implicitly, works in naturalistic settings (in-product), and fills the post-purchase gap the field has identified.

## Anti-Patterns

1. **Pre-purchase tunnel vision** — Measuring only awareness/ad response and ignoring purchase and post-purchase. This replicates the field's own gap rather than differentiating.
2. **Single-tool over-reliance** — Using only eye-tracking or only sentiment analysis. Every tool has a blind spot the framework explicitly pairs against.
3. **Self-report substitution** — Treating surveys as equivalent to neuromarketing. The review's core finding is that self-report suffers from social desirability, misremembering, and the intention-behavior gap.
4. **Biometric surveillance creep** — Importing lab tools (facial coding, GSR) into products without consent. A-Tech's values require behavioral-signal proxies, not biometric capture.
5. **Lab-only generalization** — Assuming lab fMRI findings transfer directly to in-product behavior. Ecological validity is the field's acknowledged limitation.

## Alignment with A-Tech Values

- **Open-Source AI:** The framework is published open-access (CC BY). The privacy-first behavioral-signal adaptation can be open-sourced as a measurement reference architecture.
- **Data Privacy:** The entire A-Tech adaptation uses on-device behavioral signals, never biometrics. This is the privacy-first version of a field built on biometric labs.
- **Financial Freedom:** Post-purchase loyalty is the highest-value retention outcome. Measuring and optimizing it directly drives revenue durability and financial independence.
- **Practical Implementation:** The 3×3 typology and tool-pairing matrix give a concrete measurement plan. The behavioral-signal proxies make it executable without lab equipment.

## Relationship to Existing Skills

- **`neuromarketing-2026-practical-operating-model`** provides the six-layer operating model (Attention → Emotion → Memory → Trust → Action → Measurement). This skill adds the **stage dimension** (pre-purchase / purchase / post-purchase) and the **tool-selection logic** the operating model lacks.
- **`neuromarketing-research-landscape-2026`** maps the field's themes bibliometrically. This skill maps the field's **stages and tools** methodologically.
- **`neuromarketing-three-layer-discipline`** distinguishes basic/translational/applied. This skill provides the applied measurement framework that sits in the "applied" layer.
- **`choice-closure-effect`** addresses post-purchase confirmation rituals. This skill provides the broader post-purchase measurement context that choice-closure sits within.
- **`curiosity-progression-marketing`** uses open-loop storytelling across stages. This skill provides the stage-by-stage measurement framework to evaluate whether curiosity loops actually move the neural proxies.

## Research Source

- Gupta R, Kapoor AP, Verma HV (2025) "Neuro-insights: a systematic review of neuromarketing perspectives across consumer buying stages." Frontiers in Neuroergonomics 6:1542847. doi: 10.3389/fnrgo.2025.1542847 — PRISMA systematic review of 109 peer-reviewed studies (2020–2025), proposing the 3×3 typology, cross-modal tool framework, and stage-specific neural correlate mapping.