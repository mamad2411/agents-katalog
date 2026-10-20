---
name: intelligence-pulse
description: "Perpetual intelligence check — scan saved content, cross-reference against active projects, triage cash-generation pipeline, check actual recent activity, and deliver a structured pulse with focus recommendations, quick wins, and ADHD-sprawl prevention. The heartbeat that keeps the operator on track."
version: 1.36.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [productivity, intelligence, pulse, bookmarks, cross-reference, adhd, bizdev, relevance, notification, focus]
    triggers: [pulse, intelligence, bookmarks, bizdev, adhd, focus, cron, daily-brief, morning-brief]
    related_skills: [adhd-aware-agent-communication, quiet-hours-pulse-digest, project-documentation-standards, daily-pulsar-summarizer]
---

# Intelligence Pulse

**Purpose:** The user saves content constantly — browser bookmarks, YouTube videos to playlists, GitHub repos to stars, X/Twitter bookmarks, LinkedIn posts — with the *intent* of coming back to them, but never does. This skill compensates for that by making those saved items actionable:

1. **Check all sources** for new content since the last scan
2. **Cross-reference** each item against active project priorities (from the monthly roadmap or pulse config)
3. **Attribute relevance** — WHY did the user save this? How does it fit into their stack?
4. **Deliver connections** — point out linkages the user might have missed
5. **Flag urgent/important** items that directly impact active work

## When to Load

- On the **4-hour pulse heartbeat** (cron job) — add an intelligence check section
- On a **daily intelligence digest** run — batch analysis of all new content
- When the user asks "what have I saved recently that's relevant to X?"
- When a cron job triggers a data-source ingestion (bookmarks, YT extraction, etc.)
- **When self-enhancing loop reports regressions** — cross-reference against project health

## Self-Enhancing Loop Integration (2026-08-09)

The intelligence pulse integrates with the autonomous self-enhancing loop. Every pulse cycle, the FOSS Radar phase feeds discovered tools/enhancements into the enhancement registry. The loop then:

- **🟣 Auto-Implement**: Clear improvements auto-executed with rollback safety
- **🟢 Queue for Review**: Worth evaluating, flagged in pulse
- **🟡 Watch**: Tracked for future relevance
- **🔴 Skip**: Irrelevant

**Pulse ↔ Loop Handoff:** When the FOSS Radar phase discovers a tool, it is scored against the project relevance matrix. 🟣 items are auto-implemented via `auto_implementation_engine.py`, recorded in `enhancement-registry.db`, verified through gates, and measured for impact. Regressions are reported in the next pulse.

**Loop Health Check:** Each pulse should query `python scripts/impact_tracker.py --report --json` and flag verification pass rate < 80%, regressions in last 24h, growing Tier 2 queue, or stalled implementation rate.

## Data Sources

| Source | Access Method | Frequency | Notes |
|--------|--------------|-----------|-------|
| **Firefox bookmarks** | Direct SQLite: `places.sqlite` or `intelligence_collector.py` (stdib) | Every 3h (via consolidated pipeline) | Part of the unified PIM ingestion cron. `scripts/intelligence_collector.py` wraps this. |
| **YouTube** | `yt_extract.py` — Firefox Phantom-MCP full library extraction via YouTube Library page. Extracts all playlists (Liked Videos=LL, Watch Later=WL, Favorites, every custom playlist), scrolls each up to 30x. Then `yt_transcripts.py` pulls transcripts for new videos. | Every 3h (via consolidated pipeline) | Was a separate weekly job; now part of the unified 3h pipeline with ChatGPT/Grok. Runs as Step 1 of the pipeline. Auth works because Firefox is already logged in (port 9223). |
| **GitHub starred repos** | `git-stars` MCP server or `intelligence_collector.py` direct query of `gitmcp.db` | Every 3h (via consolidated pipeline) | Was a separate weekly job; now ingested every 3h. Top 100 unseen repos per run. |
| **Gmail AI News** | `email_intelligence.py` — IMAP via `<your-email>@gmail.com` (primary) + `<your-email>@gmail.com` (secondary, IMAP app password auth) | Every pulse | Scans INBOX for AI-keyword emails + known newsletter senders. Secondary account catches AlphaSignal and other subscriptions sent to the operator's personal address. Newsletter processing workflow: see `references/newsletter-tech-signal-processing.md`. |
| **X/Twitter** | `x_intelligence.py` — nitter public scrape + Firefox fallback | Every pulse | Two-tier: public scrape always available, browser extraction when logged in |
| **ChatGPT conversations** | Firefox BiDi on port 9223 via unified pipeline script | Every 3h | Consolidated cron job `PIM Ingestion & Sync — every 3h` (b0490179124c). Patched Firefox already running at port 9223 (DO NOT start new instance). Max 10 convos per run. |
| **Grok conversations** | Firefox BiDi on port 9223 via unified pipeline script | Every 3h | Same consolidated pipeline as ChatGPT. Uses `/c/` URL pattern (not `/chat/`). |
| **Personal Intelligence DB** | Direct SQLite of `pim.db` at `${MY_REPOS}/git-mcp/services/personal-intelligence-mcp/pim.db` | Each check | Centralized knowledge base with ~1500+ tagged items from all sources. Auto-syncs to MemPalace (personal-intelligence wing) every 3h after each pipeline run via `pim_sync_mempalace.py`. See `references/pim-mempalace-sync.md`. |
| **ArXiv Research Feed** | `ai_ecosystem_scan.py` — script at `${USER_HOME}/AppData/Local/hermes/scripts/ai_ecosystem_scan.py` — searches 8 frontier arXiv categories per run | Every 6h (via AI Ecosystem Pulse cron) | Self-contained Python stdlib script (no pip deps). Respects arXiv rate limits (3.5s between queries). Also queries GitHub Trending API for AI repos. See `references/ai-ecosystem-scanning.md`. |
| **Blogwatcher RSS** | Direct SQLite: `~/.blogwatcher-cli/blogwatcher-cli.db` — `articles` + `blogs` tables | Every 4h (no_agent watchdog) | Installed May 30, 2026. 8 feeds: Ars Technica AI, Hacker News, Krebs on Security, MIT Tech Review AI, Manufacturing Dive, TechCrunch AI, The Verge, Wired. Pulse reads DB directly for trend detection. See `references/blogwatcher-setup.md`. |
| **Google News RSS** | `curl` to `news.google.com/rss/search` with Python XML parsing. No dependencies beyond stdlib. | On-demand per pulse | **External web news scanning** — use when `web_extract` or browser tools are unavailable. Supports `after=` date param for recency filtering. Ideal for multi-category regional/local news scanning where no RSS feed exists. Dedup by title; filter obituaries for small-region queries. See `references/google-news-rss-scanning.md`. |

| **A2ASearch FOSS Radar** | `mcp_a2asearch_mcp_search_agents` — query MCP servers, AI coding agents, CLI tools by type | Every pulse | Two-tier: (1) Search trending MCP servers + AI coding agents + agent skills, (2) Follow with `list_agents(type=...)` for top stars. Cross-reference against current stack. See Phase 1.3. |
| **ArXiv Research Feed** | `ai_ecosystem_scan.py` — script at `${USER_HOME}/AppData/Local/hermes/scripts/ai_ecosystem_scan.py` — searches 8 frontier arXiv categories per run | Every 6h (via AI Ecosystem Pulse cron) | Self-contained Python stdlib script (no pip deps). Respects arXiv rate limits (3.5s between queries). Also queries GitHub Trending API for AI repos. See `references/ai-ecosystem-scanning.md`. |
| **GitHub Trending (AI/Agent)** | `web_search` — `site:github.com/trending ai agents OR MCP server OR "open source"` + `blogwatcher-cli` scan for FOSS AI articles | Every pulse | Catch new repos and tools hitting GitHub trending in AI/agent/open-source space. High signal when a new Hermes-compatible tool appears. |

**Consolidation note (May 29, 2026):** The old `Weekly Extraction — YT, GitHub, Bookmarks` cron was eliminated. All external PIM ingestion (ChatGPT, Grok, YouTube, GitHub stars, Firefox bookmarks) now runs as one unified pipeline every 180m via the `PIM Ingestion & Sync — every 3h` job. MemPalace sync runs as the final step — every run, everything new is mined into the `personal-intelligence` wing.

**FOSS Radar addition (June 22, 2026):** Added A2ASearch MCP + GitHub Trending as regular FOSS monitoring sources. See Phase 1.3.

**ArXiv Research Feed (June 22, 2026):** Added as a new data source for bleeding-edge AI/ML coverage. Runs via `ai_ecosystem_scan.py` at `${USER_HOME}/AppData/Local/hermes/scripts/ai_ecosystem_scan.py`. Searches 8 frontier arXiv categories plus GitHub Trending API. See `references/ai-ecosystem-scanning.md`.

## Active Project Cross-Reference

Map new items against these priority buckets. **These priorities change based on the operator's stated focus — listen to his voice messages and adapt.** The table below is the default/fallback; if he says priorities shifted, update this table.

