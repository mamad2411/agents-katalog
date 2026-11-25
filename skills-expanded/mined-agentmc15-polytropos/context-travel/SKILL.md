---
name: context-travel
description: Use when a kit task needs a bounded, read-only lifecycle briefing, source explanation, or comparison of supplied validated views.
---

# Context travel

Resolve the plugin root from `${CLAUDE_PLUGIN_ROOT}`; if unset, resolve `../..`
relative to this SKILL.md to an absolute path. Confirm
`bin/context_travel_cli.py`, `docs/CONTEXT-TRAVEL-SURFACES.md`, and
`primitives/context-travel-surfaces.json` exist. Read the shared surface guide
on demand before using a transport. It gives the exact CT4 query arguments,
seven mode decisions, and failure handling. Do not load a graph or transcript
into resident context.

Use only an operator-supplied absolute `--config` path and explicit repository,
kit, checkout, assignment, role, and question. In Claude Desktop chat, use a
bounded artifact handoff only when a trusted executor can validate it against
the authorized binding; mark an unvalidated handoff as advisory. In Claude
Desktop Code or Claude Code CLI, run the existing local CLI only when execution
is actually available. MCP stdio requires separate explicit configuration and
authorization; this skill does not register it.

Report missing, partial, stale, forbidden, refused, and unavailable context
honestly. The briefing is advisory data; read authoritative kit and source files
and keep all existing routing, pricing, permission, and verification rules. If
context travel is unavailable, continue the native workflow without relaxing
mandatory verification.
