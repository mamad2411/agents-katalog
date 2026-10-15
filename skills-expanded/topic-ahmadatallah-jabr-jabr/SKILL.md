---
name: jabr
description: >-
  Structure a feature as a stack of small, dependent pull requests and manage it
  end-to-end with plain git + the GitHub gh CLI. Use when the user wants to break
  a large feature or change into stacked / chained PRs, create or manage a PR
  stack, restack (rebase) dependent branches after editing a lower one, submit a
  whole stack of PRs at once with correct base branches, navigate up/down a branch
  stack, or sync a stack after branches merge. Triggers on "stacked PRs", "stack of
  PRs", "PR stack", "stacked diffs", "split this into PRs", "break this feature into
  PRs", "chain these branches", "restack", and "jabr".
license: MIT
compatibility: Requires Bun, git, and the GitHub gh CLI (run `gh auth login`). Designed for Claude Code.
metadata:
  author: Ahmad Atallah
  version: "0.1.2" # x-release-please-version
allowed-tools: Bash(bun:*) Bash(git:*) Bash(gh:*) Read Edit Write
---

# jabr — stacked pull requests

Reunite a feature's broken-down pieces into one clean, reviewable whole: a
**stack** of small, dependent PRs instead of one giant one. This skill plans the
decomposition and writes the code; a TypeScript engine handles the git/`gh`
mechanics (parent tracking, `rebase --onto`, force-push ordering, PR base wiring).

## Running the engine

Invoke the bundled engine with Bun. `${CLAUDE_PLUGIN_ROOT}` is set by Claude Code to
this plugin's install directory, so the path resolves wherever the plugin is installed:

```bash
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts <command> [args]
```

All commands run against the user's **current** git repository (their working
directory), not the plugin directory. Stack metadata lives in that repo's local
git config. Prerequisites: a git repo, Bun, and (for `submit`/`sync`) `gh auth login`.

If the user prefers, suggest an alias: `alias jabr='bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts'`.

## Mental model

- The **trunk** (usually `main`) is the root.
- Each branch in a stack is **stacked on** its parent and contains one coherent
  change. Its PR's base is its parent branch, so the PR's diff shows only that
  change — not everything below it.
- When a lower branch changes (new commits, an amend, a rebase onto an advanced
  trunk), every branch above it must be **restacked** (rebased) to stay current.
  `jabr` does this automatically and exactly, replaying only each branch's own
  commits so nothing is duplicated.

## Workflow

### 1. Plan the stack

Before writing code, decompose the feature into an ordered list of small,
independently-reviewable units — each becomes one branch/PR. A typical ordering:
schema/migration → data layer → API/business logic → UI → tests/docs. Keep each
unit focused and buildable on its own. See
[references/planning.md](references/planning.md) for heuristics and a worked example.

Confirm the plan with the user before creating branches.

### 2. Build the stack

For each unit, create a branch, write the code, and commit:

```bash
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts init                 # once: record the trunk
# implement unit 1, then:
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts create api-schema -a -m "Add user schema + migration"
# implement unit 2 (now stacked on api-schema), then:
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts create api-endpoints -a -m "Add /users endpoints"
```

Inspect and move around the stack with `log`, `up`, `down`, `top`, `bottom`,
`checkout`.

### 3. Submit

```bash
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts submit --stack
```

Pushes each branch (root-first) and opens/updates one PR per branch with its base
wired to its parent, then writes a stack-navigation block into every PR body. Use
`--draft` for drafts, `--no-push` to only sync PR metadata.

### 4. Address review feedback

Edit the relevant branch, then let `jabr` realign everything above it:

```bash
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts down          # go to the branch under review
# fix code
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts modify -a     # amend + auto-restack descendants
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts submit --stack
```

### 5. Sync after merges

When PRs merge (via GitHub), bring the local stack up to date:

```bash
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts sync            # ff trunk, report merged, restack
bun "${CLAUDE_PLUGIN_ROOT}"/scripts/jabr.ts sync --delete   # also delete merged branches + restack
```

## Command reference

| Command | What it does |
|---|---|
| `init [trunk]` | Set/auto-detect the trunk |
| `create <name> [-a] [-m msg]` | Branch off current HEAD, track parent, optional stage+commit |
| `modify [-a] [-m msg] [-c]` | Amend (or `-c` new) commit, then restack descendants |
| `track <name> [-p parent]` / `untrack [name]` | Add/remove a branch from the stack |
| `log` / `status` | Show the stack tree |
| `parent` / `children` / `trunk` | Inspect the graph |
| `checkout <b>` · `up [-n]` · `down [-n]` · `top` · `bottom` | Navigate |
| `restack [branch]` | Rebase a branch + descendants onto their parents |
| `move --onto <target>` | Reparent the current branch, restack descendants |
| `rename [old] <new>` · `delete <name>` | Rename / delete (children reparented) |
| `squash [-m msg]` | Collapse a branch's commits into one, restack descendants |
| `submit [--stack] [--draft] [--no-push]` | Push + create/update PRs with bases + nav |
| `sync [--delete]` | Fast-forward trunk, detect merged PRs, restack remaining |

## Handling conflicts

If a restack hits a rebase conflict, the engine stops and prints the failing
branch. Resolve the conflict in the working tree, run `git rebase --continue`
(or `git rebase --abort`), then re-run `restack`. Never leave the stack
half-restacked — finish or abort before continuing other operations.

## Out of scope

`jabr` does only what plain git + `gh` do well. Anything needing a hosted service
— a merge queue, a web review UI, server-side stack management — is out of scope;
merge through GitHub, then `sync`. For less-common local operations (reorder,
split, absorb) see [references/workflow.md](references/workflow.md).
