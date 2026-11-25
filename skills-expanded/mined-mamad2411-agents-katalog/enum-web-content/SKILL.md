---
name: enum-web-content
description: Web content enumeration and directory discovery across in-scope targets. Covers directory and file path probing, virtual host discovery, interesting-file detection, backup and config-file exposure, and content-structure mapping. All active probing is rate-limited, scope-bound, and authorization-gated.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, content-inventory, exposed-file-report]
---

# Enum web content

Use this skill to enumerate web-accessible content on in-scope targets: directories, files, virtual hosts, backup artifacts, configuration files, and exposed administrative interfaces. Content enumeration moves from passive sources (robots.txt, sitemaps, JavaScript references) to active probing with small, targeted wordlists. Every active probe must stay within rate limits, scope boundaries, and authorization gates.

## Required inputs

- Validated target list with base URLs for all in-scope web endpoints.
- Scope file defining allowed probing methods, path exclusions, rate limits, and testing windows.
- Authorization cache valid for all in-scope hosts.
- Wordlist or content corpus appropriate to the target technology stack. Use small, focused lists; avoid generic million-entry wordlists.
- Optional: sitemap files, API documentation, or content inventories provided by the target owner.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every host, base URL, and virtual host before contact.
3. Use `pentest_agent_check_authorization` before any active probe.
4. Use `pentest_agent_build_command` for dry-run preview of content-discovery and fuzzing tools.
5. Use `pentest_agent_execute_tool` for all active probing with rate-limit, timeout, and output policy enforcement.
6. Use `pentest_agent_append_evidence` for content inventories, exposed-file reports, and discovery logs.

## Workflow

### Phase 1 — Passive content discovery from documentation and references

Gather content paths from sources the target intentionally publishes.

- Fetch and parse `robots.txt` for every in-scope host. The `Allow` and `Disallow` directives reveal paths the site owner considers sensitive. A `Disallow: /admin/` entry confirms the admin path exists.
- Fetch and parse `sitemap.xml` and any linked sitemap index files. Sitemaps enumerate URLs the site owner wants indexed; they often reveal content not linked from the main navigation.
- Fetch and parse `security.txt` at `/.well-known/security.txt` for security contact information.
- Inspect the HTML source of the main page and key landing pages for: `<a href>` links to internal paths, `<script src>` and `<link href>` referencing internal static resources, `<img src>` paths revealing asset directories, and `<form action>` endpoints.
- Inspect JavaScript bundles for path references: route definitions (React Router, Vue Router), API endpoint strings, asset URLs, and webpack chunk references.
- Document all passively discovered paths with their source.

### Phase 2 — Directory and file path probing

Probe for common directory and file paths using small, technology-targeted wordlists.

- Select a wordlist appropriate to the target technology. For unknown tech stacks, start with a small common-paths list (~100-200 entries): `admin`, `login`, `api`, `backup`, `config`, `debug`, `docs`, `files`, `includes`, `logs`, `temp`, `test`, `uploads`, `vendor`.
- Use catalog content-discovery tools (like `ffuf`, `feroxbuster`, or `dirsearch`) from the catalog. Use `pentest_agent_build_command` for dry-run preview and `pentest_agent_execute_tool` for controlled execution.
- Configure the tool for the target's rate-limit parameters:
  - Thread count: ≤5 for strict targets, ≤20 for moderate targets.
  - Delay between requests: ≥200ms for strict targets, ≥50ms for moderate targets.
  - Match HTTP status codes: 200, 201, 204, 301, 302, 307, 401, 403. A 403 Forbidden confirms the path exists but is access-protected. A 401 Unauthorized likewise. Both are findings, not negatives.
  - Filter HTTP status codes: 404, 400, 405, 500, 502, 503 (noise and server errors).
- For each discovered path, record: URL, HTTP status code, response size, redirect target (for 30x), and whether the response differs from the site's standard 404 page (custom error pages can mask path existence).
- Test discovered directories recursively with a shorter wordlist (20-30 entries) to find nested content. Limit recursion to 2 levels.

### Phase 3 — Interesting-file detection

Check for exposed sensitive files that should not be publicly accessible.

