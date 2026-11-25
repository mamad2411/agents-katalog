---
name: dast-workflow
description: Dynamic Application Security Testing workflow — OWASP ZAP automation (baseline/full/API scans), Burp Suite Professional playbooks, Burp Collaborator for out-of-band detection, auth-state orchestration, and CI integration with scope-safe active scanning.
---

# DAST Workflow

## When to use

DAST tests a running application from the outside. Where `sast-orchestrator` reads code, DAST sends HTTP requests and looks at response patterns. That covers runtime behaviour SAST doesn't see (auth flows, session handling, header config, reverse-proxy misconfig, DoS sensitivity).

Activates on:

- A request like "set up ZAP against our staging", "run a baseline scan", "review this Burp output", "how does the scanner log in", "DAST in CI".
- A new deployable environment (staging, QA, security sandbox) that needs security testing before promotion to production.
- A periodic scan against staging, or a pre-release regression run.
- A handoff from `security-review` where runtime behaviour needs to be verified (e.g. are the security headers actually present in the response?).
- Bug-bounty preparation: scan with DAST first to clear out the low-hanging fruit before paying hunters look at it.

### When NOT to use (handoff)

- Static code analysis → `sast-orchestrator`. DAST doesn't see source.
- Infrastructure (Terraform/K8s/Docker) → `iac-security` / `k8s-security` / `container-hardening`.
- Pre-deploy threat model at design level → `threat-modeler`.
- OWASP API Top 10 as the substantive framework → `api-security`. DAST tools cover API scans; this skill orchestrates, that one provides the substantive checklist.
- Active offensive pentest with exploitation → `web-exploit-triage` + `payload-crafter` + `recon-agent`. DAST flags; pentest exploits.
- Triage of dep-vulns from a runtime scan → `cve-triage`.
- Production scans: this skill explicitly targets staging-style environments. Production DAST requires extra controls and ops alignment (see phase 1).

## Approach

Seven phases. Phase 1 (scope + environment) and phase 3 (auth-state) are the heart. Both are where DAST projects fail.

### 1. Scope and environment

DAST scans have real blast-radius: they fire thousands to millions of requests, hit side-effects (emails sent, payments triggered, notifications), and can DoS the target app. Setting scope is not a formality.

