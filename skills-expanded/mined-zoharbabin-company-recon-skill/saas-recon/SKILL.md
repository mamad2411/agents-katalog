---
name: saas-recon
description: Deep OSINT reconnaissance on any SaaS/tech company. Discovers subsidiaries, maps infrastructure, finds every site embedding or linking to the target's technology via certificate transparency, DNS, archives, code search, live browser inspection, analytics correlation, and business intelligence. Produces a comprehensive markdown + HTML report. Use when investigating a company's technology footprint.
disable-model-invocation: false
argument-hint: "[company name or domain]"
---

# SaaS Technology Reconnaissance: $ARGUMENTS

You are the Lead Investigator. Your mission: discover **every website, app, and platform** that embeds, links to, redirects to, or references the target company's technology.

**Current date:** !`date +%Y-%m-%d`

---

## 0. HARD RULES

### 0a. RESEARCH ONLY
This is a **read-only investigation**. You do NOT modify any external systems. All data comes from publicly accessible sources: CT logs, DNS, web archives, search engines, public code repositories, and regulatory filings.

### 0b. CITE EVERYTHING
Every finding MUST include the source (URL, API endpoint, or tool) and the date accessed. No uncited claims.

### 0c. CONFIDENCE TIERS
Every client finding is assigned a confidence tier per [classification-rules.md](references/classification-rules.md):

| Tier | Required Evidence |
|------|-------------------|
| **CONFIRMED** | Live embed verified (custom element + network request), OR 2+ independent source types (e.g., CT cert + investor filing), OR active production + UAT subdomain pair |
| **STRONG** | CT certificate + DNS CNAME resolves to client-specific deployment, OR named in investor filing, OR found in decompiled mobile app |
| **MODERATE** | Single CT certificate with client-branded production subdomain, OR single CDN archive with client folder, OR single GitHub code reference |
| **WEAK** | Demo subdomain only, OR expired cert only, OR single press mention / job listing |

### 0d. COMPLETENESS OVER SPEED
Execute ALL 9 research phases + report compilation. Do not skip phases. If a phase yields no results, document that it was attempted and returned empty.

### 0e. OUTPUT DIRECTORY
Generate `target_slug` by lowercasing the company name, replacing spaces/special chars with hyphens, stripping trailing hyphens (e.g., "Acme Corp." becomes `acme-corp`). All output goes to `_recon/{target_slug}/` under the current working directory:
```
_recon/{target_slug}/
├── profile.json           # Phase 1: structured company profile
├── findings/              # Per-phase findings
│   ├── 01-company-profile.md
│   ├── 02-certificates.md
│   ├── 03-infrastructure.md
│   ├── 04-archives.md
│   ├── 05-code-search.md
│   ├── 06-embeds.md
│   ├── 07-web-mentions.md
│   ├── 08-analytics-correlation.md
│   └── 09-business-intel.md
├── report.md              # Final compiled report
└── report.html            # Rendered HTML report
```

### 0f. REFERENCE FILES
Before executing, read these reference files for detailed rules and templates:
- [classification-rules.md](references/classification-rules.md) — subdomain classification, industry categories, confidence tiers, deduplication
- [search-patterns.md](references/search-patterns.md) — Google dorks, GitHub queries, crt.sh queries, Shodan, PublicWWW, Playwright scripts
- [api-endpoints.md](references/api-endpoints.md) — exact curl commands for crt.sh, Wayback, Common Crawl, gau, DNS, and more
- [report-template.md](references/report-template.md) — report structure (fill ALL `{PLACEHOLDER}` values with actual data)
- [html-styles.md](references/html-styles.md) — CSS to inject into rendered HTML

### 0g. TOOL AVAILABILITY CHECK

**Run this check FIRST before starting any phase.** Detect available tools and MCP servers to maximize coverage:

```bash
echo "=== CLI Tool Availability ==="
for cmd in curl dig jq pandoc gau subfinder dnsx httpx nuclei katana waymore shodan uncover amass; do
  printf "%-15s " "$cmd:"
  if command -v $cmd &>/dev/null; then echo "AVAILABLE"; else echo "MISSING"; fi
done
```

Record the results internally. For each phase, use ALL available tools — not just the minimum. The skill instructions include primary tools AND alternatives for every operation. **Use every tool that is installed.**

