---
name: dont-summarize-without-a-goal
description: "Define the decision or information need before asking for a document summary."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["goal-directed-summarization", "information-extraction", "decision-making", "executive-brief", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Don't Summarize Without a Goal (Goal-Directed Extraction) (AI Skill)

## Overview
Typing *"Summarize this document"* is one of the most common - and least effective - prompts in generative AI. Because the model doesn't know *why* you are reading the document, it defaults to a balanced, generic overview that often omits the exact metrics, dates, or risks you actually care about.

The **Goal-Directed Extraction Protocol** anchors the AI to a specific persona, decision objective, or lens before reading, ensuring 100% of the output is actionable.

---

## Generic Summaries vs. Goal-Directed Extraction

```
┌─────────────────────────────────────────────────────────────┐
│                 Generic vs. Goal-Directed Flow              │
│                                                             │
│  Generic Prompt ("Summarize this 40-page RFP"):             │
│  • AI writes 5 paragraphs summarizing company history,     │
│    introduction, high-level mission, and team bios.         │
│  • 0% of the financial terms or deadlines are highlighted. │
│                                                             │
│  Goal-Directed Prompt ("Extract costs, SLAs, & deadlines"): │
│  • AI outputs a 1-page structured breakdown:                │
│    1. Pricing tiers & setup fees                            │
│    2. Hard delivery milestones & penalties                  │
│    3. Uptime commitments & SLA credits                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Goal-Directed Prompt Templates

### Pattern 1: The Persona-Driven Lens
Use when analyzing reports for different stakeholders:

```markdown
Read the attached document: [ATTACH REPORT / PASTE TEXT].

Summarize this document through the lens of a **Chief Financial Officer (CFO)**.
Focus exclusively on:
1. All hard costs, recurring fees, and margin impacts.
2. Capital expenditure (CapEx) vs. Operational expenditure (OpEx) commitments.
3. Financial risk exposure or liability caps.

Ignore background narratives and general marketing descriptions.
```

---

### Pattern 2: The Action & Deadline Extractor
Use for contracts, schedules, or legal notices:

```markdown
Analyze the attached agreement. Do NOT write a general summary.
Extract ONLY:
- **All hard deadlines and calendar dates** (with the exact contractual event triggering them).
- **All payment due dates and penalty terms**.
- **All renewal / cancellation notice windows**.

Format as a chronologically sorted Markdown table.
```

---

## Real-World Case Study

### Scenario: Reviewing a 25-Page Cloud Migration RFP

#### Generic "Summarize This" Output (Low Signal)
> *"This RFP outlines the proposed migration of our legacy data warehouse to Snowflake. It covers the migration methodology, team credentials, testing procedures, and data governance best practices. The vendor emphasizes their extensive experience in enterprise data architecture..."*
> 
> ❌ *(Completely useless for an executive deciding whether to approve the budget).*

#### Goal-Directed Output (High Signal, Decision Ready)

> **Lens**: Technical Risk & Cost Sizing for VP of Engineering
> 
> ### 1. Key Timelines & Downtime
> - **Total Migration Window**: 14 weeks (Phased rollout starting Oct 1).
> - **Planned Production Cutover Downtime**: 4-hour maintenance window on a Sunday (2:00 AM - 6:00 AM EST).
>
> ### 2. Resource & Budget Commitments
> - **Fixed Implementation Fee**: $145,000 (Milestone-based billing: 30% upfront, 40% on alpha schema validation, 30% on cutover).
> - **Required Internal Staffing**: 1 dedicated internal DBA (15 hrs/wk) + 1 Senior Data Engineer (full-time).
>
> ### 3. Identified Critical Risks
> - **Legacy Stored Procedures**: 42 legacy Oracle PL/SQL procedures must be manually rewritten into dbt models (estimated 120 engineering hours).

---

## Summary Best Practices
1. **Never say just "Summarize"**: Pair the request with an objective (*"Summarize to help us decide whether to approve this budget"*).
2. **Name the persona**: *"Read this as an SRE"*, *"Read this as a litigation attorney"*, *"Read this as a non-technical customer"*.
3. **Specify what to ignore**: Adding *"Skip corporate boilerplate and introductory history"* cuts output token waste by 40%.
