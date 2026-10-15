---
name: builder-loop
description: Disciplined plan → validate → checkpointed-build workflow with a bounded final agent-review gate. Use when explicitly asked to break a non-trivial feature, refactor, or migration into validated checkpoints, plan before coding, or implement with named review gates. Pairs with the agent-review skill.
---

# Builder Loop

Deliver a non-trivial change as a few coherent, validated checkpoints followed by
one integrated agent-review gate. The goal: catch design flaws before coding and
implementation flaws with focused proof, without repeatedly reviewing the same
change.

Use only when the user explicitly requests checkpointed planning/building or named
review gates. Do not infer it from generic requests such as "do this end-to-end" or
from a change merely spanning layers. Skip for trivial edits and prefer one to
three checkpoints for most work.

The review engine is the repo's **`agent-review`** skill. Read
`.agents/skills/agent-review/SKILL.md` for its contract and commands. This skill
orchestrates *when* to invoke it; that skill defines *how*.

## Pipeline

Keep this checklist in the available task tracker:

- [ ] **CP0 — Plan & validate locally** (no production code yet)
- [ ] **CP1..N — Implement each checkpoint** (focused project gate)
- [ ] **CP-final — Full validation + bounded full-change agent-review + handoff**

Create a branch before any code (never work on the default branch).

## CP0 — Plan & validate before coding

1. Decompose the task into the fewest coherent checkpoints that compile and are
   independently verifiable, each with its own gate (typecheck / lint / focused
   tests / build). Prefer one to three checkpoints and order dependencies clearly.
2. Explore the real code first (read the actual files / call sites), then record the
   plan in the task tracker. Use a scratch doc (e.g. `PLAN-<slug>.md`) only when the
   plan needs durable detail beyond the tracker. Cover verified current state with
   `file:line` refs, design decisions, per-checkpoint scope + gate, and risks.
3. **Validate the plan against reality:**
   - When the user or active agent instructions explicitly request parallel
     review, use independent subagents to pressure-test separate concerns.
     Otherwise perform the same checks locally against the real code. See
     `references/playbook.md` for the review rubric.
   - Resolve concrete gaps against the real code. Do not run agent-review on the
     plan doc: the runner sees changed files, not the unchanged implementation the
     plan describes.
4. If you created a scratch plan doc, delete it after validation and before CP1. It
   is a working artifact, not a review or delivery artifact.

Do not start CP1 while a concrete design decision remains unresolved. Ask the user
when resolving it would expand or materially change the requested task.

## CP1..N — Implement each checkpoint

Group checkpoints into coherent compilable units (e.g. all backend, then all iOS) —
reviewing a half-written layer with no consumer produces noise. For each unit:

1. Implement the checkpoint. Keep edits at the right ownership boundary; update docs
   in the same change (per `AGENTS.md`).
2. Run the checkpoint gate: the project's typecheck / lint / focused tests, or the
   build for client code. Fix until green. See `references/playbook.md` for the gate
   matrix.
3. Do not run agent-review automatically at each checkpoint. Focused proof is the
   checkpoint gate; the integrated change is reviewed at CP-final.
   - Run a checkpoint review only when the user explicitly requested per-checkpoint
     review for that checkpoint.
   - When requested, use the same bounded process as CP-final below; never restart
     a complete multi-round sequence after every fix.
4. Commit the checkpoint (only when the user authorizes commits). Move to the next.

A finding outside touched files is in scope only when the requested behavior would
otherwise be incorrect (e.g. new copy that leaves another affected surface stale).
Classify other adjacent findings as follow-up work.

## CP-final — Full validation, full-branch review, handoff

1. Update colocated docs and the session changelog (`.agents/sessions/...`).
2. Run the full gate: complete typecheck / lint / test suite and a clean build.
3. Run one bounded agent-review landing review over the complete change: use branch
   mode for a committed branch or local mode when work remains uncommitted.
   - Start with round 1 using the combined correctness, security, structural-
     simplicity, modularity, and reuse contract.
   - Verify findings against the real code and fix only in-scope blockers.
   - After an accepted fix changes the source, rerun relevant proof and advance to
     the next convergence round. Allow round 3 only when round 2 produces another
     accepted blocker whose fix changes the source.
   - Stop after round 3 and report unresolved findings; do not loop until clean.
4. If the user requested publishing, use the available GitHub workflow to open or
   finish the PR and confirm CI is green and the PR is mergeable.
5. **Stop at ready.** Do not merge or deploy — report merge/ship-readiness and let
   the owner decide (per `AGENTS.md`).

## Reference

| Need | Read |
|------|------|
| Subagent plan-validation prompt template, agent-review commands, gate matrix, pitfalls | `references/playbook.md` |
| Agent-review engine contract + flags | `.agents/skills/agent-review/SKILL.md` |
