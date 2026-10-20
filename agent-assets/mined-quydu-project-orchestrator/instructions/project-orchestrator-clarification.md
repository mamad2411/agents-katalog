---
applyTo: "**"
description: Mandatory clarification protocol applied to every user prompt before any work begins.
---

# Clarification Protocol

This protocol has the highest precedence in this repository. It applies to every new user prompt, in every file, for every task type.

## Required sequence

1. Invoke `clarify-the-ask` before any analysis, tool use, file change, command, or answer.
2. Ask one question round only: ask **three** questions for an ordinary request, and up to **five** only when the request is complex, confusing, high-impact, or potentially damaging to the current project.
3. Stop and wait for the user's answers. Do not start work while a question is unanswered.
4. After the answers arrive, do not ask any more clarification questions for this prompt. Describe what will be done:
   - the objective in the user's terms,
   - the concrete steps,
   - the files, services, or systems that will be touched,
   - the risks, side effects, and any irreversible action.
5. Continue after the answers unless a separate approval gate applies. Approval gates are not clarification questions.

## Rules

- Run this **once** for every new prompt, including short follow-ups in an established session. The next prompt may start a new round.
- Inspect the repository first so all three questions resolve real decisions. Do not ask for information the repository already contains; ask about intent, scope, constraints, priorities, and acceptance criteria.
- Order questions by decision impact. Offer a recommended default when one is defensible.
- Never treat the plan description as approval. Approval is an explicit user response.
- Do not ask filler questions. Use four or five only when extra decisions are genuinely material. Unresolved material ambiguity still blocks.
- Never request passwords, tokens, keys, or other secrets through clarification.

## Only exception

The current prompt explicitly instructs you to skip clarification, including the exact
`--proceed` or `--Proceed` token. Treat the token case-insensitively. A prior prompt's instruction does not carry forward. This token never
overrides approval gates or authorizes destructive, external, privileged, irreversible, commit, or
push actions.

## Recording

Write the resolved understanding to `reports/clarification-result.json` through `clarify-the-ask`, then hand off to `workflow-planner`.
