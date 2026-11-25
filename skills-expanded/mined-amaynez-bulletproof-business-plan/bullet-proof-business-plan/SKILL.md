---
name: bullet-proof-business-plan
description: Stress-test and strengthen a business plan through iterative rounds of adversarial investor critique and strategic re-engineering. Use when you need to identify existential risks in a business model and transform vulnerabilities into defensible moats. Do NOT use for creative writing, general notes, or non-business strategies.
---

# Bulletproof Business Plan

## Quick start
"Run the bulletproof process for the business plan at [path/to/plan.md]."

## Workflows

### 1. Initialization & Scoping
- **Target Plan**: Locate the business plan file.
- **Rounds**: Ask the user: "How many rounds of hardening should I execute? I recommend 3-5 rounds for a balanced value between token usage and having a great plan."
- **Setup**: Create a directory named `hardening_[plan-basename]/` in the same folder as the plan.
- **Archive**: Save the original plan as `rounds/r0_original.md`.
- **Summary**: Create `summary.md` to track the strategic evolution and pivots.

### 2. The Hardening Loop (For Round N = 1 to Total)
#### **Step A: Investor Review**
- **Persona**: World-class investor.
- **Task**: Conduct the Round [N] review of the business plan. Identify all possible objections for investing in the business.
- **Metric of Importance**: To avoid nitpicking, assign a metric to each objection indicating how important it is for an investor that this objection is resolved (e.g., "Probability of Rejection if Unresolved: 90%"). This ensures the plan owner understands the gravity of each risk.
- **Constraint**: Every objection must be sustained and backed by logic or hard data from the web (use `search_web`).
- **Output**: Save all objections to `rounds/r[N]_investor_review.md`.

#### **Step B: Plan Hardening**
- **Persona**: Strategic Founder / Consultant.
- **Task**: Improve the business plan by addressing the objections from the latest round one by one.
- **Severity-Informed Thinking**: Read carefully the severity/metric of each objection. Think hard on how to improve the plan so that the objection **disappears** (if critical) or is **significantly reduced** (if medium), transforming that vulnerability into a strong point of the plan.
- **Output**: Save the improved version to `rounds/r[N]_hardened_plan.md`.

#### **Step C: Update Summary**
- **Task**: Extract key pivots and status updates and log them in `summary.md`.

### 3. Finalization
- Present the final `hardened_plan.md` and the `summary.md` to the user.
