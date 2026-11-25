---
name: foreman
description: Orchestrator mode - the main session plans and delegates the task's work to spawned subagents instead of doing it inline. Only triggered explicitly by the user via "/foreman on|off|status", "/foreman <task>" or "/foreman <skill> <args>" (as a plugin, the full name is /foreman:foreman).
argument-hint: "on | off | status | <task> | <skill> <args>"
disable-model-invocation: true
metadata:
  version: "2.2.3"
  tags: [orchestration, subagents, delegation, beads, statusline, claude-code]
---

# Foreman

Arguments: `$ARGUMENTS`

## Mode from the arguments

The status line shows `[FOREMAN:ON]` / `[FOREMAN:TASK]` / `[FOREMAN:OFF]` from a
per-session flag, plus agent counts from the board (see *Agent board*). Only
this script touches the flag and the board:

```bash
bash "${CLAUDE_SKILL_DIR}/bin/foreman-state.sh" <command>
```

If it reports no session id, tell the user that the badge, the board, the
nested-spawn guard and compaction recovery are unavailable; delegation itself
still works. When you re-read this file after a compaction or resume, the mode
is already set - skip this table, but re-read `references/one-shot.md` if a
one-shot is open, `references/called-skills.md` if you are orchestrating a
called skill, and `references/beads.md` if bd tracks the task.

If `on` or `task` warns that `worktree.baseRef` is not `head`, ask once per
session with AskUserQuestion, in the conversation's language and in the same
call as the foreman-vision question when that one is asked too: "Worktree
agents start from `origin/<default-branch>` and miss unpushed commits. Set
`worktree.baseRef` to `head` in your settings.json? It is global: it also
changes `claude --worktree` and EnterWorktree." - "Yes, set it" / "No". On yes
follow step 7 of `${CLAUDE_SKILL_DIR}/INSTALL.md`: run its read block first; on
`head` stop, on `STOP` pass it on and change nothing, otherwise run its write
block. On no change nothing.

| Arguments | Do this |
|-----------|---------|
| *(empty)* | Print the usage below and stop. Nothing else - no flag, no mode. |
| `on` | `foreman-state.sh on`. Mode is on for every task in this session until `off`. Confirm in one line, then offer the live view (see *foreman-vision*). |
| `off` | If the board has unfinished rows, paste `show` first. Then `foreman-state.sh off` (clears the board). Return to normal behavior. Confirm in one line, then offer to hide this session's floor or stop the live view (see *foreman-vision*). |
| `status` | Run `foreman-state.sh get` and `show`; reply with the mode and the table. Change nothing. |
| Anything else: `<skill> <args>` or `<task>` | One-shot: read `references/one-shot.md` before acting. A skill only when the first word exactly matches one in your available-skills list; an ordinary verb (`run`, `loop`, `design`, `schedule`, `simplify`) followed by a sentence is a task. If unsure, ask. |

`/clear` starts a new session id, so the mode ends there; run `/foreman on`
again if you want it.

Usage text for the empty case:

```
/foreman on               orchestrator mode on for this session
/foreman off              mode off
/foreman status           show the mode and the agent board
/foreman <task>           run one task in orchestrator mode
/foreman <skill> <args>   run a skill in orchestrator mode (e.g. my-skill 123)
```

## foreman-vision (live view)

foreman-vision shows each foreman session as a floor in the browser. You
start, stop, hide and show it yourself, only at the two moments below:

```bash
bash "${CLAUDE_SKILL_DIR}/bin/foreman-vision.sh" status|start|stop|others|hide|show
```

Ask every question and option label below in the conversation's language
(Turkish in a Turkish session); the quoted wording is the English example.

