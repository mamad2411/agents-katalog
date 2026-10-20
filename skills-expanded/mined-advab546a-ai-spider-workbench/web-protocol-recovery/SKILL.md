---
name: web-protocol-recovery
description: >-
  Build browser-free Python collectors from hostile web clients. Use for complete protocol recovery or replay, including from-scratch reconnaissance for sign/cookie/challenge/bootstrap/Ruishu/Rivers/WASM/font/transport/WebSocket/GraphQL/protobuf/response decode. Do not use for narrow entry lookup (camoufox-js-reverse), hook snippets, Node/vm patching, AST deobfuscation, compact iv8 scripts, or WeChat miniapp debugging.
argument-hint: "<target URL | request sample | artifact dir> [collector scope]"
---

# Web Protocol Recovery

## Role

Turn hostile web clients into stable protocol collectors.

This skill is not a browser automation skill.
This skill is a protocol recovery skill: browser tools are allowed for reconnaissance, but the delivered collector must not depend on browser driving.

Default posture:

1. start every fresh target without upstream evidence with an ordinary Chrome baseline before any CloakBrowser escalation
2. find the real request
3. identify the true changing state
4. rebuild that state offline
5. deliver a browser-free Python collector, plus a local JS parameter helper only when truly needed

Browser-name guard:

- In this skill, `指纹浏览器`, `fingerprint browser`, `CloakBrowser`, `反检测浏览器`, and `stealth browser` mean CloakBrowser through `js-reverse-mcp.launch_browser({cloakBinaryPath: ...})`.
- Never satisfy a `指纹浏览器` or CloakBrowser request with `camoufox-reverse-mcp`, `camoufox-js-reverse`, or any Camoufox browser tool.
- When the user explicitly says to open or visit a URL with `指纹浏览器`:
  0. Verify the authorization/scope gate below and confirm `chrome-devtools` is `parked|blocked`, never `active`.
  1. Call `js-reverse-mcp_browser_binary_info`. It returns `cloak_active` (bool), `cloak_binary_path` (string or null), and `config_file` (absolute path to the persistent config file).
  2. If `cloak_active` is true, CloakBrowser is already running. Navigate directly with `js-reverse-mcp_new_page` or `js-reverse-mcp_navigate_page`. Do not call `launch_browser` again.
  3. If `cloak_active` is false and `cloak_binary_path` is a non-empty string, call `js-reverse-mcp_launch_browser({cloakBinaryPath: <cloak_binary_path>})`, then navigate.
  4. If `cloak_active` is false and `cloak_binary_path` is null, ask the user for the CloakBrowser executable path and whether it is one-time or may be persisted. A one-time launch passes the path only to `js-reverse-mcp_launch_browser` and does not write config. Persist `{"cloakBinaryPath":"<user path>"}` to `config_file` only after a separate confirmation of that exact file side effect; report how to remove the entry.
- Do not silently substitute Camoufox and do not invent an absolute path.
- This explicit browser-opening command is reconnaissance only. It does not change the final-delivery rule: collectors must remain browser-free.

## Trigger Boundary

Use this skill when the user wants a complete browser-free collector or multi-part protocol recovery, not merely one missing component or a single-interface minimal replay.

Trigger when:

- the task asks to build, repair, or stabilize a crawler/collector or engineered multi-request replay project outside the browser
- several moving parts must be recovered together, such as signature + bootstrap cookie + response decode + transport wrapper
- the target is Ruishu/Rivers/瑞数 and the user wants the whole chain recovered, the request replayed, or the goal is broad/ambiguous rather than a single located entry
- the target is WebSocket, GraphQL, protobuf, msgpack, encrypted response, dynamic-font decode, transport pre-gate, challenge-generated state, local runtime bootstrap, or stateful session protocol
- another skill or the user already supplied real request samples, call stacks, signer formulas, fixed input-output samples, or response bodies and now asks for complete implementation beyond a single-interface minimal script

Do not trigger when:

- only the sign/token/header entry, script URL, function name, or call stack is unknown -> explicit Firefox Reverse/frx goes to `ai-browser-reverse`; otherwise `camoufox-js-reverse`
- only a single Web API sign/cookie/header needs a browser-free minimal script or fixed-input verification -> `camoufox-js-reverse`
- only a Console/Snippets hook script is requested -> `browser-hook-snippets`
- a known browser JS entry must be made to run in Node.js/vm/jsdom -> `env-patch`
- the request is a compact Python + iv8 + requests script -> `iv8-web-reverse`
- the task is whole-file AST deobfuscation or control-flow restoration -> `ast-deobfuscate`
- the target is WeChat miniapp / WMPF runtime debugging -> `wechat-miniapp-reverse`

