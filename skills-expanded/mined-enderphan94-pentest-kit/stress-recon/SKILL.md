---
name: stress-recon
description: >
  Runs Phases 0-4 of the HexStrike web assessment: discovers all live subdomains
  (subfinder, assetfinder, amass, dnsx, puredns, httpx, uncover, crt.sh CT logs),
  fingerprints tech stacks, WAFs, and cloud infrastructure (header mining → bucket
  enumeration, CSP/Link headers mined for new in-scope hosts), maps endpoints
  (ffuf, feroxbuster, gobuster, kiterunner, GraphQL), harvests URLs and parameters
  (katana, gospider, waybackurls, jsluice, arjun, paramspider), and ranks all
  discovered URLs by bug potential (1-5). Output: three frozen URL pool files
  ready for stress-scan's parallel vulnerability agents.
  Use when the user invokes "stress-recon", "recon scan", "asset discovery",
  "subdomain enumeration", "URL harvesting", "build URL pools", or
  "enumerate endpoints".
---

# Stress Recon — Asset Discovery & URL Pool Builder

## Purpose

Discover the full attack surface for a target. Build three URL pool files that
stress-scan's parallel vulnerability agents will consume.
**Phases chain outputs — do not skip phases or stop early.**

> **Key rule**: Steps marked **"always run"** use only `curl`/`grep` and must execute
> even when every tool is missing. Steps that require a specific tool print
> `[skip] <tool> — run: bash install.sh` and continue; never skip an entire phase.

Before starting, read **[references/TOOLKIT.md](references/TOOLKIT.md)** and
**[references/advanced-tools.md](references/advanced-tools.md)** for tool flags and chains.
See **[references/toolkit_web_reference.md](references/toolkit_web_reference.md)** for wordlist vars.

## Three Growing URL Pools

These three files grow continuously as phases run. Every phase reads the latest version.
New in-scope hosts found in any phase must be added and re-probed immediately.

```
recon/live_urls.txt       — live HTTP targets (hosts); grows: Ph1 → Ph2 → Ph3 → Ph4
recon/all_endpoints.txt   — all paths / routes discovered; grows: Ph3 → Ph4
crawl/all_urls_final.txt  — full parametrized URL surface; finalized: Ph4
```

**Feed-back rule**: whenever a new in-scope hostname is found (in headers, JS, redirects,
cloud buckets, CSP, VHost fuzzing) — probe it with `httpx -silent` and, if live, append to
`live_urls.txt`. Every tool that runs after that point will include it automatically.

## Scan Progress Checklist

```
- [ ] Phase 0: Environment setup + OOB server started
- [ ] Phase 1: Asset discovery              → live_urls.txt (initial)
- [ ] Phase 2: Tech + cloud fingerprinting  → tech_stack.txt, cloud_intel.txt, WAF rate set
                                              live_urls.txt updated with new hosts from headers
- [ ] Phase 3: Content + API discovery      → all_endpoints.txt
                                              live_urls.txt updated with VHost finds
- [ ] Phase 4: URL & param harvesting       → all_urls_final.txt (crawls both pools)
                                              live_urls.txt updated with hosts from JS/crawl
- [ ] Phase 4b: Target ranking             → patterns/ranked_urls.txt (1-5 score per URL)
```

---

## Phase 0 — Environment & Scope

Read `scope.txt` (project root): `TARGET_URL` (required — stop if empty),
`AUTH_HEADER`, `RATE_LIMIT_DELAY`, `MAX_REQUESTS`.

**Multi-target support**: `TARGET_URL` may contain comma-separated URLs
(e.g., `https://acn.com, https://sub.acn.com, https://sub2.acn.com`).
Parse all targets, use the first as primary, and run every phase against ALL targets:
```
# Parse targets
ALL_TARGETS=$(echo "$TARGET_URL_RAW" | tr ',' '\n' | sed 's/^ *//;s/ *$//' | grep -v '^$')
PRIMARY_TARGET=$(echo "$ALL_TARGETS" | head -1)
```

Source `skills/stress-scan/script/env_setup.sh` to load wordlist vars. Create output dir using primary domain:

```
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TARGET_DOMAIN=$(echo "$PRIMARY_TARGET" | sed -E 's|https?://||;s|/.*||;s|:.*||')
OUTDIR="reports/assets/stress_${TIMESTAMP}_${TARGET_DOMAIN}"
mkdir -p "$OUTDIR"/{recon,ffuf,crawl,params,patterns,nuclei,cloud}
```

