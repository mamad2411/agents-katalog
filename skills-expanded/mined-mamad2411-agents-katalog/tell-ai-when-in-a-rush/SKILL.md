---
name: tell-ai-when-in-a-rush
description: "Request a concise prioritized answer when time is short, preserving critical facts and uncertainty."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["emergency-mode", "high-velocity", "incident-response", "quick-answers", "triage", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Tell AI When You Are in a Rush (High-Velocity Triage) (AI Skill)

## Overview
When you are on an active customer call, in an executive meeting, or debugging a live production outage, you do not have 45 seconds to wait for an AI to generate a multi-paragraph essay. You need the **exact answer or CLI command on line 1 within 3 seconds**.

The **High-Velocity Emergency Protocol** signals extreme urgency to the model, instantly cutting off all discursive explanations and outputting pure tactical solutions.

---

## Standard Chat vs. High-Velocity Emergency Mode

```
┌─────────────────────────────────────────────────────────────┐
│                 Emergency Response Velocity                 │
│                                                             │
│  Standard Query ("How do I kill PostgreSQL backend?"):      │
│  "PostgreSQL provides administrative functions for managing │
│   client connections. In order to terminate a backend..."   │
│  ↳ 25-Second Generation Time $\rightarrow$ Production Outage Stalls │
│                                                             │
│  Emergency Directive ("EMERGENCY - COMMAND ONLY"):          │
│  `SELECT pg_terminate_backend(pid) FROM pg_stat_activity...`│
│  ↳ 2-Second Generation Time $\rightarrow$ Production Outage Fixed │
└─────────────────────────────────────────────────────────────┘
```

---

## Master High-Velocity Prompt Templates

### Pattern 1: The Outage & SRE Emergency Fix (Code / Terminal)
```markdown
🚨 EMERGENCY FIX NEEDED:
[DESCRIBE CRASH / ISSUE]

Rules:
- Give the EXACT command / SQL query on line 1.
- No greetings, no explanations. I will ask questions after it is resolved.
```

---

### Pattern 2: The Live Meeting Fact-Check (Executive / Client Call)
```markdown
⚡ IN A LIVE MEETING - 1-LINE ANSWER ONLY:
[INSERT QUESTION: e.g. Does California require overtime pay after 8 hours in a day or 40 hours in a week?]

Format:
- Line 1: Direct Yes/No or Fact.
- Line 2: The governing statutory rule.
```

---

### Pattern 3: The Live Negotiation Counter-Script
```markdown
⚡ LIVE NEGOTIATION - GIVE ME 1 SPOKEN LINE:
The client just said: "[PASTE CLIENT OBJECTION / PUSHBACK]".

Give me the single best 1-sentence de-escalating counter-phrase I can say right now.
```

---

## Real-World Case Study

### Scenario: Live Incident Response (Postgres Database Lock)

#### Standard Prompt (Too Slow for an Outage)
> **User**: *"How do I find and kill stuck queries in Postgres?"*
> ❌ *AI outputs 400 words explaining lock types, table locks, and row-level locks.*

#### Emergency Mode Prompt (Instant Fix)
> **User**: *"🚨 EMERGENCY - SERVER DOWN: Give me the SQL query to find and kill all queries running $> 60$ seconds. SQL ONLY."*

**AI Response**:
```sql
SELECT pg_terminate_backend(pid), query, state, age(clock_timestamp(), query_start)
FROM pg_stat_activity
WHERE state != 'idle' 
  AND query_start < now() - interval '60 seconds'
  AND pid <> pg_backend_pid();
```

---

## Summary Best Practices
- **Use the `⚡` or `🚨 EMERGENCY` flag**: Prefixing prompts with urgent visual flags anchors the model to brevity.
- **Demand "Line 1" execution**: Always state *"Provide the command on line 1; zero explanation"*.
