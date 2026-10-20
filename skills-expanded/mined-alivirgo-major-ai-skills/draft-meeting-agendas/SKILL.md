---
name: draft-meeting-agendas
description: "Create a time-boxed meeting agenda with discussion owners, pre-reads, and explicit decisions to reach."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["meeting-agendas", "time-blocking", "productivity", "decision-making", "executive-workflows", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Draft Outcome-Driven Meeting Agendas (Time-Blocked Agenda) (AI Skill)

## Overview
Unstructured meetings without a defined objective or time allocations almost always expand to fill their scheduled duration (Parkinson's Law), devolving into unfocused discussion without clear decisions.

The **Outcome-Driven Agenda Protocol** forces the AI to structure meetings around a **Single Primary Decision**, time-boxing each topic in 5-to-10 minute increments with assigned discussion leads and mandatory pre-read links.

---

## The Outcome-Driven Agenda Blueprint

```
┌─────────────────────────────────────────────────────────────┐
│                 Outcome-Driven Meeting Blueprint            │
│                                                             │
│  [ PRIMARY OBJECTIVE ]: The single decision we must make    │
│  [ PRE-READ (5 mins) ]: Links & materials to review before  │
│                                                             │
│  [ TIME-BLOCKED SEGMENTS ]:                                 │
│  • 00-05m: Alignment & Problem Statement (Lead: Host)       │
│  • 05-15m: Core Options & Trade-Offs (Lead: Owner)          │
│  • 15-25m: Debate & Edge-Case Q&A (Open Floor)              │
│  • 25-30m: Final Decision & Action Item Allocation (Lead: PM)│
└─────────────────────────────────────────────────────────────┘
```

---

## Master Agenda Prompt Templates

### Pattern 1: The 30-Minute Decision Sync Directive
Use when scheduling alignment or approval meetings:

```markdown
Draft a focused 30-minute meeting agenda for [MEETING PURPOSE: e.g. Q3 Architecture Decision].

Requirements:
1. State the **Single Primary Decision** at the top in bold.
2. Include a **Pre-Meeting Reading / Preparation** section (max 2 items).
3. Create a **Time-Blocked Schedule** breaking down the 30 minutes into 4 tight segments (with designated discussion lead roles).
4. Include a dedicated 5-minute wrap-up block strictly for assigning action items.
```

---

### Pattern 2: The Cross-Functional Brainstorming Agenda (45 Minutes)

```markdown
Create a 45-minute creative brainstorming agenda for [TOPIC].
- Phase 1 (10m): Context & Customer Problem
- Phase 2 (15m): Silent Idea Generation (Figma / Doc)
- Phase 3 (15m): Idea Clustering & Voting
- Phase 4 (5m): Selection of Top 2 Prototypes to Test
```

---

## Real-World Case Study

### Scenario: Product Launch Go/No-Go Decision Meeting

#### Weak Default Prompt
> *"Write an agenda for our product launch meeting."*
> ❌ *Result: A generic list of topics (Status, Marketing, Bugs, Next Steps) with no time allocations or decision focus.*

#### Outcome-Driven Agenda Output

> # 🚀 Go/No-Go Decision Sync: Q3 Mobile App Release
> 
> **🎯 Single Primary Objective**: Formally approve or delay the public App Store release scheduled for Oct 15th.
> 
> **📄 Mandatory Pre-Reads (5-Min Prep)**:
> - QA Bug Dashboard (Link)
> - Staging Server Load Test Report (Link)
> 
> ---
> 
> ### Time-Blocked Schedule (30 Minutes Total)
> 
> | Time Window | Duration | Topic | Discussion Lead | Target Outcome |
> | :--- | :--- | :--- | :--- | :--- |
> | **10:00 - 10:05** | 5 mins | **Current Status & Release Criteria** | Engineering Lead | Confirm P0 bug count ($0$) and P1 count ($< 2$). |
> | **10:05 - 10:15** | 10 mins | **Infrastructure & Scalability Risk** | DevOps Lead | Review peak load stress test results & rollback plan. |
> | **10:15 - 10:25** | 10 mins | **Customer Support & Marketing Readiness**| Marketing / CS Lead | Verify help center FAQs and launch email sequence. |
> | **10:25 - 10:30** | 5 mins | **Final Vote & Action Item Sign-off** | Executive Sponsor | Recorded Go / No-Go decision and task assignments. |

---

## 4 Rules of High-Impact Agendas
1. **No Agenda = No Meeting**: Send the agenda at least 4 hours before the call.
2. **Every topic has a dedicated lead**: Prevent "anyone can talk" vacuum.
3. **Include the target outcome in the table**: Clarify whether a segment is for *information sharing*, *debate*, or *final decision*.
4. **Reserve the final 5 minutes**: Never run out of time before assigning owners to action items.
