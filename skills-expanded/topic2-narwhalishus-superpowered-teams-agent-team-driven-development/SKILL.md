---
name: agent-team-driven-development
description: Use when executing a team-format implementation plan (produced by writing-plans-for-teams) — orchestrates a team of persistent specialist agents working in parallel with two-stage review after each task.
---

# Agent Team-Driven Development

Execute a team-format plan by orchestrating a team of persistent teammates (Agent Teams) with two-stage review (spec compliance then code quality, via one-shot subagents) per task, hybrid task assignment (lead-assigns Wave 1, teammates self-claim thereafter), and structured journal data captured in task records.

**Core principle:** Wave-based parallel execution + persistent specialists + two-stage review + self-claim after calibration = fast delivery, high quality, scalable lead (main-session orchestrator) bandwidth.

**Announce at start:** "I'm using the agent-team-driven-development skill to execute this plan."

**Requires:** Agent Teams primitives available in the running Claude Code — `TeamCreate`, `SendMessage`, `TaskCreate`, `TaskGet`, `TaskUpdate`, `TaskList`. See § Compatibility for the configuration this skill was authored against.

## Compatibility

CC-coupled assumptions live here. Update this section when any of these change; the rest of the skill should reference them rather than embedding values inline.

| Assumption | As-of authoring | Brittleness |
|---|---|---|
| Experimental flag enabling Agent Teams | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in user settings | May be renamed or graduated out of experimental |
| Minimum Claude Code version | 2.1.32 hard floor (Agent Teams introduced); 2.1.147 recommended (so `CLAUDE_CODE_SUBAGENT_MODEL` reaches teammate processes) | Tool surface and tool names may evolve |
| Model tier (all roles: lead, teammates, reviewers) | Frontier Opus-tier with ≥1M-token context (Opus 4.8-1M at writing) | Newer Opus-family models will likely be available; pick the most capable in the same tier |
| Team config path | `~/.claude/teams/<slug>/config.json` | Documentation only — skill behavior does not depend on reading this file |
| Task-record metadata fields used for dispatch | `metadata.report_ready`, `metadata.status_code`, `metadata.concerns` | If CC's `TaskUpdate metadata` schema changes, Phase 3 dispatch logic must move with it |

If a required primitive is unavailable at boot, halt and direct the user to `update-config` for settings edits. If a flag has been renamed or graduated, update this section before editing the rest of the skill.

## When to Use

Companion-skill names in this skill (`writing-plans`, `subagent-driven-development`, `finishing-a-development-branch`, `test-driven-development`, `requesting-code-review`) are unprefixed: resolve each to your local skill of that name, or its superpowers-plugin equivalent (`superpowers:<name>`) if that is where yours lives.

- Plan was written by `writing-plans-for-teams` (blockquote verifies this)
- Tasks have identifiable independence across at least 2 waves
- 4+ tasks total
- 2+ distinct specialist roles

**Don't use when:**
- Plan was written by `writing-plans` (use `subagent-driven-development` instead)
- Plan is serial or tightly coupled (fitness check should have routed you elsewhere)
- The work is mechanical fan-out over independent units with no inter-agent deliberation (map/reduce, parallel verify, schema-forced extraction). That is Workflow-shaped: use the `Workflow` tool, not a team. This skill is the persistence and deliberation primitive; the two compose (a Workflow can call this plugin's `superpowered-teams:code-reviewer` agent), but team orchestration is lead-session-driven, not workflow-driven. Under ultracode, a session may author such a Workflow by default; that does not replace this skill for genuine team-shaped plans.

## Team Structure

All roles run on the same model tier — see § Compatibility for the tier specification and currency policy.

| Role | Count | Spawn mechanism | Persistence |
|---|---|---|---|
| Lead (you) | 1 | Main session | Session |
| Implementation teammate | 1–3 simultaneous | `Agent` tool with `team_name` + `name` | Spawn-per-wave default, upgrade to full-session if ≥2 waves of work |
| Spec reviewer | Per task | `Agent` tool, no `team_name` | One-shot |
| Code quality reviewer | Per task | `Agent` tool, `subagent_type: superpowered-teams:code-reviewer` | One-shot |
| Final cross-cutting reviewer | 1 | `Agent` tool, `subagent_type: superpowered-teams:code-reviewer` | One-shot at completion |

Implementation teammates are persistent (survive across waves, remember codebase). Reviewers are one-shot subagents (fresh context, no bias from watching code get written). The asymmetry is deliberate.

**Max 3 simultaneous teammates.** More hits diminishing returns — git conflicts, coordination overhead.

Max 3 simultaneous teammates total across all roles. Do not spawn two teammates of the same role to parallelize within a single wave — if two same-role tasks are in one wave, the role's single teammate does them in sequence (which means those tasks belong in separate waves; the plan's fitness check and wave rules should prevent this configuration).

