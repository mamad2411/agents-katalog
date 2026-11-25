---
name: concept-glossary
description: "Names the concept whenever the user describes something that has an established term — in engineering, design, marketing, product, psychology, business, or everyday life — then silently logs it to a running GLOSSARY.md with a plain-English definition and the real context it came up in. Use continuously; also use when the user asks what they've learned, wants to search the glossary, or wants it exported."
---

# Concept Glossary — Name It, Then Log It

Most people can describe a concept long before they know its name. Handing them the name converts a fuzzy paragraph into a single word they can recall, search, and say out loud to a colleague.

## When to Activate

**Always on.** Trigger on the *description*, not the vocabulary — the user is explaining a thing without knowing the word for it.

Also activate on: *"what have I learned"*, *"what's that term for…"*, *"show my glossary"*, *"quiz me"*, or any export/publish request.

## The Move

One short line, then continue the work:

> "What you're describing is called **[term]** — [one-line plain-English definition]."

Then keep going. This is an aside, not a detour.

### Examples

> **User:** "I want the button to feel like it's pushing back when you tap it."
> **You:** That's **haptic affordance** — a physical cue confirming the interface registered your input. Adding it now…

> **User:** "Why does the second one feel cheaper at the same price?"
> **You:** **Anchoring** — the first number your brain sees becomes the ruler for everything after.

> **User:** "It's slow because we ask the database once per row instead of all at once."
> **You:** That's the **N+1 query problem**. Batching it now.

## Rules

1. **Name it once, briefly.** No history lesson unless asked.
2. **Only real, established terms.** Never invent a label to seem clever. If no genuine term exists, say so plainly — a confidently-used fake term will embarrass the user in front of an expert.
3. **Never interrupt the task.** One line, then back to work.
4. **Skip it when they clearly already know the term.**
5. **Correct gently.** If they're using a term slightly wrong, note the distinction in a few words.
6. **Most-used term wins.** If several fit, give the common one; mention a cousin only if genuinely useful.

## Logging

Every named term is appended to `GLOSSARY.md` — **silently**. Never announce the logging; the one-line aside is the entire visible footprint.

### Entry format

```markdown
### <Term>
**Field:** <Engineering | Design | Marketing | Product | Psychology | Business | Finance | Film/Video | General>
**Definition:** <one plain-English sentence — no jargon defining jargon>
**Came up when:** <the real thing they were doing, in their words where possible>
**Date:** YYYY-MM-DD
```

### Logging rules

1. **Append-only.** Never rewrite or delete past entries — the history is the value.
2. **No duplicates.** Grep first. If the term exists but the new context is richer, append a second `**Came up when:**` line to the existing entry.
3. **Plain-English definitions.** If the definition needs its own glossary lookup, rewrite it. Test: would it make sense read aloud to someone outside the field?
4. **`Came up when` is mandatory and specific.** "While pricing the upgrade screen" — not "discussing pricing." Context is the memory hook; a term with no anchor is a flashcard nobody recalls.
5. **Correct, don't delete.** If a logged term turns out to be misapplied, strike it with a short note. Seeing the mistake is worth more than a clean file.

## Retrieval

| Ask | Do |
|---|---|
| "What have I learned?" | Summarize by field, newest first, with counts |
| "What was that term about X?" | Grep definition + context, return the entry |
| "Show my glossary" | Render the file, grouped and readable |
| "Quiz me" | Show `Came up when` + `Definition`, hide the term, ask them to name it |

## Export & Publish

Portable by design — plain Markdown.

**Publishing is outward-facing. Confirm scope before the first push.** Once a destination is approved, routine updates there don't need re-confirmation; a *new* destination always does.

**Sanitize before any public push.** Terms and definitions are generic, but `Came up when` lines may name real clients, unreleased products, or internal numbers. Genericize them — "while building a courier dispatch flow", not the client's name. Keep the full detail in the local copy.
