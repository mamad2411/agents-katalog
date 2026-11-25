---
name: executing-micro-plans
description: Use when a micro-dev PLAN.md already exists and needs to be executed, resumed after an interruption, or picked up in a different harness (Claude Code, Antigravity, Gemini CLI) than the one that wrote it.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
  - Task
  - mcp__token-savior__search_codebase
  - mcp__token-savior__find_symbol
  - mcp__token-savior__get_call_chain
  - mcp__token-savior__get_function_source
  - mcp__token-savior__get_full_context
  - mcp__token-savior__find_dead_code
  - mcp__token-savior__ts_search
  - mcp__code-review-graph__semantic_search_nodes_tool
  - mcp__code-review-graph__query_graph_tool
  - mcp__code-review-graph__get_impact_radius_tool
  - mcp__code-review-graph__get_affected_flows_tool
  - mcp__code-review-graph__get_minimal_context_tool
  - mcp__code-review-graph__get_review_context_tool
  - mcp__code-review-graph__detect_changes_tool
  - mcp__code-review-graph__refactor_tool
---

# Executing Micro Plans

Act as an engineer who treats the plan file as the only source of truth and refuses to check a box without having just run the command that proves it.

## Overview

`micro-dev` **writes** the plan. This skill **executes** it — identically on every harness.

**Core principle:** the plan file on disk is the only state. Not the todo list, not the task artifact, not the conversation. Any harness that can read and edit a markdown file can start, resume, or finish the same task.

**Announce at start:** "Using executing-micro-plans to execute `<plan path>`."

**Violating the letter of this skill is violating the spirit of it.**

## When to Use

- A `docs/micro/<YYYYMMDD-slug>/PLAN.md` exists and execution has not started
- A plan has some steps `[x]` and some `[ ]` — resuming, same session or later
- A plan was written in one harness and is being executed in another
- Someone says "continue the plan", "reprends le plan", "finish that micro task"

**Do NOT use when:**
- No plan file exists → use `micro-dev` to produce one first
- The task was fast-path (daily-log only, no PLAN.md) → nothing to execute
- The plan sits under `docs/micro/archive/` → it is already `done`; read it for reference, do not re-run it
- The plan is multi-phase / architectural → wrong tool, that is GSD territory

## The Iron Law

```
NO [x] WITHOUT FRESH EVIDENCE IN THE SAME MESSAGE
```

A step is checked off only after the command that proves it ran **in the message where you check it**. Not "it passed earlier". Not "the code is obviously right". Not "the agent reported success".

If no command can prove a step, the step is not verifiable — say so and fix the plan before executing it.

## Execution State Contract

This is what makes the plan harness-agnostic. Every executing session maintains exactly these markers in the plan file:

| Marker | Meaning |
|---|---|
| `- [ ]` step | Not started |
| `- [~]` step | **In progress, this session** — written before doing the work |
| `- [x]` step | Done AND verified with evidence |
| `## Execution Log` entries | Append-only audit trail, one line per state change |

`- [~]` is the crash-recovery marker. A step left at `- [~]` means a previous session died mid-step: its file edits may be half-applied.

### Execution Log format (REQUIRED)

Append to `## Execution Log` in the plan file. Create the section if missing.

```markdown
## Execution Log
- 2026-08-08T14:03Z | claude-code | step 2 | started
- 2026-08-08T14:07Z | claude-code | step 2 | done | `pnpm build` exit 0
- 2026-08-08T14:31Z | antigravity | step 3 | blocked | `pytest -q` 2 failed — see Notes
```

Fields, in order: UTC timestamp | harness id | step number | state | evidence.
Harness id is one of `claude-code`, `antigravity`, `gemini-cli`. Get the timestamp from the shell (`date -u +%Y-%m-%dT%H:%MZ`), never from memory.

## Quick Reference

| Question | Answer |
|---|---|
| What is the state? | The plan file on disk. Never the todo list, never the conversation. |
| The plan has no `Definition of Done` / no `Surgical Scope`? | Format gate, Phase 1. Tick nothing. Write the finding into the file, then ask or upgrade. |
| When may a step be `[x]`? | Only with the proving command's output in the same message. |
| A step needs a file outside `Surgical Scope`? | Stop. The plan was wrong. Ask the user. |
| A step fails twice? | `status: blocked`, leave `[~]`, report. Never skip ahead. |
| Who commits? | Nobody. Staging is the user's call. |

