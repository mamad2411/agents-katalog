---
name: session-stats
description: Analyze Claude Code session data from ~/.claude/projects/ to surface usage patterns, heavy sessions, and context-limit problems. Use when the user asks about their Claude Code usage, token consumption, or why sessions keep hitting context limits or compacting.
---

# Session stats

Run the script next to this file and interpret what comes back:

```bash
python3 scripts/session_stats.py
```

When installed as a plugin the path is `${CLAUDE_PLUGIN_ROOT}/skills/session-stats/scripts/session_stats.py`. It reads every `.jsonl` under `~/.claude/projects/` and takes no arguments.

## Reading the output

The one thing that trips people up: **total tokens is dominated by cache reads**, which are re-counted on every assistant turn. A session showing hundreds of millions of "tokens" was not billed at that scale and did not process that much unique text — it means a large context was re-read many times. Output tokens and message count are the honest measures of how much work a session actually did; the total is best used as a relative signal of context weight, comparing sessions against each other rather than against an absolute number.

With that in mind, give the user a real read of their data rather than a restatement of the table:

- Which sessions look like they ran into context trouble — outlier context weight, or long duration paired with a high message count. Compare against the rest of *their* distribution, since what counts as heavy varies a lot between users.
- Which projects consume disproportionate context relative to how much they're used. Those are the candidates for a leaner CLAUDE.md or for pulling detail into skills that load on demand.
- Whether sessions are trending heavier over time, and whether one project drives the trend.

Then suggest fixes that follow from what you actually saw. Sessions that balloon in context usually want `/clear` at natural task boundaries or `/compact` before auto-compaction fires. Heavy cache-creation relative to peers points at a large always-loaded CLAUDE.md. Many tool calls per session points at verbose operations worth delegating to subagents. Very long single sessions are usually less effective than several focused ones — say so when the data shows it, and skip it when it doesn't.
