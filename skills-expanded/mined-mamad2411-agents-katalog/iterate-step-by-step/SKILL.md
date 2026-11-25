---
name: iterate-step-by-step
description: "Develop a complex deliverable in reviewable stages, carrying forward agreed requirements and decisions."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["iteration", "scaffolding", "workflow", "multi-turn", "agile", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Iterate Step-by-Step (Conversational Scaffolding) (AI Skill)

## Overview
Expecting an AI to produce a finished, 10/10 masterpiece in a single massive prompt (*"Write a complete multi-chapter marketing strategy and all ad copy"*) is a recipe for disappointment. The model spreads its attention across too many variables, producing shallow text and skipped details.

The **Conversational Scaffolding Protocol** breaks production into a **4-Turn Agile Loop**: scaffold the outline $\rightarrow$ build the core engine $\rightarrow$ harden edge cases $\rightarrow$ polish the final output.

---

## The 4-Turn Scaffolding Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 4-Turn Scaffolding Pipeline                 │
│                                                             │
│  [ TURN 1: Wireframe / Skeleton ] ──► Agree on structure    │
│                 │                                           │
│  [ TURN 2: Core Drafting / Build ] ──► Generate meat        │
│                 │                                           │
│  [ TURN 3: Stress-Test & Edges ]   ──► Catch flaws & bugs   │
│                 │                                           │
│  [ TURN 4: Surgical Polish ]       ──► Voice, SEO, & CTA    │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Iteration Prompt Templates

### Pattern 1: The 4-Turn Execution Script
Use when building a complex deliverable (e.g. business plan, landing page, software module):

```markdown
<!-- TURN 1: The Skeleton -->
"We are going to build [PROJECT]. Do NOT write the content yet.
Give me a 5-point structural outline. I will review and adjust."

<!-- TURN 2: The Core Build (After adjusting Turn 1) -->
"The outline is locked. Now write Section 1 and Section 2 ONLY. 
Follow our agreed constraints and focus on high depth."

<!-- TURN 3: Edge-Case Hardening -->
"Now review what we have so far. Where are the weak points or missing scenarios? 
Suggest 3 specific additions."

<!-- TURN 4: The Final Polish -->
"Apply the additions from Turn 3 and output the polished, production-ready version."
```

---

## Real-World Case Study

### Scenario: Building a High-Converting SaaS Landing Page

#### The 1-Shot Megaprompt Failure
> **User**: *"Write a complete landing page for my new AI bookkeeping software including headlines, features, pricing, testimonials, and FAQs."*
> 
> ❌ *Result: A generic 600-word block of clichéd marketing text ("Revolutionize your finances today! Save time and money!") with zero competitive edge.*

#### The 4-Turn Scaffolding Success
> - **Turn 1 (Scaffold)**: User asks for a 5-section narrative wireframe $\rightarrow$ AI suggests: Hero $\rightarrow$ Relatable Pain $\rightarrow$ Interactive Demo $\rightarrow$ Social Proof $\rightarrow$ FAQ. User approves.
> - **Turn 2 (Hero & Hook)**: User prompts: *"Write 3 bold variations for the Hero Section. Focus on eliminating tax season dread."* User selects the best hook.
> - **Turn 3 (Feature Breakdown)**: User prompts: *"Now write the 3 feature blocks highlighting our automated receipt OCR and zero-reconciliation features."*
> - **Turn 4 (FAQ & Polish)**: User prompts: *"Generate 4 objection-crushing FAQs addressing data security and accountant collaboration."*

**Outcome**: A cohesive, deeply tailored, high-converting landing page built in under 4 minutes with zero token waste.

---

## Why Iteration Beats Megaprompting
- 🎯 **Total Creative Steering**: You catch structural flaws in Turn 1 before writing 2,000 words in the wrong direction.
- 💡 **Deeper Attention**: The AI devotes 100% of its context window and compute to one section at a time.
- ⚡ **Zero Overwhelm**: You review bite-sized chunks rather than a 10-page wall of text.
