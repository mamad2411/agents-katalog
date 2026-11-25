---
name: suggest-split
description: Detect when a conversation has drifted across multiple unrelated topics and recommend whether to start a new conversation. Identifies the optimal split point and summarizes what to carry forward. Use when a session has been running long or has covered many different tasks.
disable-model-invocation: true
---

# Conversation Split Advisor

Analyze the current conversation and determine whether it has drifted enough that starting a new session would meaningfully improve context quality.

## Analysis process

1. **Map the conversation topics** — scan the full history and identify distinct task areas or subject shifts. A "topic" is a coherent unit of work (e.g., "debugging the auth middleware", "writing README", "reviewing PR #42").

2. **Find the current task** — what is the user actually working on right now? This is the anchor.

3. **Score past topics by carry-forward value**:
   - **Essential (carry forward)**: decisions made, constraints discovered, code written that is still active
   - **Partial (summarize)**: context that's partially relevant but could be distilled to 2–3 sentences
   - **Dead weight (discard)**: earlier topics completely unrelated to the current task

4. **Assess the split case** — is there a clear turning point where the conversation shifted to the current task? If yes, that's the split candidate.

## Output format

### If a split is recommended:

```
✂️ Split recommended — conversation has drifted across {N} topic(s)
```

Then:

**Topic map** (chronological):
| Turns | Topic | Status |
|-------|-------|--------|
| 1–8 | Debugging login timeout | 🗑️ Discard — resolved, no longer relevant |
| 9–14 | Reviewing PR #42 | 📋 Summarize — 2 decisions still apply |
| 15–now | Refactoring auth middleware | ✅ This is your current task — carry forward |

**What to carry into the new conversation:**

Write a ready-to-paste context block the user can paste at the start of their new session:

```
--- CONTEXT FROM PREVIOUS SESSION ---
[2–5 bullet points covering only the decisions, constraints, and code that are still relevant to the current task. Be specific: file names, function names, exact decisions made.]
--- END CONTEXT ---
```

**Split instructions:**
```
1. Copy the context block above
2. Start a new Claude Code session
3. Paste the context block as your first message
4. Continue with: [one sentence describing where to pick up]
```

### If no split is needed:

```
✅ No split needed — conversation is focused on a single task ({N} turns, ~{tokens} tokens used)
```

Follow with one line: `Context is coherent. Continue in this session.`

### If the conversation is too short to evaluate (< 5 turns):

```
ℹ️ Conversation is too short to evaluate for splitting ({N} turns).
```

## Decision thresholds

Recommend a split if ANY of the following are true:
- The conversation has covered 3 or more distinct topics
- More than 40% of tokens come from turns unrelated to the current task
- The current task started after turn 15 and the earlier turns add no carry-forward value
- Context is over 70% full and early turns are clearly dead weight

Do NOT recommend a split if:
- The conversation has stayed on one topic throughout
- Earlier turns contain decisions or code that are still actively referenced
- The session is under 10 turns

$ARGUMENTS
