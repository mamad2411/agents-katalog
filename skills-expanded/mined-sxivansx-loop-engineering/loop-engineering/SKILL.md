---
name: loop-engineering
description: Use when the user wants to "set up a loop", build a self-running or run-until-done agent, automate a recurring engineering task (triage, keep-CI-green, dependency bumps, backlog burndown), or stop hand-prompting an agent turn by turn. Sets up an autonomous engineering loop in the current project. It discovers work, runs a maker agent and a separate checker agent, records state on disk, and re-triggers until a verifiable stop condition is met.
argument-hint: [what the loop should do]
---

# Loop Engineering

Set up a loop: an autonomous system that prompts the agent so you don't have to. You define the goal and the stop condition once; the loop finds work, does it, checks it, writes down what happened, and runs again until the goal is met. This skill stands that loop up inside your existing project: it reads how you already test, build, and track work, then fits the loop to your conventions instead of imposing generic ones.

A loop is built from six primitives. Set up only the ones the goal needs.

| Primitive | Role in the loop | Claude Code mechanism |
|---|---|---|
| **Trigger** | starts each cycle, on a schedule or an event | `/goal` (work across turns until a condition is met), `/loop`, scheduled tasks, hooks, GitHub Actions |
| **State** | the loop's memory between cycles, on disk | a markdown file (`LOOP.md`) or an issue tracker via MCP |
| **Discovery** | finds what to work on this cycle | a triage step that reads CI, issues, diffs, a queue |
| **Maker** | does one unit of the work | a subagent in `.claude/agents/` |
| **Checker** | verifies the maker, independently | a *different* subagent in `.claude/agents/` |
| **Stop condition** | the rule that ends the loop | a verifiable check the checker runs |

For any loop that runs unattended, add a **monitor**: an oversight agent that watches the loop as a whole and halts it on drift (going off-goal), spinning (no net progress), or a crossed bound (too many cycles, too long). The maker and checker keep each item correct; the monitor keeps the whole loop pointed at the goal, so it cannot quietly wander off and run for hours.

Two more optional add-ons: **worktrees** (`git worktree`) isolate parallel makers so they don't edit the same files, and **MCP connectors** let the loop touch real tools (open a PR, update a ticket, post status). Add them when the goal needs parallelism or external side effects.

## Setup procedure

This runs inside an existing project. Follow these steps when invoked. Confirm with the user before anything with side effects: scheduled jobs, pushes, ticket writes, deploys.

1. **Read the project first.** Before scaffolding anything, learn the repo: how it runs tests, build, and lint (check `package.json`, `Makefile`, CI config, `CLAUDE.md`); what conventions and existing skills or `.claude/agents/` it already has; and where work comes from (CI, an issue tracker, a backlog, a queue). The loop has to fit this project. Reuse its real commands and conventions, don't invent new ones.

2. **Pin the goal and the stop condition.** Ask the user for the loop's one goal and the *verifiable* condition that means done (tests exit 0, the queue is empty, zero failing checks). A loop with no stop condition is the one thing you must never ship. If the user can't name one, set a bounded fallback (stop after N cycles) and say so out loud. In Claude Code, `/goal <condition>` makes this executable: Claude keeps working across turns until the condition is met, and `/goal clear` ends it early. Copy `${CLAUDE_SKILL_DIR}/templates/stop-check.sh` into the repo and fill it with that exact command — the runner runs it to confirm the model's `CYCLE: complete`, so "done" is a command that exits 0, never the model's own say-so.

3. **Write the state file.** Copy `${CLAUDE_SKILL_DIR}/templates/LOOP.md` to the repo root and fill in goal, stop condition, cadence, and the human gate. Record the verification surface in its `**Verification surface:**` field — the test dirs, CI config, and check commands found in step 1 — so the checker can auto-reject any change that touches them without being named as the item. Ask the user for the commit policy and record it in the `**Commits:**` field (e.g. the checker commits each verified item; never pushes) — unattended commits are a side effect the user must consent to once, here, not per cycle. Its `**Status:**` line (`active | paused | halted`) is the loop's on/off switch: every agent checks it first and stands down unless it says `active`. The monitor halts by flipping it; the human pauses or resumes by editing it (or with `/sync-loop pause|resume`). Its living sections: `## Open` (found, not done), `## Done` (with the evidence that verified it), `## Blocked` (needs a human), `## Discovery` (how Open gets refilled), `## Cycle log` (one line per cycle — the loop's clock), `## Sync log` (written by `/sync-loop`), plus `## Rules`, the standing instruction set every agent in the loop follows. The loop reads this file first every cycle and writes it last. Copy `${CLAUDE_SKILL_DIR}/templates/lint-loop.sh` into the repo too; `/loop-cycle` runs it at the top of every cycle, so a malformed state file — a `## Done` line with no evidence, an illegal `**Status:**`, an unparseable `## Cycle log` line — fails a command the day it happens instead of rotting silently in the history. Keeping the map true is the hard part of loop engineering; this makes "is it still true?" a check, not a vibe.

