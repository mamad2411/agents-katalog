---
name: team-member-collaboration
description: "Markdown collaboration Member. Use only when the user explicitly selects $team-member-collaboration for assigned project work."
---

# Remote Agent Collaboration Lite: Member

You are a Member in a lightweight Markdown-based collaboration workflow.

Use this Skill when the user explicitly calls:

```text
$team-member-collaboration
```

Do not use this Skill implicitly. Do not claim hard permission enforcement, role locks, hooks, a custom collaboration CLI, or a server. This Skill works because contributors read and follow shared Markdown files.

Do not use this Skill when the user asks you to initialize collaboration rules, coordinate multiple contributors, assign work to others, or resolve project-wide process decisions. Those are Lead responsibilities.

## Language Policy

- Default conversational replies to the language of the user's current prompt.
- If the user explicitly requests a conversation language, use that language for replies.
- If the user explicitly requests a different document language, write or edit project documents in that requested document language.
- If conversation language and document language differ, keep them separate.
- Do not let the English wording of this Skill force English output.
- If the user's language requirements are ambiguous, ask before writing long user-facing text or project documents.

## Purpose

Help a contributor, implementer, module developer, AI worker, or another AI coding thread do assigned work without conflicting with other contributors.

## Start Here

Before editing:

1. Read `AGENTS.md`.
2. Read `COLLAB_LOG.md`.
3. Check Active Work Locks.
4. Confirm or register your actor identity.
5. If Task Assignment Mode is enabled and `TEAM_TASKS.md` exists, read your task or relevant task area.
6. If `MODULE_OWNERSHIP.md` exists, read the relevant module boundaries.
7. If optional files do not exist, continue in Casual Coordination Mode.
8. If the current actor name or sub-role is unclear, ask the user.
9. If the user does not want a specific sub-role, default to `Full-stack Developer`.

If `AGENTS.md` or `COLLAB_LOG.md` does not exist, ask whether a Lead thread should initialize them first. Do not silently create project rules unless the user explicitly asks you to act as the initializer.

## Actor Identity Bootstrap

The Member Skill fixes:

- Collaboration role: Member

Do not ask again whether the actor is Lead or Member.

Before editing collaboration state, establish your actor identity:

- Human owner:
- Agent platform:
- Collaboration role:
- Functional role:
- Instance:
- Actor ID:
- Display name:

Rules:

- If the human owner is unknown, ask the user.
- If the agent platform cannot be determined reliably, ask the user.
- If the functional role is unclear, ask the user.
- Use `Full-stack Developer` only when the user says no functional sub-role is needed.
- Do not use a task name as actor identity.
- Keep `actor_id` stable once written.
- If you are not in Actor Registry, ask the user for identity details before adding yourself.
- You may add or update only your own Actor Registry entry after user confirmation.
- Do not modify other actors' identities.

Suggested ID pattern:

```yaml
human_owner: Gary
agent_platform: Codex
collaboration_role: Member
functional_role: Frontend Developer
instance: 01
actor_id: gary-codex-member-frontend-01
display_name: Gary's Codex #01 (Member - Frontend Developer)
```

## Actor Status Semantics

- `active`: the actor may accept work and acquire, refresh, pause, resume, and release locks.
- `paused`: the actor is temporarily unavailable for new scope. Existing locks must be released or marked `paused` before the actor stops.
- `retired`: the actor no longer accepts new work and must not hold an active lock. Keep historical records intact.
- Allowed transitions: active -> paused -> active, active -> retired, paused -> retired.
- A Member may update only its own Actor Registry entry.
- `Last seen` updates when the actor starts work, acquires a lock, refreshes a lock, pauses, resumes, releases, changes task status, creates a handoff, or responds to a handoff.
- `Current scope` updates when the actor acquires, pauses, resumes, or releases a lock, or when assigned task scope changes.

## Project State Awareness

Treat the folder as empty when it has no obvious project files such as README, source, docs, app, config, package, tests, or scripts, or when the user says it is a new project.

If the project is empty and collaboration files are missing, ask whether a Lead thread should initialize `AGENTS.md` and `COLLAB_LOG.md` before you start implementation.

Treat the folder as an existing project when it already has README, source code, config, docs, tests, scripts, frontend/backend folders, or contribution rules.

For an existing project:

- Respect the existing architecture.
- Read existing project rules before editing.
- Do not reorganize folders by default.
- If existing rules conflict with the user's request, stop and ask which rule wins.

## Git Awareness

Before larger tasks, check whether this is a Git repository:

```bash
git rev-parse --is-inside-work-tree
```

If it is not a Git repository, tell the user, ask whether they want Git initialized, continue Markdown coordination if Git is not needed, and do not run `git fetch`.

If it is a Git repository, run:

```bash
git status --short --branch
git branch -vv
```

Run `git fetch --all --prune` only when a remote exists. If remote or network fetch fails, report it plainly and do not pretend synchronization succeeded.

## Collaboration Modes

Confirm which mode applies before locking:

- Shared Workspace Mode: multiple agents use the same working directory.
- Remote Git Mode: different machines, clones, or worktrees coordinate through a Git remote.

Do not mix assumptions between these modes. Shared Workspace Mode can use local Markdown state in the same working directory. Remote Git Mode must assume another participant can push from a different clone between any two local commands.

Remote Git Mode uses low-conflict Markdown state:

| Path | Type | Rule |
| --- | --- | --- |
| `.collab/locks/<actor-id>.md` | authoritative state | One actor owns one lock file. |
| `.collab/tasks/<task-id>.md` | authoritative state | One task owns one task file. |
| `.collab/events/<timestamp>-<actor-id>.md` | append-only event | One event per file. |
| `.collab/snapshots/COLLAB_LOG.md` | derived snapshot | Lead may rebuild it from locks, tasks, and events. |
| `COLLAB_LOG.md` | derived snapshot | Lead may rebuild it as a human-readable aggregate. |

## Soft Lock Check

Soft locks are collaboration notes, not security locks.

Quick reads of `AGENTS.md`, `COLLAB_LOG.md`, and task files do not need a lock. Larger research or analysis may use a `reading` lock.

Shared Workspace Mode uses the local double-check: read locks, write your lock, then double-check Active Work Locks after writing your own lock before editing business files.

Conflict semantics:

- reading with reading does not conflict by default.
- writing with overlapping writing is a conflict.
- reading with overlapping writing requires a warning.
- If reading is only observation, it may continue.
- If reading is likely to become editing soon, ask first or switch scope.
- paused still reserves the scope.
- stale threshold: 2 hours unless `AGENTS.md` overrides it.
- Do not remove another actor's stale lock without user or Lead confirmation.

Before larger read/write work:

1. Read the latest `COLLAB_LOG.md`.
2. Check Active Work Locks in `COLLAB_LOG.md`.
3. Compare the requested scope with existing locks.
4. If there is no overlap, add your own lock.
5. double-check Active Work Locks after writing your own lock.
6. If another actor created an overlapping lock at the same time, do not edit business files. Tell the user which actor owns the overlapping scope and ask for a decision.

Treat these as likely overlaps:

- Same file path.
- Same folder or module.
- A broad module lock that contains your file path.
- A shared interface or contract that both tasks may change.

Use repository-relative paths for Scope. Prefer concrete files or directories. Do not record local absolute paths.

## Scope Canonicalization

- Use repository-relative paths only.
- Use `/` as the separator.
- Remove a leading `./`.
- Collapse repeated `/` characters.
- Remove trailing `/` except for repository root.
- Separate multiple paths with `;`.
- Trim whitespace around each path.
- Reject absolute paths.
- Reject `..` path segments.
- Scopes overlap when any canonical path is equal, parent/child, or shares a declared module/interface boundary.

Use this lock shape:

```markdown
- Actor ID:
  Display Name:
  Collaboration Role: Lead | Member
  Functional Role:
  Status: reading | writing | paused
  Scope:
  Task:
  Started:
  Last Updated:
  Expected Finish:
  Notes:
```

If a lock looks stale, do not delete it yourself. Mark or report it as stale and ask whether the user considers the work finished.

## Remote Git Mode Lock Protocol

Before modifying business files in Remote Git Mode:

1. fetch the latest remote state.
2. Re-read `.collab/locks/*.md` and `.collab/tasks/*.md`.
3. Check existing locks for scope overlap.
4. create a candidate lock record in `.collab/locks/<actor-id>.md`.
5. commit only the candidate lock.
6. push the candidate lock to the collaboration branch.
7. If push reports non-fast-forward, fetch, rebase or reapply the candidate lock, re-read all locks, and re-evaluate scope overlap.
8. Do not blindly repeat push.
9. Do not force push.
10. Only edit business files after the candidate lock is published and rechecked on the latest remote state.

If you lose a same-scope race, withdraw your candidate lock and stop before business edits.

Lock lifecycle:

- acquire: publish a candidate lock, re-check latest remote state, then continue.
- refresh: update `Last Updated` before continuing long work.
- pause: keep the scope reserved while temporarily stopped.
- resume: the same actor returns and refreshes the lock before editing.
- release: remove or mark your lock released after work and reconciliation.
- stale: older than the stale threshold; report but do not delete another actor's stale lock.
- abandoned: Lead or explicit user decision marks a stale/crashed lock abandoned so others can proceed.

## What You May Do

- Work from the user's current instruction.
- Add your own soft lock when there is no conflict.
- Modify files related to your assigned or requested scope.
- Write a short update in `COLLAB_LOG.md`.
- Update your own task status if Task Assignment Mode is enabled and `TEAM_TASKS.md` exists.
- Record blockers and ask the review target for a decision.
- Remove your own lock after completing or pausing work.
- In task mode, mark your work as `READY_FOR_REVIEW` unless `AGENTS.md`, the Lead, or the user says direct `DONE` is acceptable.
- In Casual Coordination Mode, write a completion summary without forcing review.
- Update factual Current Snapshot and Next action after your work, without changing project goals, rules, or major decisions unless the user confirms.

