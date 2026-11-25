---
name: recon-exposed-devtools
description: Exposed developer tools and debug interface detection — Webpack DevServer, React/Vue DevTools, source-map leakage, GraphiQL/GraphQL Playground, Jupyter notebooks, exposed metrics endpoints, Node.js inspector debug port, and PHP debug toolbars (Symfony Profiler, Laravel Telescope, Clockwork). Active probing requires authorization; passive detection through CT logs and subdomain patterns is safe by default.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [surface-note, command-log, redacted-evidence, finding-draft]
---

# Exposed developer tools — debug and dev interface detection

Use this skill to detect accidentally exposed developer tools, debug interfaces, and development servers in production or publicly accessible environments. Developer tools leak source code (source maps), expose internal state (debug bars, profilers), provide interactive code execution (Jupyter, GraphiQL, Node.js inspector), and reveal configuration details (phpinfo, health endpoints). Active probing requires authorization and scope validation — each HTTP request contacts the target. Passive discovery from subdomain names, CT logs, and search engines is safe and should precede active probing.

## Required inputs

- Target domain and any known subdomains.
- Scope file authorizing active HTTP probing of the target's web endpoints.
- Authorization cache for the target before any active probe.
- Rate limits: send at most 2 requests/second to avoid triggering WAF or rate-limit defenses. Space requests across endpoints.
- Evidence goal: list of exposed dev surfaces with risk classification, content summary for confirmed exposures, and remediation recommendations.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` to load authorized target URLs and any exclusion paths (e.g., "do not probe /api/health").
3. `pentest_agent_validate_target` for every endpoint before probing.
4. `pentest_agent_check_authorization` before any active HTTP request.
5. `pentest_agent_build_command` for dry-run preview of curl or nuclei commands.
6. `pentest_agent_execute_tool` for all execution — rate-limit enforcement, bounded output.
7. `pentest_agent_append_evidence` with finding details and HTTP response evidence.

## Workflow

### Phase 1 — passive endpoint candidate discovery

Build a candidate list of potential dev/debug endpoints from subdomain patterns, known URL paths, and search-engine results. No active contact in this phase.

1. Subdomain pattern matching (from existing subdomain enumeration data):
   - `grep -iE "dev\.|debug\.|test\.|staging\.|sandbox\.|beta\.|internal\.|admin\.|manage\." all_subdomains.txt > devtool_subdomains.txt`
   - These subdomains are more likely to run development servers with debug tooling enabled.
2. Known development-server port patterns:
   - Next.js dev server: port 3000. Create React App: port 3000. Vite: port 5173. Angular: port 4200. Flask dev: port 5000. Django dev: port 8000. Rails: port 3000. Express generic: port 3000/8080.
   - While port scanning is out of scope for this skill, note these ports for targeted probe if the target uses non-standard HTTP ports.
3. Search-engine dorks (passive, already covered in `recon-dorking`):
   - `site:TARGET.COM inurl:phpinfo OR inurl:info.php OR inurl:test.php`
   - `site:TARGET.COM inurl:"/debug" OR inurl:"/__debug__" OR inurl:"/sockjs-node"`
   - Use results from `recon-dorking` evidence as candidate endpoints.

### Phase 2 — known debug endpoint probe

Probe a curated list of common debug/dev paths on each target URL. Use HTTP HEAD first to minimize data transfer; follow up with GET only if HEAD indicates a non-404 response.

1. Debug and dev endpoint list (curated, non-exhaustive — add target-specific paths based on technology stack fingerprinting):
   - **General debug**: `/debug`, `/__debug__`, `/debug/`, `/_debug`, `/dev`, `/dev/`, `/test`, `/test/`
   - **Webpack DevServer**: `/webpack-dev-server`, `/__webpack_dev_server__`, `/__webpack_hmr`, `/sockjs-node`, `/sockjs-node/info`
   - **React DevTools**: `/__react-devtools-hook__`
   - **GraphQL IDEs**: `/graphiql`, `/graphql-playground`, `/playground`, `/graphql`, `/_/graphql`
   - **Health/metrics endpoints**: `/__health`, `/_health`, `/health`, `/healthz`, `/readyz`, `/status`, `/metrics`, `/actuator/health`, `/actuator/metrics` (Spring Boot), `/_status` (Django)
   - **PHP info/debug**: `/phpinfo.php`, `/info.php`, `/test.php`, `/_profiler`, `/_profiler/phpinfo` (Symfony), `/telescope`, `/telescope/requests` (Laravel), `/horizon`, `/horizon/dashboard` (Laravel), `/__clockwork`, `/clockwork/` (PHP Clockwork)
   - **Node.js debug**: `/_node_debug`, `/json` (Node.js inspector on port 9229)
   - **Jupyter/data tools**: `/jupyter`, `/lab`, `/tree`, `/notebooks`, `/api/contents`
   - **Infrastructure dashboards**: `/kibana`, `/elastic`, `/_plugin/kibana`, `/grafana`, `/portainer`, `/_dashboards`
2. Probe method:
   - `STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET$ENDPOINT" --max-time 5 --connect-timeout 3)`
   - If STATUS != 404 (or 403 for protected endpoints): the endpoint exists. Record status code, response size, and any `Server` or `X-Powered-By` headers from a follow-up HEAD request.
   - If STATUS == 200: fetch the response body (first 2 KB only): `curl -s "$TARGET$ENDPOINT" --max-time 5 | head -c 2048`
