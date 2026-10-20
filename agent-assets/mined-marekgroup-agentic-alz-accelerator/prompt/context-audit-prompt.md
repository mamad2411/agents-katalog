---
description: "Audit agent context window utilization from Copilot Chat debug logs and produce optimization recommendations."
agent: orchestrator
---

# Context Window Audit

Analyze Copilot Chat debug logs to identify context bloat, redundant file reads, and optimization
opportunities across agents.

## Prerequisites

- Copilot Chat debug logging enabled in VS Code
- Log files at `~/.vscode-server-insiders/data/logs/*/exthost1/GitHub.copilot-chat/`
- Or use `$VSCODE_TARGET_SESSION_LOG` for the current session

## Instructions

1. Read `.github/skills/context-optimizer/SKILL.md` for audit methodology.
2. Parse the debug log using the skill's log parser:
   ```bash
   python3 .github/skills/context-optimizer/scripts/parse-chat-logs.py \
     --log-dir ~/.vscode-server-insiders/data/logs/ \
     --latest 3 --summary-only
   ```
3. Analyze the parsed output for:
   - Token counts per agent invocation (latency as proxy)
   - Burst patterns (rapid sequential calls suggesting tool-call loops)
   - Latency escalation (context growing without hand-offs)
   - Model usage distribution (Opus vs mini routing)
4. For deeper analysis, read:
   - `references/analysis-methodology.md` — log format, optimization patterns
   - `references/token-estimation.md` — token cost heuristics, warning thresholds
5. Identify optimization opportunities:
   - Agents exceeding 60% context (latency > 15s on Opus)
   - Redundant file reads (same file loaded multiple times per session)
   - Missing hand-off points (context not delegated to subagents)
   - Oversized skill/instruction loading (candidates for digest variants)
6. Produce a report using `templates/optimization-report.md` as the template.
7. Save the report to `logs/copilot/context-audit-{date}.md`.

## ALZ-Specific Checks

- Verify agents with `<context_awareness>` blocks are loading `SKILL.digest.md`
  or `SKILL.minimal.md` when appropriate (not always full `SKILL.md`).
- Check if compression templates from `context-shredding` are being applied at gates.
- Verify `alz-recall` CLI is used for state queries instead of reading raw JSON files.

## Constraints

- Read-only analysis — do NOT modify agent definitions or skill files.
- Produces recommendations only — user decides what to implement.
- Reusable across sessions — compare reports over time to track improvement.