4. **Create the maker subagent.** Copy `${CLAUDE_SKILL_DIR}/templates/loop-maker.md` to `.claude/agents/loop-maker.md` and point it at the conventions and test command you found in step 1. It does exactly one item from `## Open`, follows the project's existing skills and conventions, and never marks its own work done. If a file by that name already exists, update it rather than overwriting blindly.

5. **Create the checker subagent.** Copy `${CLAUDE_SKILL_DIR}/templates/loop-checker.md` to `.claude/agents/loop-checker.md`. It is a different agent from the maker, it runs the project's actual verification (the real test, build, or lint command from step 1, not a description of it), and it is the only agent allowed to move an item to `## Done`. Its frontmatter `tools:` allowlist (no Write) keeps it a verifier rather than a second maker — hardening plus a clear contract, not hard enforcement, since Bash can still write; the checker's independence ultimately rests on it never being the agent that made the change.

6. **Create the monitor subagent (recommended for any unattended loop).** Copy `${CLAUDE_SKILL_DIR}/templates/loop-monitor.md` to `.claude/agents/loop-monitor.md`, and record how often it runs in `LOOP.md`'s `**Monitor cadence:**` field (e.g. every 3 cycles) — "due" is computed against `## Cycle log`, the one-line-per-cycle record the checker appends, which is also what makes Bounds and every-N-cycles review cadences countable at all. It watches the loop as a whole rather than any single item: it checks whether the loop is still converging on the goal, and it halts the loop and escalates to a human on drift (work that does not serve the goal), spinning (no net progress, items bouncing between Open and Blocked), or a crossed bound. This is what stops a loop from quietly wandering off and running for hours.

7. **Set the code-review and security-audit cadence (ask the user).** Ask how often the loop should run each, and record both in `LOOP.md`. Offer clear options and always include **never**:
   - **Code review** (`/code-review`): every change, before each PR or merge, every N cycles, weekly, or never.
   - **Security audit** (`/security-review`): every change, before each PR or merge, weekly, monthly, or never.

   At the chosen cadence the loop runs that built-in pass and files what it finds into `## Open` as new work items, so the maker fixes them and the checker verifies the fix. If the user picks never, skip that pass entirely and record `never` in `LOOP.md` so the loop does not reintroduce it.

8. **Install the two commands.** Copy `${CLAUDE_SKILL_DIR}/templates/loop-cycle.md` to `.claude/commands/loop-cycle.md` and `${CLAUDE_SKILL_DIR}/templates/sync-loop.md` to `.claude/commands/sync-loop.md`.

   `/loop-cycle` is the canonical cycle — the single on-disk definition of status gate → orient → refill → maker → checker → monitor-if-due → state written. Every trigger runs cycles by invoking it, so no trigger improvises its own version of the loop. It ends with a machine-readable `CYCLE: <outcome>` line that script wrappers grep. Offer (user-confirmed, since it edits a host-project file) to append one line to the project's `CLAUDE.md`: "This repo runs an engineering loop — read `LOOP.md` first; do nothing if its Status is not active."

   `/sync-loop` is the user's re-entry point: when they come back to the project they run `/sync-loop`, get a plain-language catch-up (what reached Done with evidence, what's Blocked and what questions need answering, what's still Open, how the loop tracks against its bounds), and then the loop resumes on the next open item through the normal maker → checker cycle. Each sync appends a dated entry to a `## Sync log` in `LOOP.md` so the next sync knows where to diff from.

