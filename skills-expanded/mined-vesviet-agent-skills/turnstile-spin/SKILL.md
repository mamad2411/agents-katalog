---
name: turnstile-spin
description: Implements end-to-end Cloudflare Turnstile CAPTCHA protection — widget creation, managed siteverify Worker deployment, and frontend integration — turning a "set up Turnstile" request into a validated, working integration. Use when adding bot protection to forms or gated flows in vanilla HTML, Next.js, Astro, SvelteKit, or Hugo projects.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Turnstile Spin

Turns the prompt "set up Turnstile" into a working end-to-end integration: a widget, a deployed managed siteverify Worker, frontend snippets at every chosen insertion point, and a real validation pass before reporting success.

You are the agent. Run the wizard below by invoking the scripts under `scripts/` and branching on their JSON output. The scripts hold the deterministic logic (API calls, retry/error handling); your job is orchestration, codebase reading, confirmation, and the frontend edits.

Canonical instructions live at [`developers.cloudflare.com/turnstile/spin`](https://developers.cloudflare.com/turnstile/spin/). If the docs page and this file disagree, trust the docs page.

## When to Use

- adding bot protection to a form or gated flow (login, signup, checkout)
- integrating Turnstile into vanilla HTML, Next.js, Astro, SvelteKit, or Hugo
- deploying a managed `siteverify` Worker and wiring server-side validation
- choosing the least-intrusive widget mode for a given risk level
- re-triggering the widget on token expiry or backend validation failure

## Core Rules
- Do NOT write the Turnstile secret to disk. Only pass it via stdin to `wrangler secret put`.
- Do NOT skip validation (Step 11).
- Do NOT overwrite files without showing a diff.
- Do NOT deploy a Worker to a different account than the widget was created in.
- Do NOT call siteverify from the browser. Always: browser -> user's Worker -> siteverify.
- Always choose the least-invasive widget mode (`non-interactive` or `invisible`) that maintains security requirements, falling back to `managed` for critical checkpoints.
- Ensure that tokens are never reused; they are single-use and expire within 300 seconds. Re-trigger the Turnstile widget on any failed form submission.
- **WIDGET-MODE-SELECTION**: `managed` for login/checkout/password-reset (shows interactive challenge if suspicious); `non-interactive` for medium-risk (browser telemetry only, may fail in privacy-hardened browsers); `invisible` for low-risk only (highest false-positive risk).
- **TOKEN-REUSE-PREVENTION**: On backend validation failure, frontend MUST call `turnstile.reset(widgetId)` — do NOT show a generic error; user must complete a fresh challenge.
- **CSP-TURNSTILE-DOMAINS**: Add Cloudflare Turnstile script domains to the site's Content Security Policy (`script-src` and `frame-src`) before deployment — missing CSP entries silently block the widget.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| Turnstile docs | `https://developers.cloudflare.com/turnstile/` | Core API reference, script widget parameters |

## Suggested Process
1. Check credentials and account ID by running the auth-probe script.
2. Probe active domain settings, scans codebase layout, and present insertion plans.
3. Call api.cloudflare.com client endpoints to build the CAPTCHA widget.
4. Deploy siteverify Workers templates with wrangler.
5. Apply frontend changes and check responses via validate tool scripts.
6. Guide the integration by choosing the right widget mode and setting up token expiration handling.
7. Implement frontend listeners to reset and re-render the Turnstile widget upon backend validation failure or token expiry.

### Widget Modes, Token Handling, and Verification

#### Widget Modes Selection

Widget mode details (`managed`, `non-interactive`, `invisible`) and the
rule-of-thumb for choosing the least-intrusive mode that satisfies the
security threat model are documented in
[`references/code-patterns.md`](references/code-patterns.md#widget-modes-reference).
Framework-specific integration patterns (Astro, Hugo, Next.js app/pages,
SvelteKit, vanilla HTML) live under `references/`.

#### Token Expiry & Reuse Prevention

Turnstile validation tokens are single-use to prevent replay attacks and
remain valid for exactly 300 seconds (5 minutes). If validation fails on the
backend, the token becomes spent. The frontend must immediately reset the
widget instance rather than showing a generic submission failure. The full
frontend reset pattern and the siteverify Worker template live in
[`references/code-patterns.md`](references/code-patterns.md).

#### Backend verify Worker Endpoint Pattern

Always verify the client token server-side via a secure endpoint. Never
invoke siteverify directly from the web client. The siteverify Worker
implementation is in
[`references/code-patterns.md`](references/code-patterns.md#backend-siteverify-worker-implementation).

## Checklist
- [ ] Account and API auth are verified.
- [ ] Target domain is registered for widget.
- [ ] Widget is created via Turnstile API.
- [ ] siteverify Worker is deployed.
- [ ] Frontend form submission gates on widget success.
- [ ] Widget mode (`managed`, `non-interactive`, or `invisible`) is explicitly selected based on use case constraints.
- [ ] Token reuse is prevented by resetting the widget via `turnstile.reset()` on submission failure.
- [ ] Token expiry (300-second window) is handled gracefully with automatic widget re-triggering.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and 
alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Failure Modes

- **Secret on disk**: the Turnstile secret is written to a file or committed. Mitigation: only pass the secret via stdin to `wrangler secret put`; never write it to disk.
- **Validation skipped**: a form submits without siteverify server-side check. Mitigation: require server-side validation; treat browser-side checks as untrusted.
- **Cross-account deploy**: a siteverify Worker is deployed to a different Cloudflare account than the widget. Mitigation: verify the active account before deploy; reject cross-account deploys.
- **Siteverify called from browser**: the browser calls siteverify directly. Mitigation: always route browser → user's Worker → siteverify; reject client-side siteverify calls.
- **Token reuse**: a failed submit does not reset the widget, allowing the same token to be retried. Mitigation: call `turnstile.reset(widgetId)` on backend validation failure; require a fresh challenge.
- **CSP missing**: the widget does not load because the site CSP blocks the Turnstile script. Mitigation: add `challenges.cloudflare.com` to `script-src` and `frame-src` before deploy.
- **Token expired**: a token is older than 300 seconds. Mitigation: re-trigger the widget automatically on token expiry; do not retry the same token.
- **Wrong widget mode**: a low-risk checkpoint uses `invisible` for a high-risk flow. Mitigation: use `managed` for login/checkout/password-reset; reserve `invisible` for low-risk only.
- **Diff not shown**: a frontend file is overwritten without showing a diff. Mitigation: always show a diff before writing; never overwrite silently.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a malicious frontend could try to bypass the widget by skipping the `cf_token` field. Mitigation: server-side validation must reject any request without a verified token.
- **ASI03 Identity & Privilege Abuse**: the Turnstile secret must never reach the browser; load it only into the siteverify Worker via `wrangler secret put`.
- **ASI04 Supply Chain**: the Turnstile widget script URL and the siteverify endpoint must be the canonical Cloudflare domains; reject third-party script sources.
- **ASI05 RCE Guard**: never construct siteverify payloads, widget configs, or token-handling logic from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the deployment plan is consumed by Cloudflare Engineer and DevOps; emit a structured contract so each role can validate the rollout.

## Related Skills
- **wrangler**: Manage deployment environments and bindings.
- **debug-workers-edge**: Troubleshoot execution at the edge.
