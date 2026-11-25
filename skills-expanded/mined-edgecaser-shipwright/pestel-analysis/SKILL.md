---
name: pestel-analysis
description: "Scans the macro environment across Political, Economic, Social, Technological, Environmental, and Legal dimensions to identify strategic risks and tailwinds. Produces a structured assessment useful for strategy documents, investor updates, and risk registers."
category: strategy
default_depth: standard
---

# PESTEL Analysis

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Scans the macro environment across Political, Economic, Social, Technological, Environmental, and Legal dimensions to identify strategic risks and tailwinds. Produces a structured assessment useful for strategy documents, investor updates, and risk registers.

## When to Use

- Annual strategy planning
- Entering a new market or geography
- Assessing regulatory risk for a product area
- Board or investor preparation
- Due diligence on an acquisition target

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick risk scan for a product decision or feature bet | Top 2-3 most relevant PESTEL dimensions only, no Priority Matrix |
| **Standard** | Annual strategy planning or new market entry | Executive Summary + All 6 dimensions + Priority Matrix + Monitoring Plan |
| **Deep** | Board preparation, M&A due diligence, or regulatory filing support | All sections + scenario modeling per Act Now factor, regulatory timeline mapping, cross-dimension interaction analysis |

**Omit rules:** At Light depth, skip dimensions with no material impact and omit the Priority Matrix and Monitoring Plan. Produce only dimension tables for the 2-3 factors most likely to affect the decision at hand.

## Framework

### For Each PESTEL Dimension

Analyze the external factors that could materially impact the product or business:

```markdown
## Political
| Factor | Impact | Likelihood | Timeframe | Implication |
|---|---|---|---|---|
| [e.g., Data sovereignty regulations] | High / Med / Low | High / Med / Low | Near / Mid / Long | [What it means for us] |

**Key signals to monitor:**
- [Signal 1]
- [Signal 2]

## Economic
| Factor | Impact | Likelihood | Timeframe | Implication |
|---|---|---|---|---|
| [e.g., Enterprise IT budget contraction] | ... | ... | ... | ... |

## Social
| Factor | Impact | Likelihood | Timeframe | Implication |
|---|---|---|---|---|
| [e.g., Remote work normalization] | ... | ... | ... | ... |

## Technological
| Factor | Impact | Likelihood | Timeframe | Implication |
|---|---|---|---|---|
| [e.g., LLM commoditization] | ... | ... | ... | ... |

## Environmental
| Factor | Impact | Likelihood | Timeframe | Implication |
|---|---|---|---|---|
| [e.g., Carbon reporting requirements] | ... | ... | ... | ... |

## Legal
| Factor | Impact | Likelihood | Timeframe | Implication |
|---|---|---|---|---|
| [e.g., AI regulation frameworks] | ... | ... | ... | ... |
```

### Scoring Criteria

**Impact:** How much would this change our strategy or performance?
- **High:** Forces a strategic pivot or creates a major new opportunity
- **Medium:** Requires meaningful adaptation but doesn't change direction
- **Low:** Minor adjustments needed

**Likelihood:** How probable is this factor materializing?
- **High:** Already happening or near-certain
- **Medium:** Plausible, evidence emerging
- **Low:** Possible but speculative

**Timeframe:**
- **Near:** 0-12 months
- **Mid:** 1-3 years
- **Long:** 3+ years

### Priority Matrix

Plot the highest-impact factors:

```markdown
## Priority Matrix

### Act Now (High Impact × High Likelihood × Near)
1. [Factor], [recommended action]

### Prepare (High Impact × Medium Likelihood × Mid)
1. [Factor], [contingency to develop]

### Monitor (Medium Impact or Low Likelihood)
1. [Factor], [signal to watch for]

### Acknowledge (Low Impact)
1. [Factor], [noted, no action needed]
```

## Minimum Evidence Bar

**Required inputs:** Product or business description, target market or geography, and the strategic decision this analysis is informing.

**Acceptable evidence:** Published regulation or pending legislation, government agency announcements, industry analyst reports, macroeconomic data (central bank rates, inflation indices), trade press, peer-reviewed research, company filings.

**Insufficient evidence:** If a PESTEL dimension relies only on speculation with no published source or observable trend, produce a partial artifact with unsupported dimensions marked `[TBD, requires: published sources, regulatory filings, or industry data for this dimension]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Factors scored High Impact or High Likelihood must cite a specific source, regulation, or data point.
- **Hypotheses:** Medium/Low likelihood factors and long-timeframe trends may be directional, must be labeled as emerging signals, not established facts.

## Output Format

Produce a PESTEL report with:
1. **Executive Summary**, top 3-5 macro factors that matter most
2. **Dimension Analysis**, each PESTEL dimension with factors, scores, and implications
3. **Priority Matrix**, categorized by urgency
4. **Monitoring Plan**, signals to watch and review cadence

**Shipwright Signature (required closing):**
5. **Decision Frame**, Which macro factors to act on vs. monitor, key trade-off, confidence with evidence quality, owner, decision date, revisit trigger
6. **Unknowns & Evidence Gaps**, Pending legislation outcomes, unconfirmed regulatory timelines, emerging technology trajectories without consensus
7. **Pass/Fail Readiness**, PASS if at least 4 dimensions have sourced factors and the Priority Matrix is populated (Act Now items required only if factors meet the High Impact × High Likelihood × Near-term threshold; if none qualify, explicit declaration is sufficient) (at Light depth: PASS if the 2-3 included dimensions have sourced factors, Priority Matrix is deferred); FAIL if factors are generic trends not tied to the specific product or market
8. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Listing everything**, Focus on factors that could materially affect *your* product, not every macro trend
- **No implications**, A factor without a "so what?" is trivia, not analysis
- **Ignoring positive factors**, PESTEL isn't just risk; it surfaces tailwinds too
- **Static analysis**, The macro environment shifts; build a monitoring plan, not a one-time document
- **Confusing categories**, If a factor fits multiple categories, put it in the one most relevant to the action you'd take

## Weak vs. Strong Output

**Weak:**
> **Technological:** AI is changing everything. Impact: High. Likelihood: High.

No specificity on which AI development, no implication for this product, no actionable signal to monitor.

**Strong:**
> **Technological:** LLM inference costs dropped 90% in 18 months (GPT-4 $30/1M tokens → GPT-4o-mini $0.15/1M tokens, source: OpenAI pricing 2024). Impact: High. Likelihood: High (already happening). Implication: Competitors with larger engineering teams can now ship AI features at near-zero marginal cost, our 6-month head start on fine-tuned models is eroding.

Sourced data point, quantified trend, and a product-specific implication that drives action.
