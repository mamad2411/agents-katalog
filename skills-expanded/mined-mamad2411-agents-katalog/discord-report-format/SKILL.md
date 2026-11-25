---
name: discord-report-format
description: Standard Discord markdown formatting for cron job reports, summaries, and status updates
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [discord, messaging, formatting, reports, cron]
    triggers: [discord report, format report, report format, cron report, delivery format, message format, discord delivery]
    related_skills: [social-media-automation]
---

# discord-report-format

Format cron job output for delivery to Discord/messaging platforms. Use this when generating any automated report that gets delivered to a user via a cron job destination (Discord, Telegram, etc.).

## Formatting Rules

### Headers
- Start every report with a bold emoji header + timestamp on one line: **🔵 TITLE** | Mon Jun 22 · 10:43 PM ET
- Section headings use **bold** only (no heading markdown `##` — Discord drops it)

### Section Order (adaptable per report type)
General template — reorder sections to fit the report's purpose:
1. **Header** — emoji + bold title + timestamp on first line
2. **📊 RECAP** — resolved items with outcomes (tables or compact bullet format)
3. **🎯 PRIORITIES / NEW ITEMS** — active work items, picks, or findings
4. **⏳ PENDING** — items still unresolved (table format with date/status)
5. **🎯 RECOMMENDED ACTIONS** *(required in command/council briefs)* — concrete next steps
6. **🔍 Checked:** — timestamp when scan completed + data source note

For report-specific templates (pulse brief, codebase health, command brief, council check-in, QA pulse workflow, weekly intelligence digest, etc.), see `references/report-templates.md`, `references/dev-lead-pulse-template.md`, `references/council-checkin-template.md`, `references/qa-pulse-workflow.md`, and `references/weekly-intelligence-digest.md`. For a test-focused pulse variation (Sentry-style QA sweeps), see `references/pulse-report-workflow.md#qa--ci-pulse-variation`. For formatting consecutive script/automation failures with escalating tone, see `references/script-failure-reporting.md`.

### Text Conventions
- **Bold** for key names — companies, people, project names, important terms
- `Backticks` for filenames, commands, paths, and tool names
- Plain text for everything else — no HTML, no markdown headings, no inline code for non-technical values

