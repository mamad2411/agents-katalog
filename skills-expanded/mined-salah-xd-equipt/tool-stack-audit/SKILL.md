---
name: tool-stack-audit
description: "Audits business technology stacks for redundancy, cost optimization, and integration opportunities. Use when reviewing and optimizing your business software spend."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Tool Stack Audit

## When to Use This Skill

Use this skill when you need to:
- Audit your business software stack for redundancy and waste
- Identify cost savings by consolidating or replacing tools
- Evaluate integration opportunities between existing tools
- Create a rationalized, optimized tool stack recommendation

**DO NOT** use this skill for choosing a single tool (use saas-evaluation), building automation workflows, or technical infrastructure audits. This is for business software stack review and optimization.

---

## Core Principle

EVERY TOOL IN YOUR STACK MUST EARN ITS SEAT — IF YOU CANNOT NAME THE SPECIFIC PROBLEM IT SOLVES AND THE TIME OR MONEY IT SAVES, IT IS A CANDIDATE FOR REMOVAL.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do?" | No default — must be provided |
| **Current tools** | "List every paid tool or software you use for business." | No default — must be provided |
| **Monthly spend** | "What is your total monthly software spend?" | Unknown — we will calculate it |
| **Pain points** | "What frustrates you about your current tools?" | Overlap, cost, complexity |
| **Must-keep tools** | "Are any tools non-negotiable? Which ones and why?" | None specified |
| **Budget target** | "Do you have a target monthly spend you would like to hit?" | Reduce by 20-30% |

**GATE: Confirm the tool list and goals before starting the audit.**

---

## Phase 2: Inventory and Assess

### Tool Inventory Template

For each tool, document:

| Field | Details |
|-------|---------|
| **Tool name** | |
| **Category** | (communication, project management, marketing, finance, etc.) |
| **Monthly cost** | |
| **Annual cost** | |
| **Plan tier** | (free, basic, pro, enterprise) |
| **Primary use** | (what you use it for) |
| **Usage frequency** | (daily, weekly, monthly, rarely) |
| **Integrations** | (what other tools it connects to) |
| **Users** | (how many people use it) |
| **Contract end** | (when can you cancel?) |

### Assessment Scoring

Rate each tool on:

| Criterion | Score 1-5 |
|-----------|-----------|
| **Essential** — Would your business break without this tool? | |
| **Utilized** — Do you use more than 50% of its features? | |
| **Value** — Is the cost justified by the time/money saved? | |
| **Integrated** — Does it connect to your other tools? | |

**Action thresholds:**
- Score 16-20: Keep — essential, well-utilized
- Score 11-15: Optimize — may be on wrong tier or underused
- Score 6-10: Replace — find a better or cheaper alternative
- Score 1-5: Cut — not earning its seat

**GATE: Present the scored inventory and get confirmation before making recommendations.**

---

## Phase 3: Recommend

### Optimization Actions

For each tool, recommend one action:

| Action | When to Apply |
|--------|---------------|
| **Keep** | Essential, well-used, good value |
| **Downgrade** | Using less than the plan provides |
| **Consolidate** | Two tools do the same job — pick the better one |
| **Replace** | A better or cheaper alternative exists |
| **Cut** | Not used enough to justify any cost |
| **Integrate** | Connect to other tools to increase value |

### Consolidation Opportunities

Identify tools with overlapping functionality:

```
## Overlap Analysis

**Communication:** Slack + Teams + email → Consolidate to one + email
**Project Management:** Trello + Asana + Notion → Pick one
**Email Marketing:** Mailchimp + ConvertKit → Pick one
**Design:** Canva + Adobe → Evaluate usage, choose one
**Storage:** Google Drive + Dropbox → Consolidate to one
```

### Replacement Recommendations

For each tool marked for replacement:
- **Current tool:** [Name] — $[cost]/month
- **Recommended replacement:** [Name] — $[cost]/month
- **Savings:** $[X]/month
- **Migration effort:** [Low/Medium/High]
- **Key trade-off:** [What you gain vs. what you lose]

---

## Phase 4: Polish

### 1. Savings Summary

```
## Stack Optimization Summary

**Current monthly spend:** $[X]
**Optimized monthly spend:** $[Y]
**Monthly savings:** $[X-Y]
**Annual savings:** $[X-Y x 12]

### Changes
| Tool | Action | Before | After | Savings |
|------|--------|--------|-------|---------|
| [Tool 1] | Cut | $29/mo | $0 | $29/mo |
| [Tool 2] | Downgrade | $49/mo | $19/mo | $30/mo |
| [Tool 3] | Replace | $39/mo | $15/mo | $24/mo |
| **Total** | | **$[X]** | **$[Y]** | **$[Z]/mo** |
```

### 2. Migration Plan

For tools being replaced or cut:
- Export all data before canceling
- Note contract end dates and cancellation requirements
- Sequence changes to avoid workflow disruptions
- Allow 1-2 weeks overlap during transitions

### 3. Quality Checklist

```
## Tool Stack Audit Checklist

- [ ] All paid tools inventoried with costs and categories
- [ ] Each tool scored on essential, utilized, value, and integrated
- [ ] Overlapping tools identified with consolidation recommendations
- [ ] Replacement tools researched with cost comparisons
- [ ] Total monthly and annual savings calculated
- [ ] Migration plan includes data export and timeline
- [ ] Contract end dates checked for cancellation windows
- [ ] Must-keep tools confirmed with user
- [ ] Integration opportunities between remaining tools identified
- [ ] Optimized stack documented for reference
```

---

## Example

**Business:** Freelance marketing consultant, $487/month in tools

**Audit finding:**
"You are paying for Trello ($10/month), Asana ($11/month), and Notion ($10/month). All three are project management tools. Consolidate to Notion — it covers project management, notes, and client portals. Savings: $21/month."

**Summary:**
"Current spend: $487/month. After cutting 3 unused tools, downgrading 2 plans, and consolidating 2 overlapping tools: $312/month. Annual savings: $2,100."

---

## Anti-Patterns

- **Cutting tools without a replacement plan** — removing a tool before confirming the workflow can survive without it causes chaos.
- **Optimizing only on cost** — a $49/month tool that saves 10 hours/month is worth $490 at $49/hour. Do not cut it to save $49.
- **Ignoring annual contracts** — some tools charge cancellation fees or have annual commitments. Check before recommending cuts.
- **Too many changes at once** — migrate one tool at a time. Changing 5 tools in one week guarantees confusion.
- **Forgetting free tools** — free tools still have costs (time to manage, integration complexity, data fragmentation). Include them in the audit.

---

## Recovery

- **User cannot list all their tools:** Check bank and credit card statements for recurring software charges. Review browser bookmarks and app logins.
- **User pushes back on cutting a tool:** Ask them to track actual usage for 2 weeks. Data often changes minds when feelings will not.
- **Migration breaks a workflow:** Roll back to the old tool temporarily. Diagnose what broke and fix it before migrating again.
- **Savings are minimal:** The stack may already be lean. Focus on integration improvements and workflow optimization instead of cost cuts.
