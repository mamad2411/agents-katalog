---
name: init-or-refactor-agents-md
description: Create or compress project agent instructions into one short AGENTS.md with pragmatic repro-first testing guidance.
---

# Init Or Refactor AGENTS.md

Goal: produce one short, high-signal `AGENTS.md` that agents will actually follow. Prefer one canonical file.

## Workflow

1. Read existing instruction files:
   - `AGENTS.md`
   - `CLAUDE.md`
   - `CODEX.md`
   - `.cursorrules`
   - similar repo-local agent instruction files

2. Show conflicts.
   - If instructions disagree, show both and ask which one wins.
   - Bug fixes should use repro-first testing when practical: capture the confirmed failure with a failing behavior test, fix it, then keep the test as regression coverage. Flag instructions that encourage implementation-detail tests, speculative tests for planned behavior, vanity coverage targets, or tests not tied to a confirmed failure.
   - Flag instructions that allow adding dependencies without user approval.
   - Flag instructions that require preserving local patterns when they are unsound, accidental, or undocumented.
   - Flag instructions that discourage necessary rewrites solely because they are larger.

3. Ask about commit and PR discipline before drafting.
   - Summarize any existing branch, commit, PR, review, release, or deploy rules found in the repo.
   - Ask the user to choose one workflow:
     - Direct default branch: work directly on `main` / `trunk`; commit and push early and often in logical chunks.
     - Branch and PR: create a focused branch, commit and push early and often in logical chunks, and open or update a PR for review.
     - Other: ask the user to describe the repo's workflow in one paragraph and preserve that direction faithfully.
   - If the repo already has a clear convention, recommend the matching option.
   - For Direct default branch or Branch and PR, include explicit commit-and-push discipline in the draft.
   - For Other, include only the workflow the user describes; do not invent branch or PR rules.

4. Offer Matt Pocock skill setup before drafting.
   - Explain that this optional setup configures `## Agent skills` and `docs/agents/` for Matt Pocock engineering skills.
   - Ask only whether the user wants to run `setup-matt-pocock-skills` for this repo.
   - If the user declines, skip this setup.
   - If the user elects to run it, use this fixed decision packet:
     - issue tracker: Local markdown under `.scratch/<feature>/`
     - triage labels: canonical defaults from `setup-matt-pocock-skills` at invocation time
     - domain docs: Single-context with root `CONTEXT.md` and root `docs/adr/`
   - If elected and `setup-matt-pocock-skills` is available, call it with the decision packet and ask it to treat the packet as the user's preselected answers.
   - Do not ask the user to choose GitHub, multi-context docs, or alternate labels; ask only if repo evidence makes one of the preselected answers impossible to apply.
   - Keep `setup-matt-pocock-skills` responsible for its own `## Agent skills` block and `docs/agents/*`; do not copy its templates, docs, or setup instructions into this skill.
   - If `setup-matt-pocock-skills` is unavailable, say so and continue with only the `AGENTS.md` draft.

5. Draft one short `AGENTS.md`.
   Keep only:
   - one-line project description
   - non-obvious commands
   - commit and PR discipline chosen by the user
   - hard rules, including repro-first bug testing
   - simplification discipline, quality bar, and rewrite guidance
   - dependency policy
   - critical safety or approval rules

6. Delete fluff.
   Remove vague, duplicate, or obvious advice.

7. Write terse rules.
   - Prefer bullets over prose.
   - Prefer rules over explanations.
   - State commit and PR workflow only when the user chose one or the repo already has a clear rule.
   - State testing expectations briefly and operationally.
   - State dependency approval requirements explicitly.
   - State when to challenge local patterns and consider rewrites.
   - Do not create linked docs unless explicitly asked.
   - Do not create tool-specific files unless needed.
   - If `CLAUDE.md` is needed, its entire contents must be exactly `@AGENTS.md`.

Ask for confirmation before writing files.

## Example `AGENTS.md`

```md
# Project Name

## Commands

- Build: `...`
- Test: `...`
- Lint: `...`

## Git Workflow

- Use the standard branch and PR flow.
- Create a focused branch for each logical change.
- Commit and push early and often in logical chunks.
- Keep each commit scoped to one coherent behavior, policy, or cleanup.
- Open a draft PR once the first useful slice is pushed; keep it updated as work continues.
- Do not force-push or rewrite shared history unless explicitly asked.

## Rules

- For confirmed bugs, capture the failure with a failing behavior-level repro test when practical, then fix it and keep the test as a regression test.
- Do not write tests for planned behavior, predicted risk, implementation details, coverage targets, or test-count goals.
- For non-bug changes, use existing checks and focused manual verification unless the user explicitly asks for tests.
- Work in vertical slices: one behavior at a time.
- Test only observable behavior through public interfaces; never private internals.
- Prefer a focused bug repro over broad assertions or fixture-heavy tests.
- Mock only system boundaries.
- Refactor only after the fix is verified: simplify touched code without changing behavior.
- Ask before adding dependencies; prefer stdlib, existing deps, or small local code.
- Before proposing a dependency, check maintenance, license, docs, security, and transitive deps.
- Keep diffs small.
- Proactively simplify touched code; prefer explicit over clever.
- Follow existing patterns only when they are sound and intentional; proactively challenge them when they conflict with best practices or project goals.
- Prefer the correct fix over the smallest patch; propose or perform rewrites when local structure is the problem.
- Do not avoid necessary redesign because it is larger; explain the tradeoff and proceed in reviewable slices.
- Ask before risky or destructive changes.
- Run relevant checks before finishing.
```

## Output

Present:

1. Sources gathered
2. Conflicts found
3. Commit and PR workflow choice
4. Matt Pocock skill setup choice
5. Proposed `AGENTS.md`
6. Items removed
