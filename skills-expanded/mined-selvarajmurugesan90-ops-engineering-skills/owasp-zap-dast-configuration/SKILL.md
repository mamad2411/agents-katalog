---
name: owasp-zap-dast-configuration
description: >
  Guides deep, tool-specific configuration of OWASP ZAP (Zed Attack
  Proxy) for automated dynamic scanning — baseline vs. full active scan
  selection, the ZAP Automation Framework YAML plan, authenticated
  scanning via authentication scripts/contexts, and API-driven scans
  seeded from an OpenAPI spec. Use when the user asks to "configure a ZAP
  automation framework plan", "write a ZAP context file for
  authenticated scanning", "tune ZAP alert thresholds", "run zap-baseline
  vs zap-full-scan", "script ZAP login for a scan", or "seed a ZAP scan
  from an OpenAPI/Swagger spec". ZAP-specific depth on scan types,
  automation YAML, and auth scripting; for the general DAST concept and
  tool-agnostic workflow see dast-integration in the devsecops domain.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# OWASP ZAP DAST Configuration

## Purpose

OWASP ZAP is the most widely used open-source dynamic scanner, and its
practical value depends entirely on configuration most teams get wrong
on the first attempt: running the intrusive full/active scan against
the wrong environment, letting the crawler get stuck on an
unauthenticated login page, or trusting a default alert threshold that
buries three real findings under forty low-confidence ones. This skill
goes deep on ZAP's specific mechanics — the baseline vs. full scan
distinction, the declarative Automation Framework YAML that has
superseded ad-hoc `zap-baseline.py`/`zap-full-scan.py` invocations in
current ZAP, writing authentication scripts/contexts so authenticated
areas actually get scanned, and seeding a scan from an OpenAPI spec. For
the general DAST concept — why dynamic scanning matters, where it fits
relative to SAST/SCA, and vendor-neutral CI wiring — see
[dast-integration](../../../devsecops/skills/dast-integration/SKILL.md).

## When to use

- The user asks to "set up ZAP" or "write a ZAP Automation Framework
  plan" for a specific application.
- The user needs to choose between `zap-baseline.py` (passive-only) and
  `zap-full-scan.py`/an active-scan automation job, and needs the
  concrete difference in what each does and is safe to run against.
- The user's ZAP scan never gets past the login page, or reports
  findings only on public/unauthenticated pages.
- The user wants to scan a REST or GraphQL API using an OpenAPI spec as
  the crawl seed instead of relying on ZAP's spider.
- The user wants to tune ZAP's alert thresholds/rules
  (`-config`/rules file) to cut noise without disabling whole scan
  categories.
- The user is migrating from the older standalone Python wrapper
  scripts (`zap-baseline.py`, `zap-api-scan.py`, `zap-full-scan.py`) to
  the current ZAP Automation Framework YAML format.

## Prerequisites & environment

- ZAP `2.15.x` (current stable line as of this writing) via the
  `zaproxy/zap-stable` container image, or the desktop/daemon
  distribution. The Automation Framework (`zap.yaml` plans, invoked via
  `zap.sh -cmd -autorun plan.yaml` or the `zap-x.py` wrapper's
  `-autorun` mode) is the current recommended entry point over the
  older per-mode Python scripts, which remain available but receive
  less active development attention.
- A reachable target environment — **never point an active-scan job at
  production**; use a staging/preview environment that mirrors
  production auth and middleware closely enough to be representative.
  See [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md)
  for the fuller rationale and environment-isolation guidance.
- A dedicated test account (never a real customer or admin credential)
  for authenticated scanning, sourced from a secrets manager in CI —
  see [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md).
- An OpenAPI/Swagger JSON/YAML spec or GraphQL introspection endpoint,
  if scanning an API — improves coverage dramatically over spider-only
  discovery for endpoints with no HTML links pointing to them.
- Enough CI runner memory/time budget: baseline scans typically finish
  in a few minutes; full active scans against a non-trivial app can run
  15-60+ minutes depending on crawl depth and app size.

## Step-by-step guidance

