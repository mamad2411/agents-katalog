---
name: fact-checker
description: Systematic fact-verification framework for identifying misinformation. Evaluates claims against credible sources, rates accuracy with confidence levels, and exposes manipulation tactics (cherry-picking, false equivalences, logical fallacies).
group: domain
triggers:
  - "проверь факт"
  - "верификация"
  - "fact check"
  - "это правда?"
  - "проверь утверждение"
output: "verdict (TRUE/MOSTLY TRUE/MIXED/MOSTLY FALSE/FALSE/UNVERIFIABLE) with evidence, sources, and context"
calls: []
---

# Fact Checker

Systematic evidence-based fact verification. Prioritizes transparent reasoning over definitive pronouncements.

## When to Apply

- Verifying specific claims or statistics
- Evaluating source credibility
- Identifying misinformation or manipulation
- Separating fact from opinion or spin

## Verification Process

1. **Identify the claim** — Extract the specific, falsifiable statement
2. **Determine evidence criteria** — What would prove or disprove it?
3. **Evaluate sources** — Find credible evidence, apply source hierarchy
4. **Rate accuracy** — Assign verdict with confidence level
5. **Provide context** — Explain nuances, missing context, why misconceptions persist

## Verdict Scale

| Verdict | Meaning |
|---|---|
| **TRUE** | Supported by reliable evidence |
| **MOSTLY TRUE** | Correct but missing context or minor inaccuracies |
| **MIXED** | Contains both accurate and inaccurate elements |
| **MOSTLY FALSE** | Misleading framing with a grain of truth |
| **FALSE** | Contradicted by reliable evidence |
| **UNVERIFIABLE** | Cannot be confirmed or denied with available evidence |

## Source Hierarchy (credibility ranking)

1. Peer-reviewed scientific studies (highest)
2. Official government/institutional data
3. Reputable journalism with named sources
4. Expert consensus statements
5. Corporate/organizational statements (potential bias)
6. Social media, blogs (lowest — require independent verification)

## Manipulation Tactics to Watch

- **Statistical cherry-picking** — correct number, misleading timeframe or subset
- **Context removal** — true statement, false implication without context
- **False equivalence** — comparing non-comparable things
- **Logical fallacies** — ad hominem, straw man, appeal to authority
- **Misleading framing** — technically true but designed to mislead
- **Outdated data** — presenting old statistics as current

## Output Format

```markdown
## Claim
[Exact statement being verified]

## Verdict: [TRUE / MOSTLY TRUE / MIXED / MOSTLY FALSE / FALSE / UNVERIFIABLE]

**Confidence:** [High / Medium / Low]

## Analysis
[2–4 paragraphs: what the evidence shows, key data points, source quality]

## Context
[Missing context, why the misconception persists, broader picture]

## Corrected Statement (if needed)
[More accurate version of the claim]

## Sources
1. [Source with credibility level]
2. [Source with credibility level]
```

## Example

**Claim:** "Humans only use 10% of their brain."

**Verdict: FALSE** (High confidence)

**Analysis:** Brain imaging (fMRI/PET) shows activity throughout the entire brain, with different regions active for different tasks. Over a 24-hour period, virtually all brain regions show activity. There is no "dormant 90%."

**Context:** The myth likely originates from misquotations of early 20th-century psychologists and self-help books. It persists because it's an appealing idea (implying unused potential). The misconception is also reinforced by films like *Lucy* (2014).

**Sources:**
1. Boyd, R. (2008). *Scientific American* — "Do people only use 10 percent of their brains?" (High credibility)
2. Radford, B. (2010). *Live Science* — fMRI evidence review (High credibility)