Seven phases, in order: load and reconcile → critical review → preflight → execution loop → failure protocol (on demand) → teardown → close out.

**Terminology**: *phase* = a stage of this skill. *step* = a numbered item in the plan's `## Steps`. They are never the same thing.

For a worked plan carrying a real mid-plan harness switch in its Execution Log, read `micro-dev/references/EXAMPLES.md`, example 3. It shows the exact artifact this skill is supposed to produce.

## The Process

### Phase 1 — Load and reconcile

1. Read the plan file in full.
2. Run the **Format gate** below. It gates everything that follows.
3. Read the frontmatter `status`. If `done` → stop, report it is already complete, ask before re-running.
4. Count steps by marker. Determine entry mode:

| State found | Mode |
|---|---|
| All `- [ ]`, no Execution Log | **Cold start** → go to Phase 2 |
| Some `- [x]`, none `- [~]` | **Clean resume** → go to Phase 2, skip completed steps |
| Any `- [~]` | **Dirty resume** → run the reconciliation below first |
| Frontmatter `status: blocked` | Read `## Notes`, surface the blocker to the user, wait |

**Format gate.** This protocol reads the plan by section name. Confirm all of these exist:

| Section | Which phase dies without it |
|---|---|
| frontmatter `status:` | Phase 1 entry mode, Phase 5 `blocked`, Phase 7 `done` |
| `## Surgical Scope` | Phase 2 scope check, Phase 4 drift stop, Phase 6 orphan bound |
| `## Definition of Done` | Phase 3 baseline, Phase 7 close out |
| `## Steps` | Phase 4 |
| `## Code Review` | Phase 7 |
| `## Execution Log` | the whole state contract |

Any of them missing → **do not tick anything.** Only the marker and Execution Log contract survives a format mismatch, so an agent that walks the steps anyway produces a flawless log over zero verification. That artifact is indistinguishable from success, which is exactly why the check comes first.

Two acceptable routes:

- **Stop and ask.** Write which sections are missing into the plan file itself — the finding is state, not conversation — leave every step unticked, and wait. A plan file that says why it was not executed is resumable; a silent stop is not.
- **Upgrade to the current format first, with the user's agreement**, then execute the upgraded file. Never invent a `Definition of Done` mid-run and grade yourself against it.

Also flag any step that no command can settle (`Make sure nothing else broke`, `Verify it looks right`). Saying so out loud is part of passing this gate — an unverifiable step can never legitimately reach `[x]`.

**Dirty resume reconciliation** (a `- [~]` step exists):
1. Run the version-control diff for the repo (`git status` + `git diff`).
2. Compare the diff against what that step was supposed to change.
3. Fully applied and verifiable → run its verification command now, then set `[x]`.
4. Partially applied → revert that step's partial edits, reset to `- [ ]`, redo it cleanly.
5. Cannot tell → stop and ask the user. Do not guess on a half-written file.

Log the reconciliation outcome before continuing.

### Phase 2 — Critical review before touching anything

Read the plan as an adversary, not as an author. Check:

- Every `Definition of Done` item names an **exact runnable command** or an explicit `n/a` with a reason
- Every file in `Surgical Scope → Files touched` actually exists (or is explicitly a new file)
- Every symbol in `Symbols replaced` actually exists in the codebase right now
- No step depends on a later step
- The plan still matches reality — the codebase may have moved since the plan was written

Any concern → raise it with the user **before** executing. Do not silently repair the plan and proceed.

Plan is sound → proceed. On Claude Code, mirror the steps into the todo tool for visibility; the file still wins on any disagreement.

### Phase 3 — Preflight

