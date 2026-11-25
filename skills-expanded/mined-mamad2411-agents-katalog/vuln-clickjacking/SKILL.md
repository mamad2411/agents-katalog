---
name: vuln-clickjacking
description: Clickjacking and UI-redressing validation — test framing protections, craft minimal PoC overlays, and assess sensitive-action exposure without deploying live attacker pages.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Clickjacking — framing-protection validation

Use this skill to evaluate whether a target application protects against UI redressing (clickjacking). Check X-Frame-Options, CSP frame-ancestors, and framing behavior. Build minimal proof-of-concept overlays demonstrating the risk without deploying public attacker infrastructure or tricking real users.

## Required inputs

- Written scope naming the target origin, sensitive pages to test (account deletion, password change, OAuth authorization, payment confirmation, MFA disable), and explicit permission for framing tests.
- Valid authorization cache for the target. Separate permission required if testing OAuth authorization clickjacking or cross-origin action confirmation.
- A local HTML test harness for framing verification — no public hosting required.
- Known list of sensitive one-click actions identified during recon.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — protection header audit

Check every in-scope page for anti-framing headers:
1. For each sensitive endpoint, send a HEAD or GET request.
2. Extract `X-Frame-Options`: `DENY` (most secure), `SAMEORIGIN` (allows self-framing), `ALLOW-FROM <uri>` (deprecated, limited support), or absent (vulnerable).
3. Extract `Content-Security-Policy` header and inspect `frame-ancestors` directive: `'none'` (secure), `'self'` (allows same-origin), `*` (fully permissive), or absent.
4. Note: CSP `frame-ancestors` overrides `X-Frame-Options` in modern browsers when both are present.

Record the protection posture for each endpoint. An endpoint missing both headers is the baseline for a clickjacking finding.

### Phase 2 — framing verification

Confirm whether the browser actually blocks framing:
1. Create a local HTML file with an `<iframe src="https://TARGET/sensitive-page">`.
2. Open it in a browser where you are authenticated to the target.
3. Observe whether the target page loads inside the iframe or is blocked (blank frame, console error, redirect).
4. If the page loads inside the iframe → framing is possible, clickjacking risk is confirmed.
5. Test with `sandbox` attribute variants: `sandbox="allow-scripts allow-forms allow-top-navigation"` (without `allow-same-origin`). Some protections rely on same-origin checks that sandbox can bypass.

### Phase 3 — sensitive action surface mapping

Identify actions that could be triggered via a single click if overlaid:
- Account deletion (`/account/delete`, `/settings/delete-account`);
- Password change (`/settings/password`, `/account/security`);
- Email change or recovery-email modification;
- OAuth authorization grant (`/oauth/authorize?client_id=...&response_type=code`);
- Payment or transfer confirmation;
- MFA/2FA disable (`/settings/mfa/disable`);
- API key creation or permission escalation;
- Privacy setting changes (making a private profile public).

For each action, record: URL, HTTP method (GET vs POST — GET is riskier for clickjacking), whether the action has a confirmation step (secondary button, CAPTCHA, re-authentication), and whether it uses CSRF tokens.

### Phase 4 — proof-of-concept construction

Build a minimal local PoC overlay — this is evidence, not an attack tool. Do not deploy publicly:

```html
<!-- local PoC: demonstrates overlay risk without tricking real users -->
<!DOCTYPE html>
<html>
<head><title>Clickjacking PoC — LOCAL ONLY</title>
<style>
  body { font-family: sans-serif; }
  #decoy {
    position: absolute; top: 300px; left: 200px; z-index: 1;
    padding: 12px 24px; background: #007bff; color: white;
    border: none; border-radius: 4px; font-size: 16px; cursor: default;
  }
  #target_frame {
    position: absolute; top: 100px; left: 0; width: 100%; height: 600px;
    opacity: 0.3; z-index: 2;
  }
</style>
</head>
<body>
  <h2>Clickjacking PoC — LOCAL TEST ONLY</h2>
  <p>This page demonstrates that <code>TARGET/sensitive-action</code> can be framed and overlaid.</p>
  <div id="decoy">Harmless decoy button — DO NOT CLICK in production session</div>
  <iframe id="target_frame" src="https://TARGET/sensitive-action"></iframe>
</body>
</html>
```

