---
name: client-side-testing
description: Test client-side and cross-origin vulnerabilities — reflected/stored/DOM XSS, CSRF, CORS misconfiguration, postMessage abuse, clickjacking, and prototype pollution. Use when input reflects into a page, a DOM sink processes attacker-controlled data, or cross-origin trust is involved. Validation requires observing a real browser side-effect.
metadata:
  domain: offensive-security
  standards: "OWASP Top 10:2025 A05/A06, WSTG-CLNT"
  tier: playbook
---

# client-side testing

client-side bugs are proven by *execution or a cross-origin effect in a real
browser*, never by reflected markup in an http response. always validate in a
`browser_context`.

## xss

three sources, one proof standard:
- **reflected**: input echoed into the current response.
- **stored**: input persisted and rendered later, often to another user — trigger it
  as the *victim* in a separate `browser_context`.
- **dom**: a client-side sink (`innerHTML`, `document.write`, `eval`,
  `location`, template) consumes a source (`location.hash`/`search`, `postMessage`,
  `name`, referrer).

method: identify the exact context (html body, attribute, js string, url, css,
template) and break out of it. try encoding, event handlers, and framework-specific
sinks. a WAF/CSP block is a signal about the filter, not proof of safety — adapt the
context or find a sink CSP allows.

validation (see `resources/oracles.md`): observe a real side-effect — `browser_wait_for` a
fired `dialog`, a node injected (`browser_snapshot`/`browser_find`), or an exfil to
`callback_oast`. minimum evidence `impact_demonstrated`. reflected markup alone is
`signal` only.

## csrf

- check for a token: is it present, unpredictable, and *verified* server-side?
- test removal, reuse across users, empty value, method downgrade (POST→GET), and
  content-type change (json vs form) to skip the check.
- proof: a state-changing action performed from a cross-origin context (a second
  `browser_context` with no token) with server-side readback. tie to an
  authenticated, meaningful action.

## cors

- reflect the `Origin` header: does the server echo it into
  `Access-Control-Allow-Origin` with `Allow-Credentials: true`? try an
  attacker-origin, a subdomain, `null`, and prefix/suffix tricks.
- proof: a cross-origin credentialed read of authenticated data succeeds.

## postMessage

- find `addEventListener("message", ...)` handlers that trust `event.data` without
  checking `event.origin`.
- send a crafted message from an attacker frame; observe the sink executing or state
  changing.

## clickjacking

- missing `X-Frame-Options` / `frame-ancestors` is a lead; prove it with a framed
  poc that performs a sensitive action, not just framability.

## prototype pollution

- client: a `__proto__`/`constructor.prototype` key in json/query merged into an
  object; observe a gadget (a property appearing globally) then a concrete effect
  (xss sink, auth flag).
- proof: the polluted property produces a real effect, not just presence.

## failure / adapt

a blocked context does not close xss — change the context, sink, or encoding, or
pivot to csrf/cors/postmessage. record the filter/csp behavior observed.

## routing

`campaign_hypothesis` per sink; `campaign_test` in a browser; validate via
`evidence-and-validation`. stored-xss-as-victim and cors-read often become
`vulnerability-chaining` primitives. resource: `resources/xss-contexts.md`.