## Canonical Cross-Skill Handoff v1

This section is the single source of truth for installed reverse-skill handoffs. Neighboring reverse skills must reference it instead of defining a competing field set. Use this packet for full ownership transfers, bounded sidecar requests/returns, and blocked returns:

```yaml
schemaVersion: reverse-handoff/v1
handoffId: <stable id>
handoffRevision: <integer, increment on every return or retry>
handoffKind: full | sidecar | blocked-return
handoffStatus: ready | blocked | complete
sourceSkill: <skill>
targetSkill: <skill>
ownerSkill: <current full-handoff owner; unchanged for sidecar/blocked-return>
ownerPhase: discover | structure | local-runtime | compact-replay | protocol-delivery
nextPhase: <same enum; unchanged for sidecar/blocked-return>
authorizationBasis: owned | explicitly-authorized | public-unauthenticated | unknown
allowedHostsAndRoutes: <exact hosts plus absolute route prefixes>
actionClass: read-only | verifier | mutation | other
accountOrSessionUse: none | approved-identifiers-only | approved-account-bound | blocked | unknown
requestBudget: {total: <count>, remaining: <count>, minDelayMs: <count>, concurrency: <count>}
browserReconAllowed: yes | no | unknown
liveReplayAllowed: yes | no | unknown
artifactRetention: {mode: metadata-only | redacted | raw-approved, approvedRawFields: [], paths: [], retainUntil: <ISO-8601 or none>, purgeOwner: <actor or none>}
projectRoot: <absolute existing project root or none>
targetLandingRoot: <absolute approved destination or none>
rootMode: standalone | existing-project | task-cache-only | no-write
engineProvenance: [{engine: <firefox-reverse | camoufox | chrome | cloakbrowser | wechat-miniapp | node-vm | iv8 | offline | none>, mcpServer: <name or none>, browserInstanceId: <id or none>, sessionId: <id or none>, targetId: <id or none>, capturedAt: <ISO-8601 or none>, lifecycle: live | closed | unknown}]
sourceIds: [{kind: request | script | frame | target | websocket | trace | session | worker, id: <value>, engine: <same enum>, mcpServer: <name or none>, browserInstanceId: <id or none>, sessionId: <id or none>, targetId: <id or none>, capturedAt: <ISO-8601 or none>, lifecycle: live | closed | unknown, status: live | stale | artifact-only}]
targetPageUrl: <URL, redacted URL, or none>
targetApiUrl: <URL, redacted URL, or none>
knownFields: []
requestSamples: []
fixedInputOutput: []
availableRuntimeArtifacts: []
cookieArtifacts: [{name: <name>, source: set-cookie | document-cookie | cookie-jar | request-cookie | imported | unknown, domain: <domain or unknown>, path: <path or unknown>, flags: <HttpOnly/Secure/SameSite metadata>, redaction: metadata-only | redacted | raw-approved, retentionUntil: <ISO-8601 or none>, artifactPath: <path or none>}]
missingEvidence: []
acceptanceTest: <one objective receiver check>
```

Use `none`, `unknown`, or an empty list explicitly; never omit a field and never promote an unknown value. Do not put raw cookie/token/header values in the packet unless `artifactRetention.mode=raw-approved`, the field is named in `approvedRawFields`, and a retention deadline and purge owner exist.

### Sender And Receiver Invariants

