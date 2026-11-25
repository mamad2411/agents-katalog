---
name: state-your-goal-not-just-command
description: "Explain the underlying outcome and constraints so a requested implementation can be assessed against the real goal."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["xy-problem", "intent-prompting", "problem-solving", "clarity", "root-cause", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# State Your Goal Not Just the Command (The XY Problem Solver) (AI Skill)

## Overview
The **XY Problem** is a classic cognitive trap: you want to achieve goal **X**, but you assume mechanism **Y** is the solution, so you ask an AI for help implementing **Y** (*e.g., "How do I use a complex regex to extract the last 3 letters of a filename?"*).

The AI will faithfully answer your literal question (writing a fragile regex), whereas if you had stated your true goal **X** (*"I want to check if a file is an image"*), the AI would provide the vastly superior 1-line native solution (`filename.endswith(('.png', '.jpg'))`).

The **Underlying Intent Protocol** ensures you always state the ultimate outcome, enabling the AI to recommend simpler, more elegant approaches.

---

## The XY Problem Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 The Classic XY Problem                      │
│                                                             │
│  TRUE GOAL (X): "I need to check if uploaded files are PNGs"│
│           │                                                 │
│           ▼ (User assumes wrong path)                       │
│  ATTEMPTED FIX (Y): "Write a complex regex on file string"  │
│                                                             │
│  • Asking for Y only $\rightarrow$ Fragile, 20-line regex   │
│  • Stating X + Y     $\rightarrow$ "Use `pathlib.suffix` or │
│                                    MIME validation instead" │
└─────────────────────────────────────────────────────────────┘
```

---

## The 2-Part Intent Formula

```
┌───────────────────────────────────────────────────────────────────────────┐
│ 1. THE TASK I AM TRYING TO DO: "I was trying to write a custom cron job..."│
│ 2. THE ULTIMATE GOAL (WHY):    "...because I need to auto-delete temporary │
│                                 uploads older than 24h from AWS S3."       │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Master Intent-First Prompt Templates

### Pattern 1: The "Outcome + Attempted Path" Template
Use for software architecture, devops, and database design:

```markdown
Here is what I am trying to achieve:
- **Ultimate Goal (X)**: [DESCRIBE THE FINAL OUTCOME / USER EXPERIENCE]
- **My Current Idea (Y)**: [DESCRIBE WHAT YOU WERE PLANNING TO DO]

Questions:
1. Is my current idea (Y) the optimal way to achieve (X)?
2. If yes: provide the implementation.
3. If no: what is the simpler, standard industry pattern to achieve (X)?
```

---

### Pattern 2: The Business & Operational Intent Directive
Use for workflows, automation, and spreadsheet logic:

```markdown
I want to [INSERT BUSINESS GOAL: e.g. Automatically notify sales reps when a lead books a demo].

Instead of just answering my literal question, let me know if there is a zero-code or built-in tool that accomplishes this faster.
```

---

## Real-World Case Study

### Scenario: Sizing Cloud Instances

#### Literal Command (Trapped in Y)
> **User**: *"How do I configure a custom Python daemon on an EC2 instance to poll a database every 5 seconds for new customer signups and send a Slack alert?"*
> 
> ❌ *AI gives 80 lines of Python daemon code, systemd service units, and connection pooling.*

#### Intent-First Prompt (Solved with X)
> **User**: *"Goal: We need real-time Slack alerts when a new customer signs up in our PostgreSQL database. I was thinking of running a polling script on an EC2 server, but what is the simplest, lowest-maintenance way to do this?"*

**AI Response**:
> **Superior Solution**: Do not run a server or polling daemon. 
> Use a native **PostgreSQL Database Webhook / Supabase Edge Function** or an **AWS Lambda function on DynamoDB Streams** to push a webhook to Slack directly on row insertion.
> - **Cost**: $0.00 / month (Runs within free tier vs $15/mo EC2 server).
> - **Maintenance**: Zero servers to patch or keep alive.

---

## Summary Best Practices
- **Always include the word "Because"**: Adding *"I need to do this because [GOAL]"* unlocks the model's architectural reasoning.
- **Invite better alternatives**: Explicitly prompt: *"If there is a better way to solve this, challenge my approach."*