Add ALL target URLs to `live_urls.txt` as initial seeds before Phase 1 begins:
```
echo "$ALL_TARGETS" > "$OUTDIR/recon/live_urls.txt"
```

For each target URL, extract its domain and add to the subdomain enumeration list.
All phases run against every target — the three URL pools aggregate results from all targets.

Start **interactsh-client** → save `$COLLAB_HOST` for OOB blind testing in later phases.

---

## Phase 1 — Asset Discovery

**Goal**: Build initial `live_urls.txt`. This is the seed — it grows in Phases 2, 3, 4.

### 1a — Passive subdomain enumeration

- Run **subfinder** (`-timeout 5`), **assetfinder**, `timeout 5m` **amass** `-passive -timeout 5` in parallel
- **Normalize and deduplicate**: `cat subfinder.txt assetfinder.txt amass_parsed.txt | tr '[:upper:]' '[:lower:]' | sed -E 's/:443$//' | sort -u > all_subs.txt`
  (lowercase all hostnames, strip default port, dedup)
- **Certificate transparency** (**always run — curl only**):
  ```
  curl -s --max-time 30 "https://crt.sh/?q=%25.$TARGET_DOMAIN&output=json" \
    | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u \
    | anew "$OUTDIR/recon/all_subs.txt"
  ```
- **AlienVault OTX** (**always run if `$OTX_API_KEY` is set — curl only**):
  Queries OTX passive DNS for subdomains not found by other tools.
  ```
  if [ -n "${OTX_API_KEY:-}" ]; then
    curl -s --max-time 30 \
      "https://otx.alienvault.com/api/v1/indicators/domain/$TARGET_DOMAIN/passive_dns" \
      -H "X-OTX-API-KEY: $OTX_API_KEY" \
      | jq -r '.passive_dns[].hostname' 2>/dev/null \
      | grep -i "\.$TARGET_DOMAIN$" | sort -u \
      | anew "$OUTDIR/recon/all_subs.txt"
    echo "[+] OTX passive DNS merged into all_subs.txt"
  fi
  ```
  If `$OTX_API_KEY` is not set, skip silently — this is an optional enhancement.

### 1b — Active DNS resolution + brute force

- `timeout 10m` **dnsx** `-wd $TARGET_DOMAIN -timeout 5 -retries 1` → resolve + filter wildcards → `live_subs.txt`
- `timeout 5m` **puredns** resolve (if installed) → wildcard-safe secondary validation → merge
- **Active DNS brute force**: `timeout 15m` `dnsx -d $TARGET_DOMAIN -w $DNS_SUBS_110K -silent -timeout 3 -retries 1` → merge into `all_subs.txt`
  **Note**: use `$DNS_SUBS_5K` instead of `$DNS_SUBS_110K` if target is behind Cloudflare/WAF to avoid hours-long DNS hangs

### 1c — HTTP probing + explicit prefix coverage

- **httpx** `-status-code -title -follow-redirects -timeout 10` on `all_subs.txt` → `live_targets.txt`; always add `$TARGET_URL`
- `timeout 5m` **tlsx** `-l all_subs.txt` → harvest SANs from TLS certs → new subdomains → merge into `all_subs.txt`; re-probe
- **Explicit prefix probe** (**always run**): probe `{prefix}.$TARGET_DOMAIN` for each of:
  `files cdn static media assets storage img images backup data idv pay id verify auth sso api2 api-v2 dev staging admin portal internal ops gateway`
  → httpx-probe results → merge live into `live_targets.txt`
- `timeout 2m` **uncover** `-q "hostname:$TARGET_DOMAIN"` → Shodan/Censys/FOFA → merge

### 1d — Missed host recovery (**always run — curl only**)

Some subdomains may fail httpx probing (Cloudflare challenge, timeout, rate limit) but
still be live. This step catches them. **This is critical — it prevents the bug where
discovered hosts are silently dropped.**