- The sender owns packet accuracy: preserve authorization, account/session scope, and roots; decrement `requestBudget.remaining` for traffic already spent; append every engine/MCP lifecycle used; and mark each source ID with matching engine/session provenance. A handoff never widens hosts, routes, actions, account/session use, budget, replay permission, raw fields, retention, or write roots.
- `projectRoot` is the existing execution/project root; `targetLandingRoot` is the approved final destination. `rootMode` controls writes. A receiver must not merge them, invent a directory, or ask again unless both are `none` or the user changes the destination.
- An ID is callable only when its `mcpServer`, browser instance/session, and target still match and its status is `live`. Navigation, reload, target/session switch, browser close, resource cleanup, or engine/MCP switch requires the sender to revalidate or mark affected IDs `stale`; a receiver never tries a stale ID on another engine. Saved redacted samples and files remain `artifact-only` evidence.
- Cookie evidence keeps name, writer/source, domain, path, flags, redaction, retention, and artifact path together. Never flatten scoped cookies into one global header or merge same-name cookies across domain/path boundaries.
- The receiver validates schema, scope, phase, roots, provenance, budget, retention, prerequisites, and `acceptanceTest` before tools or writes. Unknown authorization or out-of-scope traffic remains offline. Missing prerequisites produce the same `handoffId` with incremented revision, `handoffKind=blocked-return`, and precise `missingEvidence`; the receiver does not open a reverse handoff to an earlier skill.
- For `full`, `ownerSkill` remains the sender until the receiver validates the packet and explicitly accepts `nextPhase`; after acceptance it becomes the receiver. For `sidecar`, ownership and `ownerPhase` never change. A `blocked-return` swaps message `sourceSkill`/`targetSkill` to send the response back, but keeps `ownerSkill`, `ownerPhase`, `nextPhase`, every scope/root/provenance field, and the remaining budget unchanged except for budget actually spent; it must use `handoffStatus=blocked` and list only unmet prerequisites in `missingEvidence`.

### Monotonic Routing Ownership

Full ownership moves only forward: `discover -> structure -> local-runtime -> compact-replay -> protocol-delivery`. Route corrections before tool use may select a different `discover` owner; after work starts, same-phase or backward work is a `sidecar` and the current owner remains responsible.

- `discover`: `wechat-miniapp-reverse` owns WeChat/WMPF targets; `ai-browser-reverse` owns only explicit Firefox Reverse/frx or explicit Delegate/Direct-drive requests; `camoufox-js-reverse` owns other ordinary Web entry discovery. This priority prevents generic Web API competition.
- `structure`: `ast-deobfuscate` owns bounded whole-file/source-structure restoration. It does not discover network entry points.
- `local-runtime`: `env-patch` owns a known `target_js` plus known entry in Node/vm/jsdom. It does not reopen browser discovery.
- `compact-replay`: `iv8-web-reverse` owns compact Python+iv8 delivery from trusted JS/entry artifacts.
- `protocol-delivery`: `web-protocol-recovery` owns complete collectors and may start here from a collector-shaped fresh target. It retains ownership while using lower-phase skills as bounded sidecars.
- `browser-hook-snippets` is always a capture sidecar or standalone snippet deliverable; it never owns a phase.

If a full handoff packet contains enough request samples or fixed outputs, take the **evidence reuse** path and do not redo browser baseline work. If this skill owns a fresh collector-shaped target with no usable artifact, take the **fresh target** path and perform discovery internally; do not transfer ownership backward to an entry skill.

## Non-Negotiables

- Final delivery is protocol-owned and browser-free. Python owns live HTTP, retries, parsing, persistence, and scaling; never ship Playwright, Selenium, CDP page driving, submit-through-browser flows, profiles, or automation as the answer, fallback, or temporary path.
- Every fresh target without upstream evidence gets a normal-Chrome baseline before collector implementation. Use `js-reverse-mcp` in normal-Chrome mode for ordinary JS reverse work; CloakBrowser is an evidence-based escalation, not a default for signer, wrapper, decode, or request-diff work.
- Browser reconnaissance is lifecycle-serialized and profile-isolated. Never call `chrome-devtools-mcp_*` and `js-reverse-mcp_*` browser tools in the same parallel batch, warm js-reverse while Chrome is active, or share a profile/`user-data-dir` without an explicit user request and recorded contamination risk.
- At Chrome phase end, save evidence, leave only a sacrificial `about:blank`, and report Chrome as `parked`, not `closed`; never use shell process killing. Then start js-reverse headless with `launch_browser({headless: true, cloakBinaryPath: ""})`; headful requires recorded interaction, rendering, fingerprint, or headless-mismatch evidence.
- Tool switching is reversible but exclusive: close `js-reverse-mcp` at phase end and before returning to Chrome. Switch to CloakBrowser with its confirmed `cloakBinaryPath`; switch back with an empty `cloakBinaryPath`.
- Local JS, WASM, bootstrap, decoder, signer, or `iv8` helpers are allowed only for explicit artifact reconstruction when a verified Python port is not yet safer or cheaper. They must run without page driving, `document`, `window`, manual clicks, browser profiles, or hidden browser dependencies.
- Recover one stable request before scaling pagination, concurrency, or submission.
- Every conclusion must be backed by artifacts: request samples, fixed-input helper outputs, cookies, headers, and replay proof.
- All reconnaissance artifacts such as downloaded JS, WASM, fonts, HTML, network exports, state snapshots, screenshots, traces, and fixed-input vectors must go under the generated project's root-level `js_reverse_cache/`; create the project scaffold before saving target artifacts.
- Final collector code must live in the same dedicated protocol project directory using the bundled scaffold shape: `analysis/`, `collector/`, `js_reverse_cache/`, `tests/`, `README.md`, and `requirements.txt`. Do not collapse the delivery into a single `main.py` except for a temporary throwaway probe saved under that project's `js_reverse_cache/`.
- Once a protocol recovery project exists, it owns the project root. Any later `iv8-web-reverse` help must be embedded into that existing project using explicit paths; do not let the helper create a second project root, standalone `main.py`, or separate `utils/` tree unless the user explicitly changes the goal to a compact standalone Python+iv8 script.
- Stay in one execution loop until you reach protocol delivery or hit a real external blocker.
- Confirmation Checkpoints always override the execution-loop rule. If a step needs sensitive replay, mutation, scale-up, fresh browser collection, or raw secret printing, pause before continuing.

