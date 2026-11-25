---
name: teammode
description: "Parallel subagent orchestration for Antigravity: run multiple cooperating workers to work on a task in parallel. The main session acts as the conductor, managing and coordinating subagents via invoke_subagent. Use when the work is not perfectly isolated but parallelizing helps. Triggers: team mode, teammode, make a team, run as a team, team of agents, parallel threads, archive the team."
---

# Teammode

Run multiple cooperating subagents under one leader session in Antigravity.
This workflow coordinates multiple child agents in parallel using the `invoke_subagent` tool. The main session acts as the leader, defining specific deliverables for each child worker.

## When to use a team (and when to use plain subagents instead)

Use a TEAM when EITHER holds:
- the work does NOT split into perfectly isolated pieces, but doing it in parallel is clearly
  more convenient - members will need to see and react to each other's findings; or
- one task still needs exploration, yet its GOAL is already clear - parallel investigation under
  a fixed objective.

Use plain fire-and-forget subagents (`invoke_subagent` workers) - NOT a team - when
EITHER holds:
- the work IS perfectly isolated, so there is no coordination cost worth paying; or
- the GOAL is still ambiguous, where one mind should resolve direction before any fan-out.

A team buys cross-member coordination at a real overhead cost; only spend it when coordination
is the thing you actually need.

## Antigravity Subagent Coordination (Teammode)

In Google Antigravity, we coordinate subagents using the native `invoke_subagent` tool.
Tell the user in one line which route you are taking:
- `Teammode transport: Antigravity invoke_subagent.`

## You are the leader - orchestrate, do not implement

The main session is ALWAYS the team leader; you orchestrate directly and never spin up a separate
leader worker. Your job is orchestration, NOT writing product code: split the work and assign each
slice, hold live situational awareness of every member, verify and QA what they deliver, relay
findings between members, instruct and unblock, and synthesize the result. DELEGATE every code edit
to a member - if you catch yourself editing product files while the team runs, that work was a
member's slice you should have handed off. You own direction, verification, and integration (the
merge), not the keystrokes.

## Compose by part, ownership, or perspective - not by job title

A team is ALWAYS two or more members - never a single-member team. One worker on an isolated
job is a plain subagent, not a team; if you end up with a single member,
either split off a second distinct slice or drop the team and use a subagent.

Compose the team from what you actually KNOW about the work. Ground the split in real knowledge
of the problem, then divide it into clear, non-overlapping responsibilities - one per aspect of
the work - and give each member exactly one. No two members may own the same thing. Define each
member by a concrete slice: a specific part of the codebase, an ownership area, or a distinct
perspective/lens. Assigning a vague role ("backend dev", "release analyst", "the tester") is an
anti-pattern - it gives the member no real boundary and invites overlap. Each member's `focus`
names what they own concretely; the `lens` is one of `area`, `ownership`, or `perspective`.
Give each member a short, distinct `--name` too - its role or what it watches (e.g.
`app-server-lifecycle`, `mailbox-delivery`) - it labels the member everywhere; never reuse
one name for two members. On MultiAgentV2 teams also give each member a unique
`--task-name` in `lowercase_digits_underscores` form - it becomes the member's permanent
agent path `/root/<task_name>`.

## Run the script - never hand-write team state

A bundled, dependency-free Node script owns all team state so you never author `team.json` or
the member manual by hand. Run it with `node` (or `bun`); it works on macOS, Linux, and Windows.
Replace `<skill-root>` with this skill's own directory.

```
node "<skill-root>/scripts/team.mjs" init        --name "<team>" --session-name "<session>" --transport multi_agent_v2|codex_app [--session <leader_thread_id>] [--worktree] [--base-branch dev]
node "<skill-root>/scripts/team.mjs" add-member  --team <session_id> --id A --name "<short role>" [--task-name <v2_task_name>] --focus "<part/ownership/perspective>" --lens area|ownership|perspective --deliverable "<...>" [--branch <branch>]
node "<skill-root>/scripts/team.mjs" bind-agent   --team <session_id> --id A --agent-path /root/<task_name> [--cwd <path>]   # multi_agent_v2 teams
node "<skill-root>/scripts/team.mjs" bind-thread  --team <session_id> --id A --thread <thread_id> [--cwd <path>]             # codex_app teams
node "<skill-root>/scripts/team.mjs" member-prompt --team <session_id> --id A
node "<skill-root>/scripts/team.mjs" set-status   --team <session_id> --id A --status reported|blocked|active|archived [--note "<...>"]
node "<skill-root>/scripts/team.mjs" worktree-add    --team <session_id> --id A [--base-branch <branch>]
node "<skill-root>/scripts/team.mjs" worktree-remove --team <session_id> --id A [--force]
node "<skill-root>/scripts/team.mjs" integrate       --team <session_id> [--id A]
node "<skill-root>/scripts/team.mjs" archive      --team <session_id> [--id A] [--note "<...>"]
node "<skill-root>/scripts/team.mjs" delete       --team <session_id> [--force]
node "<skill-root>/scripts/team.mjs" status       --team <session_id>
```

