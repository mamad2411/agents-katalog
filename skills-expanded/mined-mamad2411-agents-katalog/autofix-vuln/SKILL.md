---
name: autofix-vuln
description: Request or fetch Qwiet recommended fixes and branch autofixes. Invoke when the user runs /autofix-vuln or explicitly asks for cloud AutoFix after triage. Do NOT use for local PostToolUse hook findings — fix those in the editor. Do NOT call sl_get_recommended_fix* without this skill active.
argument-hint: '<app> <finding-id> [branch]'
---

# AutoFix

Uses **slmcp** AutoFix APIs. Requires **app** and finding ids from triage (`top_actionable[].id`). If MCP tools are missing, run `/setup-harness-code-security-mcp` first. MCP setup: [mcp-setup.md](references/mcp-setup.md).

**Invoke `sl_*` as MCP tools** (ToolSearch + native tool call with the host-prefixed name). **Never** run them via Bash.

## When to run this skill

The user (or you) must invoke **`/autofix-vuln`** so this file is loaded. Some hosts prefix skills, for example `/harness-sast-and-sca:autofix-vuln`. If they ask for autofix or "recommended fixes" after triage **without** a slash command, **invoke this skill** first — do **not** jump straight to `sl_request_finding_fix` / `sl_get_recommended_fixes` from the prior turn's context alone.

Prerequisite: **`/triage-vuln`** should have produced **`top_actionable`** ids. If not, re-run **`sl_list_findings`** for the scan and read **`top_actionable[].id`**.

**Do not** invoke this skill or `sl_request_finding_fix` when PostToolUse local hooks already reported findings after an edit — fix those in the editor. Cloud AutoFix requires platform finding ids from an explicit `/run-security-scan` + `/triage-vuln` workflow.

## Which findings to fix

Fix **all** `top_actionable` ids from triage unless the user narrows scope — **SAST, SCA, and OSS risk** (including `pkg:...` titles). Use the same Qwiet AutoFix path for every id.

Collect ids from **`top_actionable[].id`** only — never from prose summaries.

## Hook follow-up suppress (plugin only — required before edits)

While AutoFix applies **`edits[]`**, a **Harness SAST and SCA plugin** with hooks enabled runs **PostToolUse** local scans on edited files. Those scans queue findings and inject inline messages; the **stop** hook can then inject a “fix findings” follow-up — all of which fight cloud AutoFix.

**This skill does not ship suppress tooling.** Standalone skill installs can skip this section. When the **Cursor or Claude plugin** is installed, **you must** suppress hook gathering and stop follow-up for the current agent session:

**Before** applying cloud **`edits[]`** (plugin `handlers/` directory):

```text
node "<plugin-root>/handlers/hook-followup-suppress.js" on
```

**After** all fixes (success, partial, or failure):

```text
node "<plugin-root>/handlers/hook-followup-suppress.js" off
```

`off` is **deferred until the Stop hook** on this turn (suppress stays active through your summary message). The Stop handler clears it automatically; you do not need to wait for the next turn.

Examples:

- **Claude plugin:** `node "${CLAUDE_PLUGIN_ROOT}/handlers/hook-followup-suppress.js" on`
- **Cursor plugin:** `node "<path-to-cursor-plugin>/handlers/hook-followup-suppress.js" on`

The script is **Node.js** (Windows/macOS/Linux). By default it **exits 0** when the hook bus is unavailable (skills-only, or no `sessionStart` yet) — autofix continues without suppress. Pass **`--strict`** to fail instead.

State lives under **`~/.shiftleft/hook-bus/`**, keyed by session (`QWIET_HOOK_BUS_SESSION` from plugin **sessionStart**). While suppress is on, **PostToolUse gathering** (local scans, pending queue, inline hook messages) and the **stop** hook’s auto follow-up are skipped.

Advanced: `node "<plugin-root>/handlers/hook-bus.js" suppress-on|suppress-off|clear-session|status`

## AutoFix workflow (request → poll → apply)

Prefer **generating** fixes on the platform, not only reading stale recommendations.

### 1. Request fixes (write)

For each finding id (or any id with no ready fix yet), call **`sl_request_finding_fix`** with `{ "app": "...", "finding": "..." }`.

You may batch requests in parallel (one tool call per finding).

### 2. Poll until ready

Poll **`sl_get_recommended_fixes`** in batches of up to **5** ids: `{ "app": "...", "findings": ["id1", "id2", ...] }`.

- Repeat until every finding has **`apply_mode`** **`ready`** or **`partial`**, or **`status`** indicates failure.
- Between polls, use a short wait (e.g. Bash `sleep 3`) — fixes are async on the platform.
- If **`apply_mode`** is **`markdown_only`**, ensure **`WORKSPACE_FOLDER`** (or **`CURSOR_WORKSPACE_FOLDER`**) points at the scanned repo root and poll again.

**Single finding:** **`sl_get_recommended_fix`** with `{ "app": "...", "finding": "..." }`.

### 3. Apply fixes automatically

When **`apply_mode`** is **`ready`**, each finding includes **`edits[]`**:

- **`file`** — path relative to the workspace root
- **`old_string`** / **`new_string`** — exact strings for your file **Edit** tool

**Do not** paste the fix as markdown and ask whether to apply — apply **`edits[]`** directly (same file: apply **bottom-to-top** by `start_line` so offsets stay valid).

If **`apply_mode`** is **`partial`**, apply available **`edits[]`** and use **`fix_markdown`** for the rest.

If Qwiet returns no applicable AutoFix after polling, summarize **`fix_markdown`** / **`fix_notes`** when present and note the finding for manual follow-up in the Qwiet app — do **not** substitute `npm audit`, `npm audit fix`, or other non-Qwiet dependency tooling unless the user explicitly asks outside this skill.

## Branch AutoFixes

**`sl_list_branch_autofixes`** with `{ "app": "...", "branch": "..." }` (compact summary by default)

Default branch from git when omitted.

## After fixes

- If you used hook follow-up suppress, run **`hook-followup-suppress.js off`** (plugin only)
- Apply **`edits[]`** for every finding that returned them; summarize what changed
- Suggest **`/run-security-scan`** to verify — do not commit unless the user explicitly asks

## Workflow order (reference)

1. **`/run-security-scan`** — `sl_analyze`, brief summary, save `scan_id`
2. **`/triage-vuln`** — `top_actionable`, dataflows, ranked list
3. **`/autofix-vuln`** — this skill
