---
name: client-xs-leaks
description: Cross-site leak signal validation — detect binary oracles, timing side-channels, resource-event inference, frame counting, and redirect-chain leaks without extracting private user data or building phishing pages.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# XS-Leaks — cross-site information leakage validation

Use this skill to validate cross-site leak vectors on an authorized in-scope target. Focus on detecting binary oracles, timing side-channels, resource-event inference, and browser side-channels that reveal private user state to a cross-origin attacker. Every test must use test-owned accounts and benign signal detection. Never extract private user data, build phishing pages, collect credentials, or target real users.

## Required inputs

- Written scope naming the target application, authorized test accounts (minimum two with distinct private state: different group memberships, different content access, different account tiers), and explicit permission for cross-origin oracle detection.
- User-owned or project-approved test accounts only. Two accounts must differ in at least one binary state: member vs non-member of a group, paid vs free tier, has-unread-messages vs none, etc.
- Valid authorization cache for the target. XS-Leak testing inherently involves cross-origin requests — confirm that cross-origin probing against the target is within scope.
- Known rate limits, CORS policy, CSP configuration, and escalation contact.
- A local HTML test harness or the ability to serve local PoC files for browser testing.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — binary oracle discovery

Find responses where the application's behavior differs based on user state, and that difference is observable from a cross-origin context:

1. **Status-code oracles**: identify endpoints where an authenticated user sees a different HTTP status code than an unauthenticated user for the same URL. Example: `/profile` returns 200 for authenticated, 302 (redirect to login) for unauthenticated.
2. **Response-size oracles**: identify endpoints where response body size differs based on user state. Example: an inbox page returns 50KB when messages exist, 2KB when empty.
3. **Redirect oracles**: identify endpoints that redirect to different URLs based on user state. Example: `/dashboard` redirects to `/dashboard/admin` for admins or `/dashboard/user` for regular users.
4. **Content-type oracles**: endpoints that return different content types based on state — `application/json` for data, `text/html` for error.
5. **Header oracles**: endpoints that set different response headers (e.g., `X-Role: admin`) based on user state.
6. For each candidate oracle, test with two test accounts in different states. Record the differential signal: what changes, by how much, and whether a cross-origin attacker can observe it.

### Phase 2 — resource-event inference

Test whether cross-origin resource loading reveals state:

1. **Image/Script onload/onerror**: create a cross-origin `<img>` or `<script>` tag pointing to a state-revealing endpoint. If `onload` fires, the resource loaded (200-class status). If `onerror` fires, the resource failed (400/500-class status or network error). This reveals binary state without reading the response body.
2. **`<link>` stylesheet detection**: load a cross-origin CSS file. If it loads, the `onload` fires. If it fails or requires authentication, `onerror` fires. Some applications serve different CSS to different user roles.
3. **Cache-based probes**: use `performance.getEntries()` to check whether a cross-origin resource was served from cache (fast timing) or fetched fresh (slow timing). If the resource is only cached for authenticated users, timing reveals authentication state.
4. **CORB/COOP/COEP analysis**: check which response headers (X-Content-Type-Options, Cross-Origin-Resource-Policy, Cross-Origin-Opener-Policy, Cross-Origin-Embedder-Policy) the target sets. These headers control what a cross-origin attacker can observe — map the target's actual protections against what would be needed to prevent each oracle.

### Phase 3 — timing-based side-channels

Test whether response timing reveals private state:

1. **Direct timing measurement**: use `performance.now()` before and after a `fetch` with `no-cors` mode. Compare timing for Account-A (in-group) vs Account-B (out-of-group) for the same endpoint. If timing differs by >50ms consistently, a timing oracle exists.
2. **Timing amplification**: if direct timing differences are small, amplify them: request a large resource vs a small resource where the size depends on state. The larger the size difference, the easier the timing signal.
3. **Partial-response timing**: some servers respond incrementally — the first byte arrives faster for one state than another. Use `performance.getEntriesByType('resource')` to measure `responseStart - requestStart` and `responseEnd - responseStart` separately.
4. **Binary search via timing**: if an endpoint returns slow for "user exists" and fast for "user does not exist," an attacker can enumerate valid usernames. Test this only on test accounts you control, never against real users.

### Phase 4 — frame-counting, history-length, and window references

Test browser side-channel APIs:

