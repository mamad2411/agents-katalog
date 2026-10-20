---
name: cyber-intel-workflow
description: "Nightly cybersecurity research and morning briefing pipeline — CVE/PoC tracking, breach monitoring, threat intel aggregation, and operator-ready briefing compilation across a cron chain."
version: 1.3.0
author: Phantom (Cyber Lead)
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cybersecurity, threat-intel, cve, poc-tracking, cron, briefing, discord-formatting, phantom]
    triggers: [cyber-research, night-research, morning-briefing, cyber-briefing, threat-intel-sweep, cve-scan, phantom, auto-action-handler, tiered-briefing, cyber-intel-scanner]
    related_skills: [discord-report-format, intelligence-pulse, cyber-tiered-intel]
---

# Cyber Intelligence Workflow

## Overview

Two-phase cron pipeline for operational cybersecurity intelligence:

1. **Night Research** (`cyber-night-research`) — runs ~10 PM ET. Comprehensive sweep of CVEs, exploits, breaches, threat intel, and industry news.
2. **Morning Briefing** (`cyber-morning-briefing`) — runs ~7 AM ET. Consumes the night report, does a quick freshness sweep for overnight developments, and produces a concise operator briefing.

## Phase 0: Context Recovery

### Night Research → Morning Briefing Chain

The morning briefing always follows a night research run. The previous cron output may be truncated in your prompt (common with long cron outputs). Recover it immediately:

**Step 1 — Find the night research session:**
```python
result = session_search(query="cyber-night-research Phantom", sort="newest", limit=1)
# The response contains session_id for the night research run
```

**Step 2 — Read the full night research output:**
```python
# Use scroll mode with the match_message_id from Step 1's anchor message
# Search for the final assistant output message in the session
session_search(session_id="<id>", around_message_id=<match_message_id>)
```

The night research output has a header like `🔴 **CYBER NIGHT RESEARCH** | Jun 22, 2:02 AM ET`.

**Step 3 — Check for a PRIOR morning briefing (dedup check):**
```python
prior = session_search(query="MORNING CYBER BRIEFING", sort="newest", limit=1)
```
If the prior briefing already covered the same findings and nothing has changed overnight, respond `[SILENT]`. Only deliver a full briefing when there are genuinely new findings since the last delivery.

### Freshness Check (Morning Briefing)

Before producing output, verify whether there's genuinely new intel since the last briefing:

1. `session_search(query="MORNING CYBER BRIEFING", sort="newest", limit=1)` to find your last output
2. Read the last briefing's timestamp and content
3. Do a quick morning sweep of feeds (Phase 2 step 1)
4. If nothing has changed since the last briefing AND the underlying night research is the same, respond `[SILENT]`
5. Only deliver a full report when there are genuinely new findings

### Auto-Action Handler Cross-Reference (Morning Briefing)

The morning briefing must VERIFY what the auto_action_handler.py actually did, not just trust the pipeline claim. The handler deduplicates by fingerprint and may fail to run entirely. Recover evidence from the filesystem:

**Step 1 — Check if the handler actually ran:**
```bash
# Check state file timestamp
stat -c "%Y %y" /path/to/monitoring/findings/auto_action_state.json
# Check action log timestamp
stat -c "%Y %y" /path/to/monitoring/findings/cyber_actions_log.jsonl
```
If the timestamps are from yesterday or earlier, the handler did NOT run at today's 07:00 slot.

**Dual State File Tracking**

There are TWO independent auto-action state files. Do not conflate them:

| File | Scope | Fingerprint Prefixes | Contents |
|------|-------|---------------------|----------|
| `auto_action_state.json` | General — all AI/research/code actions | `enhance_skill:`, `enhance_config:`, `enhance_soul:`, `clone:`, `paper:`, `note:` | Covers ALL domains (cyber, dev, skills, soul, config) |
| `cyber_auto_action_state.json` | Cyber-specific | `hardening:`, `log_intel:` | Only cyber findings that wrote to hardening notes or intel log |

Check BOTH files. The general handler may have logged a `enhance_config:` entry for a gateway crash finding in `auto_action_state.json`, while the cyber-specific handler never processed the same finding's `hardening:` or `log_intel:` fingerprint. This means the finding was "noted" but never produced a cyber-specific artifact.

**Step 2 — Check self-healer for handler failures:**
```bash
cat /path/to/monitoring/findings/self_healer_state.json
```
Look for `cron_failures:auto_action_handler` in the `recent_issue_fps` array. This confirms the handler cron job is failing.

