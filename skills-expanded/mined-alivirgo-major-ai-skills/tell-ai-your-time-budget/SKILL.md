---
name: tell-ai-your-time-budget
description: "State the available time so the proposed approach fits the deadline and level of effort."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["time-budget", "scoping", "pragmatism", "quick-fixes", "engineering-tradeoffs", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Tell AI Your Time Budget (Time-Calibrated Scoping) (AI Skill)

## Overview
When you ask an AI how to solve a problem (*"How do I fix memory leaks in Node.js?"*), it assumes you have infinite time and recommends a 3-day deep architecture overhaul with profiling tools, automated heap snapshots, and load-testing pipelines.

If you only have **15 minutes before an executive presentation**, an architectural overhaul is useless. You need a fast, low-risk operational patch.

The **Time-Calibrated Scoping Protocol** anchors the AI to your **exact available execution window** (5 Minutes, 1 Hour, or 1 Week), ensuring the suggested solution fits your real-world calendar constraints.

---

## The 3-Tier Time Budget Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 Time-Calibrated Solutions                   │
│                                                             │
│  [ TIER 1: 5-Minute Quick Patch ]  ──► Band-aid for demo    │
│  [ TIER 2: 1-Hour Practical Fix ]  ──► Stable sprint PR     │
│  [ TIER 3: 2-Day Permanent Build ] ──► Complete refactor    │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Time-Budget Prompt Templates

### Pattern 1: The Demo / Emergency 5-Minute Patch

```markdown
I have a bug / problem: [DESCRIBE ISSUE].

Time Budget: **I have only 10 minutes before an executive demo.**
- Give me the fastest, lowest-risk band-aid to hide or bypass the issue right now.
- Do NOT suggest deep refactoring. 
- State the 1-line emergency fix.
```

---

### Pattern 2: The Multi-Tier Time Spectrum
Use when evaluating tactical trade-offs:

```markdown
I need to solve [PROBLEM: e.g. High latency on user profile image loading].

Provide 2 solutions based on time budget:
1. **The 30-Minute Tactical Win**: What can I implement and test in $<30$ minutes today?
2. **The Weekend Strategic Fix**: What is the robust, permanent solution for next sprint?
```

---

## Real-World Case Study

### Scenario: High Memory Usage on a Production Server

#### Without Time Budget (Unrealistic 3-Day Plan)
> **User**: *"Node.js server memory is growing steadily every hour. How do I fix it?"*
> ❌ *AI recommends installing Clinic.js, recording 4-hour heap profiles, setting up Prometheus metric scrapers, and rewriting memory caching libraries.*

#### With 10-Minute Time Budget (Immediate Mitigation)
> **User**: *"Node.js server memory is growing steadily. **I have 5 minutes to prevent a crash before peak traffic.** Give me an emergency operational mitigation."*

**AI Response**:
> **Immediate 5-Minute Emergency Action**:
> 1. **Restart Workers with PM2 Memory Ceiling**: Configure PM2 to automatically recycle workers when they hit 800MB without dropping connections:
>    ```bash
>    pm2 reload all --max-memory-restart 800M
>    ```
> 2. **Result**: Eliminates the risk of OOM crash immediately; buys you 2 weeks to profile the memory leak calmly during normal business hours.

---

## Summary Best Practices
- **State your clock time**: *"I have 15 minutes right now"* completely transforms the model's recommendation.
- **Differentiate 'Patch' from 'Architecture'**: Clarify whether you want an immediate emergency tourniquet or a permanent architectural cure.
