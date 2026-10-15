---
name: implement-issues
description: >-
  Implement a set of GitHub issues in parallel - triage or take an explicit
  issue list, group by file-conflict, create a worktree per lane, delegate to
  sub-agents, open a PR per lane; never merges. Use when asked to implement
  issues, work the backlog, or pick up multiple issues in parallel.
disable-model-invocation: true
---

# Implement Issues

Turn a set of GitHub issues into open PRs via parallel, worktree-isolated lanes.
One lane per issue: its own worktree, its own branch, its own PR. This skill
orchestrates and composes `branch`, `commit`, and `pr` — it **never merges**.
Hand-off to `babysit-pr` / `babysit-pr --merge` for shepherding and merge.

## Invocation

- `/implement-issues #12 #14 #17` — implement exactly these issues.
- `/implement-issues` (bare) — triage the backlog (`gh issue list`), prefer
  self-contained, file-disjoint issues, **propose a set and confirm before
  spawning** any lane.
- `--sequential` — run one lane at a time (still one worktree/branch/PR each).

## Inputs & readiness

- **Load repo context first.** At start, from the target repo checkout root,
  read `AGENTS.md` and/or `CLAUDE.md` if present. **Precedence:** `AGENTS.md`
  is authoritative when both exist — do not also apply conflicting `CLAUDE.md`
  instructions; if only one exists, use that file; if both conflict in a
  blocking way, stop and ask. Record which filename is authoritative (e.g.
  `AGENTS.md` or `CLAUDE.md`) and treat its house standards, operating
  agreement, and standing constraints as **binding** for every lane. Pass that
  chosen filename into each lane prompt so lanes do not re-pick. See the
  `stand-general` skill's **Per-repo agent context** section for the expected
  file shape. Missing the file is fine — fall back to chat instructions and
  `stand-*` skills.
- Take issues from the args, or select from `gh issue list` favouring
  self-contained and file-disjoint work.
- Every issue **must** carry an AI Implementation Prompt comment (per the `issue`
  skill). Missing it means the issue is **not fan-out-ready** — write one first,
  or run that issue as a single lane yourself. Do not hand a bare issue to a
  sub-agent.
- **Reproduce against current `main` before implementing** — specs can be stale.
  If the reported problem no longer exists, report back rather than fabricating a
  change.

## Conflict grouping

- Build a file-overlap matrix from each issue's declared file targets.
- **Disjoint** file sets → run in **parallel** lanes.
- **Overlapping** file sets → **sequence** them, or bundle into a single lane
  only when the issues genuinely must share files.
- Cap at **~10 lanes** — beyond that, batch across sessions.

## Lane claiming

Before spawning, **claim each lane** — assign the issue to yourself and/or add a
working label. This prevents a second session from opening a duplicate PR for the
same issue (a race that has bitten this workflow before).

## Per lane

1. **Orchestrator** creates the worktree per the `branch -w` convention: a
   sibling directory, branch `type/NN-slug` cut from a **freshly fetched
   `origin/main`**. **Never** place a worktree under `.claude/` — lint configs
   commonly exclude that path and will silently scan nothing.
2. **Sub-agent prompt is pointers, not content.** Instruct the lane to:
   - Work only inside the lane worktree path the orchestrator created.
   - Read issue #N and its AI Implementation Prompt comment.
   - From the **lane worktree root** (absolute path), read the authoritative
     context file the parent already chose (`AGENTS.md` or `CLAUDE.md`) when
     present. Do not resolve context from the parent checkout or any other
     directory; do not re-pick between the two files. Treat its
     standards/constraints/contract as binding; follow applicable `stand-*`
     skills.
   - Run the **full** lint and **full** test suite before **every** commit —
     never a subset.
   - Use the `commit` skill, then the `pr` skill with `Closes #N`.
   - **Never merge.** Report the PR URL on completion.
3. **Orchestrator verifies** each PR exists once the lane reports done.

## Guardrails

- **Signing pre-flight before spawning.** Confirm commit signing works now — a
  locked signing key must be surfaced to the user *before* you go AFK, not
  discovered mid-run.
- A lane that **cannot stay green STOPS and reports.** Never weaken or delete
  tests, never open a knowingly broken PR.
- Final report lists **every PR URL** and **every blocked lane** with the reason.

## Hand-off

Shepherding and merging are **not** this skill. Once PRs are open, hand off to
`babysit-pr` (drive to merge-ready) or `babysit-pr --merge`.

See also `backlog`: the interactive routing entry point that composes this
skill with `babysit-pr`. It does not auto-invoke either.

## Harness mechanics (Claude Code)

- Run lanes as **background sub-agents** so the main thread stays free.
- **Model per lane** by risk:
  - docs / config / mechanical → `sonnet`
  - logic / refactor / security / auth / CI-touching → `opus`
  - **never `haiku` for code.**
  - An explicit user instruction overrides these defaults.
- **Elsewhere** (harnesses without sub-agent spawning): run the lanes
  **sequentially** using the same worktree-per-lane layout.
