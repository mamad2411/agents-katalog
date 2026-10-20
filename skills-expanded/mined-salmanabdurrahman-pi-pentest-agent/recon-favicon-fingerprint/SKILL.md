---
name: recon-favicon-fingerprint
description: Favicon hash fingerprinting for infrastructure discovery and technology identification — compute MurmurHash3 (mmh3) of favicon.ico from target URLs, search Shodan/FOFA/Censys for matching infrastructure, identify technology stack from known favicon hashes (Grafana, Jenkins, GitLab, Jira, phpMyAdmin, etc.), and verify discovered assets with HTTP probing. Active favicon fetch requires authorization; passive hash search against third-party databases does not contact the target.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [fingerprint-notes, command-log, redacted-evidence, hypothesis-queue]
---

# Favicon hash fingerprinting — infrastructure and technology discovery

Use this skill to fingerprint a target's web infrastructure through favicon hash computation and search. The favicon (favicon.ico) is a small icon file served by almost every web application. Its content hash is a stable, low-noise fingerprint: identical favicons mean identical software stacks, shared infrastructure, or the same organization. Computing the hash requires fetching the favicon from the target (active, needs authorization). Searching third-party databases (Shodan, FOFA, Censys) with the hash to discover other servers with the same favicon is passive relative to the target.

## Required inputs

- Target URLs (at minimum the root, plus common subdomains).
- Authorization cache before fetching any favicon from the target.
- Shodan/FOFA/Censys API keys if using their search APIs (optional; manual dork-based search works without API keys).
- Scope file for validating discovered infrastructure as in-scope or out-of-scope.
- Evidence goal: favicon hash, matched technology identification, discovered infrastructure with same hash, and handoff to active scanning for confirmed in-scope assets.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` to load authorized target URLs for favicon fetching and to validate discovered infrastructure.
3. `pentest_agent_validate_target` for each target URL before fetching favicon, and for each discovered IP/host before any active probe.
4. `pentest_agent_check_authorization` before fetching ANY favicon from the target. Hash search against Shodan/FOFA/Censys is passive and does not require authorization.
5. `pentest_agent_build_command` for dry-run preview of any tool fetch commands.
6. `pentest_agent_execute_tool` for all HTTP fetches — rate-limit enforcement.
7. `pentest_agent_append_evidence` with favicon hash, technology identification, and discovered infrastructure.

## Workflow

### Phase 1 — favicon fetch and hash computation

Fetch the favicon from the target's web server and compute its mmh3 hash (the standard used by Shodan for `http.favicon.hash`).

1. Favicon URL candidates (in priority order):
   - `https://TARGET.COM/favicon.ico` — standard location.
   - `https://TARGET.COM/static/favicon.ico`
   - `https://TARGET.COM/assets/favicon.ico`
   - `https://TARGET.COM/images/favicon.ico`
   - `https://TARGET.COM/public/favicon.ico`
   - `https://www.TARGET.COM/favicon.ico` — the www subdomain may serve a different favicon.
   - Extract from HTML: `curl -s "https://TARGET.COM" | grep -iE 'rel=".*icon"' | grep -oE 'href="[^"]+"'` — the page may reference a non-standard favicon path or use a PNG/SVG instead of ICO.
2. Fetch each candidate:
   - `curl -s -o favicon_tmp.ico "https://TARGET.COM/favicon.ico" -w "%{http_code}, %{size_download} bytes" --max-time 5`
   - Skip if HTTP status is not 200 or if file size is 0. Favicons are typically 1-150 KB.
   - Verify the file is actually an image: `file favicon_tmp.ico`. Should show `MS Windows icon resource`, `PNG image data`, or `SVG XML`.
3. Compute mmh3 hash in Python:
   - The Shodan-compatible mmh3 hash uses a specific encoding: Base64-encode the favicon bytes, then compute mmh3 of the Base64 string. This is NOT the same as mmh3 of the raw bytes.
   - Script:
     ```python
     import base64, mmh3, sys
     with open(sys.argv[1], 'rb') as f:
         favicon_b64 = base64.encodebytes(f.read())
         h = mmh3.hash(favicon_b64)
         print(h)
     ```
   - Run: `python3 compute_favicon_hash.py favicon_tmp.ico`
   - Record: favicon URL, file size, detected image format, and computed mmh3 hash.
4. Alternative: use `httpx` with `-favicon` flag (if the target URL is live):
   - `httpx -u TARGET.COM -favicon -json` — returns favicon mmh3 hash directly. This is faster but redundant if you already have the hash.

### Phase 2 — technology identification from known hash database

Compare the computed favicon hash against a database of known software favicons. Many popular applications have distinctive favicons that persist across installations.

