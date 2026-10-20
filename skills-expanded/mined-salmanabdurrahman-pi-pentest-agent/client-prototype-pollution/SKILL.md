---
name: client-prototype-pollution
description: Client-side prototype pollution validation — detect Object.prototype injection sources, identify exploitable gadgets, verify impact with safe marker properties, and assess server-side Node.js pollution risks without RCE or credential theft.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Prototype pollution — source-to-sink validation

Use this skill to validate prototype pollution vulnerabilities on an authorized in-scope target. Focus on source identification, gadget discovery, and safe impact demonstration using harmless marker properties. Every test must use test-owned accounts and local reproduction environments. Never execute RCE chains, credential theft, persistence mechanisms, or server-side pollution against production without explicit separate approval.

## Required inputs

- Written scope naming the target application, authorized test accounts, allowed pollution surfaces (URL parameters, JSON body, query string, hash fragment, `postMessage`, cookie properties, header values), and explicit permission for client-side injection.
- User-owned or project-approved test accounts only.
- Valid authorization cache for the target. Separate explicit permission required for server-side Node.js pollution testing.
- Known rate limits, WAF detection thresholds, testing window, and escalation contact.
- Target technology stack: frontend framework and version, bundler, known merge/deep-extend libraries (lodash, jQuery `$.extend`, `Object.assign` wrappers, custom merge utilities), server-side runtime if Node.js, and any known CSP or sanitizer configurations.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — source identification (entry points)

Identify every location where user-controlled data enters the application and might reach a merge operation:

1. **URL query parameters**: test `?__proto__[testprop]=polluted`, `?constructor[prototype][testprop]=polluted`, and variant encodings (dot-notation, bracket-notation, URL-encoded brackets). Check whether `Object.prototype.testprop` is set in the browser console after page load.
2. **JSON body fields**: if the application parses JSON request bodies, submit `{"__proto__": {"testprop": "polluted"}}`, `{"constructor": {"prototype": {"testprop": "polluted"}}}`, and nested variants with arrays.
3. **Hash fragments**: test `#__proto__[testprop]=polluted` in SPA applications that process hash-based routing.
4. **`postMessage` listeners**: if the application listens for `postMessage`, send `{__proto__: {testprop: "polluted"}}` as the message data and check the prototype after receipt.
5. **Cookie and header injection**: test whether cookie names or custom header names parsed as objects can pollute — less common but applicable in isomorphic/SSR applications.
6. **WebSocket messages**: if the application processes JSON over WebSocket, test pollution via WebSocket message payloads.
7. After each injection, verify in the browser console: `Object.prototype.testprop` or `({}).testprop`. If the marker property appears, a pollution source exists.

### Phase 2 — gadget discovery (sinks and impact)

Once a source is confirmed, identify exploitable gadgets:

1. **Client-side gadgets — script injection**: check for sinks that read polluted properties: `innerHTML`, `document.write`, `eval`, `setTimeout(string)`, `Function()`, `script.src`, `iframe.srcdoc`. If a polluted property reaches any of these, DOM XSS is possible.
2. **Client-side gadgets — property override**: check whether polluted properties affect application logic:
   - `isAdmin`, `role`, `permissions` → auth bypass.
   - `config`, `settings`, `options` → behavior manipulation.
   - `transports`, `url`, `host` → request hijacking.
   - `html`, `text`, `src` → content injection.
3. **Library-specific gadgets**: 
   - jQuery `< 3.5.0`: `$.extend` with deep copy reads `__proto__`.
   - lodash `< 4.17.11`: `_.merge` and `_.defaultsDeep` are vulnerable.
   - Immer, MobX, Redux connect — check whether state merge utilities pollute.
4. **Framework-specific gadgets**: 
   - AngularJS: `$scope` merging, template injection.
   - Vue 2: `Vue.util.defineReactive` on polluted properties.
   - React: less directly vulnerable but check custom merge utilities.

### Phase 3 — safe client-side impact validation

For each identified source+gadget pair, validate impact with non-destructive payloads:

1. **Marker property verification**: confirm pollution persists across page navigation or only within current page context.
2. **DOM XSS validation**: inject `<img src=x onerror=console.log('PP_DOM_XSS')>` via a polluted property that reaches `innerHTML`. Confirm the console log fires. Never use payloads that exfiltrate data, steal cookies, or redirect.
3. **Auth bypass validation**: pollute `isAdmin` or `role` and check whether admin-only UI elements render. Record which components respond to the polluted property.
4. **Request hijack validation**: pollute a `baseURL` or `host` property and observe whether API requests are redirected. Use a local listener or controlled endpoint — never redirect to external servers.
5. For each validated gadget, record: the source (URL param, JSON body, postMessage), the merge operation (identify exact line from source maps or error stacks), the sink (innerHTML, eval, etc.), and the observed impact.

