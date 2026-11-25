---
name: ai-use-case-finder
description: "Identifies AI automation opportunities in business workflows with feasibility assessment and ROI estimates. Use when evaluating where AI can save time and money in your business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# AI Use Case Finder

## When to Use This Skill

Use this skill when you need to:
- Identify which business tasks can be automated or enhanced with AI
- Evaluate the feasibility and ROI of AI adoption for specific workflows
- Prioritize AI implementation opportunities by impact and effort
- Create an AI adoption roadmap for a solopreneur or small business

**DO NOT** use this skill for building AI models, writing prompts, or evaluating specific AI tools. This is for identifying and prioritizing where AI fits in your business.

---

## Core Principle

AI SHOULD AUTOMATE THE REPETITIVE SO YOU CAN FOCUS ON THE STRATEGIC — THE BEST AI USE CASES SAVE MEASURABLE TIME ON TASKS YOU ALREADY DO, NOT TASKS YOU IMAGINE DOING.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do?" | No default — must be provided |
| **Team size** | "How many people work in the business?" | Solo (1 person) |
| **Weekly tasks** | "List the tasks you spend the most time on each week." | No default — must be provided |
| **Pain points** | "Which tasks do you dread or wish you could delegate?" | No default — ask for top 3 |
| **Current AI usage** | "Do you use any AI tools already? Which ones?" | None or basic ChatGPT |
| **Budget** | "What is your monthly budget for tools and software?" | Under $100/month |

**GATE: Confirm the brief and task list before analyzing opportunities.**

---

## Phase 2: Audit and Identify

### Task Audit Framework

For each task the user listed, evaluate:

| Task | Hours/Week | Frequency | Repetitive? | Requires Judgment? | AI Potential |
|------|-----------|-----------|-------------|--------------------|----|
| [Task 1] | | | Yes/No | Low/Med/High | High/Med/Low |
| [Task 2] | | | Yes/No | Low/Med/High | High/Med/Low |

### AI Opportunity Scoring

Score each task on three dimensions:

| Dimension | Score 1-5 | Description |
|-----------|-----------|-------------|
| **Time savings** | 1=minimal, 5=hours saved weekly | How much time will AI save? |
| **Feasibility** | 1=complex, 5=tools exist today | Can current AI tools handle this? |
| **Impact** | 1=nice-to-have, 5=revenue-affecting | What is the business impact of automating this? |

**AI Priority Score = Time Savings x Feasibility x Impact (max 125)**

### Common High-Value AI Use Cases

| Business Area | Task | AI Solution | Time Saved |
|---------------|------|------------|-----------|
| **Content** | Writing first drafts | LLM (Claude, ChatGPT) | 5-10 hrs/week |
| **Email** | Drafting responses | AI email tools | 3-5 hrs/week |
| **Social media** | Caption and post writing | LLM + scheduling tool | 2-4 hrs/week |
| **Research** | Market and competitor research | AI search + summarization | 2-3 hrs/week |
| **Admin** | Meeting notes and summaries | AI transcription | 1-2 hrs/week |
| **Finance** | Invoice and expense categorization | AI bookkeeping tools | 1-2 hrs/week |
| **Customer support** | FAQ responses | Chatbots, templated AI | 3-5 hrs/week |
| **Design** | Basic graphic creation | AI image generation | 1-3 hrs/week |

**GATE: Present scored opportunities and confirm the top 3-5 to develop further.**

---

## Phase 3: Build the Implementation Plan

### For Each Top Opportunity

```
## Opportunity: [Task Name]

**Current state:** [How the task is done now]
**AI solution:** [Specific tool or approach]
**Time saved:** [Hours per week]
**Cost:** [Monthly tool cost]
**ROI:** [Time saved x hourly rate] vs. [Tool cost]
**Implementation effort:** [Hours to set up]
**Risk:** [What could go wrong]

### Setup Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Success Metric
[How to measure whether this is working]
```

### Implementation Roadmap

Sequence opportunities by quick wins first:

| Phase | Timeline | Tasks to Automate | Expected Savings |
|-------|----------|-------------------|-----------------|
| Quick wins | Week 1-2 | [Low effort, high impact tasks] | [X] hrs/week |
| Foundation | Week 3-4 | [Medium effort tasks] | [X] hrs/week |
| Advanced | Month 2-3 | [Higher effort, higher reward] | [X] hrs/week |

---

## Phase 4: Polish

### 1. ROI Summary

```
## AI Adoption ROI Summary

**Total tasks audited:** [X]
**Tasks with AI potential:** [X]
**Estimated weekly time savings:** [X] hours
**Monthly tool costs:** $[X]
**Monthly value of time saved:** $[X] (at $[hourly rate]/hour)
**Net monthly ROI:** $[X]
**Payback period:** [X] weeks
```

### 2. Risk Assessment

For each recommended AI implementation:
- **Quality risk:** Will AI output meet your standards? (Mitigation: human review)
- **Dependency risk:** What if the tool shuts down? (Mitigation: avoid single points of failure)
- **Cost risk:** Will pricing increase? (Mitigation: monitor usage and alternatives)

### 3. Quality Checklist

```
## AI Use Case Finder Checklist

- [ ] All major weekly tasks audited with time estimates
- [ ] Each task scored on time savings, feasibility, and impact
- [ ] Top 3-5 opportunities identified and prioritized
- [ ] Specific AI tools recommended for each opportunity
- [ ] ROI calculated (time saved vs. tool cost)
- [ ] Implementation steps outlined for each opportunity
- [ ] Roadmap sequences quick wins first
- [ ] Risks identified with mitigation strategies
- [ ] Success metrics defined for each implementation
- [ ] Total projected time savings and ROI summarized
```

---

## Example

**Business:** Freelance marketing consultant
**Top opportunity:**

```
## Opportunity: Client Report Writing

**Current state:** Manually compiling analytics into reports, writing summaries. Takes 4 hours per client per month across 6 clients = 24 hours/month.
**AI solution:** Claude + template. Feed analytics data, generate narrative report draft, human review and customize.
**Time saved:** 16 hours/month (from 24 to 8)
**Cost:** $20/month (Claude Pro)
**ROI:** 16 hours x $75/hour = $1,200/month value saved for $20 cost
**Implementation effort:** 3 hours to create templates and test
**Success metric:** Report creation time drops below 1.5 hours per client
```

---

## Anti-Patterns

- **Automating tasks you should eliminate** — if a task adds no value, do not automate it. Stop doing it.
- **Starting with the hardest use case** — begin with the simplest, most repetitive tasks. Build confidence before tackling complex workflows.
- **Ignoring quality requirements** — AI drafts need human review. Build review time into your time savings estimate.
- **Tool hoarding** — signing up for 10 AI tools creates complexity. Start with 1-2 tools that cover the most use cases.
- **Expecting perfection** — AI that saves 70% of the time on a task is a win. Waiting for 100% automation means waiting forever.

---

## Recovery

- **User cannot identify repetitive tasks:** Walk through a typical work week hour by hour. Tasks become visible when mapped to time.
- **All tasks seem to require high judgment:** Break tasks into sub-steps. The research, drafting, and formatting sub-steps are often automatable even when the final decision is not.
- **Budget is zero:** Focus on free tiers of AI tools (ChatGPT free, Claude free, Canva free). Many tools offer generous free plans.
- **User is overwhelmed by options:** Pick ONE task, ONE tool, and ONE week to try it. Expand only after the first win.