**Step 3 — Read what the handler DID do (most recent run):**
```bash
tail -20 /path/to/monitoring/findings/cyber_actions_log.jsonl
```
Each entry shows `action_type` (hardening_note, intel_logged, etc.), `target`, `result` (file path), and `finding_tier`. Group by action_type to count.

**Step 4 — Read what's in the dedup state:**
```bash
cat /path/to/monitoring/findings/auto_action_state.json
```
The `actioned_fps` array shows fingerprints the handler already processed. The `noted_fps` array shows Tier 2/3 noted items.

**Step 5 — Cross-reference against current findings:**
```bash
cat /path/to/monitoring/findings/cyber_intel_findings.json
```
Compare current Tier 1 findings against `actioned_fps`. Recurring fingerprints (same `fingerprint` field across dates) get skipped by the handler's dedup. Flag these as "recurring, needs escalation decision" rather than "unprocessed."

**⚠️ Scanner re-scoring across dates:** The cyber-intel-scanner re-scores ALL historical findings on every run. Findings from July 10 and July 18 will both have `date: 2026-07-19T10:30:30` in the JSON — the timestamp reflects when the scanner ran, not when the finding was first identified. To determine genuine newness, compare fingerprints against the `actioned_fps` in `auto_action_state.json`. A fingerprint NOT in `actioned_fps` is genuinely new, regardless of the findings file's timestamp. A fingerprint already in `actioned_fps` is re-scored history. The `log_scan` source type (gui.log, watchdog.log) produces unique fingerprints per run because the match count changes — these are the best signal of genuinely new findings.

**Step 6 — Build the separation:**
- **Auto-implemented**: Actions the handler actually logged to the filesystem (hardening notes written, intel entries appended)
- **Auto-skipped (dedup)**: Findings already processed from prior runs. These are not auto-implemented today but also not pending review in the normal sense — they're monitored repeats.
- **Handler failures / gaps**: Findings the handler could not process because it didn't run, or that were never in the state file.

**Typical handler actions for cyber intel:**
| Tier | Change Type | Handler Action | Result |
|------|-------------|----------------|--------|
| T1 | clone/paper (github.com or arxiv.org URL) | `clone_success`, `paper_downloaded` | Cloned repo, saved PDF |
| T1 | soul (hermes_agent category) | `enhance_soul` | Appended to `SOUL.md` |
| T1 | skill (skill category) | `enhance_skill` | Created `.md` skill file |
| T1 | config (hermes_security category) | `enhance_config` | **No-op** — logs "needs review" to `auto_actions_log.jsonl` only. Does NOT write to `cyber_hardening_notes.md` or `cyber_intel_log.md`. See `cyber-tiered-intel` pitfalls for details. |
| T2 | any | `research_note` | Appended to `ai_ecosystem_notes.md` or `cyber_intel_log.md` |
| T3 | any | Skipped entirely | Nothing |

**Important:** The `enhance_config` action for Tier 1 cyber findings (dark web sweeps, gateway crash spikes, etc.) produces no persistent artifact beyond a JSONL log entry. It does not write hardening notes, update the intel log, or trigger any downstream action. This is the handler's designed behavior — not a bug, but a gap if you expect cyber-specific outputs from these findings.

The handler logs its own actions to `auto_actions_log.jsonl` (main) and `cyber_actions_log.jsonl` (cyber-specific). The action state is in `auto_action_state.json`. Both paths are under `monitoring/findings/`.

### Pipeline Diagnostics

The night pipeline has three sequential components plus the morning briefing. Any component can fail independently, and partial failures are the norm, not the exception:

| Component | Scheduled | What It Produces | Failure Signal |
|-----------|-----------|------------------|----------------|
| deep-spider-sweep | 05:00 | `deep-spider/results/*.json` (new files) | `tor.log` updated but `results/` has no new files |
| cyber-intel-scanner | 06:30 | `cyber_intel_findings.json` (updated) | File timestamp old or re-scored historical-only findings |
| auto_action_handler | 07:00 | `cyber_actions_log.jsonl` (appended), state files (updated) | State file timestamps from previous day |
| Cyber Morning Brief | 07:00 | Discord briefing | N/A |

**Diagnosing partial pipeline failure:**

