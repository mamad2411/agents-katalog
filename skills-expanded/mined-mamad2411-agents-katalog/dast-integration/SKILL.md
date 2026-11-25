---
name: dast-integration
description: >
  Guides adding Dynamic Application Security Testing (DAST) — automated
  black-box scanning of a running web application or API — using tools
  such as OWASP ZAP or Nuclei, in CI/CD or on a scheduled cadence against
  a staging environment. Use when the user asks to "add DAST scanning",
  "run a ZAP baseline scan against staging", "automate OWASP scanning in
  the pipeline", "test the running app for injection/auth/config
  vulnerabilities", or "scan our API for security issues before release".
  Complements, but does not replace, SAST or SCA static analysis.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# DAST Integration

## Purpose

Dynamic Application Security Testing (DAST) exercises a running
application from the outside — sending crafted HTTP requests and
observing responses — to find vulnerabilities that only manifest at
runtime: broken authentication/session handling, security misconfiguration
(missing headers, verbose error pages, exposed debug endpoints),
server-side request forgery, injection flaws reachable through the actual
request/response path, and issues in how components are wired together in
a deployed environment. Because it treats the app as a black box, DAST
finds a different, often complementary, class of issues to SAST (which
reads source but never sees runtime config or deployment topology) and
SCA (which reads dependency manifests but never exercises the app).
Integrating DAST into CI/CD or a recurring pipeline turns this from an
occasional pentest activity into continuous, automated feedback against
every staging deploy.

## When to use

- The user asks to "add DAST scanning", "run ZAP against staging", or
  "automate dynamic security scanning" for a web app or API.
- A team has SAST/SCA in place but no runtime testing, and wants to close
  the gap for auth flows, session management, and misconfiguration issues
  that static analysis cannot see.
- The user wants a pre-release gate that scans a running staging/preview
  environment before promoting to production.
- The user needs to scan a REST/GraphQL API using an OpenAPI/Swagger spec
  as the seed for automated scanning.
- The user is troubleshooting DAST scan noise (false positives from
  authenticated-only pages, CSRF tokens breaking scans, rate limiting
  triggering on the scanner) and needs a tuning strategy.
- The user explicitly wants a passive-only scan (safe against production)
  versus an active scan (should only run against staging/test
  environments due to write/mutation traffic it generates).

## Prerequisites & environment

- A reachable, running instance of the application — a staging
  environment, ephemeral PR-preview environment, or a locally-run
  container in CI. **DAST must never run active scans against production**
  without a carefully scoped, pre-approved exception, since active scans
  send exploit-like payloads (SQLi, XSS, path traversal probes) that can
  create real data, trigger real emails/webhooks, or affect real users.
- **OWASP ZAP** (`zaproxy/zap-stable` container image, current stable line
  `2.15.x` as of this writing) — the most common open-source DAST tool,
  usable via the `zap-baseline.py` (passive-only, fast, safe for CI) or
  `zap-full-scan.py` (active, slower, more intrusive) wrapper scripts, or
  its Automation Framework YAML for finer control.
- **Nuclei** — template-based scanner good for fast, targeted checks
  (known CVE patterns, misconfigurations, exposed panels) with a large
  community template library; complements ZAP rather than replacing it.
- Test credentials/service accounts for authenticated scanning (never
  real user or production credentials), provisioned via your secrets
  manager — see [secrets-management](../secrets-management/SKILL.md).
- An OpenAPI/Swagger or Postman collection spec if scanning an API,
  to seed the scanner's crawl instead of relying on link discovery alone.
- CI runner with enough memory/CPU headroom — active scans against a
  non-trivial app can run 15-60+ minutes; budget pipeline time
  accordingly or run on a schedule rather than every commit.

## Step-by-step guidance

1. **Start with a passive/baseline scan** against a staging or
   PR-preview environment — it only observes traffic and crawls
   passively, so it's safe to run frequently and unattended:
   ```yaml
   # GitHub Actions
   name: dast-baseline
   on:
     pull_request:
   jobs:
     zap-baseline:
       runs-on: ubuntu-latest
       steps:
         - name: ZAP Baseline Scan
           uses: zaproxy/action-baseline@v0.12.0
           with:
             target: 'https://pr-${{ github.event.number }}.staging.example.internal'
             rules_file_name: '.zap/rules.tsv'
             cmd_options: '-a'
   ```

2. **Seed the scan with an API spec** for better coverage of non-linked
   endpoints:
   ```bash
   docker run --rm -v "$(pwd)":/zap/wrk/:rw \
     -t zaproxy/zap-stable zap-api-scan.py \
     -t https://staging.example.internal/openapi.json \
     -f openapi \
     -r zap-api-report.html
   ```

3. **Add authenticated scanning** for endpoints behind login, using a
   dedicated test account and a ZAP authentication script or context
   file — never scan authenticated flows with production customer
   credentials. Store test credentials as CI secrets, not inline:
   ```yaml
   env:
     DAST_TEST_USER: ${{ secrets.DAST_TEST_USER }}
     DAST_TEST_PASSWORD: ${{ secrets.DAST_TEST_PASSWORD }}
   ```

4. **Reserve active/full scans for a scheduled job against a dedicated
   test environment**, not every PR — active scans send exploit-style
   payloads and can be slow and disruptive:
   ```yaml
   name: dast-full-nightly
   on:
     schedule:
       - cron: '0 3 * * *'
   jobs:
     zap-full:
       runs-on: ubuntu-latest
       steps:
         - uses: zaproxy/action-full-scan@v0.12.0
           with:
             target: 'https://dast-test.example.internal'
             rules_file_name: '.zap/rules.tsv'
   ```

