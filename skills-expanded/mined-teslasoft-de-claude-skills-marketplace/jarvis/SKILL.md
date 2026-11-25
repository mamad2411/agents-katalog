---
name: jarvis
version: 1.4.0
last_updated: 2026-06-05
description: |
  AI assistant layer for the Teslasoft harness. Reads pre-collected state from
  the Drone sidecar, surfaces alerts, answers ad-hoc queries, and provides
  instant dashboard data.
triggers:
  - /jarvis
  - /jarvis status
  - /jarvis alerts
  - /jarvis query
  - /jarvis collect
  - /jarvis health
  - /jarvis dashboard
  - /jarvis monitor
  - /jarvis policies
  - /jarvis reviews
  - /jarvis process
negative_triggers:
  - git operations
  - project creation
  - real-time monitoring
---

# Jarvis

Nikola's AI assistant layer -- reads pre-collected state from the Drone sidecar,
surfaces alerts, answers ad-hoc queries, and provides instant dashboard data.

## When to Use

- Starting a session -- get instant status without manual file reads
- Checking service health, inbox count, or telemetry metrics
- Reviewing and resolving alerts (P0-P3 priority)
- Answering ad-hoc questions about vault state
- Dashboard Phase 1 data collection (SQLite-backed, <500ms)
- Any role needing a quick system status brief

## When NOT to Use

- Creating or modifying projects/goals (use vault templates)
- Git operations (use collab skill)
- Real-time monitoring (use drone TUI directly)
- When drone sidecar is not running (direct tools fallback handles services/inbox/git only)

## Commands

| Command | Description | Roles |
|---------|-------------|-------|
| `/jarvis` | Brief status: services, inbox, branch, alerts | All |
| `/jarvis status` | Same as `/jarvis` | All |
| `/jarvis alerts` | List unresolved alerts by priority | All |
| `/jarvis alerts resolve <id>` | Mark alert resolved | All |
| `/jarvis query <question>` | Ad-hoc question answered from state + Ollama | All |
| `/jarvis collect` | Force immediate collection cycle | All |
| `/jarvis health` | Detailed service health breakdown | All |
| `/jarvis dashboard` | Full state for dashboard rendering (Nikola) | Nikola |
| `/jarvis monitor` | Check sidecar monitoring loop status | Nikola |
| `/jarvis policies` | Policy compliance report from telemetry | Nikola, Architect |
| `/jarvis reviews` | Show pending review queue by role | Reviewer Roles |
| `/jarvis process` | Trigger role-based review processing | Nikola |
| `/jarvis process --dry-run` | Preview processing without modifying files | All |

## Procedure

### For `/jarvis` or `/jarvis status`

1. **Read state file:** `coordination/jarvis/state.json`
   - If file exists AND `collected_at` < 2 minutes ago: use directly
   - If file missing or stale: call `POST http://localhost:3737/jarvis/collect`
   - If drone unreachable: use direct tools fallback (see Fallback section)

2. **Read alerts:** `GET http://localhost:3737/jarvis/alerts` or parse state `alerts` field

3. **Render brief:**
   ```markdown
   ### Jarvis Status

   | Services | Inbox | Branch | Telemetry | Alerts |
   |----------|-------|--------|-----------|--------|
   | [N]/3 up | [N] items | [branch] | [N] events | [summary] |

   > **[P0/P1 alerts shown here if any]**
   ```

### For `/jarvis alerts`

1. Fetch: `GET http://localhost:3737/jarvis/alerts`
2. If drone down: query SQLite `alerts` table via `getUnresolvedAlerts()`, or use cached state.json `alerts` field
3. Render table sorted by priority (P0 first):

   ```markdown
   | ID | Priority | Message | Suggested Fix | Age |
   |----|----------|---------|---------------|-----|
   ```

4. Offer resolution actions via AskUserQuestion

### For `/jarvis alerts resolve <id>`

1. Call: `POST http://localhost:3737/jarvis/alerts/<id>/resolve`
2. Confirm resolution to user

### For `/jarvis query <question>`

1. Read `coordination/jarvis/state.json` for context
2. If answer is in state data: respond directly from JSON (no Ollama needed)
3. If answer needs analysis: call drone's query endpoint
   `POST http://localhost:3737/jarvis/query` with `{ "question": "<question>" }`
4. If drone down: answer from state.json best-effort, note limitations

### For `/jarvis collect`

1. Call: `POST http://localhost:3737/jarvis/collect`
2. Wait for response (typically <1s with SQLite extraction)
3. Render updated status brief

