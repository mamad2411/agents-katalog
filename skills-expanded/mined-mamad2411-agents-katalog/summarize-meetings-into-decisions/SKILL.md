---
name: summarize-meetings-into-decisions
description: "Extract decisions, rationale, owners, and unresolved questions from a meeting transcript."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["meeting-summaries", "decision-records", "executive-brief", "transcript-parsing", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Summarize Meetings into Decisions (Decision Log Extraction) (AI Skill)

## Overview
When asked to summarize a 45-minute meeting transcript, standard AI outputs create a chronological play-by-play (*"First, Sarah presented the Q3 slide deck. Then Mark asked about pricing. Then Sarah replied that pricing was under review..."*). 

This chronological narrative is nearly useless for executives and team members who weren't in the room. What matters are **the final decisions agreed upon, the rationale behind them, and who is accountable for execution**.

The **Decision Log Extraction Protocol** filters out conversational chatter and formats the meeting into an **Architecture / Executive Decision Record (ADR)**.

---

## Chronological Narrative vs. Decision Record

```
┌─────────────────────────────────────────────────────────────┐
│                 Transcript Processing Models                │
│                                                             │
│  Chronological Narrative (Low Value):                       │
│  • 4 pages of "Bob said this, then Alice disagreed..."      │
│  • High reading fatigue, impossible to find final agreements│
│                                                             │
│  Decision Record (High Value):                              │
│  • [DECISION 1]: What was decided & why                     │
│  • [OPTIONS REJECTED]: What was eliminated & why            │
│  • [ACTION ASSIGNMENTS]: [Owner] + [Task] + [Deadline]      │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Decision Record Prompt Templates

### Pattern 1: The Executive Decision Record (ADR)
Use for product, strategy, and leadership meetings:

```markdown
Analyze the attached meeting transcript: [ATTACH TRANSCRIPT / PASTE TEXT].

Do NOT write a chronological timeline of who spoke.
Extract a structured **Executive Decision Record**:

### 🎯 1. Key Decisions Made
For each decision, format as:
- **Decision**: [Clear 1-sentence statement of what was approved]
- **Rationale**: [Why this option won over alternatives]
- **Trade-off / Cost**: [What we are giving up or spending]

### 🚫 2. Options Explicitly Rejected
- [Option Name]: [Why the team decided NOT to proceed with this path]

### ⚡ 3. Accountable Action Items
| Task | Owner | Due Date | Definition of Done |
```

---

## Real-World Case Study

### Scenario: Product Team Pricing Sync

#### Chronological AI Output (Rambling)
> *"The meeting began at 2 PM. Dave suggested increasing enterprise pricing by 20%. Lisa expressed concern that existing customers might churn. Mark mentioned that our churn rate is currently 1.8%. After some back-and-forth discussion regarding grandfathering policies, the team decided to increase new customer pricing..."*

#### Decision Record Output (Instant Clarity)

### 🎯 1. Key Decisions Made
- **Decision**: Increase Enterprise Tier pricing by **20% (from $500/mo to $600/mo)** for all new signups starting September 1st.
- **Rationale**: Competitor benchmarks show we are 35% underpriced; low churn rate (1.8%) demonstrates strong price tolerance.
- **Grandfathering Policy**: All existing customers remain on legacy $500/mo pricing for 12 months.

### 🚫 2. Options Explicitly Rejected
- **Immediate Price Hike for Existing Customers**: Rejected due to risk of relationship damage with long-term champion accounts.

### ⚡ 3. Accountable Action Items
| Task | Owner | Due Date | Definition of Done |
| :--- | :--- | :--- | :--- |
| **Update Stripe Pricing Table** | Dave | Aug 25 | New $600/mo pricing tier live on staging. |
| **Draft Grandfathering FAQ Email** | Lisa | Aug 20 | Customer update email reviewed and approved. |

---

## Summary Best Practices
- **Ban "Who said what"**: Explicitly prompt *"Focus on team consensus and final decisions, not individual speech chronologies."*
- **Always record rejected options**: Capturing *why* an alternative was killed prevents the team from debating the exact same idea again 3 months later.
