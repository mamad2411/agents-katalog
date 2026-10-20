---
name: mcp-governance
description: Use when considering adding an MCP server, when context feels bloated with tool definitions, when auditing which servers consume the most context budget, before committing mcp_config.json changes, or when deciding which servers to keep active per task. Estimates per-server tool-definition token cost and guides lazy enablement.
triggers: [user, model]
---

# MCP Governance

Every MCP server injects **all its tool definitions** into the system prompt
of every conversation — even when unused. Two "plug-and-play" servers can eat
a third of a 200k window before the first user message. Audit before adding;
keep only what earns its tokens.

**Principle:** MCP servers should be active only when a task needs them.
Default state: minimal or zero MCP servers. Enable on demand; disable when
done.

Rule of thumb: **tool count per server under 10-15** keeps tool-selection
accuracy above 90% (arXiv:2606.30317). A 5-tool server with huge descriptions
can still cost more than a 15-tool terse one — measure token cost, not just
count.

## Audit workflow

1. **List configured servers:**
   `python3 "{{APPDATA}}/devin/skills/mcp-governance/scripts/mcp-context-audit.py" --config mcp_config.json`
   Reports transport, command/url, static bloat risk. No tool calls made.
2. **Measure real tool counts:** `mcp_list_tools server_name="<srv>"`, then
   pipe the tool list to the estimator:
   `python3 ".../scripts/mcp-context-audit.py" --tools tools_<srv>.json`
   Estimates token cost (chars/4) and flags >10-15 tools.
3. **Decide:**

   | Signal | Action |
   |---|---|
   | Server unused in N sessions | Remove from `mcp_config.json` |
   | Tool count > 15 | Prefer narrower server or scope tools |
   | Token cost > 5% of window | Justify with concrete usage; else remove |
   | Untrusted server | Review code/permissions first; sandbox |

4. **Verify after removal:** re-run step 1; confirm budget dropped
   (`context-budget.py --full`).

## Lazy enablement workflow

1. **Classify each server:**

   | Classification | Criteria | Action |
   |---|---|---|
   | Always-on | Used in >50% of sessions, cost <3% of window | Keep |
   | On-demand | Specific task types (Jira, database, deploy) | Enable only for those tasks |
   | Rarely used | <10% of sessions | Remove; re-add when needed |
   | Never used | Configured but never invoked | Remove immediately |

2. **Disable temporarily:** move the server entry from `mcp_config.json` to
   `mcp_config.disabled.json`, restart session; move back when needed.
3. **Plugin installs:** `devin plugins info <name>` shows which MCP servers a
   plugin provides — factor that cost into keeping the plugin.
4. **Verify savings:** re-run `context-budget.py --full`.

Decision heuristic: task starts → needs MCP tools? NO → minimal servers
active. YES → enable only what's needed → audit cost → work → disable.

## Anti-patterns

- Keeping all servers always-on "just in case" — the #1 cause of MCP bloat.
- Auditing once and never again — servers grow tools over time.
- Adding servers without measuring before/after.
- Trusting tool count alone — check token cost.
- Skipping the trust review — MCP servers run with user permissions; evaluate
  architecture patterns/anti-patterns before adding.
- Treating MCP config as immutable — it's a living config.

## Source

Tool-count accuracy threshold: arXiv:2606.30317. Context tax framing: Matt
Pocock, "Context Windows Explained for Coding Agents".
