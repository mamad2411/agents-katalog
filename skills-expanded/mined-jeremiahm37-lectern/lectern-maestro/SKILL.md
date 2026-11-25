---
name: lectern-maestro
description: "Use when the user explicitly chooses a Maestro workflow audit or improvement: diagnose, fortify, refine, reflect, agent-workflow, or teach-maestro."
disable-model-invocation: true
---

# Maestro for Lectern

Optional workflow guidance adapted from sharpdeveye/maestro. Original skill
files, references, MIT license, notice and pinned revision are in `upstream/`.
This adapter supplies skills; it does not install Maestro's editor extension or
MCP server, and does not create automatic audit or cost telemetry.

Invoke `/lectern-maestro <mode> <request>` in Claude Code or
`$lectern-maestro <mode> <request>` in Codex. Main modes:

| Mode | Outcome |
| --- | --- |
| `diagnose` | Assess the project's AI workflow and prioritize findings |
| `fortify` | Improve workflow reliability and error handling |
| `refine` | Improve prompt clarity and precision |
| `reflect` | Review available evidence from past workflow runs |
| `agent-workflow` | Consult workflow principles and supporting references |
| `teach-maestro` | Establish missing project workflow context |

If no mode was provided, show this menu and stop. For the selected mode:

1. Read `upstream/source/skills/agent-workflow/SKILL.md` relative to this file.
2. Read `upstream/source/skills/<mode>/SKILL.md` and follow it for the request.
3. Resolve reference links relative to that upstream skill's own directory.

Adaptation rules take precedence over the upstream instructions:

- A referenced command such as `/diagnose`, `/teach-maestro`, or
  `/agent-workflow` means load that mode's bundled SKILL.md through this adapter,
  not call an uninstalled slash command or MCP tool. All bundled modes can be
  resolved this way. Don't launch unrelated follow-up modes automatically.
- Read the existing AGENTS.md, CLAUDE.md, configured shared memory, project
  handoffs and any existing `.maestro/context.md` or `.maestro.md` first. Those
  sources can satisfy the context gathering protocol. Do not make a user repeat
  known answers, create a parallel memory store, or rewrite project instructions.
- `teach-maestro` may propose missing context, but use the established project
  context system for durable updates. Create `.maestro.md` only if explicitly
  requested; never overwrite existing context. Report findings in the current
  session by default.
- `reflect` uses actual available session records and project artifacts. If
  `.maestro/audit.jsonl` or decisions are absent, say so; do not fabricate run
  counts, spend, outcomes or quality measurements.
- Upstream tool-count and context-budget suggestions are heuristics. Judge
  findings against this project's evidence and configurable tools. Preserve
  existing agent permissions, shared memory and verification requirements.
- Enabling this feature makes guidance available. It does not run an audit,
  change application behavior or replace Lectern's execution/review system.

Disabling removes only the owned skill attachment. Project documents and any
existing Maestro records remain intact. Start a new agent session after toggling.