The PoC must:
- Use a dummy decoy button with no real consequences.
- Set iframe opacity to a visible level (≥0.3) for reviewer clarity — the point is to demonstrate overlay, not to hide it.
- Include clear labeling that this is a local test, not a live attack.
- Never be hosted on a public URL unless the scope and maintainer explicitly authorize a demonstration environment.

### Phase 5 — bypass technique assessment

Test only if initial protections appear present but may be incomplete:
- **Sandbox bypass**: `<iframe sandbox="allow-scripts allow-forms allow-top-navigation">` — if the page loads without `allow-same-origin`, same-origin framing restrictions may be bypassed.
- **Double framing**: frame the target inside an allowed-origin frame, which is itself framed by the attacker page. Legacy ALLOW-FROM bypass.
- **Drag-and-drop variant**: if the target page allows text selection, dragging selected text from the framed target into an attacker-controlled textarea may leak content without requiring a click. This is a distinct finding (drag-and-drop data extraction), not classic clickjacking.

## Decision points

- **Stop at missing headers + successful framing**: if both `X-Frame-Options` and CSP `frame-ancestors` are absent on a sensitive one-click action, clickjacking is confirmed.
- **Downgrade on SAMEORIGIN + no sensitive GET actions**: `X-Frame-Options: SAMEORIGIN` is acceptable when the application has no sensitive GET-only one-click actions.
- **Escalate on critical action exposure**: account deletion, OAuth authorization, or payment confirmation without framing protection is high severity.
- **Refuse live deployment**: do not host the PoC on a public server, send PoC links to real users, or use the overlay against production user sessions.

## Prohibited behavior

- Hosting clickjacking PoC pages on public infrastructure accessible to real users.
- Tricking real users, employees, or testers into clicking overlaid buttons.
- Using clickjacking to perform actions on real user accounts or production data.
- Combining clickjacking with CSRF or XSS to chain attacks beyond the framing demonstration.
- Framing pages that display real user data in the PoC screenshot or evidence.

## Stop conditions

- Both `X-Frame-Options: DENY` and CSP `frame-ancestors 'none'` present → protected, stop.
- Framing confirmed on a sensitive one-click endpoint → finding confirmed, stop testing that endpoint class.
- WAF adds framing headers, CDN blocks iframe loads, or detection-team contact.

## Evidence — framing posture matrix

For each tested endpoint, record:

```text
Endpoint: <URL>
Action type: <account delete | OAuth authorize | password change | payment confirm | ...>
Action method: <GET | POST>
X-Frame-Options: <DENY | SAMEORIGIN | ALLOW-FROM | absent>
CSP frame-ancestors: <'none' | 'self' | * | absent>
Framing confirmed: <yes | no | blocked>
Sandbox bypass works: <yes | no | not tested>
Confirmation step present: <yes (CAPTCHA | re-auth | secondary button) | no>
Impact: <none | clickjacking confirmed | critical action clickjackable>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a framing posture matrix per endpoint class. Include both protected and vulnerable endpoints. Never store: screenshots containing real user data, iframe content showing authenticated sessions, or PoC files hosted on public URLs.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected endpoint, missing headers, action risk, CVSS estimate (4.3–6.5 for medium-impact actions, 6.5–8.0 for account deletion/OAuth/payment), and remediation guidance.
2. Reference the framing posture matrix and local PoC file location.
3. Recommend: `X-Frame-Options: DENY` on all pages, CSP `frame-ancestors 'none'` (or `'self'` if same-origin framing is required), confirmation dialogs with re-authentication for all sensitive actions, and SameSite cookie attributes.
