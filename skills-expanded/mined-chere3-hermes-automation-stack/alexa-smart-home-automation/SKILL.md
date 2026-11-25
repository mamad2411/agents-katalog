---
name: alexa-smart-home-automation
description: Securely discover and control Amazon Alexa/Echo devices, and build Alexa Custom Skill voice bridges to Hermes, including exact-device speech, scheduled briefs, appliance control, and state verification.
version: 1.3.10
author: Hermes Agent
metadata:
  hermes:
    category: smart-home
    tags: [alexa, echo, smart-home, tts, automation, private-api, custom-skill, hermes, voice-bridge, scheduling]
    requires_toolsets: [terminal, file]
---

# Alexa Smart-Home Automation

Use this skill when configuring or operating Alexa/Echo automations through Amazon’s web/mobile APIs: cookie acquisition, device discovery, exact-device speech, scheduled spoken reports, appliance control, and state verification. Also use it when designing an official Alexa Custom Skill as a secure voice bridge to Hermes; see `references/hermes-synchronous-voice-bridge.md` for ASK limits and bridge architecture.

The web/mobile automation APIs are private and undocumented. Treat every such endpoint and payload as version-sensitive, and do not confuse them with the official Alexa Skills Kit APIs. Read current state before private-API writes, validate exact targets, and verify state after writes.

## Core Safety Contract

1. **Resolve human names to exactly one device.** Use case-insensitive exact matching after discovery. Abort on zero or multiple matches.
2. **Never widen scope silently.** A user naming one Echo does not authorize an account-wide announcement, group, room, or “everywhere” target.
3. **Separate descriptive fields from selectors.** Verify whether fields such as `name` identify a target or merely label the sender. Inspect implementation before acting.
4. **Minimize each write.** If asked to power on an appliance, send only power-on. Do not also alter temperature, mode, fan speed, brightness, or schedules.
5. **Read → write → read.** Query current state, issue one authorized command, then poll a bounded number of times to verify the resulting state.
6. **Report API confirmation accurately.** Distinguish “command accepted” from “physical outcome verified.” If state already matched before the command, say so.
7. **Keep secrets local.** Never print cookies, customer IDs, endpoint IDs, serials, or appliance IDs. Output only names, categories, capabilities, status, and sanitized state.
8. **Avoid accidental nighttime playback.** Scheduled speech helpers should enforce a narrow local-time window. Manual tests require an explicit override tied to current user authorization.

## Workflow

### 1. Acquire and validate authentication

- Capture `ubid-main` and `at-main` locally from an authenticated Alexa mobile session using a temporary trusted interception proxy when necessary.
- A lower-friction desktop alternative is for the user to copy those two cookie values from Chrome DevTools (`Application` → `Cookies` on the authenticated Amazon domain) directly into the corresponding 1Password fields. The values must never pass through chat, screenshots, shell arguments, or agent-visible output.
- When `op inject` consumes item references, prefer immutable item IDs over titles. Duplicate item titles in one vault make title-based references ambiguous and cause injection to fail before Alexa is contacted. Verify item metadata only, point each field reference to the intended item ID, and do not delete the older item without explicit authorization.
- For durable automatic renewal, follow `references/oauth-cookie-refresh.md`. It covers one-time OAuth device enrollment, read-only 1Password operation, ephemeral cookie derivation, locking, atomic cache updates, daemon reloads, redaction and verification.
- Store credentials in a mode-0600 environment file; never place values in commands, logs, chat, or source control.
- On a VPS, have the user connect from their own device over SSH and run a hidden-input (`getpass`) helper that validates then atomically stores the secret. Do not open a remote GUI terminal merely to paste a key, and do not pass the key as a shell argument.
- Design capture helpers to exit automatically after both values are securely saved.
- After capture, restart only the Alexa integration service and validate with read-only calls before any action.
- Tell the user to remove the temporary Wi-Fi proxy and CA certificate immediately afterward.
- If the user asks only to reopen the capture process, do that task directly; pause unrelated debugging or code cleanup.

### 2. Discover devices and capabilities

- Echo inventory: query `devices-v2` for account names, online status, device family/type, and internal targeting fields.
- Smart-home inventory: use the Alexa Nexus GraphQL `CustomerSmartHome` endpoint query. The legacy `smarthome/v2/endpoints` shape may contain only Echo transport records and no useful friendly names.
- Present only sanitized fields: friendly name, primary category, and supported interfaces.
- Identify capabilities from interfaces, especially:
  - `Alexa.PowerController`
  - `Alexa.ThermostatController`
  - `Alexa.ModeController`
  - `Alexa.ToggleController`
  - `Alexa.TemperatureSensor`
  - `Alexa.EndpointHealth`

