---
name: harness
description: Run the FULL SDLC pipeline end-to-end — Plan → Implement → Verify → Maintain — with a checkpoint between every phase. Use for a complete feature from a one-line idea to merge-ready. Chains the four phase orchestrators; you approve each phase boundary.
---

# /harness — the full pipeline

The top-level orchestrator. It walks all four phases by invoking the phase
orchestrators in order, **pausing at every phase boundary for your go-ahead**. It is a
convenience wrapper — it adds checkpoints and a running summary, nothing the phase
skills don't already do.

## Flow

```
/harness-claude:harness-plan ──▶ [checkpoint] ──▶ /harness-claude:harness-implement ──▶ [checkpoint]
   ──▶ /harness-claude:harness-verify ──▶ [checkpoint] ──▶ /harness-claude:harness-maintain (optional)
```

1. **Plan** — run `/harness-claude:harness-plan`. At its HALTs, get the user's answers/approvals.
   → **CHECKPOINT:** show the approved spec + plan (+ ADR). Wait for "go" before coding.

2. **Implement** — run `/harness-claude:harness-implement` against the approved plan.
   → **CHECKPOINT:** report what was built and test status. Wait for "go" before verify.

3. **Verify** — run `/harness-claude:harness-verify`. Halt on Critical/High; stop at the git boundary.
   → **CHECKPOINT:** show review/security verdicts, coverage, observed-working evidence.

4. **Maintain** — **offer** `/harness-claude:harness-maintain`. Run it only if the user wants cleanup now.

## Rules
- Honor every HALT and CHECKPOINT — this is a guided pipeline, not an autonomous run.
- Delegate heavy work to subagents; `/harness-claude:save-session` at each checkpoint so a long feature
  survives compaction or a new session.
- Never commit or push without an explicit user ask — branch creation happens automatically
  at first write in the Implement phase (`rules/git.md`). `/harness-claude:harness-verify`
  ends at "ready to commit/PR."
- For a small change, a single phase orchestrator (or atomic skill) is lighter — `/harness-claude:harness`
  is for full features.

## Output
A phase-by-phase rollup ending in "merge-ready (awaiting your git go-ahead)."