9. **Define discovery.** Fill `LOOP.md`'s `## Discovery` section with the triage step that refills `## Open` from where this project's work actually lives (CI status, open issues, recent commits, a work queue): the exact commands or sources to scan, and how findings become discrete, individually checkable items sized to one cycle each. Keep its dedupe rule intact — new findings are checked against Open, Blocked, and Done, and a Done match re-enters as an explicit regression item. Discovery lives on disk like every other primitive; a discovery that exists only in this setup conversation is lost by the next session. Make it deterministic wherever you can.

10. **Choose isolation.** Two kinds, decided separately:
   - **Branch isolation** — for any loop whose items produce commits: the loop never commits to the default branch. One branch and one PR per item (or per logical batch, to avoid PR spam); the human gate becomes concrete as PR review. Mandatory for unattended triggers; default but overridable when the user is in-session, since they are already the gate. On hosted platforms, turn on branch protection with required CI checks — that makes CI a third verifier that neither the maker nor the checker can write to.
   - **Worktrees** — only if more than one maker runs per cycle: give each its own `git worktree` and branch so they never write the same code file. One worktree per item — and one writer for state: only the coordinating session edits `LOOP.md`; parallel makers report their results back and never touch it, or every branch rewrites the same file and the merge conflicts are guaranteed.

11. **Wire connectors (optional).** If the loop must open PRs, update tickets, or post status, connect the matching MCP server. Otherwise the loop's output stays local and a human relays it.

