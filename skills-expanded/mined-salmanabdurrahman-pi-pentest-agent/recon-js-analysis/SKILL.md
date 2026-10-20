---
name: recon-js-analysis
description: Client-side JavaScript review for API endpoints, internal hostnames, framework routing tables, environment configs, and exposure clues — passive collection of JS bundles with static analysis for architecture discovery. Framework-aware (React, Vue, Angular, Next.js, Svelte). Every JS file download must be scope-validated.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [js-notes, endpoint-list, secret-sighting, redacted-evidence, hypothesis-queue]
---

# JavaScript analysis — architectural discovery from client-side bundles

Use this skill to extract architectural intelligence from client-side JavaScript: API endpoints, internal hostnames, framework routing tables, environment configuration, third-party integrations, and exposure signals. Modern SPAs ship their entire routing table, API client configuration, and often environment-specific variables inside minified bundles. This is passive analysis — downloading JS files is a normal HTTP GET request that browsers make constantly. However, every download must be scope-validated and rate-limited.

## Required inputs

- List of in-scope URLs or subdomains with live HTTP services (from `recon-web-surface`, `recon-subdomain`, or `recon-archive-urls`).
- Scope file with authorized hosts and any restrictions on JS file collection.
- Rate limits for JS file downloads (default: max 5 concurrent, no more than 10 files per host).
- Optional: authentication credentials for JS behind login (session token, not hardcoded).

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before any downloads.
2. `pentest_agent_parse_scope` to validate every host before downloading JS.
3. `pentest_agent_validate_target` for each host.
4. `pentest_agent_check_authorization` is conditional — downloading a publicly accessible JS file is passive and does not constitute active testing. If the JS file requires authentication, authorization is required.
5. `pentest_agent_build_command` for dry-run argv preview of curl, httpx, or browser-automation downloads.
6. `pentest_agent_append_evidence` with source URL, file hash, and analysis findings.

## Workflow

### Phase 1 — JS file collection

Collect JavaScript files from target hosts through multiple channels.

1. **Extract JS URLs from archive data** (if `recon-archive-urls` ran):
   - `grep -iE '\.js(\?|$)' archive_urls.txt | sort -u > js_archive_urls.txt`
   - Archive-sourced JS files reveal historical endpoints that may no longer be linked from the live site but whose APIs may still be active.
2. **Scrape JS from live pages**:
   - For each target URL, extract `<script src="...">` and inline `<script>` blocks.
   - `curl -s "https://TARGET.COM" | grep -oP '(?<=src=")[^"]*\.js[^"]*' | sort -u`
   - Also check for dynamic imports: `import(`, `require(`, webpack chunk loading.
   - Also check for `<link rel="preload" as="script" href="...">` and `<link rel="modulepreload" href="...">`.
3. **Scrape JS from sitemap and robots.txt**:
   - Check if sitemap XML files reference JS: `curl -s "https://TARGET.COM/sitemap.xml" | grep -i '\.js'`
   - Some sitemaps reference JavaScript-rendered pages.
4. **Download each JS file**:
   - `curl -s "https://TARGET.COM/js/main.abc123.js" -o js_files/TARGET_COM_main.abc123.js`
   - Record: source URL, file size, HTTP response headers (Content-Type, ETag, Last-Modified, Cache-Control).
   - Skip files larger than 5 MB — heavily bundled JS is difficult to analyze and unlikely to be hand-written code. Flag for manual review.
5. **Source map check**:
   - For each JS file ending in `.js`, check if a source map exists: append `.map` and request.
   - `curl -s "https://TARGET.COM/js/main.abc123.js.map" -o js_maps/TARGET_COM_main.abc123.js.map`
   - If the source map is accessible: CRITICAL finding. Source maps contain the original unminified source code, including comments, variable names, and sometimes environment-specific configuration. Stop further analysis of the minified file — analyze the source map instead.

### Phase 2 — endpoint and routing extraction

Extract API endpoints, URL patterns, and framework route definitions from downloaded JS.