If RECOMMENDED tools are missing, output one suggestion line to the user before proceeding:
```
⚠ Install recommended tools for deeper coverage: brew install subfinder dnsx nuclei katana; go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

### 0h. TOOL MATRIX

| Tool | Category | Phase(s) | Priority | Fallback |
|------|----------|----------|----------|----------|
| **MCP: google-researcher-mcp** | Web search | 1, 7, 8, 9 | PRIMARY | WebSearch + WebFetch |
| **MCP: playwright** | Browser automation | 1, 6 | PRIMARY | WebFetch + source grep |
| **MCP: github** | Code search | 5 | PRIMARY | WebFetch on github.com/search |
| **MCP: browser-tools** | DevTools inspection | 6 | OPTIONAL | Playwright fallback |
| **MCP: fetch** | Web content | 1, 7 | OPTIONAL | WebFetch |
| **MCP: sequential-thinking** | Analysis | All | OPTIONAL | Direct reasoning |
| Bash: `curl` | API calls | 2, 3, 4 | REQUIRED | No fallback |
| Bash: `dig` | DNS resolution | 1, 3 | REQUIRED | No fallback |
| Bash: `jq` | JSON parsing | All | REQUIRED | Python one-liner |
| Bash: `pandoc` | HTML rendering | 10 | PRIMARY | Write HTML directly |
| Bash: `gau` | URL collection | 4 | PRIMARY | Wayback CDX + CC CDX only |
| Bash: `subfinder` | Subdomain discovery | 1, 2 | RECOMMENDED | crt.sh only |
| Bash: `dnsx` | Bulk DNS resolution | 3 | RECOMMENDED | dig loop |
| Bash: `httpx` (ProjectDiscovery) | Batch URL probing | 6 | RECOMMENDED | WebFetch per-URL |
| Bash: `nuclei` | Template scanning | 6 | OPTIONAL | httpx match-string |
| Bash: `katana` | JS site crawling | 6 | OPTIONAL | Playwright crawl |
| Bash: `waymore` | Extended URL collection | 4 | OPTIONAL | gau covers most sources |
| Bash: `shodan` | Server search | 3, 5 | OPTIONAL | Web-based Shodan search |
| Bash: `uncover` | Multi-engine search | 5 | OPTIONAL | Individual searches |
| Bash: `amass` | Asset discovery | 1 | OPTIONAL | subfinder + crt.sh |

---

## 1. PHASE 1 — COMPANY PROFILING

**Goal:** Build a complete picture of the target — all names, brands, subsidiaries, products, and domains. This phase determines the scope for all subsequent phases.

### 1a. Identify the Target

Parse `$ARGUMENTS`:
- Contains `.` → treat as primary domain; research the owning company
- No `.` → treat as company name; discover its domains

### 1b. Company Deep Dive

Use `mcp__google-researcher-mcp__search_and_scrape` (or fallback) to research:

1. **Corporate identity**: Full legal name, HQ, founding year, stock ticker
2. **Subsidiaries & acquisitions**: Every owned/acquired company — each may have separate domains
3. **Product portfolio**: Every product name, brand, sub-brand — each may have its own domain
4. **Domain inventory**:
   - Scrape company website footer, legal pages, terms of service for linked domains
   - Search: `"company name" site OR domain OR website`
   - For each discovered domain, check if alternate TLDs exist via web search (NOT via `dig` — most won't resolve)
   - Look for redirect chains between domains using WebFetch
5. **Public company filings** (if ticker found): Check SEC EDGAR, SEDAR+, Companies House. Search for investor presentations naming customers.

### 1c. Passive Subdomain Discovery

**If `subfinder` is available:**
```bash
subfinder -d DOMAIN1 -d DOMAIN2 -silent -o _recon/{target_slug}/subdomains_subfinder.txt
```
This queries 40+ passive sources (SecurityTrails, Censys, VirusTotal, Shodan, etc.) — far more comprehensive than crt.sh alone.

**If `amass` is available:**
```bash
amass enum -passive -d DOMAIN1,DOMAIN2 -o _recon/{target_slug}/subdomains_amass.txt
```

**Always:** Merge results with crt.sh output in Phase 2 for maximum coverage.

### 1d. Technology Fingerprinting

**If Playwright MCP is available**, load each product domain and extract:

```javascript
// Navigate
mcp__playwright__browser_navigate({ url: "https://PRODUCT_DOMAIN" })

// All external scripts
mcp__playwright__browser_evaluate({
  expression: "Array.from(document.querySelectorAll('script[src]')).map(s=>s.src).filter(u=>!u.includes(window.location.hostname))"
})

// Custom HTML elements
mcp__playwright__browser_evaluate({
  expression: "[...new Set(Array.from(document.querySelectorAll('*')).map(e=>e.tagName.toLowerCase()).filter(t=>t.includes('-')))]"
})

// Branded JS globals (last 50 — browser built-ins are first)
mcp__playwright__browser_evaluate({
  expression: "Object.keys(window).slice(-50)"
})