### Section Separators
Place a line of box-drawing characters between sections for visual structure:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━
```
These render as plain text in Discord (not actual horizontal rules), so they are safe. Use sparingly — one separator per distinct section boundary, never multiple in a row.

### Emoji Conventions
| Emoji | Meaning | Use Case |
|-------|---------|----------|
| 🔵 | Scan header | First line of report |
| 📊 | Stats/recap | Results section |
| 🎯 | New/picks/actions | New recommendations or recommended actions |
| ⏳ | Pending | Unresolved items |
| 🔍 | Verification | Checked timestamp |
| ✅ | Won/positive | Positive outcome or passed check |
| ❌ | Lost/negative | Negative outcome or failed check |
| ❓ | Uncertain | Needs investigation |
| ⚠️ | Warning | Degraded state, non-critical issue |
| 🔴 | Critical | Blocking issue, requires immediate attention |
| 🟡 | Medium/emerging | Notable risk, degraded-but-working |
| 🟢 | All clear | Healthy service, no issues |
| 🏗️ | New feature/architecture | Upstream additions, new subsystems, architectural changes |
| 🗂️ | File/codebase tracking | God-file sizes, line counts, growth rates, size monitoring |

### Tables
Standard Discord-compatible markdown tables:
```
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| val     | val     | val     |
```

### Compact Format (CRITICAL Principle)
Apply **compact scannability** to every report:
- Fit key info into as few lines as possible — no padding, no filler phrases
- One item per line, no blank lines between related items
- Use pipes (`|`) for inline separation of values instead of multiple lines
- Omit sections that have nothing to report — do NOT write "nothing new" or "no changes"
- When every section would be empty, respond with `[SILENT]` instead
- Target: a full brief should be scannable in under 10 seconds

### Outcome Formatting
Won bets: `✅ PICK (-ODDS) | WON, +Xu | SCORE RESULT`
Lost bets: `❌ PICK (-ODDS) | LOST, -Xu | SCORE RESULT`
General status line: `✅ ITEM | outcome, +$value`
Failure line: `❌ ITEM | failure description`

### Running Record
Format: `Record: W-L (win%), +/-Xu, +/-X% return`

### When Nothing to Report
Respond with exactly `[SILENT]` — no other content. Suppresses delivery.

## Pulse Report Workflow

Heartbeat / pulse reports (e.g., 4-hour pulse) must surface **actual work first, intelligence second**. The old pattern of scanning a fixed handful of repos and relying on blogwatcher misses commits that happened elsewhere.

**Required sequence:**
1. **Dynamic git scan** — enumerate every repo under the user's GitHub/projects root and report repos with commits
2. **Cross-reference other pulses** — read the daily digest / previous pulse outputs for the same window and surface findings from sibling pulses (dev-lead, qa-lead, integration-lead, docs-lead, skills-lead, Self-Healing, etc.)
3. **Cron / system state** — note any job errors, rate limits, or next-run schedules that affect operations
4. **Documentation health scan (Scribe-specific)** — for roles that own documentation, check project docs for staleness before the intel pass:
   - Verify release notes match the current upstream version
   - Check CHANGELOG is current against recent commits
   - Validate roadmap/project-priority docs updated within the last 30 days
   - **Check roadmap cross-section consistency** — the priority matrix summary and each project's detail section must agree. A matrix showing "Active" but details still saying "Research phase" with stale research-checkboxes is the single most common roadmap maintenance defect. Flag any mismatch.
   - Spot-check a sample of `docs/` files for stale references or broken cross-links
   - Flag empty/stale artifact files (0-byte empties with no git history)
   - See `project-documentation-standards` for the full assessment workflow
5. **Intel scan** — only if time permits after the above: blogwatcher, PIM, news feeds

### Robust Dynamic Git Scan

Use `find` + `xargs` rather than a shell `for` loop over `*/`. Iterating 100+ directories with `git rev-parse` per directory is slow and can hang or be killed on large roots. Use parallel `xargs` and target `.git` directories directly:

```bash
find /path/to/github -maxdepth 2 -name .git -type d -print0 2>/dev/null | \
  xargs -0 -P4 -I{} bash -c '
    d="$(dirname "{}")"
    repo=$(basename "$d")
    count=$(git -C "$d" log --oneline --since="4 hours ago" 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then
      printf "[%d] %s\n" "$count" "$repo"
      git -C "$d" log --oneline --since="4 hours ago" 2>/dev/null | head -3
    fi
  '
```

If the scan returns zero commits, also check the working tree of the most active repo (usually `_project` or the the planning repo root) for uncommitted changes:

```bash
git -C /path/to/github/_project status --short
git -C /path/to/github/_project diff --stat
```

Pulse users often create files over several days before committing; a commit-only scan will miss this work.

**For single-repo pulse targets** (e.g., Forge scanning Hermes Agent), run the working-tree check as a **primary action every cycle**, not just a zero-commit fallback. Developers frequently start fixes, get interrupted, and leave them half-done in the working tree. An uncommitted change found this way may be a legitimate fix that would be lost on the next rebase — review it, commit it if ready, or flag it as at-risk in the report.

### Cross-Pulse Digest Read

Always verify today's digest file exists before grepping:

```bash
digest="/path/to/github/_project/daily-digest/$(date +%Y-%m-%d).md"
[ -f "$digest" ] && grep -E "Self-Healing|dev-lead|qa-lead|integration-lead|docs-lead|skills-lead" "$digest" | head -30
```

If the file does not exist, read the most recent file in the directory instead:

```bash
ls -t /path/to/github/_project/daily-digest/*.md 2>/dev/null | head -1 | xargs -I{} grep -E "dev-lead|qa-lead|integration-lead" {} | head -30
```

**Pitfalls:**
- **Windows/MSYS (git-bash): `git -C ${MY_REPOS}/...` absolute MSYS paths SILENTLY FAIL** with `fatal: not a git repository` — the scan returns zero commits even when repos have activity, and the pulse misses everything. Fix: `cd` into the root first and use **relative** paths (`git -C "$d"` where `$d` comes from `find . -maxdepth 2 -name .git`), or use Windows-style `E:/...` absolute paths. Verify the scan works before trusting a zero result (e.g. spot-check one known-active repo with `git -C ./<repo> log --oneline -3`).
- Do NOT hard-code a short list of repos to check. Use shell globbing or `find` against the root.
- Do NOT use a plain `for d in .../*/` loop for 100+ repos — it is slow and may be killed.
- Do NOT trust a commit-only scan when it returns empty. Check working-tree status and recent file timestamps in the the planning repo root.
- Do NOT grep a daily-digest file without checking it exists first.
- Do NOT lead with blogwatcher/Intel when git or cross-pulse data is available.
- Do NOT report "no commits" as a section if there really are none — but always verify with the dynamic scan and working-tree check first.
- **Do NOT use `write_file` to append a new pulse entry to PULSE.md (or any append-only log) after reading only a partial window via `read_file(path, offset=N, limit=N)`** — you only have a subset of the file in context. Calling `write_file` with that partial content silently truncates the file to those lines. The tool warns with `"was last read with offset/limit pagination (partial view). Re-read the whole file before overwriting it."` — heed it. **Safe pattern:** read the full file with `read_file(path)` (no offset/limit), construct the new content = existing + new entry, then write back with `write_file(path)`.

## Related Skills
- `recurring-status-checks` — stale-state reconstruction, escalation tracking, and archive workflow for periodic reports

## Anti-Patterns
- Do NOT use HTML or raw markdown in Discord — plain + emoji only
- Do NOT include `[SILENT]` alongside content — it's mutually exclusive
- Do NOT wrap timestamps in code blocks — keep them as plain text
- Do NOT use horizontal rules (---) in Discord — use box-drawing chars (`━━━━`) or newlines instead
- Do NOT write "nothing new", "no changes", or filler text in empty sections — omit the section entirely
- Do NOT use blank lines between items in a section — one item per line, contiguous
- Do NOT omit the **🎯 RECOMMENDED ACTIONS** section in command/council briefs — it's the section the user reads first
