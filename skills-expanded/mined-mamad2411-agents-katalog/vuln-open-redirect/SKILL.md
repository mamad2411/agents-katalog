---
name: vuln-open-redirect
description: Open redirect validation — detect unvalidated URL redirect parameters, confirm bypass of allowlist and blocklist filters with safe attacker-controlled destinations, and assess OAuth redirect_uri abuse risk only when scope explicitly authorizes OAuth flow testing.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Open redirect — unvalidated redirect and forwarder validation

Use this skill to validate open redirect vulnerabilities on an authorized, in-scope target. Confirm that user-controlled URL parameters can redirect the browser to an arbitrary external domain. Focus on demonstrating the redirect itself — one confirmed redirect to a safe, engagement-owned destination is sufficient proof. Never use the redirect to phish credentials, deliver malware, chain with OAuth token theft without explicit scope, or redirect to destinations the target's users would consider legitimate.

## Required inputs

- Written scope naming the target, authorized redirect parameters (login redirect, logout return URL, OAuth redirect_uri, payment return URL, deep-link parameters), and explicit permission for open redirect validation.
- Valid authorization cache.
- A safe, engagement-owned redirect destination — use a test URL under your control (localhost with a listener, an interactsh/Burp Collaborator host, or a safe test destination like `example.com` for non-OAuth tests). Never use a real attacker domain that could collect production user traffic.
- List of candidate redirect parameters from recon: `?redirect=`, `?return=`, `?next=`, `?url=`, `?goto=`, `?dest=`, `?destination=`, `?redir=`, `?redirect_to=`, `?redirect_uri=`, `?continue=`, `?target=`, `?back=`, `?location=`, `?to=`, `?from=`, `?link=`, `?out=`, `?r=`.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — redirect parameter discovery

Identify parameters that control browser redirects:

1. **Login/logout flows**: log in and log out while watching the URL bar. Look for `?redirect=`, `?return=`, `?next=`, or `?continue=` parameters appended to `/login` or `/logout`.
2. **OAuth/OIDC flows**: examine the authorization endpoint URL for `redirect_uri=` parameter. Check `/.well-known/openid-configuration` for the authorization endpoint.
3. **Password reset**: after entering an email, the app may redirect via `?back=` or `?return_to=`.
4. **Payment/e-commerce**: checkout flows often include `?returnUrl=` or `?cancelUrl=` parameters.
5. **Error pages**: 404/500 error pages sometimes include a "go back" link driven by a `?from=` or `?ref=` parameter.
6. **Response headers**: send requests to candidate endpoints and inspect `Location` response headers in 301/302/303/307/308 responses.

Crawl the application and collect every URL containing redirect-like parameter names. Record the endpoint, parameter name, HTTP method, and the expected behavior (302 redirect, meta-refresh, JavaScript `window.location`).

### Phase 2 — basic redirect validation

For each candidate parameter, test with a safe external destination:

1. Set the parameter value to `https://example.com` (or your engagement-owned test host).
2. Send the request with `--max-redirs 0` (do not follow redirects) or inspect the `Location` header.
3. If the response is a 3xx redirect to `https://example.com` → open redirect confirmed.
4. If the response redirects to the target's own domain (e.g., prepends `https://target.com/` to the value) → the redirect is validated — test bypass techniques.

Record the base behavior: does the app strip the protocol, enforce a domain allowlist, require a specific path prefix, or prepend a base URL?

### Phase 3 — filter bypass techniques

When basic external redirects are blocked, test common bypass patterns:

```text
Protocol-relative bypass:   //example.com
Protocol-relative stacked:  ////example.com
Backslash bypass:           /\example.com
Scheme omission:            example.com (browser may prepend http://)
URL-credential confusion:   https://target.com@example.com
Fragment confusion:         https://example.com#.target.com
Query-string confusion:     https://example.com?target.com
Semicolon confusion:        https://example.com;target.com
Whitespace suffix:          https://example.com%20
Tab suffix:                 https://example.com%09
Null byte (legacy):         https://example.com%00.target.com
Unicode homograph:          https://example%E3%80%82com (fullwidth dot)
Dotless IP:                 http://2130706433 (decimal for 127.0.0.1)
```

