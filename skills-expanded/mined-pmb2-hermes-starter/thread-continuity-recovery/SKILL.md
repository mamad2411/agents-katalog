---
name: thread-continuity-recovery
description: Recover the correct conversation thread when a user resumes an older topic, avoiding project drift and assumption-based status reports.
title: Thread Continuity Recovery
version: 1.0
category: productivity
metadata:
  hermes:
    tags: [context, session-search, continuity, recovery, discord]
    triggers: [thread continuity, resume thread, older conversation, keep going, what have we accomplished, continue, prior thread, correct thread]
---

# Thread Continuity Recovery

How to recover the correct context when a user resumes an older conversation thread and expects answers grounded in that thread, not in the current or most-recent session state.

## When to use

- User says something like "Keep going," "What have we accomplished?", "Continue," or asks a status question that clearly references a prior thread.
- The user corrects you with phrases like "This thread is the thread that we were using" or "I just wanted a system update from you."
- You are tempted to answer from recent memory, recent files, or the most active project without first confirming which thread the user means.

## Core rule

**The user owns the thread. Do not assume the active context is the right context.**

When the reference is ambiguous, recover the right thread before answering substantive questions.

## Recovery workflow

1. **Pause on assumptions.** Do not report status from current working directory, latest git repo, or recent memory.
2. **Search session history for the user's topic keywords.** Use `session_search` with specific terms the user mentioned (e.g., "FCRA", "background check", "capital district website scan").
3. **Identify the matching session.** Look for the session title, timestamps, and repeated user messages like "continue" / "keep going" in that thread.
4. **Read the relevant session.** Use `session_search(session_id=..., around_message_id=...)` or a full read to reconstruct what was done, what stalled, and what files were produced.
5. **Cross-check artifacts.** Verify that files mentioned in the session still exist on disk and contain what the session claims.
6. **Answer with the recovered context.** Report status from the correct thread, cite the actual saved files, and ask the user what they want next.

## Common pitfalls

- **Project drift:** The most recently touched repo or the project in `memory` is not necessarily the project the user is asking about. Recent activity bias is real — counter it explicitly.
- **Answering from compaction summaries:** Context summaries injected by the system are reference material, not the thread itself. Use them only as a search hint; read the actual session and files before reporting.
- **Ignoring the user's correction:** If the user says "that is incorrect" and points to a different thread, stop the current line of reasoning immediately and switch to the thread they named.

## Style notes

- Keep the status report concise and factual.
- Cite file paths and dates so the user can verify.
- End with a clear next-step question.

## References

- `references/session-recovery-pattern.md` — annotated example from the FCRA background-check recovery (2026-07-12).
