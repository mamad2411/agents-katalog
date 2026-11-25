---
name: formation
description: Use when the first pane is asked to coordinate 2–11 user-selected panes in one Herdr workspace around one repo goal via agent-room Formation, including lane assignments, reports, review, and shipping; not ordinary subagent delegation, one pane, plain terminals, unselected panes, or cross-repo Programs.
---

# Formation

Formation coordinates approved panes as one temporary team for a single repository. Each admitted member owns an independent lane; any subordinate work inherits that lane's scope and limits.

## Rules for every lane

- **member-first:** 選択・admitした各member paneへ重複しない上位assignmentを確定してから下位workを使う。下位agentは未割当memberの代替にしない。Commander work follows the owner's explicit mode and bounds.
- Work only from the current assignment, its touching paths, and allowed methods. Do not widen scope. In a member lane, ask the Commander through `formation report` for decisions; do not question the user directly.
- Use the Formation CLI for assignment, correction, cancellation, reporting, acknowledgement, and release. Before each action, check `formation status --json` and match the current lane and assignment. Never send Formation messages by hand.
- Put scope, upper bounds, and completion criteria in the initial assignment: an in-flight Codex correction may not be read until its turn ends.
- Report `STARTED`, `RED`, `BLOCKED`, or `CANDIDATE_READY` as work changes. A `CANDIDATE_READY` report carries a committed SHA, clean worktree, verification, and review evidence; responsibility remains until Commander ACK.
- A report marked `unconfirmed` is already saved. Do not rerun it; the Commander reads the ledger status.
- Pane `idle` or `done` is not task-completion evidence. Check the lane report, commit, and clean worktree.
- Do not assign the next task until the prior `CANDIDATE_READY` is ACKed. Cancel an assignment before replacing it.
- Use a dedicated worktree based on current `origin/main`; the shared checkout is read-only. Members do not push.
- Use one independent `agent-room delegate --blind` review. After a fix, limit re-review to the changed area.
- Formation Shipper eligibility requires a verified `modern_cli`; a TGL ship request is not a Formation ship.
- Commander mode is `director-only` unless the owner authorizes bounded implementation as `director-and-implementer`. The capacity guard is `projectMemberCapacity` / `lane_has_active_assignment`; the ship seam is `executeFormationFfMerge`. See [implementation-map](references/implementation-map.md).

## Read procedures by branch

- Start, claim, assign, leave, roster changes, and close: [contract](references/contract.md).
- Notes, reports, delivery receipts, and transport outcomes: [messaging](references/messaging.md).
- Independent review and evidence recovery: [review](references/review.md).
- Implementation seams and history: [implementation-map](references/implementation-map.md).
- Shipping operation: [formation shipping runbook](https://github.com/fujimogn/agent-room/blob/main/docs/runbook/formation-shipping.md).

Use the relevant `agent-room formation <command> --help` for CLI options. Formation represents membership and lane responsibility; TGL, PLD, and other allowed tools are subordinate execution methods.