// Analytics IDs (GA4, GTM, UA, HubSpot, Facebook Pixel, LinkedIn)
mcp__playwright__browser_evaluate({
  expression: "document.documentElement.innerHTML.match(/G-[A-Z0-9]+|GTM-[A-Z0-9]+|UA-\\d+-\\d+|hs-scripts\\.com\\/(\\d+)|fbq\\('init',\\s*'(\\d+)'|_linkedin_partner_id\\s*=\\s*\"(\\d+)\"/g)"
})
```

**If Playwright is NOT available**, use WebFetch to fetch the page source and grep for script tags, data attributes, and analytics IDs. Note the fingerprinting gap in the report.

### 1e. DNS TXT Records

For each domain, extract TXT records to identify the company's SaaS stack:
```bash
dig DOMAIN TXT +short 2>/dev/null
```
Parse: SPF includes (email provider), DMARC, Microsoft 365 (`MS=`), Google Workspace, Atlassian, HubSpot, Bitwarden, DocuSign, Stripe, Dropbox, Palo Alto, Wiz, etc.

### 1f. Build Company Profile

Write `_recon/{target_slug}/profile.json` with the structure from section 0e. Every field must have an actual value or explicit `null`. Include:
- `target` — corporate identity
- `subsidiaries[]` — all discovered subsidiaries
- `products[]` — all products with domains
- `domains` — categorized as corporate/product/subsidiary/redirects
- `signatures` — all detection fingerprints (html_elements, js_globals, cdn_domains, tracking_endpoints, script_urls, data_attributes, file_extensions, embed_patterns)
- `analytics_ids` — GA4, GTM, HubSpot, LinkedIn, Facebook, Pendo
- `infrastructure` — DNS provider, cloud, CDN, WAF, email
- `named_customers[]` — from investor filings (if found)
- `named_partners[]` — from marketing materials (if found)

Write `_recon/{target_slug}/findings/01-company-profile.md` with human-readable summary.

### 1g. GATE CHECK — Do Not Proceed Unless:
- [ ] At least 1 product domain identified
- [ ] At least 2 detection signatures captured (or documented why signatures couldn't be extracted)
- [ ] DNS TXT records extracted for primary domains
- [ ] profile.json is valid JSON
- [ ] Subfinder ran (if available) or noted as unavailable

**If product domains found but signatures empty** (e.g., SPA that renders nothing in source, or Playwright unavailable): proceed but log a warning that embed detection in Phase 6 will be limited.

---

## 2. PHASE 2 — CERTIFICATE TRANSPARENCY

**Goal:** Query CT logs for every certificate issued to any target domain. Client-branded subdomains reveal the customer base.

Read [classification-rules.md](references/classification-rules.md) now for subdomain classification rules.

### 2a. Query crt.sh

For EVERY domain in profile.json (corporate + product + subsidiary), run:
```bash
curl -s "https://crt.sh/?q=%25.DOMAIN&output=json" 2>/dev/null
```

**Error handling:**
- If crt.sh times out (common for domains with 1000+ certs), retry once after 5 seconds
- If still failing, try with `&limit=1000`
- If the response is empty `[]`, that's valid — just means no certs found for that domain
- If the response is HTML (error page), the query failed — retry or note as gap
- Parse with `jq` if available: `jq -r '.[].name_value' | tr ',' '\n' | sort -u`
- If `jq` unavailable: `python3 -c "import sys,json; [print(x) for e in json.load(sys.stdin) for x in e.get('name_value','').split('\n')]"`

Deduplicate results across all domain queries into a single sorted list.

### 2b. Merge with Subfinder/Amass Results

If subfinder or amass ran in Phase 1, merge those subdomains with crt.sh results:
```bash
cat _recon/{target_slug}/subdomains_subfinder.txt _recon/{target_slug}/crt_domains.txt 2>/dev/null | sort -u > _recon/{target_slug}/all_subdomains.txt
```
This ensures maximum subdomain coverage — crt.sh catches certs, subfinder catches DNS records, zone transfers, and passive sources.

### 2c. Classify Subdomains

Apply rules from [classification-rules.md](references/classification-rules.md):
1. Filter out infrastructure subdomains (cdn, api, auth, portal, etc.)
2. Filter out environment-only subdomains (staging, dev, qa, etc.)
3. **Exception**: Environment subdomains containing a client name (e.g., `clientname-uat.company.com`) ARE client indicators
4. Everything remaining is a potential client — research ambiguous ones

### 2d. Client Identification

For each client-branded subdomain:
1. Parse client name from subdomain
2. Quick web search to confirm the company identity
3. Classify by industry per [classification-rules.md](references/classification-rules.md) categories
4. Note evidence level: production cert = MODERATE, production + UAT = CONFIRMED, demo only = WEAK, expired only = WEAK

### 2e. Extract Certificate Metadata

For each domain queried, record: issuer, SAN list, validity dates. Note:
- Weekly rotating certs with `CN=imperva.com` or `CN=cloudflare*` → WAF provider
- Sectigo OV certs → often contain SAN lists grouping related domains
- Let's Encrypt / cPanel AutoSSL → may contain client subdomains in bulk

Write `_recon/{target_slug}/findings/02-certificates.md`.

### 2f. IMPORTANT: Not All Companies Use Client Subdomains

If crt.sh reveals NO client-branded subdomains, the target may use:
- Shared infrastructure (all clients on same domain)
- Client-side-only embeds (no server-side client isolation)
- Randomly generated subdomain names

In this case: document that CT logs did not reveal client-specific infrastructure, and **rely more heavily on Phases 4-6** (archives, code search, embed detection) for client discovery.

### 2g. GATE CHECK:
- [ ] All domains from profile.json queried against crt.sh (or failures documented)
- [ ] Subfinder/amass results merged (if available)
- [ ] Every subdomain classified (client / infrastructure / environment / ambiguous)
- [ ] Each client assigned industry classification and confidence tier
- [ ] Certificate metadata captured for significant certs

---

## 3. PHASE 3 — DNS & INFRASTRUCTURE MAPPING

**Goal:** Resolve key subdomains, follow CNAME chains, map cloud providers, identify client deployments.

### 3a. DNS Resolution

**If `dnsx` is available (PREFERRED — much faster for bulk):**
```bash
dnsx -l _recon/{target_slug}/all_subdomains.txt -resp -cname -a -o _recon/{target_slug}/dns_results.txt
```

**Otherwise, use batched `dig`:**

**Priority 1 — Always resolve (main infrastructure):**
```bash
for sub in DOMAIN www.DOMAIN cdn.DOMAIN portal.DOMAIN api.DOMAIN auth.DOMAIN track.DOMAIN; do
  echo "=== $sub ==="
  dig +short $sub A 2>/dev/null
  dig +short $sub CNAME 2>/dev/null
done
```

**Priority 2 — Resolve all client-branded subdomains from Phase 2:**
```bash
# Batch all client subdomains into one loop
for sub in CLIENT1.DOMAIN CLIENT2.DOMAIN CLIENT3.DOMAIN; do
  cname=$(dig +short $sub CNAME 2>/dev/null | head -1)
  a=$(dig +short $sub A 2>/dev/null | head -1)
  echo "$sub|$cname|$a"
done
```

Run in a single Bash call with all subdomains in one loop. If there are 50+ client subdomains, sample the 20 most important (largest/newest certs) and note the rest as unresolved.

**Priority 3 — Environment/other subdomains:** Skip unless specifically relevant.

### 3b. CNAME Chain Analysis

Follow every CNAME from 3a. Identify cloud services per this table:

| CNAME Pattern | Provider | Service |
|--------------|----------|---------|
| `*.elb.*.amazonaws.com` | AWS | Load Balancer |
| `*.cloudfront.net` | AWS | CloudFront |
| `*.s3.amazonaws.com` | AWS | S3 |
| `*.azurewebsites.net` | Azure | App Service |
| `*.cloudapp.azure.com` | Azure | Cloud Service |
| `*.herokuapp.com` | Heroku | Platform |
| `*.netlify.app` | Netlify | Static hosting |
| `*.vercel-dns.com` | Vercel | Edge |
| `*.hscoscdn*.net` | HubSpot | CMS |
| `*.wpengine.com` | WP Engine | WordPress |
| `*.firebaseapp.com` | Google | Firebase |
| `*.run.app` | Google | Cloud Run |

**Key finding**: Client-specific CNAMEs like `clientname.azurewebsites.net` confirm a dedicated deployment and upgrade that client's confidence tier.

### 3c. Reverse IP Lookup (if Shodan CLI available)

```bash
IP=$(dig +short MAIN_DOMAIN A | head -1)
shodan host $IP 2>/dev/null
```
This reveals other domains on the same IP, open ports, and server software/versions.

### 3d. Build Infrastructure Diagram

Create an ASCII architecture diagram showing: Internet → WAF/CDN → Load Balancer → App Servers, with CDN, client deployments, and email branching off.

Write `_recon/{target_slug}/findings/03-infrastructure.md`.

### 3e. GATE CHECK:
- [ ] Core infrastructure subdomains resolved
- [ ] Client subdomains resolved (at least top 20, or all if < 50)
- [ ] CNAME chains followed and cloud providers identified
- [ ] Infrastructure diagram included in findings
- [ ] dnsx used if available (or dig batched fallback documented)

---

## 4. PHASE 4 — ARCHIVE MINING

**Goal:** Search web archives for historical evidence — CDN directory listings, client folder names, embed code, and pages that no longer exist.

### 4a. Bulk URL Collection with gau

**If `gau` is available (RECOMMENDED — queries 4 sources simultaneously):**
```bash
# Collect URLs from Wayback Machine, Common Crawl, OTX, and URLScan
for domain in DOMAIN1 DOMAIN2 DOMAIN3; do
  gau --providers wayback,commoncrawl,otx,urlscan "$domain" 2>/dev/null
