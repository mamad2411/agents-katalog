---
name: improving-prompts
argument-hint: "<prompt text or file path containing the prompt to improve>"
description: Compresses and clarifies an existing LLM prompt through concept elevation, verifying that no original instruction is lost. Use when the user supplies a prompt or prompt file and asks to improve, tighten, optimize, or refine it. Not for writing a new prompt; use writing-system-prompts.
---

# Improve Prompt Using Concept Elevation

Concept elevation finds the higher-level rule that expresses the sum of
several connected instructions. The result is shorter and lets the model adapt
to new situations instead of relying on specific cases.

The argument is prompt text or a path to a file containing it. Print the
improved prompt by default. Edit the file in place only when the user asks.

## Process

1. Number every instruction, constraint, and example in the original (I1, I2,
   ...). This is the intent inventory.
2. Group items that serve one purpose, and replace each group with the single
   rule that captures all of it. Keep an item as written when no rule captures
   it without loss.
3. Map every inventory item to the draft line that carries its intent. Restore
   each unmapped item, then map again, until every item maps. The draft must be
   shorter than the original and leave no case unaddressed that the original
   covered.

Never drop an item silently. When two items conflict or one looks obsolete, keep
both in the draft and flag the conflict.

## Deliverable

End with this format (adapt the list labels; keep the order):

````markdown
```text
<the improved prompt>
```

- Merged: I1, I4, I7 -> <the rule that replaces them, abbreviated>
- Kept as written: I3 (<why no rule captured it>)
- Flagged: I9 conflicts with I2 (<the decision the user must make>)
````