1. **Understand the scan-type spectrum before picking one:**
   - **Baseline** (`zap-baseline.py`, or an Automation Framework plan
     with only a `passiveScan-wait` job after spidering) — spiders the
     app and passively observes traffic; sends no attack payloads; safe
     to run frequently, even against a shared or lightly-loaded
     environment.
   - **Full/active scan** (`zap-full-scan.py`, or a plan with an
     `activeScan` job) — after spidering, actively sends exploit-style
     payloads (SQLi, XSS, path traversal probes) to every discovered
     parameter; can create data, trigger side effects, and is
     meaningfully slower. Restrict to isolated test/staging
     environments.
   - **API scan** (`zap-api-scan.py`, or an `openapi`/`graphql` import
     job) — seeds the crawl from a spec instead of link-following,
     since APIs usually have few or no HTML links to discover from.

2. **Write an Automation Framework plan** instead of chaining CLI flags
   — it is declarative, version-controllable, and the current
   recommended interface:
   ```yaml
   # zap-plan.yaml
   env:
     contexts:
       - name: "checkout-service"
         urls:
           - "https://staging.example.internal"
         authentication:
           method: "script"
           parameters:
             script: "/zap/scripts/auth/checkout-login.js"
             scriptEngine: "Oracle Nashorn"
         sessionManagement:
           method: "cookie"
         users:
           - name: "dast-test-user"
             credentials:
               username: "${DAST_TEST_USER}"
               password: "${DAST_TEST_PASSWORD}"
     parameters:
       failOnError: true
       progressToStdout: true

   jobs:
     - type: spider
       parameters:
         context: "checkout-service"
         user: "dast-test-user"
         maxDuration: 10

     - type: passiveScan-wait
       parameters:
         maxDuration: 5

     - type: activeScan
       parameters:
         context: "checkout-service"
         user: "dast-test-user"
       policyDefinition:
         defaultStrength: "medium"
         defaultThreshold: "medium"

     - type: report
       parameters:
         template: "traditional-html"
         reportDir: "/zap/wrk"
         reportFile: "zap-report"

     - type: exitStatus
       parameters:
         errorLevel: "High"
         warnLevel: "Medium"
   ```
   Run it:
   ```bash
   docker run --rm -v "$(pwd)/zap:/zap/wrk:rw" \
     -e DAST_TEST_USER -e DAST_TEST_PASSWORD \
     -t zaproxy/zap-stable zap.sh -cmd \
     -autorun /zap/wrk/zap-plan.yaml
   ```

