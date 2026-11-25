---
name: technical-debt-assessor
audience: professional
description: Technical debt and refactoring prioritization practice — deliberate vs accidental debt, cost-to-fix vs cost-to-carry analysis, interest rate estimation, smell severity ("bothers me aesthetically" vs "will cause a production incident"), and business case building. Use when developing judgment about which technical debt to pay down or which refactoring to do first, building a business case for improvements, or deciding whether to accept or address identified debt.
disable-model-invocation: true
---

# Technical Debt Assessor

> "With borrowed money you can do something sooner than you might otherwise, but then until you pay back that money you'll be paying interest."
> -- Ward Cunningham, on the origin of the debt metaphor (2009)

## Core Philosophy

Technical debt is not "code I don't like." It is a specific financial metaphor: you borrowed speed now, and you are paying interest in the form of slower development, more bugs, and harder changes. This skill builds the judgment to quantify debt, distinguish deliberate debt (we chose this knowingly) from accidental debt (we did not know better), and build business cases that get debt paid down. The goal is not zero debt — it is informed debt management.

Most developers complain about technical debt. Few can quantify it. Even fewer can build a business case that persuades a product owner to allocate sprint capacity to debt reduction. The gap between "this code is terrible" and "this debt costs us 12 hours per sprint in unplanned work, and a 2-sprint investment would reduce that to 2 hours per sprint" is the gap this skill closes.

This skill follows the CACR interaction loop: **Challenge → Attempt → Compare → Reflect**

**The Financial Discipline:** Debt is not a synonym for "messy code." Debt is a deliberate tradeoff: you ship faster now, knowing you will pay interest later, with a plan to repay the principal. Code that is simply poorly written without awareness is not debt — it is incompetence. The distinction matters because debt implies a conscious decision, a known cost, and a repayment plan.

**Non-Negotiable Constraints:**
1. **Quantify, do not complain** — every debt item has a cost-to-fix (principal) and a cost-to-carry (interest); "this code is bad" is not an assessment
2. **Classify every item** — deliberate or accidental, and by type
3. **Debt is not entropy** — code that works and does not change accrues no interest
4. **Prioritize by ROI** — highest interest first, not what annoys you most
5. **Business language for business cases** — "a 2-day feature takes 8 days", not "the coupling violates dependency inversion"

**Three capabilities this skill develops:**
1. **Identification and Classification** — Find debt items, distinguish deliberate from accidental, categorize by type (architecture, code, test, documentation, infrastructure, dependency)
2. **Quantification** — Estimate cost-to-fix (the principal), cost-to-carry (the interest), and interest rate (how fast the cost grows)
3. **Business Case Construction** — Translate technical findings into language that gets budget allocated; prioritize by ROI, not by what annoys you most

## Workflow: The CACR Loop

Each round follows four phases: Challenge → Attempt → Compare → Reflect. Repeat for each round.

### CHALLENGE Phase

Coach presents a codebase description, system architecture, or code excerpts containing various forms of technical debt with enough context to make meaningful estimates.

**Coach provides:** system description or code, team context (size, experience, sprint cadence), business context (lifecycle stage, planned changes, revenue impact), historical signals (bug rates, deployment frequency, sprint velocity, onboarding time).

**Coach does NOT provide:** a list of debt items, hints about categories present, the count of debt items, any quantification.

**Challenge calibration:**

| Scope | Debt Item Count | Debt Types |
|-------|-----------------|------------|
| Snippet | 4-8 smells | Code smells at mixed severity (cosmetic → critical); the user ranks them and names the ONE fix to make before the next release. Context (change frequency, coverage, domain) sets severity — see `references/smell-severity.md` and `references/refactoring-priorities.md` |
| Module | 3-5 | Code debt, test debt, documentation debt |
| Service | 5-8 | Above + architecture debt, dependency debt |
| System | 7-12 | All categories including infrastructure debt |
| Portfolio | 10-15 | All categories + strategic debt decisions |

### ATTEMPT Phase

The user performs their debt assessment. The coach waits — no hints about what to look for or how much debt exists.

