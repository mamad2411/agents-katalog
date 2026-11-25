---
name: third-party-automation-integration
description: Safely evaluate, harden, test, and connect small community automation servers and unofficial API bridges, including MCP services.
version: 1.3.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [security, MCP, integrations, automation, third-party]
---

# Third-Party Automation Integration

Use this skill when adopting a community server, unofficial API bridge, home-automation adapter, or MCP service that will receive credentials or perform external side effects.

## Principles

- Treat source as authoritative when README, examples, schemas, and implementation disagree.
- A configured secret is not access control: verify every route actually enforces authentication.
- Prefer local-only deployment for single-host integrations and cookie-authenticated unofficial APIs.
- Test security and protocol behavior with dummy credentials before permitting real side effects.
- Preserve user control around disruptive maintenance, reboots, filesystem repair, account login, and credential capture.

## Workflow

1. **Audit the repository**
   - Inspect entry points, transport routing, environment schemas, side-effecting tools, credential construction, CORS, bind behavior, dependency ranges, license, and maintenance activity.
   - Identify private or reverse-engineered upstream endpoints and document their instability.
2. **Model the exposure**
   - Enumerate REST, MCP, SSE, callback, health, and internal loopback paths.
   - Decide which endpoints may be unauthenticated; normally only a non-sensitive health check qualifies.
3. **Harden before credentials**
   - Require authentication on every functional route and transport.
   - Bind to `127.0.0.1` unless remote access is explicitly required.
   - Remove permissive CORS unless a browser client needs it.
   - Ensure internal service-to-service requests include the same authentication.
4. **Stabilize and audit the toolchain**
   - Run baseline type-check/lint and separate upstream defects from local regressions.
   - Pin CLIs or runtimes when broad semver ranges pull incompatible versions.
   - For security upgrades, distinguish each package's advisory minimum from the minimum safe **resolved combination**. Inspect the lockfile and installed graph: a patched direct package can coexist with a vulnerable exact transitive version.
   - Find the first parent-package release that natively resolves the patched child; prefer it over a package-manager override.
   - Treat peer-dependency warnings as part of the resolved security graph. Inspect auto-installed peers, pin a compatible safe peer when needed, and rerun the production audit after the final lockfile change.
   - Validate candidate versions in a disposable copy with graph inspection, production audit, type-check, tests, and a platform build/deploy dry-run. Classify API findings as mandatory, deprecated-but-compatible, or optional modernization.
5. **Verify with dummy data**
   - Test health, unauthorized denial, authorized routing, interface binding, and full protocol discovery.
   - For MCP, initialize with an SDK client and list tools; do not treat a curl response as complete protocol verification.
6. **Add real credentials locally**
   - Never request passwords, authorization codes, refresh tokens, client secrets, session cookies, or sensitive personal data through chat.
   - Use a local interactive flow and secret storage excluded from source control and logs.
   - For browser-based OAuth onboarding over chat, guide exactly one visible checkpoint at a time. Treat commentary/tool-progress text as non-delivery on messaging platforms: every action the user must take must appear complete in the final user-facing answer, with the immediate URL and click target, then wait for the exact screen the user sees. Do not bury required actions in progress narration or dump the entire wizard at once.
   - If OAuth accepts credentials/MFA but loops to login or a generic 404, stop repeated human attempts. Capture one sanitized HTTP sequence containing only method, host/path without query or fragment, status, and redirect host/path. Never log headers, cookies, bodies, authorization codes, state, or query values. Check relative XHR paths plus `Referer`/`Origin` rewriting on every method, especially GET polling endpoints.
   - When the defect is inside a pinned dependency, prove it with a focused RED harness against the installed package seam, apply the smallest patch, and persist it through an idempotent version/layout-checked install hook that fails closed on upstream drift. Re-run the focused test and full suite, then disable diagnostic tracing after confirmation.
   - See `references/oauth-proxy-login-loop-debugging.md` for a concrete safe-trace pattern and a GET-polling/Referer failure signature.
   - For mobile-cookie capture, use a narrowly filtered temporary proxy, guide setup one checkpoint at a time, and distinguish browser CA trust from app certificate pinning.
   - Complete OTP/login with the proxy disabled, then re-enable it only to refresh authenticated pages and capture final cookies; pinned code-delivery services may fail through the proxy.
   - Check the proxy's completion signal before restarting it: intentional auto-exit may mean capture succeeded.
   - Do not patch/re-sign a pinned mobile app automatically; choose a lower-risk browser session when viable or obtain explicit consent for higher-risk instrumentation.