done | sort -u > _recon/{target_slug}/gau_urls.txt

# Count results
echo "Total URLs collected: $(wc -l < _recon/{target_slug}/gau_urls.txt)"
```

**If `waymore` is also available (most comprehensive):**
```bash
waymore -i PRODUCT_DOMAIN -mode U -oU _recon/{target_slug}/waymore_urls.txt
```

### 4b. Wayback Machine CDX API (direct queries)

Even if gau ran, query CDX directly for CDN subdomains — these are highest priority for client discovery:
```bash
# CDN subdomain (highest priority — may expose directory listings)
curl -s "https://web.archive.org/cdx/search/cdx?url=cdn.DOMAIN/*&output=json&collapse=urlkey&fl=timestamp,original,statuscode,mimetype&limit=500"

# Client CDN
curl -s "https://web.archive.org/cdx/search/cdx?url=clients-cdn.DOMAIN/*&output=json&collapse=urlkey&limit=500"
curl -s "https://web.archive.org/cdx/search/cdx?url=clients.DOMAIN/*&output=json&collapse=urlkey&limit=500"

# All subdomains (domain match — broad sweep)
curl -s "https://web.archive.org/cdx/search/cdx?url=*.DOMAIN/*&output=json&matchType=domain&collapse=urlkey&limit=1000"
```

### 4c. Common Crawl CDX API

Query at least the **3 most recent indices**:
```bash
# Get latest 3 index IDs
INDICES=$(curl -s "https://index.commoncrawl.org/collinfo.json" | jq -r '.[0:3] | .[].id')

# Query each
for idx in $INDICES; do
  curl -s "https://index.commoncrawl.org/${idx}-index?url=*.DOMAIN&output=json" 2>/dev/null
done
```

### 4d. Mine CDN Directory Listings

Many SaaS platforms use S3 or similar with directory listings. Even if disabled now, archives often captured them:
```bash
# Check if CDN had directory listing
curl -s "https://web.archive.org/web/2024/https://cdn.DOMAIN/" | head -100

# Look for client folder names in XML listings (S3 style)
curl -s "https://web.archive.org/web/2024/https://cdn.DOMAIN/" | \
  grep -oE '<Key>[^<]+</Key>' | sed 's/<[^>]*>//g' | sort -u
```

### 4e. Analyze Collected URLs

From gau/waymore output, extract client indicators:
```bash
# Extract unique paths with potential client names
grep -oP '(?<=://)[^/]+/[^/]+' _recon/{target_slug}/gau_urls.txt | sort | uniq -c | sort -rn | head -50

# Find partner IDs, account IDs, client folder names
grep -oE '/p/[0-9]+/' _recon/{target_slug}/gau_urls.txt | sort -u
grep -oE '/accounts?/[^/]+' _recon/{target_slug}/gau_urls.txt | sort -u
grep -oE '/clients?/[^/]+' _recon/{target_slug}/gau_urls.txt | sort -u

# Look for embed code patterns
grep -i 'embed\|widget\|player\|uiconf' _recon/{target_slug}/gau_urls.txt | head -50
```

### 4f. Fetch Archived Pages for Evidence

For the most interesting archived URLs (client references, CDN listings, embed code):
```bash
# Access a specific archived page
curl -s "https://web.archive.org/web/TIMESTAMP/https://DOMAIN/path"
```

Write `_recon/{target_slug}/findings/04-archives.md`.

### 4g. GATE CHECK:
- [ ] gau ran for all domains (if available) or Wayback CDX queried directly
- [ ] Wayback CDX queried for CDN subdomains specifically
- [ ] Common Crawl queried for at least 1 recent index
- [ ] CDN directory listings checked in archives
- [ ] URL patterns analyzed for client indicators
- [ ] Findings file written

---

## 5. PHASE 5 — SOURCE CODE SEARCH

**Goal:** Find the target's domains, scripts, and brand names in public code repositories, source code indexes, and tracker databases.

### 5a. GitHub Code Search

Use `mcp__github__search_code` for each signature from profile.json. Execute ALL of these:

**Primary searches (always execute):**
```
"{PROD_DOMAIN}"
"{CDN_DOMAIN}"
"{SCRIPT_URL}"       (if embed script URL known)
"{CUSTOM_ELEMENT}"   (if custom HTML element known)
"{JS_GLOBAL}"        (if JS global known)
```

**Secondary searches (execute if primaries yield results):**
```
"{PROD_DOMAIN}" filename:*.html
"{PROD_DOMAIN}" filename:package.json
"{PROD_DOMAIN}" filename:*.jsx OR filename:*.tsx
"{COMPANY}" filename:config.json OR filename:config.yaml
```

**Repository searches:**
```
mcp__github__search_repositories("{COMPANY}")
mcp__github__search_repositories("{PRODUCT}")
```

**What to look for in results:**
- Decompiled mobile apps → deep integrations invisible on the web
- Integration examples → official or community SDK usage
- Developer portfolios → work experience at clients
- Tracker/blocklist repos → DuckDuckGo Tracker Radar, EFF Privacy Badger, uBlock, EasyList
- Security research repos → decompiled assets with embed code
- Client configuration files → partner IDs, account IDs embedded in code

### 5b. PublicWWW HTML Source Search

PublicWWW indexes the raw HTML source of millions of websites. Search via Google:
```
mcp__google-researcher-mcp__google_search('site:publicwww.com "{CDN_DOMAIN}"')
mcp__google-researcher-mcp__google_search('site:publicwww.com "{CUSTOM_ELEMENT}"')
```

Or fetch results directly:
```
WebFetch("https://publicwww.com/websites/%22{CDN_DOMAIN}%22/", "List all websites found containing this code")
WebFetch("https://publicwww.com/websites/%22{SCRIPT_URL}%22/", "List all websites found")
```

### 5c. Shodan HTTP Content Search

**If `shodan` CLI is available:**
```bash
shodan search 'http.html:"{PROD_DOMAIN}"' --limit 100
shodan search 'http.html:"{JS_GLOBAL}"' --limit 100
shodan search 'ssl:"{COMPANY_NAME}"' --limit 100
shodan search 'ssl.cert.subject.cn:"{PROD_DOMAIN}"' --limit 100
```

**If neither CLI nor MCP**, search via web:
```
mcp__google-researcher-mcp__google_search('site:shodan.io "{PROD_DOMAIN}"')
```

### 5d. Aggregated Search with uncover (if available)

```bash
uncover -q 'http.body:"{PROD_DOMAIN}"' -e shodan,publicwww,fofa -silent
```

### 5e. Tracker & Blocklist Database Search

Search for the target in privacy/tracker databases:
```
mcp__github__search_code("{PROD_DOMAIN} path:tracker-radar/domains")
mcp__github__search_code("{PROD_DOMAIN} path:APackets/yellowlist")
mcp__github__search_code("{PROD_DOMAIN} easylist OR easyprivacy")
mcp__github__search_code("{PROD_DOMAIN} path:hosts OR path:blocklist OR path:dns-blocklists")
```

Tracker databases are valuable because they reveal:
- Prevalence data (how many sites embed the target)
- Fingerprinting scores
- Cookie usage patterns
- Related domains grouped by owner

Write `_recon/{target_slug}/findings/05-code-search.md`.

### 5f. GATE CHECK:
- [ ] GitHub code search executed for all major signatures
- [ ] PublicWWW searched (or noted as gap)
- [ ] Shodan searched (if available, or noted as gap)
- [ ] Tracker databases checked
- [ ] Findings file written

---

## 6. PHASE 6 — LIVE EMBED DETECTION

**Goal:** For suspected client sites (from Phases 2-5), verify embeds using live browser inspection and batch scanning.

**IMPORTANT:** Playwright MCP is only available in the main context, NOT in background agents. This phase MUST run in the main context.

### 6a. Compile Target URLs

From Phases 2-5, gather all suspected client URLs:
- Client-branded domains that resolved to active IPs (Phase 3)
- URLs found in archives with embed artifacts (Phase 4)
- Sites found in GitHub/PublicWWW with target references (Phase 5)
- Case study / marketing mentioned customer sites

Limit to the **20 most promising** candidates.

### 6b. Playwright Browser Inspection

For each candidate URL (if Playwright MCP available):

```javascript
// Navigate
mcp__playwright__browser_navigate({ url: "https://CANDIDATE_URL" })

