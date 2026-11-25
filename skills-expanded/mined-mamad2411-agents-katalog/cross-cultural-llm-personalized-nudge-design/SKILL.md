---
name: cross-cultural-llm-personalized-nudge-design
description: Applies LLM-informed personalized decoy nudges tailored to individual profiles and cultural contexts, validated through large-scale cross-cultural field experiments. Use when designing personalized choice-architecture interventions across multiple countries or cultures, when LLMs will be used as a low-cost testbed to pilot nudge strategies before empirical validation, or when evaluating whether decoy-based nudges generalize across cultural contexts. NOT for domains where the decoy effect is irrelevant (binary choices without a third option) or when LLM cultural bias cannot be mitigated through local fine-tuning.
---

# Cross-Cultural LLM-Personalized Nudge Design

## Overview

LLMs can design personalized decoy-based nudges tailored to individual demographic profiles and cultural contexts without costly behavioural data collection, but their effectiveness is culturally heterogeneous — validated gains of 3-7 percentage points in Germany, Singapore, and the US, with no significant effects in China or India due to LLM cultural bias from WEIRD/English-centric training data. The method positions LLMs as a low-cost testbed for piloting nudge strategies prior to empirical validation, with cultural heterogeneity as the key boundary condition.

## When to Use

- Designing personalized choice-architecture interventions (decoy effects, compromise effects, attraction effects) across multiple countries or cultural contexts
- Using LLMs to pilot and parameterize nudge strategies computationally before investing in large-scale human experiments
- Evaluating whether a nudge strategy generalizes across cultures or requires local calibration
- When you need to test hundreds of parameter configurations that would be impractical with human participants
- NOT for binary choice contexts where no third (decoy) option can be introduced
- NOT when the LLM's training data is sparse for the target culture (China, India in this study)
- NOT as a substitute for empirical validation — LLM simulations narrow the candidate space but cannot replace real-world testing

## Core Process / Workflow

### 1. Define the choice architecture

Identify the target behavior (e.g., carbon offsetting), the target option (carbon-neutral ticket), the competitor (standard ticket), and the decoy (partially offset, higher price). The decoy must be close in parameters to the target and worse along at least one dimension (asymmetrically dominated).

### 2. Define the segmentation space

Create a factorial design of demographic and attitudinal variables. In the validated study: 5 countries × 2 genders × 2 age groups × 2 income groups × 2 trust levels × 2 concern levels = 160 unique segments. Each segment becomes a distinct LLM persona.

### 3. Run LLM simulations

For each segment, prompt the LLM (GPT-4o-mini, temperature 0.8) with the segment profile as system role:

```
"You are a [man], aged [above median], permanently resides in [Singapore], 
and your monthly income is [above median]. You [concern] environment protection 
in your daily life and [believe] that the money you pay for carbon offsets 
are really used to offset emissions."
```

Present 46 choice situations per segment (pairwise + 45 decoy configurations). Randomize option order ×4; run 25 times per situation at temperature 0.8 → 100 responses per choice situation → 3,000 LLM runs per segment.

### 4. Identify optimal decoy parameters

For each country, compute:
- **Country-optimal**: decoy parameters maximizing target choice across all segments
- **Country-non-optimal**: decoy parameters minimizing target choice
- **Individual-optimal (segment-personalized)**: decoy parameters maximizing target choice for each specific segment

### 5. Validate in a preregistered human experiment

Recruit real participants (n=3,495 across 5 countries in the validated study). Present the same choice scenarios with LLM-informed decoy parameters. Compare:
- Personalized segment-optimal vs country-optimal vs no-decoy baseline

### 6. Account for cultural heterogeneity

Expect significant variation across cultures. In the validated study:
- Significant gains: Germany (+7pp), Singapore (+7pp), US (+3pp)
- No significant effect: China, India (LLM cultural bias from WEIRD training data)

**Mitigation strategies for cultural bias**:
- Use country-specific LLMs (national models emerging in Japan, China)
- Fine-tune on small-scale representative data from the target country
- Always validate empirically before deployment

## Key Empirical Findings

| Metric | Value | Context |
|---|---|---|
| Personalized vs no-decoy | +3-7pp | Germany, Singapore, US (significant) |
| Personalized vs country-optimal | +3-7pp | Same countries; personalized beats uniform |
| China, India | n.s. | No significant improvement (cultural bias) |
| Total participants | 3,495 | 5 countries, preregistered (OSF) |
| LLM segments simulated | 160 | 5 countries × 32 demographic/attitudinal combos |
| Sceptical travellers targeted | +4-8pp | Germany, Singapore, US (the hardest segment) |
| CO₂ mitigation potential | 2.3M tonnes/year | Aviation, considered countries only |

### Key discovery: LLMs are susceptible to the decoy effect themselves

LLMs reproduce the decoy effect (a classic violation of rational choice theory) because such biases are encoded in training data and reinforced during preference alignment. This has dual implications:
1. **Opportunity**: LLMs can serve as a testbed for evaluating nudge strategies computationally
2. **Concern**: When LLMs act as autonomous purchasing agents (e.g., OpenAI's Agentic Commerce Protocol), marketing strategies may shift toward nudging the agents themselves rather than human buyers

## A-Tech Applications

- **A-Coder**: Developer-productivity nudges across cultural contexts (e.g., different coding cultures in global teams); use LLM simulations to pilot before deploying
- **Be Practical**: Curriculum on cross-cultural behavioral design; teach that LLM piloting is necessary but not sufficient
- **Builder's Club**: Open-source toolkit for LLM-informed nudge design; the simulation framework is domain-independent

## Cross-References

- `llm-iterative-personalized-nudging` — Single-culture LLM nudge personalization with iterative updating; this skill adds the cross-cultural dimension
- `nudge-transparency-disclosure-effectiveness` — Transparency framework for nudges; applies to LLM-designed nudges
- `hyper-nudging-ai-personalization-ethics` — Ethical concerns about AI-personalized hyper-nudging
- `dikw-agentic-behavioral-experiment-learning` — Multi-stage experimental learning with agentic AI; complementary infrastructure

## References

- See [references/cross-cultural-nudge-evidence-base.md](references/cross-cultural-nudge-evidence-base.md) for the full study extraction.