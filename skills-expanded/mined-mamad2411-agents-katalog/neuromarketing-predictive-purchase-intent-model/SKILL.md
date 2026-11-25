---
name: neuromarketing-predictive-purchase-intent-model
description: Apply the quantitative EEG + eye-tracking model for predicting consumer purchase intent to design pre-launch ad testing and content optimization. Covers the specific predictor hierarchy (fixation duration > frontal alpha > number of fixations > frontal beta), the 53% variance-explained regression model, the emotional-vs-informational ad effect (4.01 vs 3.43 purchase intent), product-category moderation, and the privacy-first translation to behavioral-signal proxies. Use when designing pre-launch ad testing, predicting purchase intent from attention/emotion metrics, choosing between emotional and informational ad strategies, or translating lab neuromarketing findings into privacy-safe behavioral proxies for on-device measurement. NOT for the general neuromarketing consumer-journey framework (use neuromarketing-consumer-journey-3x3-framework), the closed-loop optimization loop (use closed-loop-cognition-marketing), or broad market-sizing data (use neuromarketing-market-evidence-2026).
---

# Neuromarketing Predictive Purchase Intent Model

## Overview
A quantitative, evidence-based model for predicting consumer purchase intent from EEG neural engagement and eye-tracking visual attention metrics. Built on a 285-participant study (Iyappan et al., JMSR, Nov 2025) that used a 32-channel Emotiv EEG and Tobii Pro Nano eye-tracker across 20 video ads spanning four product categories. The model explains 53% of purchase-intent variance and identifies fixation duration as the single most powerful predictor — giving A-Tech a concrete, testable framework for pre-launch ad validation and privacy-first behavioral-signal translation.

## When to Use
- Designing pre-launch ad testing to predict purchase intent before campaign spend
- Choosing between emotional (narrative/music) and informational (feature/text) ad strategies
- Prioritizing which attention/emotion metrics to track for content optimization
- Translating lab-based EEG/eye-tracking findings into privacy-safe behavioral proxies (dwell time, scroll depth, replay rate)
- Building a predictive purchase-intent model for A-Tech product launches
- Validating ad creative with a small-sample test before scaling spend

NOT for:
- The general neuromarketing consumer-journey 3×3 framework — use `neuromarketing-consumer-journey-3x3-framework`
- The closed-loop optimization loop (measure → analyze → optimize → deploy) — use `closed-loop-cognition-marketing`
- Broad neuromarketing market sizing — use `neuromarketing-market-evidence-2026`
- Privacy-first behavioral analytics architecture — use `neuro-marketing-privacy-first-behavioral-analytics`

## Core Process / Workflow

### 1. Understand the predictor hierarchy

The regression model (R² = 0.53, adjusted R² = 0.51, F(4,280) = 78.3, p < 0.001) ranks predictors by standardized beta:

| Rank | Predictor | β | p-value | What it measures |
|---|---|---|---|---|
| 1 | **Fixation duration** | 0.38 | <0.001 | Sustained visual attention on product-related elements |
| 2 | **Frontal alpha activity** | 0.31 | <0.001 | Positive emotional engagement, approach motivation |
| 3 | **Number of fixations** | 0.21 | 0.003 | Repeated attention shifts, information processing |
| 4 | **Frontal beta activity** | 0.18 | 0.008 | Cognitive arousal, focused attention |

**Key insight:** Visual attention (eye-tracking) is a slightly more powerful predictor than neural engagement (EEG). Fixation duration alone correlates with purchase intent at r = 0.48 — the strongest single-variable relationship in the study.

**Correlation matrix:**

| Predictor | r with purchase intent |
|---|---|
| Fixation duration | **0.48** (p < 0.001) |
| Frontal alpha | 0.42 (p < 0.001) |
| Number of fixations | 0.35 (p < 0.01) |
| Frontal beta | 0.31 (p < 0.01) |

### 2. Apply the emotional-vs-informational ad effect

ANOVA results (F(1,283) = 16.8, p < 0.001):

| Ad type | Mean purchase intent (1–5) |
|---|---|
| Emotional (narrative/music) | **4.01** |
| Informational (feature/text) | 3.43 |

Emotional ads generate stronger neural engagement and longer visual attention, which translates to higher purchase intent. The effect holds across product categories.

**Design implication:** Lead with emotional storytelling. Use informational content as supporting detail, not as the primary narrative vehicle.

### 3. Account for product-category moderation

ANOVA (F(3,281) = 4.27, p = 0.006):