### For `/jarvis health`

1. Read state `services` field
2. For each service, show detailed info:
   - Drone: status, commit_organizer config, buffer size
   - RC Watcher: status, port check
   - Plugin: status, build info

### For `/jarvis dashboard` (Nikola only)

1. Read `coordination/jarvis/state.json`
2. Return full state object for dashboard rendering
3. Dashboard skill handles schema mapping and UI rendering
4. See references/state-schema.md for field documentation

### For `/jarvis monitor`

1. Call: `GET http://localhost:3737/jarvis/monitor`
2. Show: running status, interval, last collection time, collection duration

### For `/jarvis policies` (Nikola, Architect)

1. Read state `telemetry.policy_warnings` field
2. Show policy violation summary:
   - Warning count by policy_id
   - POLICY_BLOCK events (from telemetry event_counts)
   - Error rate

### For `/jarvis reviews`

1. Read `coordination/jarvis/state.json` → `review_queue.files`
2. Import `review-router.js` → `routeReview()` to filter by current role
3. Show pending files routed to the requesting role:
   ```markdown
   ### Pending Reviews (doc-specialist)

   | File | Action | Status |
   |------|--------|--------|
   | .claude/skills/foo/SKILL.md | SDL compliance | pending |
   ```

### For `/jarvis process`

1. Call: `POST http://localhost:3737/jarvis/reviews/process`
   - Body: `{ "dry_run": false }` (or `true` for `--dry-run`)
2. Response shape:
   ```json
   {
     "processed": 3,
     "auto_approved": 1,
     "role_reviewed": 1,
     "escalated": 1,
     "errors": 0,
     "files": [{ "path": "...", "gate": "...", "status": "...", "role": "..." }]
   }
   ```
3. Render summary table with gate and role assignments

### Review Routing Rules

| Pattern | Target Role | Review Action |
|---------|-------------|---------------|
| `.claude/skills/**/*.md` | doc-specialist | SDL compliance, frontmatter validation |
| `.claude/plugins/**/*.md` | developer | Manifest check, plugin structure validation |
| `**/.prompts/*.prompt.md` | planner | Paradigm check, variable validation |
| `10_Goals/G-*.md` | nikola | KR links, horizon verification |
| `20_Projects/P*.md` | nikola | Goal link, status accuracy |

### Auto-Approve Gates

Changes classified into three gate levels by `classifyChange()`:

| Gate | Condition | Action |
|------|-----------|--------|
| **auto-approve** | Whitespace-only, frontmatter-only, empty diff | `review_status: approved` (no role involvement) |
| **role-review** | Content changes, new files (conservative default) | Route to target role, `review_status: reviewed` |
| **escalate** | File deletions, new goals/projects | `review_status: needs-attention` + alert event |

### Frontmatter Review Schema

Jarvis manages review metadata as YAML frontmatter on changed documents:

```yaml
review_status: pending | reviewed | approved | needs-attention
review_notes: "Latest observation from reviewing role"
reviewed_by: doc-specialist    # Role that last reviewed
reviewed_at: 2026-02-08T12:00:00Z
review_history:
  - date: 2026-02-08T12:00:00Z
    role: doc-specialist
    status: reviewed
    note: "SDL compliance verified"
```

### Review Queue in state.json

The collector scans frontmatter across watched paths and aggregates into `review_queue`:

```json
{
  "review_queue": {
    "pending": 3,
    "reviewed": 5,
    "approved": 12,
    "needs_attention": 1,
    "total_tracked": 21,
    "files": [
      { "path": ".claude/skills/foo/SKILL.md", "review_status": "pending" }
    ]
  }
}
```

### Extended State (P37)

The collector now includes extended git state and PARA frontmatter index:

**New state.json fields:**
- `git_extended` — Complete git status: branch, tracking, ahead/behind, staged/unstaged/untracked files, recent commits, submodules, stash
- `para_index` — PARA note index summary: total notes, frontmatter coverage, last indexed timestamp

**New HTTP endpoints:**
- `GET /jarvis/para-index` — Full PARA index JSON
- `POST /jarvis/index-para` — Trigger immediate PARA re-index
- `POST /jarvis/enrich-para` — Trigger Ollama-powered enrichment cycle

**New pnpm scripts:**
- `pnpm jarvis:collect-git` — Run git-collector standalone
- `pnpm jarvis:index-para` — Run PARA indexer standalone

