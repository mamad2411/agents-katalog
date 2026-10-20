---
name: cisa-kev-data-sourcing
description: Fetch, filter, and report the CISA Known Exploited Vulnerabilities (KEV) catalog — Python urllib.request pattern for reliable cron-based data sourcing
version: 1.0.0
author: Phantom (Cyber Lead)
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [cisa, kev, cve, threat-intel, vulnerability-management]
    triggers: [cisa kev, known exploited vulnerabilities, kev catalog, fetch kev, cve tracking, vulnerability feed]
    related_skills: [cyber-intel-workflow, discord-report-format, osint-threat]
---

# CISA KEV Data Sourcing

Fetch and filter the CISA Known Exploited Vulnerabilities (KEV) catalog for cron-based threat intelligence. This is the authoritative source for vulnerabilities confirmed exploited in the wild.

## Python Fetch Pattern (Preferred)

Use Python's `urllib.request` instead of curl for reliability in cron jobs. No shell quoting issues, no subprocess overhead, no temp files.

### Minimal Fetch

```python
import urllib.request, json

url = "https://cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
data = json.loads(resp.read())

# Sort by dateAdded descending
recent = sorted(
    data.get("vulnerabilities", []),
    key=lambda v: v.get("dateAdded", ""),
    reverse=True
)[:20]

for v in recent:
    print(f"{v['dateAdded']} | {v['cveID']} | {v.get('vulnerabilityName','')[:70]}")
```

### Overnight Freshness Filter

Filter to entries added today or yesterday:

```python
today = "2026-07-30"
yesterday = "2026-07-29"

recent = [
    v for v in data.get("vulnerabilities", [])
    if v.get("dateAdded", "") in (today, yesterday)
]
```

### Full Entry Fields

| Field | Type | Example |
|-------|------|---------|
| `cveID` | string | CVE-2026-20316 |
| `vulnerabilityName` | string | Cisco Secure Firewall Management Center... |
| `dateAdded` | YYYY-MM-DD | 2026-07-29 |
| `dueDate` | YYYY-MM-DD | 2026-08-19 |
| `shortDescription` | string | Full technical description |
| `requiredAction` | string | Apply mitigations per vendor instructions |
| `knownRansomwareCampaignUse` | string | "Known" or "Unknown" |
| `notes` | URL | CISA advisory link |
| `product` | string | Affected product name |
| `vendorProject` | string | Vendor name |
| `cveTags` | list | CWE references |

### Catalog Root Fields

```python
data["title"]           # "CISA Known Exploited Vulnerabilities Catalog"
data["catalogVersion"]  # Incrementing version number
data["dateReleased"]    # Catalog publication date
```

## When To Use

- Cron contexts where curl may be unreliable (MSYS/Git Bash, Windows)
- Overnight freshness sweep when the cyber pipeline is down
- Morning briefing independent verification
- Any automated CVE tracking pipeline

## Full Freshness Sweep (KEV + PoC-in-GitHub + Google News)

For a complete overnight freshness sweep (morning briefing, 9PM-7AM gap), use the standalone script `scripts/cyber_freshness_sweep.py`. It fetches all three reliable sources in one run: CISA KEV JSON (gzip-aware, filtered by `dateAdded` with `dueDate` surfaced), PoC-in-GitHub README (top 40 CVE lines, newest additions at top), and Google News RSS cybersecurity headlines with pubDates.

Run it as a script FILE, not an inline `curl ... && python -c "..."` chain — inline chains can trip Hermes terminal command guards and break on Windows/MSYS quoting. KEV items whose `dueDate` is TODAY or TOMORROW are Tier 1 briefing material regardless of vendor relevance; check local exposure before dismissing.

## Why Not the HTML Page

CISA's HTML page layout changes periodically. The JSON feed at `/sites/default/files/feeds/known_exploited_vulnerabilities.json` is:

- **Structured** — machine-parseable, no layout shifts
- **Complete** — full catalog (1656+ entries as of Jul 2026), not a page excerpt
- **Filterable** — `dateAdded`, `cveID`, `product` are all queryable fields
- **Reliable** — serves consistently from cron contexts, no auth

## curl Fallback

When Python is not available:

```bash
curl -sL -H "User-Agent: Mozilla/5.0" \
  "https://cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json" \
  --max-time 15
```

## Pitfalls

- **No auth required** — CISA does not authenticate this feed. No API key needed.
- **No rate limit** documented. Works reliably from cron on multiple hosts.
- **All times in UTC** — `dateAdded` values are YYYY-MM-DD without timezone. For ET morning briefings (7 AM ET = 11 AM UTC), entries added that day are available.
- **Catalog is additive** — once a CVE is in KEV, it stays. Filter by `dateAdded` to find recent additions; do not use catalog version as a freshness heuristic.
- **~1 KB per entry** — the full catalog is ~1.5 MB as of mid-2026. Fetch and parse in memory is fast (<1s).
- **Over 1600 entries** — always filter by date or CVE ID. Do not dump the full catalog into a report.
- **No CVSS scores in the JSON feed** — only `dateAdded`, `dueDate`, `shortDescription`, `requiredAction`. For CVSS, cross-reference with NVD API.

## Related

- `cyber-intel-workflow` — broader nightly pipeline that consumes KEV data in the morning briefing
- `osint-threat` — threat intelligence skill that can cross-reference KEV with other sources

## Reference Files
- `references/session-precedents.md` — real-world session examples: fetching KEV when the cyber pipeline is fully disabled, findings from July 2026 overnight sweeps