3. For each non-404 response: record endpoint URL, HTTP status, response snippet (first 500 chars, redacted), and initial assessment.

### Phase 3 — source-map detection and extraction

Source maps (`*.js.map` files) map minified production JavaScript back to the original source code. When exposed, they reveal full original source with comments, developer notes, internal API endpoints, and logic.

1. Collect JavaScript URLs from the target's HTML pages:
   - `curl -s "$TARGET" | grep -oE 'src="[^"]+\.js"' | sed 's/src="//;s/"//' > js_urls.txt`
   - Also check common bundle paths: `/static/js/main.*.js`, `/build/static/js/main.*.js`, `/_next/static/chunks/*.js`
2. For each JS URL, check if a source map exists:
   - Source maps are typically referenced by a `//# sourceMappingURL=<file>.js.map` comment at the END of the JS file.
   - If the JS file itself ends with `.map` (e.g., `main.abc123.js.map`), that's the source map directly.
   - Fetch the last 500 bytes of each JS file: `curl -s "$JS_URL" | tail -c 500 | grep "sourceMappingURL"`
   - If a sourceMappingURL is found, fetch the source map: `curl -s "${JS_URL}.map" --max-time 10 | head -c 4096`
3. Source map content analysis:
   - The `.sources` array lists all original source files: `jq '.sources[]' 2>/dev/null`
   - The `.sourcesContent` array contains the FULL original source code for each file.
   - Extract source file names and content snippets: `jq '[.sources, (.sourcesContent[] | .[0:200])]' 2>/dev/null | head -100`
   - Flag: any source file containing `TODO`, `FIXME`, `HACK`, `password`, `secret`, `token`, `api_key`, `key`, `admin`, or hardcoded internal hostnames.
4. Source-map exposure is a HIGH finding — it exposes the complete application source code. Record the source-map URL, number of source files exposed, and any secrets or internal details discovered in the source.

### Phase 4 — Jupyter, data-science, and interactive tools

Detect exposed data-science and analytics tools that may allow code execution or data access.

1. Jupyter notebook detection:
   - Probe `/jupyter`, `/lab`, `/tree`, `/notebooks`, `/api/contents` on target URLs and on common ports (8888, 8889).
   - Jupyter returns JSON from `/api/contents` when authenticated or when no auth is configured: `curl -s "$TARGET:8888/api/contents" --max-time 5 | jq '.content[]?.name' 2>/dev/null`
   - If Jupyter is exposed and unauthenticated, the attacker can execute arbitrary Python code, access the server filesystem, and potentially pivot to internal networks. CRITICAL finding.
