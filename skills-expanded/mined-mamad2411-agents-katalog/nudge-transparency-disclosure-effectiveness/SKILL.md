---
name: nudge-transparency-disclosure-effectiveness
description: Applies the disclosure transparency framework for nudging interventions, distinguishing four disclosure types (presence, purpose, mechanism, combined) and their differential effects on nudge effectiveness and perceived autonomy. Use when designing transparent nudging systems, evaluating whether disclosures help or harm nudge effectiveness, or studying the autonomy-effectiveness trade-off in behavioral interventions. NOT for covert nudging, manipulative choice architecture, or contexts where transparency is legally mandated without behavioral evaluation.
---

# Nudge Transparency Disclosure Effectiveness

## Core Concept

Cuypers, Raymaekers & Van de Walle (Behavioural Public Policy, May 2026) conducted a vignette survey experiment (n=1,916) measuring how different types of transparency disclosures influence both nudge effectiveness and perceived autonomy. The study tested a salience nudge for sustainable food choices with four disclosure types, revealing that disclosures neither enhance nor reduce nudge effectiveness, but also cannot offset the small autonomy decrease that nudges themselves cause.

## The Four Disclosure Types

Following de Ridder et al. (2022), disclosures are categorized by fundamental communication elements (Lasswell, 1948):

| Disclosure Type | Content | Example |
|---|---|---|
| **Presence** | Informs that behavioral techniques are used | "Behavioural insights are used to make certain dishes more visible" |
| **Purpose** | Communicates the policy goal | "Helping people make more sustainable choices" |
| **Mechanism** | Explains how the nudge works | "Visual elements increase salience and attractiveness of sustainable dishes" |
| **Combined** | All three: presence + purpose + mechanism | Full transparency disclosure |

## Key Findings

### Nudge Effectiveness
- The salience nudge **was effective**: +10.4 percentage point increase in sustainable dish selection (Wald=7.50, p=0.006)
- **No disclosure significantly changed nudge effectiveness** — neither enhanced nor reduced it
- Combined disclosure group had highest sustainable choices (46.4%) but not significantly different from nudge-only (43.4%)
- TOST equivalence tests: Mechanism disclosure statistically equivalent to nudge-only

### Perceived Autonomy
- The nudge itself caused a **small but significant decrease** in perceived autonomy (-2.4 percentage points)
- **No disclosure offset this autonomy decrease**
- Three of four disclosures (Presence, Mechanism, Combined) were statistically equivalent to nudge-only on autonomy
- Purpose disclosure showed no significant difference from control on autonomy (potential but inconclusive mitigation)

### Disclosure Awareness
- 40.8% failed nudge awareness check (didn't notice the "chef's choice" nudge)
- 40.0% failed disclosure awareness check (didn't notice the disclosure)
- High failure rates are consistent with transparent nudging literature

## Theoretical Implications

### Persuasion Knowledge Model (Friestad & Wright, 1994)
- When information is incomplete, people rely on skeptical assumptions about agent's intentions
- **Type interference** presence disclosures (general, no specifics) should be most susceptible to triggering suspicion
- Finding: presence disclosure did NOT trigger reactance or reduce effectiveness — contradicts theoretical expectation

### Self-Determination Theory (Deci & Ryan, 2000)
- Understanding intervention rationale allows internalization of behavior → experienced as self-endorsed
- Purpose disclosure should enhance autonomy by clarifying intent
- Finding: purpose disclosure did NOT significantly enhance autonomy — contradicts theoretical expectation

### Psychological Reactance (Brehm, 1966)
- Perceived autonomy threat triggers reactance → deliberate choice of alternatives
- Finding: no evidence of reactance from any disclosure type

## The Central Tension

**Disclosures can be applied without compromising nudge effectiveness, but they are not sufficient to mitigate concerns about autonomy in nudging interventions.**

This creates a practical dilemma:
- Transparency advocates argue disclosures protect autonomy
- Effectiveness advocates worry disclosures undermine nudge impact
- **Evidence**: Neither side is right — disclosures don't help autonomy and don't hurt effectiveness

## Salience vs. Default Nudges

This study tested **salience nudges** (making options more noticeable), which are theoretically more overt than **default nudges** (preselecting options). The existing transparency literature is dominated by default nudge studies. Key difference:

- **Default nudges**: covert, rely on inertia, frequently seen as autonomy-threatening
- **Salience nudges**: overt, guide attention, theoretically more transparent

The finding that even salience nudges reduce perceived autonomy (slightly) suggests autonomy concerns extend beyond default nudges.

## Limitations and Future Directions

1. **Vignette methodology**: hypothetical scenarios may not fully simulate real-world complexity
2. **Single nudge type**: salience food choice; results may not generalize to all nudge types
3. **No direct transparency perception measure**: can't confirm disclosures were experienced as transparency-enhancing
4. **Low attention**: 40%+ failure rates on manipulation checks; disclosures may not reach their audience
5. **Autonomy construct heterogeneity**: freedom of choice, agency, self-constitution may not form a coherent construct

## A-Tech Applications

- **A-Coder**: Transparent nudge design for developer productivity features (disclose presence, purpose, mechanism without fearing effectiveness loss)
- **Be Practical**: Behavioral intervention transparency curriculum (disclosure design, autonomy-effectiveness trade-off)
- **Builder's Club**: Open-source nudge transparency framework (disclosure templates, A/B testing protocols)

## Cross-References

- `llm-iterative-personalized-nudging` — LLM-personalized nudges should include disclosure design; this skill provides the disclosure framework
- `llm-agent-nudge-sensitivity` — LLMs are more nudge-sensitive than humans; disclosure design must account for this
- `nudge-persistence-technology-adoption` — Persistence mechanisms are orthogonal to disclosure; both can coexist
- `bottom-nudge-analysis-framework` — BOTTOM framework for nudge classification; this skill adds the transparency dimension
- `optimal-nudging-resource-rational-framework` — Resource-rational optimal nudges; disclosure doesn't affect optimality

## A-Tech Alignment

| Value | Alignment |
|---|---|
| Open-source AI | Open access (Creative Commons); preregistered at OSF; R analysis code published |
| Data privacy | Flemish representative sample; GDPR-compliant; anonymous responses |
| Financial freedom | Transparent nudges maintain effectiveness → no cost to policy goals; disclosures are free to implement |
| Practical implementation | Vignette experiment; 1,916 participants; preregistered; R code available; directly applicable to nudge design |