### 3. Speak on one Echo

- Account-wide communications announcements are not device selectors merely because their payload contains a `name` field; that field can be the sender name.
- For one Echo, use a `PREVIEW` behavior sequence with a single `Alexa.Speak` operation targeted by device type, serial number, customer ID, and locale.
- Query devices immediately before playback and require one exact online Echo match.
- Keep spoken briefs bounded (typically 60–90 seconds and under the tested character limit).
- For scheduled briefs, write the exact spoken text to a local audit file, dry-run validation first, then perform one live call. Do not retry live playback more than once automatically because a timeout can still have produced audio.
- For a manually authorized non-morning brief, use a distinct manual mode plus an explicit outside-window override. Do not weaken the scheduled morning helper's required opening or time gate globally.
- On screen-capable Echo devices, a capability such as `EFDCARDS` indicates card/display support but does not prove that `Alexa.Speak` rendered a visual card. Report HTTP 200 as targeted voice-command acceptance; report visual rendering as unverified unless a separate display operation or device-state signal confirms it.

### 4. Schedule source-grounded spoken briefs

- Collect facts deterministically before the model writes prose: current weather, date-scoped durable journals/state/artifacts, and current monitor snapshots.
- Never bind a brief to a Claude Code/Chrome/Hermes conversation ID or assume one long-lived session. Export a shared collector function that accepts a calendar date so written and spoken briefs aggregate all persistent records across changing sessions.
- Prefer calling that shared date-scoped collector directly over reading another cron job's saved response by job ID. This removes unnecessary cron-to-cron coupling and prevents a renamed/recreated briefing job from breaking the spoken brief.
- Compare live read-only data against stored baselines when freshness matters, without mutating the monitor’s baseline.
- Require an exact opening, locale, maximum length, source hierarchy, and forbidden internal names.
- Never let the model invent missing metrics. If a source is absent or stale, state that briefly.
- Deliver locally when the user requested Alexa-only output; avoid duplicate chat delivery.
- The host, scheduler, network, credentials, and target Echo must be available at fire time.

### 5. Control a smart-home appliance

- Discover all candidate appliances first. If multiple air conditioners or thermostats exist, ask the user to choose by friendly name.
- Verify the selected endpoint exposes the requested writable interface.
- Query Phoenix state using the appliance/entity identifier and requested properties.
- For power, send a Nexus GraphQL `setEndpointFeatures` operation to the endpoint ID.
- For thermostat changes, apply and verify mode before temperature. Phoenix `setThermostatMode` can set `COOL`, but target temperature should use Nexus `featureName: thermostat`, `featureOperationName: setTargetSetpoint`, and a JSON `payload.targetSetpoint` object; see the reference payload.
- Skip any write whose pre-read already matches the requested value.
- Parse HTTP status, top-level GraphQL errors, and feature-control errors.
- Poll state a small bounded number of times and report before/after values, connectivity, and unchanged settings when relevant.

### 6. Build a shared internal CLI and MCP core

When Alexa actions start accumulating as one-off scripts, consolidate them into a class-level internal CLI backed by a runtime-neutral core that the MCP imports directly.

- Keep transport, exact-device resolution, risk policy, recursive redaction, domain normalization, and verification in shared modules.
- Make the CLI JSON-first with stable error codes; writes are dry-run by default and require explicit confirmation.
- Make MCP tools thin adapters over the same client instead of chaining MCP → REST → Alexa.
- Maintain two endpoint inventories: a small curated operational allowlist and a generated source-snapshot research inventory.
- Scope “all endpoints” to named source snapshots and evidence levels. Static discovery is not proof of liveness, authorization, or safety.
- Validate with TDD, type-check, lint, dependency audit, live read-only probes, and a separate MCP runtime exercise when restart/deploy is authorized.

See `references/internal-cli-and-endpoint-inventory.md` for the architecture, command safety contract, endpoint extraction method, recurrence normalization, tests, and verification gates.

## Common Pitfalls