Test each bypass independently. Rules:
- One successful bypass is sufficient. Do not enumerate all variants for a single parameter.
- If the domain allowlist only permits `target.com`, test subdomain confusion: `https://target.com.example.com` (not actually target.com).
- If the application uses a blocklist (rejects `//`, `@`, `#`), test encoding variants of blocked characters.
- Browser behavior matters: `\/\/example.com` may be interpreted as `//example.com` by some URL parsers. Use a real browser or `curl` with `--location` to verify.

### Phase 4 — OAuth redirect_uri validation

OAuth open redirects are higher impact because they can enable authorization code theft:

1. Identify the OAuth authorization endpoint (from `/.well-known/openid-configuration` or by intercepting an OAuth login flow).
2. Identify the `client_id` and `redirect_uri` parameters.
3. Replace `redirect_uri` with your engagement-owned test host.
4. If the authorization server redirects to your host with an authorization `code` parameter → OAuth redirect_uri validation bypass. Critical finding.

Test OAuth redirect_uri only when scope explicitly authorizes OAuth flow testing. Never:
- Use a real client application's `client_id` in a way that could affect production users.
- Intercept real user authorization codes.
- Attempt to exchange captured codes for tokens (that requires separate authorization).

### Phase 5 — impact demonstration without phishing

Demonstrate impact safely:

- For standard open redirects: show the redirect URL that sends the browser to your controlled test host. Record the exact URL, the `Location` header, and the HTTP status code.
- For OAuth: show that the authorization server issues a redirect to your test host. Document the vulnerable `redirect_uri` parameter and the lack of strict matching.
- Do not create a phishing page, capture credentials, steal tokens, or serve malicious content. The redirect URL itself is the proof.

## Decision points

- **Stop at first confirmed redirect**: one parameter redirecting to an external domain is sufficient proof.
- **Bypass is not required for a finding**: if the app allows `https://example.com` directly, that is an open redirect. Bypass techniques are only needed when the app blocks direct external URLs.
- **OAuth redirect_uri is critical**: if the OAuth authorization server accepts an arbitrary `redirect_uri`, report immediately. This enables account takeover.
- **Not all redirects are vulnerabilities**: if the app validates redirect destinations against an allowlist and only redirects to trusted domains, that is correct behavior — document and move on.

## Prohibited behavior

- Creating phishing pages, credential-capture forms, or malware-download pages at the redirect destination.
- Intercepting authorization codes, access tokens, or session tokens from real users.
- Redirecting to domains that impersonate the target (homograph attacks in production).
- Using `javascript:` or `data:` URIs to execute script in the redirect context — that is XSS, not open redirect.
- Chaining open redirect with stored content injection to create a persistent phishing flow.

## Stop conditions

- External redirect confirmed → stop testing that parameter.
- All filter bypasses fail → domain allowlist or strict validation likely in place, document.
- OAuth redirect_uri validated → stop, critical finding.
- Rate limiting or WAF blocks repeated redirect attempts → document, do not bypass.

## Evidence — redirect matrix

For each tested parameter, record:

```text
Endpoint: <URL> | parameter: <parameter name>
Base behavior: <direct external redirect | validated | allowlist | prepend base URL>
Bypass required: <none | protocol-relative | credential confusion | unicode | other>
Redirect destination: <engagement-owned test URL>
HTTP status: <302 | 301 | 307 | 303 | meta-refresh>
OAuth redirect_uri affected: <yes | no | not applicable>
Client ID (if OAuth): <redacted>
Impact: <none | open redirect | OAuth redirect_uri bypass>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a parameter × bypass matrix. Never store: redirect URLs containing real user session tokens, OAuth authorization codes, `client_secret` values, or PII from the target.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected endpoint, parameter, bypass technique (if any), CVSS estimate (4.0–5.5 for standard open redirect, 6.5–8.0 for OAuth redirect_uri bypass), and remediation guidance.
2. Reference the redirect matrix.
3. Recommend: validate redirect destinations against a server-side allowlist of trusted domains and paths, use relative redirects where possible, validate OAuth `redirect_uri` against a pre-registered list per client, display an interstitial warning page for external redirects, audit all redirect parameters in CI, and never accept user-controlled URLs directly in `Location` headers.