1. **Frame counting**: open a cross-origin page in an iframe. Count the number of frames inside that iframe via `iframe.contentWindow.frames.length` (if same-origin access is restricted, the count itself may still be observable). If the number of frames differs based on user state (e.g., admin has an extra frame for admin toolbar), state leaks.
2. **History length**: navigate a popup window through the target application and check `history.length`. If the redirect chain length differs based on state, it leaks.
3. **Window references**: open a cross-origin popup at the target URL. Some browsers allow checking `window.opener`, `window.name`, or other properties indirectly. If these properties differ based on state, it leaks.
4. **`postMessage` broadcast detection**: some applications broadcast state over `postMessage` to all frames. Listen on the attacker origin for `message` events from the target — if data leaks without origin validation, it is an information leak.

### Phase 5 — practical attack scenario analysis

For each confirmed oracle, assess the practical attack scenario — but never build a production exploit:

1. **What user state is revealed?** Group membership, account tier, unread-message count, specific content access, admin vs user role.
2. **What is the attack prerequisite?** Victim visits attacker page while logged in? Attacker can inject content on a same-origin page? Victim clicks a link? Each prerequisite reduces severity.
3. **What is the maximum information gain?** Single bit per visit (binary), multi-bit, full enumeration possible, or content extraction.
4. **Is the leak deterministic or probabilistic?** Deterministic leaks are higher severity.
5. **Rate limiting**: can the attacker probe rapidly (hundreds of requests/second) or slowly (minutes between probes)?

## Decision points

- **Stop at no oracle**: if no binary oracle, timing signal, or frame count difference exists, record negative result.
- **Escalate on deterministic binary oracle**: consistent status/size/or timing difference that reveals private state → medium/high depending on state sensitivity.
- **Escalate on enumeration oracle**: timing or status reveals whether a specific user/resource exists → high (enables targeted attacks).
- **Escalate on content extraction via timing**: if timing reveals actual content (not just existence), escalate to high/critical.
- **Downgrade when CORS/COEP/CORP already mitigate**: if the target's cross-origin headers already block the attack vector, record as "mitigated."

## Prohibited behavior

- Building phishing pages, credential-collection forms, or social-engineering landing pages.
- Targeting real users as victims — all tests must use only test-owned accounts with browser automation.
- Exfiltrating actual private user data or content to an attacker-controlled server.
- Deploying proof-of-concept code to a public website.
- Automating user enumeration against production authentication endpoints.
- Using XS-Leak techniques to bypass authentication or access controls.

## Stop conditions

- Confirmed private-data content extraction → critical finding, stop.
- Real user data inadvertently observed → stop, redact, notify escalation contact.
- Target deploys new cross-origin headers mid-test (mitigation detected) → record and stop.
- Rate limiting or IP block → stop.
- Test account state change irreversible from probing → stop.

## Evidence — oracle and side-channel matrix

For each test vector, record:

```text
Target: <URL>
Oracle type: <status-code | response-size | redirect | timing | frame-count | history-length>
Endpoint: <method> <path>
Test account state A: <Account-A state — admin, in-group, paid-tier>
Test account state B: <Account-B state — user, out-of-group, free-tier>
Signal A: <status 200, 50KB, 120ms, 3 frames>
Signal B: <status 302, 2KB, 40ms, 1 frame>
Observable cross-origin: <yes | no | partially (explain)>
Attack prerequisite: <victim visits page | content injection | link click>
Mitigation present: <CORP | COEP | COOP | SameSite cookies | Framing protections>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into an XS-Leak posture summary:
- all identified oracles by type and endpoint;
- cross-origin observability assessment;
- existing cross-origin isolation headers assessment;
- practical attack scenario impact per oracle;
- recommended mitigations per oracle.

Never store: real user identifiers, authentication tokens, private user content, PII, or unredacted response bodies from cross-origin probes containing customer data.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with oracle type, endpoint, revealed state, attack prerequisite, CVSS estimate (7.0–8.0 for deterministic content extraction, 5.0–6.0 for enumeration oracle, 3.5–5.0 for binary state oracle with significant attack prerequisite), and remediation guidance.
2. Reference the oracle matrix evidence.
3. Recommend: deploy Cross-Origin-Resource-Policy (CORP) with `same-origin` or `same-site`, Cross-Origin-Opener-Policy (COOP) with `same-origin`, Cross-Origin-Embedder-Policy (COEP) with `require-corp` where compatible, consistent error responses with uniform status codes and body sizes for all unauthenticated requests, SameSite=Lax or Strict cookies, X-Frame-Options: DENY or CSP frame-ancestors: 'none' to prevent frame-counting, and Fetch Metadata headers to reject cross-site requests to state-revealing endpoints.
