---
name: implement-from-plan
description: "Implement an approved plan doc step-by-step in application or systems codebases, including Node/TS, Python, and C/C++ repos (build/lint/test per step, atomic commits, progress log hygiene). Use when you have a plan/*.md and want to execute it."
---

# Implement From Plan (step-by-step)

Input: a plan doc path (for example: `plan/my-feature.md`).

## Preconditions (stop if missing)

1. Confirm you are in the intended repo: `git rev-parse --show-toplevel`
2. Confirm the plan doc exists: `test -f <plan-doc-path>`
3. Confirm the working tree is clean: `git status --porcelain` is empty
4. Ensure `codex-progress.log` is gitignored and not tracked:
   - Add `codex-progress.log` to `.gitignore` if missing.
   - If it is tracked: `git rm --cached codex-progress.log` (keep the file locally).

## Workflow

1. Record a base commit for later review: `BASE_SHA=$(git rev-parse HEAD)`
2. When running this skill with Codex, use model `gpt-5.4` unless the caller explicitly overrides the model.
3. Open `references/prompts/step-auto-mixed.md` and follow it using the plan doc path.
   - Important: it includes a one-time tooling discovery + dependency install + "Tooling config" phase; do that once and reuse it for every step.
   - For C/C++ repositories, extend the prompt's tooling discovery to identify the repo-native build/test/lint path before Step 1. Check for `CMakeLists.txt`, `compile_commands.json`, `meson.build`, `BUILD`/`WORKSPACE`, `Makefile`, and repo docs. Reuse the canonical configure/build/test/lint commands for each later step instead of rediscovering them.