**New alert rules:**
- `git_extended_errors` (P2) — Git collection errors detected
- `para_index_stale` (P2) — PARA index older than 15 minutes
- `para_coverage_low` (P2) — Frontmatter coverage below 30%

**PARA Indexer** runs on a separate 5-minute timer (`PARA_INDEX_INTERVAL_MS`), independent of the 60s collection cycle. Scans all 7 PARA folders (10_Goals through 70_Skills), extracts YAML frontmatter, normalizes fields, and writes `coordination/jarvis/para-index.json`.

**PARA Enricher** runs after indexing, using Ollama to generate note summaries, suggest missing frontmatter fields, and detect broken wikilinks.

### Deprecation Note

The original `/release-cycle` inbox-based review workflow (P19/P28) is **deprecated** as of P32 Phase 5. Use `/jarvis reviews` and `/jarvis process` instead. The RC Watcher file-watcher.ts now only posts events to Jarvis and updates frontmatter — inbox generation has been removed. Discord webhook notifications were decoupled from RC; future integration planned as a Jarvis webhook notifier for P1+ alerts (`DISCORD_WEBHOOK_URL` env var).

## Fallback Strategy

When the drone sidecar is unreachable:

```
1. Try: Read coordination/jarvis/state.json
   → If exists and < 5 min old: use (mark as "cached")
   → If exists and > 5 min old: use with warning "stale data"
   → Note: state.json now includes full telemetry/thread/agent data
     from SQLite, so cached data is comprehensive

2. Try: Direct tools fallback (no drone)
   → Services: curl health endpoints directly
   → Inbox: Glob 00_Inbox/**/*.md, count results
   → Git: Bash git branch + git status
   → Telemetry: NOT AVAILABLE (requires drone + SQLite)
   → Threads: NOT AVAILABLE (requires drone + SQLite)
   → Agents: NOT AVAILABLE (requires drone + SQLite)

3. Render with limitations noted:
   "Drone offline -- showing direct checks only.
    Telemetry, thread, and agent data unavailable."
```

## Alert Priorities

| Priority | Action | Behavior |
|----------|--------|----------|
| **P0** | ESCALATE | Show immediately. Cannot be ignored. |
| **P1** | ACT | Propose fix on next status check. |
| **P2** | NOTIFY | Badge count only. No interruption. |
| **P3** | LOG | Silent. Visible in `/jarvis alerts` only. |

Escalation: P3 -> P2 (30 min) -> P1 (1 hour). P1 never auto-promotes to P0.

### Merge Gate Events

Git hooks (`coordination/git-hooks/`) emit events to Jarvis during merge workflows:

| Event | Source | Trigger | Priority |
|-------|--------|---------|----------|
| `MERGE_GATE_PASS` | pre-merge-commit | Tests pass at target tier | P3 (log) |
| `MERGE_GATE_FAIL` | pre-merge-commit | Tests fail (merge blocked) | P1 (act) |
| `POST_MERGE_REDEPLOY` | post-merge | Build + restart completed on protected branch | P3 (log), P2 if status=WARN |
| `POST_MERGE_BUILD_FAIL` | post-merge | `pnpm build` failed after merge | P2 (notify) |