1. **Check deep-spider freshness** — Compare `results/` directory listing dates against today:
   ```bash
   ls -lt /path/to/deep-spider/results/ | head -5
   ```
   If the most recent result file is from yesterday or earlier, the sweep failed to produce new results. Check `tor.log` for errors. Tor can start (file timestamps update) without any actual sweep results being written.

2. **Check scanner output freshness** — The findings JSON gets rewritten on every run:
   ```bash
   stat -c "%y" /path/to/monitoring/findings/cyber_intel_findings.json
   ```
   If today's date, the scanner ran. But visual inspection is needed for re-scored vs genuinely new findings (see re-scoring pitfall in Step 5 above).

3. **Cross-check component independence** — The scanner can run successfully even when the deep-spider-sweep failed (it re-scores old findings). The auto-handler can fail even when both preceding components succeeded. Report ALL three statuses in the briefing, not just what found something.

4. **Briefing structure under pipeline failure** — When the pipeline is degraded, emphasize what DID run vs what didn't as the first message to the operator, then proceed with findings from whatever sources actually executed. An independent freshness sweep (CISA KEV, Playwright) becomes the primary intel source when the pipeline fails.

## Phase 1: Night Research

### Feed Hierarchy & Fallbacks

Order by reliability. Fall down the chain when a source fails.

**Tier 1 — RSS Feeds (try first, often fail):**
- The Hacker News RSS: `curl -sL "https://feeds.feedburner.com/TheHackersNews" --max-time 15`
- BleepingComputer RSS: `curl -sL "https://www.bleepingcomputer.com/feed/" --max-time 15`

**Tier 2 — Structured Data Feeds:**
- NVD Modified Feed (JSON): `curl -sL "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-modified.json.gz" | gunzip`
- NVD Recent Feed: `curl -sL "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.gz" | gunzip`
- CISA KEV (JSON feed): `curl -sL -H "User-Agent: Mozilla/5.0" "https://cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json" --max-time 15`
- GitHub API: `curl -sL "https://api.github.com/search/repositories?q=CVE-2026&sort=updated&order=desc&per_page=15" --max-time 15`

**Tier 3 — Resilient Fallbacks (most reliable):**
- PoC-in-GitHub README: `curl -sL "https://raw.githubusercontent.com/nomi-sec/PoC-in-GitHub/master/README.md" --max-time 15`
  Parse with grep for CVE patterns. This source almost never fails even when RSS/CISA/NVD are down.
- Packet Storm: `curl -sL "https://packetstormsecurity.com/files/tags/exploit/page1" --max-time 15`

### Processing Pattern (Night Research)

For each source, extract:
- CVE ID, CVSS score, severity
- Brief technical description (1-2 lines)
- PoC availability / in-the-wild status
- Relevance to ops (firewall patches, WordPress plugins, etc.)

Categorize findings into:
- **Critical CVEs** (CVSS 9+) — top of the report, bold
- **High CVEs** (CVSS 7-8.9) — second section
- **New PoC Exploits** — list with GitHub repo names
- **Breaches & Incidents** — company affected, impact summary
- **Threat Intel** — malware, APT activity, zero-days
- **Patch Urgency** — consolidated action items with deadlines

## Phase 2: Morning Briefing

### Quick Freshness Sweep (9-Hour Overnight Gap)

The night research runs at ~10 PM ET. The morning briefing runs at ~7 AM ET. **That's a 9-hour gap** where new CVEs, breaches, and threat intel can be published. Do NOT just summarize the night research — independently check for overnight developments.

Sweep pattern — try in order, falling through when a method is unavailable:

**Option A — web_search (preferred, when available):**
```python
web_search(query="cyber security breach news today [Mon DD] 2026", limit=5)
web_search(query="new CVEs published [Mon DD] 2026 critical severity", limit=5)
web_search(query="[specific CVE ID] update [Mon DD]", limit=5)
```

**Option B — browser navigation fallback (when web_search is NOT available but browser tools work):**
Use browser tools to navigate directly to cybersecurity news sites and extract current headlines via `browser_snapshot`.

Navigation targets (most reliable order):
1. **BleepingComputer** — `browser_navigate(url="https://www.bleepingcomputer.com/")` then `browser_snapshot()`. Front page lists latest articles with headings, timestamps, and bylines. Articles from today's date or late last night are fresh. Timestamps are precise HH:MM AM/PM.
2. **CISA Alerts & Advisories** — `browser_navigate(url="https://www.cisa.gov/news-events/cybersecurity-advisories")` then `browser_snapshot()`. Lists KEV additions and alerts with date tags.
3. **The Hacker News** — `browser_navigate(url="https://thehackernews.com/")` then `browser_snapshot()`. Tertiary check.
4. **Threatpost** — Fallback only. May return stale content.