12. **Set the trigger.** Pick the lightest mechanism that fits the cadence:
   Whatever fires, the cycle it runs is `/loop-cycle` — the trigger chooses *when*, never *what*.

   - run until the goal is met, in this session → `/goal <stop condition>` (Claude runs `/loop-cycle` across turns until the condition is true; `/goal clear` ends it early)
   - repeat on a cadence, on demand → `/loop /loop-cycle`
   - periodic and unattended → a scheduled task whose prompt is `/loop-cycle`, or the shipped runners: copy `${CLAUDE_SKILL_DIR}/templates/loop.sh` (cron / local: fresh `claude -p "/loop-cycle"` context per iteration, hard iteration cap, Status grep, run log) or `${CLAUDE_SKILL_DIR}/templates/trigger-github-action.yml` to `.github/workflows/loop.yml` (schedule + manual dispatch, concurrency group, timeout, minimal permissions)
   - react to an event (push, PR, file change) → a hook or a GitHub Action invoking `/loop-cycle`

   The unattended doctrine, regardless of mechanism: **one cycle = one fresh context** — `LOOP.md` and git are the loop's memory, never the conversation; and **bounds are enforced twice** — mechanically in the trigger (iteration caps, `--max-turns`, `timeout-minutes`) and semantically by the monitor. Never by the monitor alone: a dumb outer cap stops the runaway that talks its way past every smart guard.

   **Unattended means isolated.** A trigger with no human attached runs with auto-approved tool use, and its discovery reads attacker-influenceable text (CI logs, issue bodies) — that combination on a raw machine is how credentials leave. Match the isolation to the trigger: CI runners and hosted scheduled agents already run on isolated machines; a local cron or scheduled task gets the sandboxed Bash tool or a devcontainer with an egress allowlist. Everywhere: repository-scoped short-lived tokens, no mounted `~/.ssh` or long-lived cloud credentials, and never `--dangerously-skip-permissions` outside such isolation. Isolation reduces the blast radius; it does not make an unattended loop safe — the human gate from step 10 stays.

   Confirm with the user before creating any scheduled job. For script-wrapped triggers (cron, GitHub Actions), gate the run on the Status marker before any tokens are spent: `grep -q '^\*\*Status:\*\* active' LOOP.md || exit 0`. (In-session triggers can't pre-grep; their Status check is the first instruction the agents run.)

13. **Dry-run, verify, then enable.** Run one cycle by hand. Read everything it produced. Confirm the checker actually blocks bad output and that state was written. Only then turn on the trigger.

## Guardrails (non-negotiable)

- **The checker is never the maker.** The agent that wrote the code does not get to declare it correct.
- **The stop condition is verifiable, not vibes.** "Looks done" is not a stop condition. A command that exits 0 is — and the runner runs that command (`stop-check.sh`) to confirm the model's `CYCLE: complete`, rather than trusting the model to declare itself done. The one gate the whole loop rests on is the one gate the model must not adjudicate.
- **State is written every cycle.** If the loop forgets what it tried, it repeats itself. The model forgets; the file does not.
- **A human gate stays on anything irreversible.** Shipping, deploying, deleting, spending money. The loop drafts, a person confirms. An unattended loop makes unattended mistakes.
- **Blocked beats guessing.** When the loop can't verify or can't proceed, it writes to `## Blocked` and stops that item. It does not ship a guess.
- **A long loop is watched and bounded.** Any unattended loop runs with a monitor and a bound. If it drifts off the goal or runs past the bound, the monitor halts it and escalates. A loop never gets to run forever in the wrong direction.
- **A rule that exists only as prose is a suggestion.** Agents under pressure do what passes the check, not what the sentence asked (agents have been measured editing tests they were explicitly forbidden to touch). Anything the loop must *never* do deserves a deterministic guard, not another sentence — which is why the checker audits the diff against the verification surface instead of trusting the rule that says "don't touch tests".

### Optional hard enforcement (recommended for unattended loops)

The templates enforce invariants by process (separate checker, diff audit, Status gate). To make the must-nevers mechanical too:

- **Per-agent hooks:** a `hooks:` block in an agent's frontmatter (works for project `.claude/agents/` copies — plugin-distributed agents ignore it) can run a PreToolUse script that exits 2 to block the call. Typical guards: the maker editing `## Done`, the `LOOP.md` header, or anything in the verification surface. Match `Bash` too, not just Edit/Write, or `sed -i` walks around the guard.
- **Permission deny rules:** for actions *no* agent may take (force-push, deploy, destructive database commands, spending), add `permissions.deny` rules in the project's `.claude/settings.json` — session-wide, deterministic, and visible in review.
- **Platform guards:** branch protection plus required CI checks give an unattended loop a verifier that no agent in the loop can write to at all.

## What the loop looks like once it's set up

```
your-project/
├── LOOP.md                   # goal, stop condition, bounds, rules, Open/Done/Blocked
├── stop-check.sh             # the stop condition as a command — the runner runs it to confirm "done"
├── lint-loop.sh              # asserts LOOP.md is structurally true — run every cycle
├── .claude/
│   ├── agents/
│   │   ├── loop-maker.md      # does one unit of work
│   │   ├── loop-checker.md    # verifies it, independently
│   │   └── loop-monitor.md    # watches the whole loop for drift + runaway
│   └── commands/
│       ├── loop-cycle.md      # /loop-cycle: the one definition of a cycle, invoked by every trigger
│       └── sync-loop.md       # /sync-loop: catch the user up, then resume the loop
└── (trigger: /goal, /loop, a scheduled task, or a GitHub Action)
```

## Anti-patterns: do not ship these

- A loop with no stop condition (runs forever, burns tokens).
- One agent that writes and grades its own work.
- A loop with no state file (re-derives everything, repeats work, forgets what failed).
- An unattended loop with no monitor or bounds (drifts off-goal and runs for hours before anyone notices).
- An unattended loop outside isolation — auto-approved tools on a raw machine with mounted credentials, or committing straight to the default branch.
- Unattended shipping with no human gate on irreversible actions.
- One loop carrying many unrelated jobs. One loop, one goal, one stop condition. Split the rest into their own loops.

## Files in this skill

- `templates/LOOP.md`: the state file to copy into the target repo.
- `templates/loop-maker.md`: the maker subagent definition.
- `templates/loop-checker.md`: the checker subagent definition.
- `templates/loop-monitor.md`: the monitor subagent definition (drift and runaway guard).
- `templates/loop-cycle.md`: the `/loop-cycle` command to copy into the target repo — the canonical single-cycle definition every trigger invokes.
- `templates/sync-loop.md`: the `/sync-loop` command to copy into the target repo — the user's re-entry point after time away (catch-up summary, then resume).
- `templates/stop-check.sh`: the stop condition as a runnable command; the runner executes it to confirm `CYCLE: complete` instead of trusting the model's word.
- `templates/lint-loop.sh`: structural linter for `LOOP.md` (Status legal, Done lines carry evidence, cycle-log lines parse) — run every cycle and in CI so the state file can't drift stale unnoticed.
- `templates/loop.sh`: fresh-context-per-iteration headless runner for cron or local unattended loops, with mechanical bounds.
- `templates/trigger-github-action.yml`: scheduled GitHub Action that runs one cycle per run, gated on Status.
- `examples/keep-ci-green.md`: a complete worked loop, from goal to trigger.