`init` creates `.omo/teams/{session_id}/` containing `team.json` (the single durable state file:
team id, transport, the main-session leader, the member roster, status, worktree config, and a
lifecycle log), `guide.md` (the auto-generated member field manual), and `artifacts/` (a shared
exchange space). On codex_app teams `{session_id}` is the leader's Codex session id when you can
pass it via `--session`; otherwise the script generates a stable handle. Re-running `init` is a
safe no-op. Every mutating subcommand rewrites `guide.md`, so the manual always matches the
current team.

Mutating subcommands take a per-team state lock before reading and rewriting `team.json`. It is
safe to run independent `add-member`, `bind-agent`, `bind-thread`, `set-status`, `archive`,
`delete`, `guide`, and worktree mutation commands concurrently against the same team: they
serialize and each command reads the latest committed state before writing. If a command reports
that team state is locked, do not treat the intended mutation as complete; retry after the named
command finishes, or inspect `.omo/teams/{session_id}/.team.lock/owner.json` if the previous
command crashed. `bind-agent` refuses codex_app teams and `bind-thread` refuses multi_agent_v2
teams, and a refused command never changes `team.json`.

## Create the team and its members

In Antigravity, spawn members using `invoke_subagent`:

```typescript
invoke_subagent({
  Subagents: [
    { TypeName: "sisyphus-junior", Role: "<member_A_role>", Prompt: "<member_A_instructions>" },
    { TypeName: "sisyphus-junior", Role: "<member_B_role>", Prompt: "<member_B_instructions>" }
  ]
})
```

1. If a member needs an isolated worktree, run `worktree-add` BEFORE spawning it or pass the worktree path in the bootstrap prompt.
2. Spawn members concurrently via `invoke_subagent`. Capture the returned subagent IDs.
3. Manage active subagents via `manage_subagents` / `manage_task` (action: "list", "status", "kill").

## Communication

Members push to you and to one another; you never poll them as a routine:

- Subagents to orchestrator: `send_message` with the leader's conversation ID as recipient.
- Orchestrator to subagents: `send_message` with the target subagent's conversation ID as recipient.
- Peer to peer: include peer subagent IDs in the bootstrap prompt so members can exchange digests and updates directly via `send_message`.
- Lifecycle management: use `manage_subagents` / `manage_task` to inspect task status or kill completed workers.

All member-to-member and member-to-leader traffic is in English; when the END user addresses a
member, that member replies in the user's own language. Members hand off files and memos
through the team `artifacts/` directory and reference them by path.

## Let members work - do not rush them

Members heartbeat every few tool calls and message you on every finding, blocker, and finished
slice (their manual binds them to this). So a member that is quiet between heartbeats is **working,
not stalled** - a stretch of silence is the normal sound of focused work, not a problem to chase.
Re-reading a calm member's state, or sending "any update?" / "are you done?" / "hurry up" pings,
interrupts that member and slows the whole team. Trust the heartbeat and let them cook.

Message a member only when one of these is true:
- you have new information, context, or a correction it needs to do its slice right;
- you are reassigning, narrowing, or unblocking its scope;
- a peer's result changes what it should do; or
- it has gone fully silent well past its heartbeat cadence AND that stall is blocking the team -
  then send one specific question, not a barrage.

Otherwise stay calm and keep the channel open: read inbound updates as they arrive and act on them.
A long-running member is alive; a heartbeat you have not received yet is not a failure. Fallback only when
a member is completed without its deliverable, explicitly `BLOCKED:`, or no longer running - then
unblock, reassign, or re-task that slice instead of waiting on it. Wait for
every required member's final report before you declare the team done - rushing toward "done" while
members are still mid-slice just produces half-built work you will have to redo.

