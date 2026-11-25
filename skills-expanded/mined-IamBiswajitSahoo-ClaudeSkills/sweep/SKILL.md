---
name: sweep
description: Maintainability sweep of a code change in any codebase — checks it against the project's own rules, cuts vestigial, redundant, speculative and dead code, reverse-analyses it against what the codebase already provides and what was asked for, flags correctness, contract-drift, security, performance and test risks, and checks touched docs for accuracy and bloat. Fans the reading out to haiku/sonnet lens agents, reports one severity-ranked table, and fixes only what the user approves. Use when the user says "sweep", "sweep the changes", "clean this up", or before committing a non-trivial change.
metadata:
  author: Biswajit Sahoo (https://github.com/IamBiswajitSahoo)
  license: Apache-2.0
argument-hint: '[path | commit-range | --module <dir> | --all]'
---

# Sweep

A post-change pass that keeps code maintainable. The overriding bias is **the simpler change**: a
fix that adds abstraction, indirection or configuration the code does not need is not a finding.

## Phase 1 — Scope and rules

1. **Scope** from `$ARGUMENTS`: a path, a commit range, `--module <dir>` (every file of that
   module), or `--all`. Empty means the working tree (`git diff HEAD`, plus untracked files); if
   that is clean, the last commit. Sweep what is on disk, never memory. State the scope in the
   report's first line.
2. **Project rules.** Collect the paths of whichever exist: `CLAUDE.md` and `AGENTS.md` at the root
   and in touched directories, `.claude/rules/`, `.cursor/rules/`, `CONTRIBUTING.md`, linter and
   formatter configs, and any list of shared helpers. Project rules override this skill's defaults.
3. **Test and build commands** from the rules, `package.json`, `Makefile`, or the project's
   equivalent. Note them for Phase 5; do not run them yet.
4. **Never read or print secrets** (`.env*`, keys, credentials). Name the variable, never the
   value. Repeat this in every agent brief.

## Phase 2 — Fan out

The main session orchestrates; agents read. Dispatch every lens in **one message** of parallel
`Agent` calls. Use the fully-qualified `subagent_type`, or the call falls back to
`general-purpose` and ignores the agent's model.

| Lens | subagent_type | Model | Runs when |
|---|---|---|---|
| Conventions | `bix-utils:sweep:conventions` | haiku | always |
| Simplify | `bix-utils:sweep:simplify` | sonnet | always (`mode: diff`) |
| Module simplify | `bix-utils:sweep:simplify` | sonnet | a file is added or removed, 3+ files of one module change, or `--module` (`mode: module`) |
| Risk | `bix-utils:sweep:risk` | sonnet | always |
| Reverse | `bix-utils:sweep:reverse` | sonnet | always |
| Docs | `bix-utils:sweep:docs` | sonnet | any `.md` is in scope |

**Standalone install** (no `bix-utils:sweep:*` agents available): launch `general-purpose` with
the model above, and start each brief with "Read
`${CLAUDE_SKILL_DIR}/references/agents/<lens>.md` and follow it as your instructions", where
`<lens>` is the last part of the `subagent_type`.

- **Partition by size.** Up to ~5 files and ~400 changed lines: one agent per lens. Larger: split
  each lens by module so no agent gets more than that.
- **Brief** each agent with: the scope, its partition's file list and diff command, the rule-file
  paths, the requirement (the user's request, plan and decisions from the conversation, else the
  commit message or tracker entry), the shared-helper list if any, user-chosen designs to keep, findings already known, the
  path to `references/symbol-search.md` in this skill's directory, and the no-secrets rule. Agents
  read the full files themselves.

## Phase 3 — Verify and report

Agent output is untrusted. Before reporting:

- Drop rows without `file:line` and an exact snippet, and rows you cannot demonstrate.
- Re-verify every removal, move, rename and correctness claim yourself (LSP references, or the
  grep and controls in `references/symbol-search.md`).
- Merge duplicates; the same `file:line` from two lenses keeps the higher severity.
- A defect in a touched file that predates the change stays in, tagged `pre-existing`.

Report one table, sorted by severity, then by file:

| # | Severity | File:Line | Category | Issue | Proposed fix |
|---|---|---|---|---|---|

- 🔴 **Critical** — correctness, security or contract risk, or a doc that actively misleads.
- 🟠 **High** — debt that will bite: misplacement, coupling, over-engineering, a broken project rule.
- 🟡 **Medium** — redundant, vestigial or dead code; avoidable complexity.
- 🟢 **Low** — naming and comment polish. Collapse more than a few into one row.

**Issue** names the defect and what breaks under which input. **Proposed fix** is phrased so the
user can approve it as-is. If nothing survives, say so; never pad.

## Phase 4 — Propose and apply

After the table: one short plan grouping the fixes, which to leave and why, and only the genuine
decisions (a trade-off, a name, a wire or migration rename), one question each. Apply nothing
until the user approves. Findings deferred for later go to the project's tracker if it has one.

Apply approved fixes in dependency order, so cosmetic work is done once:

1. Placement and moves.
2. Redundancy and constants.
3. Complexity (inlining, merges, splits).
4. Correctness, contracts, security, performance.
5. Naming (LSP rename, or whole-word grep with controls).
6. Comments, docstrings and docs.

If the plan proves wrong mid-way, stop and re-report rather than improvise.

## Phase 5 — Finish

1. Re-read the final diff against the project rules.
2. Grep for dangling references to anything removed or renamed.
3. Run the build and tests found in Phase 1, or ask the user to when they need an editor or
   device. Report the real output; never claim a pass you did not see.
4. Hand back numbered manual checks where behaviour changed.
5. Leave the work uncommitted unless the user asks to commit; then follow the project's commit
   rules.
6. Summarise in a few lines what was applied and what was left, with the reason.
