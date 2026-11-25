---
name: recon-screenshot-map
description: Screenshot-based surface mapping for authorized web assets using headless browser automation — capture visual snapshots of every live HTTP/HTTPS service, organize by technology and response pattern, detect default installs, error pages, and login portals visually. Every screenshot requires scope validation and gated browser automation. Output is a visual asset map for rapid triage and report enrichment.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [screenshot-index, command-log, redacted-evidence, finding-draft]
---

# Screenshot mapping — visual asset inventory with headless browser automation

Use this skill to capture visual snapshots of every live HTTP/HTTPS service in the target scope. Automated screenshots reveal the "face" of each web asset — default CMS installs, admin login panels, error pages, captive portals, maintenance pages, and custom applications — that status codes and headers alone cannot describe. A screenshot gallery enables rapid triage: an operator can visually scan hundreds of web assets in minutes and flag high-interest targets. Every browser request requires scope validation and authorization.

## Required inputs

- Live URL list from `recon-subdomain`, `recon-web-surface`, or equivalent (hosts with HTTP/HTTPS services confirmed).
- Scope file with authorized hosts and any restrictions on browser automation.
- Rate limits: max concurrent browser instances, max screenshots per minute, viewport/rendering preferences.
- Authorization cache valid for every target host.
- Optional: authentication credentials for screenshotting behind login (session cookie or token).

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before launching any browser automation.
2. `pentest_agent_parse_scope` to validate every URL before screenshotting.
3. `pentest_agent_validate_target` for each host.
4. `pentest_agent_check_authorization` before any browser request to the target.
5. `pentest_agent_build_command` for dry-run argv preview of screenshotting commands.
6. `pentest_agent_execute_tool` for all browser automation — rate-limit, timeout, bounded output.
7. `pentest_agent_append_evidence` with screenshot metadata and redacted visual findings.

## Workflow

### Phase 1 — screenshot capture setup

Choose and configure a headless browser automation tool for batch screenshot capture.

1. **Tool selection**:
   - **gowitness** (Go, fast, stable): `gowitness scan file --file url_list.txt --screenshot-path screenshots/ --write-db --chrome-path /usr/bin/chromium`
     - `--screenshot-path`: output directory. `--write-db`: SQLite database of results for later querying.
     - Pros: fast, well-maintained, supports Chrome/Chromium, produces clean reports.
   - **aquatone** (Go, classic): `cat url_list.txt | aquatone -out aquatone_output/ -ports 80,443,8080,8443`
     - Aquatone also groups screenshots by similarity in its HTML report. Useful for detecting clusters of identical error pages or CDN challenge pages.
   - **eyewitness** (Python, more features): `eyewitness --web -f url_list.txt -d eyewitness_output/ --no-prompt --timeout 15 --threads 10`
     - Eyewitness can also capture response headers in its report, combining screenshot + metadata.
   - **Playwright/Puppeteer** (custom, for complex auth flows): custom Node.js script using `playwright` to navigate, authenticate, and screenshot. Use only if authentication is required and other tools cannot handle the auth flow.
2. **Browser configuration**:
   - Viewport: 1440x900 (standard desktop), 1920x1080 (full-HD) for high-resolution capture.
   - User-Agent: match a recent Chrome/Firefox UA string. Some sites serve different content to headless browsers.
   - Timeout: 15 seconds per URL. Sites that take longer are likely broken, slow-loading, or behind a WAF challenge.
   - JavaScript: enabled (render SPAs). If the site is purely static HTML, disabling JS may speed up capture, but most modern sites require JS rendering.
   - Accept insecure TLS: consider enabling `--ignore-certificate-errors` in Chrome/Chromium if the target uses self-signed certificates (common in dev/staging).
