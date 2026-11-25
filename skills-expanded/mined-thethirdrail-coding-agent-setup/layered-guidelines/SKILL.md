---
name: layered-guidelines
description: |
  Use when a task involves focused coding-agent guardrails beyond the lean global instructions:
  testing and verification, security/secrets/auth/privacy, dependency or environment setup,
  runtime errors/logging/observability, documentation/runbooks, archive/continuity/handoff,
  MCP/tool-use discipline, or deciding which focused guideline lane applies. Activate only
  the relevant reference lane and avoid loading unrelated guidance.
---

# Layered Guidelines

This is a compact router skill for focused operational guidance that should not live in the always-on `AGENTS.md`.

Use this skill when the task touches one of the focused guideline lanes below. Load only the needed reference file.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| Agent discipline | `agent-discipline.md` | When a task needs extra guardrails for assumptions, surgical edits, escalation, or concise reporting. |
| Testing and verification | `testing.md` | When implementing, fixing, refactoring, reviewing, or claiming completion. |
| Security and sensitive data | `security.md` | When touching secrets, auth, permissions, privacy, payments, user data, or security posture. |
| Environment and dependencies | `environment.md` | When installing packages, changing setup, selecting tooling, or dealing with project environments. |
| Runtime observability | `runtime-observability.md` | When changing errors, logs, runtime behavior, API failures, or release-readiness diagnostics. |
| Archive and continuity | `archive-continuity.md` | When work creates durable context, handoff notes, setup decisions, or long-running project memory. |
| Documentation | `documentation.md` | When behavior, commands, setup, env vars, or usage changes need docs/runbooks. |
| MCP and tool use | `mcp-tool-use.md` | When deciding whether to use MCP, Serena, Docker MCP, docs lookup, or other configured tools. |

## Loading Protocol

1. Match the task to the narrowest guideline lane.
2. Read only `references/<lane>.md` for that lane.
3. Compose lanes only when the task genuinely crosses responsibilities.
4. Do not use this skill as a reason to broaden scope, refactor unrelated code, or add ceremony.
5. State the loaded lane only when it matters for auditability, handoff, or recovery.

## Non-Goals

- This skill does not replace `AGENTS.md`.
- This skill does not replace Codex `default.rules` command policy.
- This skill does not contain project-specific framework rules.
- This skill should not be loaded for trivial edits where the global rules are sufficient.
