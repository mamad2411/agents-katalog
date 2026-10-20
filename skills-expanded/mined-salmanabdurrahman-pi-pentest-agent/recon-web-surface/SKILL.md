---
name: recon-web-surface
description: Web surface mapping with technology fingerprinting, HTTP response analysis, virtual-host detection, and gated live probing — transforms raw URL/subdomain lists into a categorized asset inventory with technology-to-vulnerability routing. Every active probe requires authorization and scope validation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [web-asset-map, command-log, redacted-evidence, finding-draft]
---

# Web surface mapping — technology fingerprinting and live-asset inventory

Use this skill to map the web-accessible surface of an authorized target by fingerprinting technologies, analyzing HTTP responses, detecting virtual hosts, and routing discovered assets to the appropriate vulnerability-assessment skills. Input is a list of live URLs or subdomains (from `recon-subdomain`, `recon-archive-urls`, or direct scope specification). Output is a categorized asset inventory with technology stacks, server profiles, and routing recommendations for downstream skills.

## Required inputs

- Live URL or subdomain list from prior recon phases.
- Scope file with in-scope URL patterns, out-of-scope exclusions, and allowed HTTP methods/probe types.
- Rate limits: max requests per second, max concurrent connections.
- Authorization cache valid for every target host to be probed.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before active probing.
2. `pentest_agent_parse_scope` to validate every URL against in-scope/out-of-scope rules.
3. `pentest_agent_validate_target` for each host before sending requests.
4. `pentest_agent_check_authorization` before any HTTP request to a target host.
5. `pentest_agent_build_command` for dry-run argv preview of httpx, whatweb, nuclei tech-detect commands.
6. `pentest_agent_execute_tool` for all probing — rate-limit enforcement, bounded output.
7. `pentest_agent_append_evidence` with headers, technology data, and scope-filtered results.

## Workflow

### Phase 1 — HTTP response profiling

Send HTTP/HTTPS probes to every URL and capture response metadata: status codes, headers, redirects, and TLS certificate information.

1. **HTTPS-first probing with httpx** (prefer HTTPS, fall back to HTTP):
   - `httpx -l url_list.txt -sc -title -server -tech-detect -cdn -location -websocket -silent -t 50 -o httpx_full.txt`
   - `-sc`: status code. `-title`: page title (useful for identifying default installs, error pages, CMS patterns). `-server`: Server header value. `-tech-detect`: Wappalyzer-based technology signature matching. `-cdn`: detects if host is behind a CDN (Cloudflare, CloudFront, Fastly, Akamai). `-location`: follows and reports redirect Location headers. `-websocket`: flags WebSocket endpoints.
   - Rate limit: `-t 50` max concurrent unless scope specifies higher.
2. **Response header extraction** for all hosts:
   - `httpx -l url_list.txt -sc -server -x-powered-by -content-type -silent -json -o headers.json`
   - Parse the JSON for:
     - **Server header**: Apache, nginx, IIS, cloudflare, Netlify, Vercel, Express, Gunicorn, uWSGI, Tomcat, Jetty, Caddy, LiteSpeed.
     - **X-Powered-By**: PHP versions, ASP.NET versions, Express, Next.js (indicates framework and possible version).
     - **Set-Cookie**: PHPSESSID→PHP, JSESSIONID→Java/Tomcat, ASP.NET_SessionId→ASP.NET, laravel_session→Laravel, django_session→Django, connect.sid→Express/Node.
     - **Content-Type**: text/html (standard), application/json (API), application/xml (SOAP/XML service).
     - **Security headers** (present/absent): `Strict-Transport-Security` (HSTS), `Content-Security-Policy` (CSP), `X-Frame-Options` (clickjacking), `X-Content-Type-Options` (MIME sniffing), `Referrer-Policy`, `Permissions-Policy`.