// Check for custom elements
mcp__playwright__browser_evaluate({
  expression: "document.querySelector('{CUSTOM_ELEMENT}') !== null"
})

// Check for JS globals
mcp__playwright__browser_evaluate({
  expression: "typeof window.{JS_GLOBAL} !== 'undefined'"
})

// Capture all network requests
mcp__playwright__browser_network_requests()
// Filter for: product domain, CDN domain, tracking endpoints

// Extract all external script sources
mcp__playwright__browser_evaluate({
  expression: "Array.from(document.querySelectorAll('script[src]')).map(s=>s.src).filter(u=>!u.includes(window.location.hostname))"
})

// Extract all iframe sources
mcp__playwright__browser_evaluate({
  expression: "Array.from(document.querySelectorAll('iframe[src]')).map(f=>f.src)"
})
```

### 6c. Batch URL Scanning with httpx (if ProjectDiscovery httpx available)

```bash
# Create URL list from candidates
echo "URL1\nURL2\n..." > _recon/{target_slug}/candidate_urls.txt

# Scan for target signatures in responses
cat _recon/{target_slug}/candidate_urls.txt | httpx \
  -match-string "{CDN_DOMAIN}" \
  -match-string "{CUSTOM_ELEMENT}" \
  -match-string "{JS_GLOBAL}" \
  -status-code -title -tech-detect -follow-redirects \
  -json -o _recon/{target_slug}/httpx_results.json
```

### 6d. Nuclei Template Scanning (if nuclei available)

Create a custom detection template:
```yaml
id: {target_slug}-embed-detect
info:
  name: {COMPANY} Embed Detection
  author: saas-recon
  severity: info
http:
  - method: GET
    path:
      - "{{BaseURL}}"
    matchers-condition: or
    matchers:
      - type: word
        words:
          - "{CUSTOM_ELEMENT}"
          - "{CDN_DOMAIN}"
          - "{JS_GLOBAL}"
          - "{SCRIPT_URL}"
        condition: or