| Priority | Projects | Signals to Watch For |
|----------|----------|---------------------|
| 🔴 **P0** | **Land Sales CRM** — #1 priority Jun 2026 | Lehigh Acres FL spec builders, lot listings, buy boxes, land wholesale deals, builder outreach, Zillow/Trulia/NewHomeSource data |
| 🔴 **P0** | **website-landlord** — lead gen website for land sales | Area lead scraping (Serper Maps + Scrapling), zip-code auto-detect, VA ops pipeline, lead scoring. Active: 105 hot leads from 12302 scan. Tracks as sub-project of Land Sales CRM. |
| 🔴 **P0** | **C2C Revenue** — cash generation | Solumina MES contracts, small integrators (50-500), remote C2C roles $100-200/hr, email responses to outreach |
| 🟡 **P1** | **Intelligence Pipeline** | PIM/memory systems, pulse freshness, dedup across cron jobs |
| 🟡 **P1** | **Agent Ecosystem** | MCP servers, memory layers, model routing, pulse quality |
| 🟡 **P1** | **FOSS Radar** (NEW) | Open-source AI agents, MCP servers, CLI tools, agent skills that could improve Hermes stack. Monitor A2ASearch + GitHub trending. See Phase 2.5. |
| 🟢 **P2** | **YT Animation** | Video gen (Wan2.1, AnimateDiff), consistent characters, AI voice. Pipeline in beta. |
| 🔵 **P3** | **Bookends** (ON HOLD — was P0) | Only if the operator explicitly re-engages |
| 🔵 **P3** | **Construct Manage** (ON HOLD — was P0) | Only if the operator explicitly re-engages |
| 🔵 **P3** | **Solumina Agent** (BLOCKED) | Solumina/ExampleVendor news — only actionable when contract obtained |

**Items no longer in scope (removed per the operator):**
- ❌ Scouts project — ON HOLD, do not mention
- ❌ Model Gateway — not a priority, do not recommend decisions about it
- ❌ Tax payments — not relevant, do not mention
- ❌ Twitch Farm — removed, not a priority
- ❌ Burn Bounty (BCH) — removed, not a priority

## Workflow

### Phase 0: FRESHNESS FIRST — Check Before Reporting

**This is the single most important rule for every pulse. the operator explicitly called out stale, repetitious responses as a problem. Apply this before any other phase.**

**1. Check prior pulse outputs via session_search before reporting anything.**
- Use `session_search(query="<pulse name>", sort="newest", limit=2)` to find what you last reported
- Read the most recent output with `session_search(session_id="...", around_message_id=...)` to see the exact content
- Only report items that are GENUINELY NEW — never repeat what was already surfaced

**2. "Nothing new" is a VALID and PREFERRED output.**
- Sections with no change → "No change since last scan" or omit entirely
- Full pulse with nothing new → Stay SILENT. Do not deliver "nothing new to report" — that's been explicitly rejected as spam.
- Only deliver when there's actual news worth the operator's attention

**3. Watchdog pattern: Silent when healthy, vocal when broken.**
- Infrastructure pulse: don't list 79/79 healthy containers every 4 hours. Only report CHANGES.
- Intelligence pulse: don't re-list blog articles from the last scan. Only report NEW items.
- The quieter the pulse, the better it's working.

**4. Deduplicate across sources.**
- Same item from bookmark AND YouTube? Report it once, note the source.
- Same finding from last week? Don't re-report.
- Use URL hash or title match as dedup keys.

The ingestion pipeline runs as a separate cron job (`PIM Ingestion & Sync — every 3h`). For pulse delivery, you usually don't need to re-ingest — you just need to check what was ingested since the last pulse. **Try PIM direct queries first, but beware: the DB can be locked by the MCP server (see Timeout Mitigation below).**

**Preferred approach (fast when it works):**
```bash
# Count new items by source type since last check
sqlite3 "${MY_REPOS}/Documents/github/git-mcp/services/personal-intelligence-mcp/pim.db" \
  "SELECT source_type, COUNT(*) FROM saved_items WHERE ingested_at > datetime('now', '-4 hours') GROUP BY source_type;"

# Full details of new items
sqlite3 "${MY_REPOS}/Documents/github/git-mcp/services/personal-intelligence-mcp/pim.db" \
  "SELECT source_type, substr(title,1,55), tags, ingested_at FROM saved_items WHERE ingested_at > datetime('now', '-4 hours') ORDER BY ingested_at DESC LIMIT 20;"
```
Full query library in `references/pim-fallback-queries.md`.

**When you need fresh ingestion (rare — only if PIM data is stale):**
```python
# Run intelligence_collector.py check-new — does ALL of the following:
# 1. Firefox bookmarks via direct places.sqlite
# 2. GitHub stars via gitmcp.db query
# 3. Gmail AI news via imaplib
# 4. YouTube via yt-dlp search
# 5. X/Twitter via nitter public scrape + Firefox fallback
# 6. Blogwatcher RSS via direct SQLite (~/.blogwatcher-cli/blogwatcher-cli.db)
#
# Returns JSON grouped by source_type and project tag.
```

The single command is:
```bash
cd ${MY_REPOS}/hermes-config && python scripts/intelligence_collector.py check-new
```

**⚠️ Timeout mitigation — multiple layers, not just Firefox:**

The `check-new` action does NOT just query PIM — it calls `main()` FIRST, which spawns ALL of these subprocesses sequentially:
1. Firefox bookmarks extraction (places.sqlite — can hang if Firefox holds a lock)
2. GitHub stars ingestion (fast — gitmcp.db query)
3. **Email intelligence** (`email_intelligence.py` via `subprocess.run(timeout=60)`)
4. **YouTube extraction** (`yt_intelligence.py` via `subprocess.run(timeout=90)`)
5. **X/Twitter scan** (`x_intelligence.py` via `subprocess.run(timeout=120)`)
6. THEN queries PIM for new items since last check

Any ONE of these subprocesses hanging causes the entire command to time out. The 60s timeout on email or 120s on X/Twitter can cascade.

**⚠️ NEW FAILURE MODE (observed June 8, 2026): PIM DB locked by its own MCP server.**
Both `intelligence_collector.py` AND direct SQLite queries to `pim.db` can hang simultaneously. The personal-intelligence MCP server (if running) holds an exclusive SQLite write lock that prevents any concurrent connection — even read-only queries with `PRAGMA busy_timeout=5000` block indefinitely. The DB stays locked as long as the MCP server is active. This means the `pulse_query_pim.py` script, `sqlite3` CLI fallback, and all documented PIM direct queries ALL fail in this state. **This is not a transient glitch — it's a structural constraint when the MCP server runs alongside cron pulse jobs.**

**Full fallback chain (Tiers 1→2→3):**

| Tier | Method | Success Rate | When To Try |
|------|--------|-------------|-------------|
| **1** | `terminal(timeout=90)` on `intelligence_collector.py check-new` | ~60% in cron context | First attempt. If it hangs past 20s with no output, assume locked. |
| **2** | PIM DB direct query (`sqlite3` CLI or `pulse_query_pim.py`) | ~70% (fails when MCP server holds lock) | Try after Tier 1 fails. If it also hangs >20s, MCP has the lock. |
| **3** | MCP tools as intelligence source | ~95% (independent of SQLite) | Use MCP tools to query git-stars and/or personal-intelligence servers directly. These work even when the underlying DB is locked. See `references/fallback-mcp-intel.md`. |

**⚠️ Critical implementation detail:** Each tier consumes wall-clock time and tool-call budget. **Do not attempt all three sequentially** — if Tier 1 hangs for 90s and Tier 2 hangs for 20s, you've burned 110s and multiple tool calls. Instead:
- Run Tier 1 with `timeout=20` (not 90) — enough to detect whether the script starts producing output or is stuck
- Run Tier 2 with `timeout=10` — if sqlite3 doesn't return instantly, MCP has the lock
- If both Tier 1 and Tier 2 hang, **bail immediately to Tier 3**. Don't keep retrying.
- Tier 3 MCP calls (git-stars list/search, personal-intelligence health) return almost instantly regardless of DB lock state. They bypass SQLite entirely and talk to the running server process.

Full query library in `references/pim-fallback-queries.md`.

**ESCALATION (if you actually need fresh ingestion and suspect the ingestion pipeline itself is stalled):**
Pass `terminal(timeout=90)` instead of the default 30s. Most Firefox locks resolve within 60s, but the cumulative subprocess chain means you may need 90-120s for the full pipeline. **But be warned: if Firefox itself is not running (port 9223 down), no amount of timeout will help.**
For full counts, recent items, and source breakdown, see `references/pim-fallback-queries.md`. The sqlite3 CLI approach is preferred for simple queries (one-liner, no quoting issues). If you need Python features (row_factory, JSON parsing), use the standalone `scripts/pulse_query_pim.py` — run it directly with:

```bash
python scripts/pulse_query_pim.py              # Last 4h items by source
python scripts/pulse_query_pim.py --recent      # Recent item titles + URLs
python scripts/pulse_query_pim.py --sources     # Source freshness check
python scripts/pulse_query_pim.py --all         # Full summary
python scripts/pulse_query_pim.py --hours 24    # Custom time window
```

The script resolves the PIM DB path automatically (uses `${MY_REPOS}/Documents/github/git-mcp/services/personal-intelligence-mcp/pim.db` or `$PIM_DB_PATH` env var override).

**⚠️ `pulse_query_pim.py` silent failure signal:** When the script fails (DB locked by MCP server, path resolution error, or import issue), it outputs exactly **"SCRIPT_FAILED"** as its stdout. This is distinct from the script hanging — if you see this literal string, the DB was reachable but the script errored internally. Immediately fall through to the Tier 3 MCP fallback — do not retry the script or try sqlite3 CLI (same DB lock).

**Do NOT use `timeout 15` or any value under 45s** — Firefox DB contention can take 30-60s to resolve. Premature timeout wastes time and produces an empty report. Prefer `terminal(timeout=90)` over wrapping the command in `timeout 90` for better integration with the Hermes tool lifecycle.

**⚠️ `python -c` inline script — no longer blocked in `terminal()` (June 2026):** Early Hermes versions blocked `python -c` execution via the `execute_code` tool security layer (pattern: `script execution via -e/-c flag`). `python -c` inside a `terminal()` call is now confirmed working for SQLite queries and general Python scripting. **Environment note:** use `E:/` (Windows-native) paths — Python's `sqlite3.connect()` does not resolve MSYS `/e/` paths. Still prefer sqlite3 CLI for simple queries (cleaner, no quoting edge cases). Full examples in `references/pim-fallback-queries.md`.