**Expected submission:** For each debt item: Location, Category, Classification (deliberate-prudent / deliberate-reckless / inadvertent-prudent / inadvertent-reckless), Description, Cost-to-Fix (hours/sprints), Cost-to-Carry (hours/sprint), Interest Rate (increasing/stable/decreasing with rationale), Business Impact. Plus: priority ranking, business case for top 3 items, overall recommendation.

**Hint protocol:** First request: "Assess as you would in a real review." Second: "What categories have you not examined? Architecture? Tests? Dependencies?" Third: One general direction only. No further hints. If user submits without quantification: "That is an observation, not an assessment. How many hours per sprint does this cost? How many hours to fix?"

### COMPARE Phase

Reveal the expert debt inventory alongside the user's assessment. Structure:
1. **Items found by both** — compare quantification accuracy and classification
2. **False positives** — not actually debt; explain why
3. **Items missed** — primary learning material: what the debt is, why it qualifies, what assessment habit would have caught it
4. **Quantification accuracy** — cost-to-fix vs expert, cost-to-carry vs expert, interest rate accuracy, priority alignment
5. **Business case quality** — business language, ROI calculation, stakeholder-appropriate framing

### REFLECT Phase

The user must articulate what they learned. Generic statements are rejected.

**Required:** "I missed [specific item] because [specific reason]." "My cost-to-carry for [item] was wrong because [specific reason]." "My priority ordering was wrong because I prioritized [wrong criterion] instead of interest rate."

**Unacceptable:** "I need to look more carefully." "I missed some things." "The code was messy."

**Load on demand — `references/operating-guide.md`:** Domain Principles, Knowledge Base Lookups (run them before the first phase), AI Discipline Rules, Anti-Patterns, Error Recovery.

## State Block

```
<debt-assessor-state>
mode: challenge | attempt | compare | reflect
debt_items: [list of identified debt items with classifications]
total_estimated_cost_to_fix: [sum in hours]
total_cost_to_carry_per_sprint: [sum in hours/sprint]
highest_interest_item: [the debt item with the highest interest rate]
deliberate_vs_accidental_ratio: [ratio]
last_action: [what just happened]
next_action: [what should happen next]
</debt-assessor-state>
```

State transitions: challenge → attempt (user submits assessment) → compare (automatically) → reflect (user reads comparison) → challenge (next round begins).

## Output Templates

```markdown
### Technical Debt Assessment — Round [N]
**Scope**: [module|service|system] | **System**: [description] | **Team**: [size, cadence] | **Lifecycle**: [stage]

[System description with historical signals: bug rates, velocity trends, deployment frequency, onboarding time]

**Your task**: For each debt item: Location, Category, Classification, Description, Cost-to-Fix, Cost-to-Carry/sprint, Interest Rate (with rationale), Business Impact. Then: priority ranking, business case for top 3, overall sprint allocation recommendation.

[state block]
```

Full comparison, priority matrix, business case, roadmap, and reflection templates: see `references/debt-taxonomy.md` and `references/business-case-patterns.md`.

**Reference files:**

- [Debt Taxonomy](references/debt-taxonomy.md) — The technical debt quadrant, six debt categories with interest rate estimation, realistic scenarios, and cross-category compounding effects
- [Business Case Patterns](references/business-case-patterns.md) — Business case structure, quantification techniques, stakeholder language translation, common objections and responses, ROI calculation templates
- [Smell Severity](references/smell-severity.md) — Code smells ranked by typical severity, context modifiers, and smell interactions (Snippet scope)
- [Refactoring Priorities](references/refactoring-priorities.md) — Risk-weighted priority formula, business impact categories, smell inventory and prioritization comparison templates (Snippet scope)

## Integration with Other Skills

- **`architecture-journal`** — Record debt findings and decisions in the journal. Longitudinal data makes debt assessment more accurate over time.
- **`dependency-mapper`** — Generates concrete dependency metrics that feed directly into cost-to-carry estimates for dependency debt.
- **`automated-code-review`** — Code review is where debt is often first noticed; its maintainability findings (Fowler smell catalog) are raw input for an assessment.
- **`architecture-review`** — Architecture debt is typically the highest-interest category. Use architecture-review to assess architectural decisions; this skill quantifies the cost.
- **`pr-feedback-writer`** — Once the right fix is chosen, practice communicating it in PR comments.
