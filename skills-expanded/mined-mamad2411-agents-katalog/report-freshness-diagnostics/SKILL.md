---
name: report-freshness-diagnostics
description: >-
  Detect, classify, and report on data staleness and zero-activity periods in
  recurring cron reports. Bridges the gap between data-gathering and
  report-formatting by adding freshness-aware diagnostics.
version: 1.1.0
author: Hermes Agent
metadata:
  hermes:
    tags: [freshness, staleness, diagnostics, cron, reporting, data-quality]
    triggers: [stale data, data freshness, auto-pilot week, zero activity week, quiet week, how old is this data, is this data current]
    related_skills: [discord-report-format, recurring-status-checks]
---

# Report Freshness Diagnostics

When generating any recurring report (weekly digest, daily brief, pulse heartbeat, status check), add a freshness diagnostic layer between your data-gathering phase and your report-formatting phase. This skill covers how to detect, classify, and report on data staleness and zero-activity periods.

## Phase 0: Discover the Actual Data Path

Never assume documented repo roots, data directories, or archive paths exist. Always discover at runtime:

```bash
# Find ALL git repos dynamically
find ${USER_HOME} -maxdepth 4 -name .git -type d 2>/dev/null | while read d; do
  echo $(dirname "$d" | xargs basename)
done

# Find data files to check freshness
find ${HERMES_HOME} -name "*.csv" -o -name "*.json" 2>/dev/null | head -30

# Find project directories
ls ${USER_HOME}/ | head -40

# Check for digest / archive directories
find ${USER_HOME} -maxdepth 4 -type d -name "daily-digest" -o -type d -name "digests" 2>/dev/null
```

If the documented paths don't exist, use the discovered paths. Log the mismatch.

### Finding Your Own Cron Job's Output Dir (IDs drift)

Job IDs change whenever a cron prompt is edited, and `hermes cron list` is frequently unparseable/empty inside a cron session. Discover the correct output dir by grepping for a unique string from YOUR OWN prompt across the output root, then confirm identity via the job's "You are the..." line:

```bash
# 1. Find candidate dirs: any output file whose prompt contains your unique fragment
grep -rl "trumpian-accounting-kb/monitoring/findings/latest.json" ~/AppData/Local/hermes/cron/output/*/ | tail -5
# 2. Confirm job identity + read the last report (no skill-preamble bloat)
grep -o "You are the [^.]*" ~/AppData/Local/hermes/cron/output/<job>/<file>.md | head -1
tail -30 ~/AppData/Local/hermes/cron/output/<job>/<latest-file> | tr -d '\r'
```

