---
name: grimoire-clarify
description: Round-based interrogation that builds a design tree to resolve every implicit assumption before action.
---

# Purpose

Question the user round by round until every decision is resolved and no hidden assumptions remain.

# Design tree

A tree of decisions. Each node is a question. Children depend on parent answers. Frontier nodes = unanswered nodes whose every ancestor is answered. These are the questions ready to ask now.

# Loop

Repeat until frontier is empty:

1. **Calculate frontier** — walk the tree. Collect every unanswered node whose ancestors are all answered. Skip nodes blocked by a pending sub-agent.

2. **Dispatch fact-checks** — for any frontier question that needs file contents, tool output, or environment data, dispatch a sub-agent now. The node remains blocked until results arrive. Do not wait. Do not ask the user for verifiable facts.

3. **Present frontier** — number every ready question. Give each a recommended answer with reasoning. List pending fact-checks separately.

4. **Collect answers** — wait for user. User accepts, overrides, or skips each question. User may also revise past answers (prune affected subtree).

5. **Reshape** — for each answered node, generate children: "Given this answer, what else must be decided?" Attach children. Check sub-agent results; unblock any that returned.

6. **Repeat** — recalculate frontier. If empty, proceed to close.

# Close

Summarize every decision path from root to leaf. Announce completion. Ask user to confirm consensus. Do nothing until confirmed.

# Rules

- Complete interrogation within 5 rounds. Prioritize high-impact decisions. Merge low-stakes questions.
- Never ask the user for something you can look up.
- Never execute the objective during interrogation.
- User has final authority on every answer.
- Sub-agent results are checked once per round (step 5).
