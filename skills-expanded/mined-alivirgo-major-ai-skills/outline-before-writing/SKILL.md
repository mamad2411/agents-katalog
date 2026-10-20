---
name: outline-before-writing
description: "Agree on a document outline and logical progression before drafting a long piece."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["outlining", "writing-workflows", "document-structure", "planning", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Outline Documents Before Writing (The Structural Gate) (AI Skill)

## Overview
When asked to write a 1,500-word article, technical guide, or report in a single prompt, AI models generate a flat, unstructured wall of text where subtopics overlap, key arguments are buried, and transitions feel disjointed.

The **Structural Outline Gate Protocol** requires the AI to generate a strict, hierarchical **5-to-7 point outline** first. Once you review, reorder, or trim headings, each section is expanded with surgical precision.

---

## The Structural Gate Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                 The Structural Outline Gate                 │
│                                                             │
│  User Topic ──► [ STEP 1: Generate 5-Point Hierarchical Outline ] │
│                                   │                         │
│  Human Reviews & Adjusts ◄────────┘                         │
│  (Swap sections, delete filler, add unique case study)      │
│           │                                                 │
│           ▼                                                 │
│  [ STEP 2: Lock Headings & Expand Section by Section ]       │
│  ↳ Cohesive, High-Depth, Zero-Rambling Final Document       │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Outlining Prompt Templates

### Pattern 1: The Hierarchical Outline Gate
Use for long-form essays, whitepapers, guides, and proposals:

```markdown
I want to write a comprehensive guide on [TOPIC].
Target Audience: [AUDIENCE: e.g. Staff Engineers / Marketing Directors].
Primary Thesis / Message: [CORE THESIS].

Do NOT start writing the full text yet.
Provide a **Hierarchical Outline** with:
1. Exactly 5 to 6 major numbered H2 sections.
2. Under each H2, list 2-3 specific bullet points detailing the exact arguments, examples, or metrics to be covered.
3. Suggest a 1-sentence opening hook for the introduction.

Conclude by asking: "Do you want to adjust any section before we draft?"
```

---

### Pattern 2: The Section-by-Section Expansion Directive
Use after you approve or modify the outline:

```markdown
The outline is approved.

Now, draft **Section 1 and Section 2 ONLY**:
- Maintain an authoritative, conversational tone.
- Include concrete examples and code/data blocks where specified.
- Stop at the end of Section 2 so I can review tone before you continue.
```

---

## Real-World Case Study

### Scenario: Writing an Architecture Guide on Event-Driven Microservices

#### The 1-Shot Writing Failure
> **Prompt**: *"Write a 2,000-word guide on event-driven architecture."*
> ❌ *Result: A rambling, repetitive essay that mentions Kafka 40 times, repeats the definition of pub/sub in 3 different sections, and skips critical dead-letter queue (DLQ) failure handling.*

#### The Outline Gate Success
> **AI Outline Generated**:
> 1. **The Distributed Monolith Trap**: Why REST API chains fail under load.
> 2. **Core Pub/Sub Mechanics**: Producers, Brokers, Consumers, and Topic Partitioning.
> 3. **The 3 Golden Rules of Event Design**: Immutability, Schema Evolution (Protobuf/Avro), and Idempotent Consumers.
> 4. **Handling Partial Failures**: Dead Letter Queues (DLQ) and Exponential Backoff Retries.
> 5. **Migration Blueprint**: From synchronous HTTP calls to asynchronous messaging in 4 steps.

**Human Edit**: *"Add a section on Outbox Pattern between 3 and 4, then proceed with Section 1."*

**Outcome**: The resulting guide was rigorous, structured logically, and required zero rewriting.

---

## Summary Rules
- **Never skip the outline gate for content $> 500$ words**: It is 10x faster to delete an outline bullet than to rewrite a 400-word generated paragraph.
- **Lock the headings first**: Once headings are locked, generation tokens are channeled with maximum depth into each subtopic.
