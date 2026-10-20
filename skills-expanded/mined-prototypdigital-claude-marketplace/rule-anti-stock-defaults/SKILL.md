---
name: anti-stock-defaults
description: Decide the visual direction before prompting; AI averages toward stock UI, so name what you want and refuse the safe default.
---

# Anti-stock defaults

Vague prompts make the model average across everything it has seen — rounded corners, a neutral palette, system fonts, a subtle gradient. The output is fine. It is also instantly forgettable. The fix is not a better tool: decide what you want before you ask, and say no when the result plays it safe.

## Patterns

- Set the visual direction *before* generating UI. Never ask for "a clean, modern component" and accept the first result.
- When output looks generic, treat it as drift to correct — not a neutral baseline to refine.
- Prefer one opinionated choice over five tasteful, interchangeable ones.
- The designer directs; the AI builds. Specific direction in, distinctive work out.

## Examples

```text
// BAD — vague prompt; model will produce a forgettable default
"Build a clean, modern hero section for a SaaS product."
→ Result: rounded card, neutral blue, Inter font, subtle gradient

// GOOD — specific direction set before generating
"Build a hero section in the spirit of early Experimental Jetset — dense grid,
 black and white only, grotesque type at large size, no decoration.
 NOT: gradients, rounded corners, or stock photography."
→ Result: constrained output with a defined point of view
```

## Why it matters

"Helpful" defaults are the average of everything the model has seen. Distinctiveness comes from constraint, not from asking nicely. Every other rule in this pack is a way of applying that constraint.
