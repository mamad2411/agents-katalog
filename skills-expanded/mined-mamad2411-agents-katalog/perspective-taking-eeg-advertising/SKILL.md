---
name: perspective-taking-eeg-advertising
description: Use when designing video ads with testimonials or product interactions, explaining why viewers identify with ad characters, planning EEG pre-testing of narrative content, or building content that transports viewers into a character's perspective.
---

# Perspective-Taking in Video Ads: EEG Spectral + Connectivity Evidence

**Source:** Bilucaglia, Casiraghi, Russo & Zito (IULM Behavior & Brain Lab, Milan), "Perspective-taking in video advertising: insights from EEG connectivity and channel-wise spectral analysis," Frontiers in Behavioral Neuroscience 20:1740368, published July 24 2026 (CC-BY). Exploratory: N=20 (19 analyzed, 27–55 yrs), 4 food/beverage testimonial-style ads, product-interaction segments (eating/drinking, ~3.1s). EEG + self-reports of cognitive perspective-taking (COG), emotional perspective-taking (EMO), and perceived ad effectiveness (EFF).

## Findings

- **Cognitive perspective-taking correlates with network efficiency:** COG correlated negatively with frontal θ power (F7, F4: r ≈ −0.71) and positively with α clustering coefficient (Cα, r = 0.709).
- **Perceived ad effectiveness shows a distinct, partially overlapping pattern:** EFF correlated with α clustering coefficient, α path length, α kappa divergence, plus δ average degree and path length.
- **Overlap → shared mechanism:** COG and EFF share α-clustering correlates, consistent with Narrative Transportation Theory — adopting a character's perspective is one plausible process behind ad effectiveness.
- **Key methodological insight:** a control analysis on matched neutral pre-stimulus windows (same testimonial, no product interaction) killed all correlations (all p > .10, uncorrected). The interaction segment — not the testimonial's mere presence — drives the neural signature.

## Practical Takeaways

1. **Show the interaction, not the product.** The neural correlates tied to effectiveness appear only in moments when the testimonial *uses* the product, not adjacent "product alone" shots. Edit toward interaction beats.
2. **Perspective-taking is a mechanism you can aim at:** the viewer simulating "how does that taste/feel" predicts both cognitive identification and perceived effectiveness.
3. **Don't over-claim the mechanism.** Working-memory and reward explanations are explicitly post-hoc — the authors flag untested constructs and scalp-vs-source limits (22 electrodes; confirmatory work needs ≥40 participants and HD-EEG/source-level analysis).
4. **EEG connectivity (MST metrics: leaf fraction, diameter, hierarchy, kappa divergence) adds dimensions that spectral power alone misses** — but this was exploratory; treat as hypothesis-generating.

## Limitations (carry them forward)

N=19 final; α threshold lowered to 0.10; FDR-corrected; four heterogeneous stimuli; segments 1.3–4.9s (connectivity estimates need ≥6s epochs); no behavioral outcome measure (no purchase, no memory task). Do not treat any single correlation as actionable without confirmation.

## Cross-Links

- `narrative-transportation-developer-trust` — transportation theory applied to dev audiences
- `neural-ad-liking-temporal-dynamics` — fMRI temporal dynamics of ad liking; complementary modality
- `sustained-attention-purchase-paradox` — EEG deliberation signals in the same lab lineage (BCN journal)
- `perspective-taking` (consumer journey) — behavioral-layer counterpart

## A-Tech Fit

- **Open source:** EEG pipelines (EEGLab, MST analysis via Brain Connectivity Toolbox) are open — a low-cost replication is feasible for content A/B testing.
- **Privacy:** scalp EEG with consent + GDPR compliance demonstrated; supports "consent-first, local-analysis-first" neuro pre-testing posture.
- **Practical:** directly actionable edit guidance — interaction segments over product shots; perspective-taking scales (Palcu et al.) as a low-cost pre-test supplement.