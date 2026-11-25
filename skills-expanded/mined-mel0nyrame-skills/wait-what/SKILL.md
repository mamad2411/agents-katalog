---
name: wait-what
description: "Stop. That last message did not land: re-pitch it."
disable-model-invocation: true
---

Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context, then explain it again using the rules below:

### 1. Core Recovery Actions

- **Acknowledge & Reset:** Briefly acknowledge the misalignment without being defensive. Do not stack more complex logic on top of the previous confusion.
- **Restore Context:** Explicitly state the missing prerequisites, where we currently are in the problem, and what assumptions are being made.
- **Match User Language:** Respond in the same language the user is currently using (e.g., Simplified Chinese, English, etc.).

### 2. Communication Principles

- **Accuracy & Clarity:** Use direct, precise, and unambiguous language. Aim for one main fact, action, or judgment per sentence. Eliminate vague filler words (e.g., "to some extent," "handle accordingly," "related stuff").
- **Explicit Logic:** Prefer clear Subject-Verb-Object structures. Explicitly state conditions, actions, and outcomes using structures like "If \[condition], then \[action/result]." Avoid ambiguous pronouns like "this" or "it"—repeat the specific noun when necessary.
- **Consistent Terminology:** Always use the exact same term for the same concept; never swap in synonyms just for stylistic variety. Provide a brief definition the first time a technical term is introduced. Preserve exact code identifiers, commands, and API names.
- **Structured Delivery:**
  - Answer the core question first before providing background details.
  - When explaining complex concepts, follow the sequence: **Definition → Mechanism/Principle → Concrete Example → Limitations/Edge Cases**.
  - Do not sacrifice necessary technical details, prerequisites, or risks just to make the response shorter. Clarity and completeness take priority over brevity.
- **Fact vs. Assumption:** Clearly distinguish between verified facts, logical inferences, assumptions, and recommendations.
