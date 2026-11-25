---
name: saas-evaluation
description: "Evaluates SaaS tools for business adoption with feature comparison, pricing analysis, and migration planning. Use when choosing between software options for your business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# SaaS Evaluation

## When to Use This Skill

Use this skill when you need to:
- Evaluate and compare SaaS tools for a specific business need
- Create a structured decision framework for software selection
- Analyze pricing, features, and migration requirements
- Document a tool selection decision for future reference

**DO NOT** use this skill for full tech stack audits (use tool-stack-audit), building software, or vendor contract negotiations. This is for evaluating individual SaaS tool choices.

---

## Core Principle

THE BEST TOOL IS NOT THE ONE WITH THE MOST FEATURES — IT IS THE ONE THAT SOLVES YOUR SPECIFIC PROBLEM AT A PRICE YOU CAN SUSTAIN, WITH THE LEAST FRICTION TO ADOPT.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Problem to solve** | "What specific problem are you trying to solve with this tool?" | No default — must be provided |
| **Must-have features** | "What features are absolutely required? Non-negotiable." | No default — list 3-5 |
| **Nice-to-have features** | "What features would be great but you could live without?" | None specified |
| **Budget** | "What is your monthly budget for this tool?" | Under $50/month |
| **Options being considered** | "What tools are you evaluating? List 2-5 options." | No default — research if needed |
| **Current solution** | "What are you using now, if anything?" | Manual process or spreadsheets |
| **Integration needs** | "What other tools does this need to connect to?" | None specific |

**GATE: Confirm the brief before starting the evaluation.**

---

## Phase 2: Research and Compare

### Comparison Matrix

| Criteria | [Tool A] | [Tool B] | [Tool C] |
|----------|----------|----------|----------|
| **Monthly price** | | | |
| **Annual price** | | | |
| **Free tier/trial** | | | |
| **Must-have 1** | Yes/No/Partial | | |
| **Must-have 2** | Yes/No/Partial | | |
| **Must-have 3** | Yes/No/Partial | | |
| **Nice-to-have 1** | Yes/No | | |
| **Nice-to-have 2** | Yes/No | | |
| **Integrations** | | | |
| **Mobile app** | Yes/No | | |
| **API access** | Yes/No | | |
| **Support quality** | | | |
| **Data export** | Yes/No | | |

### Weighted Scoring

Assign weights to each criterion:

| Criterion | Weight | Tool A | Tool B | Tool C |
|-----------|--------|--------|--------|--------|
| Must-have features | 40% | /10 | /10 | /10 |
| Price/value | 25% | /10 | /10 | /10 |
| Ease of use | 15% | /10 | /10 | /10 |
| Integrations | 10% | /10 | /10 | /10 |
| Support and reliability | 10% | /10 | /10 | /10 |
| **Weighted total** | 100% | /10 | /10 | /10 |

### Hidden Cost Analysis

Check for costs beyond the subscription price:
- Setup or onboarding fees
- Per-user pricing (how does cost scale with team growth?)
- Data storage limits and overage charges
- Add-on features that should be included
- Annual vs. monthly pricing difference
- Contract length requirements

**GATE: Present the comparison and scores before making a recommendation.**

---

## Phase 3: Recommend

### Recommendation Format

```
## Recommendation: [Tool Name]

**Why this tool wins:**
1. [Primary reason — tied to must-have features]
2. [Secondary reason — tied to price or integration]
3. [Tertiary reason — tied to ease of use or support]

**Trade-offs to accept:**
- [What this tool does not do as well as competitors]
- [Feature gap that you can live without]

**Recommended plan:** [Plan name] at $[X]/month
**Total first-year cost:** $[X] (including any setup fees)

**Runner-up:** [Tool name] — choose this if [specific condition]
```

### Trial Testing Plan

Before committing, test the recommended tool:

```
## Trial Checklist (7-14 days)

- [ ] Sign up for free trial
- [ ] Complete onboarding and initial setup
- [ ] Perform your top 3 use cases
- [ ] Test integration with [connected tool]
- [ ] Test data import from current solution
- [ ] Evaluate mobile experience (if relevant)
- [ ] Contact support with a test question (measure response time)
- [ ] Export data to confirm you can leave if needed
```

---

## Phase 4: Polish

### 1. Migration Plan

```
## Migration Plan: [Old Solution] → [New Tool]

**Timeline:** [X] weeks

**Week 1: Setup**
- Create account on recommended plan
- Configure settings and preferences
- Set up integrations

**Week 2: Data Migration**
- Export data from old solution
- Import into new tool
- Verify data accuracy

**Week 3: Transition**
- Run both tools in parallel
- Train yourself/team on new workflows
- Resolve any issues

**Week 4: Cutover**
- Disable old tool
- Cancel old subscription (check billing cycle)
- Confirm all workflows run on new tool
```

### 2. Decision Documentation

Save the evaluation for future reference:

```
## Decision Record: [Category] Tool Selection

**Date:** [Date]
**Decision:** Selected [Tool] for [purpose]
**Alternatives considered:** [List]
**Key factors:** [Top 3 reasons]
**Cost:** $[X]/month on [Plan]
**Review date:** [6 months from now — re-evaluate]
```

### 3. Quality Checklist

```
## SaaS Evaluation Checklist

- [ ] Problem to solve is clearly defined
- [ ] Must-have features listed (3-5 minimum)
- [ ] At least 3 tools compared side by side
- [ ] Comparison matrix includes features, pricing, and integrations
- [ ] Weighted scoring applied with rationale
- [ ] Hidden costs identified (setup, overages, scaling)
- [ ] Recommendation includes trade-offs and runner-up
- [ ] Trial testing plan documented and followed
- [ ] Migration plan created for switching tools
- [ ] Decision documented for future reference
```

---

## Example

**Problem:** Need a project management tool for client work
**Budget:** $20/month
**Must-haves:** Client-facing views, task assignments, file attachments

**Recommendation excerpt:**
"Select Notion ($10/month, Plus plan). It covers all must-haves: shared client pages, task databases with assignments, and file attachments. It scores highest on ease of use and price, though Asana wins on advanced project reporting. Since you manage under 10 active projects, Notion's simplicity is a better fit than Asana's complexity. Re-evaluate in 6 months if project volume exceeds 20."

---

## Anti-Patterns

- **Feature fixation** — choosing the tool with the most features instead of the best fit. You will use 20% of features — focus on the right 20%.
- **Ignoring exit costs** — if you cannot export your data, you are locked in. Always verify data portability before committing.
- **Skipping the trial** — reviews and comparisons are not substitutes for hands-on testing. Always run a trial with your real workflow.
- **Cheapest wins** — the cheapest option that does not solve the problem costs more than the right tool at the right price.
- **Analysis paralysis** — comparing 10 tools for 3 months is worse than picking a good-enough tool and starting. Set a decision deadline.

---

## Recovery

- **Cannot decide between two tools:** Run a 1-week trial with each using the same test scenario. The hands-on experience usually breaks the tie.
- **Recommended tool is over budget:** Check if annual billing reduces the cost. If still over budget, evaluate which must-have features you can compromise on.
- **Tool selected but not adopted:** The problem is usually onboarding friction, not the tool. Dedicate one focused session to setup and migration.
- **Tool is not working after 30 days:** Refer back to the evaluation. If the runner-up addresses the issues, switch early before more data accumulates.
