---
name: scan-fase-0
description: Execute FASE 0 - Backend Detection. Identifies backend type (Supabase, Firebase, Custom API) and extracts relevant configurations. This phase determines the scan path for all subsequent phases. Invoke with /scan-fase-0 {url}.
---

# FASE 0: Backend Detection

Identify the backend technology and extract configurations. This phase is **MANDATORY** and determines which subsequent phases apply.

## Purpose

- Detect backend type (Supabase, Firebase, MongoDB, Custom API, GraphQL)
- Extract relevant configurations (URLs, keys, project IDs)
- Determine scan path (which phases to execute)

## Invocation

```
/scan-fase-0 {target_url}
```

**Example:** `/scan-fase-0 https://myapp.com`

## Output

This skill returns structured YAML results for `/scan-write` to log.

**Output format:**
```yaml
FASE_0_RESULTS:
  # METADATA
  target_url: "{url}"
  scan_timestamp: "{ISO 8601: 2026-01-24T14:30:00Z}"
  status: "{completed|partial|blocked}"
  status_reason: "{only if partial/blocked}"

  # DETECTION RESULTS
  backend_detected:
    type: "{supabase|firebase|custom_api|graphql|unknown}"
    confidence: "{high|medium|low}"
    evidence: "{how detected}"

  configs_extracted:
    supabase_url: "{url or null}"
    supabase_anon_key: "{key or null}"
    firebase_config: "{object or null}"
    api_base_url: "{url or null}"
    graphql_endpoint: "{url or null}"
    project_id: "{id or null}"
    source: "{where configs were found}"

  scan_path:
    - "{list of phases to execute based on backend type}"

  secure_findings:
    - test: "{what was tested}"
      result: "SECURE"
      evidence: "{proof}"

  tests_skipped:
    - test: "{test name}"
      reason: "{why skipped}"
      recommendation: "{how to enable}"
```

---

## Execution Steps

### Step 0.1: Navigate and Analyze

1. Navigate to target URL using Playwright
2. Wait for full page load (including JS execution)
3. Capture initial network requests

### Step 0.2: Check for Supabase

**Detection patterns:**

```javascript
// In HTML/JS source
https://[a-z0-9]+\.supabase\.co

// In window object
window.supabase
window.__SUPABASE__

// In network requests
*.supabase.co/rest/v1/*
*.supabase.co/auth/v1/*
*.supabase.co/storage/v1/*
```

**Extract if found:**
- Supabase URL: `https://{project}.supabase.co`
- Anon Key: `eyJ...` (JWT format)
- Project ID: from URL

**Verification:**
```bash
curl -I "https://{project}.supabase.co/rest/v1/" -H "apikey: {anon_key}"
# 200 = confirmed Supabase
```

### Step 0.3: Check for Firebase

**Detection patterns:**

```javascript
// In HTML/JS source
firebaseConfig
firebase.initializeApp
firebaseio.com
firestore.googleapis.com

// In window object
window.firebase
window.__FIREBASE__
```

**Extract if found:**
- apiKey
- projectId
- storageBucket
- authDomain
- messagingSenderId
- appId

### Step 0.4: Check for AWS Amplify

**Detection patterns:**

```javascript
// In HTML/JS source
Amplify.configure
aws-amplify
@aws-amplify/

// URL patterns
*.execute-api.*.amazonaws.com
*.amplifyapp.com
*.cloudfront.net

// Config keys
aws_project_region
aws_cognito_identity_pool_id
aws_user_pools_id
```

**Extract if found:**
- API Gateway URL
- Cognito Pool IDs
- AppSync endpoint
- Region

### Step 0.5: Check for Hasura

**Detection patterns:**

```javascript
// Endpoints
/v1/graphql
*.hasura.app

// Headers in requests
X-Hasura-Admin-Secret
X-Hasura-Role
```

**Verification:**
```bash
curl -s -X POST "{url}/v1/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __typename }"}'
# Check response for Hasura indicators
```

### Step 0.6: Check for Appwrite

**Detection patterns:**

```javascript
// URLs
*.appwrite.io
/v1/account
/v1/databases

// SDK
appwrite
new Client()

// Headers
X-Appwrite-Project
```

**Extract if found:**
- Appwrite endpoint
- Project ID

### Step 0.7: Check for Pocketbase

**Detection patterns:**

```javascript
// Endpoints
/api/collections
/api/admins
/_pb/

// SDK
PocketBase
new PocketBase(
```

**Verification:**
```bash
curl -s "{url}/api/health"
# Check for Pocketbase response
```

### Step 0.8: Check for Nhost

**Detection patterns:**

```javascript
// URLs
*.nhost.run
*.hasura.nhost.run

// SDK
@nhost/nhost-js
NhostClient
```

