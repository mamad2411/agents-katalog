---
name: triage-vuln
description: List and explain findings from a scan with data flow. Invoke when the user runs /triage-vuln or says triage, review findings, or investigate finding ids after a scan. Do NOT satisfy triage by calling sl_* tools without this skill active; run /triage-vuln first.
argument-hint: "<app> <scan> [finding-id]"
---

# Triage findings

Uses **slmcp** against the Qwiet API. Requires completed **code analysis** (`/run-security-scan`; some hosts may prefix the skill name). If MCP tools are missing, run `/setup-harness-code-security-mcp` first. MCP setup: [mcp-setup.md](references/mcp-setup.md).

**Invoke `sl_*` as MCP tools** (ToolSearch + native tool call with the host-prefixed name). **Never** run them via Bash. **Never** read `~/.shiftleft/config.json` or call apiv4 from Shell. See `/run-security-scan` for the same rule (including host timeout: wait and retry MCP, do not invent a CLI fallback).

## When to run this skill

The user (or you) must invoke **`/triage-vuln`** so this file is loaded. Some hosts prefix skills, for example `/harness-sast-and-sca:triage-vuln`. If the user says "triage", "review findings", or "explain finding X" after a scan **without** a slash command, **invoke this skill** (Skill tool or ask them to run the slash command) — do **not** call `sl_get_findings` / `sl_get_finding_dataflows` from memory of the prior scan turn alone.

## Inputs

- **app** — same id used for the scan (workspace folder name or user-provided)
- **scan** — from `sl_analyze.scan_id` or `sl_list_branch_scans.latest.id`
- **finding** (optional) — API finding id for a single deep-dive (not rank 1/2/3)

## Workflow

### List findings

**`sl_list_findings`** with `{ "app": "...", "scan": "..." }`

- Read **`counts`** for severity/category overview
- Use **`top_actionable`** for critical/high SAST, SCA, and OSS risk (e.g. malicious packages) — real **`id`** values
- If **`top_actionable`** is empty, read **`actionable_query_warnings`** and **`counts`** — do **not** jump to `full: true`
- Do **not** use `full: true` unless the user explicitly needs the raw API payload

### Multiple findings (preferred)

**`sl_get_findings`** with `{ "app": "...", "findings": ["id1", "id2", ...] }` (max 10)

Pass ids from **`top_actionable[].id`**, not ordinal labels.

### Single finding

**`sl_get_finding`** with `{ "app": "...", "finding": "..." }` when you only need one.

### Data flow

- One finding: **`sl_get_finding_dataflow`** with `{ "app", "finding", "scan" }`
- Several: **`sl_get_finding_dataflows`** with `{ "app", "scan", "findings": [...] }` (max 5)

Present **source → steps → sink** from compact `nodes` when present.

## Output

- Ranked short list of findings to fix first (from `top_actionable` and `counts`)
- Per deep-dive: impact, location, fix direction

## Next step (required handoff)

When triage is complete, tell the user to run **`/autofix-vuln`** for remediation (or invoke that skill on a **new** turn if they ask for autofix). Some hosts prefix skills, for example `/harness-sast-and-sca:autofix-vuln`.

Pass **`app`** and **all** finding ids from **`top_actionable[].id`** (code + OSS) — not ids guessed from an earlier scan summary. AutoFix should request and apply fixes for the full list unless the user asked for a subset.
