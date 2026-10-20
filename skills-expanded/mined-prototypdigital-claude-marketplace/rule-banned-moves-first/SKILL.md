---
name: banned-moves-first
description: Keep a concrete banned-moves list and apply it to every UI build; closing off easy defaults forces something more intentional out.
---

# Banned moves first

Telling the model what *not* to do is the fastest way out of stock output. The moment the easy defaults are closed off, something more interesting has to come out. Keep a banned-moves list for the project and treat it as a hard constraint, not a suggestion.

## Patterns

- Maintain a banned-moves list of 10–15 specific items covering shapes, color moves, type behaviors, interaction clichés, and generic copy.
- Be concrete. Not "no generic icons" but "no rounded-square icons in pastel boxes." Vague bans do nothing.
- Re-state the relevant banned moves in every build or refinement prompt — they fade from context as a conversation grows.
- When reviewing generated UI, check it against the list explicitly before accepting it.

## Examples

```text
// BAD — vague ban; the model can satisfy it and still ship stock UI
"Don't make it look generic."

// GOOD — concrete banned-moves list, restated in the build prompt
Banned moves (restate every build):
- No rounded corners on cards; no drop shadows.
- No blue as the primary accent.
- No full-width hero with centered headline + subhead + two buttons.
- No pill-shaped filled filters.
- Copy: no "Oops!", no "seamless", no exclamation marks.
```

## Why it matters

A vague ban ("nothing generic") is unverifiable and the model routes around it. A concrete list is checkable on review — drop it and the easy defaults creep back in build by build.
