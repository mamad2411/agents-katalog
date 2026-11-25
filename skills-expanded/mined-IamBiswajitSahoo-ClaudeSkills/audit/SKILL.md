---
name: audit
description: Security audit for Claude Code skills, MCP servers, hooks, and CLAUDE.md files — runs fast pattern scan then parallel deep-analysis agents. Use when the user wants to vet a skill or MCP server before installing it, or check their Claude Code setup for risky hooks or instructions.
metadata:
  author: Biswajit Sahoo (https://github.com/IamBiswajitSahoo)
  license: Apache-2.0
argument-hint: "<mode> [target]  — modes: skill <path|url>, mcp [server|package], hooks, claudemd, all"
---

# Security Audit

Audit Claude Code extension surfaces (skills, MCP servers, hooks, CLAUDE.md) for security risks. Quick pattern scan first, then optional parallel deep analysis.

## Phase 1 — Parse & route

**Prereq:** verify Python 3 with `python3 --version 2>/dev/null || python --version 2>/dev/null`. Store the working command as `{PY}`. If neither works or it's Python 2.x, stop and tell the user to install Python 3.

**Parse `$ARGUMENTS`** for `<mode> [target]`:
- Modes: `skill`, `mcp`, `hooks`, `claudemd`, `all`.
- Targets (skill/mcp only): local path, GitHub URL, GitHub subdirectory URL (e.g. `.../tree/main/skills/x`), or npm package `@scope/pkg` (mcp only).
- If mode is missing/invalid, ask via `AskUserQuestion` with the 5 modes.
- If `skill` or `mcp` with remote target and no local target given, ask for one.

**Resolve target** (skill/mcp with target):

```bash
{PY} "${CLAUDE_SKILL_DIR}/scripts/resolve-target.py" "<target>" --type <skill|mcp>
```

Returns `{source, resolved_path, is_temporary, temp_root, error}`. On `error`, stop. If `is_temporary`, remember `temp_root` for Phase 4 cleanup and tell the user the target was downloaded.

For `mcp` without target: run `gather-mcp-config.py` — if no servers, stop with "No MCP servers configured". For `hooks`/`claudemd`: no resolution needed.

## Phase 2 — Quick scan

Run the relevant gather + pattern-scan scripts in parallel (multiple `Bash` calls in one message):

| Mode | Gather | Pattern scan |
|---|---|---|
| skill | `gather-skill-inventory.py <path>` | `pattern-scan.py <path> --type skill` |
| mcp | `gather-mcp-config.py <server-or-empty>` | `pattern-scan.py <src>` per server with local files |
| hooks | `gather-hooks-config.py` | `pattern-scan.py <script>` for each referenced script |
| claudemd | — | `pattern-scan.py ./CLAUDE.md --type skill` (+ `.claude/CLAUDE.md` if present) |
| all | all four gather scripts in parallel | `pattern-scan.py . --type plugin` |

All scripts are `{PY} "${CLAUDE_SKILL_DIR}/scripts/<name>" ...`.

**Show summary:**

```
## Quick Scan Results
Risk Score: {score}/100 — {verdict}
Files scanned: {files_scanned}
Pattern matches: {critical} critical, {high} high, {medium} medium, {low} low
```

If SAFE (0–20): "No suspicious patterns detected." If CAUTION+: list top 3 findings by severity.

**Ask next step** via `AskUserQuestion`:
- SAFE: **Deep scan** / **Done**
- CAUTION+: **Deep scan (recommended)** / **Show findings** / **Done**

**Done** → Phase 4 with quick-scan results only. **Show findings** → print all findings by severity, then stop.

## Phase 3 — Deep analysis (parallel)

Read templates from `${CLAUDE_SKILL_DIR}/templates/`:

| Mode | Template(s) | Agent(s) to launch |
|---|---|---|
| skill | `agent-skill-audit.md` | 1 skill audit agent |
| mcp | `agent-mcp-audit.md` | 1 MCP audit agent |
| hooks | `agent-hooks-audit.md` | 1 hooks audit agent |
| claudemd | `agent-claudemd-audit.md` | 1 CLAUDE.md audit agent |
| all | all four | up to 4 agents in parallel |

Launch all agents in a single message with parallel `Agent` calls. Each agent receives: its template instructions + relevant quick-scan JSON + inventory/config JSON + target path. Use `"model": "sonnet"` and a descriptive `description` per agent.

Wait for completion. Merge findings, sort by severity (Critical > High > Medium > Low > Info). Note any failed/timed-out agents in the report but continue.

## Phase 4 — Report & cleanup

**Combined score:** start with pattern-scan score, add weight for new deep findings, cap at 100.

| Score | Verdict |
|---|---|
| 0–20 | **SAFE** — no significant concerns |
| 21–40 | **CAUTION** — minor concerns |
| 41–60 | **SUSPICIOUS** — manual review recommended |
| 61–80 | **DANGEROUS** — do NOT install without expert review |
| 81–100 | **MALICIOUS** — avoid |

Build the report using `${CLAUDE_SKILL_DIR}/templates/report.md`. Sections: header (target, date, mode, score, verdict), scope audited, critical/high findings in full, medium/low and info in `<details>` blocks, clean signals, recommendations.

If DANGEROUS or MALICIOUS, prepend:

> **WARNING:** This audit found serious security concerns. Do NOT install or use this without careful manual review.

Include the original GitHub URL or npm package name in the header if the target was remote.

**Cleanup:** if `is_temporary` was true, `rm -rf "<temp_root>"`.

## Rules

- **Never auto-remediate** — report only, never modify files.
- **Never fabricate** — only report what's observed.
- **Quick scan always first**, even if deep scan will follow.
- **Parallel agents** when multiple surfaces are in scope — never sequential.
- **Sonnet for sub-agents.** Critical > Info ordering in findings.
- **Scope discipline** — auditing a skill does not scan the whole filesystem.
- **Respect the user** — if they say Done, stop; don't push deep analysis.
- **Context matters** — a deployment skill needing Bash is normal; a text-formatting skill needing Bash is suspicious. Assess purpose vs. permissions.