1. Known favicon hashes (curated list, expandable):
   - `-116323821`: Grafana — monitoring/observability platform.
   - `-247388890`: Jenkins (older versions) — CI/CD automation server.
   - `-1697334194`: Jenkins (newer versions).
   - `1073741824`: Kibana — Elasticsearch analytics UI.
   - `-1555533817`: GitLab — source-code management.
   - `-2100059989`: GitLab (alternate).
   - `-1922044295`: Jira — issue tracking.
   - `-1800948952`: Confluence — documentation/wiki.
   - `-1642474089`: SonarQube — code quality.
   - `-471736142`: phpMyAdmin — MySQL administration.
   - `116323821`: Grafana (alternate).
   - `-150751098`: Jupyter Notebook.
   - `1028228059`: Cisco device management.
   - `-1834225032`: Palo Alto Networks GlobalProtect portal.
   - `815962369`: Apache Tomcat.
   - `-772295965`: WordPress (default favicon).
   - `-2020561382`: Drupal (default favicon).
   - `915816449`: F5 BIG-IP management.
2. Check computed hash against the known list. If matched: high-confidence technology identification. Record the matched software name and version hints (if the hash is version-specific).
3. If no match: this is a custom or less-common favicon. The hash is still useful for infrastructure correlation (Phase 3). Record the hash as `UNKNOWN` technology.
4. Additional hash sources: `https://github.com/sansatart/scrapts/blob/master/shodan-favicon-hashes.csv` — community-maintained hash database. Use only if accessible and the data is current.

### Phase 3 — Shodan infrastructure search

Use the favicon hash to search Shodan for all internet-facing servers serving the same favicon. This reveals the target's infrastructure beyond what DNS enumeration finds — servers behind load balancers, non-HTTP services on the same host, and servers in different IP ranges but running the same software.

1. Shodan CLI search (requires API key):
   - `shodan search "http.favicon.hash:HASH" --fields ip_str,port,hostnames,org,domains --separator "," --limit 200 > shodan_results.csv`
   - The `--limit` caps results. Shodan may index many more matching servers — 200 is sufficient for initial triage.
2. Shodan web interface (manual, no API key needed):
   - URL: `https://www.shodan.io/search?query=http.favicon.hash%3AHASH`
   - Browse results manually. Filter by country, organization, or port to narrow the results.
3. FOFA search (requires account):
   - FOFA query: `icon_hash="HASH"`. URL: `https://fofa.info/result?qbase64=<base64_query>`
   - FOFA with country filter: `icon_hash="HASH" && country="US"`
   - FOFA has different coverage than Shodan, especially for Asian infrastructure.
4. Censys search (requires account, uses SHA-256 not mmh3):
   - Censys uses SHA-256 of the favicon content, not mmh3. Compute the SHA-256: `sha256sum favicon_tmp.ico`
   - Censys query: `services.http.response.favicons.hashes:"sha256:HASH256"`
5. ZoomEye search: `iconhash:"HASH"` (similar to Shodan/FOFA).

### Phase 4 — scope validation and infrastructure correlation

Analyze the discovered infrastructure to identify in-scope assets and organizational patterns.

1. For each discovered IP:
   - Check if the IP falls within an in-scope CIDR from the engagement scope file. Flag as `IN_SCOPE`.
   - Check the organization (org/ISP field from Shodan) — is it the target organization, a cloud provider hosting the target, or an unrelated third party?
   - Check hostnames/domains — do they belong to the target domain or a known subsidiary?
   - Check ports — does the server expose services beyond HTTP that may be entry points?
2. Infrastructure correlation:
   - Servers with the same favicon hash AND the same organization are likely managed by the same team, share the same deployment pipeline, or are part of the same infrastructure estate.
   - Servers with the same favicon but DIFFERENT organizations may be false positives (the favicon is from a common software package) or true positives (the target uses a cloud provider and Shodan attributes the IP to the cloud provider, not the target).
   - Cross-reference with DNS enumeration and ASN data to disambiguate.
3. Prioritize in-scope, non-obvious servers: servers not in the DNS enumeration output, servers on non-standard ports, and servers in IP ranges not previously associated with the target.

### Phase 5 — live verification of discovered infrastructure

For in-scope discovered servers, verify they are live and serve HTTP/HTTPS before handing off to active scanning.

1. HTTP probe of discovered IPs:
   - `httpx -l discovered_ips.txt -silent -title -status-code -tech-detect -favicon -o favicon_live.txt`
   - The `-favicon` flag re-computes the favicon hash and confirms the match.
2. Filter confirmed matches:
   - `grep "HASH" favicon_live.txt` — servers where the favicon hash matches the target's hash. These are confirmed infrastructure matches.
3. For confirmed matches: record IP, port, hostname (if any), HTTP title, technology stack, and organization. Hand off to `recon-web-surface` for further probing.
4. For non-matches (favicon hash differs on live probe): the favicon may have changed since Shodan last scanned, or the server may serve different content based on Host header. Record as `UNCONFIRMED`.

## Decision points

