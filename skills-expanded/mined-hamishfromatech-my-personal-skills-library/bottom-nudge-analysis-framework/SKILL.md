---
name: bottom-nudge-analysis-framework
description: The BOTTOM framework (Brain, Orientation, Transparency, Triggers, Objective, Mind) — a holistic six-dimensional analysis model that integrates six validated nudge taxonomies and extends MINDSPACE. Shifts attention from fixed typologies to the underlying mechanisms through which nudges operate. Use when comparing nudges, designing behavioral interventions, evaluating nudge effectiveness across mechanisms, or analyzing dark nudges. NOT for general choice architecture (see nudge-theory-choice-architecture) or nudge transparency/autonomy research (see nudge-disclosure-transparency-effectiveness).
---

# BOTTOM: A Holistic Framework for Nudge Analysis

## The Core Problem

Research on nudges relies on several competing frameworks, making it difficult to compare interventions or identify the mechanisms that drive their effectiveness. A nudge classified under one taxonomy may be classified differently under another, and the underlying mechanism — why it works — gets lost in the typology.

BOTTOM (Brain, Orientation, Transparency, Triggers, Objective, Mind) integrates six validated taxonomies and extends the widely used MINDSPACE framework. Rather than replacing MINDSPACE, BOTTOM decomposes each of its nine nudge categories into six analytical dimensions, shifting attention from fixed typologies to the underlying mechanisms through which nudges operate.

## The Six Dimensions

### B — Brain
Which cognitive or neural mechanism does the nudge engage? Dual-process theory (System 1 vs System 2), attention allocation, reward processing, loss aversion, social cognition. The brain dimension identifies the cognitive substrate the nudge targets.

### O — Orientation
Is the nudge oriented toward automatic (System 1) or deliberative (System 2) processing? Decision structure nudges (defaults, effort, composition) tend toward automatic; decision information nudges (translation, visibility, social reference) tend toward deliberative. The orientation dimension predicts which processing mode the nudge engages.

### T — Transparency
Is the nudge visible and disclosed to the person being nudged? Transparent nudges (nudge+, boosts) engage people with their decisions; non-transparent nudges operate outside awareness. The transparency dimension addresses the ethics and autonomy implications. (Cross-references `nudge-disclosure-transparency-effectiveness` and `boosts-vs-nudges-public-preference`.)

### T — Triggers
What specific behavioral trigger does the nudge deploy? Defaults, social proof, anchors, framing, salience, commitment devices, reminders. The triggers dimension identifies the specific behavioral lever.

### O — Objective
What behavior is the nudge trying to change? Food choice, energy conservation, financial saving, health behavior, prosocial action. The objective dimension contextualizes the nudge within its behavioral domain. (Cross-references the PNAS meta-analysis finding that food choices are 2.5× more responsive than financial decisions.)

### M — Mind
What is the target psychological state or mental model? Attitude change, norm activation, preference construction, habit formation, identity shift. The mind dimension identifies the psychological outcome the nudge aims to produce.

## How BOTTOM Extends MINDSPACE

MINDSPACE (Messenger, Incentives, Norms, Defaults, Salience, Priming, Affect, Commitment, Ego) is a widely used nine-category framework for classifying nudges. Its limitation: it is a typology, not a mechanism analysis. Two nudges in the same MINDSPACE category may operate through entirely different mechanisms.

BOTTOM decomposes each MINDSPACE category across the six dimensions. For example:
- **Defaults** (MINDSPACE: Defaults) → BOTTOM: Brain=loss aversion/status quo bias; Orientation=automatic; Transparency=variable; Triggers=preselection; Objective=context-dependent; Mind=preference construction via inertia
- **Social norms** (MINDSPACE: Norms) → BOTTOM: Brain=social cognition; Orientation=automatic; Transparency=typically visible; Triggers=social reference; Objective=context-dependent; Mind=norm activation

This decomposition reduces inconsistencies arising from the arbitrary use of a single classification system and enables comparison of nudges that appear in different MINDSPACE categories but share underlying mechanisms.

## Application Examples

### Nudges to Increase Vegetable Consumption
A default nudge (preselecting vegetable side dishes) and a salience nudge (placing vegetables at eye level) appear in different MINDSPACE categories (Defaults vs Salience) but share the Orientation dimension (both automatic) and the Objective dimension (both food choice). BOTTOM reveals they may be combined or compared on the mechanism they share, not just the category they differ on.

### Vaccine Adherence
A social norm nudge ("most people in your area got vaccinated") and a reminder nudge (SMS appointment reminder) differ in Brain (social cognition vs attention), Triggers (social reference vs reminder), and Mind (norm activation vs intention reinforcement) but share Orientation (both can be automatic) and Objective (health behavior). BOTTOM enables analysis of which mechanism is more effective for which population.

### Dark Nudges in Financial Decision-Making
A dark nudge (e.g., hiding the opt-out from a subscription default) can be analyzed across all six dimensions: Brain=loss aversion; Orientation=automatic; Transparency=low (the ethical problem); Triggers=preselection+friction; Objective=financial commitment; Mind=preference construction via inertia. The Transparency dimension makes the ethical problem visible and comparable across dark nudge variants.