Confirmed Aug 1 2026: the Daily Cash-Flow Briefing prompt fragment resolves to job `e3ac683bc4f3`, now firing ~18:06 ET (drifted from the documented 8am — verify, don't assume).

## Phase 1: Zero-Activity Detection

### Git Zero-Commit Week
Scan ALL repos for commits in the report's time window. When all return zero:

1. **Verify the scan worked** — check that `find .git` returned hits. If it returned nothing, the scan itself failed (no git repos found).
2. **Cross-check with working tree** — `git status --short` on the 5 most active repos. Files may have been created/edited but not committed.
3. **Cross-check with file timestamps** — `find /path -mmin -10080 -type f | head -20` (files modified in last 7 days, non-.git). Catches doc edits, data exports, any activity.
4. **Cross-check with cron session history** — use `session_search` to check if any cron jobs reported meaningful findings this week.

### Classification Matrix

| Signal | Healthy Autopilot | Stalled System |
|--------|-------------------|----------------|
| Cron job status | All `ok` | Multiple errors |
| Pipeline movement | Numbers changing (targets up, outreach sent) | Same numbers as 4 weeks ago |
| Data freshness | < 7 days | > 14 days (actionable staleness) |
| User activity | Session_search shows recent user messages | No user messages in cron channels |
| Working tree | Has uncommitted work-in-progress | Clean, no changes |

**Theme when healthy:** "Stable week, system humming. Pipeline maintenance mode."
**Theme when stalled:** "Full autopilot, zero forward momentum. Data rot setting in."

## Phase 2: Data Staleness Detection

### Find + Age All Data Artifacts

```bash
find /path/to/data -type f \( -name "*.csv" -o -name "*.json" \) 2>/dev/null | \
  while read f; do
    age_days=$(( ($(date +%s) - $(stat -c %Y "$f")) / 86400 ))
    echo "$age_days|$f"
  done | sort -rn
```

On Windows/MSYS2 where `stat -c %Y` may not work or the output format differs:

```bash
find ${HERMES_HOME} -type f \( -name "*.csv" -o -name "*.json" -o -name "*.md" \) \
  -not -path "*/.git/*" 2>/dev/null | xargs ls -lt | head -30
```

### Per-Source Staleness (catches a dead connector the aggregate misses)

For database-backed sources (e.g. PIM `saved_items`), the aggregate "newest row" query looks healthy while one connector is silently dead. Check per source:

```bash
sqlite3 "${MY_REPOS}/Documents/github/git-mcp/services/personal-intelligence-mcp/pim.db" \
  "SELECT source_type, COUNT(*), MAX(ingested_at) FROM saved_items GROUP BY source_type ORDER BY MAX(ingested_at) DESC;"
```

Confirmed Aug 1 2026: the PIM email connector was dead for 8 days (MAX(ingested_at)=Jul 24) while Grok/bookmarks flowed through Jul 29-30 — the aggregate `LIMIT 3` query looked only mildly stale, and a sibling brief reported "no new emails in 48h", under-stating a week of silently-dropped recruiter leads. **Never trust a sibling pulse's staleness claim — verify per-source `MAX(ingested_at)` yourself.** One connector dead while others flow = pipeline failure to flag (email especially — it feeds C2C cash streams), not a quiet period.

### Staleness Classification

Classify every stale artifact into one of three categories:

| Category | Criteria | Action |
|----------|----------|--------|
| 🟢 Benign | Reference data that doesn't change (static lists, one-time scrapes, seed data) | Note age but do NOT flag as urgent |
| 🟡 Actionable | Data that should be refreshed but hasn't been (builder inventories, market comparables, lot listings, call sheets) | Flag with exact age + recommend re-scrape |
| 🔴 Critical | Data that directly blocks decision-making (CRM-ready leads that haven't been imported, buy-box data for current season, assessment data for upcoming TRIM cycle) | Flag prominently in report header, escalate if same artifact flagged 2+ reports running |

### Reporting Format

```
| `path/to/file.csv` | X days stale | 🟡 Actionable | Last updated Jun 16 — recommend re-scrape |
```

If multiple artifacts share the same staleness date, group them:
```
| `builders.csv`, `comparables.json`, `call_sheet.md` | 40 days stale | 🟡 Actionable | All Jun 16 — entire dataset needs refresh |
```

## Phase 3: Deadline and Timeline Awareness

Check for deadlines that passed since the last report:

1. **Open loop deadlines** — check `deadline` or `due` fields in open loops from the cron prompt
2. **Assessment/seasonal catalysts** — upcoming events that will make data freshness suddenly matter:
   - TRIM notices (August) — assessment shock window
   - Quarter ends — financial reporting deadlines
   - FAR rule changes — compliance mandate dates
   - Tax deadlines — filing windows

Format:
```
| OL-004 | Jul 16 | 10 days past | Land Sales CRM seeding |
```

## Phase 4: Freshness-Aware Reporting

When a zero-activity week combines with actionable staleness, this IS the story. Structure the report around it:

```
**This week's theme:** Full autopilot, zero forward momentum. 
Builder data 40 days stale. C2C pipeline unchanged in 4 weeks.

━━━━━━━━━━━━━━━━━━━━━━━━━━

🏗️ LAND SALES CRM (P0)
10 builders on file | buy-box $30K-$100K/lot | all data 40 days stale
Email watchdog: 3 replies from Jun 23 — no follow-up sent
OL-004: 10 days past due

⚠️ DATA STALENESS
| `builders.csv`, `comparables.json`, `call_sheet.md` | 40 days | 🟡 Actionable |
| TRIM assessment window | Aug (2 weeks) | 🔴 Catalyst approaching |
```

## Phase 5: Forward-Looking Signal

Every weekly report needs a catalyst prediction. What's the next event that will change the status quo?

```
**Next week's focus:** TRIM notice prep. Re-scrape builder data before 
August assessment shock window opens. Push data into Twenty CRM.
```

Common catalysts to watch for:
- **August**: FL TRIM notices → assessment shock → motivated sellers
- **September/October**: Q3 wrap, budget planning season
- **November/December**: End-of-year land sale windows, builder inventory rollover
- **Any month**: FAR rule changes, FedRAMP milestones, regulatory deadlines

## Phase 6: Pre-Delivery Deduplication Check

Before emitting any recurring report — especially high-frequency cycles (4-hour pulses, hourly sweeps, 2x daily scans) — verify that your findings haven't already been reported by a sibling cron job that ran moments before.

### Why This Exists

Multiple cron jobs (legal watchdog, integration-lead pulse, dev-lead, qa-lead) can cover overlapping domains. A 4-hour pulse and a legal sweep may both find the same FTC comment deadline, the same stale data, or the same blocked source. Reporting the same finding twice in the same delivery channel is noise.

### How to Check

Use `session_search` to find recent sessions covering the same topic:

```python
# Discovery: find most recent sessions matching this report's domain
session_search(query="FTC comment deadline legal watchdog pulse", limit=2, sort="newest")
```

Look at the timestamps and findings in the returned sessions. If a recent session (within the report's window) already covered the same items, you have two options:

| Finding Age | Overlap | Action |
|------------|---------|--------|
| Same items, within same window | >80% overlap with a session <4h old | Respond with `[SILENT]` — the user already saw this |
| Same items, but >1 report cycle ago | Any overlap, but older than one full cycle | Surface with note: "as previously reported" — but only if something NEW changed |
| Totally new findings | No overlap | Deliver normally |
| Nothing found (session_search returns empty) | N/A | Deliver normally |

### When Session Search Fails

If `session_search` returns no results (e.g., first run, or DB not populated), deliver the report normally. The dedup check is a best-effort filter, not a blocker.

### Pitfalls

- **Do NOT check for generic breadcrumbs.** Query for the specific finding (e.g., `"FTC AI Accuracy" legal watchdog`) not generic terms like `"4-hour pulse"` or `"cron report"`. Generic queries return false-positive matches on unrelated sessions.
- **Do NOT skip this for high-frequency cycles.** The tighter the cycle, the more likely you are to overlap with sibling crons. A 4-hour pulse and a daily sweep overlap on the same data sources.
- **Do NOT repeat old findings just to pad a report.** If the only content you could report was already covered, produce `[SILENT]`. The user prefers no output over echo.
- **Do NOT list every sibling cron that ran.** Names like "Legal Watchdog already reported this" in delivery content are helpful context; a full enumeration of every recent session is noise.
- **Do NOT trust a sibling pulse's staleness claim — verify per-source yourself.** The aggregate "newest row" check can look mildly stale while one connector is silently dead. Run the per-source `MAX(ingested_at)` check in Phase 2 before repeating any sibling's "no new X in 48h" line.
- **Do NOT treat a failed sibling/cron run as "nothing new".** An output file whose tail ends in an `## Error` block (e.g. `SSL_CERT_FILE points to a missing CA bundle`) means NO report was delivered — that run is a delivery GAP (reportable), not a data point. When a sibling brief (Morning Brief, etc.) ran ~1h before you and covered the static streams, report only the DELTA (sharper staleness, delivery gaps, root causes) — never rehash.

**Pitfalls**

- **Don't trust documented paths.** Discover actual repos/data at runtime.
- **Don't report "no commits" without verifying the scan worked.** If `find .git` returned 0 results, the machine may have no repos at the searched depth, not zero activity.
- **Don't report stale data without its age in days.** "40 days stale" is actionable; "data is old" is not.
- **Don't classify static seed data as actionable staleness.** Distinguish between reference data (benign) and dynamic data (actionable/critical).
- **Don't omit the catalyst window.** The user reads "TRIM notices in 2 weeks" and knows what to prioritize.
- **Don't repeat last report's freshness findings unchanged.** Escalate: if same data was flagged last week as "35 days stale" and this week it's "42 days stale," the tone should escalate (from 🟡 to ⚠️ or 🔴).
- **Don't use `nc` for port health checks on Windows/MSYS2.** `nc` (netcat) on Windows git-bash returns false negatives — it reports CLOSED for ports that respond normally via `curl` or browser. Use `curl --connect-timeout N http://localhost:PORT/` with status-code checks instead. If checking non-HTTP ports (Postgres, custom TCP), use a language-native client (psql, python socket test) rather than nc.
- **Don't forget the line-number prefix hazard when reconstructing append logs from `read_file`.** The `read_file` tool returns lines with `N|` prefixes (e.g., `1|## Pulse @ ...`). When reconstructing `existing + new` to write back via `write_file`, you MUST strip these `N|` prefixes or the file accumulates embedded line numbers. Read → strip prefixes → concatenate → write. After write, verify the line count is old_lines + new_lines, not just new_lines (which means you wrote only the new entry instead of existing + new).
- **On Windows/MSYS2, `git -C <path>` can fail with "not a git repository" on repos whose `.git/` is a real directory and resolves via interactive `cd`.** This is a path-resolution quirk with certain mount mappings in git-bash (observed with `_project`). **Workaround:** inside `xargs -I{} bash -c '...'` subshells or loops, use `cd "$repo" && git <cmd>` instead of `git -C "$repo" <cmd>`. Apply this to at minimum the the planning repo root directory and any other paths that fail `git -C`.
- **Don't report on a high-frequency cycle without checking if the previous cycle's output is identical.** For 4h (or shorter) intervals, the last report may have run minutes ago. Use `session_search` to retrieve the previous pulse's findings and timestamp. If the current scan shows the exact same state (same commits, same working tree, same digest entries), return `[SILENT]` — do not repeat findings. The freshness check should be a Phase 0 gate, not an afterthought.
