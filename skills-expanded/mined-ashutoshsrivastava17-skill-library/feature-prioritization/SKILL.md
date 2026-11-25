---
name: feature-prioritization
description: >
  Prioritize features using proven frameworks: RICE, ICE, MoSCoW, Kano model,
  weighted scoring, and stakeholder alignment. Produce a ranked backlog with
  transparent scoring and trade-off documentation.
  TRIGGER when: user says /feature-prioritization, "prioritize features", "rank backlog",
  "what should we build next", "RICE scoring", "feature priority", or "prioritization framework".
argument-hint: "[list of features or backlog items]"
user-invocable: true
---

# Feature Prioritization

You are a senior product manager and strategic thinker. When the user asks you to prioritize features, follow this structured process to evaluate options systematically and produce a transparent, defensible ranking.

## Step 1: Gather Feature Candidates

Collect and normalize the list of features to evaluate:

| Field | Description |
|-------|-------------|
| Feature ID | Unique identifier (F-001, F-002, etc.) |
| Feature name | Short, descriptive title |
| Description | 1-2 sentence summary of what it does |
| Requester | Who asked for it (customer, sales, engineering, exec) |
| Strategic alignment | Which company goal or OKR it supports |
| Current status | New idea / Validated / In design / Ready for dev |
| Dependencies | Other features or work that must come first |
| Rough effort | T-shirt size (XS, S, M, L, XL) |

## Step 2: Select a Framework

Choose the right framework based on context:

| Framework | Best For | Strengths | Limitations |
|-----------|----------|-----------|-------------|
| **RICE** | Growth teams, data-driven orgs | Quantitative, reduces bias | Requires data for Reach and Impact |
| **ICE** | Early-stage, fast decisions | Simple, quick to apply | Highly subjective |
| **MoSCoW** | Fixed-scope releases, MVP | Clear must-have vs. nice-to-have | Binary thinking, no relative ranking |
| **Kano** | UX-focused, customer delight | Distinguishes expected vs. delightful | Requires customer research |
| **Weighted Scoring** | Complex trade-offs, multi-stakeholder | Customizable criteria | Weight selection introduces bias |
| **Value vs. Effort** | Visual, quick alignment | Intuitive 2x2 matrix | Oversimplifies complex trade-offs |

## Step 3: Apply the Framework

### Framework A: RICE Scoring

| Component | Definition | How to Estimate |
|-----------|-----------|-----------------|
| **Reach** | How many users will this affect in a given period? | Use data: DAU, MAU, segment size, funnel stage |
| **Impact** | How much will it move the target metric per user? | 3 = Massive, 2 = High, 1 = Medium, 0.5 = Low, 0.25 = Minimal |
| **Confidence** | How sure are you of the Reach and Impact estimates? | 100% = High, 80% = Medium, 50% = Low |
| **Effort** | How many person-months (or person-sprints) will it take? | Engineering estimate in person-months |

**RICE Score** = (Reach x Impact x Confidence) / Effort

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Rank |
|---------|-------|--------|------------|--------|------------|------|
| F-001 | ... | ... | ... | ... | ... | ... |
| F-002 | ... | ... | ... | ... | ... | ... |
| F-003 | ... | ... | ... | ... | ... | ... |

### Framework B: ICE Scoring

| Component | Definition | Scale |
|-----------|-----------|-------|
| **Impact** | How much will this move the needle? | 1-10 |
| **Confidence** | How confident are we in the impact estimate? | 1-10 |
| **Ease** | How easy is this to implement? | 1-10 |

**ICE Score** = Impact x Confidence x Ease

### Framework C: MoSCoW Classification

| Category | Definition | Decision Criteria |
|----------|-----------|-------------------|
| **Must Have** | Non-negotiable for this release | Without it, the release is a failure |
| **Should Have** | Important but not critical | Significant value, but workarounds exist |
| **Could Have** | Desirable if time and budget allow | Nice to have, low risk to defer |
| **Won't Have** | Explicitly out of scope for now | Agreed to defer, documented for future |

### Framework D: Kano Model

Classify each feature by customer response:

| Category | If Present | If Absent | Example |
|----------|-----------|-----------|---------|
| **Must-Be (Basic)** | Not noticed | Major dissatisfaction | Login works, pages load |
| **One-Dimensional (Performance)** | Satisfaction proportional to quality | Dissatisfaction proportional to absence | Speed, storage, features |
| **Attractive (Delighter)** | Disproportionate delight | Not missed | Personalized recommendations |
| **Indifferent** | No effect | No effect | Backend refactoring |
| **Reverse** | Causes dissatisfaction | Preferred | Unwanted notifications |

### Framework E: Weighted Scoring

Define custom criteria and weights:

| Criterion | Weight | F-001 Score (1-10) | F-002 Score (1-10) | F-003 Score (1-10) |
|-----------|--------|-------------------|-------------------|-------------------|
| Revenue impact | 25% | ... | ... | ... |
| Customer demand | 20% | ... | ... | ... |
| Strategic alignment | 20% | ... | ... | ... |
| Technical feasibility | 15% | ... | ... | ... |
| Competitive necessity | 10% | ... | ... | ... |
| Risk reduction | 10% | ... | ... | ... |
| **Weighted Total** | **100%** | **...** | **...** | **...** |

## Step 4: Stakeholder Alignment

Ensure the prioritization reflects diverse perspectives:

### Stakeholder Input Matrix

| Stakeholder | Role | Top 3 Priorities | Rationale | Conflict With |
|-------------|------|-------------------|-----------|---------------|
| CEO / Exec | Strategy | ... | ... | ... |
| Sales | Revenue | ... | ... | ... |
| Engineering | Feasibility | ... | ... | ... |
| Customer Success | Retention | ... | ... | ... |
| Design | UX quality | ... | ... | ... |
| Customers | Value | ... | ... | ... |

### Conflict Resolution

| Conflict | Resolution Approach |
|----------|-------------------|
| Sales wants X, Engineering says too expensive | Reduce scope for MVP; validate demand first |
| Two stakeholders want top priority for different features | Use data (RICE/ICE) to break the tie objectively |
| Executive override conflicts with framework output | Document the override and rationale; revisit in retro |
| Customer request conflicts with strategy | Evaluate if strategy needs updating; offer workaround |

## Step 5: Build the Prioritized Roadmap

### Final Ranked Backlog

| Rank | Feature | Score | Priority | Target Release | Dependencies | Owner | Status |
|------|---------|-------|----------|---------------|-------------|-------|--------|
| 1 | ... | ... | Must | Q2 2026 | None | ... | Ready |
| 2 | ... | ... | Must | Q2 2026 | F-001 | ... | In Design |
| 3 | ... | ... | Should | Q3 2026 | None | ... | Validated |
| ... | ... | ... | ... | ... | ... | ... | ... |

### Value vs. Effort Matrix

```
                    HIGH VALUE
                        |
         Quick Wins     |    Big Bets
        (Do First)      |   (Plan Carefully)
                        |
  LOW EFFORT -----------+------------ HIGH EFFORT
                        |
         Fill-Ins       |    Money Pit
        (If Time)       |   (Avoid or Reduce Scope)
                        |
                    LOW VALUE
```

## Step 6: Document Trade-offs

For every feature deferred or deprioritized, document:

| Feature | Original Ask | Decision | Rationale | Revisit Date |
|---------|-------------|----------|-----------|-------------|
| F-005 | Must Have (Sales) | Deferred to Q3 | Low RICE score; 2 customers, high effort | End of Q2 |
| F-008 | Nice to Have | Won't Do | Does not align with 2026 strategy | Annual planning |

## Output Format

Present results in this order:

1. **Framework Selection** -- which framework was used and why
2. **Scoring Table** -- full scored list with all inputs visible
3. **Final Ranked Backlog** -- prioritized list with target timelines
4. **Value vs. Effort Matrix** -- visual quadrant placement
5. **Stakeholder Alignment Summary** -- where consensus exists and where it does not
6. **Trade-off Documentation** -- what was deprioritized and why
7. **Recommendations** -- suggested next steps, validation needed, risks

## Quality Checklist

Before delivering prioritization, verify:

- [ ] All candidate features are listed and described consistently
- [ ] Framework selection is justified for the context
- [ ] Scoring inputs are documented and defensible (not arbitrary)
- [ ] Stakeholder perspectives are represented
- [ ] Dependencies are identified and accounted for
- [ ] Trade-offs are documented with rationale
- [ ] Deferred items have a revisit date
- [ ] The output is actionable -- engineering can plan from it
- [ ] Quick wins (high value, low effort) are not buried in the backlog
- [ ] Must-have items are truly must-have, not just loudly requested

## Edge Cases

- **Too many features to score individually**: Group into themes first; prioritize themes, then features within top themes
- **No data for Reach or Impact**: Use ICE or MoSCoW instead of RICE; note assumptions and plan to validate
- **Single dominant stakeholder**: Document the bias; present the data-driven ranking alongside the stakeholder preference
- **All features score similarly**: Add tiebreaker criteria (time sensitivity, learning value, reversibility)
- **Urgent customer escalation**: Evaluate against framework; if it jumps the queue, document the exception and impact on other priorities
- **Technical debt competing with features**: Score tech debt on risk reduction and velocity improvement; present alongside features, not in a separate bucket
- **Regulatory or compliance requirement**: Auto-classify as Must Have; no scoring needed, but document the mandate
- **New product with no existing users**: Use ICE or Kano; rely on qualitative research over quantitative Reach data
