---
name: boosting-comprehensive-framework
description: Applies the Herzog & Hertwig (Annual Review of Psychology 2025) comprehensive boosting framework for empowering citizens with behavioral science. Use when designing competence-building interventions, choosing between nudging and boosting, or fostering citizen agency.
---

# Boosting: A Comprehensive Framework for Competence-Building

## Overview

Boosting is a behavioral public policy approach focused on *empowering citizens* by building their competences — the skills, heuristics, and decision strategies that improve their ability to navigate complex environments autonomously. Where nudging modifies the choice environment to steer behavior, boosting targets the person's capacity to make better choices across any environment. Herzog & Hertwig's (2025) comprehensive framework in the *Annual Review of Psychology* synthesizes the theoretical foundations, empirical evidence, and practical applications of boosting across six competence domains. This skill applies that framework to A-Tech's open-source, privacy-first, autonomy-respecting ethos: boosting is the behavioral science approach most aligned with empowering users rather than optimizing them.

## When to Use

- Designing competence-building interventions (teaching heuristics, decision rules, critical thinking skills)
- Choosing between nudging and boosting for a given behavioral problem
- Fostering user/citizen agency and autonomy in product design
- Building digital literacy, financial literacy, or health literacy features
- Designing interventions against misinformation and manipulation
- Creating self-nudging tools that put choice architecture in the user's hands

NOT for:
- Situations requiring immediate behavior change without user cooperation (use nudging — see `nudging-meta-analysis-effectiveness`)
- Covert behavioral influence (boosts are necessarily transparent and require active participation)
- High-stakes environments where users lack the cognitive resources to apply learned competences

## Core Distinction: Boosting vs. Nudging

| Dimension | Nudging | Boosting |
|-----------|---------|----------|
| **Target** | Behavior (the choice made) | Competence (the capacity to choose) |
| **Mechanism** | Modifies choice environment | Teaches skills, heuristics, rules |
| **User cooperation** | Not required (works on passive users) | Required (can be refused) |
| **Transparency** | Debated (some nudges work better when hidden) | Necessarily transparent (you can't learn a skill without knowing you're learning it) |
| **Duration** | Often short-term (effect fades when nudge removed) | Often long-term (competence persists) |
| **Autonomy** | May reduce autonomy (chooses for you) | Enhances autonomy (enables you to choose better) |
| **Generalizability** | Context-specific (works in the nudged environment) | Transferable (competence works in any environment) |
| **Ethical profile** | Paternalism concerns | Empowerment-oriented |

**Key insight:** Boosting and nudging are not competitors — they are complementary. The question is not "which is better?" but "which fits this problem?" See the decision framework below.

## The Six Competence Domains

Herzog & Hertwig organize boosts into six domains of competence. Each domain includes specific, evidence-based boosting techniques.

### 1. Risk Competences

**Goal:** Enable people to understand and act on risk information accurately.

**Boosts:**
- **Fact boxes:** Standardized visual format presenting absolute risks, relative risks, and baseline rates in a single panel. Eliminates the framing effects that distort risk perception.
- **Visual representations:** Icon arrays (e.g., 100 figures with affected ones highlighted) make base rates tangible. Forest plots for treatment effect comparisons.
- **Interactive simulations:** Let users experience risk distributions (e.g., sampling from a probability distribution) to build intuitive understanding of variance and uncertainty.
- **Natural frequencies:** Present probabilities as natural frequencies (e.g., "1 in 1,000" rather than "0.1%") — reduces confusion and improves Bayesian reasoning. Gigerenzer's foundational finding.

**Application:** Health risk communication, financial risk disclosure, AI model confidence/uncertainty communication.

### 2. Financial Competences

**Goal:** Enable people to make better financial decisions without requiring expert knowledge.

**Boosts:**
- **Heuristics:** Simple rules of thumb (e.g., "save 10% of income automatically," "never carry a credit card balance") that outperform complex optimization in noisy environments
- **Rule of 72:** Quick mental math for compound growth (72 ÷ interest rate ≈ years to double). Builds intuitive understanding of compounding.
- **Accounting routines:** Simple categorization and tracking routines (e.g., envelope budgeting, zero-based budgeting) that make financial flows visible

**Application:** Personal finance tools, financial wellness features, investment decision support. Note: the nudging meta-analysis found financial domain least responsive to nudges (d = 0.24) — boosting is the better fit for financial behavior change.

### 3. Judgment and Decision-Making Competences

**Goal:** Improve the quality of decisions under uncertainty and complexity.

**Boosts:**
- **One-reason heuristics:** Decision rules that use a single best predictor (e.g., "choose the option that scores highest on the most important criterion") — often outperform complex multi-attribute models in noisy environments (Gigerenzer & Goldstein)
- **Simple decision trees:** 2–3 branch trees that guide classification decisions (e.g., emergency triage trees, "is this email phishing?" decision aids)
- **Tallying:** Count positive features across options without weighting — robust when cue weights are unknown or unreliable

**Application:** Product decision aids, comparison tools, AI-assisted decision support that teaches (not replaces) human judgment.

### 4. Digital World Competences