1. `git status`. Uncommitted changes inside the Surgical Scope from another session → stop and surface. Never stash or discard silently.
2. **Read the project's convention files.** The plan is never the full contract. Your harness auto-loads only the filenames it knows, only at the paths it looks at — so a convention file named for a different harness, or nested one directory below the root, is invisible to you until you go looking. List them, then read the ones covering the files in `Surgical Scope`:

   ```bash
   # root, then every level down to the directories you are about to touch
   ls CLAUDE.md AGENTS.md GEMINI.md CONTRIBUTING.md .cursorrules 2>/dev/null
   find . -not -path '*/node_modules/*' \( -name 'CLAUDE.md' -o -name 'AGENTS.md' -o -name 'GEMINI.md' \)
   ```

   Name the files you read in `## Notes`. A convention obeyed by luck is not obeyed — the next execution breaks it. A convention file that contradicts the plan is a Phase 2 concern: raise it, do not pick a side yourself.

3. Run each `Definition of Done` command **once, now**, before changing anything. This captures the baseline: which ones already pass, which already fail. A DoD command that errors out because the tool is not installed is a broken plan, and you find that out now rather than at the end.
4. Log the baseline in `## Notes`.

### Phase 4 — Execution loop

For each unchecked step, in order:

```
1. Set the step to `- [~]` in the plan file. Save. (before doing the work)
2. Append to Execution Log: <ts> | <harness> | step N | started
3. Do exactly what the step says — nothing adjacent, nothing "while I'm in here"
4. Dead Code Gate: if the step replaced a symbol listed in Surgical Scope,
   search for remaining references and delete or migrate them IN THIS STEP.
   Search with `mcp__token-savior__find_symbol` or `ast-grep -p '<symbol>(...)'
   -l <lang>` — raw grep is blocked until a higher-tier search has run.
5. Run the verification command for this step. Read the exit code.
6. Exit 0 → set `- [x]`, append: <ts> | <harness> | step N | done | <evidence>
   Non-zero → the step is NOT done. Go to Phase 5 (Failure protocol).
```

**Scope drift is a stop condition.** If executing a step requires touching a file not listed in `Surgical Scope`, do not touch it. Stop, tell the user the plan's scope was wrong, and let them decide whether to widen it. An unplanned file edit invalidates the plan's contract.

### Phase 5 — Failure protocol

A step failed. Do not create a new step. Do not skip ahead.

1. Attempt the fix **inside the current step**. Max 2 attempts.
2. Each attempt: state the hypothesis before changing anything, then re-run the same verification command.
3. Fixed → `- [x]` with evidence, and one line in `## Notes` describing the failure and the fix.
4. Still failing after 2 attempts → **stop**:
   - Leave the step at `- [~]`
   - Set frontmatter `status: blocked`
   - Write the exact failing command and its output under `## Notes`
   - Append to Execution Log with state `blocked`
   - Report to the user and wait

If the cause of the failure is genuinely unknown (not a typo, not an obvious oversight), stop and use a systematic-debugging process instead of continuing to guess.

### Phase 6 — Teardown

Run the plan's teardown step. Bound the orphan scan strictly to the symbols in `Surgical Scope → Symbols replaced` — never a repo-wide dead-code sweep. Confirm zero orphans from this task's own symbols.

Where a code graph is available, the orphan scan is a `callers_of` query per replaced symbol (zero callers left = no orphan), confirmed by a text grep on the symbol name — the graph misses dynamic references (string dispatch, templates, reflection) and can be stale. Without a graph, the text grep alone. See `references/HARNESS_MAP.md` § Tooling that may be absent.

### Phase 7 — Close out

1. Re-run **every** `Definition of Done` command, fresh, in one pass. Not the cached results from Phase 3.
2. **Read the whole diff, line by line**, before filling anything in. `git diff` plus `git status` for new files. The DoD checks what someone thought to check; the diff shows what you actually did. A green DoD over a diff nobody read is the failure mode this step exists for — a stray `.parent`, a deleted docstring, a debug print and an inline style all pass every test in the plan. For each changed line, answer: does it trace to a step, and does it obey the convention files read in Phase 3?
3. **Any test added by this plan must pass with no external service running.** Run it with the project's services down. A test that needs a live database, a live API or a network key is an integration test — it belongs behind an explicit marker or a skip, never in the default suite, or the next person's DoD fails for reasons that have nothing to do with their change.
4. Fill `## Code Review` completely — every field gets a value, no blanks.
5. All DoD items pass → frontmatter `status: done`. Any item fails → `status: blocked` with the reason. Write `done` exactly — not `complete` or `completed`; `micro-dev`'s archive sweep matches it literally. Leave the plan folder where it is: archiving is the sweep's job, not this skill's.
6. Final Execution Log line with state `done` or `blocked`.
7. Report to the user: what changed, the DoD output, and what is left.

