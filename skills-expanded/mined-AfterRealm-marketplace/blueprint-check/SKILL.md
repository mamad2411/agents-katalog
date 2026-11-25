---
name: blueprint-check
description: Analyze pasted Blueprint data for bugs and anti-patterns. Use when the user pastes Blueprint nodes or T3D text and wants a review.
allowed-tools: [Read, Glob, Grep, Bash]
---

# Blueprint Check

The user has pasted or provided Blueprint data (T3D export text, node descriptions, or copied Blueprint nodes). Analyze it for bugs, anti-patterns, and correctness.

## Before Starting

Read the knowledge base:
1. **Always read:** `${CLAUDE_SKILL_DIR}/../../data/patterns/ue5-universal-patterns.md` — all known bug patterns
2. **Always read:** `${CLAUDE_SKILL_DIR}/../../data/language-rules.md` — how to communicate about Blueprints

## Analysis Steps

### 1. Parse What Was Provided

Identify:
- Which Blueprint / function this belongs to
- All nodes present (list them with friendly names)
- The execution flow (trace the white arrow wires)
- Data connections (trace the colored wires)
- Variables referenced (Get / Set)
- Default/literal values on pins

### 2. Summarize in Plain English

Explain what the Blueprint is doing like you're describing it to someone who's never coded:
- "This function fires when the player interacts with the object..."
- "It loops through all the materials and sets each one to..."

### 3. Run Pattern Detection

Check against EVERY pattern in the knowledge base (P-001 through P-025). For each:
- Does this Blueprint contain the trigger condition?
- If yes, is it a real bug or a false positive? Explain WHY.

### 4. Run Graph Health Checks

- **Dead-end exec paths:** Does every execution branch reach a meaningful endpoint?
- **Orphaned nodes:** Any nodes with no connections at all?
- **Missing IsValid checks:** After Casts, GetComponentsByClass, or Array Gets?
- **Unguarded array access:** Array Get without Length check?

### 5. Report

**If clean:** Say so clearly. "This looks correct."
**If issues found:** For each issue:
1. Name the pattern (e.g., "P-001: BreakStruct Copy Bug")
2. Explain in plain English what's wrong and what the player would see
3. Give the exact fix using language rules (pin colors, sides, node names)

Be encouraging. Acknowledge what's correct before pointing out issues.

## Response Format

```
## What This Does
[Plain English summary]

## Verdict: [Clean / Has Issues / Needs Review]

## Issues Found
### Issue 1: [Pattern ID] — [Short Name]
**What's wrong:** [Plain English]
**Where:** [Exact node and pin references]
**Fix:** [Step-by-step using language rules]

## What Looks Good
[List things that are correctly done — positive reinforcement matters]
```