1. **Generic URL pattern extraction**:
   - `grep -oP '"(?:https?://[^"]*|/api/[^"]*|/v[0-9]+/[^"]*|/graphql[^"]*|/rest/[^"]*|/ws/[^"]*)"' js_files/*.js | sort -u > extracted_urls.txt`
   - Also match single-quoted strings: `grep -oP "'(?:https?://[^']*|/api/[^']*|/v[0-9]+/[^']*|/graphql[^']*|/rest/[^']*|/ws/[^']*)"' js_files/*.js | sort -u`
   - Also match template literals (backtick-delimited): ``grep -oP '`(?:https?://[^`]*|/api/[^`]*|/v[0-9]+/[^`]*|/graphql[^`]*|/rest/[^`]*|/ws/[^`]*)`' js_files/*.js | sort -u``
2. **Fetch/XHR/axios call extraction**:
   - `grep -oP '(?:fetch|axios\.(?:get|post|put|delete|patch)|XMLHttpRequest)\s*\(?\s*["\x60]([^"'\x60]+)["\x60]' js_files/*.js | sort -u > api_calls.txt`
   - These are programmatic API calls — the most reliable source of endpoint intelligence.
3. **Framework-specific routing extraction**:
   - **React Router**: `grep -oP '<Route\s+path=["\x60]([^"*\x60]+)' js_files/*.js | sort -u`
   - **React Router v6**: `grep -oP 'path:\s*["\x60]([^"*\x60]+)' js_files/*.js | sort -u`
   - **Vue Router**: `grep -oP 'path:\s*["\x60](/[^"\x60]*)["\x60]' js_files/*.js | sort -u`
   - **Angular**: `grep -oP '(?:path|loadChildren|redirectTo):\s*["\x60]([^"\x60]+)["\x60]' js_files/*.js | sort -u`
   - **Next.js**: look for `pathname` references and `useRouter` patterns.
   - **SvelteKit**: look for route parameter patterns like `[slug]`.
   - **Sapper**: look for `routes/` patterns in bundled code.
   - **Nuxt.js**: look for `router` configuration objects.
4. **Internal hostname extraction**:
   - `grep -oP '(?:[a-zA-Z0-9-]+\.(?:internal|local|corp|lan|priv|infra|intra|dmz|lab|dev|staging|test))' js_files/*.js | sort -u > internal_hostnames.txt`
   - These are hostnames referencing internal infrastructure that may not be publicly accessible but reveal naming conventions and potential targets.
   - Also extract private IP patterns: `grep -oP '(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})' js_files/*.js | sort -u > internal_ips.txt`

### Phase 3 — environment configuration discovery

Detect environment variables, API keys, and configuration objects leaked into client-side bundles.

1. **Environment variable prefixes**:
   - `grep -oP '(?:REACT_APP_|NEXT_PUBLIC_|VITE_|VUE_APP_|NUXT_ENV_|GATSBY_|ANGULAR_APP_|SVELTE_APP_)\w+' js_files/*.js | sort -u > env_vars.txt`
   - These are intentionally public — they are build-time injected. But they reveal feature flags, API base URLs, and third-party service keys that map the target's architecture.
2. **Base URL and API host configuration**:
   - `grep -oP '(?:apiUrl|baseUrl|API_URL|BASE_URL|API_HOST|backendUrl|graphqlUrl|GRAPHQL_URL|serverUrl)\s*[:=]\s*["\x60]([^"\x60]+)["\x60]' js_files/*.js | sort -u > api_config.txt`
   - This reveals the backend API hostname, which may be different from the frontend hostname — a backend not previously discovered.
3. **Feature flag extraction**:
   - `grep -oP '(?:featureFlag|FEATURE_|FLAG_|ENABLE_|DISABLE_)\w+' js_files/*.js | sort -u > feature_flags.txt`
   - Feature flags reveal unreleased functionality, admin-only features, and debug modes.
4. **Third-party service IDs**:
   - Google Analytics: `grep -oP 'UA-\d+-\d+|G-[A-Z0-9]+' js_files/*.js`
   - Google Tag Manager: `grep -oP 'GTM-[A-Z0-9]+' js_files/*.js`
   - Stripe: `grep -oP 'pk_(?:live|test)_[A-Za-z0-9]+' js_files/*.js`
   - Mapbox: `grep -oP 'pk\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+' js_files/*.js`
   - Sentry: `grep -oP 'https://[a-f0-9]+@sentry\.io/\d+' js_files/*.js`
   - These are public IDs, not secrets, but they confirm third-party integrations.

### Phase 4 — chunk and bundle analysis

Understand the application's module architecture through webpack/bundle analysis.

1. **Webpack chunk map detection**:
   - Look for `webpackChunkName` comments: `grep -oP 'webpackChunkName:\s*"([^"]+)"' js_files/*.js`
   - These reveal the application's code-splitting structure — each chunk name is a feature or page.
2. **Lazy-load route detection**:
   - `grep -oP '(?:lazy|import)\s*\(\s*["\x60]([^"\x60]+)["\x60]' js_files/*.js | sort -u`
   - Lazy-loaded modules point to additional JS files to download and analyze.
3. **Vendor/library detection**:
   - Check for known library signatures: `grep -oP '(?:node_modules|webpack|react|vue|angular|svelte|d3|three|moment|lodash|jquery)' js_files/*.js | sort | uniq -c`
   - This confirms the framework and library versions detected in `recon-web-surface`.

## Decision points

- **Source map accessible**: CRITICAL finding. Stop minified-file analysis. Download and analyze the source map (unminified code with full comments, variable names, and environment data).
- **Backend API hostname discovered that differs from frontend**: new target asset. Validate through scope, then hand off to `recon-web-surface` for fingerprinting.
- **Internal hostname or private IP in JS**: confirms internal infrastructure naming. Do not probe the IP/hostname unless scope explicitly includes internal network assessment. Flag as INFO finding.
- **Stripe publishable key, Mapbox token, Sentry DSN in JS**: these are public by design and not a vulnerability. Do not flag as secret exposure. Flag as third-party integration mapping.
- **JavaScript file is >5 MB or heavily obfuscated**: skip automated analysis, flag for manual review. Obfuscation scripts (e.g., `javascript-obfuscator`) are common in pharma, gambling, and anti-bot industries — they are not necessarily malicious.

## Prohibited behavior

- Executing JavaScript in a browser or Node.js runtime without sandboxing — static analysis only.
- Running extracted API endpoints or probing discovered services — hand off to active skills.
- Downloading JS from out-of-scope hosts.
- Storing source maps or unminified code in plain-text evidence if they contain secrets — redact first.
- Deobfuscating or reversing JavaScript beyond static pattern extraction — if deeper RE is needed, hand off to `re-static`.
- Automating JS downloads at rates that could trigger WAF/rate-limiting.

## Stop conditions

- All JS files hosted on a third-party CDN (e.g., `cdn.jsdelivr.net`, `unpkg.com`) and not on the target's domain → limited architectural insight. Document external dependency mapping and stop.
- Source map reveals full unminified source → stop minified analysis, pivot to source map review.
- JS is heavily obfuscated and automated pattern extraction yields no results → flag for manual RE.
- WAF blocks JS file downloads or rate-limits requests → stop, document WAF behavior.

## Evidence

For each analyzed host, record: JS file inventory (URLs, sizes, hashes), extracted endpoints, framework routes, internal hostnames/IPs, environment configuration keys, third-party integrations, source map status, and webpack chunk structure. Evidence template:

```text
JS analysis for: TARGET.COM
Files analyzed: 24 JS files, 3 source maps discovered (2 accessible)
Total size: 12.4 MB

Endpoints extracted: 487 unique API paths
  - /api/v1/users: 12 references
  - /api/v1/products: 8 references  
  - /api/v2/auth/login: 3 references (v2 API — possible legacy v1)
  - /graphql: 5 references
  - /api/internal/health: 1 reference (internal health endpoint in public JS)

Framework routes (React Router):
  - /dashboard, /dashboard/settings, /dashboard/billing
  - /admin (lazy-loaded chunk: "admin-panel")
  - /profile/:id, /user/:username

Internal hostnames discovered:
  - api-internal.TARGET.local (referenced in Axios baseURL config)
  - dev-db.TARGET.corp (referenced in a comment, possibly left by developer)

Source maps accessible:
  - main.abc123.js.map: YES [CRITICAL] — full unminified source with developer comments
  - dashboard.def456.js.map: YES [CRITICAL]
  - vendor.ghi789.js.map: NO (404)

Environment config:
  - REACT_APP_API_URL: https://api.TARGET.COM (matches public API)
  - REACT_APP_FEATURE_NEW_CHECKOUT: true (feature flag — new checkout flow active)
  - REACT_APP_SENTRY_DSN: https://abc123@sentry.io/12345

Third-party integrations:
  - Google Analytics: G-XXXXXXXXXX
  - Stripe (publishable): pk_live_XXXXXXXXXX
  - Sentry: confirmed
  - Intercom: confirmed
```

Redact API keys (these should be in Phase 3 of `recon-js-secrets`, but if spotted here, redact immediately). Redact any user data or PII in code comments. Never store source maps containing secrets or internal hostnames in cleartext evidence.

## Report handoff

1. Hand off extracted endpoints to `recon-js-endpoints` for validation and deduplication.
2. Hand off API base URLs and backend hostnames to `enum-api-surface`.
3. Flag source-map accessibility as a CRITICAL finding — route to `vuln-sensitive-exposure`.
4. Hand off internal hostname discoveries to `internal-network-assessment` if within scope.
5. Package the endpoint list as structured JSON for consumption by `enum-api-surface`, `vuln-sqli`, `vuln-xss`, `vuln-ssrf`, and other validation skills.
6. Explicitly note: all JS files were downloaded through standard HTTP GET requests, no browser automation or script execution was performed, no discovered endpoints were probed, and all files were scope-validated before download.