7. **Exercise the smallest safe side effect**
   - Compare the tool description with the actual upstream request payload; implementation determines whether a field targets one device or broadcasts.
   - If actual scope differs from requested scope, stop and reconfirm before acting.
   - Use a short, non-sensitive test against one explicitly selected target.
   - Distinguish upstream acceptance from observed delivery, then close temporary servers, browsers, and sessions.

## Mid-run cancellation

When the user cancels an integration build or deployment:

- Stop immediately; do not continue installs, tests, credential setup, deployment, cleanup, or retries unless the user explicitly asks.
- Do not delete partial artifacts by default. Deletion is a separate state-changing action and may destroy useful work.
- Cancel outstanding checklist items and report the exact boundary reached: local files created, credentials configured or not, external deployment performed or not, and any process that may still be running.
- Never describe an unverified partial scaffold as working. If execution stopped before RED/GREEN verification, label it partial and untested.

## Transactional browser automations

For automations that can create orders, reservations, paid subscriptions, or other consequential transactions:

- Separate the availability detector from the transaction executor. The detector emits a stable product/resource ID; the executor re-fetches and independently validates identity, variant, stock, quantity, currency, unit-price ceiling, and final-total ceiling.
- Resolve user-supplied names to stable IDs and exact variants before arming. Never let fuzzy name matching authorize a transaction.
- Make rehearsal mode structurally unable to commit: stop at the merchant's final review page, leave terms unchecked, and omit any code path that presses the final order/payment control.
- Revalidate the total after shipping and again after choosing the payment method. Packaging, insurance, international shipping, taxes, or payment-method fees may appear only on the final review.
- Normalize the cart after authentication. Saved-account carts may merge with anonymous carts and retain unrelated or out-of-stock items; remove every non-allowlisted line and force the exact permitted quantity before continuing.
- Treat merchant login, payment-provider login, delivery address, and MFA as separate prerequisites. A payment credential alone may not be enough to reach checkout.
- Use an atomic claim/ledger before any live commit so concurrent heartbeat ticks cannot place duplicate orders. Record a durable order reference before releasing the claim.
- Report state precisely: “payment method selected,” “final review reached,” “order created,” and “payment completed” are distinct outcomes.
- Close browser contexts in `finally`, store evidence with restrictive permissions, and crop or redact screenshots so addresses and payment data are not captured.
- See `references/transactional-browser-checkout-rehearsal.md` for checkout-specific probes and failure patterns.

## Consequential non-payment form submissions

For job applications, registrations, claims, and similar forms that create a durable external record:

- Separate discovery, evaluation, staging, and submission; each stage must be independently idempotent and verifiable.
- Once the user grants a standing auto-submit policy, encode stable defaults once and stop asking for per-record approval. Preserve hard stops for unknown facts, ambiguous eligibility, duplicate/rejected attempts, authentication challenges, and missing first-party confirmation.
- Submit only through the canonical first-party form, and mark success only after durable visible evidence from that system.
- Bound unattended evaluators with an exclusion lock, process timeout, small batch size, and guaranteed cleanup; never let a background reasoning process outlive the reporting cron unnoticed.
- On Linux Chromium/CUA, force renderer accessibility, bind to the exact window/session, use stable element handles, and visually verify every field/action. A tool reporting success while the field remains empty is a failed action, not progress.
- Treat `mutation_allowed=false` as a typed-page-route refusal, not proof that all safe GUI automation is blocked. Continue through the native CUA ladder with fresh snapshots: AX element action → verified pixel action → foreground delivery only after an observed/refused background attempt. Stop only when the supported ladder is exhausted or authentication/factual input is genuinely required.
- Design authentication handoffs for resumability: prepare a reusable driver-owned isolated browser profile before asking the user to log in, preserve only that profile, and make the user perform passwords, magic links, MFA, or CAPTCHA—not the rest of the form.
- Report blockers as short bullets containing the record, exact blocker, and single required user action. Put the action summary at the end; do not bury it under implementation history.
- See `references/consequential-form-auto-submission.md` for the policy model, runner contract, Linux Chromium launch flags, exact-bound interaction loop, authentication handoff, and safe-upgrade procedure.

