---
name: enum-waf-tech
description: "WAF and protection-layer enumeration: detect presence, type, and version of Web Application Firewalls, CDN security layers, rate-limit mechanisms, and bot-protection services. Maps the defensive posture without attempting bypass or evasion."
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, waf-inventory, protection-profile]
---

# Enum WAF and protection technology

Use this skill to detect, identify, and profile Web Application Firewalls (WAFs), CDN security layers, rate-limit mechanisms, and bot-protection services deployed in front of in-scope targets. Knowing the defensive layer informs tool selection, rate-limit tuning, and risk assessment for downstream testing. This skill enumerates defenses; it does not attempt to bypass or evade them.

## Required inputs

- Validated target list with all in-scope hosts and endpoints.
- Scope file defining allowed testing methods, rate limits, and any WAF-specific testing restrictions.
- Authorization cache valid for all in-scope hosts.
- Optional: architecture documentation or WAF/CDN configuration details provided by the target owner.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every target before contact.
3. Use `pentest_agent_check_authorization` before any active probing.
4. Use `pentest_agent_build_command` for dry-run preview of WAF detection tools.
5. Use `pentest_agent_execute_tool` for all active probing with rate-limit and output policy enforcement.
6. Use `pentest_agent_append_evidence` for WAF inventories, detection evidence, and protection profiles.

## Workflow

### Phase 1 — Passive WAF detection from response headers

Many WAFs and CDNs identify themselves in HTTP response headers.

- For each in-scope endpoint, collect all response headers and check for WAF/CDN signatures.
- Cloudflare: `CF-Ray`, `CF-Cache-Status`, `CF-Request-ID`, `__cfduid` cookie, `Server: cloudflare`.
- Akamai: `X-Akamai-Transformed`, `X-Cache-Key`, `X-Cache-Remote`, `Server: AkamaiGHost`.
- AWS CloudFront / AWS WAF: `X-Amz-Cf-Id`, `X-Amz-Cf-Pop`, `X-Amzn-RequestId`, `Server: CloudFront`, `X-Amzn-Errortype`.
- Fastly: `X-Served-By`, `X-Cache`, `X-Cache-Hits`, `X-Timer`, `Fastly-Debug` headers.
- Imperva / Incapsula: `X-Iinfo`, `X-Cdn`, `visid_incap_` cookie, `incap_ses_` cookie.
- Sucuri: `X-Sucuri-ID`, `X-Sucuri-Cache`, `Server: Sucuri/Cloudproxy`.
- F5 BIG-IP: `X-WA-Info`, `X-Cnection`, `Server: BigIP`, persistence cookies (`BIGipServer`).
- Citrix NetScaler: `Set-Cookie: NSC_`, `Server: Citrix-ADC`.
- ModSecurity: often no header signature; detected by behavioral fingerprinting in Phase 3.
- Barracuda: `Server: Barracuda`, `X-Barracuda`.
- Fortinet FortiWeb: `X-FortiWeb`, `Set-Cookie: FORTIWEB`.
- Wordfence (WordPress): `X-Wordfence`, `Server: Wordfence`.
- Document every identified WAF/CDN with the header evidence and confidence level.

### Phase 2 — Cookie-based WAF and CDN detection

Protection layers often set cookies for session tracking, load balancing, or bot detection.

- Collect all cookies from each endpoint and check for WAF/CDN cookie patterns.
- Check for WAF challenge cookies: `__cf_bm` (Cloudflare Bot Management), `ak_bmsc` (Akamai Bot Manager), `incap_ses_*` (Imperva), `_imp_apvr_` (Imperva).
- Check for load-balancer persistence cookies: `BIGipServer*` (F5), `NSC_*` (Citrix NetScaler), `SERVERID` (HAProxy), `ARRAffinity` (Azure App Service).
- Check for CDN-specific cookies: `__cflb` (Cloudflare Load Balancer), `AWSALB` / `AWSALBCORS` (AWS ALB), `INGRESSCOOKIE` (Kubernetes NGINX Ingress).
- Check for bot-detection cookies: `ak_bmsc` (Akamai), `dtCookie` (Dynatrace), `_dd_s` (Datadog RUM).
- Document cookie-based detection evidence with cookie names and the associated protection technology.

### Phase 3 — Behavioral WAF fingerprinting

When headers and cookies provide no signature, detect WAF presence through behavioral testing.

- Send a request with a benign parameter value (e.g., `?q=hello`). Record the response status, headers, and body as the baseline.
- Send the same request with a generic attack-like payload that is unlikely to cause harm but triggers WAF inspection: `?q=<script>`, `?q=1' OR '1'='1`, `?q=../../etc/passwd`, `?q=;cat /etc/passwd`.
- Compare the response to the baseline. A WAF typically responds with:
  - 403 Forbidden with a WAF-specific error page (check body for brand mentions).
  - 406 Not Acceptable (ModSecurity default).
  - Connection reset (aggressive blocking).
  - Redirect to a challenge page (Cloudflare, Akamai).
  - HTML body containing WAF-specific text: "The requested URL was rejected", "Web Application Firewall", "Access Denied", "Mod_Security".