| Product category | Mean purchase intent |
|---|---|
| Fashion | **3.95** (highest) |
| Lifestyle | ~3.75 |
| FMCG | ~3.60 |
| Electronics | **3.51** (lowest) |

Product category moderates the ad-type effect. Fashion and lifestyle products benefit most from emotional advertising; electronics respond less to emotional framing and may require more functional/informational balance.

### 4. Build the pre-launch testing protocol

```
1. RECRUIT: 30–50 participants (lab) or 200+ (online behavioral proxy)
   - Screen for neurological disorders, vision problems, prior ad exposure
   - Balance demographics (the study used 145M/140F, age 18–45, mean 28.7)

2. STIMULI: Create 10–20 ad variants (30–60s each)
   - Split: emotional vs. informational
   - Span 2–4 product categories relevant to your launch
   - Randomize presentation order to limit order effects

3. MEASURE (lab):
   - EEG: frontal alpha (8–13 Hz) + frontal beta (13–30 Hz), 32-channel
   - Eye-tracking: fixation duration, number of fixations, gaze heatmaps
   - Self-report: 5-point Likert purchase intent after each ad

4. MEASURE (privacy-first behavioral proxy):
   - Fixation duration → dwell time on key elements, replay rate
   - Number of fixations → scroll-back frequency, element revisits
   - Frontal alpha → sentiment of open-ended responses, share/forward rate
   - Frontal beta → task completion speed, interaction intensity

5. ANALYZE:
   - Pearson correlations: each predictor vs. purchase intent
   - Multiple regression: all four predictors → purchase intent
   - ANOVA: emotional vs. informational × product category
   - Target R² ≥ 0.50 for a valid predictive model

6. OPTIMIZE:
   - Rank ad variants by predicted purchase intent
   - Adjust creative: increase fixation-driving elements (product close-ups,
     brand placement in high-attention zones), strengthen emotional narrative
   - Re-test top 3 variants; deploy the winner
```

### 5. Translate to privacy-first behavioral proxies (A-Tech values)

The lab study used EEG and eye-tracking hardware. A-Tech's privacy-first principle requires translating these to behavioral signals measurable without biometric surveillance:

| Lab metric | Privacy-first behavioral proxy | Why it works |
|---|---|---|
| Fixation duration | Dwell time on product page element; video replay rate | Sustained attention = longer dwell |
| Number of fixations | Scroll-back frequency; element revisit count | Repeated attention shifts |
| Frontal alpha (positive emotion) | Share/forward rate; open-ended sentiment; community post tone | Approach motivation → sharing |
| Frontal beta (cognitive arousal) | Interaction intensity; feature exploration depth; session length | Focused engagement → deeper exploration |

**On-device processing:** All behavioral signals computed locally; only aggregated, consented metrics leave the device. No biometric data collection.

### 6. A-Tech application

**A-Coder:**
- Build a pre-launch ad/landing-page testing module using behavioral proxies (dwell time, replay rate, scroll-back) as the fixation-duration analog
- Implement the predictor hierarchy in the analytics dashboard (fixation-proxy weighted highest)
- Use the emotional-vs-informational effect to guide A-Coder's own marketing: lead with developer stories (emotional), support with feature lists (informational)

**Be Practical:**
- Create a chapter on "pre-launch ad testing on a budget" — the 30–50 participant protocol with behavioral proxies
- Teach the predictor hierarchy so marketers know which metric to optimize first (attention > emotion > arousal)
- Include the product-category moderation table so readers calibrate emotional vs. informational balance for their category

**Builder's Club:**
- Open-source the behavioral-proxy mapping as a reference implementation
- Community challenge: validate the 53% variance-explained model using only behavioral proxies (no EEG/eye-tracking)
- Share pre-launch testing results across the community to build a cross-category benchmark database

## Anti-Patterns

- **Optimizing only for self-reported purchase intent** — self-report suffers from social desirability bias and the intention-behavior gap; the study's neural/attention metrics predict what surveys miss.
- **Ignoring fixation duration as the top predictor** — marketers often focus on emotional metrics (alpha) but the data shows sustained visual attention is the stronger driver.
- **Using emotional ads for all categories equally** — electronics respond less to emotional framing; calibrate by category.
- **Collecting EEG/eye-tracking data without consent** — violates A-Tech's privacy-first principle; use behavioral proxies instead.
- **Testing with too few participants** — the study used 285 for statistical power; lab tests should use ≥30, online behavioral proxy tests ≥200.

## References
- See [references/purchase-intent-study-evidence.md](references/purchase-intent-study-evidence.md) for the full study methodology, statistical tables, stimuli design, and the privacy-first translation framework.