## Persistent local service discipline

When promoting a validated temporary server into a user service:

- Treat `active (running)` as provisional; wait for readiness, hit health/auth endpoints, inspect the current invocation's logs, and confirm the listener address.
- Add systemd hardening iteratively. JavaScript Worker runtimes may require narrowly writable state/log directories and `AF_NETLINK` for interface discovery even when the application binds only to loopback.
- Whitelist exact paths rather than weakening `ProtectSystem` or `ProtectHome` globally.
- Re-test MCP discovery from the actual client after enabling the service.
- For private single-user web apps, use loopback-only rootless containers, Tailscale Serve as the sole ingress, a lingered user service, and verified database/storage backups; do not claim registration is closed before the first account exists and the disabled state is read back.
- See `references/local-worker-service-and-mobile-session-capture.md` for a concrete checklist and failure signatures.
- See `references/private-tailnet-self-hosting.md` for the validated rootless Podman, alternate-port Tailscale Serve, persistence, onboarding, and backup pattern.

## Failure isolation

Package-manager errors such as `EBADMSG`, error `-74`, inode checksum failures, or corroborating kernel filesystem errors are storage signals, not dependency-resolution failures.

- Stop retrying the same disk-backed directory.
- Inspect the mount, exact path, and kernel logs before cleanup.
- Never run `fsck` on a mounted root filesystem or reboot without explicit approval.
- A tmpfs build can separate code/dependency problems from disk corruption, but both the working directory and package store/cache must be in tmpfs.
- Verify `pwd` immediately before the package-manager command.
- A successful RAM build is diagnostic, not a permanent installation.

## Verification checklist

- Type-check and lint pass.
- Listener is bound only to intended interfaces.
- Unauthenticated functional requests return `401`.
- Authenticated requests reach the expected transport.
- MCP SDK initializes and discovers the expected tools.
- No real side effect occurred during dummy-credential testing.
- Temporary services, proxies, browser sessions, mobile proxy settings, and user CAs are cleaned up.
- Secrets are absent from chat, Git, logs, and public deployment configuration.

## References

- `references/dependency-security-upgrade-analysis.md` — resolved-tree security analysis, disposable upgrade validation, and an MCP/Cloudflare compatibility case study.
- `references/community-mcp-adoption.md` — detailed MCP/reverse-engineered API audit and tmpfs isolation notes.
- `references/local-worker-service-and-mobile-session-capture.md` — systemd hardening for local Worker runtimes and safe Android session-capture workflow.
- `references/private-tailnet-self-hosting.md` — private rootless Podman web stacks behind Tailscale Serve, including persistence, registration handoff, and verified backups.
- `references/transactional-browser-checkout-rehearsal.md` — safe checkout rehearsal, cart normalization, final-total validation, and no-commit boundaries.
- `references/consequential-form-auto-submission.md` — standing auto-submit policy, staging/confirmation contract, bounded runners, Linux Chromium/CUA exact-bound controls, authentication handoffs, and safe upgrades with local integrations.
- `references/cloud-health-data-oauth.md` — Google Health/Fitbit direction, read-only health scopes, OAuth token lifetime, one-checkpoint onboarding, and sensitive-data minimization.
- `references/connected-health-device-private-api-and-ble.md` — discovery and safe read-only integration of consumer health devices whose apps use private cloud APIs and BLE, including cloud-vs-local source selection, model-dependent metrics, and the pacer-sector/physical-zone distinction.
- For Alexa-specific exact-device speech, smart-home discovery, thermostat control, and private-API payloads, load the class-level `alexa-smart-home-automation` skill rather than duplicating those version-sensitive details here.
