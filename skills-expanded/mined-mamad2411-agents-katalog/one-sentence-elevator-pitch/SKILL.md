---
name: one-sentence-elevator-pitch
description: "Condense a product or initiative into one sentence identifying its audience, purpose, and distinguishing benefit."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["elevator-pitch", "value-proposition", "positioning", "copywriting", "distillation", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Request a One-Sentence Value Proposition (The XY Pitch Formula) (AI Skill)

## Overview
When asked to describe a new product, startup, or internal initiative, founders and team leads often write 3 paragraphs of technical jargon that obscures what the product actually does.

The **One-Sentence XY Pitch Protocol** forces the AI into radical distillation, generating crisp, memorable elevator pitches using proven venture capital and positioning formulas.

---

## The XY Positioning Formula

```
┌─────────────────────────────────────────────────────────────┐
│                 The Classic XY Pitch Formula                │
│                                                             │
│  "We help [TARGET AUDIENCE] achieve [TRANSFORMATIVE BENEFIT]│
│   without [THE PRIMARY PAIN POINT / OBSTACLE]."             │
│                                                             │
│  • Example: "We help remote engineering teams ship 2x faster│
│              without running daily status standups."        │
└─────────────────────────────────────────────────────────────┘
```

---

## Master One-Sentence Pitch Prompt Templates

### Pattern 1: The 4-Archetype Pitch Generator
Use when launching a product or clarifying your company positioning:

```markdown
Here is a raw description of my product / project: [PASTE PRODUCT NOTES].

Condense this into 4 distinct **1-Sentence Elevator Pitches** following these formulas:
1. **The Classic XY Formula**: "We help [X] do [Y] without [Z]."
2. **The High-Concept Analogy**: "The [Famous Product A] for [Niche B]."
3. **The Quantified ROI Pitch**: "Save [Metric/Time/Money] by [Core Mechanism]."
4. **The Pain-Killer Pitch**: "Stop [Painful Problem] with [Simple Solution]."

Rules:
- Strictly ONE sentence per option.
- Under 25 words per pitch.
- Zero vague buzzwords ("revolutionize", "seamless", "synergy").
```

---

### Pattern 2: The Internal Project Executive Pitch
Use when pitching a budget or initiative to senior management:

```markdown
I need a 1-sentence summary for our executive leadership team about [PROJECT: e.g. Kubernetes Migration].
- Focus on cost savings and uptime impact.
- Make it so clear that a non-technical CEO understands it immediately.
```

---

## Real-World Case Study

### Scenario: API Observability & Debugging Tool

#### Bloated Traditional Description (Confusing & Jargon-Heavy)
> *"Our state-of-the-art distributed telemetry platform leverages advanced eBPF kernel instrumentation and AI-driven anomaly heuristics to empower enterprise microservice architectures with real-time holistic visibility across multi-cloud Kubernetes clusters..."*
> 
> ❌ *(Takes 45 seconds to read; nobody understands what it actually does).*

#### One-Sentence Pitch Archetypes (Instant Comprehension)

| Archetype | One-Sentence Pitch | Why It Works |
| :--- | :--- | :--- |
| **1. Classic XY** | *"We help backend engineers pinpoint API errors in production in 30 seconds without adding logging code to their codebase."* | Highlights exact target user, core benefit, and eliminated pain. |
| **2. High-Concept Analogy** | *"The Google Analytics for backend API performance."* | Leverages instant mental models from familiar products. |
| **3. Quantified ROI** | *"Cut production downtime diagnosis from 45 minutes to 60 seconds."* | Focuses purely on quantifiable business time savings. |
| **4. Pain-Killer** | *"Never wake up at 2 AM to read through messy cloud server logs again."* | Taps into deep emotional frustration and immediate relief. |

---

## Summary Best Practices
- **Enforce the word ceiling**: Adding *"Keep each option under 20 words"* forces the AI to eliminate filler and choose the strongest verbs.
- **Ban analogy abuse**: If using the *"X for Y"* formula, make sure the comparison is immediately obvious (e.g. *"Uber for groceries"* vs *"Salesforce for dog walkers"*).
