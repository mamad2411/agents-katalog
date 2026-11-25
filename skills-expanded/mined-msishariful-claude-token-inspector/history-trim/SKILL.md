---
name: history-trim
description: Analyze conversation history turn-by-turn and identify the exact point to run /clear from to prune stale history while keeping everything relevant to the current task. Use when history has grown long but you want to continue in the same session.
disable-model-invocation: true
---

# History Trim Advisor

Analyze the conversation history and find the safest `/clear` point — the turn where pruning everything before it costs nothing in terms of current task context.

## Analysis process

1. **Read the full conversation history** — every turn, from first to last.

2. **Identify the current task anchor** — the turn where the work the user is *currently* doing began. This is turn T.

3. **Classify every turn before T**:
   - **Active dependency**: a prior turn contains a decision, piece of code, constraint, or output that is still referenced or needed. Cannot be cleared without loss.
   - **Resolved context**: a prior turn was relevant at the time but the work it relates to is complete and no longer needed. Safe to clear.
   - **Dead weight**: unrelated to anything still in progress. Clear immediately.

4. **Find the trim point** — the latest turn where everything before it is either "resolved" or "dead weight" with no active dependencies. That's the recommended `/clear` point.

5. **Estimate the savings** — tokens recovered by clearing up to that point.

## Output format

Open with a verdict line:

```
✂️ Safe to clear {N} turns — recover ~{tokens} tokens
```

Or if no trim is safe:

```
⚠️ No safe trim point found — all prior turns have active dependencies
```

---

Then a turn-by-turn summary table (keep it tight — one row per distinct topic block, not per individual turn):

| Turns | Summary | Status | Safe to Clear? |
|-------|---------|--------|----------------|
| 1–5 | Initial project setup discussion | Resolved | ✅ Yes |
| 6–10 | Debugged login timeout — fixed in auth.ts | Resolved | ✅ Yes |
| 11–13 | Decided to use JWT over sessions | **Active dependency** | 🔴 No — still shapes current work |
| 14–now | Current task: refactor auth middleware | Current | — |

---

Then the recommended action:

```
💡 Recommended: /clear {N}
```

Where N is the turn number to clear up to (everything before turn N is pruned).

If there is an active dependency blocking a full clear, add:

```
⚠️ Before clearing: note this from turn {X}: "{one-sentence summary of the active dependency}"
```

List each active dependency that would be lost, so the user can manually preserve it before running `/clear`.

---

### If everything is safe to clear (no active dependencies at all):

```
✅ Full clear is safe — /clear will lose nothing relevant to your current task.
💡 Run: /clear
```

### If no turns can be cleared:

```
🔴 No safe trim point — every prior turn contains context still relevant to your current task.
💡 Consider /token-inspector:suggest-split to start a fresh session instead.
```

## Trim point rules

- Never recommend clearing a turn that contains: a decision still being acted on, code that was written and is still in use, a constraint or requirement that shapes current work.
- Prefer a trim point at a natural topic boundary (end of a resolved subtask) over an arbitrary line.
- If in doubt about a turn, mark it as active dependency — err on the side of preserving context.

$ARGUMENTS
