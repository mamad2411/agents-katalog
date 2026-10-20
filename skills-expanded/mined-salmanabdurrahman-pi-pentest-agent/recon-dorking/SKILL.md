---
name: recon-dorking
description: Search-engine dorking for passive OSINT reconnaissance — Google/Bing/DuckDuckGo operator-based discovery of exposed credentials, sensitive files, admin panels, directory listings, dev/staging environments, injection points, and infrastructure details. Fully passive; zero direct contact with the target. All results are hypotheses requiring scope validation before any active probing.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [query-notes, url-list, redacted-evidence, hypothesis-queue]
---

# Search-engine dorking — passive OSINT discovery

Use this skill to discover exposed target assets, sensitive files, credentials, and attack surface through search-engine operators (Google dorks). Dorking is fully passive — you query search engines, not the target. Every result is a hypothesis: the search engine indexed something, but you have not verified it is still accessible, belongs to the target, or is within scope. Never actively probe a dork result without scope validation and authorization.

## Required inputs

- Target domain, organization name, or identifying keywords.
- Scope file for validating discovered URLs as in-scope or out-of-scope.
- Rate limits: search engines aggressively rate-limit automated queries. Space queries at least 10 seconds apart for manual-style searching. Use search-engine APIs where available with proper API keys.
- Evidence goal: categorized URL inventory with confidence ratings and scope-validation flags.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` to load domain/URL scope rules for filtering dork results.
3. `pentest_agent_validate_target` to classify each discovered URL as in-scope or out-of-scope before any active validation.
4. `pentest_agent_check_authorization` NOT required for passive search-engine queries, but REQUIRED before accessing, probing, or validating any discovered URL.
5. `pentest_agent_append_evidence` with search query, date, source engine, and confidence.

## Workflow

### Phase 1 — domain and subdomain mapping

Discover the target's indexed web presence — subdomains, alternate domains, dev/staging environments, and forgotten microsites.

1. Core domain mapping dorks:
   - `site:TARGET.COM` — all indexed pages for the domain.
   - `site:TARGET.COM -www` — subdomains beyond the main www site.
   - `site:TARGET.COM -www -mail -shop -blog` — progressively exclude known subdomains to surface rare ones.
   - `site:*.TARGET.COM` — wildcard subdomain search (if supported by the engine).
2. Environment discovery:
   - `site:TARGET.COM inurl:dev OR inurl:staging OR inurl:test OR inurl:uat OR inurl:sandbox OR inurl:preview OR inurl:beta`
   - `site:TARGET.COM inurl:dev OR inurl:staging -inurl:device -inurl:developer` — filter false positives.
3. Tool-assisted enumeration:
   - `theHarvester -d TARGET.COM -b google,bing,duckduckgo,yahoo -f harvester_output.html` — aggregates results from multiple engines.
   - Certificate transparency as complementary passive source: `curl -s "https://crt.sh/?q=%25.TARGET.COM&output=json" | jq -r '.[].name_value' | sort -u` — not dorking, but fills gaps in search-engine coverage.
4. Record: total indexed pages estimate, distinct subdomains found, previously unknown subdomains (not in the initial scope file).

### Phase 2 — sensitive file and credential discovery

Search for accidentally exposed files containing credentials, configuration, or sensitive data.

1. Configuration and environment files:
   - `site:TARGET.COM filetype:env` — `.env` files containing application secrets.
   - `site:TARGET.COM filetype:conf OR filetype:config OR filetype:cfg` — configuration files.
   - `site:TARGET.COM filetype:ini OR filetype:yaml OR filetype:yml` — structured config files.
   - `site:TARGET.COM filetype:xml intext:password` — XML configs with credentials.
   - `site:TARGET.COM filetype:json intext:password OR intext:api_key OR intext:secret` — JSON files with secrets.
2. Backup and database files:
   - `site:TARGET.COM filetype:sql OR filetype:sql.gz OR filetype:dump` — database dumps.
   - `site:TARGET.COM filetype:bak OR filetype:backup OR filetype:old OR filetype:save OR filetype:swp` — backup files.
   - `site:TARGET.COM filetype:tar OR filetype:gz OR filetype:zip intext:password` — compressed archives.
3. Log files:
   - `site:TARGET.COM filetype:log` — log files (may contain session tokens, PII, internal paths, stack traces).
   - `site:TARGET.COM inurl:logs OR inurl:log` — log directories.
4. Credential dorks:
   - `site:TARGET.COM intext:"DB_PASSWORD" OR intext:"DATABASE_URL" OR intext:"DB_CONNECTION"`
   - `site:TARGET.COM intext:"api_key" OR intext:"secret_key" OR intext:"SECRET_KEY"`
   - `site:TARGET.COM intext:"aws_access_key_id" OR intext:"AWS_ACCESS_KEY"`
   - `site:TARGET.COM intext:"-----BEGIN RSA PRIVATE KEY-----" OR intext:"-----BEGIN PRIVATE KEY-----"`
   - `site:TARGET.COM intext:"password" intext:"username" filetype:txt`
5. For each discovered file: record the URL, the dork query that found it, the exposed content type, and a confidence rating. Confidence is "HIGH" if the search snippet clearly shows credentials. Do NOT visit the URL to confirm — this is passive-only. Hand off to `vuln-sensitive-exposure` for active validation.

### Phase 3 — admin panels and login pages

Discover exposed administrative interfaces, login portals, and management consoles.

1. Admin panel dorks:
   - `site:TARGET.COM inurl:admin`
   - `site:TARGET.COM inurl:login OR inurl:signin OR inurl:auth`
   - `site:TARGET.COM inurl:dashboard OR inurl:manage OR inurl:console`
   - `site:TARGET.COM intitle:"admin panel" OR intitle:"login" OR intitle:"dashboard"`
2. Specific application panels:
   - `site:TARGET.COM inurl:wp-admin` — WordPress admin.
   - `site:TARGET.COM inurl:phpmyadmin` — phpMyAdmin database interface.
   - `site:TARGET.COM inurl:jenkins` — Jenkins CI/CD.
   - `site:TARGET.COM inurl:grafana` — Grafana dashboards.
   - `site:TARGET.COM inurl:kibana` — Kibana Elasticsearch interface.
   - `site:TARGET.COM inurl:portainer` — Portainer Docker management.
   - `site:TARGET.COM inurl:adminer` — Adminer database management.
3. For each admin panel: record the URL pattern, the application type (if identifiable from the URL), and the exposure risk. Admin panels intended for internal use only are HIGH findings; admin panels intended to be public (e.g., customer login) are INFO. Hand off to `enum-web-content` for live verification.

### Phase 4 — exposed infrastructure and directory listings

Identify directory listings, Git repository exposure, error messages, and debug output.

1. Directory listing dorks:
   - `site:TARGET.COM intitle:"index of"` — Apache/Nginx directory listing.
   - `site:TARGET.COM intitle:"index of" "parent directory"` — more specific listing page.
   - `site:TARGET.COM intitle:"index of" inurl:backup` — backup directories with listing enabled.
   - `site:TARGET.COM intitle:"index of" .git` — exposed Git repositories.
2. Git exposure:
   - `site:TARGET.COM inurl:"/.git/config"` — Git configuration file (contains repository URL).
   - `site:TARGET.COM inurl:"/.git/"` — exposed Git directory.
3. Error messages (leak stack traces, file paths, versions):
   - `site:TARGET.COM intext:"Warning: mysql_connect"` — PHP MySQL connection error (exposes DB host, user, path).
   - `site:TARGET.COM intext:"ORA-01756"` — Oracle DB error.
   - `site:TARGET.COM intext:"Fatal error" intext:"on line"` — PHP fatal errors with file paths.
   - `site:TARGET.COM intext:"Stack trace:"` — stack traces (Java, Python, Node.js).
   - `site:TARGET.COM intitle:"500 Internal Server Error"` — server errors potentially exposing backend details.
   - `site:TARGET.COM intext:"phpinfo()"` — PHP info page (exposes full PHP config, environment variables, loaded modules).
4. Debug and dev output:
   - `site:TARGET.COM inurl:phpinfo.php OR inurl:info.php OR inurl:test.php` — debug pages.
   - `site:TARGET.COM inurl:"/debug" OR inurl:"/__debug__"` — debug toolbars (Symfony, Laravel Debugbar).
   - `site:TARGET.COM inurl:"/sockjs-node" OR inurl:"/__webpack_dev_server__"` — Webpack dev server.

### Phase 5 — injection-point mapping

Identify URLs with parameters that may be injection points. These are hypotheses — do NOT test them during passive recon.

1. Parameter dorks:
   - `site:TARGET.COM inurl:"?id="` — potential SQL injection / IDOR.
   - `site:TARGET.COM inurl:"?search=" OR inurl:"?q=" OR inurl:"?query="` — potential XSS.
   - `site:TARGET.COM inurl:"?page=" OR inurl:"?file=" OR inurl:"?path="` — potential LFI/RFI/path traversal.
   - `site:TARGET.COM inurl:"?redirect=" OR inurl:"?url=" OR inurl:"?next=" OR inurl:"?goto="` — potential open redirect / SSRF.
   - `site:TARGET.COM inurl:"?lang=" OR inurl:"?locale="` — potential LFI via language include.
2. Use `waybackurls` or `gau` output (from `recon-archive-urls`) combined with `gf` (grep-friendly patterns) to identify parameterized URLs more comprehensively than search engines alone.
3. For each injection-point candidate: record URL pattern, parameter name, suspected vulnerability class, and confidence (LOW — search result only, no verification). Hand off to the appropriate vulnerability skill for active validation.

### Phase 6 — GitHub, paste sites, and code repositories

Search third-party platforms for the target's accidentally exposed source code, credentials, or internal documentation.

1. GitHub dorks:
   - `site:github.com "TARGET.COM" password OR secret OR token OR api_key`
   - `site:github.com "TARGET.COM" "BEGIN RSA PRIVATE KEY"`
   - `site:github.com "TARGET.COM" filename:.env`
   - `site:github.com "TARGET.COM" filename:config.json`
2. GitLab: `site:gitlab.com "TARGET.COM" password OR secret`
3. Paste sites:
   - `site:pastebin.com "TARGET.COM"`
   - `site:paste.ee "TARGET.COM"`
   - `site:hastebin.com "TARGET.COM"`
4. Code-sharing platforms: `site:codeshare.io "TARGET.COM"`, `site:replit.com "TARGET.COM"`
5. For any credential found on third-party platforms: record the platform, the exposed data type, and the finding. Do NOT use or test the credentials. Flag as CRITICAL if the credential appears current (based on context in the snippet). Hand off to the engagement lead for incident response — exposed credentials on third-party platforms are an active data leak, not just a passive finding.

### Phase 7 — scope validation and handoff

1. For every URL or endpoint discovered, apply scope validation:
   - IN_SCOPE: domain matches an in-scope host pattern. Eligible for active validation handoff.
   - OUT_OF_SCOPE: clearly third-party or explicitly excluded. Document count, exclude from handoff.
   - UNKNOWN: not clearly in or out of scope. Flag for operator review.
2. For IN_SCOPE URLs, classify by risk and priority:
   - **Priority 1 (CRITICAL/HIGH)**: exposed credentials, database backups, .env/config files with secrets, Git repository exposure, phpinfo pages.
   - **Priority 2 (MEDIUM)**: admin panels, directory listings, debug pages, error messages with path disclosure.
   - **Priority 3 (LOW/INFO)**: static assets, informational pages, benign parameterized URLs.
3. `pentest_agent_append_evidence` with the categorized and prioritized URL inventory. Each entry includes: URL, dork query used, source engine, discovery date, confidence, scope status, and priority.
4. Hand off to active skills based on finding type.

## Decision points

- **Search snippet clearly shows a credential (password, API key, token)**: do NOT visit the URL. Record the finding as CRITICAL with HIGH confidence (the snippet provides evidence). Flag for immediate operator action — the exposed URL should be taken down or the credential rotated before it is cached or scraped by others.
- **Search engine returns CAPTCHA or blocks automated queries**: stop automated querying. Use a different search engine, reduce query rate, or manually verify select high-value dorks through a browser.
- **Dork result is from a third-party domain (e.g., a vendor's documentation site referencing the target)**: record as OUT_OF_SCOPE or UNKNOWN. The asset is not owned by the target — probing it would be out of scope.
- **Same result appears across multiple search engines**: increase confidence from LOW to MEDIUM. Multiple independent indexes increase the likelihood the page exists.
- **GitHub search reveals the target's private repository is public**: CRITICAL. Do NOT clone or browse the repository further. Record the repository name, URL, and the exposed data visible in the search snippet. Flag for immediate incident response.

## Prohibited behavior

- Accessing, probing, downloading, or interacting with any URL discovered through dorking — this is passive recon only. Active validation is a separate skill with separate authorization.
- Using discovered credentials to authenticate to any service.
- Scraping search engines at high rates — stay within rate limits (≥ 10 seconds between queries for the same engine).
- Using search-engine APIs with credentials not authorized for the engagement.
- Storing search-engine snippets containing credentials, PII, or internal data in unredacted evidence.

## Stop conditions

- Search engine CAPTCHA or block → stop automated queries for that engine. Document the block. Use remaining engines or manual verification.
- Discovery of active credential exposure in a search snippet → stop querying that specific URL pattern. Flag as CRITICAL and escalate. Do not attempt to gather more information about the exposed credential through additional dorks.
- All target dork patterns exhausted without actionable findings → document. The target has good search-engine hygiene. Move to other recon skills (archive URLs, certificate transparency, subdomain enumeration).

## Evidence

For each dorking session, record: search engines used, dork queries executed, approximate result counts, categorized findings with scope validation, priority classification, and handoff skill references. Evidence template:

```text
Search-engine dorking for: TARGET.COM
Engines used: Google (via API), Bing (manual), DuckDuckGo (manual)
Query date: 2024-01-15
Queries executed: 42

