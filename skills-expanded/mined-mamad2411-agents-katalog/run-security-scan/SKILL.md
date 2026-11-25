---
name: run-security-scan
description: Run code analysis via sl analyze or look up package CVEs (Intelligent SCA) via Qwiet. Invoke when the user runs /run-security-scan or explicitly asks for a cloud upload scan. Do NOT use for local PostToolUse hook findings, triage, or autofix — fix hook findings in the editor; use /triage-vuln and /autofix-vuln only after an explicit cloud scan workflow.
argument-hint: "[app] [branch]"
---

# Run security scan

**Code analysis** and **Intelligent SCA** via the **slmcp** MCP server (Qwiet API + Qwiet CLI). If MCP tools are missing, run `/setup-harness-code-security-mcp` first or see [mcp-setup.md](references/mcp-setup.md).

## Scope (this skill only)

Run **`sl_ensure_cli`** + **`sl_analyze`** (or package CVE lookup). You may call **`sl_list_findings`** once to give a **short scan summary** (`counts`, `top_actionable` titles).

**Stop here.** Do **not** deep-triage findings, fetch dataflows, read source for exploitability, or request AutoFix in this skill. MCP tools stay available, but the workflows for those steps live in other skills — see **Next step** below.

**Do not** run this skill or `sl_analyze` when PostToolUse (local Ocular scan after Edit/Write) already reported findings in this session — fix those in the editor with your Edit tool instead.

**Do not** run `hook-followup-suppress` in this skill — that helper is **only** for `/autofix-vuln` when applying cloud edits.

## Invoke `sl_*` tools (required)

Logical names like `sl_ensure_cli` are **MCP tools**, not shell commands.

1. If tools are deferred, use **ToolSearch** first (e.g. `select:...sl_ensure_cli,...sl_analyze,...sl_list_findings`).
2. Call each tool with a **native MCP tool invocation** using the **exact prefixed name** from ToolSearch (e.g. `mcp__harness-code-security-mcp__sl_ensure_cli` or `mcp__plugin_harness-sast-and-sca_slmcp__sl_ensure_cli`).
3. **Never** run `sl_*` via **Bash** — not `sl`, not `~/.shiftleft/sl`, not `npx harness-code-security-mcp`. Do not look for `.js` files under `handlers/`.
4. **Never** read `~/.shiftleft/config.json`, print `accessToken` / `orgId`, or call `app.shiftleft.io` / apiv4 from Shell. The MCP server already has credentials.
5. If ToolSearch returns tool references but invocation fails, run `/setup-harness-code-security-mcp` — do **not** guess shell paths. A host **timeout** is not a missing-tool failure — see **Host timeout** below.

## Prerequisites

- `sl auth` → `~/.shiftleft/config.json`
- **slmcp** MCP server (install with `/setup-harness-code-security-mcp`; also included in the Harness SAST and SCA Cursor/Claude plugins)

## Code analysis (`sl analyze`)

1. **`sl_ensure_cli`** — install or update the Qwiet CLI under `~/.shiftleft` (separate tool call so install errors return quickly with stderr traces).
2. **`sl_analyze`** — run `sl analyze --wait` in the workspace. Do **not** call `sl_list_applications` first — `sl` creates the app if needed.

Analysis runs on the local workstation; findings upload to Qwiet AI by Harness.

| Input    | Default when omitted            |
| -------- | ------------------------------- |
| `app`    | Workspace folder name           |
| `branch` | Current git branch, else `main` |

Example: `sl_ensure_cli` with `{}`, then `sl_analyze` with `{}` or `{ "app": "my-service", "branch": "feature/foo" }`.

### Scan id for triage (important)

`sl_analyze` returns **JSON** (not raw `sl` stdout). Use **`scan_id`** from that response for `sl_list_findings` and dataflow tools.

- **`scan_id`** — per-language API scan id (e.g. `"5"`) — **use this for findings**
- **`polyglot_scan_id`** — compound scan id sometimes printed in human `sl` output (e.g. `"6"`) — **do not** pass to `sl_list_findings`

If `scan_id` is missing, call **`sl_list_branch_scans`** and use **`latest.id`**.

When the user invokes this skill for a normal repo scan, run the workflow above — do not ask SAST vs CVE vs list-scans unless they asked for something else.

## Host timeout / MCP disconnect (required)

`sl_analyze` often takes **1–3+ minutes** (Java especially). slmcp waits up to **30 minutes**. The **agent host** (Cursor) may report a tool timeout much sooner and mark the MCP server **Not connected**.

That is **not** permission to leave MCP.

| May do | Must not do |
| --- | --- |
| Wait 30–60s, then retry **MCP** `sl_ensure_cli` / `sl_list_branch_scans` | Run `sl analyze` (or any `sl …`) via Shell |
| If a new scan exists, **MCP** `sl_list_findings` with **`latest.id`** (language scan id, not the UI/compound id) | Read `~/.shiftleft/config.json` or use `accessToken` |
| Tell the user to **reload the Cursor window** so plugin MCP reconnects, then stop | Call apiv4 / `app.shiftleft.io` from node/curl |
| Point at `/setup-harness-code-security-mcp` if tools stay disconnected | Grep plugin bundles, worktrees, or `handlers/` to reimplement tools |

**Stop this turn** after asking for a reload. Do not invent a CLI or HTTP fallback.

## Next step (required handoff)

After summarizing the scan, tell the user to run **`/triage-vuln`** — or invoke that skill yourself if the user said "triage" in a **new** message; do not continue triage on this turn. Some hosts prefix skills, for example `/harness-sast-and-sca:triage-vuln`.

Pass along **`app`** and **`scan_id`** from `sl_analyze`. Triage uses **`top_actionable[].id`** — not ids copied from a prose summary.

## Intelligent SCA / package CVEs

1. Build **PURLs** (e.g. `pkg:npm/lodash@4.17.21`)
2. **`sl_lookup_package_cves`** with `{ "purls": ["..."] }`
3. Summarize severities and fixed versions

## Notes

- **Harness SAST and SCA** extension / **Secure AI Coding** (on-save IDE analysis) is a different workflow — no `scan_id` from this MCP path
- **`sl analyze`** uses the project workspace as cwd when the MCP server starts