Extraction pattern: Read the snapshot output for article headings, dates, and bylines. Key data points from BleepingComputer include exact publication time (e.g. "03:47 AM") — use this to confirm overnight freshness vs stale carryover.

**Option C — curl-based API/feed fallback (when both web_search AND browser CDP fail):**
If neither web_search nor browser CDP are available (common in cron contexts), use direct curl against structured data sources:

1. CISA KEV JSON feed — most reliable structured source:
   ```bash
   curl -sL -H "User-Agent: Mozilla/5.0" "https://cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
   ```
   Filter by `dateAdded` field (format `YYYY-MM-DD`). Catalog version field tells you the release date.

2. GitHub API PoC search — check for recently published PoCs:
   ```bash
   curl -sL "https://api.github.com/search/repositories?q=CVE+2026+poc+exploit&sort=updated&per_page=10"
   ```
   Rate limit: 60/hr unauthenticated. Use sparingly.

3. Google News RSS — text headlines without rendering:
   ```bash
   curl -sL "https://news.google.com/rss/search?q=cybersecurity+zero+day+exploit+2026&hl=en-US&gl=US&ceid=US:en"
   ```
   Parse RSS XML for titles, pubDate, links.

4. NVD API — CVSS + description for specific CVEs:
   ```bash
   curl -sL "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-XXXXX"
   ```

Cross-reference findings against the night research manually. Flag anything dated today or late yesterday evening.

**2. Cross-reference against night research** — flag items that are genuinely new, not rehashes of what was already reported. Skip anything already covered in the night report.

**3. Known overnight-arrival categories** (items commonly published after 10 PM):
   - Botnet/discovery reports (AryStinger, new IoT malware campaigns)
   - ClickFix / malvertising campaign updates
   - Late-breaking breach confirmations
   - Overnight vulnerability disclosures (Europe/Asia-timezone researchers)
   - CISA KEV additions (often published mid-day ET, carry over to next morning)

**4. If nothing new is found**, deliver a shorter briefing based on night research plus a note that no overnight developments occurred. Do NOT fabricate freshness.

### Briefing Structures

The skill supports two briefing formats. Use the standard format for general cyber briefings and the tiered format when the pipeline includes auto-action handler results.

**Standard Briefing Structure** (general purpose):

```
🟠 **MORNING CYBER BRIEFING** | Mon DD, HH:MM AM/PM ET
━━━━━━━━━━━━━━━━━━━━━━

**TL;DR** 2-3 sentence executive summary

━━━━━━━━━━━━━━━━━━━━━━

🚨 **CRITICAL PRIORITY ITEMS**
Up to 3 items needing immediate attention today

━━━━━━━━━━━━━━━━━━━━━━

🔥 **CVE HIGHLIGHTS**
Most impactful CVEs: ID, CVSS score, brief technical, PoC status

━━━━━━━━━━━━━━━━━━━━━━

💥 **BREACHES & INCIDENTS**
What happened, who's affected, impact

━━━━━━━━━━━━━━━━━━━━━━

👁️ **WATCH LIST (Today)**
Emerging threats to monitor today, 3-5 items

━━━━━━━━━━━━━━━━━━━━━━

🎯 **BOTTOM LINE**
One key takeaway — the single most important thing to act on today

━━━━━━━━━━━━━━━━━━━━━━

🎯 **RECOMMENDED ACTIONS**
2-4 concrete, specific steps with timeframe
```

**Tiered Briefing Structure** (when using auto-action handler pipeline):

Use this format when the morning briefing follows the cyber-intel-scanner + auto_action_handler pipeline. It separates what was auto-implemented from what still needs manual review.