## Confirmation Checkpoints

Do not let protocol recovery expand from artifact analysis into live side effects without a short user confirmation. Pause before:

- using account-bound cookies, Authorization headers, session ids, private API keys, or paid/privileged data sources in live replay
- submitting verifier answers, CAPTCHA/behavior payloads, forms, mutations, orders, payments, messages, or any request that can change server state
- increasing from one stable proof request to pagination, concurrency, retries, long-running collection, or high-volume scraping
- saving or printing full raw cookies, tokens, Authorization values, request bodies, response bodies, decrypted payloads, or account-bound samples; default to minimal fields, hashes, lengths, or masked excerpts
- switching from evidence reuse to fresh browser reconnaissance because provided artifacts are insufficient; state the missing artifact first, then ask for permission to collect it

No pause is needed for offline fixed-input signer checks, local decoder tests, static source reading, or replay against user-provided mock/sample artifacts.

## Authorization And Scope Gate

Before any browser navigation, live HTTP, login/session use, challenge interaction, or target-derived artifact capture, record:

```text
authorizationBasis: owned / explicitly-authorized / public-unauthenticated / unknown
allowedHostsAndRoutes:
actionClass: read-only / verifier / mutation / other
accountOrSessionUse: none / approved-identifiers-only / approved-account-bound / blocked / unknown
browserReconAllowed: yes/no
liveReplayAllowed: yes/no
requestBudget: count, minimum delay, concurrency
artifactPolicy: metadata-only / redacted samples / approved raw fields + retention deadline
```

If `authorizationBasis=unknown`, `browserReconAllowed=no`, or the requested host/action is outside scope, remain offline with user-provided artifacts and do not navigate or send requests. Public reachability is not authorization for account access, mutation, verifier submission, or broad collection. Reconfirm when the target host, action class, account, volume, or retention policy expands.

## Startup Gate

The Authorization And Scope Gate precedes all navigation. On a fresh target, obtain `browserReconAllowed=yes`, then emit the startup gate before deep tool use. `references/startup-triage-playbook.md` is the canonical family-triage procedure.

Choose one path:

1. Evidence reuse: when real requests, headers/cookies, call stacks, formulas, fixed samples, or response bodies are supplied, scaffold the project and `js_reverse_cache/`, classify the family, state the final shape, and verify those artifacts without browser availability checks. If they fail, read `references/troubleshooting-playbook.md`, name the missing evidence, and apply Confirmation Checkpoints before fresh collection.
2. Fresh target: run `scripts/check_reverse_env.py` when available, record normal Chrome as the first tier, capture and park the Chrome baseline before checking js-reverse, then freeze one real request. Record `chrome=active|parked|blocked` and `js-reverse=not-started|active-headless|active-headful|closed|blocked`; report blockers when their phase is reached.
3. Near-miss: route narrow signer lookup, hook snippets, Node/jsdom patching, compact iv8 scripts, AST restoration, or WeChat miniapp work to the neighboring skill and retain useful evidence.
4. Escalation: state the proved failure, then read only the matching focused playbook before widening runtime, patch surface, transport profile, or collection scope.

