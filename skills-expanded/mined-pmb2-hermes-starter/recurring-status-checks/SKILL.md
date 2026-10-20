---
name: recurring-status-checks
description: >-
  Run recurring cron-based status checks across multiple stakeholders, leads, or
  services when live polling is unavailable. Covers freshness detection, state
  reconstruction from offline sources, delta analysis, escalation tracking, and
  report delivery/archival.
version: 1.2.0
author: Chief of Staff
metadata:
  hermes:
    tags: [cron, reporting, status-checks, escalation, tracking, weekly, recurring]
    triggers: [cron-status, weekly-checkin, recurring-report, status-reconstruction, offline-polling, multi-stakeholder, status-check]
    related_skills: [discord-report-format]
---

# Recurring Status Checks

Run recurring status checks (weekly council check-ins, daily briefs, watchdog reports) when live polling of stakeholders is unavailable. The agent reconstructs state from offline sources, detects changes from the last report, tracks escalation across consecutive runs, and delivers a compact actionable report.

## Overview

When a cron job fires and expects to poll N stakeholders but no live messaging channel is available, follow this reconstruction pipeline instead of attempting (and failing at) live polling.

## Phase 0: Freshness Check

Always start by checking whether the last report is still current. If nothing has changed, stay silent.

1. `session_search(query="<report name>", sort="newest", limit=1)` — find the last delivery
2. Read the last output via `session_search(session_id, around_message_id)` — examine its content and timestamp
3. If the same findings would be repeated, respond `[SILENT]` (agent cron) or exit silently with no output (no_agent script)

## Phase 1: Gather Baseline

Reconstruct the state of each stakeholder/lead from available offline sources:

- **Previous report(s)** — read last 1-2 archived reports for baseline state, tracked items, escalation counters
- **Memory files** — read each stakeholder's memory.md for structural context (projects, blockers, dependencies, key contacts)
- **gbrain** — query for any new pages or updates since last check. Also check brain health (`get_health()`) — if brain_score < 60 or orphans > 50% of pages, run the cross-link repair workflow before proceeding. See `references/pulse-brain-health-remediation.md`.
- **Past sessions** — search for recent conversations involving the stakeholders

For each stakeholder, collect:
- Current status (✅/🟡/🔴)
- Active blockers with days unresolved
- Needs from the operator or other leads
- Key metrics if available

## Phase 2: Detect Activity Signals

Check for changes since the last report:
- **Git logs** — `git log --since="<last report date>"` in relevant repos
- **File timestamps** — check if memory files or report directories have been modified
- **Related reports** — read recent daily briefs, pulse reports, or other periodic reports for interim changes
- **System state** — container counts, service health, any monitoring data available

## Phase 2a: Script Failure / CLI-Limited Fallback

When the designated data-collection script is missing, broken, returns an error code, **produces template stubs with placeholder values** (e.g. `{{description}}`, `{{amount}}`), or the CLI tool lacks the filtering you need (e.g. `--limit` but no `--days` flag), do NOT abort the report. Fall back to manual data gathering from alternative sources:

**Silent-stub detection:** A script that exits 0 and writes a file is NOT necessarily working. After a data-collection script runs successfully, always verify the output contains real data, not template placeholders. Check for pattern markers like `{{...}}`, `TODO`, `PLACEHOLDER`, or boilerplate headers with no filled-in values. If the output is a stub, treat it as a script failure and escalate accordingly.

- **Direct SQLite DB query** (fastest) — query the project's backing database directly with SQL for accurate date-bounded aggregation. Run `#!python from pathlib import Path; [list(p for p in Path('.').rglob('*.db'))]` to find all databases. See `references/direct-db-query-pattern.md` for the full pattern: how to find DBs, detect date columns, aggregate by source across time windows, and compare two periods. Keep the reference open so you can reuse the SQL patterns without memorizing them.