### Phase 4 — server-side Node.js pollution assessment

Only when the application runs on Node.js and server-side testing is explicitly authorized:

1. **JSON body pollution via spaces parameter**: Node.js `JSON.parse` with a custom reviver can be polluted. Test with `{"__proto__": {"spaces": 2}}` and check whether response formatting changes.
2. **Status code pollution**: Express applications may read `res.statusCode` from a polluted property. Test `{"__proto__": {"status": 555}}` and check the response status.
3. **Query string pollution via qs**: the `qs` library (used by Express by default) parses `a[__proto__][b]=c`. Test `?__proto__[isAdmin]=true` and check server behavior.
4. **Environment variable pollution**: check whether polluted `env`, `NODE_ENV`, `NODE_OPTIONS`, or `DEBUG` properties affect child_process spawns or debug output.
5. **Always test server-side pollution in a local reproduction environment first**. Never attempt RCE chains against production servers without explicit separate approval and safe rollback capability.

### Phase 5 — source code and dependency review

1. Search the application's client-side bundles for known merge patterns:
   - `_.merge(`, `_.defaultsDeep(` → lodash version check.
   - `$.extend(true,` → jQuery deep extend.
   - `Object.assign(` → not vulnerable directly, but check for recursive wrappers.
   - Custom deep-merge utilities that iterate `for...in` without `hasOwnProperty`.
2. Check `package.json` for dependency versions: lodash, jQuery, merge, deepmerge, merge-deep, assign-deep, Hoek.merge (hapi).
3. If source maps are available, inspect the merge utility source for unsafe iteration patterns.
4. Check for prototype-hardening measures: `Object.freeze(Object.prototype)`, `Object.create(null)` usage, `hasOwnProperty` guards, or `Map` usage instead of plain objects.

## Decision points

- **Stop at source without gadget**: if a source exists but no reachable gadget is found, record as "pollution source — no known gadget" with medium severity.
- **Escalate on DOM XSS gadget**: confirmed injection via polluted property → high finding.
- **Escalate on auth bypass gadget**: polluted role/permissions changes UI behavior → high finding.
- **Escalate on confirmed server-side pollution**: RCE, auth bypass, or information disclosure via server-side pollution → critical finding.
- **Stop if pollution causes persistent state change**: if a polluted property survives page reload or affects other users (rare in client-side, possible in SSR) → stop and record as server-side pollution.

## Prohibited behavior

- Executing RCE chains against production servers without explicit separate approval.
- Deploying payloads that steal credentials, cookies, or tokens.
- Using prototype pollution for persistence (service workers, background sync, stored XSS).
- Exfiltrating data to external servers via polluted properties.
- Testing server-side pollution on production without local reproduction first.
- Bypassing CSP or security headers through pollution unless scope explicitly permits CSP bypass testing.

## Stop conditions

- DOM XSS confirmed → stop, record finding, do not escalate to credential theft.
- Server-side RCE confirmed → stop immediately, notify escalation contact.
- Pollution causes persistent state change affecting other sessions → stop.
- WAF blocks, rate limiting, or account lockout → stop.
- Evidence would include real credentials, tokens, or PII → redact and stop.

## Evidence — source-to-sink matrix

For each test, record:

```text
Target: <URL>
Source: <query | JSON body | hash | postMessage | cookie>
Payload: <pollution payload>
Entry point: <URL parameter name | body field | postMessage origin>
Object.prototype.testprop after injection: <true | false>
Gadget library: <lodash version | jQuery version | custom merge>
Sink: <innerHTML | eval | config property | auth check>
Observed impact: <DOM XSS | auth bypass | request redirect | none>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a pollution posture summary:
- all identified sources with marker-propagation status;
- all identified gadgets with library and version;
- validated client-side impacts;
- server-side assessment results (if authorized);
- dependency versions at risk;
- prototype-hardening measures present.

Never store: authentication tokens, session cookies, credential payloads, server-side environment variables, production RCE commands, or unredacted source code containing secrets.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected source, gadget, sink, CVSS estimate (9.0–10.0 for server-side RCE, 7.0–8.0 for DOM XSS via pollution, 6.0–7.0 for auth bypass via polluted properties, 4.0–5.0 for source-only without known gadget), and remediation guidance.
2. Reference the source-to-sink matrix.
3. Recommend: update vulnerable merge libraries (lodash >= 4.17.11, jQuery >= 3.5.0), add `hasOwnProperty` guards to all deep-merge and object-iteration utilities, use `Object.create(null)` for maps/dictionaries, `Object.freeze(Object.prototype)` as defense-in-depth, input sanitization that strips `__proto__`, `constructor`, and `prototype` keys, and prototype-pollution detection tests in CI.