- Common sensitive files by technology:
  - Generic: `.env`, `.env.bak`, `.env.local`, `.env.prod`, `.env.development`, `.git/config`, `.git/HEAD`, `.svn/entries`, `.DS_Store`, `Thumbs.db`.
  - PHP: `config.php`, `config.php.bak`, `wp-config.php`, `wp-config.php.bak`, `settings.php`, `database.php`.
  - Python: `settings.py`, `settings.py.bak`, `config.py`, `requirements.txt`, `Pipfile`, `Pipfile.lock`.
  - Node.js: `package.json`, `package-lock.json`, `.npmrc`, `server.js`, `app.js`.
  - Ruby: `Gemfile`, `Gemfile.lock`, `config/database.yml`, `config/secrets.yml`.
  - Java: `application.properties`, `application.yml`, `pom.xml`, `build.gradle`, `WEB-INF/web.xml`, `WEB-INF/classes/`.
  - Docker/Kubernetes: `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `k8s/`, `helm/`.
  - CI/CD: `.gitlab-ci.yml`, `Jenkinsfile`, `.github/workflows/`, `.travis.yml`, `azure-pipelines.yml`.
- For each file check, send a single GET request. Do not brute-force with extension variants unless the file name pattern is confirmed.
- Flag any file that returns content (200) or redirects (30x). A 200 OK on `.env` or a database config file is a critical finding.
- Flag files that return 403 Forbidden: the file exists but is access-protected. The protection may be bypassable via other methods.
- Flag files that return 401 Unauthorized: the file requires authentication that may be tested in a later phase.
- Do not download or store the content of exposed sensitive files beyond the first few bytes needed to confirm their nature. If a file contains secrets, stop immediately and record the finding category without storing the content.

### Phase 4 — Virtual host discovery

Discover content served on different Host headers.

- Identify the target's IP address(es) through DNS resolution.
- Send requests to the IP address with different Host header values: known subdomains from recon, common virtual host names (`dev`, `staging`, `uat`, `admin`, `internal`, `portal`, `mail`, `vpn`, `api`, `ws`), and permutations of the main domain.
- Compare response content, status code, and headers across Host values. A different response confirms a virtual host.
- Use a focused virtual-host wordlist (50-100 entries). Do not brute-force thousands of hostnames — this triggers IDS alerts and is rarely productive.
- Test whether the IP address itself serves a default site when no Host header or an unrecognized Host is provided. The default site often leaks internal information.
- Document discovered virtual hosts with the differentiated response evidence.

### Phase 5 — Backup, archive, and temporary file detection

Locate accidentally published backup and editor files.

- For each discovered content path and file, test common backup and editor artifact suffixes:
  - Backup: `.bak`, `.old`, `.orig`, `.backup`, `.save`, `.tmp`, `.swp`, `~`, `-`, `.1`, `.2`.
  - Archives: `.zip`, `.tar.gz`, `.tgz`, `.tar`, `.7z`, `.rar`.
  - Editor: `.swp` (Vim), `~` (Emacs/Gedit backup), `.swo` (Vim), `.save` (nano).
  - Version control: `.git/index`, `.svn/wc.db`, `.hg/store`.
- Test common backup directory names: `/backup/`, `/backups/`, `/db/`, `/database/`, `/sql/`, `/dump/`, `/export/`, `/archive/`, `/old/`, `/previous/`.
- If a backup file is discovered, do not download it beyond confirming its existence (head request or first bytes). Backup files can contain full database dumps, credential sets, and source code.
- Document discovered backup artifacts with path, estimated size (from Content-Length header), and content-type.

### Phase 6 — Content-structure mapping and reporting

Build a content map that informs the next testing phases.

- Organize discovered content by functional area: authentication pages, administrative interfaces, API endpoints, file upload/download paths, user-content areas, static assets, third-party integrations.
- For each functional area, note the authentication requirement and any interesting behaviors observed during discovery: custom error pages, redirect chains, parameter handling, content-type variations.
- Cross-reference discovered paths against the scope file. Flag any path that appears to be outside the authorized scope (e.g., a path on a third-party domain, or a path pointing to a backend system).
- Produce the content-structure map as structured evidence for downstream enumeration and vulnerability-validation skills.

## Decision points

- Wordlist selection: if the target technology is identified, use a technology-specific wordlist (WordPress paths, Django paths, Spring Boot paths). Generic wordlists produce high noise and low signal on known-technology targets.
- Recursion depth: if the initial directory probe finds 50+ directories, recurse only into directories with high-value names (`admin`, `api`, `backup`, `config`, `internal`). Do not recurse into asset directories (`images`, `css`, `js`, `fonts`).
- Backup file checks: if a backup file is detected, stop probing for additional backup variants on that path and escalate to a finding. Do not enumerate all possible backup extensions once one is confirmed.
- Virtual host scope: only test Host values corresponding to subdomains known to be in scope. Do not probe Host values outside the authorized target domain unless the scope explicitly includes virtual-host discovery.

## Prohibited behavior

No brute-force with large wordlists (thousands of entries). No downloading of discovered files beyond the minimum needed to confirm existence. No accessing, storing, or copying backup files, database dumps, or configuration files containing credentials. No probing of out-of-scope hosts, subdomains, or IP addresses. No recursive probing beyond 2 directory levels. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop content probing on a host when: the rate-limit budget for that host is exhausted, you encounter an exposed backup or credential file (escalate to finding immediately), a WAF starts returning challenge pages, or the authorization cache expires. Stop the full enumeration when all in-scope hosts are mapped and all interesting-file checks are complete.

## Evidence

Append evidence via `pentest_agent_append_evidence`:
- Passively discovered path list with sources.
- Active-probe results: path, status code, response-size bucket, content-type, redirect target.
- Exposed sensitive-file report: path, detection method, risk classification, whether content was confirmed.
- Virtual host inventory with response differentiation evidence.
- Backup artifact report: path, estimated size, content-type.
- Content-structure map organized by functional area.

Never store content of exposed files, backup archives, database dumps, or configuration files. For confirmed sensitive-file exposures, record the path and response metadata only. Redact any credentials, tokens, or secrets observed in response previews.

## Report handoff

Record findings via `pentest_agent_record_finding` for: exposed `.env` or configuration files (critical), exposed `.git` directory (critical), backup files containing data (critical), exposed database dumps (critical), admin panels without IP restriction (high), exposed version-control metadata (medium), directory listing enabled (medium), and exposed editor temporary files (low). Generate the content-structure map as structured evidence for downstream testing phases. Render the final report with `pentest_agent_render_report`.