2. Grafana detection:
   - Probe `/grafana`, `/`, `/api/health` on port 3000.
   - `curl -s "$TARGET:3000/api/health" --max-time 5 | jq '.commit, .version' 2>/dev/null`
   - Check for default credentials: `curl -s -u admin:admin "$TARGET:3000/api/org" --max-time 5 | jq '.name' 2>/dev/null`
   - Flag if Grafana allows anonymous access or default credentials. HIGH finding.
3. Kibana detection:
   - Probe `/kibana`, `/_plugin/kibana`, `/` on port 5601.
   - `curl -s "$TARGET:5601/api/status" --max-time 5 | jq '.version.number, .status.overall.state' 2>/dev/null`
   - Exposed Kibana provides Elasticsearch query access. HIGH finding if unauthenticated.
4. Node.js inspector detection:
   - Probe port 9229 (Node.js debugger default): `curl -s "$TARGET:9229/json" --max-time 5 | jq '.[] | {title: .title, url: .url, webSocketDebuggerUrl: .webSocketDebuggerUrl}' 2>/dev/null`
   - The Node.js inspector allows attaching a Chrome DevTools debugger for full runtime introspection and code execution. CRITICAL finding.

### Phase 5 — PHP and framework-specific debug toolbars

Detect server-side debug toolbars that leak internal state in production.

1. Symfony Profiler (`/_profiler`):
   - `curl -s "$TARGET/_profiler/" --max-time 5 | grep -i "symfony\|profiler\|token"`
   - If the profiler is accessible, it shows request details, database queries, configuration, and environment variables for recent requests.
2. Laravel Telescope (`/telescope`):
   - `curl -s "$TARGET/telescope/requests" --max-time 5 | grep -i "telescope\|laravel"`
   - Telescope exposes all application events: requests, database queries, queued jobs, mail, notifications, cache operations.
3. Laravel Horizon (`/horizon`):
   - `curl -s "$TARGET/horizon/dashboard" --max-time 5 | grep -i "horizon\|laravel"`
   - Horizon shows queued job metrics and configuration.
4. PHP Clockwork (`/__clockwork`):
   - `curl -s "$TARGET/__clockwork/" --max-time 5 | jq '.' 2>/dev/null | head -30`
   - Clockwork returns JSON profiling data for the most recent request.
5. Django Debug Toolbar:
   - Check response headers for `X-Django-Debug-Toolbar` or probe `/_debug_toolbar/`.
6. For any exposed debug toolbar: this is a HIGH finding. The toolbar exposes internal application state, database queries, configuration values, and potentially session data.

### Phase 6 — nuclei automated devtool scanning

Use nuclei templates to automate detection of common devtool exposures.

1. Run nuclei with dev/debug related templates:
   - `nuclei -t http/exposures/ -t http/misconfiguration/ -u TARGET_URLS.txt -o nuclei_devtools_results.txt`
   - Relevant template categories: `exposed-panels`, `debug-endpoints`, `devtools-detection`, `phpinfo`, `sourcemap`, `graphql`, `jupyter`.
2. Review and verify nuclei findings manually. Nuclei may detect generic patterns that are false positives — confirm each with a manual curl request.
3. Document verified findings with nuclei template name, matched URL, and manual verification note.

## Decision points

- **Source map exposes API keys or credentials**: CRITICAL finding. Immediately flag for the engagement lead. The exposed keys should be rotated by the target. Do NOT store the raw source-map content in evidence — store only the source-map URL, file count, and a summary of what was exposed.
- **Jupyter notebook is exposed without authentication**: CRITICAL finding. Do NOT execute code or browse the filesystem beyond the initial probe that confirmed exposure. Document the finding.
- **Node.js inspector debug port (9229) is publicly accessible**: CRITICAL finding. The debugger allows full runtime introspection and potential remote code execution. Do NOT attach a debugger — document the open port and the `/json` endpoint response.
- **Debug toolbar is behind authentication (HTTP 401/403)**: downgrade finding to INFO or LOW. The toolbar exists but is protected. Probe for authentication bypass separately (hand off to `auth-workflow`).
- **Endpoint returns 200 but content is not a devtool (e.g., `/debug` serves a customer-facing debug information page)**: false positive. Record as benign. The path exists but is not a developer tool.

