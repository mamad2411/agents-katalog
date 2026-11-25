---
name: context-compaction
description: Keep a long agent session inside its context window without losing the plot. Use when a session is getting long, tool outputs are large, the agent starts "going off the rails" late in a task, or context usage is high. Trigger on big logs, long transcripts, or before a context-heavy step.
---
# context-compaction

The context window is the agent's working memory and it fills fast; even within the window, stale
tool output dilutes focus. If an agent goes off the rails late in a long task, the cause is almost
always context, not the model.

## Steps
1. **Truncate at the boundary.** A 50k-line log is not more useful than its first/last 200 lines
   plus a count. Cap large tool outputs before they enter context.
2. **Summarize-and-compact.** When the conversation crosses a threshold, replace the older middle
   with a model-written summary ("what we've done and learned so far"), keeping the original task
   and the most recent turns verbatim.
3. **Retrieve, don't carry.** Keep large reference material on disk; pull in only the chunks needed,
   when needed.
4. **Externalize state.** Write the plan/progress to `tasks/todo.md` and re-read it instead of
   holding it in the conversation. The agent forgets between runs; the repo doesn't.
5. **Reset to anchors.** On a fresh tick of a loop, reset context to the anchor files (AGENTS.md,
   the skill, the spec) rather than growing it.

## Notes
- `token-lean` pathway truncates aggressively; `accuracy-max` summarizes so nothing needed is lost.