```
🔵 CYBER BRIEFING | Mon DD · HH:MM AM/PM ET

**TL;DR** 2-3 sentence summary including handler status and key overnight findings

━━━━━━━━━━━━━━━━━━━━━━

🔴 TIER 1 — AUTO-IMPLEMENTED
For each action the handler actually took:
✓ [Action type]: [what was done] — [result file/path]
Example: ✓ Hardening note: Breach sweep for credentials → cyber_hardening_notes.md
Example: ✓ Intel logged: Dark web found 24 results → cyber_intel_log.md
If the handler did NOT run, include: ⚠️ Auto-action handler is down. [details from self-healer]

━━━━━━━━━━━━━━━━━━━━━━

🔴 TIER 1 — REMAINING / OVERNIGHT
New Tier 1 items found that need manual action.
For each: Recommendation: [specific action]

━━━━━━━━━━━━━━━━━━━━━━

🟡 TIER 2 — RECOMMENDED ACTIONS
For each: Recommendation: [specific suggested action]

━━━━━━━━━━━━━━━━━━━━━━

🔵 TIER 3 — WATCH LIST
Items to keep an eye on. One line per item.

━━━━━━━━━━━━━━━━━━━━━━

🎯 SUMMARY
✓ Auto-implemented: [N] actions
🔄 Pending review: [N] items
👁️ Monitoring: [N] items
⚠️ System issues: [any handler/cron failures]

🔍 Checked: HH:MM AM/PM ET | Sources: [data sources]
```

**Do NOT skip the Recommended Actions section.** Include it in both formats.

### Formatting Rules

Follow `discord-report-format` skill rules strictly:
- **No em dashes** — use commas, periods, or plain spaces
- Compact one-line-per-item format
- **Bold** for CVE IDs, company names, product names
- Backticks for GitHub repo names, commands, filenames
- Direct, short sentences over complex construction
- Prefer exclamation points for urgency
- Box-drawing separators between sections (`━━━━━━━━━━━━━━━━━━━━━━`)
- No blank lines between items in a section
- No blank lines around separators

## Phantom Persona

When operating as the Cyber Lead ("Phantom"), adopt these voice rules:

- **Sharp and direct** — this is a morning read for operators. No fluff, no setup paragraphs, no throat-clearing.
- **Action-oriented** — every section leads to a specific action or decision. If a finding doesn't drive action, omit it.
- **Authority without alarm** — state the severity plainly. "Patch PAN-OS today" not "we recommend considering patching."
- **Context for ops** — include relevance signals operators need (CVSS score, PoC in wild, patch availability, exploitation likelihood).
- **Bottom Line** — one key takeaway in the TL;DR that the reader can act on immediately.
- **Timestamps in ET** — all times in America/New_York, format "Mon DD, HH:MM AM/PM ET".

## Pitfalls

