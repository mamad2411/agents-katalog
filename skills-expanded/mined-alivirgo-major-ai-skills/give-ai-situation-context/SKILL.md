---
name: give-ai-situation-context
description: "Include role, scale, budget, and constraints so an answer fits the actual working situation."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["context-anchoring", "constraints", "tailored-advice", "prompt-engineering", "efficiency", "productivity"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Give AI Situation & Constraint Context (AI Skill)

## Overview
Asking an unanchored question like *"What database should I use for my app?"* forces the AI to guess who you are. The model will often recommend enterprise solutions like Amazon DynamoDB clusters with multi-region replication - which is disastrously complex for a solo founder building a weekend MVP.

The **Situation Anchoring Framework** teaches you to spend 15 seconds defining your **Role, Scale, Budget, and Constraints** upfront, ensuring the AI's advice is 100% appropriate for your real-world circumstances.

---

## The 4-Pillar Situation Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 The 4-Pillar Situation Stack                │
│                                                             │
│  1. WHO I AM      ──► Solo founder, Lead Architect, Student │
│  2. WHAT I HAVE   ──► $50/mo budget, 2-person team, Node.js │
│  3. CONSTRAINTS   ──► Must ship in 7 days, zero DevOps staff│
│  4. SUCCESS STATE ──► First 100 paying users, sub-50ms speed│
└─────────────────────────────────────────────────────────────┘
```

---

## Master Situation-Anchoring Prompt Templates

### Pattern 1: The Tactical Situation Anchor
Use before asking for architectural, marketing, or business strategy advice:

```markdown
Situation Context:
- **My Role / Team**: Solo non-technical founder building an MVP.
- **Budget**: Maximum $50/month total infrastructure spend.
- **Timeline**: Must launch a working beta in 14 days.
- **Existing Tech Stack**: Next.js hosted on Vercel.

Question / Problem:
[INSERT QUESTION: e.g. How should I handle transactional emails and user notifications?]
```

---

### Pattern 2: The Enterprise vs. Startup Filter
Forces the model to eliminate enterprise bloat or naive beginner tools:

```markdown
I need advice on [TOPIC].

Filter your response through these realities:
- We are a [SERIES A STARTUP / BOOTSTRAPPED INDIE / FORTUNE 500 ENTERPRISE].
- We have [X] engineers and [Y] monthly active users.
- Discard any recommendations that require heavy custom Kubernetes infrastructure or >$500/mo licensing.
```

---

## Real-World Comparison

### Scenario: Choosing an Authentication System

#### Without Situation Context (The Enterprise Bloat Trap)
> **User**: *"How should I set up user authentication for my new web app?"*
> 
> ❌ *AI Output: "Set up an enterprise Okta or Auth0 tenant, configure OAuth2 with PKCE, deploy a Redis token cache, and manage SAML single sign-on..."* (Cost: $250+/mo, Weeks of setup).

#### With Situation Context (Laser-Targeted Perfection)
> **User**: *"Situation: Solo developer building a lightweight SaaS tool with Next.js and Supabase. Zero budget for third-party auth fees. What is the fastest, safest way to implement auth?"*

**AI Response**:
> **Recommendation**: Use **Supabase Auth (Native SSR)**.
> 
> **Why It Fits Your Situation**:
> 1. **Zero Added Cost**: Free tier includes 50,000 monthly active users.
> 2. **Instant Setup**: Built directly into your Supabase database; handles Google Sign-In, Magic Links, and JWT session cookies in under 30 lines of Next.js middleware code.
> 3. **Launch Time**: Implementable in under 2 hours with zero third-party auth redirect overhead.

---

## Summary Checklist
- **State your team size**: Solo vs. 5-person team vs. 100-person company changes the answer completely.
- **Declare your budget ceiling**: Prevents models from recommending expensive SaaS tools when a free open-source script will do.
- **Name your deadline**: Tells the AI whether to optimize for long-term perfection or immediate shipping speed.
