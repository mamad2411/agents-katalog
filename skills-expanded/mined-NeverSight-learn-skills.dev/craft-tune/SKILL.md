---
name: craft-tune
description: Improve an existing prompt or skill with targeted, minimal-diff edits that preserve its core intent, and return the revised artifact plus a short changelog and tradeoffs note. Use this whenever the user wants to refine, sharpen, tighten, or upgrade an existing prompt or skill, asks to "make it better," or wants a small high-leverage edit instead of a full rewrite — even if they don't explicitly mention tuning.
---

# craft-tune

## Purpose

Improve an existing prompt or skill with targeted edits while preserving its core intent.

Minimal-diff tuning matters because full rewrites lose hard-won context: the phrasing that a prompt accumulated over time often encodes real lessons. Tuning preserves that knowledge and changes only what is blocking the goal.

## Use this when

- a prompt is close but needs sharpening
- a skill works but feels noisy or inconsistent
- minimal-diff improvement is better than rewriting from scratch
- quality needs to improve without losing the original structure

## Inputs

- current artifact
- target improvement
- hard constraints
- optional examples or references

## Steps

1. Restate the artifact's current intent. Lock it in before changing anything — this is what you must preserve.
2. Identify the highest-leverage changes. Prefer one or two structural edits over many surface tweaks.
3. Preserve good parts unless they directly block the goal. Resist the urge to "clean up" working text.
4. Rewrite only the sections that need improvement. Leave the rest untouched so the diff is legible.
5. Produce a revised version plus a short changelog. The changelog makes the edit reviewable.
6. Note any tradeoffs introduced by the edits. Every improvement costs something; say what it costs.

## Output format

### Intent preserved
One short paragraph naming the original artifact's concrete job in task-specific terms — reference a detail a reader could use to guess what the input was about. "The original job remains intact" or "improves the existing prompt" fails the bar.

### Revised artifact
The updated prompt or skill. Every substantive change must serve the stated target improvement; no "while I'm in there" additions. When cutting content, cut in the Principle 3 order (verbose role → restated context → hedging) and preserve examples, success criteria, and output-format rules.

### Changelog
One entry per distinct change. Every entry names all three fields — not just "changed":

- **changed** — what was edited (added / removed / rewrote)
- **why** — the specific failure or gap this edit fixes
- **effect** — the behavior change a reader should expect

Use a list-of-groups per entry, or a three-column table. A bare bullet naming only the change fails the spec; bundling unrelated changes into one entry fails the spec.

### Tradeoffs
Name at least one concrete cost with a direction (length ↑, flexibility ↓, specificity ↑, adaptability ↓). "No tradeoffs" is acceptable only when paired with a one-line justification of why the edit carries no cost; vague acknowledgments ("small tradeoff in clarity") fail.

## Guardrails

- do not rewrite everything by default
- do not add complexity without payoff
- keep the result copy-pasteable
- prefer structural clarity over clever wording

## Principles

These four ideas do most of the work behind a good minimal-diff edit. When a tune feels stuck, check that the edit respects all four.

1. **Context beats instruction.** When token budget is tight, richer background usually helps more than more rules. A simple instruction with strong context outperforms elaborate instructions with none.
2. **Outcome over process.** Say what success looks like, not every step to get there. Modern agents are good at means; they need clarity on ends.
3. **Cut in this order.** When the artifact is too long, cut verbose role definitions first, then restated context, then hedging language. Do not cut examples, success criteria, or output-format specs — those change behavior the most.
4. **Right-sized beats thorough-looking.** A 50-token instruction for a simple task is a feature, not a defect. Do not inflate to look rigorous.

## Failure modes

- silently drifting the artifact's scope during "cleanup"
- adding length to look thorough when the original was already tight
- piling on ALWAYS/NEVER rules instead of explaining the underlying reason
- producing a diff so large it's effectively a rewrite without admitting it

## Example

### Input
Current prompt:

> Improve this prompt.

Target improvement: make it more reusable for coding agents.

### Output

**Intent preserved**
The original job is to improve an existing prompt.

**Revised artifact**

> Improve the prompt below for reuse by coding agents. Preserve the original intent. Return: 1) revised prompt, 2) key changes, 3) likely failure modes.

**Changelog**
- added target audience
- added preservation constraint
- added explicit output structure

**Tradeoffs**
- slightly longer prompt
- much higher consistency