1. Print counts: `"httpx probed: $(wc -l < all_subs.txt) subdomains → $(wc -l < live_targets.txt) live"`
2. Compare `all_subs.txt` against `live_targets.txt` → find missed subdomains:
   ```
   # Extract just hostnames from live_targets.txt for comparison
   sed -E 's|https?://||;s|[:/].*||' live_targets.txt | tr '[:upper:]' '[:lower:]' | sort -u > live_domains.txt
   tr '[:upper:]' '[:lower:]' all_subs.txt | sort -u > all_subs_clean.txt
   comm -23 all_subs_clean.txt live_domains.txt > missed_subs.txt
   echo "[!] $(wc -l < missed_subs.txt) subdomains missed by httpx"
   ```
3. For each missed subdomain, retry with curl — try **both HTTPS and HTTP**:
   ```
   while IFS= read -r sub; do
     # Try HTTPS first
     code=$(curl -sk -o /dev/null -w "%{http_code}" --max-time 15 \
       -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
       "https://$sub" 2>/dev/null)
     if [[ "$code" =~ ^(200|301|302|303|307|308|401|403|405)$ ]]; then
       echo "https://$sub" >> live_targets.txt
       echo "[+] Recovered: https://$sub (HTTP $code)"
       continue
     fi
     # Try HTTP if HTTPS failed
     code=$(curl -sk -o /dev/null -w "%{http_code}" --max-time 15 \
       -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
       "http://$sub" 2>/dev/null)
     if [[ "$code" =~ ^(200|301|302|303|307|308|401|403|405)$ ]]; then
       echo "http://$sub" >> live_targets.txt
       echo "[+] Recovered: http://$sub (HTTP $code)"
     fi
   done < missed_subs.txt
   ```
4. Print reconciliation:
   ```
   TOTAL_SUBS=$(wc -l < all_subs.txt)
   LIVE_BEFORE=$(wc -l < live_domains.txt)
   RECOVERED=$(grep -c "Recovered" recovery_log.txt 2>/dev/null || echo 0)
   LIVE_AFTER=$(wc -l < live_targets.txt)
   PERMANENTLY_MISSED=$((TOTAL_SUBS - LIVE_AFTER))
   echo "=== Host Reconciliation ==="
   echo "  Total subdomains found:  $TOTAL_SUBS"
   echo "  httpx confirmed live:    $LIVE_BEFORE"
   echo "  curl recovered:          $RECOVERED"
   echo "  Final live hosts:        $LIVE_AFTER"
   echo "  Permanently unreachable: $PERMANENTLY_MISSED"
   ```
5. Save permanently missed hosts: `comm -23 all_subs_clean.txt <(sed -E 's|https?://||;s|[:/].*||' live_targets.txt | sort -u) > missed_unrecoverable.txt`

### 1e — URL extraction and normalization

Extract clean URLs → `live_urls.txt`:
```
# Normalize: lowercase hostname, strip default ports, strip trailing slashes
sed -E 's|https?://|&|; s|([^/]):443/|\\1/|; s|([^/]):80/|\\1/|; s|/$||' live_targets.txt \
  | tr '[:upper:]' '[:lower:]' | sort -u > live_urls.txt
```
Print count. If 0 — stop, report DNS failure.

### Feed-back recovery rule (applies to ALL later phases)

**Whenever a new in-scope hostname is found in Phases 2, 3, or 4** (from headers, JS,
crawl output, waybackurls, etc.), apply this recovery sequence:
1. `httpx -silent` probe → if live, add to `live_urls.txt`
2. If httpx fails → curl fallback (HTTPS then HTTP, 15s timeout, browser User-Agent)
3. Log result: `"[+] New host from Phase N: $host (live)"` or `"[!] New host from Phase N: $host (unreachable)"`

**Never silently drop a discovered host.** Every host must be either confirmed live or
explicitly logged as unreachable.

---

## Phase 2 — Tech + Cloud Fingerprinting

**Goal**: Stack/WAF/cloud intel. **Also mines response headers for new hosts → updates live_urls.txt.**

### 2a — Stack, WAF, and TLS detection

- **httpx** `-tech-detect` on `live_urls.txt` → `tech_stack.txt`
- **wafw00f** on `$TARGET_URL` → WAF: `TOOL_RATE=10 TOOL_THREADS=10`; no WAF: `TOOL_RATE=50 TOOL_THREADS=30`
- `timeout 2m` **nikto** `-maxtime 30` on `$TARGET_URL`; `timeout 3m` **testssl.sh** for TLS weakness audit
- `timeout 3m` **wpscan** `--max-threads 5` if WordPress detected; `timeout 2m` **graphw00f** to fingerprint GraphQL across live targets
- **Sensitive path probe** (**always run — curl only**): on `$TARGET_URL`:
  `/.git/HEAD /.env /robots.txt /sitemap.xml /api/swagger /api/openapi.json /actuator /server-status /phpinfo.php /.well-known/security.txt`
  → save 200/403 content to `recon/sensitive_paths.txt`; extract any paths from robots.txt/sitemap.xml → `all_endpoints.txt`

