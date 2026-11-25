---
name: architect-implement
description: Implement or resume an existing Architect track by executing its approved plan and updating track status. Use when the user asks to implement, continue, resume, or complete a planned Architect track.
---

# Architect Implement

Execute one approved track through implementation, verification, synchronization, finalization, and optional cleanup. Follow `references/implement-track-protocol.md` as the source of truth.

## Hard Boundaries

- Require valid core context and track artifacts; `plan.md` defines scope and `workflow.md` defines lifecycle.
- Capture the worktree before editing. Never stage or commit unrelated or ambiguous changes, and never use broad staging.
- Preserve the plan's Task status granularity, phase, Manual/Auto, verification, and documentation approval gates.
- In Auto Mode, continue until finalization; task size and unfinished phases are not reasons to stop or send a final response.
- Never archive or delete without exact confirmation.

## Authorization

The implementation request authorizes one final track-scoped commit unless the user opts out. Auto Mode also authorizes phase checkpoint commits. Manual checkpoints, ordinary task commits, cleanup commits, and unrelated commits require separate authorization.

## Run

1. Read `references/implement-track-protocol.md`, validate context, and confirm the target track.
2. Load track and project context, capture the worktree baseline, and select Manual or Auto Mode.
3. Execute tasks and phase verification in state order.
4. Complete track bookkeeping and synchronize approved project documentation.
5. Create and verify the final track-scoped commit unless opted out.
6. Offer review, archive, delete, or skip cleanup under the protocol's approval rules.
