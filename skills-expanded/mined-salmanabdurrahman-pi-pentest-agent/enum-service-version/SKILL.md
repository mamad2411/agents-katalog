---
name: enum-service-version
description: "Service and technology version enumeration through multi-layer fingerprinting: HTTP response analysis, JavaScript artifact inspection, default-file probing, error-message parsing, and behavior-based detection. Maps every identified component to known vulnerability databases without active exploitation."
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, tech-stack-inventory, version-cve-map]
---

# Enum service version

Use this skill to fingerprint the technology stack of every in-scope target: web servers, application servers, backend frameworks, CMS platforms, JavaScript libraries, database engines, caching layers, and CDN providers. Version enumeration enables precise vulnerability matching and informs risk prioritization. This skill focuses on detection and classification; vulnerability validation is performed by downstream vuln-class skills.

## Required inputs

- Validated target list with in-scope hosts and endpoints.
- Scope file defining allowed testing methods and rate limits.
- Authorization cache valid for all in-scope hosts.
- Optional: technology stack documentation or software bill of materials (SBOM) provided by the target owner.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every target before contact.
3. Use `pentest_agent_check_authorization` before any active probe that generates traffic.
4. Use `pentest_agent_build_command` for dry-run preview of fingerprinting tools.
5. Use `pentest_agent_execute_tool` for all active probing with rate-limit and output policy enforcement.
6. Use `pentest_agent_append_evidence` for technology inventories, version evidence, and CVE mappings.

## Workflow

### Phase 1 — Passive technology detection from responses

Extract technology indicators from normal HTTP responses without sending specialized probes.

- For each in-scope endpoint, collect response headers that indicate technology: `Server`, `X-Powered-By`, `X-Generator`, `X-Drupal-Cache`, `X-Joomla-Cache`, `Set-Cookie` session-cookie name patterns.
- Map session-cookie names to technologies: `PHPSESSID` → PHP, `JSESSIONID` → Java/Tomcat/Jetty, `ASP.NET_SessionId` → ASP.NET, `laravel_session` → Laravel, `_session_id` → Rails, `connect.sid` → Express.js, `django_session` → Django.
- Inspect HTML source for generator meta tags: `<meta name="generator" content="WordPress 6.4.2">`, `<meta name="generator" content="Drupal 10">`.
- Inspect HTML for framework-specific markup: React root element IDs (`#root`, `#__next`, `#app`), Angular attributes (`ng-version`, `_nghost`), Vue.js attributes (`data-v-`), or Svelte markers.
- Inspect CSS and JS URLs for versioned filenames: `jquery-3.7.1.min.js`, `bootstrap-5.3.2.min.css`, `font-awesome/4.7.0/css/`.
- Inspect HTTP response bodies for version strings in comments, JSON responses, or error messages: `<!-- Built with Hugo 0.121.1 -->`, `"apiVersion": "v2"`, `"django_version": "4.2.7"`.
- Document every technology indicator with the source (header, HTML, JS, CSS, error) and confidence level.

### Phase 2 — Active fingerprinting with catalog tools

Use catalog fingerprinting tools to detect technologies that passive collection misses.

- Select fingerprinting tools from the catalog appropriate to the target technology. Use `pentest_agent_build_command` for dry-run preview of each tool invocation.
- Use HTTP-focused fingerprinting tools (like `whatweb` or `httpx -tech-detect`) against each in-scope host. These tools match response patterns against signature databases and identify web servers, CMS platforms, JavaScript libraries, and analytics services.
- Use CMS-specific detection: WordPress (`/wp-login.php`, `/wp-json/`, `/wp-content/`), Drupal (`/user/login`, `/core/CHANGELOG.txt`), Joomla (`/administrator/`, `/components/`), Magento (`/admin/`, `/skin/frontend/`), and other platforms.
- For each detected technology, attempt version extraction: WordPress exposes version in `/feed/` generator tags, `/readme.html`, and CSS/JS URLs; Drupal exposes version in `/core/CHANGELOG.txt`; many frameworks expose version in default error pages or debug endpoints.
- Run template-based technology detection (like `nuclei -tags tech`) to identify exposed panels, admin consoles, and technology-specific paths that confirm technology presence.
- Do not probe paths that could trigger authentication lockouts, database connections, or state changes.

### Phase 3 — JavaScript library and frontend component detection

Client-side libraries are often the most version-precise indicators.

- Download and inspect all JavaScript bundles served by the target. Search for library version strings embedded in source: `jQuery v3.7.1`, `React v18.2.0`, `Vue.js v3.4.0`, `Angular v17`.
- Search for library-specific global identifiers: `window.jQuery`, `window.React`, `window.angular`, `window._` (Lodash/Underscore), `window.moment`.
- Inspect `package.json` or `bower.json` files if exposed at common paths (`/package.json`, `/bower.json`). These files list exact dependency versions.
- Inspect JavaScript source maps (`.js.map` files) if exposed. Source maps often reveal the original TypeScript/JSX source and build tooling.
- For SPAs, use the framework's developer-tools API (React DevTools, Vue DevTools, Angular DevTools signals in the DOM) to confirm framework version without sending additional requests.
- Document every detected library: name, detected version, detection method, and whether the version is current or outdated.