- **Global announcement trap:** an announcement API may broadcast to all eligible Echos even when a `name` field is present.
- **New endpoint representation shape:** `smarthome/v2/endpoints` can return records with `endpointDecorators` and no direct names/categories; use Nexus GraphQL for smart-home discovery.
- **Duplicate or ambiguous names:** smart-home inventories often contain repeated generic names. Never choose the first match for a physical action. A user's singular phrase such as “the air conditioner” is not sufficient when discovery yields multiple `AIR_CONDITIONER`/`THERMOSTAT` candidates, even if one friendly name sounds like the most obvious semantic match; present only sanitized friendly names and ask which exact device.
- **Aggregate online-count trap:** a smart-home inventory summary can report zero online devices while still returning endpoints and capabilities. Do not use that aggregate alone to declare every appliance offline or online. Resolve the exact candidate, then query its endpoint health/state before a write; if exact health or pre-state cannot be established, fail closed.
- **Split identity bug:** do not resolve a requested light and then fetch a separate “primary” appliance or endpoint ID. Preserve endpoint, CHRS entity, appliance, and merged-appliance identifiers from the same exact `CustomerSmartHome` record; bind control to the identifier that produced the pre-state.
- **Discovery without readable state:** a friendly-name match is not enough for a safe physical write. If no identifier belonging to that exact endpoint yields usable pre-state, return `STATE_UNAVAILABLE` and do not write blindly.
- **Permissive empty responses:** accept empty `2xx/204` only for explicitly declared write endpoints. Missing or malformed inventory/state arrays must fail closed; treating them as `[]` can turn an upstream failure into a duplicate alarm or unintended write.
- **CLI flag-as-value bug:** reject missing/repeated value flags and any next token beginning with `--`; otherwise an authorization flag can accidentally become the command payload while also enabling the write.
- **Mocked transport is not device proof:** source code and unit fixtures validate request construction, not that a private endpoint still performs the physical action. Label evidence accurately and require a separately authorized live write plus post-read before calling the operation live-verified.
- **1Password env-file quoting mismatch:** `op inject` may write `KEY=value` without quotes while older helpers parse only `KEY="value"`. Parse both quoted and unquoted dotenv assignments without logging values, and validate only required-key presence before targeted playback.
- **Already-on state:** a successful `turnOn` response does not mean the command changed state. Report that it was already on if the pre-read says `ON`.
- **State lag:** use bounded polling instead of one immediate read or an unbounded retry loop.
- **False-success thermostat write:** Phoenix can return HTTP 200 for `setTargetSetpoint` or `setTargetTemperature` while leaving the target unchanged. Verify state and use Nexus GraphQL `thermostat/setTargetSetpoint` with JSON payload when Phoenix is a no-op.
- **Schema nullability:** Alexa payloads may legitimately return `null` in descriptive fields. Validation schemas should model observed nullability rather than rejecting the entire inventory.
- **Scope creep during setup:** do not mix credential capture, repository cleanup, unrelated bug fixes, and device actions when the user asked for one immediate operation.
- **Alexa app UI assumption:** never instruct the user to press a Dev Skill `Launch`/`Open` button without first confirming it exists in their app version. A current Android detail page may expose only `DISABLE` plus the bottom `Ask Alexa` text field; use that field for a typed invocation when isolating ASR from upstream routing.
- **Publishing-example/model mismatch:** `publishingInformation.locales[*].examplePhrases` only controls store/app metadata; it does not train the interaction model. Ensure every carrier phrase shown to the user is represented in the custom intent samples. For example, `Alexa, dile a Hermes personal que diga hola` reaches the skill as an utterance shaped like `diga hola`, so the model needs `diga {query}`. If launch succeeds but a direct query produces no new ngrok request, inspect NLU samples before debugging Hermes. Add a regression test, build the locale to `SUCCEEDED`, and read the model back.
- **Free-form UX overclaim:** do not present one successful test carrier (for example, `diga`) as the Skill's intended interface or imply that Hermes accepts only canned questions. `AMAZON.SearchQuery` is open-ended but Amazon requires carrier text in normal samples, so a bare `{query}` cannot implement guaranteed `Alexa, <invocation> <anything>`. Offer the closest official UX explicitly: one-shot `Alexa, pregúntale a <invocation> <natural question>`, or two turns—`Alexa, <invocation>` followed by the natural question while the session is open.
- **Default-assistant routing overclaim:** enabling one Custom Skill across an Amazon account does not make it the catch-all assistant on every Echo. Routines match predefined phrases, `AMAZON.FallbackIntent` only runs after the Skill is open, and ordinary Custom Skills cannot claim every post-wake-word utterance. Before suggesting Name-Free Interaction, re-check Amazon's current eligibility and locale docs; in the July 2026 documentation it was limited to hidden Alexa Smart Properties skills and English locales, and Alexa—not the developer—selected among eligible handlers.
- **Per-Echo continuity is not global interception:** once a signed Skill request arrives, use `context.System.device.deviceId` only as input to an HMAC/hash-derived conversation key so each Echo can have independent continuity and the response naturally returns to the originating device. Keep user authorization separate, never log/store the raw device ID, and do not imply that per-device routing changes Alexa's upstream invocation requirement.
- **Private-API/reverse-engineering boundary:** private Alexa APIs can discover/control devices and trigger exact-device speech, but they are not a reliable ingress for always-on microphone audio, arbitrary transcripts, or replacement of the Echo's default cloud endpoint. Do not propose polling voice history or wildcard routines as a substitute for a supported voice ingress. For truly direct `Hermes <anything>` interaction, recommend a separate voice satellite (local wake word + STT + Hermes + TTS); an Echo may be an output speaker, but its closed microphones should not be assumed reusable.
- **Question-carrier loss:** samples such as `qué {query}` and `por qué {query}` strip the carrier from the delivered slot. If Hermes needs the complete question, use one intent per semantic carrier and reconstruct the prefix before dispatch (`qué`, `cuál`, `cómo`, `cuándo`, `dónde`, `quién`, `por qué`). Cover both the interaction-model samples and reconstruction mapping with regression tests; publish to `SUCCEEDED` and read the remote model back.
- **Valid speech response but silent Echo:** `HTTP 200` alone is insufficient, but a timely signed `IntentRequest` response containing valid `version`, nonempty `response.outputSpeech`, and `shouldEndSession` proves the bridge produced speech. If the Echo remains silent after that boundary, do not rewrite NLU, TLS, or Hermes blindly. Inspect the sanitized/decode-only response body, then isolate downstream Amazon/device rendering with a built-in Alexa speech check, volume/DND/network state, and one bounded retry.
- **Outer-cron false success:** an agent-driven cron can finish with `last_status: ok` after correctly reporting that its nested exact-device speaker exited nonzero. Diagnose scheduled audio from the helper's exit code and durable playback ledger, not the cron status alone. A generated script and successful dry-run prove neither Amazon acceptance nor physical audio.
- **Manual replay after a proven authentication failure:** an idempotency ledger should block `started`, `accepted`, `unknown`, and `uncertain_or_failed` by default. Replay a missed brief only after (a) authentication again passes a read-only probe, (b) the user explicitly confirms the earlier brief was not heard and authorizes playback now, and (c) the helper uses separate explicit outside-window and retry-known-failed flags. Permit the override only for `uncertain_or_failed`, perform one dry-run and one live attempt, never bypass an `accepted`/`started`/`unknown` record, and verify the ledger becomes `accepted` for the exact Echo with HTTP 200.
- **Injected-but-expired session:** successful 1Password injection and nonempty `ubid-main`/`at-main` fields do not prove Alexa authorization. Confirm with a read-only device query; if it returns `HTTP 401`, rotate only those mobile-session fields rather than debugging volume, DND, ngrok, NLU, or the brief renderer.
- **Capture destination drift:** after migrating runtime secrets to 1Password, re-audit the mobile capture addon's destination. A capturer that still writes project `.dev.vars` can appear to succeed while leaving scheduled jobs broken. Capture to a protected pending file, validate read-only, then update the durable 1Password fields with a human write-capable identity while keeping the service account read-only.
- **OAuth proxy readiness mistaken for failure:** `alexa-cookie2` 5.x proxy-only enrollment calls its callback first with an `Error` telling the user to open the loopback URL, then calls it again after login with registration data. Do not stop the proxy or settle the operation on that first callback. Ignore only the exact expected readiness message for the configured `127.0.0.1` port; treat all other errors as terminal and cover the two-callback lifecycle with a regression test. See `references/oauth-cookie-refresh.md`.
- **Post-login loop mistaken for user error:** if Amazon shows an inactive-page message and `Continue` returns to login, stop asking the user to re-enter credentials. No private pending registration file means the callback did not complete. Reproduce once with a bounded trace that records only method/status/host/path after stripping query, fragments, userinfo, cookies, headers and tokens; isolate `/ap/signin`, `/ap/maplanding`, callback exchange or regional redirect before changing one configuration variable. See `references/oauth-cookie-refresh.md`.
- **CVF/OTP 404 from embedded loopback return URLs:** a trace that reaches `/ap/cvf/transactionapproval` and then redirects `approval/poll` or `verifyOtp` to `/a/c/404` can come from loopback proxy URLs left inside URL-encoded query or POST fields even when `Referer` rewriting is correct. `alexa-cookie2` 5.0.6 adds embedded-query and buffered-form rewriting; pin the fixed version, preserve any separate GET-Referer patch with a layout check, and prove both behaviors with focused tests before one bounded live retry. See `references/oauth-proxy-cvf-404.md`.
- **Tokens-per-second shortcut:** advertised generation speed is not Alexa end-to-end latency. Benchmark the actual bridge client with identical bounded context before switching; include prompt-prefill/network time, cold and warm runs, errors, and spoken-answer quality. Route Alexa through a dedicated API Server model alias so WhatsApp/global model selection remains untouched; see the low-latency routing section in `references/hermes-synchronous-voice-bridge.md`.
- **Custom-provider option loss:** a working API Server alias can still drop provider `request_overrides` or output caps while preserving credentials. Inspect the resolved runtime shape, add a route-propagation regression, and verify low reasoning plus the live token cap through the actual alias.
- **Free-tier retry beyond Alexa's deadline:** a large Hermes prompt/tool schema can hit provider TPM limits; a default 60-second retry may continue after the bridge has returned a timeout. Space E2Es by the quota window, minimize voice-route toolsets, and prevent long retries on synchronous turns.
- **Contaminated or agentic E2E prompt:** never reuse a failed test conversation, and avoid test wording such as “prueba de voz” that can trigger Alexa speech tools recursively. Use a fresh opaque conversation and a neutral prompt; judge clean bounded speech, latency, fallback state, and unintended tools rather than exact text alone.
- **Gateway-child lifecycle trap:** bridge and tunnel processes launched as children of a live Hermes session can die on gateway restart. Install them as independent supervised user services and verify live tunnel-to-manifest equality after startup.
- **ASK wildcard-certificate enum trap:** a publicly trusted wildcard certificate is not configured as `Trusted` merely because a CA issued it. If the endpoint is covered by a wildcard CN/SAN (for example `*.ngrok-free.dev`), set the manifest's exact case-sensitive `sslCertificateType` to `Wildcard` for both default and regional endpoints. `Trusted` can produce `SSL certificate verification failed` before any HTTP request reaches ngrok; `WildCard` is not a valid enum. Poll the manifest to `SUCCEEDED` and read the fields back.

