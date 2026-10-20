---
name: ask-repo-question
description: Answer repository questions without editing files. Use when the user asks how the codebase works, where behavior lives, what a change would affect, or wants explanation only.
---

# Ask Repo Question

## Use When

- The user asks how the codebase works.
- The user asks where behavior lives.
- The user asks what a change would affect.
- The user asks for explanation only.
- The user asks a general repo question before deciding whether to change code.

## Workflow

1. Read `AGENTS.md` when project guardrails matter.
2. Use `.ai/context-routing.md` when the question needs repo navigation.
3. Pick the smallest relevant map from `.ai/maps/` when helpful.
4. Use `.ai/index`, `rg`, Graphify, Aider repo maps, or Understand Anything to locate likely files.
5. Read exact files before making factual claims.
6. Answer directly with file references when useful.

## Boundaries

- Never edit files.
- Never stage, commit, push, or run destructive commands.
- Prefer exact files over generated summaries.
- Treat generated maps, graphs, embeddings, and repo maps as navigation only.
- Say when evidence is missing.
- Do not speculate when exact files can answer the question.

## Output

- Direct answer.
- Files/docs inspected.
- Evidence or references from source files where useful.
- Uncertainties or missing evidence.
- Suggested next inspection or next action only when useful.
