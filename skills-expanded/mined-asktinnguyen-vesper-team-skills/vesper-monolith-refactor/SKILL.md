---
name: vesper-monolith-refactor
description: This skill should be used when decomposing an oversized Vesper owner seam by seam into adjacent modules without changing behavior, especially requests to split `sessions.ts`, large managers, route shells, or mixed-responsibility services. Use it for facade-first extraction, not local cleanup and not total-LOC minimization.
---

# Vesper Monolith Refactor

Use the facade-first seam extraction pattern observed in the `sessions.ts` refactor to split large Vesper owners safely.

## When To Use

Use this skill when:
- A Vesper file is too large to reason about safely.
- A main-process manager, route shell, settings surface, or mixed-responsibility service needs to be decomposed seam by seam.
- The user asks to break up, modularize, extract, or slim down one large owner without changing behavior.
- The current task is architectural reduction of one oversized owner, not broad product redesign.

## When This Does Not Apply

- Use `code-simplifier` for local cleanup, small readability passes, or recent-edit simplification.
- Use `reducing-entropy` when the user explicitly wants the smallest possible total codebase, even if that means deletion instead of better separation.
- Use `build-electron-features` for new feature work spanning `main` / `preload` / `renderer`.

## Before You Start

Baseline checklist:

- Run `git status --short`.
- Record the current owner size with `wc -l <owner-file>`.
- Capture the import/export surface with `rg -n "^(import|export|class|function)" <owner-file>`.
- Find nearby focused tests with `rg --files apps/electron/src packages/shared/src tests | rg "<feature>|__tests__|<owner-name>"`.
- If an active refactor plan already exists, read and update it instead of starting a second plan from scratch.

Required reading before extraction:

| Target area | Read first |
|-------------|------------|
| Session/runtime/message flow | `docs/internals/session-lifecycle.md`, `docs/internals/message-routing.md`, `docs/internals/agent-spawning.md` |
| Permissions or tool execution | `docs/internals/permissions.md`, `docs/internals/code-mode.md`, `docs/internals/platform-tools.md` |
| Scheduler or long-running execution | `docs/internals/scheduler.md`, `docs/internals/factory-production.md`, `docs/internals/fresh-supervisor-loop.md` |
| Team/delegation/orchestration | `docs/internals/agent-teams.md`, `docs/internals/factory-production.md` |
| Browser or automation seams | `docs/internals/browser-automation.md`, `docs/internals/code-mode.md` |
| Skills or MCP surfaces | `docs/internals/skills-system.md`, `docs/internals/mcp-sources.md` |

If seam choice is unclear, read `references/commit-sequence.md` for the observed extraction order from the `sessions.ts` case study.

## Core Loop

1. Build a seam map with 3-7 candidates.
   Use the seam-selection worksheet in `references/tung-method.md` and choose the highest-scoring stable seam. Break ties by lower risk and better testability.

2. Extract to an adjacent job-named module.
   Move one cohesive job into a nearby file or sibling folder named after the behavior, not the old line range.

3. Keep the original owner as the facade.
   Leave guards, orchestration order, recursion/cascades, compatibility entrypoints, and delicate event or persistence boundaries in the original owner.

4. Verify the seam before touching the next one.
   Use the verification matrix below. If no focused verification path exists for a risky seam, add that first or stop.

5. Report and update the running plan.
   Record what moved, what stayed, what verification ran, and the next likely seam so another agent can resume without reconstructing context from git history.

## Verification Matrix

| Seam type | Minimum verification | Widen when |
|-----------|----------------------|------------|
| Main-process helper or lifecycle extraction | `bun run typecheck:all` and `bun test --filter <feature-or-entrypoint>` | Add `bun run lint:electron` when shared desktop contracts or Electron app surfaces changed |
| Renderer shell, route, or state extraction | `bun run typecheck:all` and `bun test --filter <component-or-route>` | Add `bun run test:e2e` when navigation, layout, hover, focus, or real Electron behavior changed |
| IPC, persistence, or workspace contract extraction | `bun run typecheck:all`, `bun test --filter <feature>`, and `bun run test:integration` | Widen to Electron E2E if the regression depends on actual renderer/main-process interaction |
| Path, config, deep-link, or instance-isolation changes | `bun run typecheck:all` and `bun run verify:instance-isolation` | Add targeted integration or E2E if startup or restored-window behavior changed |

Pass/fail rules:

- Do not call a seam complete if the minimum row for that seam did not run.
- If the seam changes `main` / `preload` / `renderer` contracts together, widen at least one layer beyond typecheck.
- If a seam has no direct tests and is high-risk, add a focused regression test before continuing.

## Vesper Refactor Safety Checklist

- Preserve parity-by-design: keep one shared core logic path for human and agent flows where the feature already requires it.
- Do not bypass JSONL/session storage APIs with raw file mutations for session data.
- Do not hardcode `~/.vesper` or `vesper://`; use `CONFIG_DIR` and the deep-link helpers.
- Do not duplicate permission mode logic or create a parallel permission state path.
- Keep the `render_ui` marker contract stable.
- Do not strand logic in only `renderer` or only agent paths when the feature is supposed to serve both.

## Success Criteria

- The original owner still acts as the stable facade for guards, ordering, recursion, or boundary side effects.
- One adjacent job-named module now owns the extracted seam with explicit inputs or callbacks.
- The minimum verification row for that seam ran and passed.
- The active refactor plan or handoff notes now record what moved, what stayed, and the next seam.

## Stop Conditions And Recovery

Pause and reassess if:

- the helper needs broad ambient access to most of the original owner
- the extraction forces guards, recursion, and orchestration order to move out together
- circular imports appear
- the wrapper grows instead of shrinks
- no trustworthy verification path exists

Recovery options:

- shrink the seam
- add the missing regression test first
- leave a thicker facade wrapper for this pass
- revert the seam and pick a smaller extraction target

## Guardrails

- Do not start with a full rewrite.
- Do not create generic `utils.ts` dumping grounds.
- Do not split one behavior across several new files in the first pass.
- Do not claim progress from file count alone; behavior and trust matter more than fragmentation.
- Do not run broad cleanup across unrelated concerns while extracting one seam.

## Composing With Other Skills

| Skill | Usage |
|-------|-------|
| `vesper-electron-testing` | Add renderer or Electron regression coverage after shell/state refactors |
| `verify-and-ship` | Run final verification, commit, push, and optionally create a PR |
| `code-simplifier` | Do a focused cleanup pass after the seam is safely extracted |
| `reducing-entropy` | Switch here if the user explicitly wants total code size reduced rather than better decomposition |

## Response Contract

When using this skill, report:

- the chosen seam
- why it beat nearby seams
- what stayed in the facade
- what verification ran
- any stop conditions hit
- the next likely seam

Mirror this level of specificity:

```text
Chosen seam: processing cancel
Why it won: one cohesive cancellation lifecycle, narrow dependency bag, direct regression path
Stayed in facade: early return, delegation-child cascade, public entrypoint
Verification: bun run typecheck:all; bun test --filter processing
Stop conditions: none
Next seam: processing stop
```

## References

- Use `references/tung-method.md` for seam scoring, facade-boundary rules, worked patterns, and provenance.
- Use `references/commit-sequence.md` for the observed extraction order and case-study chronology from the `sessions.ts` refactor.
