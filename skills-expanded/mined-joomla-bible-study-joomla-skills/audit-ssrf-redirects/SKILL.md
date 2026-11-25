---
name: audit-ssrf-redirects
description: Audit Joomla extension URL flows for server-side request forgery and unsafe redirects — attacker-influenced URLs reaching an HTTP client or a browser Location header, including cloud-metadata and internal-service reachability and open redirects. Use when reviewing outbound requests or redirect targets in a Joomla extension, or when explicitly invoked for an SSRF audit.
---

# Audit Joomla outbound URLs and redirects

Audit attacker-influenced URLs that reach either a server-side network client or a browser redirect.

## Boundaries

This audit owns SSRF, unsafe URL schemes, redirect-based allow-list bypasses, and open redirects.

- Local filesystem wrappers and includes belong to `audit-file-operations`.
- Command execution belongs to `audit-code-execution`.
- URL output that executes script in the current page — a `javascript:` href — belongs to
  `audit-xss`.

## Server-side requests

Trace URLs, hosts, ports, and proxy settings from requests, database records, imports, webhooks,
extension parameters, and remote responses into Joomla's HTTP clients
(`\Joomla\Http\HttpFactory`, `Http`), cURL, sockets, URL-aware streams, image and PDF metadata
fetchers, link previews, importers, and callback verification.

Where the destination is not a fixed trusted endpoint, verify a policy covers schemes, credentials,
hosts, ports, and **resolved addresses**. Check IPv4 and IPv6 loopback, private, link-local,
unspecified, multicast, and cloud-metadata destinations (`169.254.169.254`); unusual numeric or
encoded host forms; DNS rebinding between validation and request; and proxy configuration.

**Every followed redirect must be resolved and validated again** — validating only the submitted URL
while the client follows a 302 to `127.0.0.1` is the standard bypass. Consider whether the client
forwards credentials or sensitive headers across hosts, and whether response size and time are
bounded.

An administrator-configured URL is lower exposure, not automatically safe. Assess delegated roles,
tampering with the stored value, imports, and whether reaching internal services exceeds what that
administrator is meant to be able to do on the host.

## Browser redirects

Inspect `$app->redirect()`, `$app->enqueueMessage()`-plus-redirect flows, and raw `Location` headers.
Relative internal destinations or fixed maps are preferred.

For external redirects require an explicit, normalised scheme/host/port policy. Reject
scheme-relative URLs (`//evil.example`), user-info tricks (`https://trusted@evil.example`), control
characters, and ambiguous parser forms.

Do not confuse an untrusted post-login `return` URL — Joomla's classic base64'd `return` parameter —
with harmless internal routing. That parameter is the most common open-redirect surface in the CMS.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — guest or low-privilege access to internal metadata, management services, or
  credentialed network resources.
- **HIGH** — general SSRF, credential forwarding to attacker infrastructure, or a highly credible
  open redirect in an authentication flow.
- **MEDIUM** — blind or constrained SSRF, elevated-user-only SSRF, or an ordinary phishing redirect.
- **LOW** — incomplete hardening with no demonstrated attacker-controlled destination.

For each finding show the URL source, the normalisation and validation applied, the sink, the
redirect-following behaviour, the privileges required, the class of reachable target, and the
mitigation — with file and line references. Note any runtime or DNS assumptions your analysis makes.

Report and await user feedback. Do not change code in this step.

### Step 2 — Feedback round

The user is a subject matter expert and may reclassify or overrule a finding after giving more
context.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-ssrf-redirects` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
