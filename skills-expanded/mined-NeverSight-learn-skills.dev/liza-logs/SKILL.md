---
name: liza-logs
description: Analyze Liza agents logs
---

SCOPE:
The logs in .liza/agent-outputs (nowhere else unless told otherwise explicitly),
The prompt may filter more specifically, e.g. a specific role and/or time range.

OBJECTIVE:
Finding recurring error patterns and proposing fixes.

PROTOCOL:
1. Start by running the analyzer:
```bash
python3 ~/.liza/skills/liza-logs/scripts/analyze-log.py .liza/agent-outputs/coder-*.txt        # all coder agents
python3 ~/.liza/skills/liza-logs/scripts/analyze-log.py .liza/agent-outputs/coder-1-*.txt # single agent
```
By default, run the analyzer per role.

Report sections: session header, token summary (fresh/cached/output, cache hit rate), content breakdown by type (chars, estimated tokens, share %), top 10 items by size, tool call frequency, MCP usage (per-server call count + error rate, result volume, top tools). Rich format adds per-turn context growth and cost breakdown.

2. Refine the analysis using the raw logs.
   - When referring to a specific session in your summary, include the log filename
     (for example `coder-1-20260417-171454.txt`) so the reader can trace the claim
     back to the exact source log quickly.

3. Before proposing a fix, check whether the fix is already implemented (e.g. an instruction already exists but agents ignore it):
   - Read one agent prompt of the relevant role in `.liza/agent-prompts/`
   - Check the contract files in `~/.liza/` (CORE.md, AGENT_TOOLS.md, MULTI_AGENT_MODE.md)

4. Propose fixes whenever possible.

FALSE POSITIVES:
- **Near-duplicate contract reads** (~8KB per session): Agents read AGENT_TOOLS.md, GUARDRAILS.md, etc. during initialization. These appear as "near-duplicate results" in the analyzer but are cache hits — negligible cost. Do not flag as waste.

NOTE:
The skill contains a web tool for humans to inspect logs: ~/.liza/skills/liza-logs/tools/liza-session-analyzer.html