```

Save to `_recon/{target_slug}/detect.yaml` and run:
```bash
nuclei -l _recon/{target_slug}/candidate_urls.txt -t _recon/{target_slug}/detect.yaml -o _recon/{target_slug}/nuclei_results.txt
```

### 6e. Full-Site Crawling with Katana (if available)

For the top 5 most promising client sites:
```bash
katana -u https://CLIENT_SITE -js-crawl -d 3 -ef css,png,jpg,gif -f qurl 2>/dev/null | grep -i "{PROD_DOMAIN}"
```

### 6f. WebFetch Fallback

If Playwright, httpx, nuclei, and katana are all unavailable, use WebFetch to fetch page source and search for signature strings manually.

Write `_recon/{target_slug}/findings/06-embeds.md`.

### 6g. GATE CHECK:
- [ ] Embed detection attempted on at least 10 candidate URLs
- [ ] Playwright used for top candidates (if available)
- [ ] Batch scanning used (httpx/nuclei) if available, or noted as gap
- [ ] Confirmed embeds documented with full evidence
- [ ] Findings file written

---

## 7. PHASE 7 — WEB & CONTENT SEARCH

**Goal:** Find third-party mentions, partner relationships, and customer evidence through web search.

Read [search-patterns.md](references/search-patterns.md) now. Map profile.json fields to placeholders:
- `{COMPANY}` ← `profile.target.name`
- `{PRODUCT}` ← `profile.products[0].name` (repeat for each product)
- `{CORP_DOMAIN}` ← `profile.domains.corporate[0]`
- `{PROD_DOMAIN}` ← `profile.domains.product[0]`
- `{CDN_DOMAIN}` ← `profile.signatures.cdn_domains[0]`
- `{ELEMENT}` ← `profile.signatures.html_elements[0]`
- `{SCRIPT}` ← first entry from `profile.signatures.script_urls[]`
- `{JS_GLOBAL}` ← `profile.signatures.js_globals[0]`
- `{GA_ID}` ← `profile.analytics_ids.ga4`

### 7a. Google Dorking (execute at least 10 queries)

From [search-patterns.md](references/search-patterns.md), run **all** of these:

1. `"{PRODUCT}" -site:{CORP_DOMAIN} -site:{PROD_DOMAIN}` — third-party mentions
2. `"{COMPANY}" -site:{CORP_DOMAIN}` — brand mentions
3. `"{COMPANY}" customer OR client OR "case study" -site:{CORP_DOMAIN}` — customer evidence
4. `"{PRODUCT}" "powered by" OR "built with" OR "using" -site:{CORP_DOMAIN}` — embed references
5. `"{COMPANY}" partner OR integration OR marketplace -site:{CORP_DOMAIN}` — partner pages
6. `"{SCRIPT}" -site:{PROD_DOMAIN}` — embed artifact (if script name known)
7. `"{CDN_DOMAIN}" -site:{PROD_DOMAIN}` — CDN references on third-party sites
8. `site:linkedin.com "{COMPANY}" AND ("we use" OR "experience with")` — professional mentions
9. `site:linkedin.com/jobs "{PRODUCT}" OR "{COMPANY}"` — job postings
10. `filetype:pdf "{COMPANY}" customer OR client` — PDF documents
11. `site:stackoverflow.com "{PRODUCT}" OR "{PROD_DOMAIN}"` — developer discussions
12. `site:reddit.com "{COMPANY}" OR "{PRODUCT}"` — community mentions
13. `"{COMPANY}" conference OR summit OR webinar speaker 2025 2026` — event mentions
14. `"{PRODUCT}" testimonial OR review -site:{CORP_DOMAIN} -site:g2.com -site:capterra.com` — organic reviews

### 7b. News & Press
```
mcp__google-researcher-mcp__google_news_search("{COMPANY_NAME}")
mcp__google-researcher-mcp__google_news_search("{COMPANY_NAME} partnership OR acquisition OR customer")
```

### 7c. Technology Marketplaces

Search for the target on **at least 5** of:
- **Review platforms**: G2, Capterra, TrustRadius
- **Cloud marketplaces**: AWS Marketplace, Azure Marketplace, GCP Marketplace
- **SaaS marketplaces**: Salesforce AppExchange, HubSpot Marketplace
- **App stores**: Shopify App Store, Zoom Marketplace
- **Industry-specific**: relevant niche marketplaces

### 7d. Patent & Academic Search
```
mcp__google-researcher-mcp__patent_search(assignee="{COMPANY_NAME}")
mcp__google-researcher-mcp__academic_search("{PRODUCT} {key_technology_term}")
```

### 7e. Job Posting Analysis

Search for companies OTHER than the target that mention the target's product in job postings — this confirms them as clients:
```
mcp__google-researcher-mcp__search_and_scrape('"{PRODUCT}" experience OR knowledge site:linkedin.com/jobs -{CORP_DOMAIN}')
mcp__google-researcher-mcp__google_search('site:indeed.com "{PRODUCT}" developer OR engineer')
```

### 7f. Conference & Event Appearances
```
mcp__google-researcher-mcp__google_search('"{COMPANY}" conference OR summit OR webinar speaker 2025 2026')
mcp__google-researcher-mcp__google_search('"{PRODUCT}" demo OR presentation site:youtube.com')
```

Write `_recon/{target_slug}/findings/07-web-mentions.md`.

### 7g. GATE CHECK:
- [ ] At least 10 Google dork patterns executed
- [ ] News search completed
- [ ] At least 5 marketplace/directory checks done
- [ ] Patent search attempted
- [ ] Academic search attempted
- [ ] Job posting search attempted
- [ ] Conference/event search attempted
- [ ] Findings file written

---

## 8. PHASE 8 — ANALYTICS & TRACKER CORRELATION

**Goal:** Find all websites sharing the target's analytics IDs, technology fingerprints, and tracker classification data. This phase reveals sister sites, client portals, and shared infrastructure that other techniques miss.

### 8a. Analytics ID Correlation

For EACH analytics ID found in profile.json:

**Google Analytics / GTM IDs:**
```
mcp__google-researcher-mcp__google_search('"{GA4_ID}" -site:{CORP_DOMAIN} -site:{PROD_DOMAIN}')
mcp__google-researcher-mcp__google_search('"{GTM_ID}" -site:{CORP_DOMAIN} -site:{PROD_DOMAIN}')
```

**HubSpot Portal ID:**
```
mcp__google-researcher-mcp__google_search('"hs-scripts.com/{HUBSPOT_ID}" -site:{CORP_DOMAIN}')
```

**Facebook Pixel / LinkedIn Partner ID:**
```
mcp__google-researcher-mcp__google_search('"fbq(\'init\', \'{FB_PIXEL_ID}\')" -site:{CORP_DOMAIN}')
mcp__google-researcher-mcp__google_search('"_linkedin_partner_id" "{LINKEDIN_ID}" -site:{CORP_DOMAIN}')
```

**Marketo / Marketing Automation IDs:**
```
mcp__google-researcher-mcp__google_search('"{MARKETO_MUNCHKIN_ID}" -site:{CORP_DOMAIN}')
```

### 8b. AnalyticsRelationships Tool

If available (can be cloned and run):
```bash
if [ ! -d /tmp/AnalyticsRelationships ]; then
  git clone https://github.com/Josue87/AnalyticsRelationships /tmp/AnalyticsRelationships 2>/dev/null
