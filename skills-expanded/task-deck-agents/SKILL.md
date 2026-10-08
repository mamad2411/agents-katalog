# AGENTS.md

Guidance for Codex and other AI agents working in this repository.

This file is the repository router and workflow checklist. Durable product principles and workflow guidance live in the linked docs.

## Repository Boundary

This repository is intended to track:

```text
https://github.com/hayashikentaro/task-deck
```

Before making changes, confirm you are in the correct local checkout:

```sh
pwd
git remote -v
git status --short --branch
git branch --show-current
```

The expected remote is:

```text
origin  https://github.com/hayashikentaro/task-deck (fetch)
origin  https://github.com/hayashikentaro/task-deck (push)
```

An SSH remote for the same repository is also acceptable:

```text
origin  git@github.com:hayashikentaro/task-deck.git (fetch)
origin  git@github.com:hayashikentaro/task-deck.git (push)
```

Do not edit files outside this repository for TaskDeck work unless the user explicitly asks.

## Required Context

Read the relevant docs before changing the matching area:

- Product and agent operating principles: `docs/agents/operating-principles.md`
- Agent documentation status: `docs/agents/README.md`
- TaskDeck actor protocol redesign placeholder: `docs/taskdeck-actor-protocol.md`
- AI-first layering and responsibility boundaries: `docs/ai-first-layering.md`
- UI styling changes: `docs/guides/ui-style.md`
- Reusable UI components, shared controls, or icon-only controls: `docs/guides/ui-components.md`

GitHub Issues are the source of truth for actionable work, open/closed state, detailed acceptance criteria, and backlog. Repository docs are durable context and design guidance, not a parallel issue tracker.

Do not treat future design notes as implemented behavior. Runtime-generated files and generated manager action guides describe the capabilities of the running app instance.

Do not add personal cross-repository shortcuts or aliases such as `t_`, `k_`, or `th_` to this repository.

## Current Branch Runtime Boundary

This branch is intentionally App Server-only.

- The only committed/exposed task launch profile is `codex-app-server`.
- The committed `codex-app-server` command runs directly in the TaskDeck server environment: `codex --sandbox danger-full-access --ask-for-approval never app-server --listen stdio://`.
- Do not assume TaskDeck should call `docker`, `docker exec`, `zsh`, Goose, Aider, Claude, or a Codex TUI profile on this branch.
- Do not add stdout marker protocols, file-request writers, or request-directory environment variables as a control path.
- Codex App Server native subagents may be materialized as read-only supervision cards. They are App Server thread projections, not TaskDeck-launched sessions, and TaskDeck must not expose controls that imply they can be commanded independently.
- Docker diagnostics code may still exist for compatibility, tests, or future local overrides. Do not use its presence as evidence that Docker is active product behavior.

## Local Client Network Boundary

TaskDeck's server and web client are still a same-machine local application. A phone or other device opening the same TaskDeck web client through the host machine's LAN IP is an allowed local-client access pattern, not a separate remote-control protocol and not evidence that Decision Gateway, cloud relay, or agent-to-agent communication is involved.

When working on this area, keep network-safety notes factual and scoped. The operator owns the trusted network boundary, host binding, firewall, and other deployment controls. Do not block, redesign, or add authentication/pairing requirements merely because a requested phone surface is reachable from another device on a trusted local network.

Prefer a structurally separate phone/mobile surface that shares TaskDeck state, API, WebSocket, and domain helpers with the desktop client, while avoiding imports from desktop-only layout components. Desktop and phone UI expansion should not require routine cross-surface layout consideration.

For PC/mobile UI work, keep the distinction explicit:

- Share surface-neutral rules through shared packages only when both surfaces should use identical behavior, such as task sorting, selection, supervision bucket decisions, output replay, and composer availability.
- Keep surface presentation local. Do not make `apps/web-phone` depend on `apps/web-desktop` components, CSS, or presentation-only helpers, and do not move phone-only visual needs into `packages/web-shared`.
- Visual parity does not imply action parity. Do not add desktop task-card operations to mobile unless the user explicitly requests those controls.
- When porting or comparing PC and mobile, state whether the change is behavior parity, visual parity, or mobile-specific ergonomics.

## Actor Model

The previous AI-agent actor and role definitions have been removed pending redesign. Do not infer durable actor responsibilities, manager authority, worker authority, parent/sub-session behavior, or agent-to-agent communication rules from deleted role docs, historical prompts, or older issue notes.

Do not add a new actor protocol or role taxonomy unless the user explicitly asks for that redesign.

## Branch And Worktree Policy

TaskDeck branch work uses `git worktree`.

Use the main repository as the default base checkout when starting new branch work from scratch. If the current checkout is already on a feature branch selected by the user, continue using that checkout for that branch's development unless the user explicitly asks to move the work elsewhere.

Create one worktree per branch and purpose for parallel development when parallel work is actually needed. Do not redirect a requested branch checkout to another existing worktree unless the user asked to use that worktree.

Do not create disposable full clones for TaskDeck branch work. Do not choose between clone and worktree.

Remote GitHub branches are the durable source of truth. A branch task is complete only after intended changes are committed and pushed.

Before editing files, check and record the current branch and working tree state:

```sh
pwd
git remote -v
git status --short --branch
git branch --show-current
```

