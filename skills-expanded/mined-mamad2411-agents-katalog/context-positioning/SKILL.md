---
name: context-positioning
description: Place load-bearing content at the edges of the context, not the middle — models access the start and end far better than the middle.
---

# Context positioning

Where information sits in the context window changes how reliably the model uses it. Accuracy follows a **U-shaped curve**: it is highest when the relevant content is at the very beginning or the very end of the input, and degrades significantly when the model must pull it from the middle — even for models marketed as long-context.

The effect is large. On multi-document QA, accuracy can drop by **more than 20 points** purely from moving the relevant document to the middle, and in 20- and 30-document settings, mid-context performance falls *below* the closed-book baseline (56.1%) — i.e. adding the documents made the model worse than giving it none.

## Rules

- Put the most load-bearing content — the actual task, the key document, the constraint that must not be missed — at the **start or end** of the context, never buried in the middle of a long block.
- Place long-form data (documents, transcripts, large inputs) **near the top** of the prompt, above the query and instructions. Put the actual question or instruction **at the end**, after the data.
- Do not assume more retrieved tokens monotonically help. Past a point, extra documents stop improving answers and start pushing relevant content into the low-recall middle.
- When you must include many retrieved chunks, **rerank** so the most relevant ones land at the edges, or **truncate** the list rather than padding the middle.
- Treat a large long-context window as more room to *lose* things in the middle, not a reason to stop curating position.

## Examples

```text
// BAD — instruction buried in the middle; likely to be missed
[document A — 500 tokens]
[document B — 500 tokens]
"Summarize the key risks."        ← middle of context
[document C — 500 tokens]
[document D — 500 tokens]

// GOOD — long-form data first, query at the end
[document A — 500 tokens]
[document B — 500 tokens]
[document C — 500 tokens]
[document D — 500 tokens]
"Summarize the key risks."        ← end of context
```

## Source

Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," *TACL* 2024 — <https://aclanthology.org/2024.tacl-1.9/> (arXiv:2307.03172). The U-shaped curve, the >20-point positional drop, and the sub-closed-book (56.1%) result are from the paper. Anthropic's prompt-engineering docs give the same "long-form data at top, query at the end" guidance; note their "up to 30% improvement" figure is a vendor self-report, not from the peer-reviewed paper, so don't cite it as an independent fact.