- **Truncated cron context** — always recover full previous output via session_search before writing. The prompt truncation is a known issue with long cron outputs.
- **Dead RSS feeds** — THN and BleepingComputer RSS frequently time out for cron jobs on some hosts. Never rely on them exclusively. Always have a Tier 3 fallback ready.
- **web_search tool may be absent** — Not every session/profile has `web_search` in the toolset. When it's missing, fall back to Playwright MCP browser navigation (see Phase 2 Option B). Do not attempt to call `web_search` — it will fail with "Tool does not exist". Detect its absence early by checking tool availability and route to browser navigation immediately.
- **GitHub API rate limits** — unauthenticated requests to api.github.com are limited to 60/hr. Use raw.githubusercontent.com for PoC-in-GitHub (no rate limit) as the primary PoC source.
- **NVD feed size** — the full modified feed can be 5K+ CVEs. Filter to high/critical (CVSS 7+) before processing to avoid token waste.
- **CISA KEV parsing** — CISA's page is HTML, not structured data. The page layout changes periodically. Prefer NVD modified feed + PoC-in-GitHub for reliable CVE tracking.
- **Freshness double-reporting** — if both night research and morning briefing ran previously on the same data, the morning briefing must use session_search to verify it's not repeating the same findings. Use `[SILENT]` when nothing is new.
- **Overnight gap = genuine new findings** — the 9-hour gap between night research (10PM) and morning briefing (7AM) routinely produces new intel that wasn't available at 10PM. In one example (Jun 22, 2026), AryStinger botnet (4,300 routers) and ErrTraffic ClickFix campaigns were published overnight and missed by the 10PM sweep. Do a dedicated web_search with current-date targeting as part of the freshness sweep. Do not assume the night research is complete.
- **Briefing must include Recommended Actions** — discord-report-format Rule 14 requires it. The morning briefing template now includes both Bottom Line (one-liner takeaway) and Recommended Actions (specific next steps). Do not omit either.
- **Browser snapshot extraction is manual** — Playwright snapshots return verbose accessibility YAML trees. Parse manually for article headings and dates; there is no structured extraction. Use the `browser_snapshot()` output's heading elements (`heading "Title" [level=2]`) to identify articles, then scan adjacent time elements and paragraphs for dates and descriptions.
- **Auto-action handler may be failing silently** — The handler runs as a `no_agent=true` cron and produces zero output when nothing is actionable. Check `self_healer_state.json` for `cron_failures:auto_action_handler` to detect handler failures. If the handler hasn't run, its state file will have an old timestamp. Do not assume no-output means "nothing to do" — it may mean the handler is down.
- **Recurring fingerprints mask new sweeps** — The auto-action handler deduplicates by fingerprint. If the same dark web keywords sweep runs daily, the fingerprint doesn't change, and new daily sweeps won't trigger new actions. The finding still gets logged to history but the handler skips it. Flag these as "recurring signal, needs escalation decision" rather than silently accepting the dedup.
- **CISA KEV JSON feed URL** — The correct feed URL is `cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` (not the HTML page). The JSON feed has a `catalogVersion` and `dateReleased` field at the root, and entries with `dateAdded` (YYYY-MM-DD format). Use this with curl and a User-Agent header. The catalog index can be >1600 entries, so filter by `dateAdded` to find recent additions.
- **Playwright MCP for CISA KEV browser check** — When CDP browser tools are unavailable, Playwright MCP `browser_navigate` + `browser_snapshot` works well for reading CISA KEV and bulletins. The snapshot returns structured YAML with article headings, CVE IDs, dates, and descriptions. Parse for `heading` elements containing CVE IDs and `listitem` elements containing "Date Added" / "Due Date" values. This is faster and more reliable than downloading the full 1600+ entry JSON feed.
- **Pipeline partial failure = don't skip the briefing** — When the Cyber Night Research job failed but the scanner still ran, or when the deep-spider-sweep produced no new results but the scanner found a log_scan anomaly, still deliver the briefing. The partial output is still actionable (gateway crashes, CISA KEV due-dates). The worst outcome is a silent morning when a Fortinet CVE is due today and no one knows. Report what you have, note the pipeline gaps, and let the operator decide.

## New Threat Categories (Black Hat 2025/2026 PIM Analysis)

Five new monitoring categories added from 19 Black Hat conference talks. Full details:
`_project/04-shared-memory/playbooks/cyber-intel-new-threat-categories.md`

### CAT-1: Autonomous AI Attacker Detection
**Source:** Black Hat Asia 2026 (5IrJf2qGZcM)
Systems performing offensive security autonomously: recon, exploitation, lateral movement.
Monitor: burst API call patterns, adaptive attack behavior, LLM-generated phishing.

### CAT-2: MCP Server Vulnerability Monitoring
**Source:** Black Hat Europe 2025 (fG36PSl_sgo)
500+ vulns, RCE in ChatGPT/Claude/Copilot. Run `mcp_security_audit.py` weekly.
Monitor: new MCP CVEs, GitHub security advisories, tool name collision registrations.

### CAT-3: IoT Management Plane Attacks
**Source:** Black Hat Europe 2025 (MVliifh92tQ)
Cloud-managed IoT devices vulnerable through management plane, not device itself.
Monitor: vendor advisories, CISA KEV for IoT CVEs, Shodan for exposed interfaces.

### CAT-4: AI Agent Containment Failures
**Source:** Black Hat USA 2026 (87DyyMV0kCY)
AI agents can autonomously break containment. This happened — OpenAI → Hugging Face.
Monitor: agent session anomalies, unusual tool usage patterns, filesystem access.

### CAT-5: Kinetic Prompt Injection (Physical-World)
**Source:** Black Hat USA 2026 (LZkdihOzfe4)
Prompt injection on AI-controlled physical devices has real-world consequences.
Monitor: physical action audit logs, behavior baseline divergence, sensor manipulation.

- `discord-report-format` — formatting rules for all Discord deliveries. Always load before producing output.
- `intelligence-pulse` — broader personal intelligence gathering. Complementary but not specific to cybersecurity.
- `blogwatcher` — dedicated RSS feed monitoring if persistent feed tracking is needed beyond cron sweeps.

## Reference Files
- `references/feed-sources.md` — documented intel source URLs, expected output format, and fallback notes
- `references/tiered-briefing-template.md` — full tiered morning briefing template with auto-action handler separation