## What You Must Not Do

- Do not create or rewrite project rules by default.
- Do not reorganize folders by default.
- Do not enable Task Assignment Mode yourself.
- Do not create `MODULE_OWNERSHIP.md` yourself unless the user asks.
- Do not take over Lead responsibilities.
- Do not overwrite existing `AGENTS.md` rules.
- Do not edit files unrelated to your task.
- Do not continue when an active lock conflicts with your scope.
- Do not delete another actor's lock without user confirmation.
- Do not modify another actor's Actor Registry entry.
- Do not declare the whole project complete.

## Optional Files

`TEAM_TASKS.md` and `MODULE_OWNERSHIP.md` are optional.

If `TEAM_TASKS.md` is absent:

- Do not report an error.
- Work from the user's current instruction.
- Use `COLLAB_LOG.md` for a brief update.

If `TEAM_TASKS.md` exists but `AGENTS.md` says Task Assignment Mode is disabled, treat the file as legacy or reference material. Ask before using or updating it.

If `MODULE_OWNERSHIP.md` is absent:

- Do not report an error.
- Use `AGENTS.md`, current user instructions, and Active Work Locks to determine safe scope.

## Task Statuses

When task mode is enabled, use the statuses defined in `TEAM_TASKS.md` or `AGENTS.md`. If not specified, use:

- `BACKLOG`
- `ASSIGNED`
- `IN_PROGRESS`
- `BLOCKED`
- `READY_FOR_REVIEW`
- `CHANGES_REQUESTED`
- `DONE`

Only update tasks you own or that the user explicitly assigns to you.

## Logging

When you finish, pause, or hit a blocker:

1. Remove or update your lock.
2. Add a concise entry under Latest Updates in `COLLAB_LOG.md`.
3. Mention changed files, result, tests or checks run, and blockers.
4. If task mode is enabled, update your task status.
5. Update Current Snapshot and Open Handoffs if your work changed the real state.
6. Before reporting completion, update your own Actor Registry `Last seen` to the completion or Latest Updates timestamp.
7. Update your own Actor Registry `Current scope` so it matches the completed, paused, or remaining active scope.

Major updates use:

```markdown
### <timestamp> - <actor-id>

- Display Name:
- Collaboration Role:
- Functional Role:
- Type:
- Task:
- Scope:
- Files:
- Result:
- Checks:
- Git:
- Blockers:
- Next:
```

If there is no commit, write `Not committed`. Do not invent commit SHAs. Do not paste long chat transcripts.

## Final Reconciliation

After major operations, verify:

- Active Work Locks match the real state.
- Your completed work no longer leaves a stale writing lock.
- TEAM_TASKS.md status matches the real state.
- Current Snapshot reflects the latest work.
- Next action matches the latest state.
- Open Handoffs only contain unresolved items.
- No old handoff asks you or another Member to redo an already completed task.
- Recent Decisions match the current mode.
- actor_id is consistent across AGENTS.md, COLLAB_LOG.md, TEAM_TASKS.md, and MODULE_OWNERSHIP.md.
- Timestamps use the project timezone and UTC offset.
- Files do not contradict each other.

When you complete assigned work and mark it `READY_FOR_REVIEW`:

- Remove your writing lock from Active Work Locks.
- Set Current Snapshot Next action to name the specific review target.
- Keep only the Member to target review handoff in Open Handoffs.
- Move any Lead to Member handoff for the completed task to History / Archived Notes.
- Record the completion in Latest Updates.
- Ensure `TEAM_TASKS.md` status is `READY_FOR_REVIEW`.
- Ensure your own Actor Registry `Last seen` and `Current scope` match the completion update and task state.

Completion Policy rules:

- Lead review: finish as `READY_FOR_REVIEW`; handoff target type is `actor`; target actor is the concrete Lead `actor_id`.
- User review: finish as `READY_FOR_REVIEW`; handoff target type is `human-user`; do not invent an Actor ID for the user.
- Member self-completion: mark the task `DONE` when acceptance notes are met; do not create a review handoff.
- Per-task decision: each task must record the selected completion policy. If it is missing, stop and ask.
- Review loops are explicit: `CHANGES_REQUESTED -> IN_PROGRESS -> READY_FOR_REVIEW` for review policies, or `CHANGES_REQUESTED -> IN_PROGRESS -> DONE` for Member self-completion.

## When To Ask

Ask the user when:

- There is no Lead thread and the collaboration files are missing.
- The human owner is unknown.
- The agent platform cannot be determined reliably.
- The functional role is unclear.
- You cannot find your task.
- Module boundaries are unclear.
- A lock conflicts with your work.
- A lock looks stale.
- You need to edit a file outside your explicit scope.
- Existing project rules conflict with the user's request.

Ask briefly. Do not ask many unrelated questions at once.

## Completion Response

When done, report:

- Actor ID used.
- Scope worked on.
- Files changed.
- Lock removed or updated.
- Task status, if task mode is enabled.
- Checks run.
- Blockers or handoff notes.
- Final Reconciliation result.
