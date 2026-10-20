---
name: thinking-threatmodel
description: |
  Tests ideas, decisions, and strategies across multiple time horizons and
  threat scenarios. Inspired by Daniel Miessler's WorldThreatModelHarness.

  [WHAT] Threat modeling that tests a strategy/idea/decision against 7 time
  horizons and 5 threat dimensions. Produces a vulnerability matrix and
  recommendations.

  [WHEN] Use when: threat model, time horizons, futures analysis, future
  implications, "how does this hold up over time?", "what happens if..."

  [EXPERTISE] Threat modeling, scenario analysis, temporal risk assessment, futures thinking
argument-hint: "[strategy or decision to test]"
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
---

# Threat Model (World Threat Model)

**Role:** temporal and dimensional threat modeling.
**Tone:** analytical, concrete, honest about uncertainty.

## Method

Test the target (strategy/decision/idea) against a matrix of time horizons and threat dimensions.

### 7 time horizons

| Horizon | Timeframe | Perspective |
|---|---|---|
| H1 | 1 week | Immediate operational |
| H2 | 1 month | Tactical |
| H3 | 6 months | Project cycle |
| H4 | 1 year | Strategic |
| H5 | 3 years | Policy horizon |
| H6 | 10 years | Structural change |
| H7 | 25+ years | Generational shift |

### 5 threat dimensions (default — adapt as needed)

| Dimension | Examples |
|---|---|
| **Technological disruption** | AI breakthroughs, quantum computing, platform collapse |
| **Geopolitical shift** | Alliance break-up, trade blocs, conflicts |
| **Institutional erosion** | Disinformation, institutional capture, polarization |
| **Regulatory change** | EU legislation, data sovereignty, AI Act |
| **Economic stress** | Recession, budget cuts, funding drought |

## Output format

```markdown
## Threat Model: [The target]

### Vulnerability matrix

|  | Tech | Geopolitical | Institutional | Regulatory | Economic |
|---|---|---|---|---|---|
| H1 (1w) | ○/◐/● | ... | ... | ... | ... |
| H2 (1m) | ... | ... | ... | ... | ... |
| H3 (6m) | ... | ... | ... | ... | ... |
| H4 (1y) | ... | ... | ... | ... | ... |
| H5 (3y) | ... | ... | ... | ... | ... |
| H6 (10y) | ... | ... | ... | ... | ... |
| H7 (25y) | ... | ... | ... | ... | ... |

○ = Robust  ◐ = Vulnerable  ● = Critical vulnerability

### Critical intersections

[Where in the matrix do threats converge? Which combinations are most dangerous?]

### Top 5 threats

1. [H?/Dimension]: [Specific threat, concretely described]
2. ...

### Recommendations

[How to strengthen robustness against the identified threats?]
```

## Rules

- Be SPECIFIC per cell. "Tech could disrupt" is worthless. "GPT-6-level AI could automate the manual analysis step, undermining the team's expertise advantage" is valuable.
- Not every cell needs to be filled. Focus on ◐ and ● cells.
- Threat dimensions can be adapted to the question (e.g. add "Key-person risk" or "Climate").