- **Git activity** — enumerate ALL repos under the user's GitHub/projects root (e.g., `for d in /path/to/github/*/; do git -C "$d" log --since="<interval>" ...`) and report every repo with commits. Do not hardcode a repo list.

  **⚠️ Large-repo-collection fallback:** On systems with 100+ repos, a full iterative `git log` scan gets killed (SIGTERM/exit 15) before finishing. When the full scan fails, use this fast fallback sequence:
  **Known reliability gap: `find + xargs` with `bash -c` can silently return empty** even when repos have commits. This happens on MSYS2/Windows due to path translation in nested shells, quoting issues in xargs, or the process being killed before completing. Do NOT trust a zero-result from xargs — always double-check with the steps below.

  1. **File-timestamp gate** — check `.git/HEAD` modification timestamps with `find -newer` against a recent reference file. Fast (no git commands), catches any repo with new commits.
  2. **Targeted repo checks** — even when the file-timestamp gate returns empty, explicitly check the 5-10 most active repos individually with direct `git log`. For the operator's environment these include `website-landlord`, `_project`, `hermes-agent`, and `scroll-world-*` repos.
  3. **Working tree check** — `git status --short` on key repos (catches uncommitted work staged or started overnight)
  4. **File timestamp check** — as a final cross-check, use `find /path/to/github/website-landlord -mmin -240 -type f | head -20` to catch uncommitted doc changes
  5. Only expand to a full scan if the fast checks found something worth investigating
- **MCP endpoints** — query available business-intelligence MCP servers (e.g., BizDev dashboard for pipeline stats, CRM connectors for contact/opportunity counts). These bypass the broken script and provide real operational data.
- **session_search** — search for recent sessions involving the report's topic, previous iterations of this same cron job, and any user activity since the last report. Provides context the script would have gathered.
- **File/directory inspection** — check watchdog state files (`.last_check` timestamps), import logs, and pipeline data files for staleness. Flag anything older than 7 days.
- **Cron job prompt itself** — the user's instructions and priorities passed into the prompt are authoritative context. Use them as the baseline for what matters.

**Data source priority order:**
1. MCP endpoints (structured, real-time operational data)
2. Git activity (confirms real work happened)
3. session_search (context and history)
4. File inspection (system state and pipeline health)
5. Web/blog/intel (external — last resort)

Attempt sources in order until sufficient data is collected. Combine evidence from multiple sources rather than aborting after one.

**Recording the failure:** Always note the script failure in the report header. Use `❌` for first occurrence, `⚠️` for second consecutive, `🔴` for third+ consecutive with the same error.

## Phase 3: Delta Analysis

Compare current state against the last report. Specifically:

- **New blockers** — items not present in last report
- **Resolved items** — things that were blocked and are now unblocked
- **Metric drift** — revenue, expenses, pipeline values, deadlines
- **Priority shifts** — items that were urgent and are now dropped or downgraded
- **Silent abandonment** — items that disappeared from daily briefs or other intermediate reports without resolution

## Phase 4: Escalation Tracking

Maintain a per-issue escalation counter across consecutive reports:

| Run | Issue | Weeks Flagged | Action Taken? | Level |
|-----|-------|--------------|--------------|-------|
| 1 | Tax Payment | 1 | No | 🟢 |
| 2 | Tax Payment | 2 | No | 🟡 |
| 3 | Tax Payment | 3 | No | 🔴 |
| 4 | Tax Payment | 4 | No | ❌ Deadline passed |

**Escalation levels:**
- 🟢 First flag — recommendation only
- 🟡 Repeated (2-3 runs) — note "no action taken"
- 🔴 Critical (4+ runs) — escalate language, highlight in header
- ❌ Deadline passed — mark as permanent failure with penalty assessment

For each consecutive run on the same issue, the tone should escalate. Use phrases like "Xth consecutive report with zero action" rather than restating the same neutral recommendation.

**Script/automation failures** also follow the escalation ladder. Track each distinct failure (by script path or error message) as a separate escalation item:

| Run | Failure | Count | Action Taken? | Level |
|-----|---------|-------|--------------|-------|
| 1 | `daily_brief.py` not found | 1 | No | 🟢 |
| 2 | `daily_brief.py` not found | 2 | No | 🟡 |
| 3 | `daily_brief.py` not found | 3 | No | 🔴 |

When a script failure appears 3+ times with the identical error, escalate language to name the specific script path, state the consecutive count, and recommend a concrete fix. At 🔴 level, include a one-line fix recommendation (e.g., "3rd failure: `scripts/scripts/daily_brief.py` — double-nested path mismatch. Consider fixing path or replacing with manual-fallback cron prompt.").

## Phase 5: Report Production

Produce the report following the `discord-report-format` conventions:
- Compact, one-line-per-item format
- No blank lines between items
- No em dashes
- Emoji + bold for section headers
- Always include a Recommended Actions section (2-4 items)
- Timestamp in ET (America/New_York)

**Required sections for any status check:**
1. Header with emoji + bold + timestamp
2. At-a-Glance table (one line per stakeholder/lead)
3. Blockers/recommendations
4. Escalation tracker for repeat items
5. Recommended Actions (2-4 concrete next steps)

## Phase 6: Archive

1. Write the full report to the designated archive directory
2. Use the naming convention: `YYYY-MM-DD-<report-name>.md`
3. Verify the file was written
4. Reference the archive path in the delivery message

## Pitfalls

- **Don't assume live polling works.** In cron context the user is not present. Always use offline reconstruction.
- **Don't restate the same recommendation identically each week.** Escalate language when an issue appears in consecutive reports with zero action.
- **Don't ignore silent abandonment.** When daily briefs or intermediate reports stop referencing previously-flagged items, note it explicitly in the next status check.
- **Don't report stale data as current.** Check file timestamps and flag staleness in days. If memory files haven't been updated, say "X days stale."
- **Don't produce long reports.** The user reads these in seconds. At-a-glance first, details on request.
- **Don't report on every stakeholder identically.** Lead with the moving parts. Stakeholders with no change since last report can be noted briefly.
- **Don't skip the Recommended Actions section.** This is what drives decision-making. Include timeframe and owner.
- **Don't treat script failures as fresh each time.** Check session_search for previous runs of this same cron job. If the identical error appeared before, escalate the language from the start. A script that fails identically 3 times is a systemic issue, not a transient error.
- **Don't rely on session_search for cron-delivery freshness checks.** Cron job outputs are delivered directly to Discord/messaging, NOT stored in the Hermes session DB. `session_search` will find nothing for a cron job's own past deliveries — it only captures assistant-user dialog turns. For freshness detection in cron context, use: daily digest files, archive directories, or watchdog state files (`.last_check` timestamps) instead.
- **Don't iterate 100+ repos with git commands.** The `for d in .../*/` loop and `find + xargs` approaches both get killed (SIGTERM/exit 15) on large repo collections. Use the file-timestamp gate (`find .git/HEAD -newer`) for a fast pre-filter, then expand to targeted repo checks only when the gate finds something.
- **On Windows/MSYS2, don't use MSYS2-style paths (`/e/`, `/c/`) when calling Python utility scripts from bash.** Windows-native Python resolves `/e/` to `C:\e\` (relative to the system drive), not `E:\`. This breaks digest-append, data-collection, and reporting scripts. **Safe pattern:** use Windows drive-letter format with forward slashes — e.g., `python ${MY_REPOS}/Documents/github/_project/scripts/append-digest.py "Pulse" "findings"` — or use the full Windows path `E:\...` with escaped backslashes. Verify the script resolves before passing arguments.
- **Don't use `pip show <package>` to detect the latest upstream release** — `pip show` reports the locally installed version, which may be multiple releases behind GitHub. For release-notes verification, query GitHub Releases: `gh release list --repo <org>/<repo> --limit 3` or the GitHub API `releases/latest` endpoint. Add the confirmed tag to the **Checked:** footer so the user can see which version is being tracked.
- **Don't use `write_file` to append to a daily digest or other multi-agent append log without the full file in context.** This is the single most destructive pitfall in the report-production pipeline. The tool warns `"was last read with offset/limit pagination (partial view)"` when you pass partial content from a paginated `read_file` — but it CANNOT warn when you read the file with `head -40` via terminal and then `write_file` with what you assume is complete content. In either case the file is silently truncated to just the lines you had at write time.
  **Multi-agent append logs (daily digest, pulse roundup) — canonical safe pattern:** use the dedicated append script: `python ${MY_REPOS}/Documents/github/_project/scripts/append-digest.py "Pulse Name" "- finding1\n- finding2"`. This atomically appends — no race condition with sibling agents in the same cycle.
  **Single-agent logs — read-reconstruct-write:** read the full file with `read_file(path)` (no offset/limit, verify `truncated: false`), construct `existing_content + "\\n" + new_entry`, then `write_file`.
  **Single-agent logs — patch-append (PREFERRED for large files):** Use `skill_manage(action='patch')` or the standalone `patch()` tool with a unique `old_string` anchored at the file's end (e.g., the last `- **Next Action**:` line). This avoids reading the full file into context and doesn't truncate — `patch()` operates on the actual file, not the in-memory window. Ensure the `old_string` includes enough context to guarantee a single match (include the preceding `- **Findings**:` or `- **Status**:` lines). **Pitfall:** if multiple entries have identical Next Action text, match may hit the wrong entry — verify the diff. The partial-view warning from an earlier `read_file(offset=N)` is harmless for `patch()`.
  **Shell append (`>>`) is safe** for simple text — `echo "## [timestamp] Pulse" >> digest.md`. Use when no append script exists and the message is short.
  **Recovery after accidental truncation:** Do NOT reconstruct from memory. Re-read what remains on disk, then mine the session transcript for the original content — every `read_file` call returned line-numbered text. Assemble segments in order, strip `N|` prefixes, append your new entry, write back. If only a `head`/`tail` snippet is in context, the most recently archived version plus git reflog may fill the gap. In the worst case, admit the loss and regenerate from remaining archives.