## Tool Call Conventions

A few patterns repeat across the skill:

- **`SendMessage` with structured message:** When sending protocol messages like shutdown requests, the typed object is the value of `message:`, not a top-level field. Example: `SendMessage({to: "backend-engineer", message: {type: "shutdown_request", reason: "wave complete"}})`. No `summary:` field required when `message` is a structured object.
- **`SendMessage` with text:** Prose messages pass `message:` as a string and include a `summary:` (5–10 words, shown in the UI).
- **`Agent` tool with `team_name`:** Spawns a persistent teammate. Omit `team_name` to spawn a one-shot subagent (reviewers).
- **Teammate names:** Addressed by `name` (not `agentId`) throughout — in `SendMessage.to`, in `TaskUpdate owner:`, and in team discovery via `~/.claude/teams/<team>/config.json`.

## Message Discipline (Echo Defense)

Two failure modes can make the lead act on stale directives. Guard against both.

**1. Peer-DM idle-summary echoes.** When a teammate DMs another teammate, a brief summary appears in the next idle notification the lead receives. The platform docs describe these as informational. **The lead must not act on peer-summary content** — only on direct messages where the lead is the recipient, on completion-report metadata flags (see Phase 3), or on `TaskList`/`TaskGet` state.

**2. Quote-back loops.** If a teammate quotes a prior reviewer report or lead message in their reply, the original directive text re-enters the lead's context and risks re-triggering pattern-matched dispatch. The implementer prompt forbids quoting; if you observe a teammate quoting anyway, treat the quoted content as already-handled and discard.

**Practical rule for the lead:** dispatch reviewers and mark tasks complete based on `TaskGet`/`TaskList` state and metadata flags written by the teammate (`metadata.report_ready: true`), not on prose patterns like `Status: DONE` appearing anywhere in your inbox.

## The Process

### Phase 1 — Boot

1. Read plan file end-to-end. Extract tasks, Specialists table, Waves, Dependency Graph, Lifetime Plan.
2. Verify the plan's `> **For agentic workers:**` blockquote names `agent-team-driven-development`. **Scope the check to blockquote lines only** (lines beginning with `>`); e.g., `grep -E "^>.*agent-team-driven-development" <planfile>`. A plan that merely mentions the skill name in prose (Goal/Architecture/Tech Stack/task text) must NOT pass this check; only the blockquote's named sub-skill counts. If the blockquote is absent or names a different skill (e.g., `subagent-driven-development`, `executing-plans`), halt: *"This plan was written for a different execution model; re-run `writing-plans-for-teams` or use the skill the blockquote names."*
3. Verify environment matches § Compatibility (experimental flag for Agent Teams in user settings, CC version meeting the documented minimum, required primitives available). Halt with remediation pointing to `update-config` skill if any prerequisite is missing.
4. Verify git worktree if the plan modifies code (skip for docs-only plans). Halt if on `main`/`master` without explicit user consent.
5. `TeamCreate` with `team_name: <plan-slug>` (derived from plan filename), `agent_type: "lead"`, and `description` set to plan's Goal line. Verify team creation succeeded before proceeding; on failure, apply the slug-collision recovery from Error Handling.
6. `TaskCreate` for every plan task, in plan order:
   - `subject` = `[<role>] Task N: <name>` (role prefix drives self-claim filtering)
   - `description` = terse task reference: the Specialist/Depends on/Produces metadata block plus the bulleted step titles (not the full step bodies — those travel in the spawn prompt from `./implementer-prompt.md`)

   Role names in subjects must be identifier-safe (alphanumerics, hyphens, underscores) so prefix matching works reliably. The Specialists table in the plan establishes the canonical strings.

   **`<role>` is the shared role identifier, not an individual teammate name.** When multiple instances of one role exist (e.g., `js-engineer-1`, `js-engineer-2`, `js-engineer-3` running three Wave 1 tasks in parallel), every one of them filters on the shared prefix `[js-engineer]`. Any of them can self-claim any task with that prefix; their individual names only appear in the `owner` field, never in the subject.

   **Issue `TaskCreate` calls serially (not in parallel) to preserve plan-order task IDs.** Parallel creation assigns IDs in completion order, which breaks the correspondence between "Task N" in the plan and "lowest-ID-first" self-claim preference. In either case, keep a mapping from plan task number to returned `taskId` for dependency wiring.