### Phase 4 — Default-file and path-based version detection

Default installation files and version-specific paths reveal exact software versions.

- Check for version-indicating default files: `CHANGELOG.txt`, `RELEASE_NOTES.txt`, `VERSION`, `README.md`, `LICENSE.txt`, `INSTALL.txt`, `UPGRADE.txt`.
- Check for framework-specific version files: WordPress `/readme.html`, Drupal `/core/CHANGELOG.txt`, Joomla `/administrator/manifests/files/joomla.xml`, Laravel `/composer.json`, Django `/requirements.txt`.
- Check for build-artifact paths: `/build/`, `/dist/`, `/static/version/`, `/assets/rev-manifest.json`. Build hashes and manifest files often include version data.
- Check for source-control metadata: `/.git/HEAD`, `/.svn/entries`. If accessible, they reveal the repository state and sometimes the last commit message including version tags.
- Check for CI/CD artifacts: `/.gitlab-ci.yml`, `/.github/workflows/`, `/Jenkinsfile`. These reveal build and deployment infrastructure.
- Probe with caution: many of these paths trigger 404 on a well-configured server. Only test paths consistent with technologies already detected. Do not brute-force large wordlists of version paths.

### Phase 5 — Error-message and debug-endpoint version extraction

Error messages and debug endpoints often expose precise version numbers.

- Trigger safe error conditions that are unlikely to affect availability: request a non-existent ID, send an invalid Content-Type, request a too-large page number, or omit a required parameter.
- Inspect error responses for version strings: `Django 4.2.7`, `Laravel 10.x`, `Spring Boot 3.2.0`, `Express 4.18.2`, `ASP.NET Core 8.0`.
- Check for framework debug endpoints: Spring Boot Actuator (`/actuator/info`, `/actuator/env`, `/actuator/health`), Django Debug Toolbar (`/__debug__/`), Laravel Telescope (`/telescope/`), Rails `/rails/info/routes`.
- Inspect 404 and 500 error pages for server signatures. Default error pages from Apache, Nginx, IIS, and Tomcat include server version in the footer or error message.
- Trigger OPTIONS or TRACE methods on API endpoints. Some servers reveal version in response headers only for non-standard HTTP methods.
- Stop error triggering if the server returns stack traces, database queries, or file paths. Record the information disclosure finding but do not continue probing that endpoint.

### Phase 6 — Version-to-vulnerability mapping

Translate detected versions into actionable CVE references.

- For each detected technology with a specific version, query vulnerability databases for known CVEs affecting that version. Use catalog tools or reference databases.
- Focus on CVEs with known public exploits, high or critical severity, and relevance to the technology's role (e.g., a remote-code-execution CVE in the web server is critical; an information-disclosure CVE in a static-asset library is low).
- Flag technologies running versions past end-of-life (EOL). EOL software receives no security patches and all future vulnerabilities are zero-day by definition.
- Cross-reference version data across hosts: if one host runs Apache 2.4.41 and another runs 2.4.57, the older host may be unpatched for CVEs fixed between those versions.
- Produce a technology inventory with CVE references, severity ratings, and remediation priority. This inventory informs downstream vulnerability-validation skills.

## Decision points

- Default-file probing: if a technology is detected with high confidence, probe the corresponding version files. If the technology is only tentatively identified, skip default-file probing to avoid noise.
- Error triggering: start with the safest error triggers (missing ID, invalid Content-Type). Only escalate to riskier triggers (malformed payloads, boundary values) if passive and active fingerprinting have failed to identify a critical component.
- Version-to-CVE mapping: do not claim a CVE is exploitable based on version alone. Mark detected versions as "potentially affected by CVE-X" and leave exploitation confirmation to vuln-validation skills.
- EOL software: flag EOL versions as critical-finding candidates regardless of known CVEs, because unreported vulnerabilities are likely.

## Prohibited behavior

No exploitation of detected CVEs. No triggering of error conditions that could cause service disruption, data corruption, or log flooding. No probing of debug endpoints that could expose production secrets or customer data. No brute-force scanning of version paths with large wordlists. No testing against out-of-scope hosts. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop fingerprinting a host when all key technology components are identified with version precision. Stop error triggering if the application returns stack traces or sensitive data. Stop if the target rate-limits or blocks fingerprinting requests. Stop if the authorization cache expires.

## Evidence

Append evidence via `pentest_agent_append_evidence`:
- Technology stack inventory with detection method and confidence per component.
- Detected version list with evidence source (header value, HTML snippet, file path).
- JavaScript library inventory with version and EOL status.
- Version-to-CVE mapping with severity and exploit-availability flags.
- EOL component list with remediation recommendation.

Never store debug-endpoint responses containing environment variables, database credentials, API keys, or internal infrastructure details. Redact version evidence that contains unique identifiers or timestamps.

## Report handoff

Record findings via `pentest_agent_record_finding` for: end-of-life software versions (critical), exposed version files (medium), debug endpoints with version information (medium), verbose error messages with version disclosure (low), and exposed source-control metadata (high). Generate the technology inventory as structured evidence for downstream vuln-validation skills. Render the final report with `pentest_agent_render_report`.
