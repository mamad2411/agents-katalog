---
name: ps-help
description: Answer "how do I…" and "what is…" questions about Process Street, grounded in the official help docs and bundled best-practices. Use when the user asks how Process Street works, how to do something in it, or for guidance/best practices.
---

# Answer Process Street questions (help docs + best practices)

Answer the user's Process Street question accurately, grounded in real sources — not guesses.

## Sourcing order

1. **Bundled knowledge first** — check `reference/best-practices.md` (design guidance) and `reference/api-reference.md` (what the API can/can't do). These are authoritative for "should I…" and "can the API…" questions.
2. **Live help docs** — for product/how-to questions ("how do I add a member field", "how do approvals work", "what plan includes X"), fetch the official help center. Use a web fetch on:
   - `https://www.process.st/help/` (help home / search)
   - Specific articles under `https://www.process.st/help/docs/...` when you know or can find the slug (e.g. `code-task`, `ai-task`, `conditional-logic`, `approvals`, `data-sets`, `webhooks`).
   If a fetch fails or web access is unavailable, say so and answer from bundled knowledge, clearly labeling what's general guidance vs. confirmed from docs.

## How to answer

- Give the **direct answer first**, then a short "how" (steps or the relevant CLI command if it's something this toolkit can do).
- **Cite the source**: link the specific help article you used, or say "from the bundled best-practices guide."
- If the question is really a "do it for me" (build/edit/audit/organize), answer briefly then offer to run the matching skill (`ps-build`, `ps-edit`, `ps-audit`, `ps-organize`).
- Be honest about **limits**: required-field flag, brand theming (colors/cover/fonts), org/SSO, and deep native-integration config are UI-only, not API-driven.
- Don't invent features, plan names, pricing, or limits. If you can't confirm something, say what you'd check and offer to fetch it.

## Examples

- *"How do I make a field required?"* → It's set in the workflow editor UI (toggle on the field); the public API can't set it. (api-reference.md)
- *"What's the best way to structure an onboarding workflow?"* → Summarize from best-practices.md (front-load capture, conditional sections, approval gate, dynamic due dates), then offer `ps-build`.
- *"How do Code tasks work?"* → Fetch `https://www.process.st/help/docs/code-task/`, explain `inputData`/`outputData`, and note this toolkit can build one via `ps-build`.
