---
name: web-auth-oauth
description: "Analyze an in-scope OAuth 2.0/OIDC flow: PKCE downgrade, weak redirect_uri validation, missing state/nonce, code reuse. Safe verification against your own accounts; user-affecting actions are approval-gated."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# Web Auth — OAuth / OIDC Analysis

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


HUNT phase. Inspect an authorization flow and assess each control. The goal here is to
**identify and safely demonstrate** weaknesses against accounts and clients you control
within scope — not to take over real users' accounts. Anything that would affect a real
account or persist state is exploitation: it is reversibility-gated and requires explicit
approval.

## When to Use

- When an in-scope target uses OAuth 2.0 / OIDC and the operator wants the auth flow assessed.
- When asked to "hunt OAuth account-takeover", "check PKCE enforcement", or "look at the login flow".

## Quick Reference

Controls to assess (capture the flow with an intercepting proxy — Burp or Caido):

| Control            | What to check |
| ------------------ | ------------- |
| PKCE               | Present? `S256` enforced (not `plain`)? Is the server's `code_challenge` actually validated, or can it be dropped/downgraded? |
| redirect_uri       | Exact-match validation? Open-redirect or path/subdomain tricks accepted? |
| state / nonce      | Present, unpredictable, and bound to the session (CSRF / replay protection)? |
| Authorization code | Single-use? Short-lived? Bound to the client and PKCE verifier? |
| Token handling     | Tokens leaking via `Referer`, logs, or browser history? Audience/issuer validated? |
| Scopes             | Over-broad or escalatable consent? |

## Procedure

1. **Scope first.** Ensure `engagement-scope` is loaded; confirm the auth host with `scope_check`. Flow capture/observation is `active_scan`; anything that exercises a real account or completes a takeover is `exploitation` and **gated**.
2. **Use test accounts you control.** Register or use operator-owned accounts within scope. Do not test against real users' accounts.
3. **Capture the flow.** Proxy the full authorization request, the redirect/callback, and the token exchange. Record parameters (`client_id`, `redirect_uri`, `code_challenge`, `state`, `nonce`, `code`, scopes).
4. **Assess each control** from the table. For each suspected weakness, write down the observation and the minimal evidence that proves the misconfiguration (e.g., "server accepts a flow with `code_challenge` removed" demonstrated between two operator-owned sessions).
5. **Stop at the gate.** A demonstration that would compromise another user's account, mint tokens for a non-consenting principal, or otherwise change real state is exploitation — **request human approval first** and keep it confined to test accounts/assets. Never broaden to real users to "prove impact".
6. **Record findings.** Capture request/response evidence (redact tokens/secrets in stored artifacts) into the evidence dir and hand off to `web-exploit-chain` (if it combines with other findings) or `web-report`.

## Pitfalls

- **Testing real accounts.** The fastest way to cause real harm and breach RoE. Operator-owned test accounts only.
- **Token leakage in artifacts.** Strip access/refresh tokens, codes, and client secrets from saved evidence and logs.
- **Provider lockouts.** Repeated failed flows can lock accounts or trip fraud controls — pace accordingly and coordinate with contacts.
- **Edge vs origin.** Some controls (e.g., redirect handling) differ at CDN/WAF versus the app; confirm where the behavior actually lives.
- **"Downgrade" assumptions.** A missing `code_challenge` in a request doesn't prove the server ignores PKCE — verify the server actually accepts the downgraded flow before reporting it.

## Verification

- Each control in the table is marked assessed with supporting evidence.
- Every demonstration used operator-controlled test accounts within scope.
- No real-user account was affected; any gated step has a recorded approval.