For every path:

- create the dedicated project and `js_reverse_cache/` before saving artifacts; final code stays in that project
- pass an existing project root, helper/cache paths, expected input/output artifacts, and acceptance check to any `iv8-web-reverse` handoff; never hand off only a URL
- classify `signer-gated`, `verifier-gated`, `decode-gated`, or `session-gated`, add secondary families and `transport-gated` when applicable, and restate the gate if classification changes
- note `iv8` or `curl_cffi` availability only when host semantics or transport admission are suspected
- state pure Python, Python plus tiny JS/WASM helper, local bootstrap executor, or narrow embedded runtime as the intended shape; reject browser-backed replay
- read `references/cookie-provenance-playbook.md` before hardcoding a rotating cookie and `references/escalation-ladder-playbook.md` before jumping layers

First-turn report: path, family and secondary tags, next three smallest proofs, confirmation needed, and browser-free final shape. If this gate is incomplete, the target is not yet understood.

## Minimal Intake

Start immediately if the user already provided enough evidence.

Otherwise ask only for the smallest missing set:

- target page URL, or
- target API URL, or
- site homepage plus collection goal, or
- captured request sample, or
- JS snippet, obfuscated bundle, cookie sample, sign sample, or packet capture

Only ask follow-ups that change implementation:

- target fields
- scope: single page, pagination, category, date range, or whole site
- output format: JSON, CSV, Excel, database, or API sink
- whether login is required
- whether incremental sync, dedupe, or resume is required

## Universal Reverse Loop

### Phase 0: Fingerprint before deep work

Classify before reading giant bundles. Distinguish:

- decoy from real endpoint; transport-pre-gated from application-visible baseline; bootstrap asset from data API
- wrapper rewrite from visible param; patched from standard helper; independent fields from a challenge-generated shared envelope
- simple formula from host-bound bootstrap or true interaction; exposed getter from self-submitting runtime or alternate-route bypass
- signer-, verifier-, decode-, or session-gated; single-shot from paired/authenticated/warmed stateful flow
- plain JSON, GraphQL, WebSocket, or binary envelope; direct, encoded, encrypted, compressed, or glyph-mapped response
- global flow from page-specific exception; anonymous from session-bound; rotating-cookie provenance known from unknown
- normal packed code from JSVMP/heavy obfuscation; stable pagination arithmetic from route pivot; raw-source metadata from parser-normalized DOM values

Use normal-Chrome js-reverse unless the Browser-name guard or proved fingerprint evidence requires CloakBrowser. Choose the smallest next proof and least destructive instrument.

### Phase 1: Identify the true request path

- follow redirects and wrapper/compatibility pages; separate visible routes from wire routes
- map bootstrap, list, detail, submission, risk-control, and later-page requests, including pivots to `/ui`, Ajax, or another family
- test whether one endpoint has bootstrap and data phases or whether the challenged document route itself is the replay target

Deliverable: one confirmed request on the real business path.

### Phase 2: Classify the moving parts

For the real request, classify:

- static/rotating headers and cookies; timestamp, nonce/random fragment, signed body/query
- transport envelope, operation/message type, pagination or page-specific exceptions
- compressed, binary, encrypted, glyph-mapped, or otherwise transformed responses and their keys/maps
- account/session and bootstrap dependencies, including login/pairing, key schedules, exported secrets, heartbeat/ack/counter/tag state, and media/download keys
- host semantics such as lifecycle, timers, cookie behavior, parser order, XHR wrappers, native surfaces, or probe-chain state

Separate what must be reproduced from noise.

### Phase 3: Locate the canonical mutation point

Look in this order:

1. transport wrappers such as `$.ajaxSetup`, `beforeSend`, fetch wrappers, interceptors
2. bootstrap side scripts and inline payloads
3. page-exposed helper functions
4. WebAssembly exports
5. server-returned JS challenges
6. response-side refresh fields that seed the next request
7. handshake transcripts, frame serializers, binary node encoders, protobuf parsers, or session key schedules

Rule:

- the canonical mutation point is where the wire payload actually changes, not where the business code first creates a placeholder

### Phase 4: Rebuild the moving parts offline

Choose the cheapest valid offline shape:

1. pure Python
2. Python plus isolated JS signer
3. Python plus minimal local JS or WASM helper
4. Python plus local challenge bootstrap executor or narrow embedded runtime such as `iv8` when host-visible semantics are proven necessary
5. Python plus local font decoder

Never add browser automation to the final path.
Escalate only one rung at a time; before moving to a heavier runtime, broader patch surface, or transport exception, record what failed at the current rung and why the next rung is the smallest honest move.

### Phase 5: Prove repeatability

Do not call it solved until the same logic succeeds 2 to 3 times, pagination advances, final fields are complete, dynamic state regenerates, and account-bound constraints are documented.

## Tool Priorities

`references/tool-playbook.md` is canonical for browser lifecycle, cleanup, capability selection, headful fallback, and CloakBrowser path handling. For fresh targets without upstream evidence:

1. classify with `references/startup-triage-playbook.md`
2. capture page state, redirects, visible flow, and first-pass network in normal Chrome through `chrome-devtools-mcp`
3. save artifacts, close extra pages, park the last Chrome page at `about:blank`, then start normal-Chrome js-reverse headless for initiators, source search, wrappers, breakpoints, and mutation proof
4. close js-reverse before any return to Chrome; never parallelize tool families or share profiles without explicit approval and contamination reporting
5. diff requests, verify helpers on fixed inputs, replay locally, and escalate one rung only after a proved gap

Do not skip this baseline unless upstream evidence replaces it or a real blocker is reported. CloakBrowser requires explicit user wording under the Browser-name guard or at least one of:

- normal Chrome receives fingerprint, webdriver, bot, risk-control, `403`, `412`, `429`, or challenge behavior that a direct request or header diff cannot explain
- page code reads or hashes `navigator`, `screen`, canvas, WebGL, audio, fonts, timing, plugins, permissions, WebRTC, or automation flags before the protected request
- clean normal-Chrome baseline and local replay disagree on fixed environment-dependent outputs
- hooks or breakpoints change the failure mode and you need a less detectable capture to separate observer effect from protocol logic

Record the escalation evidence. Prefer `compare_env`, source search, initiator stacks, and narrow hooks; never switch to Camoufox for CloakBrowser wording or engine tracing. Deeper interaction is limited to observing a redirect/wrapper, handling anti-debug extraction, or sampling fixed helper output and never becomes a delivery dependency.

## Canonical References

- `references/startup-triage-playbook.md`: startup checks and family triage
- `references/tool-playbook.md`: tool capabilities, serialized browser lifecycle, cleanup, and one-time versus persistent CloakBrowser paths
- `references/reference-router.md`: canonical symptom-to-playbook map; read at most the 1-2 references matching the blocker
- `references/escalation-ladder-playbook.md`: proof required before widening runtime, patch surface, or transport
- `references/pattern-atlas.md`: compact recurring patterns for endpoint, bootstrap, challenge, decode, transport, pagination, and runtime cases
- `references/verification-gates.md` and `references/report-templates.md`: completion gates and phase reports
- `references/anti-patterns-playbook.md`: evidence-first recovery when a shortcut appears attractive

## Bundled Scripts

Use local helper scripts when they shorten repeatable work:

- `scripts/scaffold_reverse_project.py`: generate a protocol-first Python project skeleton with profile-aware layouts for `generic`, `public-envelope`, `structured-transport`, and `response-decode` targets
- `scripts/check_reverse_env.py`: verify the minimal local reverse environment fast
- `scripts/crypto_fingerprint.py`: fingerprint suspicious digest, Base64, or custom-alphabet outputs
- `scripts/protocol_diff.py`: compare captured request or response samples and surface the meaningful deltas
- `scripts/validate_eval_coverage.py`: enforce prompt/eval parity and high-risk boundary coverage
- `scripts/test_safety.py`: offline regression tests for redaction, bounded helpers, scaffold overwrite/backup, and volatile-artifact exclusion
- `scripts/test_validate_eval_coverage.py`: verify complete reviewed-response manifests without keyword-based grading

For stateful stream targets, start from the `structured-transport` scaffold and split handshake, session, frame-codec, decode, and media logic into separate modules early.

## Implementation Rules