**Never commit or push.** Staging is the user's call unless they asked for it as part of the task.

## Handoff

Before ending a session with unfinished work — context running out, user stopping, switching harness — leave the plan file resumable:

- No step left at `- [~]` unless you also wrote what state it is in under `## Notes`
- Execution Log up to date with the last real action
- `## Notes` states the next concrete action in one sentence

A plan that satisfies these can be picked up by any harness with no conversation history.

## Red Flags — STOP

- About to write `- [x]` without having just run a command
- "The build passed earlier so this step is fine"
- "I'll clean up the dead code in the teardown step" — no, in the step that created it
- Editing a file that is not in `Surgical Scope`
- Rewriting a plan step to match what you already did
- Adding steps to the plan mid-execution instead of stopping
- Marking `status: done` with an unchecked step anywhere in the file
- Trusting a subagent's "success" report without checking the diff yourself
- Ticking a step on a plan that has no `Definition of Done` to grade it against
- Closing out without having read the diff — a green DoD is not a review
- Adding a test that needs a live database or API to the default suite

## Rationalizations

| Excuse | Reality |
|---|---|
| "The plan is obviously fine, skip the review" | Phase 2 costs one minute. A stale plan costs an hour. |
| "It's a small step, no need to mark `[~]`" | `[~]` is what makes the crash recoverable. It is the whole contract. |
| "I already ran the tests two steps ago" | Two steps ago is not this step. Run it. |
| "The Execution Log is overhead" | It is the only thing the other harness can read. |
| "This one extra file is clearly needed" | Then the plan was wrong. Stop and say so. |
| "I'll fix the remaining failure after marking it done" | Then it is not done. `blocked` is an honest status. |
| "The plan is simple enough, the format doesn't matter here" | Five of seven phases bind to sections by name. Without them you are logging, not verifying. |
| "The plan didn't ask for a docstring / a test / that convention" | The plan is not the only contract. Phase 3 reads the repo's convention files. |
| "The DoD is green, the diff is fine" | The DoD checks what someone predicted. Read the diff — that is where the surprises are. |
| "The user is waiting, just finish it" | A wrongly-`done` plan wastes more of their time than a `blocked` one. |

## Tooling on Claude Code

The plan file is the state, and this machine's hooks assume that. Three
consequences while executing:

- **Search** — pick the tool by what the question is. Natural-language question
  about the code: `mgrep '<question>'` first (paid, and the point of paying).
  Known symbol name: `mcp__token-savior__find_symbol`, exact and free. Code
  shape: `ast-grep -p '<motif>' -l <lang>`. `grep`, `rg`, `find -name` and the
  `Grep` tool are refused until one of those has run in the same turn.
- **Read** — no `Read` over 500 lines without `offset`/`limit`. Locate the zone
  first (`ast-grep outline -l <lang> <file>`), read it after.
- **Compaction** — the context compacts at 200 000 tokens, subagents included.
  The plan file is what survives it. Write `- [~]` and the Execution Log line
  *before* doing the work, not after; that is what makes a mid-step compaction
  or crash recoverable.

Delegating a step to a subagent: `sonnet` covers ordinary implementation and
verification steps. Reserve `opus` for steps whose cost of being wrong is
irreversible — schema migrations, security-relevant edits. A step that is only
running a command and reading its exit code does not need a subagent at all.

## Harness mapping

This skill speaks in actions. See `references/HARNESS_MAP.md` for how each action resolves on Claude Code, Antigravity (`agy`), and Gemini CLI.

## Related

- `micro-dev` — writes the plan this skill executes
- `superpowers:verification-before-completion` — the evidence discipline behind the Iron Law
- `superpowers:systematic-debugging` — when Phase 5 hits an unknown cause