## The Mechanism Shift

The key contribution of BOTTOM is shifting analysis from "what type of nudge is this?" (typology) to "through what mechanism does this nudge operate?" (mechanism). This matters because:

1. **Comparison across taxonomies** — Nudges classified differently under MINDSPACE, TIPPME, or other frameworks can be compared on shared mechanisms.
2. **Mechanism-based design** — Instead of choosing a nudge type, designers choose a mechanism and then select the trigger that best deploys it.
3. **Dark nudge analysis** — The Transparency dimension makes ethical problems visible and comparable, regardless of the nudge's typological category.
4. **Meta-analytic research** — The 789-intervention database (Gandhi et al., 2026) coded on 298 variables enables mechanism-based meta-analysis rather than just type-based aggregation.

## Connection to the PNAS Meta-Analysis

The PNAS meta-analysis (Mertens et al., 2021, 447 effect sizes, n=2,148,439) found:
- Overall effect size Cohen's d = 0.43 (small to medium)
- Decision structure interventions consistently outperform decision information and decision assistance
- Food choices 2.5× more responsive than financial decisions
- ~15% of interventions backfire

BOTTOM explains **why** decision structure outperforms: decision structure nudges share the Orientation dimension (automatic processing) and require lower cognitive engagement, while decision information nudges require deliberative processing that exceeds cognitive limits under load. The mechanism (automatic vs deliberative) explains the effectiveness difference that the typology (structure vs information) only describes.

## A-Tech Values Alignment

| Value | Alignment |
|---|---|
| **Open-source AI** | The 789-intervention database is an open resource; BOTTOM is an open analytical framework |
| **Data privacy** | BOTTOM enables analysis of nudges without requiring personal data collection — the framework analyzes the nudge design, not the nudged individual |
| **Financial freedom** | The dark-nudge-in-finance analysis dimension directly serves financial-freedom values by making manipulative mechanisms visible |
| **Practical implementation** | Six dimensions + MINDSPACE decomposition + three application examples + dark nudge analysis |

## Practical Implementation for A-Tech

### A-Coder
- BOTTOM can analyze the nudges embedded in developer tool UX: defaults (Orientation=automatic, Transparency=variable), social proof (Brain=social cognition), salience (Triggers=attention). The Transparency dimension reveals which UX patterns are ethical and which are dark.
- The mechanism shift applies to onboarding design: instead of "should we use a default or a social norm?", ask "which mechanism (inertia vs norm activation) is more effective for this developer population?"

### Be Practical
- BOTTOM is a teachable critical-thinking framework: "through what mechanism does this nudge operate?" applies to consumer protection, financial literacy, and health behavior.
- The dark-nudge analysis dimension is directly relevant to Be Practical's financial-freedom curriculum.

### Builder's Club
- The framework enables community-contributable nudge analysis without requiring behavioral data collection.
- The Transparency dimension becomes a community standard for ethical nudge design.

## Cross-References to Existing Skills

- **`nudge-theory-choice-architecture`** — Foundational nudge theory. BOTTOM extends this with mechanism-based analysis.
- **`nudge-disclosure-transparency-effectiveness`** — Transparency research. BOTTOM's Transparency dimension integrates this.
- **`boosts-vs-nudges-public-preference`** — Boosts vs nudges. BOTTOM's Orientation dimension (automatic vs deliberative) maps to this distinction.
- **`boosting-empowering-behavior-change`** — Empowering behavior change. BOTTOM's Mind dimension (target psychological state) connects to this.
- **`digital-nudging-ethical-persuasion`** — Ethical persuasion. BOTTOM's Transparency dimension operationalizes the ethics.
- **`gap-behavioral-science-framework`** — GAP framework. BOTTOM is complementary — GAP is a design process; BOTTOM is an analysis framework.
- **`behavior-change-synthesis-2026`** — Behavior change synthesis. BOTTOM provides the mechanism-analysis layer.

## Anti-Patterns

- **Treating BOTTOM as a replacement for MINDSPACE** — BOTTOM extends MINDSPACE by decomposing its categories, not replacing them. Use both: MINDSPACE for classification, BOTTOM for mechanism analysis.
- **Analyzing nudges without the Transparency dimension** — The Transparency dimension is what makes ethical problems visible. Skipping it produces mechanism analysis without ethical analysis.
- **Conflating typology with mechanism** — Two nudges in the same MINDSPACE category may operate through different mechanisms. Always decompose across all six dimensions.
- **Ignoring the meta-analytic evidence** — The PNAS meta-analysis (d=0.43, decision structure > decision information, food > finance, 15% backfire) provides the empirical baseline. BOTTOM explains the mechanism behind these findings.

## The Key Insight

The contest in nudge design is no longer "which type of nudge?" (the typological question) but "through what mechanism?" (the mechanism question). BOTTOM shifts the analytical frame from classification to mechanism, enabling comparison across taxonomies, mechanism-based design, ethical analysis of dark nudges, and meta-analytic research that aggregates by mechanism rather than by type. The mechanism explains the effectiveness; the typology only describes it.