Three modes available:
- `collect` — Full ingestion run (all sources, no reporting)
- `check-new` — Ingest + report items since last check timestamp
- `check-all-week` — Ingest + report items from past 7 days

### Phase 1.5: Proactive Blogwatcher Scan (if stale)

The blogwatcher feeds often go 24-48h between scans (no_agent watchdog drift). Before reading articles, check when each feed was last scanned:

```bash
blogwatcher-cli blogs
```

If any feed's `Last scanned` is >24h old — or you see no date at all — **run a scan first**:

```bash
blogwatcher-cli scan
```

This pulls fresh articles into the DB. Then read what's new:

```bash
blogwatcher-cli articles   # unread only — articles tagged [new] are since-last-scan
```

**Do NOT skip this step** even if `intelligence_collector.py` succeeded — the collector's blogwatcher read may be stale data from the SQLite file that hasn't been refreshed. Proactive scanning catches articles the ingestion pipeline missed.

**⚠️ Blogwatcher DB contention after scan:** `blogwatcher-cli scan` holds an exclusive SQLite write lock while inserting new articles. If you run `blogwatcher-cli articles` (or direct SQLite queries to `~/.blogwatcher-cli/blogwatcher-cli.db`) immediately after a scan, both will hang or return exit code 1 with no output. This is structurally identical to the PIM MCP lock pattern — the writing process blocks all concurrent readers.

**Mitigation:** If `blogwatcher-cli scan` succeeded (printed "Found N new articles") but `blogwatcher-cli articles` returns exit code 1 with empty output, the scan process still holds the lock. Wait 5-10 seconds and retry the articles listing. If it's a no_agent watchdog cron that ran just before you, the lock may persist longer. Fall back to the SQLite queries in `references/blogwatcher-setup.md` — but note those will ALSO fail if the lock is active. The safest pattern: run the scan in a separate terminal call, then wait briefly before querying articles.

```bash
# Safe pattern: scan, small pause, then read
blogwatcher-cli scan && sleep 5 && blogwatcher-cli articles --limit 15
```

**Manufacturing Dive specific (BizDev lead gen):** When scanning returns Manufacturing Dive articles with "[new]", flag the count in the pulse. These are potential lead sources for MES industry intelligence — one article surfaces a new factory buildout, which means a new Solumina/ExampleVendor prospect.

### Phase 1.25: Firefox Health Check (Pre-Flight for Firefox-Dependent Sources)

The PIM ingestion pipeline depends on Firefox BiDi on port 9223 for YouTube, ChatGPT, Grok, and bookmarks extraction. If PIM data looks stale or you see a partial pipeline stall (email items only, nothing from Firefox-dependent sources), check Firefox before investigating further:

```bash
# Quick health check via the dedicated script
python "${USER_HOME}/AppData/Local/hermes/scripts/firefox-health.py" check

# Expected output: HEALTHY
```

If the script returns anything other than `HEALTHY` (or if the command itself fails with a MSYS path error — see Phase 6 MSYS pitfall), Firefox is down. Restart it:

```bash
python "${USER_HOME}/AppData/Local/hermes/scripts/firefox-health.py" start
# Expected output: [FF-HEAL] Starting Firefox headless on port 9223...
#                 [FF-HEAL] Firefox ready after ~1s
#                 STARTED
```

The `firefox-health.py` script launches headless Firefox on port 9223 using the profile at `${USER_HOME}\AppData\Local\hermes\firefox-profile`. It typically comes up in ~1s. The script can also check, start, or restart with `watchdog` mode (silent when healthy, vocal when action needed).

**When to run this check:**
- PIM DB returns items ONLY from `source_type='email'` — the IMAP connector works (fast, no Firefox dep) but everything else is silently failing
- `ingested_at` timestamps in pim.db are >6h old despite the pipeline cron showing `ok`
- `hermes cron list` shows the `stealth-browser-watchdog` or `Firefox Remote Debugging Watchdog` last ran with an error or timeout
- curl to `http://localhost:9223/json/version` returns nothing (no connection)

**When to SKIP this check:**
- PIM data is flowing normally from all source types with fresh timestamps — Firefox is healthy, don't waste a tool call
- The pulse is targeting sources that don't need Firefox (sqlite3 PIM queries alone, blogwatcher CLI, git log)

See `references/firefox-remote-debugging-setup.md` for full Firefox BiDi troubleshooting, session exhaustion handling, and Grok SPA content extraction.

### Phase 1.75: Categorization Health Check (Every Pulse)

Before cross-referencing individual items, check the **overall categorization health** of the PIM — a pulse that reports "N items in PIM" without flagging the untagged gap is missing a key signal.

```bash
# Untagged items per source
sqlite3 "${MY_REPOS}/Documents/github/git-mcp/services/personal-intelligence-mcp/pim.db" \
  "SELECT source_type, COUNT(*) FROM saved_items WHERE tags IS NULL OR tags = '[]' OR tags = '' GROUP BY source_type ORDER BY COUNT(*) DESC;"
```

**What to flag:**
- If >30% of items are untagged, the PIM is a hoard, not an asset. Mention in pulse: "N untagged items — 10-min batch-scan would unlock value."
- If P0-project tags (bookends, construct-manage) have <5 items each while P1 tags have 300+, the operator's saving behavior is misaligned with his priorities.
- Growth trend: track the untagged count week-over-week. If it's widening, flag the pattern.

Full query library in `references/pim-fallback-queries.md` under "Categorization Health Dashboard."

### Phase 2: Cross-Reference Each Item

For each new item, determine:
1. **Which project(s) does this relate to?** — Check the title, description, tags against priority keywords
2. **Why did the user save it?** — If it's a bookmark, check the parent folder name; if GitHub, check the topics; if YouTube, check the channel/title
3. **What's the connection?** — Is this a tool that could replace something in their stack? A dependency they're already using? A competitor to their own project?
4. **Urgency** — Is this time-sensitive? (RFP deadlines, API deprecations, conference CFPs)

### Phase 2.5: FOSS Radar — Open-Source AI/Agent/MCP Scan

**Purpose:** Spot new open-source tools that could improve the operator's stack — Hermes Agent upgrades, MCP servers, AI coding agents, CLI tools, agent skills. the operator explicitly wants this band widened to catch anything that enhances what's already running.

**When to run:** Every pulse (4h cycle) + every Morning Brief (7am). Quick scan — takes <2min. Can parallelize with Phase 3.

**Sources to query (run ALL in parallel):**

```python
# 1. A2ASearch — structured search across MCP servers, AI coding agents, CLI tools, agent skills
# Search for trending content
mcp_a2asearch_mcp_search_agents(query="MCP server", limit=5)
mcp_a2asearch_mcp_search_agents(query="AI coding agent", limit=5)
mcp_a2asearch_mcp_search_agents(query="Hermes AI agent", limit=3)

# 2. List by category (sorted by stars for popularity)
mcp_a2asearch_mcp_list_agents(type="MCP Server", sort="stars", limit=5)
mcp_a2asearch_mcp_list_agents(type="AI Coding Agent", sort="stars", limit=5)
mcp_a2asearch_mcp_list_agents(type="Agent Skill", sort="stars", limit=5)
mcp_a2asearch_mcp_list_agents(type="CLI Tool", sort="stars", limit=5)

# 3. GitHub trending — fresh AI/open-source repos hitting front page
web_search(query="site:github.com/trending ai agents OR MCP open source", limit=3)
web_search(query="best new open source AI agent tools June 2026", limit=3)
```

**How to evaluate each result:**

| Score | Label | Criteria |
|-------|-------|----------|
| 🟣 | **Auto-Implement** | Clear improvement over what we're running. Directly aligns with stack, fills a documented gap, or replaces a paid tool with a better FOSS alternative. Install, configure, inform the operator, commit, and document all changes. |
| 🟢 | **Try it** | Worth installing/evaluating soon. Improves Hermes Agent, fills a gap in the stack, replaces a paid tool, or adds capability we're missing. Flag for next actionable slot. |
| 🟡 | **Watch** | Interesting but not immediately actionable. Might become relevant later. |
| 🔴 | **Skip** | Irrelevant, low quality, or duplicates something we already have. |

**🟣 Auto-Implement Protocol (when you score something purple):**
Only trigger auto-implement when the tool is a **clear improvement** over what's currently running or in **direct alignment** with the stack. Do not implement speculatively.

1. **Install** the tool — use the appropriate method (pip, npm, cargo, go, brew, docker, git clone + setup)
2. **Configure** it — integrate with existing Hermes config (config.yaml, MCP server configs, skills, cron jobs)
3. **Test** it — verify it works, check for conflicts with existing setup
4. **Commit** all changes — use meaningful commit messages describing what was added and why
5. **Document** — update relevant docs (config files, skill docs, READMEs, AGENTS.md)
6. **Inform** — in the pulse report, note what was implemented with a brief summary of changes made

