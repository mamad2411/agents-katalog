---
name: instruction-architect
description: "Use when designing elite, production-grade system instructions for AI agents, assistants, and GPTs. Sets the gold standard for AI system instruction design with structured methodologies."
version: "1.0"
tags:
  - system-instructions
  - prompt-engineering
  - ai-agents
  - gpt
  - production-grade
---

# Instruction Architect

## Overview

Production-grade system instruction design for AI agents, assistants, and GPTs. A structured methodology that produces reliable, testable, and maintainable system prompts — not ad-hoc prompt writing. Applies software engineering rigor to the craft of instruction design.

## When to Use

- Building a new AI agent or assistant from scratch
- Auditing and hardening existing system instructions
- Scaling a single-use prompt into a reusable, production system prompt
- Designing instructions that must work reliably across thousands of conversations
- When precision, safety, and consistency are non-negotiable (enterprise, compliance, customer-facing)

## How It Works

The **A.R.C.H.I.T.E.C.T.** methodology:

1. **A**udience & Purpose — Who uses this and why?
2. **R**ole Definition — Precise persona and scope boundaries
3. **C**onstraints & Guardrails — Hard rules, soft rules, escalation paths
4. **H**euristics & Decision Trees — How to handle ambiguous situations
5. **I**nput/Output Spec — Explicit formats, schemas, and examples
6. **T**esting Protocol — Systematic validation methodology
7. **E**rror Recovery — Graceful degradation and fallback behaviors
8. **C**ontinuous Refinement — Feedback loops and version management
9. **T**ool Integration — How the instructions interact with tools/actions/functions

## Steps

### Step 1: Audience & Purpose Discovery
Document these before writing a single instruction line:
- Primary user persona (role, skill level, expectations)
- Core use cases (top 5 things users will ask)
- Success metrics (how do we know the instructions work?)
- Failure modes (what must never happen?)

### Step 2: Role Definition
Write a precise role statement. Avoid vague descriptors:
- ❌ "You are a helpful assistant"
- ✅ "You are a senior DevOps engineer specializing in AWS infrastructure. You provide infrastructure-as-code solutions using Terraform and CDK. You prioritize security, cost-efficiency, and maintainability."

### Step 3: Constraint Layering
Layer constraints from hardest to softest:
1. **Hard gates** (NEVER do X — safety, legal, ethical)
2. **Always rules** (ALWAYS do Y — mandatory behaviors)
3. **Default behaviors** (When unsure, do Z)
4. **Style preferences** (Prefer approach A over B)

### Step 4: Decision Heuristics
For ambiguous situations, provide explicit decision trees:
```
If user asks for [X]:
  If [X] is in knowledge base → answer directly
  If [X] requires live data → use web browsing
  If [X] is out of scope → politely redirect with alternatives
  If [X] is unsafe → refuse with explanation
```

### Step 5: I/O Specification
Define exact output formats for common response types:
```yaml
code_review:
  format: |
    ## Summary
    [one paragraph]
    ## Issues Found
    - [severity] [file:line] [description] [fix]
    ## Recommendations
    - [recommendation]
analysis:
  format: |
    ## Key Finding
    [finding]
    ## Supporting Evidence
    - [point]
    ## Action Items
    - [item]
```

### Step 6: Testing Protocol
Build a test suite covering:
- **Functional tests**: Does it do the job for each core use case?
- **Guardrail tests**: Does it refuse unsafe requests?
- **Edge case tests**: Empty input, extremely long input, non-English, adversarial prompts
- **Persona drift tests**: Does it stay in character across 20+ turn conversations?
- **Tool-use tests**: Does it call tools correctly and handle tool failures?

### Step 7: Error Recovery Patterns
Define fallback for every failure mode:
- Tool unavailable → "I can't access [tool] right now. Here's what I can do instead: [...]"
- Ambiguous input → "To give you the best answer, could you clarify: [specific question]?"
- Out of scope → "That's outside my area. I can help with [related alternative] instead."
- System failure → "Something went wrong. Let me try a different approach: [...]"

### Step 8: Version Management
- Version your instructions (v1.0, v1.1, etc.)
- Maintain a changelog of what changed and why
- Tag versions with test results
- Archive, don't delete — old versions reveal what didn't work

### Step 9: Tool Integration Design
For systems with tool/function calling:
- Define when to use each tool (not just how)
- Specify tool call ordering rules
- Define tool output handling (validation, error parsing, retry logic)
- Add tool-specific guardrails (max calls per turn, rate limiting)

## Common Pitfalls

- **Kitchen-sink instructions**: Including every edge case bloats the prompt and degrades core performance. Keep core instructions tight; use knowledge files for reference material.
- **No failure mode design**: Most instructions only describe the happy path. Define what happens when things go wrong.
- **Persona mismatch**: The tone in system instructions doesn't match the actual use case (e.g., casual tone for enterprise compliance use).
- **Testing only your own prompts**: You're blind to your own instructions' ambiguities. Have others test without coaching.
- **Version neglect**: Untracked edits lead to "it worked yesterday, now it doesn't" with no way to diff.

## Source

Original methodology based on production experience across hundreds of GPT and agent deployments. Gold standard for AI system instruction design.