fi
cd /tmp/AnalyticsRelationships && python3 analyticsrelationships.py -u {CORP_DOMAIN} 2>/dev/null
```
This finds ALL domains sharing the same GA/GTM ID automatically by querying multiple sources.

### 8c. BuiltWith Technology Lookup

**Via web search:**
```
mcp__google-researcher-mcp__search_and_scrape("site:builtwith.com {PROD_DOMAIN}")
```

**Or via direct fetch:**
```
WebFetch("https://builtwith.com/{PROD_DOMAIN}", "List all technologies detected on this site and any 'sites also using' data")
```

BuiltWith reveals: all technologies on the target's site, other sites using the same tech stack, and historical technology changes.

### 8d. DuckDuckGo Tracker Radar Analysis

Check if the target's domains are classified in tracker databases:
```
mcp__github__search_code("{PROD_DOMAIN} path:APackets/APackets")
mcp__github__search_code("{PROD_DOMAIN} path:APackets/yellowlist")
mcp__github__search_code("{PROD_DOMAIN} path:APackets/yellowlist.txt")
```

Also search directly:
```
mcp__github__search_code("{PROD_DOMAIN} tracker-radar")
```

If found, extract: tracker classification, prevalence data, fingerprinting score, cookie usage, related domains.

### 8e. EFF Privacy Badger / EasyList / DNS Blocklists

```
mcp__github__search_code("{PROD_DOMAIN} easyprivacy OR easylist")
mcp__github__search_code("{PROD_DOMAIN} path:hosts OR path:blocklist")
```

DNS blocklists categorize domains by purpose and often group domains by owner — revealing additional infrastructure and product domains.

### 8f. Shared Infrastructure via Analytics

If analytics ID correlation finds other domains sharing the same IDs, those domains are either:
- **Same company**: Different product lines, regional sites, or acquired properties
- **Client portals**: White-labeled client instances sharing the parent's analytics
- **Partner sites**: Co-marketing or distribution partner pages

Investigate each shared-ID domain to classify it.

Write `_recon/{target_slug}/findings/08-analytics-correlation.md`.

### 8g. GATE CHECK:
- [ ] Analytics ID search attempted for all known IDs (or documented that none were found)
- [ ] BuiltWith lookup attempted
- [ ] Tracker database search completed (GitHub: tracker-radar, privacy-badger, easylist)
- [ ] DNS blocklist search completed
- [ ] AnalyticsRelationships tool attempted (if available)
- [ ] Findings file written

---

## 9. PHASE 9 — BUSINESS INTELLIGENCE

**Goal:** Discover named customers, revenue data, partner relationships, and market intelligence from business sources.

### 9a. Public Company Filings (if ticker found)

| Source | What You Find |
|--------|---------------|
| SEC EDGAR (US) | 10-K, 10-Q, proxy statements with customer names |
| SEDAR+ (Canada) | Canadian public company filings |
| Companies House (UK) | UK company registrations |
| Investor presentations | Named customers, ARR data, growth metrics |
| Earnings call transcripts | Customer names mentioned verbally |

Search investor relations:
```
mcp__google-researcher-mcp__search_and_scrape("{COMPANY_NAME} investor relations earnings Q4 2025")
mcp__google-researcher-mcp__search_and_scrape("site:seekingalpha.com {COMPANY_NAME} earnings call transcript")
mcp__google-researcher-mcp__google_search("{COMPANY_NAME} 10-K annual report site:sec.gov")
```

### 9b. Named Customer Extraction

From the target's own marketing materials:
```
mcp__google-researcher-mcp__search_and_scrape("site:{CORP_DOMAIN} case study OR customer story")
mcp__google-researcher-mcp__search_and_scrape("site:{CORP_DOMAIN} resources case-studies")
mcp__google-researcher-mcp__search_and_scrape("site:{CORP_DOMAIN} customers OR clients")
```

Scrape the case studies/customers page to extract ALL named customers, not just the first page.

### 9c. Conference & Event Intelligence
```
mcp__google-researcher-mcp__google_search('"{COMPANY}" conference OR summit OR webinar speaker 2025 2026')
mcp__google-researcher-mcp__google_search('"{PRODUCT}" demo OR presentation site:youtube.com')
mcp__google-researcher-mcp__google_search('"{COMPANY}" exhibitor OR sponsor')
```

### 9d. Competitor Intelligence
```
mcp__google-researcher-mcp__google_search('"{COMPANY}" vs OR versus OR alternative OR competitor')
```

### 9e. Revenue & Market Data

For public companies:
```
mcp__google-researcher-mcp__search_and_scrape("{COMPANY_NAME} annual revenue ARR customers 2025")
mcp__google-researcher-mcp__google_news_search("{COMPANY_NAME} funding OR acquisition OR partnership 2025 2026")
```

### 9f. M&A and Partnership Activity
```
mcp__google-researcher-mcp__google_news_search("{COMPANY_NAME} acquisition OR merger OR partnership")
mcp__google-researcher-mcp__search_and_scrape("{COMPANY_NAME} strategic partner OR reseller OR OEM")
```

Write `_recon/{target_slug}/findings/09-business-intel.md`.

### 9g. GATE CHECK:
- [ ] Investor filings checked (if public company, or noted as private)
- [ ] Named customers extracted from case studies
- [ ] Conference/event appearances searched
- [ ] Revenue/market data researched
- [ ] M&A / partnership activity searched
- [ ] Findings file written

---

## 10. PHASE 10 — REPORT COMPILATION

**Goal:** Compile all findings, cross-reference, generate report.

### 10a. Build Cross-Reference Matrix

Read ALL findings files (01 through 09). For each unique client found across ALL phases, build a row:

| Client | Industry | CT Cert | DNS | CDN | Code | Embed | Analytics | Filing | Press | Confidence |
|--------|----------|:-------:|:---:|:---:|:----:|:-----:|:---------:|:------:|:-----:|:----------:|

Mark each cell with `X` if evidence exists from that source. Apply confidence tier per [classification-rules.md](references/classification-rules.md) rules (NOT by simple column count — use the specific evidence-type rules defined there).

Deduplicate clients per the deduplication rules in classification-rules.md. Merge aliases.

### 10b. Compile Report

Read [report-template.md](references/report-template.md). Create `_recon/{target_slug}/report.md` following that structure exactly:
- Replace EVERY `{PLACEHOLDER}` with actual computed values
- `{COUNT}` → actual numeric count
- `{CLIENT}`, `{INDUSTRY}`, etc. → expand to as many rows as there are entries
- `{DATE}` → the date captured at the top of this skill
- Remove any section that has zero findings BUT include a note: "No findings from this source."
- Do NOT leave any `{PLACEHOLDER}` text in the final report

The report MUST include ALL 13 sections from the template:
1. Executive Summary (metrics, confidence breakdown, industry breakdown)
2. Company Profile
3. Confirmed Clients & Customers (cross-reference matrix + by-industry tables)
4. Technology Partners & Integrations
5. Infrastructure Map (IPs, CDN, DNS chains, architecture diagram)
6. Certificate Transparency Findings
7. DNS & Resolution Details
8. Archive & Code Search Findings
9. Live Embed Confirmations
10. Analytics & Tracker Correlation
11. Third-Party Mentions & Press
12. Detection Signatures (for future monitoring)
13. Methodology & Tools (every query executed, every source used)

### 10c. Render HTML

```bash
pandoc _recon/{target_slug}/report.md -f markdown -t html5 --standalone \
  --metadata title="{COMPANY_NAME} Technology Reconnaissance Report" \
  -o _recon/{target_slug}/report.html
