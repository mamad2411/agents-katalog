---
name: discount-clarity-memorization-fixation
description: Applies the Fylaktou/Yfantidou et al. EEG + eye-tracking supermarket-leaflet study (LJMU/CERTH, Corporate Communications, DOI 10.1108/CCIJ-04-2025-0089, accepted Dec 26 2025, OA Mar 23 2026) — fixation duration is the strongest purchase predictor, memorization (EEG) predicts buying while approach-withdrawal does not, and clear discount types engage different predictors than vague ones. Use when designing discount/promo layouts, auditing leaflets or PDP promo mechanics, choosing neurometrics for shopper research, or briefing retailers on discount design.
---

# Discount Clarity, Memorization & Fixation in Shopper Choice

## Overview

Yfantidou, Oikonomou, Georgiadis, Kalaganis, Matta, Nikolopoulos & Kompatsiaris (LJMU Business School / CERTH-ITI — the NeuMa/Brain-Informatics group), "What Drives Consumer Choices? Neuro-Insights from a Supermarket Simulation Study," *Corporate Communications: An International Journal* (DOI 10.1108/CCIJ-04-2025-0089; accepted 26 Dec 2025; first OA 23 Mar 2026; CC-BY). Design: simulated supermarket leaflet identical to real flyers; 42 participants; synchronized eye-tracking + EEG; discount types compared head-to-head; behavior of 42 shoppers analyzed for clarity of promotional messages.

**Findings that matter for promo design:**

1. **Fixation duration is the strongest single predictor of purchase** — robust positive association between time spent viewing a product and likelihood of purchase.
2. **EEG memorization predicts buying decisions; approach-withdrawal does not.** Buying a familiar/remembered product beats mere affective valence in this realistic layout task.
3. **Discount type gates which predictors work:**
   - "50% off" → *shopping duration* predicts purchases (comparative shoppers convert)
   - "1+1 free" → *age* is the relevant covariate
   - Vague "ONLY" framing → *neither* predictor works; ambiguous discounts degrade the whole predictive structure
4. Clear and substantial discounts outperform ambiguous ones — ambiguity suppresses the very behavioral signals marketers otherwise optimize.

## When to Use

- Designing or auditing discount/promotional mechanics (leaflets, flyers, PDP promo strips, category banners)
- Choosing neurometrics for shopper research: what to measure (fixation duration, memorization) vs. what underperforms here (approach-withdrawal alone)
- Advising retailers on message clarity: why "ONLY X%" and hedged promo copy underperform
- Segmentation: matching discount type to shopper segment (time-in-store vs. demographic)
- NOT for: post-cookie ad targeting or personalized recommender design (different mechanism class — see neuro-contextual-advertising skill)

## Core Process / Workflow

### 1. The Fixation-Duration Principle (with a Stage Caveat)

Longer gaze on a product → higher purchase probability in this leaflet setting. Operationally:

- Design layouts that earn legitimate dwell: legible type, real product imagery, uncluttered placement.
- Pair with the sustained-attention-purchase-paradox skill: attention is *stage-dependent*. In leaflet/browse contexts (observation stage) fixation duration is a purchase asset; in deep-deliberation contexts (evaluation of complex/high-stakes offers) over-attention signals friction. Diagnose which stage your surface is before applying.
- Privacy-first proxies without eye tracking: dwell proxies from scroll/pointer interaction data, aggregated — never neural inference (see neuro-marketing-privacy-first-behavioral-analytics).

### 2. Memorization Beats Mere Affect (for Considered Shopper Tasks)

The EEG result — memorization significant, approach-withdrawal not — argues that in realistic choice settings, **memory availability of the product/offer, not raw affective pull, carries the decision signal**. Practical consequences:

- Repeat-exposure systems matter more than one-shot emotional appeals for catalog shopping: consistent product presentation across touchpoints builds the memory traces that convert.
- Brand/familiarity assets (consistent naming, imagery, price anchors across leaflets and app) are decision infrastructure, not decoration.
- For measurement: if you can only afford one EEG index in shopper studies, prefer memorization indices over frontal asymmetry alone.

### 3. The Discount-Clarity Matrix

| Discount type | What predicts purchase | Design implication |
|---|---|---|
| "50% off" (clear, comparative) | Shopping duration (browse → convert) | Let comparison happen; place related items together |
| "1+1 free" (clear, bundling) | Age (demographic segment) | Target bundle promos by segment |
| "ONLY" / vague framing | None — predictive signal collapses | Ban vague qualifiers; state the deal plainly |

Rule: **clarity is a precondition for any optimization.** An ambiguous discount doesn't just convert worse — it destroys the behavioral signal (dwell, duration) you would otherwise use to improve the layout. Audit all promo copy for unambiguous units: percentage vs. amount, single vs. bundle, eligibility conditions stated once, no hedging adverbs.

### 4. Study-Boundary Honesty

- N=42, simulated leaflet, supermarket products (dairy, frozen, etc.); generalization to digital-first, high-consideration, or service categories needs testing.
- Exploratory EEG indices (memorization, approach-withdrawal) are population-level correlates — use for design hypotheses and pre-tests, not individual profiling (privacy-and-trust alignment; also SB-1223-style neural-data caution).
- The study replicates the lab's earlier GFT-hybrid work: eye-tracking descriptors carry more predictive power than standard EEG indices alone, and hybrid (EEG+gaze) beats either unimodal — budget multimodal measurement before scaling conclusions.

## A-Tech Alignment

- **Data privacy**: operationalizes via dwell/duration proxies and aggregate metrics; explicitly avoids neural inference on individuals.
- **Open science**: CERTH/LJMU line is open-access (CC-BY), builds on the public NeuMa dataset — replicable, inspectable evidence for promo design.
- **Financial freedom (consumer side)**: clarity of discounts is consumer protection — ambiguous offers obscure real unit prices; the same clarity matrix works as a consumer-side heuristic for evaluating offers.
- **Practical implementation**: three tables (fixation rule, memorization principle, clarity matrix) are directly usable as a promo-design checklist.

## References

- Primary: Yfantidou et al., Corporate Communications (Emerald), DOI 10.1108/CCIJ-04-2025-0089, LJMU Research Online eprint 27795.
- Companion (same group, Brain Informatics 12:23, 2025): hybrid EEG-GFT + gaze decoding of Buy/NoBuy — eye descriptors outperform standard EEG indices; hybrid wins (κ ≈ 0.35 avg).
- Related existing skills: `sustained-attention-purchase-paradox` (stage-dependence of attention), `multimodal-eeg-eye-tracking-consumer-choice`, `hybrid-eeg-gaze-graph-signal-neuromarketing`, `neuro-marketing-privacy-first-behavioral-analytics`, `consumer-mentalizing-eeg-social-cognition`.
