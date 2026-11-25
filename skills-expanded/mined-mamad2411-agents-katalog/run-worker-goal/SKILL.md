---
name: run-worker-goal
description: Dispatch or continue one identified, approved persistent Codex worker goal when the user explicitly requests execution. Require an exact goal and verified worker mapping. Do not trigger for generic go/continue, status-only reads, goal preparation, or non-Codex browser/terminal workflows.
---

# Run Worker Goal

Execute the approved contract, not another round of architecture planning.
Use [prepare-worker-goal](../prepare-worker-goal/SKILL.md) only when the goal is
missing, ambiguous or needs a scoped revision. Tiny direct tasks need no lane.

## Required inputs and authority

Read the owning repository's `AGENTS.md`, applicable SPEC, current context and
the exact approved goal. The goal or private registry must supply:

- repository/workspace and allowed files or systems;
- goal ID/revision, one outcome and exact approved mutations;
- worker role and verified thread UUID, with exact controller `Reply-To`;
- result/evidence/marker paths and success/stop conditions;
- cleanup owner, approved durable destination and retention decision.

Do not infer a machine path, worker identity, model or target from a lane name.
Preserve existing paths and marker schemas; parallel goals must not share a
writable marker or root context. Missing or conflicting mapping is a blocker,
not permission to start a replacement worker.

The repository's SPEC and current approval govern action. A skill, model choice,
`safe_to_continue=yes`, queue receipt or plan UI cannot grant authority. Preserve
REVIEW/EDIT/COMPLETE and explicit no-merge/no-mutation limits when applicable.

## Pre-dispatch gate

1. Read the smallest current goal/result/marker evidence required to determine
   whether this exact goal is active, accepted, blocked or undispatched.
2. Do not dispatch a duplicate or overwrite active work. `Working`/`Ready` is
   only an observation; stale or uncertain evidence must be reconciled.
3. For a blocked goal, require a resolved blocker and an approved continuation
   or revision. For a completed goal, verify the controller decision and that
   any next action stays inside the approved SPEC.
4. Resolve `approved` or `go` only when exactly one goal is the clear target.
   Ambiguity means ask for that target, not guess or broaden the task.
5. Verify installed queue support and the goal's configured model/effort through
   the native adapter. Model selection belongs there, not in this skill. A
   queue message does not reconfigure the receiving session.

Use cheaper operators only for decided, proven work. Escalate unexpected output,
new PROD/IAM/network/state scope, partial cleanup, auth failure or conflicting
truth to the controller. Do not automatically restart or change a worker model.

## Execution mode

- **Direct bypass:** tiny result/status or local-validation work belongs to
  the controller, outside this dispatch skill. Do not create a lane, prompt
  copy or worker dispatch merely to handle it.
- **Goal:** execute the complete approved goal and its existing Probe/MVP/Full
  Lane gates. Require private-network, workload/security and rollback evidence
  when the owning policy calls for them.
- **Plan-only:** use when explicitly requested or when new PROD/stable-service,
  IAM/network, exposure, rollback, cleanup or approval questions remain. Do not
  mutate AWS or implementation files. Preparation is not execution permission.

A plan may proceed to execution only when the user authorized execution, the
plan stays inside the goal, and no unresolved gate remains. Do not choose plan
UI buttons or clear context according to an arbitrary percentage.

## Native dispatch

Follow the [Codex Native Controller-Worker Protocol](https://github.com/amitkarpe/agent-os/blob/535be4b923cb996d85613d970159d71499ad75ae/kb/playbooks/delegation/codex-native-controller-worker-protocol.md)
for controller-to-worker, worker-to-worker and result notifications.

Send one short queue message pointing to the complete goal, with provenance and
exact `Reply-To`. Do not create another prompt copy merely to send a path.
A valid receipt means `notification_queued` / transport admission only; it ends
that send attempt. Never send a second copy through queue, tmux, composer,
supervisor, Enter, Tab, F12 or a file mention.

Without a valid receipt, record `BLOCKED_TRANSPORT`; reconcile possible original
admission/execution. Follow the canonical stop-and-repair rule: at most one
redispatch after authorized repair, only when the original was not admitted or
executed. Unknown outcomes or another failure stay blocked. Do not create a
retry loop. Tmux remains lifecycle/observation only.

## Result and acceptance

The worker owns the operation until terminal evidence or an explicit blocked
handback. Use existing deterministic commands/waiters and required validation;
never infer completion from a returned prompt or leave a live process unowned.
Write `RESULT.md` before the existing marker and one native result notification
to `Reply-To`. Preserve the result if notification is blocked.

Use the owning marker schema and paths rather than a second schema in this
skill. Preserve result status/path, next action, blocker, `safe_to_continue`, and
required resource/exposure evidence. `safe_to_continue=yes` is not a new goal or
cleanup approval. Reports do not replace required evidence.

The controller reviews evidence and required fresh state before acceptance.
Cleanup/retention follows the adopted shared lifecycle and exact goal approval;
worker completion alone must not delete the lane. Leave an unresolved cleanup
obligation in the owning work record, not another handoff packet.

## Completion summary

Return execution mode, goal ID/revision, verified target, result or expected
result path, admission/work/acceptance states separately, blocker and one next
action. Do not claim execution from queue admission or local runtime from old
repository notes. Non-Codex workers use their separately approved adapter.
