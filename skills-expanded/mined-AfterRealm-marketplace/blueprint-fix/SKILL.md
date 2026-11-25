---
name: blueprint-fix
description: Generate step-by-step fix instructions for Blueprint bugs found during audit. Use when the user wants to fix specific issues.
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

# Blueprint Fix

Generate detailed, beginner-friendly fix instructions for Blueprint bugs. Every fix must be wirable by someone who has never coded before.

## Before Starting

Read the knowledge base:
1. `${CLAUDE_SKILL_DIR}/../../data/patterns/ue5-universal-patterns.md`
2. `${CLAUDE_SKILL_DIR}/../../data/language-rules.md`

## Input

The user will reference either:
- A specific bug from a previous audit ("fix Bug 1 in MyFunction")
- A general request ("fix the BreakStruct issue in SaveState")
- A function name ("fix MyFunction" — find and fix all bugs)

## Steps

### 1. Understand the Bug

Read the relevant export data. Identify:
- Which pattern this matches
- The exact nodes and wires involved
- What the bug causes from the user's perspective

### 2. Plan the Fix

For each bug:
- What nodes need to be added?
- What wires need to be moved or added?
- What existing connections need to be broken?
- Will the fix affect other functions?

### 3. Write the Instructions

Follow the language rules STRICTLY. Each step must include:

1. **What to do** — place a node, connect a wire, set a value
2. **Exact search term** — what to type in the right-click search
3. **Pin colors and sides** — "the green output pin on the right side"
4. **What it connects to** — reference only nodes from previous steps

### 4. Self-Validate

For each fix step, verify:
- Does the referenced node exist (or was it placed in a prior step)?
- Are the pin names and colors correct?
- Does the execution flow remain intact?
- Could this fix introduce new bugs?

## Response Format

```
=== FIX: [FunctionName] ===

BUGS FOUND: [count]
DIFFICULTY: [Easy / Medium / Hard]

--- Bug [N]: [Pattern ID] — [Short Name] ---

WHAT'S WRONG (plain English):
  [2-3 sentences from the player/user perspective]

WHY THIS HAPPENS:
  [Simple analogy — e.g., "Like editing a photocopy instead of the original"]

FIX STEPS:

1. Right-click in an empty area and search **[NodeName]**. Place it near [reference node].

2. Drag a wire from the **[color] [pin name]** pin on the **right side** of **[SourceNode]** to the **[color] [pin name]** pin on the **left side** of **[TargetNode]**.

[...continue with all steps...]

BEFORE → AFTER:
  Before: Entry → OldNode → Return
  After:  Entry → OldNode → NewNode → Return
```

Be encouraging. Blueprint debugging is hard and the user is learning.