**Goal:** Enable people to navigate the digital information ecosystem critically and resist manipulation.

**Boosts:**
- **Critical ignoring:** The skill of *not* attending to low-quality information. Distinct from critical thinking (which engages with content) — critical ignoring is about strategic inattention. Includes do-not-engagement rules.
- **Lateral reading:** Verify claims by leaving the source and checking other sources (the method professional fact-checkers use), rather than vertical reading (analyzing the source itself for credibility cues)
- **Psychological inoculation against misinformation:** Pre-exposure to weakened forms of manipulation techniques (false dichotomy, emotional language, ad hominem) builds "antibodies" — resistance to future manipulation. Like vaccination for reasoning.
- **Self-nudging via one sec app:** The *one sec* app introduces friction before opening addictive apps (a 10-second breathing delay before Instagram opens). This is self-nudging: the user sets their own choice architecture. Bridges boosting and nudging — the user builds the competence of self-regulation by designing their own friction.

**Application:** Misinformation defense, digital wellbeing features, media literacy tools, anti-manipulation training. Core to A-Tech's autonomy-supportive mission.

### 5. Motivational Competences

**Goal:** Help people align their actions with their intentions and values.

**Boosts:**
- **Temptation bundling:** Pair a "want-to-do" behavior with a "should-do" behavior (e.g., only listen to favorite podcast while exercising). Builds the competence of self-regulation through strategic reward coupling.
- **MCII (Mental Contrasting with Implementation Intentions):** Four-step technique: (1) identify desired outcome, (2) imagine best outcome, (3) identify main obstacle, (4) form if-then plan to overcome obstacle. Evidence-based goal-strategy that outperforms pure positive thinking.
- **Dutch Reach:** A physical competence boost — open car door with the far hand, forcing body rotation to look for cyclists. A motor skill that becomes automatic and prevents "dooring" accidents. Demonstrates that boosts can be physical, not just cognitive.

**Application:** Habit formation features, goal-setting tools, health behavior change, safety training.

### 6. Health Competences

**Goal:** Build capacities for healthier behavior through routines and skills.

**Boosts:**
- **Family meal routines:** Establishing regular family meal patterns improves nutrition, family cohesion, and child development outcomes. A routine-based boost rather than an information-based intervention.
- **Mental health apps:** Evidence-based apps teaching cognitive-behavioral techniques (e.g., mood tracking + cognitive restructuring) build psychological competences. Must be evaluated for evidence quality — many apps lack empirical support.

**Application:** Health and wellness features, mental health tools, preventive health routines.

## Self-Nudging as Citizen Choice Architecture

A key insight from the framework: **self-nudging** bridges the nudge-boost distinction. When users design their own choice architecture (setting their own defaults, adding their own friction, choosing their own commitment devices), they are:

1. **Nudging themselves** — modifying their choice environment
2. **Boosting their competence** — developing self-regulation skills through the act of designing their architecture

