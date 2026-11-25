---
name: claude-token-audit
description: Show where Claude Code tokens and usage limits go, from the local session logs in ~/.claude/projects. Breaks usage down by project, session, day, model and tool, finds the biggest tool outputs flooding the context, measures cache hit rate and peak context per session, sizes what loads into every session (CLAUDE.md, MCP servers, skills), and gives specific fixes. Use when the user hits limits too fast, asks why usage is high, where tokens go, or how to make Claude Code cheaper.
---

# claude-token-audit

`scripts/token-audit.mjs` is zero-dependency Node 22+ and reads only local files. It takes about 4 s for 200 MB of logs.

```
node token-audit.mjs                    # last 30 days, all projects → token-audit.md
node token-audit.mjs --days 7
node token-audit.mjs --project myapp    # project folders containing "myapp"
node token-audit.mjs --out ~/usage.md
```

It prints the top recommendations and writes a full markdown report:
- totals (fresh input, cache writes, cache reads, output, cache hit rate) and the API-equivalent cost from Claude Code's own per-session counter
- **By project**, **Heaviest sessions** (with peak context size), **By model**, **By day**
- **Tool output fed back into context**: which tools flood the context window (Read, Bash, MCP…)
- **Biggest tool outputs**: the single results over ~5k tokens, with a preview so you can see what it was
- **Loaded into every session**: CLAUDE.md sizes, MCP server count, description size of the skills in `~/.claude/skills` and in installed, enabled plugins

## Reading the results with the user
- One API response is logged across several lines with the same usage. The script de-duplicates by message ID, so totals are not inflated.
- Subagent (Agent tool) transcripts in `<session>/subagents/` are included and counted under the session that launched them. Peak context is the main thread's.
- Cache reads cost ~10% of fresh input. A high hit rate (90%+) is good; long sessions are still expensive because *every* turn re-reads the whole context.
- Recommendations, in order of usual impact: one task per session (`/clear`), `/compact` before continuing long work, trim noisy command output (`| tail -50`, `-q`), read files with offset/limit, use Sonnet/Haiku for routine work and subagents, remove unused MCP servers and skills, keep CLAUDE.md short.
- "Cost" is the API-equivalent number Claude Code computes. On a subscription the user isn't billed that, but it tracks how fast they burn through limits.
- Token counts for tool output are estimates (~4 characters per token). Request totals come straight from the API usage fields.
