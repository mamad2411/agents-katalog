---
name: use-good-answers-as-templates
description: "Use an approved response as a structural example for a new task while replacing its facts and context."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["few-shot-templates", "self-exemplar", "cloning", "formatting-consistency", "documentation", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Use Past Winning Answers as Templates (The Self-Exemplar Clone) (AI Skill)

## Overview
Attempting to describe a complex formatting structure in descriptive prose (*"Make it have a bold header, then a 3-column table, then two bullet points with emojis, and a code block at the bottom..."*) is tedious and leaves room for model hallucination.

The **Self-Exemplar Clone Protocol** leverages the fundamental superpower of Large Language Models: **in-context pattern completion**. By pasting a past response that you loved and telling the AI to *"replicate this exact schema for Topic B"*, you achieve 100% structural fidelity on Turn 1.

---

## Descriptive Prose vs. Self-Exemplar Cloning

```
┌─────────────────────────────────────────────────────────────┐
│                 Format Consistency Mechanics                │
│                                                             │
│  Descriptive Prose Specification (High Variance):           │
│  "Write a feature doc like the one you did yesterday with   │
│   a title, bullet points, parameters, and a code block."    │
│  ↳ Inconsistent header sizes, omitted parameter types       │
│                                                             │
│  Self-Exemplar Pattern Injection (Zero Variance):           │
│  <exemplar_format> [PASTE EXACT PAST WINNING POST] </exemplar>│
│  "Generate the entry for [NEW TOPIC] following this schema."│
│  ↳ 100% Identical Visual Hierarchy, Tone, & Depth           │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Self-Exemplar Prompt Templates

### Pattern 1: The Exact Structural Clone Directive
Use when standardizing documentation, case studies, or employee reviews:

```markdown
I want to write an entry for: **[NEW TOPIC / FEATURE NAME]**.

Below is a gold-standard reference example that I approved earlier. 
Follow its **exact visual layout, heading hierarchy, tone, and depth**:

<exemplar_format>
[PASTE YOUR FAVORITE PAST RESPONSE HERE]
</exemplar_format>

Input Data for [NEW TOPIC]:
[PASTE RAW NOTES / DATA FOR THE NEW ITEM]

Output the new entry strictly matching the exemplar structure.
```

---

## Real-World Case Study

### Scenario: Writing API Documentation for 10 Microservices

#### The Problem
Writing prose instructions for each API doc resulted in service A having a Markdown table, service B having a bulleted list, and service C omitting error codes entirely.

#### The Self-Exemplar Fix
The team took the perfectly formatted doc for the `UserService` and used it as an exemplar template:

```markdown
Generate the API documentation for `PaymentService`:

<exemplar_format>
### `POST /v1/users`
**Description**: Creates a new user profile and triggers welcome email.

#### Request Headers
| Header | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `Authorization` | Bearer Token | Yes | Scoped OAuth2 token |

#### Example Payload (JSON)
```json
{ "email": "user@example.com", "name": "Jane" }
```
</exemplar_format>

Raw details for `PaymentService`: Endpoint `POST /v1/charges`, requires `Authorization` and `Idempotency-Key`, payload takes `amount` in cents and `currency`.
```

**Outcome**: AI produced a clone of the `PaymentService` documentation with identical tables, formatting, and JSON fences in under 5 seconds.

---

## Summary Best Practices
- **Store winning outputs**: Save 2 or 3 of your all-time favorite AI responses into an `exemplars.md` file for reuse.
- **Enclose in `<exemplar>` tags**: Cleanly isolates the reference pattern from the new prompt data.
