---
name: lifestyle-medicine-digital-nudging-slr
description: Applies the Frontiers in Digital Health scoping review (Taniar, King, Manger & Carlisle, 2026;8:1799205; 52 studies, PRISMA-ScR) mapping digital nudging across lifestyle-medicine pillars — four intervention categories (one-way, technology-interaction, peer-interaction, self-nudging) within a passive/active conceptual framework, nutrition+PA dominance (>75%), the system-development-to-behavior-change pipeline, and personalization/AI as the named future direction. Use when [mapping digital-nudging evidence by health domain, designing health-behavior interventions, selecting nudge categories for wellbeing products, or positioning AI-driven personalization in behavior change]. NOT for [smartphone screen-time interventions specifically — use wellspent-customizable-screen-time-rct — or behavioral economics theory — use behavioral-psychology core skills].
---

# Digital Nudging for Lifestyle Medicine: The 2026 Scoping Review Map

## Overview
Taniar, King, Manger & Carlisle (Monash + James Cook; *Frontiers in Digital Health* 2026;8:1799205) deliver the first scoping review to map digital nudging across **all lifestyle-medicine pillars** rather than single domains. Method: six databases (MEDLINE, EMBASE, CINAHL, Scopus, IEEE, ACM), 2,709 records screened → **52 studies included**; most from the last five years, computer-science-heavy (40 papers vs 12 health/medical).

## The four-category map (inductively derived, with the passive/active frame)
Technologies (apps, chatbots, AR/VR, wearables, voice, AI) are **delivery platforms, not categories** — the same technology can serve multiple nudging forms:

| Category | What it is | Where it shows up |
|---|---|---|
| **One-way nudging** | Passive: messages, choice architecture (ordering, defaults, labelling), warnings | 23 studies; choice architecture (product ordering, defaults, Nutri-score labelling) consistently improves healthy food selection across lab and real-world settings |
| **Nudging via system interaction** | Active: chatbots, AR/VR overlays, voice interfaces, sensor-embedded utensils, geofenced alerts | Promising for physical activity and mindful eating; limited by novelty effects and hardware practicality |
| **Peer-interaction nudging** | Social: shared step counts, gamified competition/cooperation | Increased activity via social comparison; disengages less-competitive users |
| **Self-nudging** | Agency: self-tracking, self-monitoring, guided self-experimentation | Effective and promising; trade-off between logging effort and data completeness |

Nutrition is the most-addressed pillar (half of studies), physical activity second; **sleep has one study; the "connection" pillar has zero.** Addiction/harmful-substance interventions cluster in warnings-as-nudges.

## Two structural findings beyond the taxonomy
1. **The development pipeline:** most interventions sit at the *system-development* stage (usability, accuracy, feasibility) rather than demonstrating health-behavior outcomes — about one-third of studies remain pre-behavior-change. The review's call: move beyond system evaluation to behavior-change outcomes with RCT-scale samples.
2. **The personalization gap:** baseline self-reports are thin and interventions are not tailored to individual profiles. The named fix is exactly the AI personalization direction: comprehensive data collection (wearables, smartphone sensing, behavioral metrics) feeding recommendation-style algorithms — with the honest caveat that effectiveness depends on profile completeness.

## The cross-review context
Positioned against Forberger (workplace PA only) and Benthem de Grave (food-purchase apps only), this is the integrative map — and it converges with the library's other 2026 behavioral evidence: digital nudges work, but their value is context-dependent, and the frontier is AI-driven personalization over comprehensive user profiles (the same conclusion the `cross-cultural-llm-personalized-nudge-design` and `adaptive-digital-nudging-llm-architecture` skills hold at framework level).

## Key talking points
- **Choice architecture is the most consistently effective one-way form** — defaults, ordering, and labelling produce consistent healthy-selection effects; eco-score labels alone are weaker than labels combined with prompts or social cues.
- **Emerging-technology nudges face the novelty cliff** — smart chopsticks and VR trainers engage in trials but lack everyday practicality; adoption ≠ sustained usage.
- **Warnings risk habituation** — sensory feedback (vibrations, signage) works but decays over time.
- **The connection pillar is untouched** — no digital-nudging studies address social connection, the domain the wellness industry claims hardest.

## Pairs with
`behavioral-design-process-review-2026` (the process/monetization companion), `wellspent-customizable-screen-time-rct` (the RCT-grade single-intervention evidence), `behavior-change-synthesis-2026`, `boosting-comprehensive-framework`.

## A-Tech alignment
- **Behavioral nudging:** the category map is a selection tool — match nudge form to pillar and behavior structure before building.
- **Practical implementation:** the passive/active frame and the pipeline critique tell builders where their intervention actually sits.
- **Open source ethos:** the review's own method note — the search deliberately did NOT require the "lifestyle medicine" label to avoid excluding relevant studies — is a lesson in inclusive research design.

*Source: Taniar, King, Manger & Carlisle, "Digital nudging techniques for behaviour change in lifestyle medicine: a scoping review," Front. Digit. Health 2026;8:1799205. doi:10.3389/fdgth.2026.1799205.*