3. **Pre-capture normalization**:
   - Ensure URLs include scheme (https://). If scheme is unknown, try HTTPS first, fall back to HTTP.
   - Remove fragments (`#section`) — they don't change the page visual.
   - Skip non-HTTP services (SSH, FTP, SMTP) — these cannot be screenshotted.

### Phase 2 — batch capture and organization

Run the batch screenshot tool and organize output for triage.

1. **Run capture** with rate-limited parallelism:
   - Max 5 concurrent browser instances. Each headless browser consumes ~200-400 MB of memory. Do not exceed system resources.
   - Rate limit: 120 screenshots per minute (2 per second). This avoids triggering WAF rate-limiting.
   - Total timeout: 15 seconds per URL.
2. **Capture specific URL variations per host**:
   - Root URL: `https://TARGET.COM/`
   - HTTP (if HTTPS is not available or redirects): `http://TARGET.COM/`
   - Common paths if already known: `/admin`, `/login`, `/api` (if the API returns HTML, it's an API documentation or dashboard).
   - Alternative ports: 8080, 8443, 3000, 5000, 8000 (if port scanning confirmed these are open with HTTP services).
3. **Organize output**:
   - Group screenshots by host, then by port, then by path.
   - Rename files from tool default (often URL-hash) to human-readable: `TARGET_COM_443_root.png`, `TARGET_COM_443_admin.png`.
   - Keep tool metadata: HTTP status code, title, server header, response time — these add context to the screenshot.

### Phase 3 — visual triage

Visually scan the screenshot gallery and classify assets by category and interest level.

1. **Classification categories**:
   | Visual signal | Classification | Interest level |
   |---|---|---|
   | Default CMS install page (WordPress, Drupal, Joomla) | Neglected CMS | HIGH — check for known CVEs |
   | Admin login panel (Jenkins, Grafana, Kibana, phpMyAdmin, Tomcat, Webmin) | Exposed admin panel | HIGH — test for default credentials |
   | Login page with "Forgot password" link | Auth portal | MEDIUM — test auth workflows |
   | Directory listing (file tree with parent directory link) | Information disclosure | HIGH — enumerate directory contents |
   | Default web server page (Apache, nginx, IIS welcome) | Default install / empty | LOW — may be intentional |
   | Error page with stack trace or debug info | Information disclosure | HIGH — error details leak framework/version |
   | Maintenance page ("Under construction", "Not yet launched") | Static | LOW — may have hidden content |
   | CDN/WAF challenge page (Cloudflare "Checking your browser") | CDN/WAF fronted | MEDIUM — flag for WAF bypass testing |
   | Blank white page or 404 (no content) | Empty | LOW — no visible application |
   | Custom web application (unique branding, dashboard, data tables) | Active application | HIGH — primary assessment target |
   | API error page (JSON/XML error in browser) | API exposed as HTML | MEDIUM — check API docs, version |
   | Internal tool (Jira, Confluence, GitLab, Bitbucket) | Internal tools exposed | HIGH — test for auth bypass |
   | Login with SSO/OAuth buttons ("Login with Google", "Login with Microsoft") | SSO integration | MEDIUM — test OAuth flows |
   | phpinfo() page (PHP configuration dump) | Critical info disclosure | CRITICAL — full server config exposed |
2. **Flagging criteria**:
   - **CRITICAL**: phpinfo(), .env file rendered as HTML, database error message with credentials in output, source code visible (`.git` directory browsable).
   - **HIGH**: default admin panel without apparent authentication, directory listing of sensitive paths, stack traces with file paths, Jenkins/Grafana/Kibana without login wall.
   - **MEDIUM**: login portals with email enumeration, CMS with known version in footer, error page with framework name and version.
   - **LOW**: custom application (needs assessment), static marketing page, CDN-challenge page.

### Phase 4 — report and handoff

Generate a visual asset report and hand off high-interest targets.

1. **Generate HTML report** (if tool supports it):
   - `gowitness report generate` produces an HTML gallery with screenshots and metadata.
   - `aquatone` automatically generates an HTML report grouped by visual similarity.
   - This HTML report can be shared with the operator or appended to the engagement report as an appendix.
2. **Hand off high-interest targets**:
   - Default CMS installs → `tech-wordpress`, `tech-docker`, `tech-tomcat` (based on identified CMS).
   - Admin panels → `vuln-sensitive-exposure` (for default credentials), `auth-workflow` (for auth bypass).
   - Directory listings → `vuln-sensitive-exposure` (enumerate further).
   - Error/debug pages → `vuln-sensitive-exposure` (information disclosure pattern classification).
   - Custom applications → `recon-web-surface` (deeper fingerprinting if not already done).
3. **Screenshot storage**:
   - Store screenshots under the engagement evidence directory: `.pi/pentest-agent/engagements/<id>/evidence/screenshots/`.
   - Include the HTML gallery report and individual PNG files.
   - Do NOT store screenshots that contain PII, credentials in rendered HTML, or internal hostnames/images without redaction.

## Decision points

- **All URLs return the same screenshot** (CDN challenge page, captive portal): the target is behind a protective layer that intercepts unauthenticated/unproxied requests. Stop screenshotting, document the CDN/WAF, and hand off to `enum-waf-tech`.
- **Screenshot shows a login page with SSO only (no password login)**: the application is federated. Test OAuth/SSO configuration, not password attacks.
- **Screenshot reveals internal hostnames or IPs in page content** (e.g., "Connected to db-internal.TARGET.local"): redact from evidence. Flag as information disclosure finding.
- **Screenshot contains what appears to be customer data or PII**: redact immediately. Stop screenshotting that specific URL and flag for operator review. Do not store the raw screenshot in evidence.
- **Browser crashes or times out on a specific URL**: the site may be intentionally crashing headless browsers (anti-bot technique). Flag as "headless-browser detection active" and note that manual review is needed.

## Prohibited behavior

- Screenshotting out-of-scope hosts or URLs.
- Interacting with the page beyond loading it for screenshot (no clicks, no form submissions, no script execution beyond initial page load).
- Downloading files, submitting forms, or triggering actions during screenshot capture.
- Using browser automation to exfiltrate page content beyond what is visible in a screenshot.
- Storing screenshots that contain PII, credentials, or unreleased product features in unredacted form.
- Running browser automation at rates that trigger WAF blocks or degrade target services.

## Stop conditions

- WAF/CDN blocks all requests with JavaScript challenge → stop. Document WAF presence.
- Browser process memory exceeds system limits → reduce concurrency.
- More than 20% of URLs return 404 or connection errors → the URL list may be stale. Refresh from `recon-subdomain` or `recon-web-surface` before continuing.
- A single screenshot reveals CRITICAL information (phpinfo, source code, database dump in HTML) → stop that host's capture, escalate finding.

## Evidence

For each screenshot, record: URL, HTTP status code, page title, server header, screenshot file path, and triage classification. Evidence template:

```text
Screenshot map for: TARGET.COM
Total URLs: 487 (from recon-web-surface)
Successful captures: 423 (87%)
Errors/timeouts: 64 (13% — includes WAF challenges, connection refused, non-HTTP services)

Classification:
  CRITICAL: 3
    - dev.TARGET.COM/phpinfo.php → full PHP 8.1 configuration dump [CRITICAL]
    - api.TARGET.COM/debug → stack trace with internal file paths [CRITICAL]
    - staging.TARGET.COM/.git/ → Git repository index browsable [CRITICAL]

  HIGH: 28
    - jenkins.TARGET.COM → Jenkins 2.426, login page, no auth prompt bypass [HIGH]
    - grafana.TARGET.COM → Grafana 10.2, login page, anonymous access disabled [HIGH]
    - admin.TARGET.COM → WordPress admin login, wp-login.php accessible [HIGH]
    - db.TARGET.COM:8080 → phpMyAdmin login page [HIGH]
    - wiki.TARGET.COM → Confluence, SSO redirect, on-premises instance exposed [HIGH]

  MEDIUM: 89
    - app.TARGET.COM/login → custom React app, auth portal with Google SSO [MEDIUM]
    - api.TARGET.COM/docs → Swagger UI, REST API documentation publicly viewable [MEDIUM]
    - cdn.TARGET.COM → CloudFront distribution, static assets only [MEDIUM]

  LOW: 213
    - Various CDN/WAF challenge pages, blank apps, static maintenance pages

  Empty/inaccessible: 90
    - 64 errors/timeouts, 26 non-HTTP services

Screenshot gallery: .pi/pentest-agent/engagements/<id>/evidence/screenshots/gallery.html
```

Redact PII, internal hostnames in page content, credential values in rendered error pages, and any customer data visible in screenshots.

## Report handoff

1. Include the screenshot gallery HTML as an appendix in the engagement report.
2. `pentest_agent_record_finding` for: phpinfo pages, exposed .git directories, database error messages with credentials, unauthenticated admin panels, and stack traces.
3. Hand off each CRITICAL and HIGH finding to its respective vulnerability skill.
4. Explicitly note: all screenshots were captured through passive page loading only, no interactions (clicks, form submissions) were performed, no files were downloaded, all hosts were scope-validated, and any PII/credentials visible in screenshots were redacted before storage.