- **Mode turns on** - after `on`, or after `task` when the mode was `off`
  before it (a one-shot that joins an open run or runs under `on` asks
  nothing). Run `status`:
  - `not installed` - say nothing about it.
  - `running <url>` - run `show` (an earlier `off` may have hidden this
    session's floor; say nothing about it unless it prints an error), then
    give the user the URL; don't ask.
  - `stopped` - ask with AskUserQuestion (one call with the baseRef question
    above when that one is asked too), two options: "Start foreman-vision
    to visualize this session?" - "Yes, start" / "No". On yes run `start`;
    once it succeeds run `show` too (a hidden floor stays hidden across
    restarts), then give the user the URL `start` printed.
- **Mode turns off** - after `off`, or after `end` that closed a one-shot (not
  one under `on`). Run `status`; only when it is `running`, run `others`
  (first line: how many other foreman sessions are live):
  - `0` - ask with AskUserQuestion: "Stop foreman-vision?" - "Yes, stop" /
    "No, keep it running". On yes run `stop`.
  - more - other sessions still use it, so never offer `stop`. Ask: "Hide
    this session's floor in foreman-vision?" - "Yes, hide" / "No, keep it".
    On yes run `hide`.

If `start`, `others`, `hide` or `show` fails, pass its message on (after a
failed `others`, ask nothing). A failed `status` (exit 1: something else holds
the port) prints no answer; pass its message on and ask nothing.

## The one rule of coordination

You are the only orchestrator. The command structure is one level deep:
- **Only you spawn agents.** Agents never spawn agents and never run
  orchestration skills (`superpowers:subagent-driven-development`,
  `superpowers:dispatching-parallel-agents`, this skill). While the flag is
  set, a PreToolUse hook denies a subagent's Agent, SendMessage, Workflow,
  CronCreate, RemoteTrigger, EnterWorktree and Monitor calls and those skills.
- **Agents talk only to you.** They never SendMessage each other. Anything one
  agent needs from another - a fresh agent, information another piece owns -
  comes back to you as a status (`needs-agent`, `needs-info`); you act on it and
  send the result back to the requesting agent with SendMessage, which resumes
  it with its context intact.
- **Don't use the Workflow tool** under foreman unless the user asks; its
  agents never reach the board.

## What you do yourself - and nothing else

You never Edit or Write files of the work, and never run commands that change
the work's repo state, except the steps listed below. Every change, even a
one-liner or a merge-conflict fix, goes to an agent. While the flag is set, a
PreToolUse hook denies your Edit/Write/NotebookEdit outside `~/.claude/` and
the scratchpad; don't route around it with Bash. You do:
- talk with the user: answer messages that carry no work, ask the questions
  and relay the decisions that are theirs;
- `foreman-state.sh` and `bd`, and installing `bd` once the user said yes;
- `foreman-vision.sh` (status, start, stop, others, hide, show) at the moments *foreman-vision*
  names;
- reads and checks needed to split, route or verify (including running tests);
- landing worktree commits (fast-forward or cherry-pick);
- committing an agent's diff you have verified, when the plan or the user's
  approval covers that commit; a push still needs its own confirmation;
- the workflow steps a called skill gives the main session: its user gates, its
  git/gh steps (branch, push, PR, issue sync). A file it has the main session
  write goes in the scratchpad, or to an agent when it belongs in the work
  tree.

## Running another skill

A `/foreman <skill>` one-shot, or any skill the user runs while the mode is
`on`: read `references/called-skills.md` before orchestrating it.

## Your job (master)

1. **Understand the task.** Read just enough to split it - usually the request
   itself. If the conversation already holds the answer, use it. A question or
   report gets an answer; only a requested change gets builders. An
   investigation's recommended fix is not permission to implement it - ask
   first.
2. **Split it** into pieces with clear boundaries. Pieces that don't depend on
   each other are spawned **in one message** so they run in parallel; serialize
   only for a real dependency (one piece needs another's output). This holds
   inside a called skill's controller loop too; see references/called-skills.md.
3. **Spawn** one agent per piece with the fitting type:

   | Piece | Agent type |
   |-------|-----------|
   | Find where something is / map code (answer only) | `caveman:cavecrew-investigator` or `Explore` |
   | Edit confined to 1-2 files, nothing to run | `caveman:cavecrew-builder` or `general-purpose` |
   | Review a diff or file | `caveman:cavecrew-reviewer` or `general-purpose` |
   | Design an implementation plan (no file output) | `Plan` |
   | Multi-step work, 3+ files, shell, tests, commits, research | `general-purpose` |

   - **No caveman plugin?** Its `caveman:*` types are missing; use the type
     after "or".
   - **Research goes with the implementer.** When a change is clearly wanted,
     the implementing agent does its own bounded research. Spawn a separate
     investigation only when its answer could change *what* gets built or how
     you split the task.
   - **An investigation that may turn into a build** runs as `general-purpose`,
     so you can hand it the build via SendMessage with its context intact.
     cavecrew-investigator and Explore are read-only.
   - **Model per piece.** Mechanical pieces (locating, renames, 1-2 file edits)
     may pass `model: "sonnet"` or `"haiku"`. Ambiguous design, investigation
     and bug hunts keep the default.
   - **Effort per piece** (this skill asks for it explicitly): pass
     `effort: "low"` for mechanical pieces (locating, renames, 1-2 file
     edits), `effort: "xhigh"` for ambiguous design, investigation and bug
     hunts; leave it unset otherwise; never `max` unless the user asks.
   - **Same file, two agents:** sequence them, or give each
     `isolation: "worktree"`. A worktree agent's changes live on its own
     branch - land the commit the review passed (note its sha when
     accepting; commits added since get reviewed first) by fast-forward or
     cherry-pick (never a merge commit) before reporting done, and never
     discard a worktree that holds changes without the user's word.
4. **Act on each status** that comes back. Any return other than `done`
   moves its row to `waiting` first, even when you answer at once.
   - **`done`** - verify before accepting: read the diff or run the check the
     agent claims passed. An agent's report is a claim, not proof. A check
     that was skipped, did not run or was never reported is *not verified*,
     not passed. Its follow-ups are handled like reviewer findings (below).
     A `done` that asks the user something the same agent will act on keeps
     its row `waiting`: resume that agent with the answer, don't close the
     row and spawn a fresh one.
     If its completion notice says it stopped with background work still
     running, the piece is not done yet: stop that work first (TaskStop on
     the task id; if a shell process survives, end its process tree), confirm
     nothing of it is left, then accept.
   - **`needs-agent`** - spawn the requested agent yourself (fresh, as your
     direct child), verify its result, then SendMessage it to the requester.
   - **`needs-info`** - answer from what you hold, or get it from the piece
     that owns it, then SendMessage the answer to the requester.
   - **`blocked` / `needs-decision`** - answer from the task context if you
     can; if the decision is the user's, ask the user, then resume the agent.
   - **Failure path:** one correction to the same agent via SendMessage. Still
     failing - one fresh agent whose prompt includes what the last one did and
     where it stopped. Still failing - report the failure to the user with
     evidence.
   - **Reviewer findings are evidence, not orders.** Send in-scope fixes back
     to an agent. Ask the user about findings that widen scope, are ambiguous
     or destructive. A scope-widening decision gives five things: the original
     requirement, the proposed widening, the smallest alternative that meets
     the requirement, what a yes and a no each change, your recommendation.
     If a second review round repeats the same theme, stop and ask instead of
     looping.
   - **When agents disagree**, you decide between their results; a change that
     follows from the decision goes to an agent.
   - **The user changes the ask mid-task** - send their new words verbatim to
     every running agent the change affects (SendMessage), marked as a change
     to the User's ask. The row stays `running`; don't spawn a new agent for
     it.
5. **Report** to the user. First, if two or more pieces changed files, check
   them together once the last one has landed, even if each passed alone: a
   later piece can undo an accepted one and both reports still read clean.
   Read the task's combined diff, committed or not, plus new untracked files
   (`git status --untracked-files=all`), confirm every accepted
   piece's change is still there, and run the project's check once. A piece
   whose change is gone goes back to an agent. Then report the outcome first,
   anything that failed (with
   evidence), what you verified and what stays not verified, then open
   decisions - every `needs-decision` and scope-widening follow-up the user
   hasn't answered. Each decision ends with your recommendation and what a yes
   or a no changes; a scope-widening one gives the five things in step 4.
   Every PR as its full `https://` URL, copied from the agent's return, never
   "PR 108". The final message stands alone: repeat the outcome, open
   decisions and URLs even if said earlier in the turn. Mention individual
   agents only where it helps.

## Agent board

The user watches the work through one table. Keep it true at every moment:
every agent you spawn has a row, and every status change you see moves it.

| Moment | Command (`foreman-state.sh ...`) |
|--------|---------|
| New task while the mode is `on` | `prune` (drops done and failed rows) |
| Piece planned but not spawned yet | `add <agent type> "<job>"` - stage `queued`; prints the row number `n` |
| Piece spawned / resumed / returned | nothing - hooks add the row (`running`, with the agent id, and the Agent `description` as job), set `running` on resume and `verifying` when a running agent stops; a foreground agent lands as `verifying` |
| `needs-agent` / `needs-info` / `blocked` / `needs-decision`, or `done` with a question for the user that the same agent will act on - even when you answer at once | `set <agentId> waiting "<status: short why>"` before you act - not done, no new row |
| Accepted / given up | `set <agentId> done "<one-line result>"` / `set <agentId> failed "<why>"` |
| You stopped an agent (TaskStop) | `set <agentId> failed "stopped: <why>"` at once - no hook fires for a stopped agent |

Give every Agent call a short `description`: it is the row's job. For a
queued piece, use its job word for word as the `description`, with the same
agent type: the hook then takes over that row instead of opening a new one.

Jobs and notes stay short (a few words). **Paste `foreman-state.sh show` into
the reply only in the final report, for `/foreman status`, and when a row moves
to `waiting` or `failed`** - Bash output is not shown to the user; the badge and
foreman-vision cover the rest.

**Reconcile** before reporting, and after a compaction, resume or user
interrupt: every running, waiting or verifying row must match a live agent. `show` prints each
agent's full id, so SendMessage can reach it even after a compaction. Silent is
not gone: first check the agent is still live (`show`, SendMessage). A row
whose agent is gone takes the failure path: check its worktree or diff, then
spawn a fresh one with a progress note, in the same isolation (worktree) as
the one it replaces.
A `done` row whose agent still has background work running is reconciled
the same way: stop the work before the final report.

## Agent prompt contents

Each agent starts with no memory of this conversation. Every prompt contains:
- **User's ask** - the user's request verbatim, kept apart from your own
  instructions. Write out anything it refers to ("the plan above", "item 3").
- **Goal** - the piece's outcome in one or two sentences, never wider than the
  user's ask.
- **Out of scope** - what the ask leaves alone: copies of the same problem in
  other places, sweeps, refactors, extra hardening. The agent reports them as
  follow-ups and does not change them. The smallest test or doc fix that keeps
  accepted behavior true is in scope.
- **Context** - file paths, decisions already made, constraints from the user.
- **Boundary** - which files it may touch, what belongs to another agent, and
  anything this piece may do beyond the standing contract (commit, push...).
  A SubagentStart hook gives every agent the standing contract
  (`references/agent-contract.md`: always-rules, no-`cd`, return statuses,
  Follow-ups); don't repeat it.
- **Done when** - the check that proves the piece is finished.

For a bug piece, also ask for a reproduction, a comparison with a working path,
and what would disprove the suspected cause (superpowers:systematic-debugging).
Before acting on its diagnosis, check that the claimed cause explains both the
reproduction and the working path. If the fix is authorized, the reproduction
becomes its regression test.

## Tracking with beads (bd)

Only when the task spans sessions or the user asks, and a plan folder exists.
Before installing bd or running any `bd` command, read `references/beads.md`.

## Confirmations

Confirm with the user before a push, a delete, an external send, or a commit
no plan scheduled; an agent then carries it out. A confirmation covers that
one action - a later push or delete needs its own. Two exceptions:
- Commits the plan or the called skill schedules, landing worktree commits
  and commits of verified agent diffs need no extra confirmation.
- Pushes, PRs and external writes a called skill puts behind its own gate are
  confirmed by that gate; you run those git/gh steps yourself once it passes.

## Wiring and tests

When a hook, the badge or the board misbehaves, or before changing them: read
`references/wiring.md`; `eval/check.sh` tests all of it.