## Verification Checklist

- Authentication validated with a read-only request.
- Exact target resolves uniquely and is online/connected.
- Required capability is present and writable.
- Requested action is the only state change in the payload.
- API response is successful and contains no nested errors.
- Post-action read confirms state, or the report clearly says verification was unavailable.
- No secret or internal identifier appears in logs or user-facing output.
- Scheduled task has the correct timezone, next-run time, local-only delivery if requested, and a safe playback window.

## References

See `references/private-api-patterns.md` for sanitized endpoint shapes, payload patterns, and response parsing notes discovered during real Alexa integrations.

See `references/internal-cli-and-endpoint-inventory.md` for consolidating one-off actions into a shared CLI/MCP core, generating a scoped reverse-engineering inventory, enforcing dry-run/confirmation policy, and testing the safety contracts.

See `references/alexa-session-expiry-and-brief-recovery.md` for diagnosing scheduled briefs that generated but did not play, distinguishing outer cron success from nested playback failure, confirming expired mobile sessions with read-only probes, and safely recapturing credentials after migration to 1Password.

See `references/oauth-proxy-cvf-404.md` for the sanitized transaction-approval/OTP 404 signature, the embedded loopback callback root cause in older `alexa-cookie2`, and the focused POST-body/GET-Referer regression seams.

See `references/hermes-synchronous-voice-bridge.md` when an Alexa custom skill must call Hermes within a synchronous voice turn. It covers the external-facade boundary, `/v1/responses` versus Runs API selection, ASK CLI/no-AWS deployment, ngrok hardening, signed-request enrollment, no-traffic diagnosis, regional endpoint routing, opaque conversation/memory/idempotency identifiers, timeout semantics, approval limitations, profile isolation, and verification gates.