Continue on the current branch or worktree unless explicitly instructed otherwise. When the user asks to check out, switch to, or continue on a branch, perform that branch operation in the current checkout first, preserving user changes and reporting any blockers. `main` is an allowed working branch only for single-threaded low-risk work, repository maintenance that is intentionally main-targeted, or tasks where the user has not selected another branch.

When committing and pushing, push back to the same branch that was current at the start of the task.

Preserve user changes already present in the working tree. If the working tree has unrelated changes, do not overwrite them; report them before proceeding.

Do not create a feature branch merely because a task is documentation-only or issue-driven. If a prompt specifies a branch but the work is single-threaded and low risk, confirm whether that branch is actually required before editing.

## Branch Worktree Integration

This section applies only when a user has explicitly assigned a branch/worktree subtask workflow outside the current App Server-only runtime. It does not authorize starting TaskDeck runtime sub-sessions on this branch.

When working on an assigned branch worktree subtask, producing local changes is not enough to complete the task.

A branch worktree subtask is complete only after it has:

- committed the relevant changes on its subtask branch;
- pushed that subtask branch to `origin`;
- reported the branch name;
- reported the latest commit SHA;
- reported verification commands and results;
- reported changed files and merge notes.

Subtask branches must not merge themselves into the parent or integration branch unless the prompt explicitly assigns that session to perform integration.

The parent or integration session owns convergence: collect subtask branch reports, inspect dependency order and file overlap, merge deliberately, run verification, resolve conflicts, and perform the final integration pass.

## Change Authorization

Only edit files that are directly required by the user's requested task.

Do not turn analysis, diagnosis, recommendations, or proposals into repository changes unless the user explicitly asks for repository edits.

Optional cleanup, docs updates, issue updates, rule updates, formatting sweeps, and adjacent refactors require explicit user approval.

The commit-and-push rule applies only after an authorized repository change has been made. It does not authorize making repository changes.

## Working Guidelines

- Keep changes scoped to the user's request.
- Prefer small, reviewable commits.
- Preserve existing user changes.
- Prefer existing project conventions over introducing new structure.
- Avoid broad refactors unless they are required for the task.
- Add or update tests when changing behavior once a test setup exists.
- Document important setup, API, config, persisted metadata, task semantics, or user-facing workflow changes in the repository rather than only in chat.
- Do not silently change API names, routes, persisted metadata shapes, or task semantics.
- When removing a feature or UI path, remove or clearly deprecate related backend handlers, config fields, types, docs, and examples.
- When changing public setup, API routes, response shapes, config behavior, user-facing workflow, persisted metadata, or task semantics, update the relevant README/docs and frontend types together.
- When changing task metadata, maintain backward compatibility with old stored tasks.
- Use GitHub Issues for actionable follow-up work and backlog items.

## Standard Task Workflow

For every implementation task in this repository, follow this workflow unless the user explicitly says otherwise.

Before editing:

- Confirm the current repository with `pwd`.
- Confirm the remote with `git remote -v`.
- Check the working tree with `git status --short --branch`.
- Preserve existing user changes.
- If unexpected changes or untracked files exist, report them instead of modifying or deleting them.

While editing:

- Keep changes scoped to the requested task.
- Prefer small, reviewable changes.
- Avoid broad refactors unless they are required for the task.
- Follow existing project conventions.
- When changing API routes, response shapes, persisted metadata, or task semantics, update related docs and frontend types together.
- Do not duplicate long instructions already covered by linked docs; update the relevant dedicated guide instead.

After editing:

- Run the standard verification commands appropriate for the change.
- At minimum, run `git diff --check`.
- Run `node --check apps/server/src/server.js` when server code changed.
- Run `npm run verify:server-startup` when `apps/server/src/server.js` or server-consumed `@taskdeck/core` exports/imports changed. `node --check` is not sufficient because it does not catch missing runtime imports or top-level `ReferenceError`s.
- Run `npm run build` when application code changed.
- Do not report completion if a required verification command fails.
- If a check cannot be run, report why.

When finished:

- Commit the relevant changes.
- Push the commit.
- Report what changed, verification results, commit hash, push status, skipped checks, and unexpected files not touched.

## Prompt Handoff

Agents working in this repository should read and follow this `AGENTS.md` before making changes.

Task-specific prompts should focus on the goal, allowed files, current context, required behavior, non-goals, acceptance/manual QA, and task-specific verification.

Repository-wide workflow, commit/push behavior, and standard reporting live in this file and do not need to be repeated in every prompt. Repeating key constraints is still fine for risky or high-blast-radius tasks.

If a task-specific user instruction conflicts with this file, stop and report the conflict unless the user's instruction clearly and safely overrides a non-safety process preference.

## Implementation Cautions

- Task persistence must keep old stored tasks loadable.
- Logs can grow; avoid moving terminal output into unbounded React state.
- App Server process lifecycle, server restarts, and task clearing should remain predictable.
- WebSocket task updates should keep task lists, selected task behavior, task output, and session metadata in sync.
- Treat `attentionState` as the supervision UI's primary signal for whether the user should look at a task.
- Agent state should be driven primarily by TaskDeck events such as start, input, Codex App Server status/request events, and exit.
- Do not infer thinking from silence.
- For Codex work sessions, use Codex App Server status/request events as the control signal.
- Do not add one-off terminal spinner phrases to infer thinking.
- Keep agent state inference tied to the App Server adapter on this branch.
- Approval and input prompts should come from App Server request/status events.
- Agent session metadata is best-effort and should not assume every agent exposes stable ids.