7. Second pass: for each task, parse its `Depends on:` field to get referenced plan task numbers, look up their `taskId`s in the mapping, and call `TaskUpdate addBlockedBy: [<taskIds>]`.
8. Announce: `"Starting agent-team-driven-development. Team <slug> created with N tasks across W waves. Wave 1 kickoff: [teammates], tasks [IDs]."`

### Phase 2 — Wave 1 kickoff (lead-assigned)

For each Wave 1 task (up to 3 simultaneous):

1. Spawn the teammate via the `Agent` tool using `./implementer-prompt.md` § Initial Spawn template.
2. `TaskUpdate owner: <teammate-name>` to explicitly assign the task.
3. Wait for idle notifications. Do not poll.

### Phase 3 — Wave execution (hybrid)

**Triggering rule:** Lead acts on teammate state, not on prose. When you receive a teammate message addressed to you, do not pattern-match its body. Instead, call `TaskGet` on the teammate's current task and read its metadata. The teammate signals readiness for review by setting `metadata.report_ready: true` (see implementer prompt). The metadata flag — not the words `Status: DONE` — drives reviewer dispatch.

**Lead's continuous loop** — when a teammate notification arrives, run this sequence:

1. Identify which task the notification refers to (use the `to`/`from` mapping plus `TaskList` to find their `in_progress` task).
2. `TaskGet` that task.
3. Branch on `metadata.report_ready` and `metadata.status_code`:

- **`report_ready: true`, `status_code: DONE`** → dispatch spec reviewer using `./spec-reviewer-prompt.md`. Don't wait for other teammates.
- **`report_ready: true`, `status_code: DONE_WITH_CONCERNS`** → read `metadata.concerns` from task. Correctness/scope concern → address via `SendMessage` before dispatching reviewer. Observation → note and dispatch reviewer.
- **`report_ready: true`, `status_code: NEEDS_CONTEXT`** → answer via `SendMessage`. Clear `metadata.report_ready` (set to `false` via `TaskUpdate metadata: {report_ready: null, ...}`). If the question reveals a real plan gap, update the plan file before continuing.
- **`report_ready: true`, `status_code: BLOCKED`** → diagnose per rubric below. Never ignore.
- **No `report_ready` flag** → message is informational (peer-summary echo, mid-work check-in). Do not dispatch a reviewer. If the message is a direct question to the lead, answer it; otherwise discard.

**Review-stage transitions** (also driven by metadata, not prose):

- **Spec reviewer returns** → read its verdict from the reviewer's structured report. On `SPEC COMPLIANT`, dispatch code quality reviewer using `./code-quality-reviewer-prompt.md`. On `SPEC ISSUES`, forward verbatim via `SendMessage` using `./implementer-prompt.md` § Review Feedback template; clear `metadata.report_ready` and wait for the teammate to re-set it after the fix.
- **Code quality reviewer returns** → on `APPROVED`, read current task description via `TaskGet`, concatenate the teammate's full completion report block (Status, Summary, Journal, Tests, Commits, and any Concerns — everything from the Completion Report Format) onto the end, separated by a clear marker (e.g., `\n\n---\n## Completion Report\n\n`). Call `TaskUpdate description:` with the full concatenation, then `TaskUpdate status: completed`. `TaskUpdate description` replaces; never call it with just the report block alone. On `ISSUES FOUND`, forward verbatim and wait for re-set.
- **All tasks in current wave `completed`** → verify via `TaskList`, proceed to Wave N+1 kickoff.

**BLOCKED rubric:**

| Cause | Recovery |
|---|---|
| Missing context the plan didn't provide | Answer via `SendMessage`, teammate continues |
| Reasoning limitation | Not expected at the documented model tier (§ Compatibility) — escalate as plan-too-large or plan-wrong |
| Task too large | Split task in plan file, `TaskCreate` subtasks with dependencies, shut down teammate, respawn for a subtask |
| Plan is wrong | Halt. Surface to user. Do not attempt plan rewrite autonomously. |

