---
name: ask
description: Answers a question from the vault — what is due, what do I know about X, what did I write about Y, who is Z — index first, a few nodes at most; read-only. Use for questions like "چی کارها دارم", "در مورد … چی نوشتم", "کی باید …", "what's on my plate", "what do I know about", "when did I".
---

# ask

Read-only: never create or edit nodes while answering.

## Steps

1. Read `index/INDEX.md`. Today's tasks, overdue items, active projects and inbox are answered from it alone. The runtime context's **Scope** line, when present, says which maps are in reach; a map outside it does not exist for this answer.
2. Narrow: open the relevant `index/by-type/<type>.md`, or `Grep -i "<term>" nodes/` for candidate files.
3. Open at most the 5 most relevant nodes. State facts from the files; say when something is not in the vault.
4. Answer in the user's language, short, with `[[Title]]` references so the app can link them. If nothing matches, say so and offer to capture it.

Question-type strategies: [references/strategies.md](references/strategies.md).