3. **Script authentication explicitly** rather than relying on ZAP's
   form-based auto-fill, which routinely breaks on CSRF tokens,
   multi-step logins, or JS-rendered forms. A minimal authentication
   script (JavaScript, ZAP's scripting engine):
   ```javascript
   // checkout-login.js — ZAP authentication script
   function authenticate(helper, paramsValues, credentials) {
     var loginUrl = "https://staging.example.internal/api/login";
     var msg = helper.prepareMessage();
     var requestBody = JSON.stringify({
       username: credentials.getParam("username"),
       password: credentials.getParam("password")
     });
     helper.sendAndReceive(msg, requestUri(loginUrl), requestBody);
     return msg;
   }

   function getRequiredParamsNames() { return []; }
   function getOptionalParamsNames() { return []; }
   ```
   Verify authentication actually succeeded by checking the ZAP
   "Authentication" tab/log for a logged-in indicator (e.g. absence of
   a "login failed" string) before trusting scan coverage of
   authenticated pages.

4. **Seed API scans from an OpenAPI spec** instead of relying on the
   spider to discover routes with no HTML links:
   ```bash
   docker run --rm -v "$(pwd)":/zap/wrk/:rw \
     -t zaproxy/zap-stable zap-api-scan.py \
     -t https://staging.example.internal/openapi.json \
     -f openapi \
     -r zap-api-report.html
   ```
   Or as an Automation Framework job:
   ```yaml
   - type: openapi
     parameters:
       apiUrl: "https://staging.example.internal/openapi.json"
       targetUrl: "https://staging.example.internal"
   ```

5. **Tune alert thresholds with a rules file** rather than disabling
   whole scan categories — format is `<rule-id> <TAB> <threshold> <TAB>
   <comment>`:
   ```
   # zap-rules.tsv
   10202	IGNORE	Anti-CSRF token check - bearer-token API, no cookies used
   10096	WARN	Timestamp disclosure - internal staging env only
   40018	FAIL	SQL Injection (time-based) - always block on this
   ```
   Reference it in the baseline wrapper (`-c zap-rules.tsv`) or set
   per-rule thresholds in the Automation Framework's `alertFilter` job
   type for the declarative equivalent.

6. **Gate the pipeline on risk + confidence, not raw alert count.** ZAP
   reports Risk (High/Medium/Low/Informational) and Confidence
   separately in its JSON/SARIF output; the `exitStatus` job (step 2)
   or a small post-processing script should fail only on
   High-risk-and-Medium-or-higher-confidence findings, routing the rest
   to a dashboard for manual review.

7. **Separate cadence by scan type**: baseline on every PR-preview
   deploy (cheap, safe), full active scan on a nightly/weekly schedule
   or pre-release gate against a dedicated DAST test environment
   (slower, intrusive) — see
   [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md)
   for the CI-wiring pattern this applies within.

## Best practices

- Default to the Automation Framework YAML plan over chained CLI flags
  or the older standalone wrapper scripts — it's declarative,
  diffable in code review, and keeps auth/context/policy configuration
  in one version-controlled place instead of scattered flags.
- Always verify authentication actually worked before trusting an
  authenticated scan's coverage — a silently-failed login makes ZAP
  scan only the public login page and report a false "all clear" for
  everything behind it.
- Keep the active-scan policy's `defaultStrength`/`defaultThreshold`
  explicit in the plan file rather than accepting ZAP's install
  defaults, so scan behavior doesn't silently change across ZAP
  version upgrades.
- Store the rules/alert-filter file in the repo, versioned and
  reviewed like code, not configured ad hoc in a ZAP UI session that
  disappears with the container.
- Seed every API scan from its OpenAPI/GraphQL spec — spider-only
  discovery on an API with no HTML routinely misses the majority of
  real endpoints.
- Never let an active-scan job run unattended against a shared staging
  environment other teams depend on — use a dedicated, disposable DAST
  test environment with outbound integrations (email, payment,
  third-party APIs) stubbed.
- Treat a clean ZAP report as one input, not a release gate on its own
  — it only tests what it can discover and only from an unauthenticated
  or single-test-user perspective; pair it with
  [trivy-vulnerability-scanning](../trivy-vulnerability-scanning/SKILL.md)
  for dependency/image CVEs and
  [sonarqube-code-quality-and-security](../sonarqube-code-quality-and-security/SKILL.md)
  or another SAST tool for code-level issues ZAP cannot see from the
  outside.

## Common pitfalls

- **Symptom:** The active scan reports dozens of injection findings, but
  they're all on the login page and nothing behind it — the app has
  30+ authenticated routes the scan never touched.
  **Fix:** The authentication script/context is misconfigured or
  silently failing. Check the ZAP authentication log for a successful
  login indicator, verify the `loggedInIndicator`/`loggedOutIndicator`
  regex in the context matches real page content, and confirm session
  management (cookie vs. bearer token) matches how the app actually
  authenticates.

- **Symptom:** An active scan run against the shared staging environment
  creates dozens of junk orders/accounts, or trips a third-party
  sandbox's rate limit and pages the on-call for that integration.
  **Fix:** Active scans send real exploit-style payloads that can
  mutate state — run them only against a dedicated, disposable DAST
  test environment with third-party integrations stubbed/sandboxed,
  never a shared staging environment (see
  [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md)
  for environment-isolation guidance).

- **Symptom:** The spider gets stuck and reports near-zero URLs found
  on a single-page application (SPA) built with React/Vue/Angular.
  **Fix:** ZAP's traditional spider follows `<a href>` links and
  doesn't execute client-side JavaScript routing; switch to ZAP's
  **AJAX Spider** (`ajaxSpider` job type, backed by a headless browser)
  for JS-heavy frontends, or seed the crawl from an OpenAPI spec if the
  real attack surface is the backing API rather than the rendered
  pages.

- **Symptom:** CSRF-protected login forms cause the automated
  form-fill to fail every time, and the scan never authenticates.
  **Fix:** Use a scripted authentication method (JavaScript
  authentication script, as in step 3) that explicitly extracts and
  replays the CSRF token, or injects a pre-generated session
  cookie/bearer token directly, instead of relying on ZAP's generic
  form-based auto-fill.

- **Symptom:** Two runs of the same plan against the same target a week
  apart report a different set of findings, making regressions hard to
  track.
  **Fix:** Pin the ZAP image/version, keep the plan YAML and rules
  file in version control, and run against a environment with stable,
  seeded test data rather than a staging environment whose data/state
  constantly changes between runs.

## Worked example

A REST API service (`checkout-service`) adds a ZAP baseline job on every
PR-preview deploy, and a scheduled authenticated full scan against a
dedicated DAST test environment, both driven by the Automation
Framework.

`.zap/baseline-plan.yaml`:
```yaml
env:
  contexts:
    - name: "checkout-api"
      urls:
        - "https://pr-preview.example.internal"
jobs:
  - type: openapi
    parameters:
      apiUrl: "https://pr-preview.example.internal/openapi.json"
      targetUrl: "https://pr-preview.example.internal"
  - type: passiveScan-wait
    parameters:
      maxDuration: 5
  - type: report
    parameters:
      template: "traditional-html"
      reportDir: "/zap/wrk"
      reportFile: "zap-baseline-report"
  - type: exitStatus
    parameters:
      errorLevel: "High"
```

`.github/workflows/dast-zap.yml`:
```yaml
name: dast-zap
on:
  pull_request:
  schedule:
    - cron: '0 2 * * *'

jobs:
  baseline:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ZAP baseline (Automation Framework)
        run: |
          docker run --rm -v "$(pwd)/.zap:/zap/wrk:rw" \
            -t zaproxy/zap-stable:2.15.0 zap.sh -cmd \
            -autorun /zap/wrk/baseline-plan.yaml

  full-scan-nightly:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ZAP authenticated full scan
        env:
          DAST_TEST_USER: ${{ secrets.DAST_TEST_USER }}
          DAST_TEST_PASSWORD: ${{ secrets.DAST_TEST_PASSWORD }}
        run: |
          docker run --rm -v "$(pwd)/.zap:/zap/wrk:rw" \
            -e DAST_TEST_USER -e DAST_TEST_PASSWORD \
            -t zaproxy/zap-stable:2.15.0 zap.sh -cmd \
            -autorun /zap/wrk/full-scan-plan.yaml
```

Sample baseline finding (HTML report, trimmed):
```
FAIL-NEW: SQL Injection - Time Based [40018]
  Risk: High | Confidence: Medium
  URL: https://pr-preview.example.internal/api/orders?status=
  Evidence: response delayed ~5000ms for payload "1' AND SLEEP(5)-- -"
```
Remediation: trace the `status` query parameter through the `/api/orders`
handler to confirm it reaches a raw SQL string; fix with a parameterized
query, redeploy the PR preview, and re-run the baseline plan to confirm
the finding clears before merge.

## Cross-references

- [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md) —
  the tool-agnostic DAST concept, environment-isolation rationale, and
  CI cadence pattern this skill goes deep on for ZAP specifically.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) —
  sourcing the dedicated test credentials used for authenticated
  scanning from a secrets manager instead of inline CI variables.
- [trivy-vulnerability-scanning](../trivy-vulnerability-scanning/SKILL.md) —
  covers dependency and image CVEs that a black-box DAST scan like ZAP
  cannot see from the outside.
- [sonarqube-code-quality-and-security](../sonarqube-code-quality-and-security/SKILL.md) —
  static, source-level analysis that runs earlier in the pipeline and
  finds a different, complementary class of issues to ZAP's runtime
  scanning.