- If a block or challenge is triggered, analyze the response to identify the WAF product. Error-page HTML, header values, and status-code patterns are product-specific.
- If no block is triggered, send a second probe: a request header that WAFs commonly inspect, such as `X-Forwarded-For: 127.0.0.1' OR '1'='1`. Some WAFs inspect headers but not query strings.
- Send a third probe with a non-standard HTTP method or malformed request to test whether the WAF rejects at the protocol level.
- For each probe, document the request sent, the response received, and the WAF behavior classification.
- Keep probes small and varied — no more than 5-8 WAF-probe requests per endpoint.

### Phase 4 — CDN and edge protection profiling

CDN security layers have specific behaviors beyond header signatures.

- Test cache behavior: send identical requests and check whether the response includes cache-hit headers (`X-Cache: HIT`, `CF-Cache-Status: HIT`). Cached responses indicate a CDN is active.
- Test origin IP exposure: DNS resolution of the target hostname. Cloudflare and Akamai typically resolve to their edge IPs, not the origin. Direct origin IP resolution may indicate misconfiguration.
- Test for direct origin access: if an origin IP is known from DNS history or certificate transparency logs, test whether the origin accepts direct connections bypassing the CDN. Only test this if the origin IP is in scope.
- Test rate-limiting behavior: send a rapid sequence of requests (capped at 10) and check for rate-limit responses: 429 Too Many Requests, 503 Service Unavailable with a Retry-After header, or progressive delay injection.
- Test bot-detection behavior: send requests with non-browser User-Agent values (`curl/8.0`, `python-requests/2.31`). If the WAF returns a challenge or block, bot detection is active. Use only generic User-Agents for this test.
- Document CDN profile: provider, caching behavior, rate-limit threshold (if determined), bot-detection posture, and any origin-exposure findings.

### Phase 5 — Protection gap analysis

Identify endpoints that bypass the protection layer.

- Test whether all in-scope endpoints are behind the same WAF. Typically, the apex domain, subdomains, and API endpoints should all pass through the WAF. Flag any endpoint that appears unprotected.
- Test non-standard ports. If `https://target.com:8443` has no WAF headers while `https://target.com:443` does, the non-standard port may bypass protection.
- Test internal endpoints. Staging, dev, and admin subdomains often lack WAF coverage even when production is protected.
- Test WebSocket endpoints. WAFs that protect HTTP often do not inspect WebSocket traffic after the upgrade handshake.
- Test file-upload endpoints. Some WAFs skip inspection of `multipart/form-data` requests above a size threshold.
- Document the protection coverage map: which endpoints are protected, which are not, and the protection technology for each.

### Phase 6 — WAF version and rule-set identification

Determine the WAF version and rule-set configuration for precise targeting.

- For identified WAF products, search response headers and error pages for version indicators. Cloudflare includes version in some debug headers; ModSecurity includes version in the `SecRuleEngine` response header if configured to expose it.
- For commercial WAFs, the error-page template often includes a version string or build number in HTML comments.
- For ModSecurity and open-source WAFs, test whether the CRS (Core Rule Set) version can be inferred from which payloads trigger blocks. Different CRS versions have different detection signatures. Note the CRS version hypothesis with low confidence unless confirmed.
- Test whether the WAF blocks SQL injection but allows XSS, or vice versa. Rule-set gaps indicate incomplete protection or configuration errors.
- Document the WAF version and rule-set findings with confidence levels.

## Decision points

- WAF probe count: use no more than 5-8 behavioral probes per endpoint. More probes risk triggering WAF blacklisting or alerting the security operations team.
- Payload selection: use generic, well-known attack patterns that any WAF should detect. Avoid targeted payloads that could exploit a vulnerability if the WAF fails.
- Origin IP access: only test direct origin access if the origin IP is explicitly in scope. Connecting directly to the origin bypasses the WAF entirely and may violate testing rules.
- Rate-limit threshold testing: if the first rapid-sequence test triggers a rate limit, document the threshold and stop. Do not continue escalating request frequency.

## Prohibited behavior

No WAF bypass or evasion attempts. No denial-of-service against the WAF or origin. No exploitation of detected WAF vulnerabilities. No probing of out-of-scope endpoints or origin IPs. No using payloads that contain actual exploit code; behavioral probes must use generic, benign-attempt patterns only. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop on an endpoint when the WAF/CDN type is identified, the protection profile is mapped, and coverage gaps are documented. Stop if behavioral probes trigger an IP block — immediately cease all active testing and record the block as evidence. Stop if the authorization cache expires.

## Evidence

Append evidence via `pentest_agent_append_evidence`:
- WAF/CDN inventory: product name, version (if known), detection method, confidence.
- Header-based and cookie-based detection evidence.
- Behavioral probe log: request sent, response received, WAF behavior classification.
- CDN profile: provider, caching behavior, rate-limit threshold, bot-detection posture.
- Protection coverage map: endpoint, WAF status, protection technology identified.
- WAF version and rule-set identification notes.

Never store WAF error pages that contain internal IP addresses, backend server information, or configuration details. Redact probe payloads if they contain patterns that could be mistaken for actual attack traffic in evidence review.

## Report handoff

Record findings via `pentest_agent_record_finding` for: endpoints bypassing WAF protection (high), non-standard port without WAF (medium), dev/staging endpoints without WAF (medium), origin IP directly accessible (critical), WebSocket endpoints without WAF inspection (medium), outdated WAF version with known vulnerabilities (high), and inconsistent rule-set coverage (medium). Generate the WAF inventory and protection-coverage map as structured evidence for downstream testing phases. Render the final report with `pentest_agent_render_report`.