**3-Tier Merge Gate (MRG-001):**
- **Tier 3** (master/main): Runs `pnpm test:all`
- **Tier 2** (project/*): Runs project-specific tests from P*.md frontmatter
- **Tier 1** (other): Runs branch-level tests from P*.md frontmatter

**Protected branches** (post-merge auto-rebuild): master, main, development.
Fast-forward merges skip hooks entirely — use `pnpm redeploy` manually.

## Error Handling

| Failure | Fallback |
|---------|----------|
| Drone unreachable | Use cached state.json (now has full data), then direct tools |
| state.json missing | Force collect, or direct tools |
| state.json malformed | Direct tools fallback |
| SQLite unavailable | Ollama extraction (legacy), or nulls for telemetry/threads/agents |
| Ollama unavailable | No impact on collection (SQLite handles all extraction); only `/jarvis query` degraded |
| Alert endpoint fails | Query SQLite `alerts` table directly, or use cached state.json `alerts` field |
| Query endpoint fails | Answer from state.json best-effort |

## MCP Integration

Jarvis data is accessible through **two interfaces**:

1. **HTTP API** (primary): `curl http://localhost:3737/jarvis/*` endpoints — used by dashboard skill and Claude Code sessions
2. **MCP Tools** (read-only alternative): `jarvis_status`, `jarvis_alerts`, `jarvis_collect`, `jarvis_health` — provides vault-safe read-only access without HTTP dependencies

The Vault MCP Server exposes Jarvis state via MCP tools, enabling Cowork sessions (Claude Desktop in Hyper-V) to read Jarvis data without direct filesystem or HTTP access. All write operations (alert resolution, review processing) still require the HTTP API. MCP tools are read-only and provide a subset of HTTP functionality optimized for status checks and briefings.

**Note:** The Jarvis collector runs inside the Drone sidecar and uses direct `database.js` function imports (not HTTP self-fetch) to avoid event loop contention. See "Extraction Strategy" section for details.

## Architecture

### Data Flow

```
  state.jsonl ─→ StateWatcher ─→ SQLite (telemetry.db)
                                      │
                                      ▼
                             JarvisCollector.collect()
                              ┌───────┴───────┐
                              │               │
                    Step 1: Direct      Step 2: SQLite
                    ─────────────       ──────────────
                    _checkDrone()       _extractTelemetryFromDb()
                    _checkRcWatcher()   _extractThreadsFromDb()
                    _checkPlugin()      _extractAgentsFromDb()
                    _collectInbox()         │
                    _collectGit()           │ uses database.js
                              │             │ exports directly
                              └──────┬──────┘
                                     ▼
                              state.json ─→ AlertEngine ─→ SQLite (telemetry.db)
                                     │
                                     ▼
                              Dashboard / HTTP API
```

### Extraction Strategy: Direct Imports vs Drone HTTP API

The collector runs **in-process** inside the drone (as a sidecar). It uses direct
`database.js` function imports rather than the drone's HTTP API endpoints for three reasons:

1. **No self-fetch deadlock.** HTTP self-fetch (`fetch('http://localhost:3737/...')`)
   causes event loop contention when the caller and server share the same Node.js
   process. This was a known bug that led to the `healthCheck` injection pattern.
   Direct function calls avoid the network layer entirely.

2. **Different data sources.** The drone HTTP endpoints serve different stores:
   - `GET /agents` reads from `AgentRegistry` (in-memory, ephemeral)
   - `GET /threads` reads from `thread-queue.json` (file-based, legacy)
   - SQLite `agents` and `thread_queue` tables are the persistent, migrated versions

3. **No serialization overhead.** Direct calls return JS objects. HTTP would serialize
   to JSON, send over TCP loopback, then deserialize -- adding ~10ms per call for
   data that's already in the same V8 heap.

### Extraction Performance

| Source | Method | Latency |
|--------|--------|---------|
| Telemetry | `getRecentEvents(200)` + `getEventsByType()` + `getTotalEventCount()` | ~5ms |
| Threads | `getQueueState()` + `getCompletedToday()` | ~2ms |
| Agents | `getAllAgents()` | ~1ms |
| **Total extraction** | **3 synchronous SQLite calls** | **<10ms** |

> **Note:** `getTotalEventCount()` (added Session 30) returns the true total via
> `SELECT COUNT(*) FROM events`, replacing the previous window-capped count.

Compare: previous Ollama extraction was ~26s (3 sequential LLM calls at ~8s each).

### Ollama Role After Migration

Ollama is demoted to **query-only**. It is no longer used for data extraction during
`collect()`. The only remaining Ollama integration is:

- `POST /jarvis/query` -- ad-hoc natural language questions answered by the LLM
  using `state.json` as context. This is the correct use case for an LLM (reasoning
  over structured data) vs the old pattern (structured data extraction from text).

### Legacy Fallback

The old Ollama extraction methods (`_extractTelemetry`, `_extractThreads`,
`_extractAgents`) are retained as a fallback for edge cases where the SQLite database
is not available (e.g., standalone testing without `initDatabase()`). In normal drone
operation, the database is always initialized before the collector starts.

## Security

- **Read-only by default** -- Jarvis reads state, never modifies vault content
- **Alert resolution** is the only write action (marks alerts resolved)
- **No secrets exposed** -- state.json contains no credentials or absolute paths
- **Role-restricted commands** -- `/jarvis dashboard`, `/jarvis monitor`, `/jarvis policies` are Nikola/Architect only

## References

- [Commands Reference](references/commands.md) -- Detailed command documentation
- [State Schema](references/state-schema.md) -- state.json field documentation

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.4.0
last_updated: "2026-02-07"
source: "[[docs/plans/2026-02-07-jarvis-agent-design.md]]"
migration: "[[docs/plans/2026-02-07-jarvis-sqlite-migration.md]]"
change_surface: references/ (command updates, schema changes)
extension_points: references/commands.md (new commands)
```
