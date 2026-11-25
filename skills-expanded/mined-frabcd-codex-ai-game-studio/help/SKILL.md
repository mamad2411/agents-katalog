---
name: help
description: "Analyzes what is done and the users query and offers advice on what to do next. Use if user says what should I do next or what do I do now or I'm stuck or I don't know what to do"
---

> Port provenance: adapted from the pinned upstream source at `984023ddac0d5e27624f2baacde6105e45de375f` under MIT; see the repository parity ledger for the exact path and blob.

# Contextual workflow navigator

Inspect the project read-only, infer its current stage from evidence, and show a
compact menu containing only useful next actions. Do not run those actions.

## Navigation method

1. Inspect project files, current branch state, engine markers, design and
   architecture documents, sprint artifacts, recent test evidence, generated
   assets, and `.ai-game-studio/project.json` when present.
2. State the detected stage and confidence. If evidence conflicts, explain the
   conflict in one sentence and ask a focused question.
3. Recommend one primary next skill and no more than three alternatives.
4. For every recommendation, include a copy-ready prompt beginning with the
   exact namespaced invocation `$ai-game-studio:<skill>`.
5. Mark workflows that require a plan and explicit confirmation before mutation.

## Common paths

- New concept: `$ai-game-studio:brainstorm` -> `$ai-game-studio:prototype` ->
  `$ai-game-studio:art-bible` -> `$ai-game-studio:map-systems`.
- Existing project: `$ai-game-studio:adopt` ->
  `$ai-game-studio:project-stage-detect` -> relevant audit or planning skill.
- Playable prototype: `$ai-game-studio:prompt-to-game`, followed by
  `$ai-game-studio:playtest-report` and `$ai-game-studio:scope-check`.
- Production assets: use the relevant generation skill, then
  `$ai-game-studio:visual-qa`; use `$ai-game-studio:quality-enhance` only for an
  approved, reversible improvement.
- Editor tooling: `$ai-game-studio:toolchain-doctor` ->
  `$ai-game-studio:setup-engine` -> `$ai-game-studio:engine-automation`.
- Release: `$ai-game-studio:smoke-check` ->
  `$ai-game-studio:regression-suite` -> `$ai-game-studio:release-checklist`.

Distinguish product controls from skills: `/plugins` browses or installs plugins;
the `/` picker lists enabled skills; `$ai-game-studio:<skill>` invokes a workflow.
Never invent deprecated custom slash aliases.

## Codex portability

Use the search, file-editing, shell, user-input, and subagent capabilities available in the active Codex surface. Use PowerShell syntax on Windows and POSIX syntax on macOS/Linux; do not require a Unix compatibility layer on Windows. Inherit the active model and permission mode, and do not weaken approval or sandbox boundaries.
