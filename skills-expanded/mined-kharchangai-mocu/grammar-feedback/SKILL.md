---
name: grammar-feedback
description: Detect grammar mistakes in user-written text, explain them simply in English, and provide a few clear examples. Use when reviewing or correcting grammar in user-written text.
---

# Grammar Feedback

When the user shares text and wants help with grammar:

1. Check the grammar carefully and preserve the user's intended meaning. Do not label acceptable, colloquial, or dialectal usage as wrong.
2. If there is a genuine grammar mistake, show the exact original phrase and a corrected version.
3. Explain the rule simply and briefly in English.
4. Give 2–3 short, natural examples that demonstrate the same rule. Prefer a memorable contrast or reusable pattern, not textbook-heavy prose.
5. Focus on the most useful grammar point; do not correct unrelated style choices or typos as grammar.
6. If the text is grammatically correct, say so plainly. Do not invent an error; an optional natural alternative must be clearly labeled optional.
7. If intended meaning is unclear and affects the correction, ask one brief clarifying question instead of guessing.
8. For each genuine grammar issue, include a structured `grammarIssue` object with exactly these string fields: `id`, `rule`, `original`, `correction`, `explanation`. Use a short, stable kebab-case `id` for the grammar pattern and reuse it for the same pattern later. Keep the explanation consistent with the feedback; return `grammarIssue: null` when there is no genuine error. Do not claim to store progress or decide mastery; the tutor extension tracks practice and mastery.
9. When helping a conversational tutor, invite the learner to use the corrected pattern in their next natural reply, without giving away the answer. Count success only when the learner independently uses the target form correctly in a clear practice response. Keep the examples memorable, natural, and tied to everyday contexts.

Keep the tone friendly, encouraging, and suitable for a learner. Unless the calling agent specifies a different output schema, a simple response format is:

- **Correction:** …
- **Why:** …
- **Examples:** …
- **grammarIssue:** `{ "id": "...", "rule": "...", "original": "...", "correction": "...", "explanation": "..." }` (or `null` when correct).