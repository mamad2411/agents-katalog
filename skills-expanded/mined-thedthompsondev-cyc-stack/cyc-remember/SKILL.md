---
name: cyc-remember
description: "Keep a running decision log during work and rebuild context when resuming, so the next session knows what was decided, why, and what's next. Use at checkpoints, before stopping mid-task, when the user says \"catch me up\" or \"where did I leave off\", or when handing work to another session or tool."
---

# Remember what matters

Write memory as you go, not in a batch at the end. Follow the [handoff contract](../../docs/skill-contract.md).

## During work: the decision log

Append one row per consequential decision to `.cyc/runs/<runId>/decisions.tsv`, or `.cyc/runs/decisions.tsv` outside a run:

```text
time	stage	decision	why	evidence	who
2026-09-25T14:02	design	finished is a boolean, default false	no other states requested	storage.ts:15	user
2026-09-25T14:20	build	count derives from same filter	avoids drift	Counter.tsx:8	agent
```

- **evidence** is a pointer (file:line, command, or URL), never a paragraph.
- **who** is `user` (they decided), `agent` (you proposed; not yet adopted), or `adopted` (you proposed, the user agreed).
- Never edit a row. If a decision changes, append a new row that supersedes it.

## At a checkpoint

Write a capsule of five bullets or fewer: destination, current stage, what's proven (with evidence pointers), what's open, and the next single action. Tag each open thread with one status: `[done]`, `[in progress]`, `[blocked: reason]`, or `[dropped: reason]`. Untagged threads count as not done.

Point to canonical component context and its relevant constraints/checks instead of copying them into the capsule. Retain verified reusable findings through [Context](../cyc-context/SKILL.md) before final verification; a local decision log alone is not shared project memory. Each new feature and meaningful contract change leaves its planned canonical target-project record/index before completion; use finish/context prepare and preserve restrictions as pending. Completed-run catch-up is a new scoped update with fresh verification, not an edit to old evidence. Keep adoption status and technical evidence distinct.

## When resuming

Read `node <cli> run recover --run ID` for the existing run before changing its state. It preserves the recorded budget and exposes historical check receipts without making them current proof. Use the run ID from this task's records, not another session's latest run. If the ID is missing or several match, reconstruct the association from the task records before choosing. A paused run can resume; a blocked run first needs its recorded prerequisite resolved. An exhausted, halted or stopped run needs an explicit continuation decision rather than an automatic fresh budget.

1. Read the capsule and decision log first. They are the record; don't re-derive everything from scratch.
2. Check for drift: compare them with current files and git state. Recheck only what drift affects.
3. Treat an earlier "tests passed" as history, not a current result. Rerun before relying on it.
4. Preserve the user's changes made since the checkpoint.
5. Report what changed since the checkpoint and the next action. State what remains in place without calling it a backup or claiming earlier commands had no side effects. Keep agent-caused and user-caused changes distinct only when evidence establishes authorship. If help is needed, reuse the existing review, failing receipt and recorded prerequisite as the handoff; do not send it to a teammate without authorization.

## Done when

Another worker could read the capsule and log and state what's decided, by whom, what's proven, and the safe next step, without guessing.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| End-of-day dump | The log is written from memory at the end | Append when the decision happens |
| Authorship blur | An agent idea recorded as the user's choice | Use the `who` column honestly |
| Stale proof | Reusing old test results after resuming | Rerun |
| Silent scope shrink | "Catch me up on everything" answered from the last hour only | Say what range you covered |

Keep credentials and unrelated personal data out of every record. Use the controller's pause and resume commands; never edit its state files.