### 2b — Full response header mining (**always run — curl only**)

For every URL in `live_urls.txt`, `curl -sIL --max-time 5 {url}` → save to `cloud/all_headers.txt`. Extract:

**Cloud intel** → `cloud/cloud_headers.txt`:
- `x-goog-encryption-kms-key-name` → `grep -oE 'projects/[^/]+' | sed -E 's|projects/||'` → `cloud/gcp_projects.txt`
- `x-amz-*` → bucket/region hints → `cloud/aws_hints.txt`
- `x-ms-* / x-azure-*` → Azure storage hints → `cloud/azure_hints.txt`
- `server: UploadServer` + `via: 1.1 google` = raw GCS backend, no WAF

**New in-scope hosts** → immediately httpx-probe and append live results to `live_urls.txt`:
- `Content-Security-Policy:` → extract all `https://` sources matching `*.$TARGET_DOMAIN`
- `Link:` header → extract URLs; scope-filter; add paths to `all_endpoints.txt`
- `Access-Control-Allow-Origin:` → note non-wildcard origins that match `*.$TARGET_DOMAIN`
- `Location:` redirects to a different hostname → probe + add if live and in-scope

### 2c — Cloud storage bucket enumeration (**always run — curl only**)

For each project in `cloud/gcp_projects.txt`, test these bucket names (project + suffix):
`"" -storage -backup -assets -data -static -uploads -media -files -public -prod -staging`
```
code=$(curl -s -o "$OUTDIR/cloud/gcs_${bucket}.xml" -w "%{http_code}" \
  "https://storage.googleapis.com/${bucket}/?max-keys=10")
[ "$code" = "200" ] && echo "CRITICAL: gs://${bucket}" | tee -a "$OUTDIR/cloud/exposed_buckets.txt"
```
Also test S3: `https://s3.amazonaws.com/{name}/` and Azure: `https://{name}.blob.core.windows.net/?comp=list`.
Run `timeout 5m` **cloud_enum** `-k $TARGET_DOMAIN` if installed. Any public bucket URLs → append to `all_endpoints.txt`.

---

## Phase 3 — Content + API Discovery

**Goal**: Full endpoint map. New vhosts found here → update `live_urls.txt` → downstream phases include them.

- **ffuf** `$WEB_COMMON -timeout 10` on every URL in `live_urls.txt` → `ffuf/ffuf_<host>.json` → append to `all_endpoints.txt`
- **ffuf** VHost fuzzing: `-H "Host: FUZZ.$TARGET_DOMAIN"` with `-fw <baseline_word_count> -timeout 10`
  → any live VHost → httpx-probe → add to `live_urls.txt`; re-run Phases 2b/2c on new hosts
- `timeout 10m` **feroxbuster** `--timeout 10 --time-limit 10m` recursive on `/api /admin /v1 /dashboard` paths found by ffuf → append to `all_endpoints.txt`
- `timeout 5m` **gobuster** dns + vhost modes; `timeout 5m` **dirsearch** supplementary scan on primary target
- `timeout 5m` **kiterunner** (`kr scan`) on `live_urls.txt` with Assetnote routes wordlist → REST API routes → `all_endpoints.txt`
- API versioning: ffuf on `$TARGET_URL/{v1,v2,v3,api,graphql}/FUZZ` → `all_endpoints.txt`
- If GraphQL detected: **graphql-cop** audit + **clairvoyance** schema recovery → schema paths → `all_endpoints.txt`
- Probe each discovered endpoint for response headers (Location, Link, CSP) → same feed-back rule as Phase 2b

---

## Phase 4 — URL & Parameter Harvesting

**Goal**: Build `all_urls_final.txt` from **both** live hosts and discovered endpoints.