3. **TLS certificate inspection**:
   - Extract TLS certificate Subject Alternative Names (SANs) for each HTTPS host:
   - `echo "TARGET.COM" | tlsx -san -silent -json | jq -r '.subject_an[]'`
   - SANs often reveal sibling domains, internal hostnames, and retired services not found through subdomain enumeration.
   - Check certificate validity period (expired certs = neglect signal), issuer (Let's Encrypt vs organization CA), and wildcard coverage.

### Phase 2 — technology fingerprinting

Identify the technology stack behind each web asset: web server, programming language, framework, CMS, JavaScript libraries, analytics, and CDN/WAF.

1. **Wappalyzer-style detection with httpx** (already run in Phase 1, extract tech data):
   - `cat headers.json | jq -r '.tech[]?'` — lists detected technologies per URL.
2. **WhatWeb for deeper fingerprinting**:
   - `whatweb -i url_list.txt --log-json whatweb_results.json`
   - WhatWeb uses ~1800 plugins to detect CMS, frameworks, analytics, JavaScript libraries, and more. It is slower but provides much richer detection than httpx alone.
   - Run with `--aggression 3` for passive + moderately active checks; `--aggression 4` does heavier requests that may trigger WAF/IDS.
3. **Nuclei technology detection templates**:
   - `nuclei -l url_list.txt -t technologies/ -silent -json -o nuclei_tech.json`
   - Nuclei's technology templates detect specific CMS, admin panels, and versioned software based on response fingerprints.
   - Run `-t technologies/` to detect generic technology, `-t exposed-panels/` for admin/management panels.
4. **Build technology inventory per host**:
   - Web server: Apache/2.4.57, nginx/1.24.0, cloudflare (CDN-fronted).
   - Framework: PHP/8.1, Laravel 10, React 18, Next.js 13.
   - CMS: WordPress 6.3 (detected from generator meta, wp-content paths).
   - JavaScript: jQuery 3.7, Bootstrap 5.3, Alpine.js.
   - Analytics: Google Analytics (UA-XXXXX), Google Tag Manager, Facebook Pixel, Hotjar.
   - CDN/WAF: Cloudflare, CloudFront, Fastly, Sucuri, Imperva, Akamai.

### Phase 3 — virtual-host detection and content comparison

Discover additional web applications hosted on the same IP address but accessed through different Host headers.

1. **Virtual-host brute-force** (scope-permitted, low-rate):
   - For each IP address in the inventory, test common virtual host names:
   - `ffuf -u http://<IP> -w virtual_host_wordlist.txt -H "Host: FUZZ.TARGET.COM" -fc 404 -t 20 -o vhost_results.json`
   - Wordlist should include: `www`, `admin`, `dev`, `staging`, `api`, `vpn`, `intranet`, `portal`, `blog`, `shop`, `cdn`, `static`, `assets`, `files`, `docs`, `help`, `support`, `status`, `monitor`, `test`.
   - This is active probing that sends custom Host headers — ensure scope permits Host-header manipulation.
2. **Compare response fingerprints** for IP-based vs Host-header-based requests:
   - Request `http://<IP>` directly — this is the default virtual host.
   - Compare title, content-length, redirects, and third-party includes with the named-host responses.
   - A different application on the same IP (without DNS) is a discovery finding.
3. **Content-negotiation variations**: request the same URL with different Accept headers (`Accept: application/json` vs `Accept: text/html`). Some applications expose API endpoints or different content based on Accept headers.

### Phase 4 — asset categorization and routing

Transform the technology inventory into actionable routing decisions that tell the operator which vulnerability skills to apply to which assets.

1. **Routing table — technology to target skills**:
   | Technology detected | Route to skill(s) |
   |---|---|
   | WordPress | `tech-wordpress`, `vuln-sqli`, `vuln-xss` |
   | PHP (generic) | `vuln-lfi-rfi`, `vuln-file-upload`, `vuln-ssti` |
   | Laravel | `framework-laravel`, `vuln-deserialization` |
   | Django | `framework-django`, `vuln-ssti` |
   | Express/Node.js | `framework-express`, `vuln-nosql`, `vuln-deserialization` |
   | Spring/Java | `framework-spring`, `vuln-deserialization` |
   | ASP.NET | `framework-dotnet`, `vuln-deserialization` |
   | Rails | `framework-rails`, `vuln-deserialization` |
   | GraphQL endpoint | `enum-graphql` |
   | REST API paths | `enum-api-surface` |
   | Jenkins | `tech-jenkins` |
   | Grafana/Kibana | `vuln-sensitive-exposure` |
   | Docker/Container headers | `container-docker` |
   | Kubernetes API | `container-kubernetes` |
   | Firebase/Firestore | `tech-firebase` |
   | Supabase | `tech-supabase` |
   | No anti-CSRF token + auth forms | `csrf` |
   | Missing security headers | `vuln-clickjacking`, `vuln-sensitive-exposure` |
   | CORS headers present | `cors` |
   | WebSocket detected | `websocket-security` |
   | File upload endpoints | `vuln-file-upload` |
   | Login/auth pages | `auth-workflow` |
   | OAuth redirects | `auth-oauth` |
   | JWT in responses | `auth-jwt` |

2. **Priority categorization**:
   - **Priority 1** (probe immediately): admin panels with default credentials, exposed .env/config files, debug endpoints with stack traces, API endpoints with sensitive data in responses.
   - **Priority 2** (schedule): CMS with known vulnerabilities, framework with version-specific CVEs, auth pages without CSRF protection, file upload endpoints.
   - **Priority 3** (background): static sites, CDN-fronted marketing pages, read-only informational endpoints.

3. **Out-of-scope filtering**: mark any host flagged as out-of-scope by `pentest_agent_validate_target` as `NO_ROUTE`. Do not hand off to any active skill.

## Decision points

- **CDN or WAF detected**: all probes to this host pass through the CDN/WAF. Direct-to-origin testing is out-of-scope unless the scope file explicitly lists origin IPs. Flag the host as CDN-fronted and note that WAF may interfere with validation probes.
- **Default CMS install detected** (e.g., WordPress with default theme, no customizations): the target may be neglected — prioritize for known-CVE checks but avoid destructive testing without approval.
- **Exposed .git directory** (HTTP 200 on `/.git/HEAD`): CRITICAL finding. Source code disclosure. Stop current phase and record immediately.
- **Exposed .env file** (HTTP 200 on `/.env`): CRITICAL finding. May contain database credentials, API keys, APP_KEYs. Redact all values immediately. Flag as `vuln-sensitive-exposure`.
- **Server header reveals exact version** (e.g., `Apache/2.4.49`): check for known CVEs specific to that version. Apache 2.4.49 and 2.4.50 have critical path traversal (CVE-2021-41773, CVE-2021-42013).
- **Multiple distinct applications on same IP** (virtual-host discovery): this may indicate shared hosting or multi-tenant deployment. Ensure scope covers all discovered applications before probing.

## Prohibited behavior

- HTTP requests to any host not validated through `pentest_agent_validate_target`.
- Probing out-of-scope virtual hosts discovered through IP-based requests.
- Aggressive crawling or spidering without scope permission (directory brute-force goes to `enum-web-content`).
- Sending payloads or injection attempts during fingerprinting — this is a mapping phase, not validation.
- Interacting with login/auth forms beyond what is necessary for fingerprinting (no credential testing).
- Sending requests to CDN origin IPs unless explicitly authorized in scope.

## Stop conditions

- WAF/IDS blocks probes (429 Too Many Requests, 403 Forbidden with challenge page) → stop, document WAF presence, reduce rate.
- All hosts return the same response (CDN challenge page, captive portal, WAF block) → the entire surface is fronted by a protective layer. Document and hand off to `enum-waf-tech`.
- `pentest_agent_validate_target` rejects all hosts as out-of-scope → stop, document scope boundary.
- No HTTP services detected on any host → the target surface may be non-HTTP (DNS, SMTP, FTP, SSH). Hand off to protocol-specific skills.

## Evidence

For each probed host, record: IP, status code, title, server header, detected technologies, CDN/WAF status, TLS certificate SANs, security header posture, virtual-host discoveries, and skill-routing recommendations. Evidence template:

```text
Web surface map for: TARGET.COM

Hosts probed: 487 (from subdomain recon)
Live HTTP services: 423 (312 HTTPS, 111 HTTP redirect to HTTPS)
Technology inventory:
  - Apache/2.4.57: 156 hosts
  - nginx/1.24.0: 203 hosts
  - cloudflare (CDN): 289 hosts fronted
  - WordPress 6.3: 12 hosts
  - PHP 8.1/8.2: 178 hosts
  - Laravel: 8 hosts (detected via Set-Cookie laravel_session)
  - React 18: 34 hosts (detected via bundled JS)
  - Express/Node.js: 23 hosts (detected via X-Powered-By: Express)
  - Java/Spring: 2 hosts (JSESSIONID cookie)
  - Jenkins: 1 host (jenkins.TARGET.COM, Jetty, Jenkins 2.426)
  - Grafana: 1 host (grafana.TARGET.COM, Go)
  - GraphQL endpoint: 3 hosts (/graphql returning application/json)

Security header posture:
  - HSTS: 312/423 (74%) — 111 missing
  - CSP: 89/423 (21%) — 334 missing
  - X-Frame-Options: 203/423 (48%) — 220 missing
  - X-Content-Type-Options: 267/423 (63%) — 156 missing

Virtual-host discovery:
  - 203.0.113.50: default vhost is "Welcome to nginx", admin.TARGET.COM resolves to WordPress 
    → two distinct applications on same IP

Routing recommendations:
  → tech-wordpress: 12 WordPress hosts
  → framework-laravel: 8 Laravel hosts
  → framework-express: 23 Express hosts
  → tech-jenkins: 1 Jenkins host (Priority 1)
  → enum-graphql: 3 GraphQL endpoints
  → vuln-clickjacking: 220 hosts without X-Frame-Options
  → vuln-sensitive-exposure: 1 host with exposed .git (CRITICAL)
```

Redact internal IPs, server version details that could be used for targeted attacks in shared evidence, and any PII from page titles or Cookie values.

## Report handoff

1. `pentest_agent_record_finding` for: exposed .git/.env/config files, unauthenticated admin panels, end-of-life software versions, missing security headers on sensitive applications.
2. Route each asset category to the appropriate vulnerability skill per the routing table above.
3. Package the technology inventory as structured JSON evidence so downstream skills can query it without re-probing.
4. Explicitly note: all HTTP probes were rate-limited, no out-of-scope hosts were contacted, no payloads or exploits were delivered during mapping, and CDN-fronted hosts were not probed at origin.