- keep headers, cookies, signer logic, pagination, output, retries, and persistence in separate modules
- keep handshake bootstrap, session secrets, frame codecs, business parsing, and media derivation in separate modules when the target is stateful
- generated Python collectors must support Python 3.9+ and both entrypoints: `python -m collector.main` from the project root and `python main.py` from the `collector/` directory
- make `sessionid`, timeout, retry, sleep, and output path explicit arguments
- configure `authorization_basis`, exact `allowed_hosts`, absolute segment-aware `allowed_route_prefixes`, `action_class=read-only`, total HTTP/redirect/stream request budget, and artifact policy before live traffic; `unknown` or out-of-scope targets fail closed
- reject cookies or account-bearing headers under `public-unauthenticated`; approved raw artifacts require an explicit retention deadline
- require `--confirm-live` before generated collectors send traffic; bound pages, retries, timeout, response bytes, backoff, and concurrency in code, not only prose
- share one request-attempt budget across bootstrap, retries, redirects, stream connects, reconnects, and outbound application frames
- retry only idempotent requests by default; honor bounded `Retry-After` for `429/503`, use exponential backoff with jitter, and require an explicit idempotency contract before retrying mutations
- make proxy ownership, environment-proxy use, CA bundle/TLS policy, redirect scope, and impersonated transport choice explicit per target route; never silently inherit a proxy for account-bound headers
- keep CookieJar domain/path scope and server rotations authoritative; do not flatten cookies into a global `Cookie` header or merge same-name cookies across origins
- use bounded response reads and pass raw bytes to the decode layer before text/JSON parsing when binary, encrypted, compressed, protobuf, or msgpack payloads are possible
- refuse output overwrite unless explicitly confirmed, keep paired JSON/CSV in one directory, recover interrupted publication through the output journal, and neutralize spreadsheet formula prefixes in CSV
- compare signer inputs and outputs by length, hash, field names, and masked excerpts until they match verified samples; raw values require the explicit raw-artifact checkpoint
- include fixed-input self-checks before live traffic
- drive signer, encoder, and decoder requirements from runtime settings; every required stage needs captured vectors and has no boolean readiness bypass
- capture one clean baseline before broad hooks on verifier-gated or behavior-sensitive targets
- prove one fresh minimal live replay on one session chain before broad environment patching, runtime shrink, pagination scaling, or reuse generalization on verifier-gated or challenge-bootstrap targets
- prefer Python reimplementation of crypto before falling back to JS execution
- if JS is kept, keep it narrowly scoped to parameter restoration, signer logic, token generation, cookie reconstruction, or local decoding only
- make the final runtime split explicit: Python owns HTTP, pagination, retries, parsing, storage, and orchestration; JS owns only the minimal parameter restoration that still cannot be ported safely
- strip browser-only assumptions from helper code or emulate them locally without launching a browser
- prefer stdlib HTTP clients when you want zero dependencies or the environment's third-party stack is noisy
- preserve weird delimiters and non-ASCII separators explicitly
- catalog server-issued artifacts separately from locally computed or locally minted ones
- treat bootstrap artifacts such as public keys, config blobs, nonce seeds, and wrapper field names as first-class inputs
- prove cookie provenance before caching or persisting rotating cookies in the collector
- validate compact JSON shape, sign input order, timestamp precision, and chunked-encryption boundaries separately before blaming the runtime
- default to metadata-only or redacted request/response samples during early development; approved raw fields require a named path, restrictive local permissions where supported, repository exclusion, and a retention deadline
- save approved dynamic reconnaissance materials under the generated project's `js_reverse_cache/`; keep volatile caches, input, output, state, and raw request samples gitignored, and purge them at the agreed deadline
- keep stable scaffolding separate from volatile target captures and runtime blobs
- keep bootstrap-heavy traces on one session chain until reuse is explicitly proven
- treat wire-shaped egress records, especially outbound `Cookie` headers, as replay authority when they differ from intermediate getters or jar state
- regenerate request-shaped artifacts per request when page, body, referer, keyword, timestamp, or pagination can change them
- preserve wrapper framing, JSONP, exact urlencoded bytes, odd delimiters, and exact serialization rules explicitly
- inspect native-surface probes before cargo-cult filling globals or upgrading runtime layers
- save one redacted or approved-raw handshake transcript and one post-auth business frame before rewriting the collector; never persist session secrets by default
- keep reconnect disabled by default; when enabled, require fixed reconnect vectors, bounded attempts/backoff, explicit retryable close codes or transport-error opt-in, subprotocol checks, fragment/message bounds, backpressure timeout, and configured close semantics
- support narrow per-page or per-request exceptions in configuration instead of hardcoding chaos into the main loop
- make category and pagination fields explicit when the page may be injecting hidden tab state
- fail loudly on unexpected response shapes
- if older notes disagree with live output, trust fresh live evidence