- **Environment**: staging with a production-like data schema but no real customer data is the sweet spot. Production DAST only with: explicit ops sign-off, off-peak window, scanner rate-limiting, and a kill-switch.
- **In-scope hosts**: explicit allowlist (`*.staging.example.com` is better than the `example.com` wildcard). DAST tools will otherwise spider out to external hosts that aren't yours.
- **Out-of-scope paths**: logout (causes session teardown mid-scan), destructive actions (`DELETE /users/{id}`, `POST /admin/wipe-data`), third-party-embedded content, rate-limited auth endpoints (unless you're testing them deliberately).
- **Data effects**: which actions have side effects? Email dispatch, payment creation, webhook triggers. Set up test accounts with your own email addresses and use the sandbox mode of payment providers.
- **Rate limiting**: scanner concurrency at 5–10 threads, delay between requests, respect 429 responses. A DAST scan that knocks your test environment over is not the goal.

A written scope spec with these fields is required before scan start, comparable to a pentest RoE. For internal scans this can be a commit comment; for shared staging, prefer explicit sign-off.

### 2. Tool choice: ZAP, Burp, alternatives

Two dominant tools for web DAST; choose by context.

- **OWASP ZAP** (Apache-2, OSS). Default choice for CI integration and open-source workflows. Headless mode via `zap-cli` or the Automation Framework, fully scriptable. Three scan modes: baseline (passive only, ~2 min), full (passive + active, ~30–60 min), API (driven by an OpenAPI/Swagger import).
- **Burp Suite Professional** (PortSwigger, commercial). Stronger in interactive testing and exploratory work. Burp Collaborator for out-of-band (OOB) detection — essential for blind SSRF, blind XSS, blind SQL injection. Less suitable for headless CI (Burp Enterprise is the variant for that).
- **Burp Suite Enterprise** (commercial). CI integration, dashboards. More expensive but scales better than ZAP in large orgs.
- **Other**: Nuclei (template-based, good for vuln-specific scanning driven by CVE templates), Acunetix/Invicti/Netsparker (commercial enterprise, less Rails/Node-oriented), Arachni (in maintenance).

**Heuristic**: start with ZAP in CI for a baseline-passive per PR. Schedule ZAP full-scan against staging. Burp Professional for in-depth work by a security engineer on specific features. The Enterprise variant when you have 20+ apps to scan.

### 3. Auth-state orchestration

The biggest DAST failure mode: the scanner only hits unauthenticated surface and misses everything behind the login. Setting up auth-state is per-app specific but follows patterns.

**ZAP auth modes** (in order of usefulness):

- **Script-based auth** (Zest or JavaScript) — define the login flow step by step. For complex flows (CSRF token refresh, multi-step).
- **Form-based auth** — a standard login page with username + password fields. Quick to set up.
- **JSON auth** — for SPAs that POST JSON. Provide endpoint + request body + response field for the token.
- **HTTP auth** (Basic/Digest/NTLM) — rare in modern apps.
- **Manual / browser-state export** — Burp has session-management rules; ZAP can import cookies. For cases where you can't get login scripted.

**Logged-in indicator** — how does the scanner know the session is still active? Regex on a header (`X-User-ID`), on body content (`Logout`), or a probe URL that returns 200 when authenticated and 401 otherwise. Without an indicator the scanner runs with an expired session and produces nonsense.

**Logged-out indicator** — redirect to `/login`, 401, or body text. Trigger for auto-reauth.

**Token refresh** — OAuth2/JWT sessions expire. A script that exchanges a refresh token for a new access token. ZAP's auth script can do this; Burp via session-handling rules.

**Extend the exclude set** — if logout stays in scope your session gets destroyed mid-scan. Mark explicitly: `/logout`, `/signout`, anything with `logout` in the path.

Test your auth setup manually with a single request before starting the scan. Scanner logs that say "2000 URLs scanned" mean nothing if they're all 302 redirects to login.

### 4. Scan strategy

Not every scan is the same scan. Choose deliberately.

- **Baseline (passive only)** — ZAP fetch + passive analyze without active payloading. Catches: missing security headers, wrong cookie flags, verbose error pages, information disclosure. Fast (~2 min), safe for per-PR CI. This is the CI default.
- **Full scan (passive + active)** — ZAP active-scan sends XSS/SQLi/path-traversal payloads. Longer (30–90 min, depending on app size), heavier on the target. Schedule weekend / nightly against staging.
- **API scan** — OpenAPI spec import, walk every endpoint. Combine with phase 3 auth-state for authenticated API tests.
- **Targeted** — specific endpoint or flow after a new feature. Configure manually in Burp or via the ZAP Automation Framework.

Calibrate payloads upfront:

- **Safe actives**: reflected XSS, basic SQLi, path-traversal, command-injection, open redirect. The default ZAP set is fine for these.
- **Potentially destructive**: the `postgresql` and `mysql` injection package can unintentionally modify data when the app lacks prepared statements. Disable against environments you cannot restore.
- **DoS class**: slowloris, buffer-overflow probes. Not active without explicit agreement.

### 5. Triage of findings

DAST scans produce many findings, most of them false positives.

- **Baseline hygiene**: after the first scan create a baseline file (ZAP `--report-file` then `-z "-config json.report.file=<file>"`, or Burp equivalent). Subsequent runs: diff against baseline, surface only new findings.
- **False-positive patterns**: reflected-XSS claims on endpoints that echo the payload back in a JSON body with `Content-Type: application/json` — the browser doesn't render it as HTML. SQLi claims on endpoints that 500 on every input, not just SQL syntax. Server-header-based version disclosure on endpoints that deliberately return a version header.
- **Verify by hand**: for every serious finding, reproduce manually with curl or Burp Repeater. A DAST tool that says `High: SQL Injection` without a working payload is speculation.
- **Tie to CWE + OWASP**: map findings in the report to known categories (see `security-review` phase 6). DAST tools usually do this automatically; verify the mapping is correct.

### 6. CI integration

- **Per PR**: ZAP baseline scan against an ephemeral preview environment (Vercel preview, Heroku review-app, ephemeral K8s namespace). Fail on new High findings within the diff scope.
  ```yaml
  # GitHub Actions example
  - uses: zaproxy/action-baseline@v0.13.0
    with:
      target: ${{ env.PREVIEW_URL }}
      rules_file_name: .zap/rules.tsv
      cmd_options: '-a'
  ```
- **Nightly or weekly**: ZAP full-scan or Burp Enterprise against staging. Findings to a security issue tracker, not to PR comments (too noisy).
- **Rules file** (`.zap/rules.tsv`) for suppressing false-positive rule IDs with a rationale per entry.
- **Auth state in CI**: a test user dedicated to scans, credentials in CI secrets (see `cicd-hardening` phase 3). Rotation on incident, not on schedule.
- **SLA on findings**: tie output to a `cve-triage`-style triage matrix — a new High in a production-relevant endpoint is fix-sprint; baseline-hygiene (e.g. missing HSTS) is fix-quarter.

### 7. Verification-loop

Layer 1: scope (every in-scope host scanned, no out-of-scope hosts hit accidentally, auth-state worked during the scan?), assumptions ("we are authenticated" only when the logged-in indicator actually matches), gaps (which pages were not crawled and why; are there unmet assumptions there?), consistency (do finding severities match between DAST report and security-review taxonomy?).

Layer 2: no fabricated CVE-IDs from scan output, payloads at pattern-level in the report (no ready-to-fire exploits for production targets), false-positive claims backed by a concrete repro test (the "we verified by hand" claim has to be true).

## Output

```
DAST scan — <app>, <environment>
Tool:           <ZAP x.y | Burp Pro | Burp Enterprise | Nuclei>
Scan type:      <baseline | full | API | targeted>
Duration:       <HH:MM>, requests sent: <N>

Scope:
  In:           <host(s)>
  Out:          <paths, e.g. /logout, /admin/wipe-*>
  Auth:         <mode, test user, logged-in indicator verified>

Findings (pre-triage total):
  High:          N    (confirmed: X, FP: Y, verify pending: Z)
  Medium:        N
  Low:           N
  Informational: N (don't report unless notable)

Confirmed for delivery (manually verified):
## [HIGH] <short title>
  Location:      <URL + method>
  Classification: CWE-<N> | OWASP A0<x>
  Reproduction:   <curl or Burp Repeater request>
  Impact:        <what can the attacker do>
  Fix:           <concrete direction; handoff to framework skill or secure-coding>

## [MEDIUM] ...

Baseline hygiene (security headers, etc.):
  HSTS: <present/absent>
  CSP:  <present + strictness>
  etc.

Handoffs:
  Dep-vulns detected via runtime: <cve-triage>
  Suspected design issue:         <threat-modeler>
  Exploitation depth needed:      <web-exploit-triage>

Verification-loop: ...
```

Raw tool report (ZAP HTML, Burp XML) as an attachment, not inline. The reviewer reads the summary and clicks through for detail.

## References

- OWASP ZAP — [https://www.zaproxy.org/](https://www.zaproxy.org/). Tool, docs, Automation Framework.
- ZAP Automation Framework — [https://www.zaproxy.org/docs/automate/automation-framework/](https://www.zaproxy.org/docs/automate/automation-framework/). YAML-based CI scan configuration.
- PortSwigger Burp Suite — [https://portswigger.net/burp](https://portswigger.net/burp). Professional and Enterprise docs.
- Burp Collaborator — [https://portswigger.net/burp/documentation/collaborator](https://portswigger.net/burp/documentation/collaborator). Out-of-band detection for blind-injection classes.
- OWASP Web Security Testing Guide (WSTG) — [https://owasp.org/www-project-web-security-testing-guide/](https://owasp.org/www-project-web-security-testing-guide/). Methodology backbone for web testing.
- OWASP Automated Threat Handbook — [https://owasp.org/www-project-automated-threats-to-web-applications/](https://owasp.org/www-project-automated-threats-to-web-applications/). Reference for scan-related threat classes.
- NIST SP 800-115 — [https://csrc.nist.gov/pubs/sp/800/115/final](https://csrc.nist.gov/pubs/sp/800/115/final). Technical Guide to Information Security Testing; §5 covers dynamic testing.
- Nuclei — [https://github.com/projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei). Template-based scanner, complement to ZAP/Burp.
- zaproxy/action-baseline — [https://github.com/marketplace/actions/zap-baseline-scan](https://github.com/marketplace/actions/zap-baseline-scan). Out-of-the-box GitHub Action for CI.

## Categories

- appsec