5. **Triage findings by confidence and risk**, not raw count. ZAP reports
   Risk (High/Medium/Low/Informational) and Confidence separately —
   gate on High-risk + High/Medium-confidence findings first, and route
   low-confidence results to manual review instead of auto-failing on
   them.

6. **Tune out known-noisy rules** via a rules file rather than ignoring
   whole scan categories:
   ```
   # .zap/rules.tsv — format: <rule id>\t<threshold>\t<comment>
   10202	IGNORE	Absence of Anti-CSRF Tokens - false positive, API uses bearer tokens not cookies
   10096	WARN	Timestamp disclosure - low risk, internal staging only
   ```

7. **Feed results into the same triage workflow as SAST/SCA** (SARIF
   export, ticket auto-creation, PR comments) so security findings live
   in one place rather than three disconnected dashboards.

## Best practices

- Never point an active/full DAST scan at production — use a staging
  or dedicated dynamic-test environment that mirrors production
  configuration (same auth flows, same middleware) closely enough to be
  representative.
- Run passive/baseline scans frequently (every PR or every staging
  deploy) since they're low-risk and fast; reserve active scans for a
  nightly/weekly cadence or pre-release gate.
- Seed scans with an API spec (OpenAPI/GraphQL introspection) whenever
  available — crawler-only discovery misses most API-only endpoints with
  no HTML links pointing to them.
- Rate-limit and IP-allowlist the scanner in the target environment so it
  doesn't trip WAF/bot-protection or DDoS-style alerting meant for real
  traffic.
- Treat DAST findings as one input among several: it does not see source
  code, so pair it with
  [sast-integration](../sast-integration/SKILL.md) for code-level issues
  and [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md)
  for vulnerable dependencies — none of the three alone gives full
  coverage.
- Version-pin scanner images/actions and periodically refresh them —
  scan engines and their vulnerability signature sets update frequently,
  and an old pinned version will miss newer patterns.
- Keep a persistent allowlist/rules file in the repo (not scanner UI
  config) so tuning is version-controlled and reviewable in PRs.

## Common pitfalls

- **Symptom:** DAST scan reports dozens of "false positive" injection
  findings on pages that require login, because the scanner never
  authenticated and only saw the login page.
  **Fix:** Configure authenticated scanning (ZAP context + auth script,
  or a pre-authenticated session cookie/token injected via scan config)
  using a dedicated test account, not anonymous crawling.

- **Symptom:** An active scan run against a shared staging environment
  corrupts test data, sends real emails via a working SMTP integration,
  or trips a third-party sandbox's rate limits.
  **Fix:** Run active scans only against an isolated environment with
  outbound integrations stubbed or pointed at sandboxes (fake SMTP,
  sandboxed payment processor, mocked third-party APIs), never a
  shared staging environment other teams depend on.

- **Symptom:** The DAST job routinely times out or takes over an hour,
  blocking the pipeline.
  **Fix:** Split into a fast passive/baseline scan on every PR and a
  separate scheduled full/active scan outside the critical path (nightly
  cron), and scope the full scan's crawl depth/exclusions to avoid
  scanning unrelated subdomains or huge static asset trees.

- **Symptom:** CSRF-token or anti-automation protections cause the
  scanner to get stuck on the login form and never proceed past it.
  **Fix:** Use a scripted authentication flow (ZAP authentication
  scripts, or a pre-generated session token injected as a header/cookie)
  instead of relying on the scanner to fill and submit the login form
  itself.

- **Symptom:** Every scan run reports a slightly different set of
  findings, making it hard to tell if anything regressed.
  **Fix:** Pin the scanner version/image, fix the rules/policy file in
  version control, and run against a stable, seeded test dataset rather
  than a staging environment with constantly-changing data.

## Worked example

A team adds a ZAP baseline scan to every PR preview deploy, plus a
scheduled full scan against a dedicated DAST test environment.

`.zap/rules.tsv`:
```
10202	IGNORE	Anti-CSRF token check - API is bearer-token auth, no cookies used
10096	WARN	Timestamp disclosure in response headers - internal env only
```

`.github/workflows/dast.yml`:
```yaml
name: dast
on:
  pull_request:
  schedule:
    - cron: '0 3 * * *'

jobs:
  baseline:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ZAP baseline scan against PR preview
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'https://pr-${{ github.event.number }}.staging.example.internal'
          rules_file_name: '.zap/rules.tsv'
          fail_action: true

  full-scan:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ZAP authenticated full scan against dedicated DAST env
        uses: zaproxy/action-full-scan@v0.12.0
        with:
          target: 'https://dast-test.example.internal'
          rules_file_name: '.zap/rules.tsv'
        env:
          ZAP_AUTH_USER: ${{ secrets.DAST_TEST_USER }}
          ZAP_AUTH_PASSWORD: ${{ secrets.DAST_TEST_PASSWORD }}
```

Sample high-risk finding from a baseline run:
```
WARN-NEW: X-Frame-Options Header Not Set [10020]
  x 3 URLs (clickjacking risk on unframed pages)
FAIL-NEW: SQL Injection - Time Based [40018]
  x 1 URL: https://pr-482.staging.example.internal/api/search?q=
```
Remediation: add `X-Frame-Options: DENY` (or CSP `frame-ancestors`) at the
reverse proxy/app middleware layer for the header finding, and for the
SQLi finding, trace `q` through `/api/search` to confirm it reaches a raw
query — fix with a parameterized query and re-run the baseline scan to
confirm the finding clears.

## Cross-references

- [sast-integration](../sast-integration/SKILL.md) — static, source-level
  analysis that runs earlier and faster than DAST but cannot see runtime
  configuration or deployment-specific issues.
- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — how to combine
  DAST with SAST/SCA gates into a coherent pipeline without duplicating
  or contradicting each other's blocking behavior.