## Worktrees - isolate members who would touch the same files

The moment two members' slices would edit the same files, give each its own git worktree so they
cannot clobber each other. Decide this whenever you see the collision - at team creation OR mid-run,
not only up front. For each colliding member run `worktree-add --team <id> --id <member>`: it creates
the worktree off the base branch on a derived branch, flips the team into worktree mode, records it in
`team.json`, and prints the `cd` path to hand that member. The member works and commits only inside
its own worktree. To land the work, `integrate --team <id>` merges every member branch into your
current branch with a merge commit (never a squash or rebase); resolve any conflict it reports, then
`worktree-remove` each worktree at cleanup.

Delivering the path differs by transport: on MultiAgentV2, create the worktree BEFORE spawning
so the bootstrap carries it, or send it to an already-running member as a `followup_task`; on
Codex App, send a follow-up message that includes both the worktree path and the member's
`codex://threads/<thread_id>` link. Either way, run `bind-agent`/`bind-thread` with
`--cwd <worktree>` (or `--worktree-path`) so `team.json`, `guide.md`, `status`, and
`member-prompt` all point at the same worktree-backed member.

When the member starts inside a worktree, it must verify the assigned cwd exists and contains the
repository checkout before editing. If the directory is missing, empty, or does not look like a git
worktree/repository yet, the member reports `BLOCKED: worktree not ready` to the leader and waits
instead of editing a parent checkout or an empty directory.

## Run a ulw-plan in parallel

When a decision-complete plan already exists at `.omo/plans/<slug>.md` (from ulw-plan), execute its
parallel waves as a team instead of one todo at a time. Map it directly:
- one wave's independent todos -> one member each; the todo's scope/files become that member's `focus`,
  and its acceptance criteria + QA become the member's `deliverable`.
- the plan's dependency matrix sets the shape: todos with no unmet dependency inside a wave run as
  concurrent members; a todo that depends on another waits, so launch the next wave only after the
  blocking members report.
- todos in the same wave that touch overlapping files -> give those members worktrees (see above).

Keep the plan file as the shared spec: point each member at its todo by path, and verify the member's
result against that todo's acceptance criteria before you integrate.

## Archive, delete, and cleanup

DISBAND the team the moment it is no longer needed. A team exists only to do its work; once that
work is done, or the user no longer wants it, do not leave it lying around - archive every member,
then delete the team state only after archival evidence is clean or preserved. A finished team that
is never disbanded is a leak.

- `archive` closes the team: notify each active member, copy anything useful into `artifacts/`,
  then close each member on its transport. On MultiAgentV2, `interrupt_agent` any member still
  mid-turn and record in the note that V2 exposes no runtime archive operation - the durable
  `team.json` state IS the archive; never claim a V2 agent itself was archived. On Codex App,
  try `codex_app.set_thread_archived` per member thread; treat failures such as
  "Ambiguous Codex thread id" or an id that is ambiguous across hosts as an
  app-thread archival blocker, not as a team-state blocker: record the failure in the team log,
  tell the user which member thread was not proven archived, and continue the team-state archive
  with `archive --note "<blocker>"`. Never pretend a member thread was archived. Do not delete the
  team state after an app-thread archival blocker unless the evidence has been copied elsewhere or
  the user explicitly accepts that evidence loss.
- `delete` removes `.omo/teams/{session_id}` and refuses while the team is unarchived or any member
  is still active unless `--force`.
- When the work wraps up, land it the way the user asked: `integrate --team <id>` for a direct merge
  commit, or push each member branch and open a PR. Then `worktree-remove` each worktree, archive, and
  delete. Cleanup is real work; respect the user's instruction on how to land it.

## Stop rules

- Stop and ask before deleting an unarchived team while any member is still active.
- Member communication stays English unless the user explicitly requests otherwise; user-facing
  replies follow the user's language.
- Stop if the selected transport's tools (V2 spawn/message/wait/list/interrupt, or Codex App
  create/read/send/title/archive) stop working mid-run; say so instead of faking it or silently
  switching transports. Pre-init absence is not a stop - it routes to the plain-subagent split.
- **Refusal is Final**: User refusals (NO, STOP, CANCEL, DENY) and tool/permission blocks are terminal boundaries for that operation. Never attempt workarounds via alternative tools, shell commands, or subagents; acknowledge immediately and report.