**Teammate self-claim loop (Wave 2+):**

Teammates execute this themselves per the implementer prompt. Lead observes via messages and task list changes; lead does not assign.

1. After lead marks current task `completed`, teammate calls `TaskList`
2. Filter to: `status: pending`, `owner: empty`, `blockedBy: empty`, and `subject` starts with `[<my-role>]`
3. Claim lowest ID: `TaskUpdate owner: <my-name>`
4. `TaskGet` for full description including journal entries from completed dependencies
5. Implement, test, commit, self-review, report completion via `SendMessage`

Note: `owner: empty` is the only reliable filter for claiming. The platform's `owner` field mixes IDs and names inconsistently across docs. All ownership WRITES in this skill use names (teammate's `name` from the team config, matching `SendMessage` conventions). Do not try to compare an existing `owner` value against your name directly; rely only on the empty-vs-non-empty distinction and on the rule that you always claim by writing your name.

**Wave transition:**

Before kicking off Wave N+1:
- Run `TaskList`, confirm every task in current wave (by ID, per plan's Wave Analysis) has `status: completed`
- For each teammate in Lifetime Plan:
  - Has work in new wave, already alive → `SendMessage` telling them new tasks are claimable for their role
  - Listed in Lifetime Plan but not yet alive → spawn now via `Agent` tool (`./implementer-prompt.md` § Initial Spawn)
  - Alive but no further work in Lifetime Plan → `SendMessage` with `{"type": "shutdown_request"}`

### Phase 4 — Completion

1. All tasks `completed` and reviewed.
2. Dispatch final cross-cutting reviewer via `Agent` tool with `subagent_type: superpowered-teams:code-reviewer`. Provide base-SHA-to-head-SHA diff context.
3. Write `docs/superpowers/plans/<plan-slug>.journal.md` using `./journal-snapshot-template.md` format, by walking completed tasks in order and extracting their Completion Report blocks (Status, Summary, Journal, Tests, Commits) from task descriptions.
4. **`TeamDelete` is blocked until the journal snapshot file exists.** Verify file exists before proceeding.
5. Shutdown live teammates: `SendMessage` with `{"type": "shutdown_request"}` to each.
6. `TeamDelete` after all teammates confirm shutdown. If a teammate doesn't respond to `shutdown_request` within a reasonable window, proceed only if `TeamDelete` succeeds (indicating no active members); if it fails per the "active members" path in Error Handling, recover before retrying.
7. Invoke `finishing-a-development-branch` as sub-skill.

## Status Protocol

Every teammate completion message ends with one of:

| Status | Meaning | Lead's next action |
|---|---|---|
| `DONE` | Task complete, self-review clean, ready for review | Dispatch spec reviewer |
| `DONE_WITH_CONCERNS` | Complete but teammate flagged doubts | Read concerns, route appropriately |
| `NEEDS_CONTEXT` | Can't proceed without info plan didn't provide | Answer via `SendMessage` |
| `BLOCKED` | Can't complete | Diagnose per rubric |

## Completion Report Format

Two artifacts at completion time, written by the teammate before sending the lead a notification:

**(a) Task metadata flags** (via `TaskUpdate metadata:`):
- `report_ready: true`
- `status_code: "DONE" | "DONE_WITH_CONCERNS" | "NEEDS_CONTEXT" | "BLOCKED"`
- `concerns: [<list of strings>]` (only when `status_code` is DONE_WITH_CONCERNS)

These are the dispatch triggers. The lead reads them via `TaskGet`; this is the echo-defense path described in Phase 3.

**(b) Completion Report prose** (placed in the task description by the teammate via `TaskUpdate description:`, appended after the original task text with a `---\n## Completion Report\n\n` marker):

```
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED

Summary: <one-sentence what I built>

Journal:
- Files created: [paths]
- Files modified: [paths]
- Exports added: [names]
- Schema/migrations: [if any]
- Patterns established: [notes, or "none"]
- Notes: [free text, or "none"]

Tests: <N passing / M failing / reason if failing>
Commits: <SHAs>
Self-review: <findings, or "clean">
Concerns: <if DONE_WITH_CONCERNS — list them>
Blocker: <if BLOCKED — what's wrong and why>
Questions: <if NEEDS_CONTEXT — specific questions>
```

The teammate writes the report into the task description so it survives even if the message channel drops the notification. The lead never reconstructs the report from `SendMessage` body content — always read it from `TaskGet`.

After `TaskUpdate description:` and `TaskUpdate metadata:` complete, the teammate sends the lead a one-line `SendMessage` notification: *"Task <ID> ready for review."* No quoted content, no embedded report. See implementer prompt § Notification Format.

The lead is enforced (by `TeammateIdle` hook, see Hooks Integration below) to refuse to proceed when `metadata.report_ready: true` is set without a Completion Report block being present in the description.

## Plan Approval for Risky Tasks

Agent Teams supports a `plan_approval_request` flow where a teammate works in read-only plan mode until the lead approves their approach. Use this for any task whose plan-file `Files:` block lists:

- Schema migrations
- Destructive operations (`rm -rf`, `DROP`, `TRUNCATE`)
- Changes to authentication, authorization, or session handling
- Large refactors that touch >5 files

To require plan approval, append this line to the spawn prompt under "Workflow":

> **Before implementing, send a plan_approval_request to the lead with your proposed approach. Wait for approval. Do not write code until approved.**

When the teammate sends `plan_approval_request`, respond with the matching `plan_approval_response` envelope (see SendMessage tool docs):
- Approve → teammate exits plan mode and implements
- Reject → set `feedback:` with what needs to change; teammate revises and resubmits

Make approval decisions against the plan file, not against the teammate's proposal in isolation. If the proposal contradicts the plan, reject. If it surfaces a plan gap, halt and escalate to user before approving.

## Hooks Integration (Optional but Recommended)

Three hooks elevate quality gates from prose-rule into harness-enforced. Configure in `~/.claude/settings.json`:

- **`TeammateIdle`** — exit code 2 keeps the teammate awake. Use to enforce: when `metadata.report_ready: true` is set, the task description MUST contain a `## Completion Report` section. If missing, exit 2 with feedback *"Set report_ready only after writing the Completion Report block into the task description."*
- **`TaskCreated`** — exit code 2 blocks creation. Use to enforce subject prefix discipline (`[<role>]`).
- **`TaskCompleted`** — exit code 2 blocks completion. Use to enforce that the description contains a Completion Report block before the lead can mark a task `completed`.

These hook event names are CC-coupled — see § Compatibility. If the harness renames a hook event, update there and the references here will still resolve to the right primitive.

These are optional. Without them, the rules are SKILL.md-enforced (i.e., the lead reads them and chooses to obey). With them, they are harness-enforced and can't be skipped.

## Review Feedback — Verbatim Rule

Lead forwards reviewer reports to teammates literally. No paraphrasing.

Use `./implementer-prompt.md` § Review Feedback template.

Accumulated reviewer prose is within working range at the documented model tier (§ Compatibility) by token arithmetic. There is no reliable self-detection mechanism for context quality degradation. If the user observes a teammate making mistakes inconsistent with their earlier work, the user should prompt a controlled refresh via shutdown + respawn.

## Error Handling and Edge Cases

**Teammate idle without completion** — nudge once via `SendMessage`: *"Status check — are you working on Task N, blocked, or waiting for something?"* If no productive response, shut down via `{"type": "shutdown_request"}` and respawn with context about what went wrong. Never try to fix from the lead.

**Teammate active but silent for extended duration** — if you have not received an idle notification or completion message after a reasonable implementation window (judgment call: compare to prior tasks of similar scope in the same session), send a status-check `SendMessage` as in "Teammate idle without completion." If they respond, resume normal flow. If not, follow shutdown-and-respawn.

**Teammate's code catastrophically wrong** — after **2 full review cycles** (spec + quality, with fixes between) without convergence, shut down and respawn with prior commit SHA as starting point and reviewer findings as context. If replacement also fails, escalate to user.

**Contradictory reviews across iterations** — dispatch fresh third reviewer with both prior reports. If still unresolved, escalate (spec is ambiguous). Never average.

**Approved-but-broken caught by final reviewer** — reopen task (`TaskUpdate status: in_progress`), respawn teammate, fix, re-review. Note in journal snapshot.

**Reviewer subagent timeout/failure** — redispatch once. On second failure, lead does inline review (acceptable since review is read-only context addition, not modification).

**Wave stuck on one teammate** — other teammates do not advance. Follow teammate-level recovery per the idle-without-completion or active-but-silent case.

**Unclaimed task after wave declared complete** — halt Wave N+1. Inspect `TaskList` for `pending` tasks with empty `owner`. Fix subject prefix or manually assign. Resume only when all prior-wave tasks `completed`.

**`TeamCreate` fails (slug collision)** — append session date to slug (e.g., `<slug>-20260502-1430`). For orphaned teams, surface to user before any deletion.

**`TeamDelete` fails (active members)** — re-send `shutdown_request`. If still stuck, surface to user.

**Session dies mid-wave** — documented Agent Teams limitation. On resume: read `TaskList`; for `in_progress` tasks with owners that no longer exist as active teammates, shut down ghosts and respawn with context about prior commit SHA. Rebuild wave tracking from `TaskList` status.

**User interrupts mid-task** — `SendMessage` teammate: *"Pause — don't commit anything in progress, report current state."* Surface state to user, await direction.

**Plan missing required fields** — boot-time halt. Suggest re-running `writing-plans-for-teams`. Do not attempt to infer missing fields.

**Cycle in dependency graph** — detect after Phase 1 `addBlockedBy` pass by checking for any task whose blocked-by chain eventually includes itself. Halt with cycle identified.

## Red Flags

**Sequencing — never:**
- Start code quality review before spec compliance passes
- Start Wave N+1 before current wave's reviews all pass
- Let a teammate start a new task while their current task has open review issues
- Start work on `main`/`master` without explicit user consent
- Do a full-file grep for `agent-team-driven-development` as the blockquote check — scope to lines starting with `>` so prose mentions don't accidentally satisfy the check

**Parallelism — never:**
- More than 3 simultaneous teammates
- Tasks touching the same files in the same wave
- Proceed when unsure about independence (serialize instead)
- Give a teammate more than one task at a time

**Communication — never:**
- Paraphrase reviewer reports to teammates (verbatim rule)
- Make teammates read plan files (provide full text in spawn prompt)
- Omit prior-wave journal data when a task has cross-wave dependencies
- Rush teammates past their `NEEDS_CONTEXT` questions
- Treat idle state as failure (it's normal)

**Reviews — never:**
- Skip re-review after fixes
- Let self-review replace actual review (both needed)
- Skip either review stage
- Proceed with unfixed issues
- Accept reviewer contradictions without a third-reviewer tiebreak

**Recovery — never:**
- Try to fix manually from the lead (context pollution)
- Attempt plan rewrite autonomously
- Ignore a stuck teammate hoping they recover (nudge once, then shut down)
- Delete or modify `~/.claude/teams/<slug>/` files mid-session

**Journal — never:**
- Mark a task `completed` without a Journal block in the task description
- Call `TeamDelete` before writing the journal snapshot file
- Reconstruct completion reports from `SendMessage` body content — read from `TaskGet` description (the teammate writes the report there before notifying). Lead does not parse prose from messages.
- TaskUpdate description: with just the report block alone (it would destroy task content). Always concatenate onto the existing description.

**Echo defense — never:**
- Act on `Status: DONE` or other prose markers found in peer-DM idle summaries
- Re-dispatch a reviewer because the same status text re-appears in the inbox
- Trust message body content over `TaskGet` metadata for dispatch decisions
- Tolerate teammates quoting prior reviewer reports or lead messages — silently discard quoted content, don't re-process it

## Prompt Templates

- `./implementer-prompt.md` — three templates: initial spawn, follow-up task assignment, review feedback forwarding
- `./spec-reviewer-prompt.md` — spec compliance reviewer subagent
- `./code-quality-reviewer-prompt.md` — code quality reviewer subagent using `superpowered-teams:code-reviewer`
- `./journal-snapshot-template.md` — format for the end-of-session journal file

## Integration

**Upstream:**
- `brainstorming` → produces spec consumed by `writing-plans-for-teams`
- `writing-plans-for-teams` → produces plan this skill executes
- `using-git-worktrees` → required if team will modify code

**Peers:**
- `subagent-driven-development` → serial alternative for plans that don't pass fitness check

**Invoked as sub-skills:**
- `test-driven-development` → implementer prompts reference this
- `superpowered-teams:code-reviewer` (this plugin's agent) → code quality review and final review
- `requesting-code-review` → review methodology

**Downstream:**
- `finishing-a-development-branch` → merge/PR/cleanup after `TeamDelete`
