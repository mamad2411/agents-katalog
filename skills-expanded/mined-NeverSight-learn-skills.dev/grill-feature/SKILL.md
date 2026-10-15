---
name: grill-feature
description: Interview the user relentlessly about a vague product or engineering feature until goals, MVP scope, tradeoffs, and key decisions are clear. Use when the user wants feature discussion, recommendations, assumption-challenging, MVP scoping, or architecture pressure-testing before planning or implementation.
---

Interview me relentlessly about this feature idea until we reach shared understanding. Walk down each branch of the feature decision tree, resolving dependencies between decisions one by one. For each question, provide your recommended answer with tradeoffs and examples.

Ask the questions one at a time, waiting for feedback before continuing.

If a question can be answered by exploring the codebase or referenced files, explore them instead.

Bring your own judgment: suggest better product shapes, smaller MVP cuts, and alternative technical directions when useful. Push back directly when the idea is too broad, confused, premature, or inconsistent, but always pair disagreement with a concrete better option.

Treat referenced files as context by default, not write targets. Do not modify code, docs, PRDs, plans, or create files during grilling unless the user explicitly asks you to write changes back after the discussion.

Do not turn recommendations into accepted decisions. When the user accepts one recommendation, continue to the next unresolved branch instead of treating the whole design as settled.

Only produce a plan after the key decisions are settled and the user asks to move from grilling to planning.