## Prohibited behavior

- Executing code, queries, or commands through exposed interactive tools (Jupyter, GraphiQL, Node.js inspector, Kibana console).
- Downloading, storing, or distributing source-map content beyond the minimum needed to confirm exposure (file names + snippets only).
- Using discovered credentials or API keys to authenticate to any service.
- Attempting to exploit discovered dev tools for persistent access.
- Brute-forcing debug paths at high volume — probe rate must stay ≤ 2 requests/second across all endpoints.

## Stop conditions

- Source map reveals an active API key or credential → stop probing that JS file. Flag as CRITICAL. Do not enumerate further source maps looking for more secrets — the finding is already critical.
- Jupyter or interactive tool returns 200 with content confirming unauthenticated access → stop probing that tool. Record the finding. Do not interact further.
- Endpoint returns 429 (rate limited) → stop all probing for 60 seconds. Reduce request rate, resume.
- Target returns a legal warning or "this system is monitored" message → stop all probing. Document the warning. Escalate to engagement lead.

## Evidence

For each confirmed devtool exposure, record: URL, HTTP status, response snippet (first 500 chars, redacted), tool type identification, exposure severity, and remediation recommendation. Evidence template:

```text
Devtool exposure recon for: TARGET.COM

Source maps:
  https://TARGET.COM/static/js/main.abc123.js.map → 200 OK, 847 KB
    Sources: 23 files (App.js, config.js, api.js, utils.js, secrets.js, ...)
    secrets.js snippet: "const API_KEY = '[REDACTED]'; const INTERNAL_API = 'https://internal-api.TARGET.COM/v2/'"
    → [CRITICAL] Source map exposes complete application source AND hardcoded API key AND internal API endpoint.
    → [HIGH] Internal hostname disclosed: internal-api.TARGET.COM.

GraphQL IDE:
  https://TARGET.COM/graphiql → 200 OK
    → GraphiQL interactive IDE accessible without authentication. Schema introspection available.
    → [HIGH] GraphQL introspection exposes full API schema. Query execution may be possible.

PHP debug:
  https://TARGET.COM/_profiler/ → 200 OK
    Symfony Profiler index page showing recent request tokens (5 entries visible).
    → [HIGH] Symfony Profiler exposes recent request details including DB queries, config, and env vars.

Jupyter:
  https://dev.TARGET.COM:8888/api/contents → 200 OK
    Contents: ["data_analysis.ipynb", "credentials.py", "customer_export.csv", "Untitled.ipynb"]
    → [CRITICAL] Unauthenticated Jupyter notebook server. File listing shows potential data exposure.
    → "credentials.py" filename suggests stored credentials.

Nuclei verification:
  nuclei -t http/exposures/ → 2 verified, 1 false positive (excluded)
    Verified: exposed-graphql, exposed-sourcemap (both confirmed manually).
```

Redact: all API keys, tokens, credentials, internal hostnames (unless already known from scope), source code snippets beyond file names, and `credentials.py` or similar sensitive file contents. Store only file names and exposure confirmation, not the actual data.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed exposure: source maps, GraphQL IDEs, Jupyter servers, debug toolbars, and Node.js inspectors. Classify by severity based on exposure type: source map with secrets = CRITICAL, unauthenticated Jupyter = CRITICAL, source map without secrets = HIGH, debug toolbar = HIGH, GraphQL IDE with introspection = HIGH, phpinfo = MEDIUM, directory listing = MEDIUM.
2. Package findings with: URL, tool type, exposure description (what is exposed and why it matters), HTTP response evidence summary, and remediation recommendation.
3. Recommend: disable source-map generation in production builds, restrict debug toolbars to development environments only (via IP whitelist or environment check), add authentication to all admin/debug interfaces, remove phpinfo and test pages from production, and configure the web server to return 404 for dev paths instead of exposing them.
4. Explicitly note: all probes were rate-limited, no code was executed through exposed tools, no data was exfiltrated beyond initial exposure confirmation, and no credentials were used or stored.
