---
name: idea-validator
description: Structured validation framework that scores product ideas. Use when evaluating problem severity, willingness-to-pay, or founder-market fit. For market intelligence, see market-research.
---

# Idea Validator Skill

## When to Use
- After completing **Phase 0 (Idea)** before entering **Phase 1 (Validation)**
- When the user proposes a new idea or pivot
- When deciding between multiple product directions
- As a sanity check before committing resources

## Tools Required

| Tool | Purpose |
|------|---------|
| `firecrawl_search` | Validate market signals, demand indicators |
| `firecrawl_extract` | Pull data from market reports, forums |

## Instructions

### 1. Collect Idea Inputs

Get from the user (or from completed Phase 0 deliverables):
- **Problem statement**: What pain does this solve?
- **Target user**: Who has this pain? (be specific: role, company size, industry)
- **Proposed solution**: How does this solve it? (one sentence)
- **Revenue model**: How does this make money?
- **Differentiator**: Why can't they just use {existing solution}?

### 2. Score on 5 Dimensions

Each dimension scored 1-5. Total score determines recommendation.

#### A. Problem Severity (1-5)
| Score | Criteria |
|-------|----------|
| 1 | Nice-to-have. Users tolerate current solutions fine. |
| 2 | Mild annoyance. Users complain but don't switch. |
| 3 | Real pain. Users actively search for alternatives. |
| 4 | Hair-on-fire. Users lose money/time daily without a solution. |
| 5 | Mission-critical. Business cannot function without solving this. |

Validate with:
```
firecrawl_search: "{problem_statement} pain point frustrated"
firecrawl_search: "site:reddit.com {target_user} struggling with {problem}"
```

#### B. Willingness to Pay (1-5)
| Score | Criteria |
|-------|----------|
| 1 | Users expect free. No existing paid solutions. |
| 2 | Users pay reluctantly. < $10/mo willingness. |
| 3 | Established paid market. $10-50/mo common. |
| 4 | Users budget for this. $50-200/mo normal. |
| 5 | Enterprise budgets. $200+/mo, multi-seat deals. |

Validate with:
```
firecrawl_search: "{category} pricing SaaS"
firecrawl_search: "{competitor} pricing plans"
```

#### C. Market Timing (1-5)
| Score | Criteria |
|-------|----------|
| 1 | Market is saturated or declining. |
| 2 | Market exists but growth is flat. |
| 3 | Growing market with room for new entrants. |
| 4 | Emerging market with strong tailwinds (AI, regulation, etc.). |
| 5 | Category creation opportunity — no one owns this yet. |

#### D. Founder-Market Fit (1-5)
| Score | Criteria |
|-------|----------|
| 1 | No domain expertise, no network, no unfair advantage. |
| 2 | Some interest but learning from scratch. |
| 3 | Adjacent experience. Understand the user but not the domain deeply. |
| 4 | Direct experience. Have felt this pain personally. |
| 5 | Deep domain expertise + network + distribution advantage. |

#### E. Execution Feasibility (1-5)
| Score | Criteria |
|-------|----------|
| 1 | Requires team of 10+, $1M+, regulatory approval. |
| 2 | Needs specialized skills the founder lacks. |
| 3 | Achievable solo with AI tools in 3-6 months. |
| 4 | MVP shippable in 30-60 days with existing tools. |
| 5 | Can validate in a weekend with no-code or AI agents. |

### 3. Generate Scorecard

```markdown
# Idea Validation Scorecard: {Idea Name}

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Problem Severity | X/5 | {one-line justification} |
| Willingness to Pay | X/5 | {one-line justification} |
| Market Timing | X/5 | {one-line justification} |
| Founder-Market Fit | X/5 | {one-line justification} |
| Execution Feasibility | X/5 | {one-line justification} |
| **TOTAL** | **XX/25** | |

## Recommendation
- 20-25: **STRONG GO** — Execute immediately.
- 15-19: **CONDITIONAL GO** — Proceed but validate {weakest dimension} first.
- 10-14: **PAUSE** — Significant risks. Pivot or de-risk before investing.
- 5-9:  **NO GO** — Fundamental problems. Explore different ideas.
```

### 4. Risk Flags

Regardless of score, flag these as deal-breakers:
- Problem Severity = 1 → "No one needs this"
- Willingness to Pay = 1 → "Can't monetize"
- Execution Feasibility = 1 → "Can't build it"

### 5. Output Format

Save to `BRAINIAC/0. Idea/VALIDATION_SCORECARD.md`

## Quality Gates
- Every score must have evidence (search result, data point, or user testimony)
- WTP score must reference actual competitor pricing
- Total recommendation must match the scoring bands exactly