### Step 0.9: Check for Custom API

**Detection patterns:**

```javascript
// API endpoint patterns
/api/*
/v1/*
/v2/*
https://api.{domain}/*

// Auth patterns
Authorization: Bearer
X-API-Key
X-Auth-Token

// Common frameworks
X-Powered-By: Express
X-Powered-By: Django
X-Powered-By: FastAPI
```

**Extract if found:**
- API base URL
- Auth mechanism
- Framework hints

### Step 0.10: Check for GraphQL

**Detection patterns:**

```javascript
// Endpoints
/graphql
/graphql/v1
/api/graphql

// In requests
query {
mutation {
__schema
```

**Verification:**
```bash
curl -X POST "{url}/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __typename }"}'
# Response with data = GraphQL confirmed
```

### Step 0.11: Application Subdomain Discovery

**CRITICAL: Many apps split marketing site and application into separate subdomains.** The marketing site (e.g., `example.com`) may be a static site (Framer, Webflow, WordPress) with no backend, while the real application lives on `app.example.com`, `api.example.com`, or similar.

**This step MUST run before determining the scan path.**

#### 11.1 - Probe Common Application Subdomains

```bash
DOMAIN="{extracted_domain}"

# Common app subdomain patterns
APP_SUBDOMAINS=(
  "app.${DOMAIN}"
  "api.${DOMAIN}"
  "admin.${DOMAIN}"
  "dashboard.${DOMAIN}"
  "portal.${DOMAIN}"
  "my.${DOMAIN}"
  "platform.${DOMAIN}"
  "console.${DOMAIN}"
  "backend.${DOMAIN}"
  "staging.${DOMAIN}"
  "dev.${DOMAIN}"
)

for sub in "${APP_SUBDOMAINS[@]}"; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "https://${sub}" 2>/dev/null)
  if [ "$HTTP_CODE" != "000" ] && [ "$HTTP_CODE" != "404" ]; then
    echo "[FOUND] ${sub}: HTTP ${HTTP_CODE}"
    # Get server header for technology fingerprinting
    curl -sI "https://${sub}" --connect-timeout 5 --max-time 10 2>/dev/null | grep -iE "^(server|x-powered-by|x-frame-options):"
  fi
done
```

#### 11.2 - Check for App Links in Marketing Site

```javascript
// Look for links pointing to app subdomains
mcp__playwright__browser_evaluate({
  function: `() => {
    const links = Array.from(document.querySelectorAll('a[href]'));
    const domain = window.location.hostname.replace('www.', '');
    return links
      .map(a => a.href)
      .filter(href => {
        const url = new URL(href, window.location.origin);
        return url.hostname !== window.location.hostname &&
               url.hostname.endsWith(domain);
      })
      .filter((v, i, a) => a.indexOf(v) === i);  // unique
  }`
})
```

#### 11.3 - Check DNS/Certificate for Subdomains

```bash
# Quick certificate SAN check reveals all subdomains on same cert
echo | openssl s_client -connect ${DOMAIN}:443 2>/dev/null | \
  openssl x509 -noout -ext subjectAltName 2>/dev/null | \
  tr ',' '\n' | grep -oE '[a-zA-Z0-9*.-]+\.[a-z]{2,}'

# DNS common subdomains
for sub in app api admin; do
  IP=$(dig +short ${sub}.${DOMAIN} 2>/dev/null | head -1)
  [ -n "$IP" ] && echo "${sub}.${DOMAIN} -> $IP"
done
```

#### 11.4 - Expand Scope if App Subdomain Found

When an application subdomain is discovered:

1. **Run backend detection on it** — the app subdomain likely has the actual backend (SvelteKit, Next.js, Django, etc.)
2. **Add to scan scope** — all subsequent phases should test BOTH marketing site and app subdomain
3. **Fingerprint separately** — the app may use completely different technology (e.g., Framer marketing + SvelteKit app)
4. **Document in output** — add `app_subdomains` to FASE 0 results

**Output addition:**
```yaml
  # APPLICATION SUBDOMAIN DISCOVERY
  app_subdomains:
    - subdomain: "app.{domain}"
      ip: "{ip}"
      http_status: {code}
      server: "{server header}"
      framework: "{detected framework}"
      separate_backend: true
      action: "EXPAND SCOPE - run full scan on this subdomain"
```

**Example scenario (multi-subdomain pattern):**
- `example.com` → Static Framer site, no backend → limited scan
- `app.example.com` → SvelteKit SSR app with auth → full scan needed
- Without this step, we'd miss the entire application!

### Step 0.12: Determine Scan Path

Based on detection:

| Backend | Phases to Execute |
|---------|-------------------|
| Supabase | 1-14, 16-21, EXTRA 1-5 |
| Firebase | 1, 7, 10-13, F1-F4, EXTRA 1-5 |
| AWS Amplify | 1, 7, 10-13, C1-C4, EXTRA 1-5 (Cognito focus) |
| Hasura | 1, 7, 10-13, 17 (GraphQL), EXTRA 1-5 |
| Appwrite | 1, 7, 10-13, C1-C4, EXTRA 1-5 |
| Pocketbase | 1, 7, 10-13, C1-C4, EXTRA 1-5 |
| Nhost | 1, 7, 10-13, 17 (GraphQL), EXTRA 1-5 |
| Custom API | 1, 7, 10-13, C1-C4, EXTRA 1-5 |
| GraphQL | 1, 7, 10-13, 17, EXTRA 1-5 |
| Unknown | 1, 7, 10-13, EXTRA 1-5 (minimal) |

---

## Detection Priority

Check in this order (first match wins):

1. **Supabase** - Most specific patterns (*.supabase.co)
2. **Firebase** - Specific SDK patterns (firebaseConfig)
3. **AWS Amplify** - AWS-specific patterns (Amplify.configure)
4. **Hasura** - GraphQL with Hasura headers
5. **Appwrite** - Appwrite SDK/endpoints
6. **Pocketbase** - /api/collections pattern
7. **Nhost** - *.nhost.run patterns
8. **GraphQL** - Generic GraphQL endpoint
9. **Custom API** - Generic REST patterns
10. **Unknown** - No clear backend detected

---

## Playwright Commands

```javascript
// Navigate
mcp__playwright__browser_navigate({ url: target_url })

// Wait for load
mcp__playwright__browser_wait_for({ time: 3 })

// Get page source
mcp__playwright__browser_evaluate({
  function: "() => document.documentElement.outerHTML"
})

// Check window object
mcp__playwright__browser_evaluate({
  function: "() => Object.keys(window).filter(k => /supabase|firebase|api/i.test(k))"
})

// Get network requests
mcp__playwright__browser_network_requests({})
```

---

## Confidence Levels

**HIGH confidence:**
- Direct SDK initialization found (supabase.createClient, firebase.initializeApp)
- API endpoint responds with expected format
- Multiple indicators match

**MEDIUM confidence:**
- URL patterns match but no SDK found
- Network requests suggest backend but not confirmed
- Partial config found

**LOW confidence:**
- Only generic API patterns
- No clear indicators
- Guessing based on framework hints

---

## Example Output

```
FASE_0_RESULTS:
  backend_type: supabase
  confidence: high

  configs_extracted:
    - name: supabase_url
      value: https://abcd1234.supabase.co
      source: JS bundle (index-abc123.js)
    - name: anon_key
      value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      source: JS bundle (index-abc123.js)
    - name: project_id
      value: abcd1234
      source: derived from URL

  scan_path:
    - FASE 1: Reconnaissance
    - FASE 2: Schema Discovery
    - FASE 3: RLS Testing
    - FASE 4: Storage & Functions
    - FASE 5: Authentication Testing
    - FASE 6: WebSocket/Realtime
    - FASE 7: Security Headers
    - FASE 8: JWT Analysis
    - FASE 9: Advanced Attacks
    - FASE 10: Third-Party Discovery
    - FASE 11: Auth Bypass
    - FASE 12: JS Bundle Analysis
    - FASE 13: Report Generation
    - FASE 14: Authenticated Testing
    - FASE 16-21: Advanced Testing
    - EXTRA 1-5: Universal Tests

  evidence:
    - "Found supabase.createClient() in index-abc123.js"
    - "Network request to abcd1234.supabase.co/auth/v1/settings confirmed"
    - "Anon key decoded: role=anon, project_ref=abcd1234"
```

---

## Error Handling

**If page doesn't load:**
```
FASE_0_RESULTS:
  backend_type: error
  error: "Page failed to load: {reason}"
  recommendation: "Check URL and try again"
```

**If no backend detected:**
```
FASE_0_RESULTS:
  backend_type: unknown
  confidence: low
  scan_path:
    - FASE 1: Reconnaissance (limited)
    - FASE 7: Security Headers
    - FASE 12: JS Bundle Analysis
    - EXTRA 1-5: Universal Tests
  recommendation: "Manual analysis recommended"
```

---

## References

- `references/backend-patterns.md` - Detection regex patterns
- `references/scan-paths.md` - Phase mapping by backend

---

## After Completion

After executing FASE 0, provide the YAML results and call `/scan-write`:

```
/scan-write {client_name} --fase 0
```

This logs the backend detection results to SCAN-IN-PROGRESS.md.