- `timeout 15m` **katana** `-timeout 10` crawls BOTH `live_urls.txt` AND `all_endpoints.txt` (`-jc -depth 3`) → `crawl/all_urls.txt`
- `timeout 10m` **gospider** `-S live_urls.txt -d 3 -t 5` → append; `timeout 5m` **hakrawler** piped from `live_urls.txt` → append
- `timeout 3m` **waybackurls** + `timeout 3m` **gau** on `$TARGET_DOMAIN` → append (these surface historical endpoints tools miss)

### 4a — New host extraction from crawl/historical output (**always run**)

After crawling and historical URL collection, extract any NEW in-scope hosts that
weren't in `live_urls.txt`:
```
# Extract all unique hostnames from crawl output
sed -E 's|https?://||;s|[:/].*||' crawl/all_urls.txt | tr '[:upper:]' '[:lower:]' | sort -u > crawl_hosts.txt
sed -E 's|https?://||;s|[:/].*||' live_urls.txt | tr '[:upper:]' '[:lower:]' | sort -u > current_live_hosts.txt

# Find new in-scope hosts from crawl/wayback/gau
comm -23 crawl_hosts.txt current_live_hosts.txt | grep -i "$TARGET_DOMAIN" > new_crawl_hosts.txt

# Probe and add new hosts (apply feed-back recovery rule from Phase 1e)
while IFS= read -r host; do
  # httpx first, curl fallback if httpx fails (HTTPS then HTTP)
  <apply feed-back recovery rule>
done < new_crawl_hosts.txt
echo "[+] Crawl phase discovered $(wc -l < new_crawl_hosts.txt) new hosts, $(grep -c 'live' recovery_log.txt) confirmed live"
```

**Why this matters**: waybackurls/gau often return URLs on subdomains not in `live_urls.txt`.
katana/gospider may follow redirects to new hosts. Without this step, those hosts exist
in `all_urls_final.txt` but were never probed — agents will waste requests on dead hosts
AND miss live hosts that weren't in the original recon.

- `timeout 5m` **jsluice** on all crawled JS files → URLs + secrets → `crawl/jsluice_output.jsonl`
  New in-scope hosts from jsluice → apply feed-back recovery rule → add live ones to `live_urls.txt`
- **unfurl** `--unique keys` on `all_urls.txt` → `params/unfurl_keys.txt`
- `timeout 2m` **arjun** on high-value endpoints in `all_endpoints.txt` (`.php .asp /api/ /user /search /query`, max 20 endpoints) → hidden params
- `timeout 3m` **paramspider** `-d $TARGET_DOMAIN` → `params/paramspider.txt` → append

### 4 final — URL normalization and merge
```
# Normalize: lowercase hostnames, strip default ports, strip trailing slashes
cat all_urls.txt all_endpoints.txt params/*.txt \
  | sed -E 's|^(https?://)([^/:]*)|\1\L\2|; s|:443/|/|; s|:80/|/|; s|/$||' \
  | sort -u > all_urls_final.txt
```
Print total count and host coverage:
```
echo "URLs: $(wc -l < all_urls_final.txt)"
echo "Unique hosts: $(sed -E 's|https?://||;s|[:/].*||' all_urls_final.txt | sort -u | wc -l)"
```

---

## Phase 4b — Target Ranking (Mythos Method)

**Goal**: Score every URL in `all_urls_final.txt` by bug potential (1-5) so stress-scan's
parallel agents can prioritize rank-5 targets first.

### Ranking Criteria

**Rank 5 — Critical targets** (highest bug potential):
- Auth endpoints: paths containing `/login /signin /signup /register /password /reset /token /oauth /sso /auth /session /verify`
- File operation params: `file= path= dir= filename= include= page= template= document= upload`
- Payment/financial params: `payment_id= transaction_id= amount= card= price= order_id= invoice=`
- Admin panels: paths containing `/admin /dashboard /manage /control /panel /console /cms`
- Direct object references: `user_id= account_id= customer_id= id= uid= pid=`

**Rank 4 — High-value targets**:
- API endpoints with user-controlled params: `/api/ /v1/ /v2/ /graphql` with query strings
- Search/filter endpoints: `search= query= q= filter= sort= keyword=`
- Redirect params: `redirect= url= next= return= goto= dest= callback=`
- Any endpoint returning JSON (API surface)

**Rank 3 — Medium targets**:
- Dynamic pages with query strings (any `?param=value`)
- Form action URLs
- Endpoints returning HTML with input forms