**Default bias: DO NOT implement** unless the tool is:
- A clearly superior replacement for something currently in the stack (better performance, more features, FOSS替代 paid)
- A direct enhancement that aligns with an active project or known gap (fills a need that's been documented)
- Something that enables a capability the operator has explicitly wanted

**When NOT to auto-implement:**
- The tool is merely interesting or "nice to have" — flag as 🟢 Try it instead
- It requires paid API keys or subscriptions not already available — flag as 🟢 Try it
- It conflicts with a core system (Hermes Agent itself, gateway, critical MCP servers) — flag as 🟡 Watch
- It's a major dependency that could destabilize the environment — flag as 🟢 Try it instead
- You don't have sufficient information to evaluate it safely — flag as 🟡 Watch instead
- It solves a problem that doesn't exist yet — flag as 🟡 Watch

**Specific things to watch for (Hermes ecosystem):**
- New MCP servers that could replace components in the current config
- AI coding agents that are Hermes-compatible or better than what's running
- Agent skills or workflows that solve problems the operator has documented
- CLI tools that reduce friction in the existing pipeline
- FOSS alternatives to paid services the operator uses

**Reporting format for FOSS Radar section in pulse:**
```
🧪 **FOSS RADAR**
🟣 [tool-name](url) | AUTO-IMPLEMENTED — what was done, what it replaced
🟢 [tool-name](url) | Why it improves the stack
🟡 [tool-name](url) | Keep on radar — [reason]
🔴 [tool-name](url) | Skip — [reason]
```

**When nothing new:** Omit the section entirely (don't report "nothing new"). If previously flagged tools have changed status, report the delta only.

**Edge case — rate limits:** A2ASearch is an external API. If it's down or slow, skip gracefully and report "FOSS radar: unavailable this cycle". Don't retry.

### Phase 3: BizDev Pipeline Triage (P0 Cash Generation)

**⚠️ Check recruiter emails as cash-generation leads.** After Phase 1's intelligence scan, check if any new items have `source_type='email'` and contain AI Engineering / MES / platform-engineering keywords in their title. These should NOT just be logged — they should be **forwarded to the Job Agent pipeline** as qualification leads. A single C2C placement at $150/hr changes the month. The pulse should flag: "N recruiter emails found — these are cash-generation leads. Classify through Job Agent before they go cold."

Cash generation is the #1 priority. Before delivering the pulse, check the BizDev Agent pipeline (AND cross-reference recruiter emails from Phase 1):

```python
# Via MCP (bizdev-agent MCP server):
mcp_bizdev_agent_bizdev_dashboard()       # high-level stats
mcp_bizdev_agent_bizdev_followups(limit=5) # pending actions
mcp_bizdev_agent_bizdev_list_targets()     # top targets
```

Key metrics to flag:
- **total_outreach = 0** is a RED FLAG — means the pipeline is populated but nobody has been contacted
- **contracts_won = 0** when there are 4+ contracts in pipeline — stalled conversion
- **pending_followups = 0** — either nothing needs follow-up OR nothing is moving
- **pipeline_value** not growing between pulses
- **BizDev MCP followups quirk:** `bizdev_followups()` may return empty `[]` even when dashboard shows `pending_followups: 14`. This is a known data inconsistency in the MCP server — the dashboard count may include stale or untyped items that the followups endpoint filters out. Do NOT trust `bizdev_followups()` alone: cross-check against dashboard `pending_followups` count. If dashboard says >0 but followups returned empty, the pipeline has orphaned items needing manual cleanup, not zero actionable followups.

If the operator has 39+ targets but 0 outreach, call this out as the #1 cash generation gap.

### Daily Cash-Flow Briefing (Morning Cron)

A specialized, cash-focused variant of the pulse that runs every morning at 8am ET. It synthesizes **four sources** into a scannable, action-oriented report:

| Stream | Tool | Signal |
|--------|------|--------|
| **C2C Hunter** | `session_search(query="C2C Hunter", sort="newest", limit=2)` | Direct recruiter contacts, rates, demand waves |
| **BizDev Pipeline** | `mcp_bizdev_agent` MCP tools | Targets, outreach, contracts, followups |
| **Overnight Recruiter Emails** | PIM DB direct query: `source_type='email'` in last 48h | New recruiter leads |
| **Business Intel Monitoring** | Read `latest.json` at `${USER_HOME}/trumpian-accounting-kb/monitoring/findings/latest.json` | FL land deals, GovCon contracts, opportunity signals |

**Business Intel cross-reference query:**
```python
python -c "import json; f=open('${USER_HOME}/trumpian-accounting-kb/monitoring/findings/latest.json'); data=json.load(f); [print(f'{x[\"category\"]}: {x[\"headline\"][:80]} [{x[\"relevance_score\"]}]') for x in data if x.get('category') in ('fl_land_intel','govcon_c2c_intel','opportunity_signals') and x.get('relevance_score',0)>=0.5]"
```
Flag any finding directly connected to a cash opportunity — GovCon contract awards, builder acquisitions (land deal), or opportunity signals that could become revenue.

**When to use this:** This is NOT a replacement for the full pulse (Phase 4-9). It's a stripped-down, velocity-focused delivery that prioritizes cash-generation leads over project intelligence. Only use it for the explicitly-titled Daily Cash-Flow Briefing cron job.

Full workflow documented in `references/cash-flow-briefing.md` — including the exact C2C Hunter session_search + scroll pattern, PIM recruiter-email queries, BizDev MCP calls, Business Intel cross-ref, and delivery format.

### Morning Brief Consolidation (7:01 AM EST)

The Morning Brief is the 7:01 AM ET consolidation cron (triggered by `quiet-hours-pulse-digest`) - NOT the same as the Daily Cash-Flow Briefing. It uses an **inverted workflow** (digest-first, verify independently, synthesize). Full delivery format, section rules, opening-line rules, [SILENT] conditions, and cron-specific pitfalls: `references/morning-brief-consolidation.md`.

### Phase 4: Cross-Reference Intelligence Against Active Priorities

For each new item found in Phase 1, determine:
1. **Which project(s) does this relate to?** — Check title/description/tags against priority keywords
2. **Why did the user save it?** — Browser folder name, GitHub topics, YouTube channel context
3. **Whats the connection?** — Is this a tool that could accelerate their stack? A competitor to their own project?
4. **Urgency** — Time-sensitive? (RFP deadlines, API deprecations, conference CFPs)

If a cross-project connection exists that the user probably missed, call it out explicitly (e.g., 'That OpenRouter data about model routing? It maps directly to your Model Gateway project').

### Phase 5 (Augmented): User Commitments — Open Loops, Decisions, Risks

Beyond project priorities and new intelligence items, check the user's own commitment management system. The Command OS stores deadlines, pending decisions, and active risks — and these are often **more urgent** than any new intelligence item.

Files live under `_project/04-shared-memory/`:

- **Open Loops Register** (`playbooks/open-loops.json`) — items requiring the operator's attention with deadlines and priority. Flag any loop with a deadline within the next **7 days**, especially 🔴 CRITICAL loops. These are the week's real non-negotiables.
- **Decision Log** (`decisions/log.md`) — pending decisions (🟡 Pending / 🟡 Planned) that need promotion to action. Check whether any new intelligence or recent activity changes the context for a pending decision.
- **Risk Register** (`risks/register.md`) — active 🔴 CRITICAL and 🟡 HIGH risks. Acknowledge any risk whose status has changed or which is affected by today's findings.

Quick reads (fast, no parsing needed):
```bash
# Get deadline dates from open loops — use Python JSON parser, grep is fragile on nested JSON
# NOTE: cd first to avoid MSYS path issues in Python's open() on Windows
cd ${MY_REPOS}/_project && python -c "
import json
with open('04-shared-memory/playbooks/open-loops.json') as f:
    data = json.load(f)
loops = data if isinstance(data, list) else data.get('loops', [])
for loop in loops:
    status = loop.get('status', '?')
    deadline = loop.get('deadline', 'none')
    desc = loop.get('description', '?')[:50]
    print(f'  {loop[\"id\"]} [{status}] due {deadline}: {desc}')
"

# Check pending decisions
grep '🟡 Pending\|🟡 Planned' ${MY_REPOS}/_project/04-shared-memory/decisions/log.md | head -5

# Check active CRITICAL risks
grep '🔴 CRITICAL' ${MY_REPOS}/_project/04-shared-memory/risks/register.md | head -5
```

**Priority rule:** If a critical open loop has a deadline within 7 days, **elevate it to the pulse headline** — it takes precedence over new intelligence items. The Phase 9 focus recommendation should reference the nearest deadline as a forcing function. Pulse delivery that ignores the user's own deadlines is noise.

### Phase 6 (Augmented): Full Context Layer — Session + Git + MemPalace

Do NOT just check intelligence sources. The pulse should also reconstruct **what the user actually did** across all available context layers.

**Quick Session Check (do this first — often the highest-signal finding):**
Run browse-mode session_search before checking repos or intel. Session titles and previews reveal what the user accomplished since the last pulse — shipped repos, strategy sessions, outreach — that git commits alone won't capture. If the user was active in Discord/CLI, this becomes the top pulse finding.

```bash
session_search()  # browse mode — last 3 sessions by recency with source labels
```

Parse the results for sessions with `source: "discord"` or `source: "cli"`. Read the preview to extract accomplishment-level findings. In testing from cron context, browse mode returned user sessions as the top 3 results when the user had been recently active (contrary to the earlier pitfall that cron sessions always dominate — the behavior appears resolved or activity-dependent). Even when git shows zero commits, user session findings can carry the pulse.

```bash
# STEP 0: Discover repos — new ones appear frequently without warning.
# Use a dynamic scanner instead of a hardcoded list. This catches every
# repo with recent activity, including ones you don't know about yet.
#
# ⚠️ Use cd + git, NOT git -C. On MSYS/Windows, git -C can return exit
# code 128 when a repo has a .git.broken.* directory alongside its .git
# dir (known git-for-windows edge case). The ghl repo is confirmed. The
# cd approach works every time.
for d in ${MY_REPOS}/*/; do
  repo=$(basename "$d")
  commits=$(cd "$d" && git log --oneline --since="48 hours ago" 2>/dev/null | wc -l)
  if [ "$commits" -gt "0" ]; then
    latest=$(cd "$d" && git log --oneline -1 --format="%as %an: %s" 2>/dev/null)
    authors=$(cd "$d" && git log --since="48 hours ago" --format="%an" 2>/dev/null | sort -u | tr '\n' '/' | sed 's|/$||')
    echo "  $commits commit(s) in $repo: $latest [authors: $authors]"
  fi
done

# Any repo with activity that isn't in the roadmap's P0-P2 list is
# scope creep — flag it in the ADHD sprawl check.

# STEP 1: P0-specific deep check — wider window for repos that
#         often go cold for days between bursts.
# ⚠️ Use cd + git, NOT git -C (see pitfall below for .git.broken.* issue)
for repo in ${MY_REPOS}/constructManage ${MY_REPOS}/bookends; do
  if [ -d "$repo" ]; then
    commits=$(cd "$repo" && git log --oneline --since="14 days ago" 2>/dev/null | wc -l)
    echo "  $commits commit(s) in $(basename $repo) (14d): $(cd "$repo" && git log --oneline -1 --format='%s' 2>/dev/null)"
  fi
done

# STEP 2: Session search — find sessions that touched P0/P1 projects.
#          CRITICAL: in cron context, session_search bookends can carry
#          full skill content (~200KB+). Use browse mode first to find
#          the right session, then scroll with targeted around_message_id.
session_search()  # browse mode — last 3 sessions, no bloated bookends
session_search(query="bookends OR construct-manage OR bizdev OR model-gateway OR agent-fleet OR spacebar OR fermi", sort="newest", limit=3)
```

**Repo map changes over time** (check which repos exist before relying on git log):
- `git-mcp` was absorbed/renamed — its services (personal-intelligence-mcp, firefox-remote-mcp, git-stars) now exist elsewhere or as standalone MCP servers
- `constructManage` is a top-level repo at `${MY_REPOS}/constructManage/` — NOT inside hermes-config
- `bookends` is at `${MY_REPOS}/bookends/`
- `model-gateway` is at `${MY_REPOS}/model-gateway/`
- Always `ls ${MY_REPOS}/` to discover new repos that may have been created since the last check

#### P0 Deep Check (14-day window)

P0 projects go cold frequently — Bookends and ConstructManage both stall just before shipping. Run an extended window to detect the stall-just-before-shipping pattern:

```bash
for repo in ${MY_REPOS}/constructManage ${MY_REPOS}/bookends; do
  if [ -d "$repo" ]; then
    commits=$(cd "$repo" && git log --oneline --since="14 days ago" 2>/dev/null | wc -l)
    last_commit=$(cd "$repo" && git log --oneline -1 --format="%as %an: %s" --since="30 days ago" 2>/dev/null || echo "(none in 30d)")
    last_date=$(cd "$repo" && git log -1 --format="%as" 2>/dev/null || echo "no commits")
    echo "  $commits commit(s) in $(basename $repo) (14d): $last_commit | last_commit: $last_date"
  fi
done```
```

If a P0 project had bursts of activity in the last 14 days but no commits in the last 3-7 days → **stall-just-before-shipping** pattern detected. Flag it in the pulse with the exact date of the last commit.

**This check is mandatory every pulse, even when the main 48h scan is busy.** A P0 project that went cold 7 days ago after being "almost done" is a bigger signal than 22 commits on P1/P2 infrastructure.

#### Cross-Repo Same-Date Stall Detection

**New in v1.19.0:** Flag when multiple repos share the exact same last-commit date. This is a systemic signal, not coincidence — it usually means the user hit a migration wall, made a frustrated "pre-migration commit" across all projects, and abandoned them simultaneously.

Detection (add after the P0 deep check loop). **Use the standalone script** — it auto-detects the correct repo base path:

```bash
# ✅ Use quoted Windows-native path — MSYS /c/ paths fail when passed to Windows Python
python "${USER_HOME}/AppData/Local/hermes/skills/productivity/intelligence-pulse/scripts/cross_repo_freeze_check.py"

# Or with explicit GITHUB_BASE env var if the auto-detect fails:
GITHUB_BASE="${MY_REPOS}/Documents/github" python "${USER_HOME}/AppData/Local/hermes/skills/productivity/intelligence-pulse/scripts/cross_repo_freeze_check.py" --hours 7
python "${USER_HOME}/AppData/Local/hermes/skills/productivity/intelligence-pulse/scripts/cross_repo_freeze_check.py" --json
python "${USER_HOME}/AppData/Local/hermes/skills/productivity/intelligence-pulse/scripts/cross_repo_freeze_check.py" --full
```

**⚠️ Important:** The script is in the skill's `scripts/` dir, NOT in `hermes-config/scripts/`. Always reference it by full path from the skill location above, or copy it locally. If running inside a cron prompt that has its own workdir, verify the path resolves correctly.

**⚠️ MSYS path pitfall:** Do NOT use `/c/Users/...` MSYS-style paths when calling Python scripts through `terminal()`. MSYS reduces `/c/` to the current drive mount point (e.g., `E:\c\...`) rather than resolving to `C:\...`, producing a "can't open file" error. Always use Windows-native paths with forward slashes and double quotes:

```bash
# ✅ WORKS — quoted Windows path with forward slashes
python "${USER_HOME}/AppData/Local/hermes/skills/productivity/intelligence-pulse/scripts/cross_repo_freeze_check.py"

# ❌ FAILS — MSYS /c/ path confuses native Windows Python
python ${USER_HOME}/.../cross_repo_freeze_check.py
```

**⚠️ Broader MSYS path failure — `/e/` paths in Python arguments:** The same failure mode hits `/e/` paths too. When you pass a variable-expanded MSYS path to `python.exe` as a script argument:

```bash
# ❌ FAILS — variable with /e/ path passed to Windows Python
SCRIPTS="${MY_REPOS}/_project/scripts/unseen-backlog.py"
python "$SCRIPTS" list --unseen-only

# Observed result: can't open file 'C:\e\yourdata\...'
```

MSYS translates literal `/e/` paths for bash commands (ls, git, cd), but path translation is unreliable when the path travels through variable expansion and into a Windows-native executable argument. The fix for ALL Python script invocations on this host:

```bash
# ✅ WORKS — cd to the repo root first, then use relative path
cd ${MY_REPOS}/_project && python scripts/unseen-backlog.py list --unseen-only
```

This applies to ANY Python script call where the path starts with `/e/` or `$MSYS_MOUNT_PREFIX`. Use `cd` + relative path, never `python /e/...` or `python "$VARIABLE"`. This pattern is already used correctly for `intelligence_collector.py` (`cd /e/.../hermes-config && python scripts/...`) and the open-loops JSON reader (`cd /e/.../_project && python -c "..."`).

For inline Python (`python -c`) that opens files by path, use `E:/` Windows-native notation — MSYS does not translate paths inside `-c` string arguments:

```bash
# ✅ WORKS — E:/ is valid on both Windows and MSYS
python -c "import json; d=json.load(open('${MY_REPOS}/.../unseen-backlog.json'))"

# ❌ FAILS — /e/ inside -c string is passed raw to Windows Python
python -c "with open('${MY_REPOS}/...') as f: ..."
```

This applies to ALL skill scripts run via `terminal()`. `python "C:/..."` is the safe pattern. The `/c/...` alias works for bash commands (ls, cd, git) but NOT when passed as an argument to a Windows-native executable like python.exe.

The script lives under the `intelligence-pulse` skill at `scripts/cross_repo_freeze_check.py`. It walks every git repo under `GITHUB_BASE` (default: `${MY_REPOS}/`), extracts last-commit date + message + author, and outputs:

- **Multi-repo stalls** — ≥3 repos with the same last-commit date AND that date is >`STALL_DAYS` ago
- **Pre-migration freezes** — a multi-repo stall where ≥3 of the repos have commit messages containing "pre-migration" or "prep:" — the classic migration-wall-abandonment pattern
- **Recent human activity** (with `--full`): non-autogit commits in the last 48h, for user-absence detection

**Fallback (quick inline check if script isn't available):**
```bash
for d in ${MY_REPOS}/*/; do
  repo=$(basename "$d")
  [ -d "${d}.git" ] && echo "$repo:$(cd "$d" && git log -1 --format='%as' 2>/dev/null || echo 'no-commits')"
done | sort -k2
```
Then group manually. The awk one-liner for automated grouping is fragile on MSYS (brace+quote conflicts with `terminal()` shell invocation) — prefer the Python script.
```

**What to flag:** If 3+ repos all share the same last-commit date AND that date is >3 days ago, this is a **multi-repo stall** — more severe than a single-project stall. The likely root cause:
- The user attempted a migration/refactor that required touching everything at once
- The migration introduced friction (broken builds, config changes, docs to update)
- The user bounced off the friction and moved to a different (more fun) project
- All the stalled repos share a commit message like "pre-migration commit" or "prep"

**Pulse response:** Name the date and the number of repos explicitly. Ask whether the migration completed or stalled. Recommend either finishing the migration on ONE repo as a proof-of-concept, or documenting the blocker and officially parking the repos.

#### Cross-Pulse Reference: Check Other Pulse Outputs

**Problem:** Multiple cron jobs run on the same 4h cadence (self-healing pulse, dev-lead-pulse, qa-lead-pulse, etc.), but the operator's Pulse only checks git + PIM + sessions — it never reads what OTHER pulses discovered. This creates a blind spot: the self-healing pulse may find a Docker container OOM-crashing for 8 hours, while the operator's Pulse reports "no activity" across repos. The two systems exist in parallel silos.

**Fix:** Before reporting project status, check the daily digest file for recent findings from **other pulses** that may affect project status:

```bash
# Read today's digest for non-the operator pulse findings
# The digest appends every pulse's output as "## HH:MM — Pulse Name" blocks
grep -i -A3 "Self-Healing\|dev-lead\|qa-lead\|integration-lead\|docs-lead\|skills-lead" \
  "${MY_REPOS}/_project/daily-digest/$(TZ='America/New_York' date +%Y-%m-%d).md" 2>/dev/null
```

**Which pulses to cross-reference:**

| Pulse | Relevance to the operator's Pulse | Key Signals |
|-------|-----------------------------|-------------|
| **Self-Healing Pulse** (4h) | **HIGH** — infrastructure issues affect project work | Container crash-loops (OOM), disk pressure, gateway state, Firefox down |
| **dev-lead-pulse** (4h) | MEDIUM — engineering changes | Codebase health, config changes, skill updates |
| **qa-lead-pulse** (4h) | MEDIUM — test/CI status | Test suite regressions, CI failures that block shipping |
| **integration-lead-pulse** (6h) | LOW | MCP server health — relevant if a server an active project depends on is down |

**Priority rule:** Self-healing pulse findings trump all other pulse data. A crash-looping container for `yt-anim-*` directly affects YT Animation project status. Report the infrastructure issue alongside the project status, not as a separate note.

**Do NOT read every pulse's full output** — just grep for the relevant blocks. The digest file is append-only and grows throughout the day. A targeted grep costs <1s.

#### User Absence Streak Detection

**New in v1.11.0:** Beyond checking repo activity, track whether the *user* has been present. All recent git commits might be from subagents/cron jobs — the user may have been absent for days.

Technique: cross-reference three data streams to determine user vs. subagent activity:

```bash
# 1. Session search browse mode — shows all recent sessions WITH source labels.
#    Look for sessions with source="discord" or source="cli" (NOT source="cron").
session_search()  # browse mode — returns by recency, includes "source" field

# 2. Cross-reference session timestamps against git commit timestamps
#    If all commits in the last N days correlate with cron schedules but
#    no user sessions exist, the user is absent
session_search(query="bookends OR construct-manage OR bizdev OR <project>", sort="newest", limit=3)

# 3. Determine "days since last user session" metric
#    browse mode → scan results for sessions with source="discord" or "cli"
#    The most recent such session's last_active timestamp ≈ last user interaction
```

**⚠️ `session_search(query="discord")` does NOT work for absence detection.** FTS5 matches the word "discord" more densely inside loaded skill content than actual conversation messages. Use browse mode instead (step 1 above) which returns sessions with their source labels intact.

**Absence severity levels:**
- **1-3 days**: Normal pause. No flag needed.
- **4-7 days**: Stretch. Flag as "Last user session was [N] days ago." Move focus recommendation to simplest possible action (one commit, one email, one decision).
- **8+ days**: Critical absence. Elevate to pulse headline. The user may be experiencing life circumstances, burnout, or project fatigue. Focus recommendation should be *minimal* — a 5-minute task that rebuilds momentum. Flag that subagents are keeping the lights on.

This complements the repo-level activity scan: a repo may show 0 commits because the user is absent, not because the project is stalled. The distinction matters for the ADHD sprawl check (Phase 9) — the appropriate response to user absence is different from the response to active scope creep.

**P0 repos that also have no git history** (like bookends/) should be flagged for verification — the project may exist only as files on disk or in an unsaved Docker volume, not as a git repo.

Then build an actual-vs-planned table:

```
| Project      | Priority | Activity                  | Gap       |
|--------------|----------|---------------------------|-----------|
| Bookends     | P0       | Silent 3 days             | 🔴 COLD   |
| Model Gateway| P1       | Worked on today           | 🟡 drift  |
| AI-Scientist | unparked | Setup today               | 🟠 sprawl  |
```

The most common pattern: the operator builds infrastructure (MCP servers, agent teams, tooling) instead of shipping P0 products. **Flag each non-P0 project he touched** in the pulse, and ask whether it was worth the diversion.

### Phase 7: Priority Discrepancy Detection

The **monthly-priorities.md** in `hermes-config/roadmap/` is the source of truth, but the standing pulse instructions in the cron job prompt may have different priority rankings. Cross-check them:

1. Read `monthly-priorities.md` — note each project's P-level
2. Compare against the pulse prompt's priority buckets
3. If they disagree (e.g., roadmap says Twitch Farm=P1 but pulse prompt says P2), **flag it** in the pulse as a discrepancy to resolve

**Check roadmap accuracy, not just consistency.** The priorities doc often goes stale between updates. For each project in the roadmap:
- Cross-reference against actual commit logs in the corresponding repo
- If a project's status says "Research phase" but the repo has a working beta pipeline (e.g., YT Animation), flag the discrepancy
- If a project says "In development" but has zero commits in 30+ days, flag it as cold
- The last-updated date at the top of the priorities doc is a rough proxy for staleness
- **Staleness heuristic**: If `last-updated` date at the top of `monthly-priorities.md` is > **7 days** old, flag it in the pulse: \"monthly-priorities.md last updated [N] days ago — priorities may be stale.\" At >14 days, elevate to a stronger flag: \"Roadmap hasn't been touched in [N] days — project statuses are likely inaccurate. Recommend a 10-minute review to reset priorities.\" This is a first-class pulse finding, not a footnote.
- **OS mtime check (more reliable):** The YAML frontmatter `last-updated` date can be manually set and go stale even when the file was actually modified. Use the OS modification timestamp as a ground-truth cross-check:
  ```bash
  # Linux (WSL/MSYS)
  stat -c "%y" ${MY_REPOS}/hermes-config/roadmap/monthly-priorities.md
  
  # Windows cmd/PowerShell
  Get-Item "${MY_REPOS}\Documents\github\hermes-config\roadmap\monthly-priorities.md" | Select LastWriteTime
  ```
  If the OS mtime is newer than the frontmatter date, flag that the priorities have been modified but the date wasn't bumped. If it's older, the roadmap hasn't been touched since that date.

## Common stale entries to look for:

See `references/common-stale-entries.md` for the full checklist of stale patterns across data sources (bookmarks, GitHub stars, YouTube playlists, X/Twitter bookmarks, LinkedIn saves).

## Pitfalls

- ~~**Cron prompts override this skill's git scan with hardcoded repo lists** — FIXED June 17, 2026.~~ All 5 pulse cron prompts (Evening Wrap-Up, Morning Wrap-Up, Live Scan, the operator's 4h Pulse, Weekly Roundup) were rewritten to use the dynamic `for d in ${MY_REPOS}/*/` scan. The root cause was that the old prompts said "check git activity" but didn't specify HOW — the agent defaulted to 3 hardcoded repos. Each prompt now includes the exact bash for loop inline. If new pulse cron jobs are created in the future, replicate the Phase 6 dynamic pattern — never write prompts that just say "check recent commits" without specifying the full dynamic scan.
- **Standalone pulse cron prompts drift from this skill over time** — Any cron job that inlines pulse instructions rather than loading the skill will silently become stale. When you encounter a pulse cron that hardcodes repo lists or intelligence commands, update its prompt to use the dynamic scan patterns from Phase 6. The cross-repo freeze check script path should use the correct absolute Windows path with quotes: `python "${USER_HOME}/AppData/Local/hermes/skills/productivity/intelligence-pulse/scripts/cross_repo_freeze_check.py"` — do NOT use `/c/...` MSYS paths (see MSYS path pitfall in the cross-repo freeze detection section).
- **Python subprocess and git don't resolve MSYS paths on Windows** — Python's `subprocess.run(["git", "-C", "${MY_REPOS}", ...])` fails because native Windows Python doesn't understand MSYS `/e/` paths when passing them as arguments to subprocesses. The `cross_repo_freeze_check.py` now auto-detects this (tries `E:/` first), but any new script calling git via subprocess on this host must use Windows-native paths (`E:/...`), never MSYS paths (`/e/...`). Use `Path.exists()` or `Path.is_dir()` as the discovery method (those DO work with MSYS paths), then convert to `E:/` before passing to subprocess.
- **`git -C` unreliable on MSYS/Windows with repos containing `.git.broken.*` dirs** — The Phase 6 dynamic scan using `git -C` can silently return exit code 128 and produce no output when a repo has both a `.git` directory and a `.git.broken.*` directory (a known git-for-windows edge case after failed migration attempts). The `ghl` repo at `ghl/.git.broken.2026-04-19` is a confirmed example. **Fix:** always use `cd "$d" && git ...` instead of `git -C "$d" ...` in the dynamic repo scan. The `cd` approach is fast, reliable, and avoids the edge case entirely. All three scan patterns in Phase 6 (STEP 0 dynamic scan, P0 Deep Check, fallback inline check) have been updated to use `cd` instead of `git -C`. If you add a new pulse cron prompt, replicate the `cd` pattern — never inline bare `git -C` commands.
- **Rate limits bite on YouTube transcript extraction** — ~400 requests per IP per window. Batch processing must plan for this. Use browser cookie auth as fallback.
- **Firefox profile path changes on update** — Verify `places.sqlite` path before querying. Cache the profile name and validate it weekly.
**⚠️ Firefox Remote Debugging MUST be running for ChatGPT/Grok/bookmarks.** The PIM connectors use WebDriver BiDi on port 9223 (controlled by `PIM_BIDI_PORT` env var). A no_agent watchdog cron (`Firefox Remote Debugging Watchdog`) checks every 15min and auto-starts Firefox if down. If Firefox extraction fails, the root cause is usually session exhaustion (connector auto-restarts Firefox to recover within 30s) rather than a permanent failure. See `references/firefox-remote-debugging-setup.md` under this skill for full setup, including BiDi-only protocol, session exhaustion handling, zombie process fixes, and Grok SPA limitations.
  
  **Timeout escalation (preferred — try first):** Increase the command timeout from 30s to 60s. The Firefox DB lock is often brief (ms-scale), and Firefox releases the lock quickly in practice. In testing, 60s timeout succeeded ~90% of the time when 30s failed.
  ```
  # In terminal(): pass timeout=90 instead of default 30
  cd ${MY_REPOS}/hermes-config && timeout 60 python scripts/intelligence_collector.py check-new
  ```
  **Fallback only when escalation fails:** Use the PIM DB directly — the ingestion pipeline already copies bookmarks into `pim.db` table `saved_items` (source_type='bookmark'). Query it directly instead of relying on Firefox SQLite. See `references/pim-fallback-queries.md`.
- **pim.db might not be ingesting** — The Personal Intelligence MCP must be running for its DB to have fresh data. If the server is down, skip that source and report the gap.
- **GitHub stars DB can be empty** — The ingest scripts may never have been run. Check `SELECT COUNT(*) FROM github_repos` in `gitmcp.db` and report if zero.
- **Don't report the same item twice** — Deduplicate across sources (a YouTube video could also be bookmarked). Use URL hash as the dedup key.
- **Cascading delay trap
- **check-new output mixes log lines with JSON** — The collector prints [INFO] level log entries interleaved with the final JSON payload. When parsing programmatically, extract the JSON from the last `{...}` block rather than treating the full stdout as JSON.
- **BizDev MCP may return empty results for contracts** — If dashboard shows 0 outreach and 0 followups but the user has targets, it is a pipeline stall, not a service issue.
- **Don't skip focus recommendation** — Even if nothing changed, the pulse MUST include a ONE thing to work on next. Without it, the user has no vector for their next action and drifts.
- **YT-DLP cannot access private YouTube playlists** — The `intelligence_collector.py` script uses `yt-dlp` for search playlist extraction ("Watch Later", "Liked Videos", "AI News Search"). For private playlists (Watch Later, Liked Videos), yt-dlp returns `ERROR: [youtube:tab] WL/LL: YouTube said: The playlist does not exist.` regardless of whether Firefox is logged in. These are auth-bound private playlists that yt-dlp cannot access via its own auth mechanism. **Mitigation:** Do not flag 0 videos from Watch Later/Liked Videos as a pipeline stall — it's a known yt-dlp limitation. For those playlists, the PIM ingestion pipeline should use the Firefox BiDi extraction path instead. The `search` playlists (e.g., "AI News Search") generally work because they use public search results. Document this as a "yellow" (low-priority) known limitation — it doesn't block pulse delivery, but the user should know their Watch Later and Liked Videos are not being ingested.
- **Blogwatcher Wired feed generates massive coupon noise
  
  **Two-layer dedup:** 
  1. `youtube_seen_ids` in `last_check.json` prevents re-reporting videos already surfaced in a prior scan.
  2. **Upload-date filtering** via `yt-dlp —print "%(id)s %(upload_date)s"` — only includes videos uploaded within the last 60 days. This prevents the initial flood of old videos when a new playlist gets ingested. 
  
  Without the upload-date filter, a newly-ingested playlist of 400+ old videos (3-5 years old) would all be reported as "new" on the first scan. The `pulse_scan.py` script implements both layers — batches yt-dlp calls (15 URLs per batch) and caches upload dates in `youtube_upload_dates` to avoid re-querying. See `references/youtube-upload-date-filter.md`.
- **PIM DB full_text for Grok/ChatGPT may be raw HTML** — When the connector extracts conversation content, it captures the page DOM before React finishes rendering the actual messages. The `full_text` column in `saved_items` can contain the complete HTML page source (40-100KB of JS bundles, CSS, and markup) instead of clean conversation text. If you need the actual message content, extract it via `document.body.innerText` (not `document.documentElement.outerHTML`) in the BiDi connector's evaluate call, or re-extract from the Grok/ChatGPT web UI directly. The `title` column is generally reliable. See `references/firefox-remote-debugging-setup.md` under the Grok SPA limitations section.
- **Grok SPA direct URL navigation shows "You need access"** — Navigating to `https://grok.com/c/{id}` in a BiDi-controlled headless browser returns "This is a private conversation link" even when the sidebar shows the user is authenticated. This is a Grok React SPA routing quirk, not an auth failure. The GrokConnector works around it by scrolling the sidebar and clicking links rather than navigating directly.
- **Blogwatcher URLs must be included in pulse output** — the operator explicitly asked for blogwatcher article links to be clickable in pulses. The `pulse_scan.py` now includes `url` in every blogwatcher content pick item. When writing the pulse delivery, include the URL so the operator can click through. Never summarize blogwatcher articles without linking to the source.
  
- **Pulse delivery must include source URLs for all picks** — Every content pick (YouTube video, blogwatcher article, PIM item) should include the original URL. the operator needs to click through to decide if something is relevant. Summary-only delivery wastes the pulse.
- **Blogwatcher Wired feed generates massive coupon noise** — The Wired RSS feed (https://www.wired.com/feed/rss) publishes a high volume of coupon/deal/promo-code articles that are *technically* new content but carry zero intelligence value. Observed: 343 unread articles, of which ~330+ were Wired coupons. **Mitigation:** When blogwatcher returns a large batch of [new] articles, check if they're overwhelmingly from Wired and categorized as "Coupons" or "Deals." If so, skip them in the pulse report (mention "N Wired coupon articles filtered" in one line) and focus on real signal from Ars, HN, TechCrunch, Manufacturing Dive. Consider removing the Wired feed if the noise outweighs signal.
- **False freshness after check-new timeout** — `check-new` calls `main()` FIRST (bookmarks → GitHub → email → YT → X subprocess chain), then queries PIM and writes `.last_intelligence_check`. If `main()` times out partway through (e.g., Firefox lock at 30s), the timestamp file is NOT written, BUT the `.last_intelligence_check` from the PREVIOUS run still exists. However, there's a subtler case: if `main()` succeeds slowly (>30s but <120s) and the terminal tool wraps in a 30s timeout, the process gets killed AFTER partial work but the `main_with_action()` exception handler may have partially updated state. **Result:** the next pulse tries `check-new`, finds 0 items because the pipeline hasn't ingested anything since the last successful check timestamp, and reports "0 new items" — a false negative. **Mitigation:** Never rely solely on `check-new` output for pulse delivery. ALWAYS query PIM DB directly for `ingested_at > datetime('now', '-4 hours')` as the primary data source. Only use `check-new` when you need to force a fresh ingestion AND you set `terminal(timeout=120)`.

### Pitfall: Relevance Scoring Bias Against Non-Trump Categories
When building a multi-category monitoring pipeline, be aware that keywords referencing a dominant figure (e.g., Trump) heavily skew scores upward (+0.25 bonus just for the name). Business intelligence categories naturally score lower (0.30-0.60) because they have no name-bonus terms. Use category-specific alert thresholds — business cats at 0.40, Trump/KB cats at 0.60+ — or calibrate against actual scores from a test run rather than an arbitrary number.

### Pitfall: latest.json Overwrite When Running Categories Sequentially
If a monitoring pipeline writes all findings to a single latest.json, running categories one at a time overwrites the file each time. Only the last category's findings survive. Mitigation: run all categories together with a 300s+ timeout, or build aggregation scripts that read from history.jsonl (last 48h) as fallback since it is append-only.

### Pattern: Alert Bridge + Daily Digest Layer
After a file-based monitoring pipeline writes findings to latest.json + history.jsonl, add two no_agent cron scripts on top:

**Alert Bridge** (every 4h, no_agent=true): Read latest + history (48h), filter business cats above threshold, check state file for dedup, print alert if new. Silent when nothing new.

**Daily Digest** (daily 6am, no_agent=true): Read latest + history, dedup against previously-reported fingerprints (state JSON), group by category, format per-category brief with top N items, update state.

State file pattern — small JSON in the findings directory tracking reported fingerprints:
```json
{"reported_fingerprints": ["fp1", ...], "last_delivery": "2026-06-23T..."}
```
Pure data-transformation — no LLM needed, use no_agent=true cron with Python scripts.

### Pitfall: Consistent 0-new-items across ALL sources is a diagnostic signal — When every PIM ingestion round returns 0 across all sources (bookmarks, YouTube, GitHub stars, ChatGPT, Grok, email), it may indicate pipeline failure rather than genuine quiet periods.

  **(1) Check the cron job's last run status first — this is the fastest diagnostic.** Run:
  ```bash
  hermes cron list | grep -i pim -A 10
  ```
  Look for the `Last run` field. If it shows `error:` followed by a message (e.g., `error: Script not found: C:\...` or `error: Script exited with code 127`), that error IS the root cause. Common error patterns:
  - `Script not found` — the cron's script path is broken (e.g., double `scripts/scripts/` nesting, missing file, wrong workdir). Fix the path in the cron definition.
  - `Script exited with code 127` — the script file is missing or the shebang points to a non-existent interpreter. Check the file actually exists at the configured path.
  - `error:` with stderr content — a runtime error in the script itself. Read the stderr to identify the issue.
  - If `Last run` shows `ok` with a timestamp >6h ago, the cron ran without errors but the pipeline is stalled (see step 3).

  **(2) Check `pim.db` directly for recent `ingested_at` timestamps via sqlite3.**
  ```bash
  sqlite3 "${MY_REPOS}/Documents/github/git-mcp/services/personal-intelligence-mcp/pim.db" \
    "SELECT ingested_at FROM saved_items ORDER BY ingested_at DESC LIMIT 3;"
  ```
  If the most recent timestamp is >6h old, nothing has been ingested since then.

  **(3) If `ingested_at` values are >6h old (and step 1 showed `ok`), the pipeline process is running but stalled** — try forcing a fresh scan:
  ```bash
  cd ${MY_REPOS}/hermes-config && python scripts/intelligence_collector.py check-new
  ```
  Pass `terminal(timeout=120)` — the cumulative subprocess chain (Firefox, YouTube, X) needs the extra time.

  **(4) If still dry after all above**, the issue is either stale auth tokens (Firefox session expired, GitHub token rotated), a connectivity/rate-limit problem in the pipeline scripts, or the Firefox BiDi port (9223) is unreachable. Check Firefox with `curl -s http://localhost:9223/json/version | head -5`.

- **Partial pipeline stall: only email shows activity** — A subtler pattern than total silence: `check-new` or PIM DB queries return items ONLY from `source_type='email'` with nothing from bookmarks, YouTube, GitHub stars, ChatGPT, or Grok. This indicates the IMAP email connector is working (it's fast, uses Gmail's API) but the Firefox-dependent connectors (bookmarks, YouTube, ChatGPT, Grok) are silently failing — likely because Firefox Remote Debugging on port 9223 is down or the PIM BiDi session is exhausted. **Action:** Run the Phase 1.25 Firefox Health Check to detect and restart Firefox. Do NOT report this as a quiet period — it's a partial pipeline failure. If Firefox responds but connectors still return empty, the issue is session exhaustion (the BiDi connector auto-restarts Firefox to recover, which can take 30-60s).
- **Cron-heavy session_search returns inflated results** — In cron context, browse mode shows only cron sessions (skill-loaded pulse contexts with ~200KB bookend payloads per session). Broad queries like "working on OR building OR deployed" match skill-internal references and inflate results further. **Mitigation:** 
  - First, check browse mode: if ALL recent sessions are `source: cron`, flag that no user sessions exist and session_search will be noisy
  - Use targeted single-term queries like `query="bookends OR constructManage OR bizdev"` instead of broad verb-based queries
  - Prefer direct data sources (git log, blogwatcher CLI, PIM DB queries) over session_search when in cron context — they're faster and don't trigger the bookend bloat
  - If you must session-search in cron context, pass `sort="newest"` and `limit=2` and read the output file with `read_file` to avoid context bloat

- **User Absence Streak false positive in cron context** — The User Absence Streak Detection (Phase 6 subsection) calls `session_search()` browse mode to find "non-cron" sessions. **In cron context, ALL visible sessions are cron sessions** — the user's Discord/CLI sessions exist in the DB but `session_search()` in a cron-run agent shows only other cron runs because the user's sessions are in different topics/threads. **Result:** every pulse run with the intelligence-pulse skill flags "No user activity in N days" even when the user was in Discord yesterday.

  **Original fix (DO NOT USE — proven broken in production):** `session_search(query="discord", sort="newest", limit=3)` was previously recommended but does NOT work. FTS5 matches the word "discord" more densely inside loaded skill content than inside actual Discord conversation messages. The top results will be cron sessions whose loaded skill text includes "discord" — not the user's Discord sessions. Confirmed in testing: query returned 2 cron sessions while the actual Discord session from June 8 was 3rd or later.

  **Verified fix — use browse mode for source-based detection:**
  ```bash
  session_search()  # browse mode — returns by recency, includes source labels
  ```
  Parse the response for sessions with `"source": "discord"` or `"source": "cli"`. The browse mode returns sessions sorted by last_active (most recent first) regardless of cron/Discord/CLI. Any Discord-source session in the list proves recent user activity. If the most recent user-sourced session is N days old, that's the absence duration.

  **Alternative — check git commits with non-subagent authorship:**
  ```bash
  git log --all --since="7 days ago" --format="%an %as: %s" | grep -iv "hermes\|cron\|subagent\|dependabot\|renovate"
  ```
  If there are human-authored commits, the user has been active even if no Discord sessions match.

  **Fallback — check PIM DB for ingestion timestamps:** If the PIM pipeline ingested fresh bookmarks/stars in the last 24h, the user likely opened Firefox at least (saved bookmarks). The pipeline runs autonomously but bookmark creation is a user action.

## Appendix: Designing Search Coverage Across Monitoring Pipelines

See `references/search-coverage-design.md` for the full framework: domain-category naming principle, audit pattern (Inventory → Categorize → Expand), pipeline expansion checklist, and wildcard category guidance.

Cross-ref: `references/search-coverage-expansion.md` — Full session transcript detailing a real expansion across 7 monitoring pipelines.

## Reference files

- `references/boss-radar-scoring.md` — Boss radar scoring rubric, action tier definitions, and threshold calibration by category group. Apply to ALL pulse deliveries.
- `references/pulse-consolidation-pattern.md` — How to detect and consolidate overlapping cron pulse jobs in the operator's ecosystem.

- `references/source-queries.md` — Exact SQL queries for each data source
- `references/fallback-mcp-intel.md` — Tier 3 MCP fallback when PIM DB is locked by the MCP server: exact tool calls, limitations, data available per tier
- `references/internal-dossier-methodology.md` — How to compile a structured executive dossier on a known entity using only internal knowledge stores (memory, user profile, session history, mempalace, gbrain, past work artifacts). Dossier format template + synthesis principles. Load when the user asks for a "dossier", "executive summary", or deep profile on someone/something already in the system.
- `references/pim-fallback-queries.md` — Direct PIM DB queries when the main script times out (Firefox lock, network issues). Sqlite3 CLI preferred; `python -c` via `terminal()` also confirmed working (June 2026). Covers both approaches with real query examples.
- `references/youtube-upload-date-filter.md` — Upload-date filtering via yt-dlp: batching, caching, cutoff logic
- `references/firefox-remote-debugging-setup.md` — Headless Firefox setup for PIM ingestion: BiDi-only protocol (Firefox 151+), start/stop/watchdog, session exhaustion handling, zombie process recovery, `PIM_BIDI_PORT` env var, Grok SPA content extraction limitation, and ChatGPT extraction notes. Required reading for anyone working with the PIM ingestion pipeline.\n- `references/pulse-cron-prompt-template.md` — Canonical template for pulse cron job prompts. Work-first structure with exact commands inline. Prevents the "vague prompt → shallow scan" failure mode fixed June 17, 2026.\n- `scripts/pulse_intel.py` — Runnable intelligence check script (standalone Python, callable from cron).
- `references/weekly-intelligence-digest.md` — Weekly Intelligence Digest (Sunday) template: data gathering sequence, fixed section structure, section rules, tone, user-context shaping, pitfalls. For the Sunday cron digest deliverable.
- `references/morning-brief-consolidation.md` — Morning Brief Consolidation (7:01 AM ET) cron: inverted digest-first workflow, delivery format, section rules, opening-line rules, [SILENT] conditions, cron-specific pitfalls. Owned by the `quiet-hours-pulse-digest` trigger.
- `scripts/pulse_scan.py` — Fleet pulse scan script at `agent-fleet/teams/social-media/pulse/tooling/pulse_scan.py` (YouTube + blogwatcher + PIM collection with dedup and upload-date filtering).
- `scripts/cross_repo_freeze_check.py` — Multi-repo freeze detection: walks all github repos, groups by last-commit date, flags ≥3 repos frozen on the same date + pre-migration-freeze sub-pattern. Replaces the fragile awk one-liner formerly in Phase 6.

### Weekly Intelligence Digest (Sunday)

See `references/weekly-intelligence-digest.md` for the full Sunday digest template: data gathering sequence (git log → session search → cash-flow briefings → nightly reports → synthesis), fixed section structure, section rules, tone guidance, user-context shaping, and pitfalls.


## Related Skills

- `quiet-hours-pulse-digest` — Quiet hours (00:00-07:00 EST) pulse management: findings save to daily digest instead of delivering separately. Morning Brief at 7:01AM consolidates overnight findings. ALL pulse cron jobs (including this one) are wired to this system.
- `daily-pulsar-summarizer` — End-of-day summarizer that reads the full day's digest, extracts action items, high-importance findings, and improvement opportunities. Saves unseen items to persistent backlog with citations. On-demand via "what did I miss". Complements the Morning Brief from quiet-hours-pulse-digest.

**⚠️ `daily-pulsar-summarizer` gotcha:** The Pulsar's Step 1 (`unseen-backlog.py digest-summary`) is broken — returns empty stdout. When reading a Pulsar output, expect it to skip Step 1 and go straight to the raw digest read. The backlog `add` and `list --unseen-only --priority=critical` commands work correctly.
- `adhd-aware-agent-communication` — Matches the brief, proactive delivery style required here
- `youtube` — For the YouTube playlist extraction workflow
- `github-stars-extraction` — For the GitHub stars ingestion workflow
- `personal-knowledge-ingestion` — For building/understanding the PIM server that powers the knowledge base
- `bizdev-agent` — When a saved item relates to MES/Solumina business development
- `project-inventory` — For the authoritative list of active projects
- `agent-council-architecture` — Multi-agent executive council design and deployment
- `spacebar-hermes-integration` — For connecting Hermes agent profiles to a self-hosted Spacebar/Harmony gateway instead of Discord

## Agent-Fleet Pulse Integration

This skill powers the Social Media Team's **Pulse agent** (analytics & research scout at `agent-fleet/teams/social-media/pulse/`). The fleet-level integration follows a cron-chaining pattern:

### Cron Chain: Collection → Delivery

```
Every 4h   → pulse_scan.py (raw data collection, prev-report context, dedup)
06:00 daily → Morning Wrap-Up (loads last 3 scans, comprehensive morning brief)
18:00 daily → Evening Wrap-Up (aggregates all today's scans, day-in-review)
```

The fleet agent `pulse_scan.py` wraps this skill's infrastructure (PIM DB queries, YouTube transcript mining, blogwatcher taps) into a single command with `--report-type morning|evening|scan` flag. See `references/agent-fleet-pulse.md`.

### Key Technique: Agent Profile Dependency Audit

Agent profile files (SOUL.md, AGENTS.md, SKILLS.md) in the fleet often reference *aspirational* data sources — APIs that aren't configured, tools that aren't installed, integrations that were planned but never wired. **Before trusting any agent's documented capabilities, audit every dependency:**

1. For each data source / API / integration the agent claims, ask: is it LIVE, NOT WIRED, or PLANNED?
2. Mark each source's status in the AGENTS.md data sources table
3. Replace aspirational sources with actual working equivalents
4. If no working equivalent exists, document it honestly — "Not wired" not "Tweepy integration"

**Pulse example (before → after):**
- Claimed: X API via Tweepy, LinkedIn API via linkedin-api → reality: neither configured
- Replaced with: blogwatcher RSS (live), YouTube transcript summaries (402 videos mined), PIM DB (1500+ items), gpt-researcher MCP (live)
- Result: every scan pulls real current data, zero API-key dependencies

Apply this audit to any agent profile in the fleet before deploying or relying on its capabilities.