The *one sec* app is the paradigmatic example: the user installs friction against their own impulsive app use. This is:
- **Transparent** (the user knows exactly what they're doing)
- **Cooperative** (the user opts in)
- **Competence-building** (the skill of self-regulation improves over time)
- **Autonomy-enhancing** (the user is the architect, not the subject)

**A-Tech application:** Build tools that let users design their own choice architecture. This is the most ethically aligned form of behavioral design — it respects autonomy while still applying behavioral science.

## The Ultra-Processed Environments Problem

Herzog & Hertwig frame a critical challenge: modern environments are "ultra-processed" — engineered to exploit cognitive biases at industrial scale (addictive app design, hyper-palatable food, attention-harvesting media). In such environments:

- **Nudging alone is insufficient** — the environment is already aggressively architected against the user's interests
- **Boosting becomes necessary** — users need competences to resist and navigate hostile choice architecture
- **The combination is ideal** — regulate the environment (structural nudges/policy) while building user competences (boosts)

**Implication for A-Tech:** In AI-augmented environments (algorithmic feeds, AI-personalized persuasion, deepfakes), boosting digital world competences is not optional — it is defensive infrastructure. Users need critical ignoring, lateral reading, and psychological inoculation to function in AI-saturated information environments.

## When to Boost vs. Nudge: Decision Framework

| Condition | Boost | Nudge |
|-----------|-------|-------|
| User needs lasting competence that transfers across contexts | ✅ | ❌ |
| User needs immediate behavior change without cooperation | ❌ | ✅ |
| The environment is "ultra-processed" / hostile | ✅ (defensive) | ✅ (environmental) |
| Problem is high-stakes and deliberative (e.g., financial) | ✅ | ⚠️ (weak, d ≈ 0.24) |
| Problem is low-stakes and habitual (e.g., food choice) | ⚠️ (overkill) | ✅ (d ≈ 0.65) |
| User agency and autonomy are the priority | ✅ | ⚠️ |
| You can change the choice environment/defaults | ❌ | ✅ (d ≈ 0.62) |
| You can teach a simple, robust heuristic | ✅ | ❌ |
| Transparency is non-negotiable | ✅ (necessarily transparent) | ⚠️ (debated) |
| User has cognitive/motivational resources to learn | ✅ | N/A |
| User lacks cognitive resources / is in crisis | ❌ | ✅ |

**Practical heuristic:** If you can change a default, nudge. If the user needs a skill that will outlast any single choice environment, boost. If the environment is hostile and exploitative, boost defensively *and* advocate for environmental regulation.

## Limits and Critiques of Boosting

### The Trap of Individualizing Responsibility
- Boosting places the burden of improvement on the individual: "if you're being manipulated, learn to resist it"
- This can let environment designers (platforms, advertisers) off the hook — they created the hostile environment
- **Mitigation:** Pair boosting with environmental/policy advocacy. Don't boost users into resilience while leaving the hostile architecture intact.

### Cognitive and Motivational Requirements
- Boosts require users to have the cognitive capacity and motivation to learn
- Users in crisis, under cognitive load, or with low literacy may not benefit
- **Mitigation:** Calibrate boost complexity to user capacity. Offer scaffolding. Don't assume universal cognitive availability.

### Social Inequality
- Boosts may benefit those who already have resources (education, time, cognitive bandwidth) — widening rather than narrowing gaps
- The well-resourced learn the heuristics faster and apply them more effectively
- **Mitigation:** Target boost delivery to under-reserved populations. Design boosts that require minimal prior knowledge. Integrate boosts into universal-access platforms (public education, healthcare, government services).

## A-Tech Alignment

### Open-Source
- The boosting research community maintains **scienceofboosting.org** — an open-access resource for boosting techniques, evidence, and implementations
- Boost techniques (fact boxes, icon arrays, decision trees, heuristics) are implementable in open-source code — no proprietary dependency
- Psychological inoculation games and lateral reading trainers are available as open-source educational tools
- A-Tech principle: boosting tools should be open-source by default — competences are public goods, not proprietary features

### Data Privacy
- Boosting *enhances* user autonomy — it does not require personal data collection, behavioral tracking, or biometric measurement
- Self-nudging tools (like *one sec*) operate entirely on-device — no server-side data collection needed
- Critical ignoring and lateral reading competences inherently reduce data exposure (users learn to withhold engagement from data-harvesting sources)
- A-Tech principle: boosting is the most privacy-aligned behavioral science approach — it empowers users to protect themselves rather than surveilling them to protect them

### Financial Freedom
- Financial competence boosts (rule of 72, simple heuristics, accounting routines) directly serve financial freedom — they build lasting capacity for financial decision-making
- Unlike financial nudges (which have weak effects, d ≈ 0.24), financial boosts build transferable competence
- A-Tech principle: financial freedom is a competence, not a nudge. Teach the heuristics, don't just change the default.

### Practical Implementation
- Table 1 in Herzog & Hertwig (2025) provides concrete examples for each competence domain — directly implementable
- Six domains with specific techniques = a menu of immediately actionable boost designs
- Self-nudging pattern (user-designed choice architecture) is a product feature pattern, not just a theory
- The nudge-vs-boost decision framework is a practical tool for product teams choosing behavioral design strategies

## Cross-References

- See `behavioral-psychology-and-nudging/nudging-meta-analysis-effectiveness` for the empirical evidence on when nudging works (and when it doesn't) — the complement to this boosting framework
- See `behavioral-psychology-and-nudging/boosts-vs-nudges-public-preference` for public perception data on boost vs. nudge acceptance
- See `behavioral-psychology-and-nudging/boosting-empowering-behavior-change` for the foundational boosting approach
- See `behavioral-psychology-and-nudging/habit-stacking-implementation-intentions` for MCII and implementation intentions in depth
- See `behavioral-psychology-and-nudging/digital-nudging-ethical-persuasion` for the ethical framework around digital behavioral influence
- See `community-and-growth/autonomy-supportive-marketing` for autonomy-respecting marketing approaches aligned with boosting philosophy
- See `community-and-growth/algorithmic-aversion-defense` for digital world competences against algorithmic manipulation
- See `privacy-and-trust/privacy-by-design-generative-ai` for privacy-preserving AI architecture that complements user competence-building

## Sources

- Herzog, S. M., & Hertwig, R. (2025). Boosting: A comprehensive framework for empowering citizens with behavioral science. *Annual Review of Psychology*, 76.
- Hertwig, R., & Grüne-Yanoff, T. (2017). Nudging and boosting: Steering or empowering good decisions. *Perspectives on Psychological Science*, 12(6), 973–986.
- Gigerenzer, G. (2014). *Risk Savvy: How to Make Good Decisions*. Viking. (Natural frequencies, rule of 72, simple heuristics)
- Gigerenzer, G., & Goldstein, D. G. (1996). Reasoning the fast and frugal way. *Psychological Review*, 103(4), 650–669. (One-reason heuristics, tallying)
- Roozenbeek, J., & van der Linden, S. (2019). Fake news game confers psychological resistance against online misinformation. *Palgrave Communications*, 5, 65. (Psychological inoculation)
- scienceofboosting.org — open-access boosting resources and technique library
- one sec app — self-nudging friction tool for digital wellbeing