```

If pandoc unavailable, write the HTML directly by wrapping the markdown content in a basic HTML template with the CSS from [html-styles.md](references/html-styles.md).

After generating HTML, inject the CSS from [html-styles.md](references/html-styles.md):
- Replace pandoc's default `max-width: 36em` with `max-width: 980px`
- Append the table, heading, code, and blockquote styles before `</style>`

Open in browser:
```bash
open _recon/{target_slug}/report.html
```

### 10d. FINAL VERIFICATION

You are DONE only when ALL checks pass:

**Completeness (1-9):**
1. [ ] Phase 1 complete: profile.json exists with at least 1 product domain
2. [ ] Phase 2 complete: crt.sh queried for all domains (or gaps documented)
3. [ ] Phase 3 complete: DNS resolved, CNAME chains followed, architecture diagram present
4. [ ] Phase 4 complete: archives searched (gau if available, Wayback CDX, Common Crawl, CDN listings)
5. [ ] Phase 5 complete: GitHub + PublicWWW + Shodan searched (or gaps documented)
6. [ ] Phase 6 complete: live embed detection attempted on candidate URLs
7. [ ] Phase 7 complete: 10+ dorks + news + 5+ marketplace checks executed
8. [ ] Phase 8 complete: analytics IDs + tracker databases + BuiltWith searched
9. [ ] Phase 9 complete: business intelligence researched

**Quality (10-14):**
10. [ ] Every finding has a source citation with date
11. [ ] Every client has a confidence tier assigned per classification-rules.md
12. [ ] Cross-reference matrix present with evidence columns (including Analytics column)
13. [ ] Client deduplication applied (no duplicate clients under different names)
14. [ ] No `{PLACEHOLDER}` text remains in report.md

**Output (15-17):**
15. [ ] profile.json exists and is valid JSON
16. [ ] report.md exists with all 13 sections
17. [ ] report.html rendered and opened in browser

If ANY check fails, fix it before declaring completion.

---

## 11. EXECUTION ORDER & PARALLELISM

1. Read ALL reference files listed in section 0f
2. **Run tool availability check** (section 0g) — record what is installed
3. Parse `$ARGUMENTS` — determine if company name or domain
4. Generate `target_slug` per section 0e rules
5. Create output directory: `mkdir -p _recon/{target_slug}/findings`
6. **PHASE 1** — Company profiling (main context)
   - Web research: identity, subsidiaries, products, domains
   - Subfinder / amass passive subdomain discovery (if available)
   - Technology fingerprinting (Playwright if available, WebFetch fallback)
   - Analytics ID extraction
   - DNS TXT records
   - Write profile.json + 01-company-profile.md
   - **GATE CHECK** section 1g
7. **PHASE 2** — Certificate Transparency (main context)
   - crt.sh queries for every domain in profile.json
   - Merge with subfinder/amass results
   - Classify subdomains per classification-rules.md
   - Identify clients with industry + confidence tier
   - Write 02-certificates.md
   - **GATE CHECK** section 2g
8. **PHASE 3** — DNS & Infrastructure (main context)
   - dnsx (if available) or batched dig resolution
   - CNAME chain analysis and cloud provider identification
   - Shodan reverse IP lookup (if available)
   - Architecture diagram
   - Write 03-infrastructure.md
   - **GATE CHECK** section 3e
9. **PHASES 4-9 — PARALLEL EXECUTION:**

   **Spawn Agent A — Archives (background):**
   Include in prompt: full domain list from profile.json, exact curl commands from api-endpoints.md, gau instructions (if available), CDN subdomain list, CDN directory mining technique, output path `_recon/{target_slug}/findings/04-archives.md`.
   - Phase 4: gau bulk URL collection, Wayback CDX, Common Crawl CDX, CDN directory mining, URL pattern analysis

   **Spawn Agent B — Code Search (background):**
   Include in prompt: all signatures from profile.json, all GitHub search queries from search-patterns.md, PublicWWW search instructions, Shodan queries (if CLI available), tracker database search queries, output path `_recon/{target_slug}/findings/05-code-search.md`.
   - Phase 5: GitHub code + repo search, PublicWWW, Shodan, tracker/blocklist databases

   **Spawn Agent C — Web + Analytics + Business Intel (background):**
   Include in prompt: all search pattern queries with placeholders filled from profile.json, analytics IDs, marketplace list, patent/academic search, investor filing search, output paths for `07-web-mentions.md`, `08-analytics-correlation.md`, `09-business-intel.md`.
   - Phase 7: All 14 Google dork queries, news search, 5+ marketplace checks, patent/academic, job postings, events
   - Phase 8: Analytics ID correlation, BuiltWith lookup, tracker radar analysis, DNS blocklists
   - Phase 9: Investor filings, named customer extraction, conference intel, revenue data

   **Main context — Live Embed Detection:**
   - Phase 6: Compile candidate URLs from Phases 2-3 results
   - Playwright browser inspection for top 20 candidates
   - httpx batch scanning (if PD httpx available)
   - Nuclei template scanning (if available)
   - Katana JS crawling (if available)
   - Write 06-embeds.md

10. **Wait for agents:** Collect results from Agents A, B, C. Read their output files to verify they exist and contain findings.

11. **PHASE 10** — Report compilation (main context)
    - Read all 9 findings files
    - Build cross-reference matrix with all evidence columns
    - Compile report.md from template
    - Render report.html with styling
    - Open in browser
    - **FINAL VERIFICATION** section 10d

12. Output summary to user: total clients found, confidence breakdown, top findings, report location, tools used vs. tools recommended for installation.