## Verification

Before delivering a status check report, verify:
- **Freshness check was performed** — last report was identified and its timestamp recorded
- **Delta detection ran** — comparison against baseline produced actual changes (not stale copy)
- **Escalation tracks correctly** — consecutive-report items have escalating language
- **Recommended Actions present** — 2-4 concrete items with owner/timeline
- **Format matches discord-report-format** — emoji header, compact bullets, no blank gaps
- **Script failure check** — if a data-collection script failed, was it detected as consecutive (not fresh) and escalated appropriately?
- **Archive written** — report file exists at the designated archive path with correct naming

## Related Skills
- `discord-report-format` — Discord formatting rules for delivery
- `qa-pulse` — codebase QA pulse checks (complementary: stakeholder focus vs codebase focus)
- `plan` — for planning mode when status check reveals a large new initiative

## References
- `references/comprehensive-health-report-pattern.md` — multi-layer system health aggregation spanning inventory, gbrain, guardian, gap reports, and cron analysis. Use for daily/weekly Dream Cycle health checks.
- `references/pulse-brain-health-remediation.md` — gbrain cross-link repair workflow for improving brain score during pulse cycles. Covers orphan categorization, strategic linking, and before/after verification.
- `references/direct-db-query-pattern.md` — direct SQLite query pattern for data gathering when the data-collection script is unavailable.
- `references/daily-brief-reconstruction.md` — multi-source reconstruction procedure for when the daily brief script fails (wrong path, missing, or template-stub output). Covers script re-invocation with prompt data flags, MCP-based data gathering (BizDev dashboard/targets/followups, gbrain, Postgres), weekly council open loops extraction, daily digest cross-reference, git activity scanning, infrastructure state, and cron prompt exclusion-rule handling.
