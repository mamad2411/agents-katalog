---
name: sh-kb-ssrf
description: "Knowledge base for finding Server-Side Request Forgery - when the server makes outbound requests to attacker-controlled destinations. Use when hunting SSRF or reviewing URL/host inputs that reach HTTP/network clients. CWE-918, OWASP A10:2021-SSRF."
---

# Server-Side Request Forgery (SSRF) - Hunter Knowledge Base

The server fetches a URL the attacker controls, letting them reach internal services, cloud metadata, or
the loopback interface from the server's trusted position.

## When to hunt this
Features that fetch remote resources: webhooks, URL preview/unfurl, image/PDF fetchers, import-from-URL,
SSO/OIDC discovery, PDF/HTML renderers, avatar-by-URL, proxy endpoints, XML/SVG with remote refs.

## Sources
Any user-supplied URL/host/IP/port: request params/body, redirect targets, `Location` following,
filenames that become URLs, hostnames in config uploaded by users.

## Sinks (grep targets)
- **Python**: `requests.get/post(`, `urllib.request.urlopen(`, `httpx.`, `aiohttp`, `urllib3`.
- **JS/TS**: `fetch(`, `axios(`, `http.get/request(`, `got(`, `node-fetch`, `request(`.
- **Java**: `URL(...).openConnection()`, `HttpClient.send(`, `RestTemplate`, `OkHttpClient`.
- **Go**: `http.Get/Post(`, `http.NewRequest(`. **PHP**: `curl_exec`, `file_get_contents($url)`, `fopen`.
- Also: SVG/XML parsers, PDF generators (wkhtmltopdf/headless Chrome), image libraries fetching remote.

## Detection recipe
1. `graft grep "requests\.|urlopen|fetch\(|axios|http\.Get|HttpClient|curl_exec|file_get_contents" --json`.
2. Check whether the destination URL/host derives from user input.
3. Look for the (usually missing) allowlist / SSRF guard: DNS-resolve + IP range check, scheme check,
   blocking of `169.254.169.254`, `127.0.0.1`, `::1`, `metadata.google.internal`, RFC1918, `.internal`.

## Payloads / PoC
- Cloud metadata: `http://169.254.169.254/latest/meta-data/iam/security-credentials/` (AWS),
  `http://metadata.google.internal/computeMetadata/v1/` (GCP, header `Metadata-Flavor: Google`),
  `http://169.254.169.254/metadata/instance?api-version=2021-02-01` (Azure).
- Internal scan: `http://127.0.0.1:<port>/`, `http://localhost/admin`, internal hostnames.
- Bypasses: `http://0/`, `http://0177.0.0.1`, `http://2130706433` (decimal IP), `http://127.0.0.1.nip.io`,
  redirect chains (allowed host 302s to internal), DNS rebinding, `http://[::]`, `http://[::ffff:127.0.0.1]`.
- Non-HTTP schemes: `file://`, `gopher://` (craft raw TCP to Redis/SMTP), `dict://`, `ftp://`.
- **URL-parser confusion** (differential parsing, per Orange Tsai's research): if the validator and the
  actual HTTP client parse the URL with different libraries/standards, craft a URL both parse differently -
  e.g. `http://expected-host\@evil.com` (backslash before `@`): WHATWG-URL-based parsers normalize `\` to
  `/` and treat `evil.com` as the host, while an RFC-3986-only parser may read `expected-host` as the
  userinfo host. Also test embedded credentials (`http://expected-host@evil.com`), `http://evil.com#@expected-host`,
  and mixed-case/percent-encoded hosts if the validator and the fetch call use different URL parsers.
- PoC: point the fetcher at a collaborator/attacker host and confirm the server connects (out-of-band).

## False-positive filters
- Destination is a hardcoded/allowlisted host or a fixed base URL with only a path from the user.
- A real SSRF guard runs: scheme allowlist (`https` only) **and** resolved-IP range check **after** DNS
  resolution, with redirects disabled or re-validated (validating the string before resolving is bypassable).
- The validation step and the fetch step use the **same** URL-parsing library/call to extract the host (no
  parser-confusion gap) - if they differ (e.g. a regex/manual parse for the allowlist check vs. the
  language's URL/HTTP-client parser for the actual request), still flag even with an allowlist present.
- Egress is network-restricted to specific hosts (note as mitigation, still flag if the code guard is absent).

## CWE / OWASP / severity
CWE-918. OWASP A10:2021. **critical** when it reaches cloud metadata/credentials or internal admin;
**high** for internal network access; medium if only blind/limited.

## Chaining hints
SSRF -> cloud metadata -> IAM credentials -> account/infra takeover; SSRF -> internal unauth admin API ->
RCE; SSRF + gopher -> Redis/DB command exec; pairs with `open-redirect` (to bypass allowlists) and XXE.

## Mitigation
Allowlist destinations (scheme + host); resolve DNS then verify the IP is public and not in blocked ranges,
re-checking on each redirect (or disable redirects); drop non-HTTP schemes; isolate egress; use a dedicated
metadata-blocking proxy; enforce IMDSv2 on AWS.