**Rank 2 — Low targets**:
- Static content with minor params (pagination, locale, cache busters)
- CDN URLs with version strings
- RSS/XML feeds

**Rank 1 — Minimal targets**:
- Pure static assets (images, CSS, JS libraries, fonts)
- Favicon, robots.txt, sitemap entries with no params
- Known third-party widget URLs

### Output Format

Write `patterns/ranked_urls.txt`:
```
5 https://app.example.com/api/v2/user?id=123
5 https://app.example.com/admin/dashboard
4 https://app.example.com/api/search?q=test
3 https://app.example.com/products?page=1&sort=price
2 https://cdn.example.com/assets/main.js?v=2.1
1 https://app.example.com/favicon.ico
```

### Implementation

Read `all_urls_final.txt` line by line. For each URL:
1. Extract path and query parameters
2. Match against ranking criteria (highest matching rank wins)
3. Write `<rank> <url>` to `patterns/ranked_urls.txt`

Sort output by rank descending: `sort -rn -k1,1 -o patterns/ranked_urls.txt patterns/ranked_urls.txt`

Print summary: `Ranked N URLs: R5=X R4=Y R3=Z R2=W R1=V`

---

## Final Output Summary

Print this at the end of the scan:

```
=== stress-recon complete ===

  Pipeline Reconciliation (no host left behind):
  ┌─────────────────────────────────────────────────┐
  │ Subdomains found (all sources):    N            │
  │ DNS resolved:                      N            │
  │ httpx confirmed live:              N            │
  │ curl recovered (Phase 1d):         N            │
  │ New hosts from headers (Phase 2):  N            │
  │ New hosts from crawl (Phase 4a):   N            │
  │ Final live hosts:                  N            │
  │ Permanently unreachable:           N            │
  └─────────────────────────────────────────────────┘

  Attack Surface:
    Live hosts:        $(wc -l < recon/live_urls.txt)
    Endpoints:         $(wc -l < recon/all_endpoints.txt)
    Parametrized URLs: $(wc -l < crawl/all_urls_final.txt)
    Unique hosts in URLs: $(sed -E 's|https?://||;s|[:/].*||' crawl/all_urls_final.txt | sort -u | wc -l)
    Ranked targets:    $(wc -l < patterns/ranked_urls.txt)
    Cloud projects:    $(wc -l < cloud/gcp_projects.txt 2>/dev/null || echo 0)
    Exposed buckets:   $(wc -l < cloud/exposed_buckets.txt 2>/dev/null || echo 0)

  Output directory: $OUTDIR
  Next step: run stress-scan to launch parallel vulnerability agents
======
```

**If "Permanently unreachable" > 0**: Review `recon/missed_unrecoverable.txt`. These hosts
were found by recon but could not be reached. They may be internal, firewalled, or
temporarily down. Consider re-scanning them later or adding to scope for manual testing.

---

## Safety Rules

- No credential brute-forcing — passive enumeration and probing only
- Respect `MAX_REQUESTS` hard cap across the entire session
- WAF detected → cap all tool rates at ≤ 10 req/s
- No destructive HTTP methods (PUT / DELETE / PATCH)
- No cloud object deletion or upload — probe only
- Missing tool → `[skip] <tool> — run: bash install.sh`; use curl fallback for "always run" steps
- **Timeout rule (MANDATORY)**: Every external tool invocation MUST have a timeout.
  Use `timeout Ns <command>` wrapper for tools without built-in timeout flags.
  If a tool hangs past its timeout, it is killed and the phase continues.
  **Read timeout values from `scope.txt`** — users can adjust these:
  - `TOOL_TIMEOUT_DNS` (default 900s/15m) — dnsx, puredns, amass
  - `TOOL_TIMEOUT_CRAWL` (default 900s/15m) — katana, gospider, hakrawler
  - `TOOL_TIMEOUT_FUZZ` (default 600s/10m) — ffuf, feroxbuster, gobuster
  - `TOOL_TIMEOUT_SCANNER` (default 600s/10m) — nuclei, dalfox, corsy
  - `TOOL_TIMEOUT_API` (default 120s/2m) — uncover, cloud_enum, OTX
  - `TOOL_TIMEOUT_CURL` (default 10s) — individual curl `--max-time`
  **Never run dnsx with 110K wordlist without `timeout $TOOL_TIMEOUT_DNS` and `-timeout 3 -retries 1`.**
