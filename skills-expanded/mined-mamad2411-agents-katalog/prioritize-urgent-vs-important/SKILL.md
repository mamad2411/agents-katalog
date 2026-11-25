---
name: prioritize-urgent-vs-important
description: "Sort a task list by urgency and importance to identify work to do, schedule, delegate, or remove."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["eisenhower-matrix", "task-prioritization", "time-management", "productivity", "deep-work", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Prioritize Tasks Using the Eisenhower Matrix (AI Skill)

## Overview
Staring at a flat list of 20 unranked tasks triggers decision fatigue. People naturally gravitate toward easy, low-impact tasks (*"clean up desktop icons"*, *"reply to casual emails"*) while avoiding high-leverage, complex strategic work.

The **Eisenhower Matrix Task Triage Protocol** commands the AI to sort your raw to-do list into the **4 Classic Productivity Quadrants**: urgent firefighting, high-ROI deep work, delegable tasks, and zero-value time traps.

---

## The 4 Eisenhower Quadrants

```
┌─────────────────────────────────────────────────────────────┐
│                 The Eisenhower Matrix Grid                  │
│                                                             │
│  Q1: DO FIRST (Urgent & Important)                          │
│  • P0 Outages, client contract deadlines, safety risks      │
│                                                             │
│  Q2: SCHEDULE (Not Urgent, but HIGH ROI) ──► 80% LEVERAGE   │
│  • System refactoring, strategic planning, skill mastery    │
│                                                             │
│  Q3: DELEGATE / AUTOMATE (Urgent, Not Important)            │
│  • Scheduling calls, routine data entry, basic formatting   │
│                                                             │
│  Q4: ELIMINATE / KILL (Neither Urgent nor Important)        │
│  • Unnecessary sync meetings, busywork, vanity metrics      │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Task Prioritization Prompt Templates

### Pattern 1: The Morning 9 AM Triage Engine
Use when staring at an overwhelming to-do list at the start of the day:

```markdown
Here is my raw to-do list for today:
[PASTE RAW TASKS & NOTES]

My Primary Goal for today is: [CORE GOAL].

Triage these tasks using the Eisenhower Matrix into 4 distinct Markdown tables:
1. **Q1: DO FIRST (Top 2-3 Urgent & Critical Tasks)** - Must finish before lunch.
2. **Q2: DEEP WORK BLOCK (High-Leverage / Strategic)** - Time-box for 90 minutes.
3. **Q3: DELEGATE / FAST BATCH** - Batch into a 20-minute admin blitz or delegate.
4. **Q4: ELIMINATE / DEFER** - Tasks that provide $<5\%$ value and should be cancelled.

For Q1 and Q2, specify the recommended order of execution.
```

---

### Pattern 2: The Project Scope Cutter (Feature Backlog Triage)

```markdown
Review our feature backlog: [PASTE FEATURE LIST].

Categorize features into:
- **Must-Have for v1 (Q1)**
- **Strategic Differentiation for v2 (Q2)**
- **Nice-to-Have / Defer (Q4)**
```

---

## Real-World Case Study

### Scenario: Freelance Founder's Monday Morning Task Dump

#### Raw Task Dump
> *"1) Fix Stripe billing bug affecting 3 users, 2) Redesign company logo, 3) Write quarterly investor update, 4) Reply to 15 cold LinkedIn InMails, 5) Refactor customer onboarding database queries, 6) Order new office coffee, 7) Prep proposal for $25k enterprise lead due at 5 PM."*

#### AI Eisenhower Triage Output

```markdown
### 🚨 Q1: DO FIRST (Immediate Revenue & Risk / Finish by 1:00 PM)
1. **Fix Stripe Billing Bug**: Direct financial leak; 3 users blocked. (Estimate: 45 mins).
2. **$25k Enterprise Proposal**: Hard deadline at 5 PM; high revenue impact. (Estimate: 90 mins).

### 🎯 Q2: SCHEDULE (Deep Work Block / 2:00 PM - 4:00 PM)
- **Investor Quarterly Update**: High strategic value for future funding runway.
- **Onboarding Query Optimization**: Drives long-term user retention.

### ⚡ Q3: FAST BATCH / DELEGATE (4:00 PM - 4:30 PM Admin Blitz)
- **Order Office Supplies**: 2-minute task.
- **Cold InMails**: Archive or use standard snippet reply.

### 🗑️ Q4: ELIMINATE / KILL
- **Logo Redesign**: Zero revenue impact; pure procrastination distraction. Kill for now.
```

---

## Summary Best Practices
- **Never start your day in Q3/Q4**: Protect your first 2 hours exclusively for Q1 and Q2 tasks.
- **Kill at least 1 task every day**: If you aren't actively eliminating items into Q4, your filter isn't strict enough.