Domain mapping:
  site:TARGET.COM: ~12,000 indexed pages
  New subdomains found: dev.TARGET.COM, internal.TARGET.COM, legacy.TARGET.COM (all UNKNOWN scope status)

Sensitive files:
  site:TARGET.COM filetype:env: 1 result
    → https://TARGET.COM/.env (Google snippet shows: DB_PASSWORD=****, AWS_SECRET=****)
    → [CRITICAL] Exposed .env file with database and AWS credentials. HIGH confidence (snippet evidence).
  site:TARGET.COM filetype:sql: 0 results
  site:TARGET.COM filetype:bak: 2 results
    → https://TARGET.COM/config.php.bak — [HIGH] Backup configuration file.
    → https://dev.TARGET.COM/database.sql.bak — UNKNOWN scope (dev subdomain).

Admin panels:
  site:TARGET.COM inurl:admin: 8 results
    → https://TARGET.COM/admin/login.php — WordPress admin. INFO (public login expected).
    → https://TARGET.COM/phpmyadmin/ — [HIGH] phpMyAdmin exposed. MEDIUM confidence.

Directory listings:
  site:TARGET.COM intitle:"index of": 3 results
    → https://TARGET.COM/uploads/ — directory listing enabled, 47 files shown.
    → [MEDIUM] Directory listing exposes uploaded files.

Injection points:
  34 parameterized URLs found. Handoff to vuln-* skills for active validation.

GitHub:
  site:github.com "TARGET.COM" password: 1 result
    → github.com/dev-intern/legacy-app/blob/master/config.js — [CRITICAL] Hardcoded credentials in public GitHub repository. HIGH confidence.
```

Redact: all credentials, API keys, tokens, and PII visible in search snippets. Replace credential values with `[REDACTED]` in evidence. Do not store raw search-snippet text that contains secrets.

## Report handoff

No direct report — the dorking output is a hypothesis inventory. Each finding type maps to a specific active skill: exposed files → `vuln-sensitive-exposure`, admin panels → `enum-web-content`, parameterized URLs → `vuln-sqli`/`vuln-xss`/`vuln-ssrf`/`vuln-lfi-rfi` based on parameter context, GitHub/paste exposures → incident-response escalation (not pentest). Include dork query, source engine, and confidence with every handoff item so the active skill can validate efficiently.
