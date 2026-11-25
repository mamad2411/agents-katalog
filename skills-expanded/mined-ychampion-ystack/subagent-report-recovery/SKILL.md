---
name: subagent-report-recovery
description: >-
  Recover a background subagent's full report when its completion notification or final message is
  empty or a one-liner ("Done.", "Complete.", "Standing by."). Use when a Claude Code Agent-tool task
  finishes with a high token count and many tool uses but the result text is missing the actual report,
  when the task's output file is 0 bytes, or when re-asking the agent with SendMessage also returns
  one-liners.
---

# Recovering reports from subagent transcripts

Claude Code specific: it reads the transcripts Claude Code writes for subagents. Other harnesses keep
their own session logs; the same idea (find the longest assistant text block) applies if you can
locate them.

## When this applies

- A background agent (Agent tool, `run_in_background: true`) completes with a useless result like
  "Done." or "No action pending.", but it clearly did the work (high token count, many tool uses).
- Re-prompting it with SendMessage returns another one-liner: the resumed agent has lost the thread or
  believes it already delivered.
- The `output_file` named in the task notification is **0 bytes**. This has been seen on Windows,
  where the tasks directory sits under `%TEMP%\claude\...\tasks\`.

## When it does not apply

- The result text contains the report. Use it.
- The agent failed early (few tool uses, small token count). There is nothing to recover; dispatch it
  again.

## Recovery procedure

The real transcript lives in the session directory, not in the task's output file:

```
~/.claude/projects/<project-slug>/<session-id>/subagents/agent-<agentId>.jsonl
```

`<project-slug>` is the working directory with path separators replaced by dashes; the agent id is in
the task notification. If you can't find it, list the session's `subagents/` folder by modification
time.

Don't read the whole JSONL into context: it can be enormous. Extract only long assistant text blocks:

```python
import json, io, sys

def blocks(path, min_len=400):
    out = []
    for line in io.open(path, encoding="utf-8", errors="replace"):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("type") != "assistant":
            continue
        for blk in (obj.get("message") or {}).get("content") or []:
            if isinstance(blk, dict) and blk.get("type") == "text" and len(blk.get("text", "")) > min_len:
                out.append(blk["text"])
    return out

found = blocks(sys.argv[1])
if not found:
    sys.exit("no assistant text block over 400 chars: lower min_len or check the path")
best = max(found, key=len)   # the report is almost always the longest block
print(best[:13000])          # print the tail separately if it is longer
```

Run it as `python recover.py <path-to-agent.jsonl>`.

## Why this works

Subagents write their report as an ordinary assistant text block in their transcript before the final
hand-back, which is the part that sometimes gets lost. The `type == "assistant"` filter skips tool
calls and results; the length filter skips status chatter. The longest block of 400+ characters is
reliably the report.

## Prevention

In background-agent prompts, say explicitly: "Your final message is the only thing returned to me. Put
the complete report in it, never 'done' or a pointer to earlier messages." Better still, ask the agent
to write its long report to a file and return the path. Both reduce the failure; neither removes it, so
keep this recovery handy.
