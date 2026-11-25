---
name: recon-archive-urls
description: Historical URL collection from web archives (Wayback Machine, Common Crawl, Google Cache) with scope triage — discover hidden endpoints, retired API versions, forgotten admin panels, exposed dev/staging environments, and parameterized URLs through passive archive enumeration. Zero direct contact with target; all collection from third-party archive services.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [url-list, redacted-evidence, hypothesis-queue]
---

# Archive URL reconnaissance — historical endpoint discovery

Use this skill to discover URLs historically associated with the target domain through public web archives. Archive services (Wayback Machine, Common Crawl, Google Cache) have crawled and indexed the target's web presence over time — this passive data reveals endpoints, parameters, retired API versions, forgotten admin panels, dev/staging deployments, and sensitive files that may no longer be linked from the live site but may still be accessible. This is fully passive: no requests are sent to the target. All data comes from third-party archive APIs.

## Required inputs

- Target domain or scope-owned seed URLs.
- Scope file with in-scope and out-of-scope host patterns to validate discovered URLs.
- Rate limits for archive API calls (typically 1-2 requests per second to avoid throttling).
- Evidence goal: URL inventory, parameter extraction, high-value endpoint flagging, and handoff to enumeration or validation skills.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` to load domain and URL-scope rules for filtering results.
3. `pentest_agent_validate_target` to classify each discovered host as in-scope or out-of-scope before further investigation.
4. `pentest_agent_check_authorization` not required for passive archive collection (no target contact), but required before any active validation of discovered URLs.
5. `pentest_agent_build_command` for preview of any tool used to download archive data.
6. `pentest_agent_append_evidence` with source attribution and confidence.

## Workflow

### Phase 1 — Wayback Machine collection

Query the Internet Archive's Wayback Machine CDX API for all captured URLs under the target domain. This is the primary archive source and covers 25+ years of web history.

1. Fetch the complete URL index:
   - `curl -s "https://web.archive.org/cdx/search/cdx?url=*.TARGET.COM&output=text&fl=original,timestamp,statuscode,mimetype&filter=statuscode:200&collapse=urlkey" > wayback_urls.txt`
   - Parameters: `url=*.TARGET.COM` matches all subdomains. `filter=statuscode:200` keeps only successfully fetched snapshots. `collapse=urlkey` deduplicates by normalized URL (removes repeated captures of the same URL).
2. Alternative: use `waybackurls` tool (Go):
   - `waybackurls TARGET.COM > wayback_urls.txt`
   - Handles pagination and rate-limiting automatically.
3. Alternative: use `gau` (Get All URLs):
   - `gau --subs TARGET.COM > wayback_urls.txt`
   - Also queries Common Crawl and URLScan in addition to Wayback.
4. Count and categorize:
   - Total unique URLs: `wc -l wayback_urls.txt`
   - Subdomain distribution: `awk -F/ '{print $3}' wayback_urls.txt | sort | uniq -c | sort -rn | head -20`
   - Path distribution: `awk -F/ '{print $4}' wayback_urls.txt | sort | uniq -c | sort -rn | head -20`

### Phase 2 — Common Crawl and additional archive sources

1. Common Crawl (monthly web crawl snapshots):
   - Query the Common Crawl Index API: `curl -s "https://index.commoncrawl.org/CC-MAIN-2024-10-index?url=*.TARGET.COM&output=json" | jq -r '.url' | sort -u > cc_urls.txt`
   - Iterate over multiple crawl indices (named by year and crawl number, e.g., `CC-MAIN-2024-33`). Use 2-3 recent indices for coverage.
2. URLScan.io (if API key available):
   - `curl -s "https://urlscan.io/api/v1/search/?q=domain:TARGET.COM" | jq '.results[] | {url: .task.url, screenshot: .task.screenshotURL}' > urlscan_results.json`
3. Google Cache (opportunistic, unreliable):
   - Check if Google has a cached version of known URLs: `curl -s "https://webcache.googleusercontent.com/search?q=cache:TARGET.COM" | head -50`
4. Merge all archive sources and deduplicate:
   - `cat wayback_urls.txt cc_urls.txt | sort -u > all_archive_urls.txt`
   - Record source counts for evidence: how many URLs came from Wayback vs Common Crawl vs other sources.

### Phase 3 — URL categorization and parameter extraction

Transform the flat URL list into actionable intelligence by categorizing endpoints and extracting parameters.

1. Categorize by path pattern:
   - Admin and internal panels: `grep -iE "admin|dashboard|manage|console|panel|internal|staff" all_archive_urls.txt > category_admin.txt`
   - API endpoints: `grep -iE "/api/|/v[0-9]/|/graphql|/rest/|/soap/|/ws/" all_archive_urls.txt > category_api.txt`
   - Dev/Staging/Test environments: `grep -iE "dev\.|staging\.|test\.|uat\.|demo\.|sandbox\.|preview\." all_archive_urls.txt > category_dev.txt`
   - Authentication pages: `grep -iE "login|signin|auth|register|signup|reset|password" all_archive_urls.txt > category_auth.txt`
   - File upload endpoints: `grep -iE "upload|import|attach|file" all_archive_urls.txt > category_upload.txt`
   - Configuration files: `grep -iE "\.env$|\.conf$|\.ini$|\.config$|\.yaml$|\.json$|web\.config$|\.htaccess$" all_archive_urls.txt > category_config.txt`
   - Backup and archive files: `grep -iE "\.bak$|\.backup$|\.sql$|\.tar$|\.gz$|\.zip$|\.old$|\.save$|\.swp$" all_archive_urls.txt > category_backup.txt`
   - Debug and error pages: `grep -iE "debug|trace|phpinfo|test\.php|info\.php|error|stacktrace" all_archive_urls.txt > category_debug.txt`
2. Extract URLs with parameters (potential injection points):
   - `grep '?' all_archive_urls.txt | sort -u > param_urls.txt`
   - Extract unique parameter names: `grep -oP '(?<=\?|&)[a-zA-Z0-9_]+(?==)' param_urls.txt | sort | uniq -c | sort -rn | head -50 > params_inventory.txt`
   - Categorize parameters by likely vulnerability class:
     - `grep -iE "(url|redirect|next|goto|return|target|dest|redir)=" param_urls.txt > params_redirect.txt`
     - `grep -iE "(q|query|search|s|keyword|find)=" param_urls.txt > params_search.txt`
     - `grep -iE "(id|uid|user|account|profile|order|product|page_id)=" param_urls.txt > params_id.txt`
     - `grep -iE "(file|path|dir|template|include|require|load|read|document)=" param_urls.txt > params_file.txt`
     - `grep -iE "(url|src|dest|fetch|link|proxy|host|image)=" param_urls.txt > params_ssrf.txt`
3. Extract JavaScript files for JS analysis handoff:
   - `grep -iE '\.js(\?|$)' all_archive_urls.txt | sort -u > js_urls.txt`

### Phase 4 — scope validation and result triage

Apply scope rules to every discovered URL before handing off to active skills. Archive data is noisy — many discovered URLs may be out of scope (third-party CDNs, analytics domains, partner sites, or subdomains explicitly excluded).

1. Normalize all hostnames: extract the domain from each URL, strip `www.` prefix, convert to lowercase.
2. Match against scope file:
   - In-scope: hostname matches an in-scope pattern (exact, wildcard, or subdomain). Flag as `IN_SCOPE`.
   - Out-of-scope: hostname matches an out-of-scope pattern or is clearly third-party (e.g., `google.com`, `cloudflare.com`, `amazonaws.com` unless the target uses these for their own infrastructure and scope includes them). Flag as `OUT_OF_SCOPE`.
   - Unknown: hostname does not match any scope rule. Flag as `UNKNOWN` and do not proceed to active validation without manual scope clarification.
3. For `OUT_OF_SCOPE` URLs: record the count and a sample in evidence for documentation, then exclude from further processing.
4. For `IN_SCOPE` URLs: prioritize by risk/interest:
   - **Priority 1**: admin panels, .env/config file exposures, backup files, debug endpoints.
   - **Priority 2**: API endpoints with parameters, authentication pages with redirect parameters, file upload endpoints.
   - **Priority 3**: static assets, images, CSS, benign informational pages.

### Phase 5 — evidence and handoff

1. Append the categorized URL inventory to evidence:
   - `pentest_agent_append_evidence` with `source=archive`, `method=wayback+commoncrawl`, timestamps, total URL count, counts per category, and priority-1 in-scope URL list (redacted of any tokens or credentials in URLs).
2. For each Priority 1 finding, create a hypothesis: what the URL suggests (e.g., "`/admin/` endpoint suggests an admin panel — test for authentication bypass" or "`.env` file archived — likely contains database credentials").
3. Hand off to the appropriate skill:
   - Admin/auth endpoints → `recon-web-surface` or `enum-web-content` for live probing.
   - API endpoints → `enum-api-surface` for endpoint mapping.
   - JS files → `recon-js-analysis` for JS endpoint and secret extraction.
   - Parameterized URLs → vulnerability-specific skills based on parameter type (`vuln-sqli`, `vuln-xss`, `vuln-ssrf`, `vuln-lfi-rfi`, `vuln-open-redirect`).
   - Config/backup/debug files → flag as potential sensitive-exposure and hand off to `vuln-sensitive-exposure`.

## Decision points

- **Archive returns thousands of URLs**: prioritize by path interest (admin, API, auth, dev, config). Do not spend time on static assets unless JS files are needed for JS analysis.
- **URL contains tokens or session data in query string**: the archive has captured a URL with a session token, API key, or password. Redact the token from evidence immediately. Record the URL pattern without the token value. If the token resembles a secret, flag as `vuln-sensitive-exposure` — the token was publicly archived.
- **Discovered subdomain not in known scope**: flag as `UNKNOWN` in the scope validation phase. Do not probe or validate. If the subdomain appears to belong to the target (e.g., consistent naming convention, same IP range from passive DNS), escalate to the operator for scope clarification.
- **Archive contains pages from a retired or decommissioned environment**: retired environments may have weaker security (no longer maintained, missing patches, default credentials). Flag as high-interest and prioritize for active validation if within scope.

## Prohibited behavior

- Sending any HTTP request to the target or discovered URLs during this skill — this is passive collection only.
- Probing or validating discovered URLs — hand off to active skills after scope validation.
- Collecting URLs for out-of-scope domains beyond documentation purposes.
- Scraping archive services at high rates — stay within rate limits (≤ 2 requests/second for Wayback CDX, ≤ 1 request/second for Common Crawl).
- Storing discovered tokens, session IDs, API keys, or passwords from archived URLs in evidence — redact immediately.

## Stop conditions

- Archive API returns 429 (rate limited) → stop, wait for the rate-limit window, reduce request rate, resume.
- Archive returns no results for the target domain → document, the target may be new, have `robots.txt` blocking in the past, or use JavaScript-only rendering that archives cannot capture. Hand off to `recon-dorking` for search-engine-based discovery.
- Scope validation reveals ALL discovered URLs are out of scope → stop, document the domain's boundary is strict, no further recon from archive data.

## Evidence

Store source attribution, query parameters, total URL count, per-category count, scope-validation summary, Priority 1 in-scope URL list, and handoff recommendations with skill references. Evidence template:

```text
Archive recon for: TARGET.COM
Sources: Wayback Machine (12,847 URLs), Common Crawl CC-MAIN-2024-33 (3,421 URLs)
Total unique after dedup: 14,203
Scope validation: 11,892 IN_SCOPE | 1,845 OUT_OF_SCOPE | 466 UNKNOWN

Category counts:
  admin/panel: 34
  API endpoints: 892
  dev/staging: 12
  auth pages: 67
  file upload: 23
  config files: 8 ← Priority 1
  backup files: 15 ← Priority 1
  debug pages: 6 ← Priority 1
  parameterized URLs: 2,311
  JS files: 1,204

Priority 1 — immediate handoff:
  - https://TARGET.COM/.env (Wayback snapshot, 2023-06-15) → vuln-sensitive-exposure
  - https://TARGET.COM/admin/config.php.bak (Wayback snapshot, 2022-11-02) → vuln-sensitive-exposure
  - https://dev.TARGET.COM/phpinfo.php (Wayback snapshot, 2023-01-20) → recon-exposed-devtools
```

Redact tokens, session identifiers, API keys, passwords, and PII from all evidence. Never store raw archive responses containing sensitive data.

## Report handoff

No direct report from this skill — the output is a categorized URL inventory that feeds into active enumeration and validation skills. The evidence record serves as the handoff artifact. Include scope-validation decisions and priority classifications so downstream skills can act without re-validating scope.
