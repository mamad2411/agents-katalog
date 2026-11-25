---
name: foss-mapping
version: 1.0.0
author: Hermes Agent
license: MIT
description: FOSS tool discovery and auto-implementation from PIM.
metadata:
  hermes:
    tags: [foss, mapping, open-source, correlation, catalog, implementation, pim, self-enhancing]
    triggers: [foss-mapping, open-source-discovery, tool-correlation, catalog-update, auto-implement]
    related_skills: [pim-ingestion-pipeline, the planning repo-architecture]
---

# FOSS Mapping Engine

Finds open-source alternatives to everything mentioned in the operator's PIM (YouTube, GitHub stars, bookmarks, emails, Grok chats, etc.) and auto-implements them.

## Architecture

```
PIM DB (5K items) → FOSS Mapping Engine → Enhancement Registry DB
                    ↓
              Cross-Source Correlation Engine (TF-IDF + DBSCAN)
                    ↓
              FOSS Catalog (222 tools, 12 categories)
                    ↓
              Implementation Agent (clone, deploy, verify)
```

## Components

### FOSS Mapping Engine
`_project/scripts/foss_mapping_engine.py` — 508 lines, runs as Phase 1 of self-enhancing loop.

**Workflow:**
1. Scan PIM with pagination (50 items/page, processes ALL items in lookback window)
2. Run cross-source correlation first
3. Update FOSS catalog from GitHub trending
4. For each item: extract tool mentions (regex + GitHub repo patterns)
5. Classify match: Tier 0 (GitHub star → auto-clone), Tier 1 (auto-implement), Tier 2 (review), Tier 3 (log)
6. Auto-implement Tier 0 + Tier 1 (max 5/cycle, rollback on failure)
7. Run implementation agent

**Key functions:**
- `scan_pim_sources(since_hours, limit, offset)` — paginated PIM query
- `count_pim_sources(since_hours)` — total count for pagination
- `extract_mentions(text)` — regex for GitHub repo + pip/npm/docker commands
- `classify_action(item, text)` — tier classification
- `auto_implement_tool(tool, item)` — clone + install + verify + register
- `run_foss_mapping(since_hours, dry_run)` — full cycle

### Cross-Source Correlation Engine
`_project/scripts/correlation_engine.py` — 476 lines.

**Method:** TF-IDF vectorization → cosine similarity → DBSCAN clustering on PIM items.

**Config:**
- `LOOKBACK_DAYS = 90` (fetch 90 days of PIM items)
- `MIN_CLUSTER_SIZE = 2` (minimum items per cluster)
- `SIMILARITY_THRESHOLD = 0.3` (DBSCAN eps — tune for cross-source)
- `MAX_ITEMS = 5000` (cap for memory safety)

**Results:** 58 clusters found, 3 cross-source (github_star + bookmark). Clusters stored in `enhancement_registry.db` `correlation_clusters` table.

**CLI:**
```bash
python scripts/correlation_engine.py --days 90              # Run full correlation
python scripts/correlation_engine.py --days 90 --json       # JSON output
python scripts/correlation_engine.py --summary              # Show unprocessed clusters
python scripts/correlation_engine.py --cluster-items <id>   # Show items in a cluster
```

### FOSS Catalog
`_project/data/foss_catalog.json` — 222 tools across 12 categories: ai, devops, security, media, data, devtools, comms, business, oss, web, crypto, iot.

**Auto-Update:** `_project/scripts/catalog_updater.py` fetches GitHub trending repos (daily/weekly/monthly) across 6 languages (python, javascript, typescript, go, rust, all). Auto-categorizes by repo name/keywords. Adds up to 20 new tools per cycle.

### Autonomous FOSS Implementation Agent
`_project/scripts/implementation_agent.py` — 420 lines.

**Full lifecycle:**
1. `analyze_repo()` — detects docker-compose, Dockerfile, package.json, Makefile, config files
2. `deploy_via_docker()` — docker compose up -d on detected compose files
3. `deploy_via_docker_build()` — docker build + run for Dockerfile-only repos
4. `smoke_test()` — HTTP health check on deployed port (GET /, status < 500)
5. `rollback()` — docker compose down on failure
6. `deployments` table in registry for tracking

**Port conflict detection:** `check_port_available()` before deployment. `find_ports_in_use()` via `netstat -an`.

## Enhancement Registry DB Schema

`_project/data/enhancement_registry.db` — SQLite database with tables:

```sql
-- Core loop tracking
CREATE TABLE loop_runs (run_id, started_at, completed_at, status, items_scanned, ...);

-- Correlation clusters
CREATE TABLE correlation_clusters (
    cluster_id TEXT PRIMARY KEY, topic_keywords TEXT, item_count INTEGER,
    source_types TEXT, source_count INTEGER, top_source TEXT,
    top_items TEXT, created_at TEXT, processed BOOLEAN DEFAULT 0
);

-- Cluster items
CREATE TABLE correlation_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT, cluster_id TEXT NOT NULL,
    pim_item_id INTEGER NOT NULL, source_type TEXT NOT NULL,
    title TEXT, source_url TEXT, llm_summary TEXT, tags TEXT
);

-- Cloned repos
CREATE TABLE cloned_repos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, repo_url TEXT UNIQUE,
    repo_name TEXT, target_path TEXT, file_count INTEGER DEFAULT 0,
    readme_refs TEXT, cloned_at TEXT, last_verified TEXT, verified_count INTEGER DEFAULT 1
);

-- Deployments
CREATE TABLE deployments (
    id INTEGER PRIMARY KEY AUTOINCREMENT, tool_name TEXT NOT NULL,
    repo_url TEXT NOT NULL, deploy_method TEXT, target_dir TEXT,
    port INTEGER, deployed_at TEXT, last_verified TEXT, status TEXT,
    health_check_url TEXT, smoke_test_passed INTEGER DEFAULT 0
);
```

## GitHub Star Auto-Clone Verification

When a GitHub star is detected in PIM (903 items), the FOSS mapper:
1. Extracts repo URL from `source_url` field
2. Clones to `${MY_REPOS}\Documents\github\<repo-name>`
3. Verifies clone has content (file count > 5)
4. Scans README.md for additional FOSS tool references (github.com/owner/repo patterns)
5. Registers in `cloned_repos` table with file count, README refs, and timestamp
6. README refs feed back into the FOSS catalog discovery loop

## Pitfalls

### Pagination (2026-08-10 fix)
All PIM queries must use LIMIT + OFFSET. Without OFFSET, only the first 50 items are ever processed.
- `scan_pim_sources()` always passes `offset` parameter
- `discover_new_items()` always passes `offset` parameter
- Main loop: `while offset < total_items: scan_pim_sources(offset=offset); offset += page_size`

### DB Paths
REGISTRY_DB must be `enhancement_registry.db` (underscore, NOT hyphen). Both `correlation_engine.py` and `foss_mapping_engine.py` must use the same path.

### Cross-Source Clusters
TF-IDF + DBSCAN clustering works best when items have rich text content. Items with only `llm_summary` + `full_text` > 50 chars are included. Items with `full_text` < 50 chars are excluded (noise). To get more cross-source clusters, increase `LOOKBACK_DAYS` or decrease `SIMILARITY_THRESHOLD`.

### Implementation Agent Port Conflicts
The implementation agent checks `find_ports_in_use()` via `netstat -an` before deploying. However, `netstat -an` is slow on Windows. If the agent times out, increase the timeout or check ports manually before running.