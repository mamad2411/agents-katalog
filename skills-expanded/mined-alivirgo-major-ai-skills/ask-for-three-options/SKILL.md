---
name: ask-for-three-options
description: "Compare conservative, balanced, and ambitious approaches with their trade-offs when choosing a course of action."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["decision-frameworks", "options-triad", "brainstorming", "risk-calibration", "strategy", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask for Options A, B, and C (The Rule of 3) (AI Skill)

## Overview
When users ask an AI for *"the best way"* to solve a problem, the model provides a single homogenized answer. However, real-world decisions always involve trade-offs between **time, cost, and risk**. 

Requesting **exactly 3 distinct options along a calibrated spectrum** (Conservative, Balanced, and Bold) provides optimal decision leverage without causing analysis paralysis.

---

## The Triad Spectrum Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 The 3-Option Decision Spectrum              │
│                                                             │
│  [ OPTION A: Low Risk / Fast ]  ──► Band-aid / Quick Fix    │
│  [ OPTION B: Pragmatic / Mid ]  ──► Industry Best Practice  │
│  [ OPTION C: Bold / Strategic]  ──► Radical / Long-term Fix │
└─────────────────────────────────────────────────────────────┘
```

- **Option A (The Conservative / Quick Fix)**: Fastest to implement, lowest risk, lowest cost, but solves only immediate symptoms.
- **Option B (The Balanced / Industry Standard)**: Proven best practice, moderate investment, balanced trade-offs.
- **Option C (The Bold / High-Leverage)**: Radical transformation, higher upfront effort/risk, but permanently solves the root cause or unlocks competitive advantage.

---

## Master 3-Option Prompt Templates

### Pattern 1: The Tactical Spectrum Prompt
Use this for technical architecture, operational problems, or business strategy:

```markdown
I am facing the following challenge: [INSERT PROBLEM & CONSTRAINTS].

Provide exactly 3 distinct solutions along this spectrum:
1. **Option A (Quick & Low-Risk)**: What can we ship today/this week with minimal effort?
2. **Option B (Balanced & Pragmatic)**: What is the proven, standard industry approach?
3. **Option C (Bold & High-Leverage)**: What is the ambitious, out-of-the-box architectural solution?

For each option, include:
- Summary (2 sentences)
- Implementation Time & Effort
- Trade-off / Primary Risk
```

---

### Pattern 2: The Communication Tone Triad
Use when drafting sensitive emails, crisis statements, or salary negotiations:

```markdown
Draft a reply to [SITUATION / EMAIL].

Give me 3 tone variations:
- **Option 1 (Diplomatic & Accommodating)**: Warm, polite, de-escalating.
- **Option 2 (Firm & Direct)**: Professional, clear boundary setting, no fluff.
- **Option 3 (Assertive & Leverage-Focused)**: Uncompromising, strictly terms-based.
```

---

## Real-World Case Study

### Scenario: High Database Query Latency Spikes

#### Weak Single-Option Prompt
> *"How do I fix high latency in MySQL during flash sales?"*
>
> ❌ *Result: AI suggests a 10-step generic guide to indexing and sharding.*

#### 3-Option Spectrum Prompt & Output
> **User Prompt**:
> *"Our MySQL database CPU hits 98% during 15-minute flash sales. Give me Options A, B, and C to resolve this."*

**AI Response**:

#### Option A: The Quick Band-Aid (Ship Today)
- **Mechanism**: Place a Redis Cache layer in front of the 5 most heavily read product/pricing queries with a 60-second TTL.
- **Effort**: 4 hours.
- **Trade-off**: Cache invalidation delays (stale stock counts for up to 60 seconds).

#### Option B: The Industry Standard (Ship This Sprint)
- **Mechanism**: Set up an AWS Aurora Read Replica specifically for read-heavy catalog traffic, routing checkout writes to the primary writer instance.
- **Effort**: 2 days.
- **Trade-off**: Additional cloud infrastructure cost (~$250/mo).

#### Option C: The High-Leverage Architectural Pivot (Next Quarter)
- **Mechanism**: Pre-generate static JSON catalog payloads at edge CDNs (Cloudflare Workers) and decouple catalog browsing completely from the SQL database.
- **Effort**: 3 weeks.
- **Trade-off**: Requires reworking frontend client fetching architecture, but enables infinite scale with zero database load during flash sales.

---

## The Effort vs. Impact Scorecard

| Option Type | Implementation Speed | Long-Term Durability | Risk Level |
| :--- | :--- | :--- | :--- |
| **Option A (Conservative)** | ⚡ Hours | ⚠️ Low (Temporary) | 🟢 Minimal |
| **Option B (Balanced)** | ⏱️ Days/Weeks | 🟢 High (Stable) | 🟡 Moderate |
| **Option C (Bold)** | 🏗️ Months | 🚀 Permanent / Game Changer | 🔴 Higher Complexity |

---

## Why "3" is the Golden Number
- **1 Option**: You are a passive spectator taking orders from an AI.
- **3 Options**: You are an empowered executive choosing the right risk/reward trade-off for your specific context.
- **5+ Options**: You trigger cognitive overload and analysis paralysis.