- **Favicon hash matches a known product (Grafana, Jenkins, etc.)**: high-confidence technology identification. Record immediately. If the product is an admin/internal tool (Grafana, Jenkins, GitLab, phpMyAdmin) and it's exposed publicly, flag as a finding — internal tools should not be public-facing.
- **Shodan/FOFA returns dozens or hundreds of matching servers for the same organization**: the target uses a standardized deployment with consistent favicons across many servers. This is common for large cloud deployments. The infrastructure correlation is strong — all these servers share the same software baseline.
- **Shodan returns matching servers for DIFFERENT organizations**: if the favicon is from a common software package (WordPress, Apache Tomcat default, nginx default), these are false positives — they belong to unrelated organizations. Exclude from infrastructure correlation. If the favicon is custom (no known match), matching servers at different organizations may indicate a shared vendor, shared CDN, or asset acquisition.
- **Favicon fetch returns 404**: the target does not have a favicon at the standard path. Check the HTML for a non-standard favicon link. If none found, document that favicon fingerprinting is not applicable for this target.
- **Multiple favicon paths return different files with different hashes**: different subdomains or paths serve different favicons. Compute hashes for each unique favicon. This may indicate different software stacks on different subdomains — record each hash separately.

## Prohibited behavior

- Fetching favicons from out-of-scope targets.
- Brute-forcing favicon paths at high volume — the candidate list is small (≤ 10 paths).
- Using Shodan/FOFA/Censys API keys without authorization or beyond rate limits.
- Probing discovered infrastructure that is OUT_OF_SCOPE or UNKNOWN without scope validation.
- Storing raw favicon files beyond the current session — the favicon itself is not evidence, just the hash.

## Stop conditions

- Shodan/FOFA/Censys API rate-limit reached → stop API queries. Use web-interface search manually for the highest-value hash.
- All favicon fetches return 404 → document that favicon fingerprinting is not applicable. Hand off to `enum-waf-tech` for alternative technology fingerprinting methods (HTTP headers, HTML meta tags, JavaScript signatures).
- Shodan returns zero results for the hash → the favicon is unique or Shodan has not indexed servers with this favicon yet. Record the hash for future correlation. The hash itself is still useful — the target's internal servers will have the same hash even if Shodan has not indexed them.

## Evidence

For each favicon analyzed, record: target URL, favicon URL, file size, image format, computed mmh3 hash, technology identification (known match or UNKNOWN), Shodan/FOFA result count, in-scope discovered infrastructure, and live-verification results. Evidence template:

```text
Favicon fingerprint recon for: TARGET.COM

Favicon #1:
  Source: https://TARGET.COM/favicon.ico
  Size: 1,150 bytes | Format: MS Windows icon resource
  mmh3 hash: -116323821
  Technology: Grafana (HIGH confidence — exact hash match with known Grafana favicon)
  → [MEDIUM] Publicly accessible Grafana favicon. Grafana is an internal monitoring tool — exposure indicates Grafana may be publicly accessible.

Favicon #2:
  Source: https://dev.TARGET.COM/favicon.ico
  Size: 4,286 bytes | Format: PNG image data
  mmh3 hash: 123456789
  Technology: UNKNOWN (custom favicon, not in known hash database)

Shodan search for #1 (Grafana hash, -116323821):
  Total results: 18 for organization "Target Corp"
  In-scope IPs: 12 (ports: 80, 443, 3000, 8080)
    → 203.0.113.50:3000 — Grafana dashboard (confirmed by httpx probe)
    → 203.0.113.51:3000 — Grafana dashboard (confirmed)
    → 203.0.113.52:8080 — secondary web interface (confirmed)
  Out-of-scope: 6 (different organization or IP range not in engagement)

Shodan search for #2 (custom hash, 123456789):
  Total results: 3 for organization "Target Corp"
  In-scope IPs: 3 (ports: 443 only)
    → 203.0.113.100:443 — dev.TARGET.COM (confirmed)
    → 203.0.113.101:443 — staging.TARGET.COM (UNKNOWN to DNS enum — new discovery)
    → 203.0.113.102:443 — internal-api.TARGET.COM (UNKNOWN to DNS enum — new discovery)

Live verification (httpx):
  Confirmed: 15 / 15 in-scope IPs responded to HTTP probe with matching favicon hash.

Findings:
  [MEDIUM] Grafana publicly accessible on 12 IPs across ports 3000, 443, 8080.
  [INFO] Two previously unknown subdomains discovered via Shodan correlation: staging.TARGET.COM, internal-api.TARGET.COM.
```

Redact: Shodan/FOFA API keys, any discovered credentials or tokens in HTTP response titles, and IP addresses of out-of-scope third-party servers.

## Report handoff

1. `pentest_agent_record_finding` for: publicly exposed internal/admin tools (Grafana, Jenkins, GitLab, etc.) identified by favicon hash, discovered infrastructure not in previous enumeration (new IPs, new subdomains), and technology stack confirmation from favicon identification.
2. Package findings with: favicon hash, matched technology, Shodan/FOFA result count, discovered IPs and hostnames with scope validation, live-verification status, and technology stack fingerprint of confirmed servers.
3. Recommend: restrict admin/monitoring tools to internal networks or VPN only, remove or customize default favicons on internal tools to reduce fingerprintability, and audit Shodan/FOFA indexing of the organization's infrastructure.
4. Explicitly note: favicon hash was computed from a publicly accessible favicon file (< 10 KB, no sensitive content), Shodan/FOFA searches are passive (no target contact), and only in-scope IPs were probed for live verification.
