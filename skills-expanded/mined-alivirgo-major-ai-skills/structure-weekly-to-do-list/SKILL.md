---
name: structure-weekly-to-do-list
description: "Organize weekly tasks into realistic work blocks based on priorities, deadlines, and available capacity."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["weekly-planning", "time-blocking", "task-management", "productivity", "thematic-days", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Structure Your Weekly To-Do List (Thematic Time-Blocking) (AI Skill)

## Overview
Dumping 25 unrelated tasks into a single unorganized to-do list creates cognitive overload. People attempt to do high-focus coding or writing between fragmented client calls, resulting in context switching and burnout.

The **Thematic Weekly Sprint Protocol** uses AI to organize a raw weekly task dump across a **5-Day Thematic Cadence**, matching task complexity with human daily energy curves and time-blocking morning deep work.

---

## The 5-Day Thematic Weekly Rhythm

```
┌─────────────────────────────────────────────────────────────┐
│                 5-Day Thematic Sprint Rhythm                │
│                                                             │
│  [ MON: Planning & High-Priority Firefighting ]             │
│  [ TUE: Deep Work Core Build (Zero Meeting Day) ] ──► PEAK  │
│  [ WED: Deep Work Integrations & Architecture ]   ──► FOCUS │
│  [ THU: Client Syncs, Code Reviews, & Demos ]               │
│  [ FRI: Low-Energy Admin, Bug Triage, & Retros ]            │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Weekly Planner Prompt Templates

### Pattern 1: The Thematic 5-Day Sprint Organizer
Use on Sunday evening or Monday morning:

```markdown
Here is my raw task dump for this week:
[PASTE RAW TASKS & DEADLINES]

Context & Preferences:
- Maximum 1 major Deep Work task (90-120 mins) per day.
- Keep Tuesday and Wednesday mornings completely clear of admin work.
- Schedule meetings and reviews for Thursday.
- Reserve Friday for low-energy admin, invoices, and planning.

Task:
Generate a structured Monday-to-Friday Weekly Plan in Markdown:
For each day, provide:
- **Daily Theme**
- **Morning Deep Work Focus (P0 Task)**
- **Afternoon Tactical / Admin Blitz (Max 3 items)**
- **Total Estimated Hours**
```

---

## Real-World Case Study

### Scenario: Freelance Engineer's Weekly Task Chaos

#### Raw Task Dump
> *"Deploy staging DB, send 3 invoices, write technical blog post, prepare Thursday client demo, fix Stripe webhook bug, update resume, review PR #42, clean email inbox, research GraphQL vs tRPC."*

#### AI Thematic Schedule Output

```markdown
### 🗓️ Monday: Scoping & Critical Fixes
- **Morning Deep Work**: Fix Stripe webhook race condition (P0 Financial Blocker).
- **Afternoon Tactical**: Deploy staging database update; triage urgent Slack messages.

### 🚀 Tuesday: Deep Build Day (Zero Meetings)
- **Morning Deep Work**: Write technical blog post on distributed caching (First draft).
- **Afternoon Tactical**: Research GraphQL vs. tRPC architecture for Q4 roadmap.

### 🏗️ Wednesday: Architecture & Code Polish
- **Morning Deep Work**: Review and merge PR #42; optimize slow query indexes.
- **Afternoon Tactical**: Finalize blog post revisions and graphics.

### 🤝 Thursday: Collaboration & Client Demos
- **Morning Focus**: Prepare interactive slides and staging demo.
- **Afternoon Tactical**: Host Client Demo call; document follow-up action items.

### 🧹 Friday: Admin, Finance & Weekly Wrap-Up
- **Morning Focus**: Send 3 pending client invoices; reconcile bank receipts.
- **Afternoon Low-Energy**: Update resume; zero out email inbox; plan next week's sprint.
```

---

## Summary Best Practices
- **Never assign more than 1 P0 task per morning**: High-focus deep work is finite ($~3\text{ hours/day}$).
- **Batch admin tasks together**: Clustering invoices, emails, and small forms on Friday afternoon prevents them from breaking your midweek coding flow.