## Verification Gates

Do not mark complete until the relevant gates in `references/verification-gates.md` pass. In short: confirm the real request path, classify moving parts, prove helper outputs on fixed inputs, document provenance for server-issued state, run repeated live replay, and keep final delivery browser-free.

## Output Contract

After each meaningful phase, emit short structured reporting instead of vague prose. Use the headings from `references/report-templates.md` when possible.

Always return the applicable fields. In evidence-reuse or blocked-tool paths, explicitly state `not used`, `skipped`, or `blocked` and why instead of inventing browser proof.

Minimum report:

- startup triage family, secondary tags, evidence path, final delivery shape, and browser-free constraint
- `chrome-devtools` result, or why the baseline was skipped/blocked/replaced by provided artifacts
- `js-reverse-mcp` result, or why mutation tracing was skipped/blocked/replaced by provided artifacts
- dual-recon profile isolation status, including any explicit profile reuse and contamination risk
- dual-recon lifecycle status, including whether Chrome was `parked`, whether js-reverse ran `headless` or `headful`, the reason for any headful fallback, and whether js-reverse was closed before a tool-family switch
- real endpoint, real moving parts, misleading signals, observer-effect risk, and CloakBrowser use if any
- cookie provenance, server-issued versus locally minted artifacts, and fixed-input proofs when those mattered
- final protocol path, sibling route reuse, collector/helper split, embedded-runtime status, and browser-free confirmation
- reusable minimal facts, saved collector/output paths, and remaining instability

## Skill Validation

When modifying this skill itself, validate against `references/official-self-test-task-suite.md` and `references/skill-maintenance.md` before calling the edit complete.

Run `scripts/validate_eval_coverage.py` for corpus parity. For behavior-changing edits, also validate a complete provider-neutral reviewed-response manifest with `--responses`; human evidence must quote the verbatim response and cover every expectation exactly once. Never grade actual responses by keyword presence alone.

Pass conditions:

- the route stays protocol-first
- every fresh target without upstream evidence begins with a normal-Chrome baseline before any CloakBrowser escalation
- paired `chrome-devtools` and `js-reverse-mcp` reconnaissance stays sequential and profile-isolated unless explicit profile reuse is documented
- browser lifecycle stays exclusive: no cross-family parallel browser calls, no early js-reverse warm-up, Chrome cleanup is reported honestly as `parked`, and js-reverse is closed before returning to Chrome
- CloakBrowser is used only after fingerprint, anti-bot, or environment-verification evidence is recorded
- final delivery never depends on browser automation
- final delivery is Python collector first, with JS limited to local parameter restoration only
- generated collector scaffolds support Python 3.9+ and pass both root-module and direct-file entrypoint checks
- generated collector profiles match `fixtures/scaffold_contracts.json`, pass their offline tests, and enforce authorization/readiness/output-recovery policy before live traffic
- structured transport, decode chains, stateful sessions, embedded runtimes, challenge-generated state, transport pre-gates, and pagination pivots are handled correctly when present
- the chosen references match the real symptom instead of generic cargo-cult loading

## Anti-Patterns

Read `references/anti-patterns-playbook.md` when a shortcut feels faster than evidence. The irreducible rule is: do not replace protocol recovery with browser automation, browser profiles, hardcoded rotating cookies, helper-name guesses, or one lucky replay.

Do not start both recon browsers during startup sanity checks. A browser availability check that launches the next engine before the current phase is saved and cleaned up is a lifecycle violation, not harmless preflight.

## Reference Router

Use `references/reference-router.md` for the full symptom-to-playbook map. Keep this file lean: choose the entry path first, then load only the 1-2 references matching the current blocker.

## Experience Deposition

After a successful job, preserve only reusable lessons. Route detailed deposition through `references/skill-maintenance.md`: convert site-specific pain into generic pattern language, keep fixed-input validation habits, preserve provenance and transport rules rather than copied secrets, and add helper scripts only when they improve many future jobs.

## Bottom Line

This skill should teach one habit above all:

When the site looks "browser-only", do not panic and do not automate.
First ask:

1. what is the real request
2. what is the real changing state
3. can that state be rebuilt locally

Most similar targets collapse once those three questions are answered honestly.
