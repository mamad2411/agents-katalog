---
name: prototype-pollution-clientside
description: Prototype pollution (server-side and client-side) plus deep client-side security — DOM clobbering, client-side CSRF/open-redirect, postMessage origin validation, web-storage/IndexedDB secrets, source-map exposure, and client-side authorization/validation bypass. Use on JS-heavy SPAs and any app with recursive merge / JSON object handling. CWE-1321/79/601.
---

# Prototype Pollution & Client-Side Security

## Prototype pollution (CWE-1321)
JS apps that recursively merge attacker-controlled objects can have `Object.prototype` polluted.
- **Server-side (Node):** send JSON with `__proto__`, `constructor.prototype`:
  `{"__proto__":{"isAdmin":true}}`, `{"constructor":{"prototype":{"role":"admin"}}}` into
  merge/config/update endpoints. Impact: **authorization bypass** (polluted `isAdmin`/`role`),
  RCE via gadget (child_process options), DoS. Confirm by observing a changed downstream behavior
  (a flag that shouldn't be settable becomes true) — reproduce and diff.
- **Client-side:** pollute via query string / JSON parsed in JS
  (`?__proto__[x]=y`, `?constructor[prototype][x]=y`). Then look for a **gadget** that turns the
  polluted property into **XSS**/redirect/config change (e.g. a sink reading `obj.template`,
  `obj.src`, `obj.url`). Trace in the bundle.
- Note: toolbox has no `ppmap`/`ppfuzz` — test manually with the payloads above; use browser/JS
  reasoning on the bundle to find gadgets.

## DOM XSS & unsafe sinks (deep)
Trace **sources** (`location`, `document.URL`, `document.referrer`, `window.name`,
`postMessage`, `localStorage`) → **sinks** (`innerHTML`, `outerHTML`, `document.write`, `eval`,
`Function`, `setAttribute`, `location=`, jQuery `$()`, framework `dangerouslySetInnerHTML`,
`v-html`). Confirm a controllable source reaches a sink unsanitised.

## DOM clobbering
Inject HTML with `id`/`name` matching JS-referenced globals (`<a id=x>`, `<form name=config>`)
to override expected objects → logic/auth bypass or XSS where markup injection (not script) is
allowed.

## postMessage
Find `addEventListener('message', ...)` handlers with **missing/weak `event.origin` checks** →
send a crafted message from an attacker frame to trigger sensitive actions or XSS (CSWSH-like).

## Client-side CSRF / open redirect
State-changing actions driven purely client-side from URL params; redirect sinks reading
`location`/params (`client-side-xss-csrf` for redirect payloads).

## Secrets & exposure in the client
- **Web storage / IndexedDB:** tokens/PII/secrets stored client-side (JWT in `localStorage` =
  XSS-stealable). 
- **JavaScript secrets:** API keys, internal URLs, credentials hardcoded in the bundle
  (`grep` the JS for `key`, `secret`, `token`, `api`, `Bearer`, cloud patterns).
- **Source maps:** `*.js.map` exposed → full original source recovery (fetch and inspect).
- **Client-side authorization/validation:** anything enforced only in JS (hidden admin routes,
  disabled buttons, client validation) must be re-tested against the backend directly.

## Confirmation & recording
Show the source→sink or the polluted-property→behavior chain with exact input+observed effect.
CWE-1321/79/200/601. Chain prototype pollution → XSS/auth as a higher-impact finding.
