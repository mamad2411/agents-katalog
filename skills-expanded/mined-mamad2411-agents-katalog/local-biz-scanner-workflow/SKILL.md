---
name: local-biz-scanner-workflow
description: Workflow for local-biz-scanner — setting up, running scans, connecting to Hermes, and interpreting results
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [local-biz, security-scanning, vulnerability-assessment, mcp]
    triggers: ["local biz scanner", "scan local businesses", "pos scanning", "vulnerability scanning pipeline", "local business vulnerability"]
    related_skills: [web-application-security-assessment, osint-recon, ai-security-practice-builder]
---

# Local Biz Scanner Workflow

**Umbrella:** `ai-security-practice-builder` — the scanning pipeline is one component of the broader security consulting practice.

## Repo
- **Location:** `${USER_HOME}\Documents\local-biz-scanner\`
- **Remote:** `https://github.com/pmb2/local-biz-scanner` **(private)**
- **Status:** Built, installed, pushed, MCP server confirmed working (8 tools registered on FastMCP 3.3.1)
- **Stack:** Python 3.11+, FastMCP 3.3.1, httpx, SQLite

## Verified Working
- Breach monitor returns real HIBP data (11 findings including 7-Eleven with 185k accounts, Abrigo with 711k)
- All 8 MCP tools register and respond via stdio transport
- Pipeline runs end-to-end: scan → AI analysis → store → dashboard

## Architecture
8 MCP tools exposed via FastMCP:
1. `scan_local_businesses(city, state, scan_type)` — network + breach scanning
2. `scan_website(url)` — single site vuln scan
3. `scan_pos_systems(city, state)` — POS/payment system detection
4. `get_recent_findings(severity, category, city, hours_back)` — query DB
5. `get_finding_detail(finding_id)` — full detail on one finding
6. `get_dashboard_data()` — aggregated stats
7. `check_recent_breaches(days_back)` — CVE + HIBP check
8. `run_full_pipeline(city, state, scan_websites, website_targets)` — everything

## Connecting to Hermes
Add to `config.yaml`:
```yaml
mcp_servers:
  local-biz-scanner:
    command: python
    args: ["-m", "src.main"]
    cwd: "C:\\Users\\<you>\\Documents\\local-biz-scanner"
```

## Alternative: Proximity Scanner (Free, No API Keys)

A complementary discovery method using OpenStreetMap APIs instead of Shodan:

- **Location:** `${USER_HOME}\Documents\github\land-agent\scripts\proximity_scan.py`
- **Data source:** OpenStreetMap Nominatim (geocoding) + Overpass API (business discovery) — both free, no keys
- **Vuln checks:** DNS, HTTP/HTTPS, SSL cert, WP login detection, DMARC/SPF — all passive (Phase 1)
- **Chain filtering:** ~60 chain names auto-skipped + corporate domain blocklist
- **Website opportunities:** Flags no-website businesses for website-landlord auto-generation

**Usage:**
```bash
python ${USER_HOME}/Documents/github/land-agent/scripts/proximity_scan.py --location "your city, NY" --radius 5000 --niches "general" --export-csv
```

Also see the `compliance-first-recon-outreach` skill for the full proximity scanning workflow, gatekeeper scripts, and AI threat pitch.

## Running Scans
- CLI: `python -m src.scripts.run_pipeline --city Schenectady --state NY`
- MCP: Call any of the 8 tools above
- Cron: `0 */8 * * *` schedule via Hermes cron or script

## Current Findings
The breach monitor is pulling real data from Have I Been Pwned. Shodan scanning requires an API key in `.env`. Without Shodan, website and breach scanning still work.

## Key Files
- `src/scanners/shodan_scanner.py` — Shodan network scanning with dangerous service definitions
- `src/scanners/website_scanner.py` — SSL, headers, CMS, sensitive file checks
- `src/scanners/breach_monitor.py` — CVE/NVD + Have I Been Pwned
- `src/mcp/tools.py` — all MCP tool implementations
- `src/mcp/__init__.py` — FastMCP server setup
- `src/scripts/run_pipeline.py` — cron-ready pipeline runner
- `src/database.py` — SQLite storage
- `HERMES_INTEGRATION.md` — full integration guide in repo
