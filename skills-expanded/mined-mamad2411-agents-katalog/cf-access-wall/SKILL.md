---
name: cf-access-wall
description: >
  Put any set of hostnames — including bare *.workers.dev Workers, no custom domain needed —
  behind a Cloudflare Access login wall (GitHub SSO and/or emailed one-time PIN for non-technical
  users) from a declarative JSON spec, idempotently. Handles the Zero Trust org, identity
  providers, per-app sessions, email allow-lists, and service tokens for CLI/CI clients. Use when
  capability URLs / unguessable slugs are no longer enough and a team needs real identity on
  private mini-sites. Triggers: "protect this site with login", "GitHub login on the site",
  "email code login", "Cloudflare Access", "put the workers behind auth", "secure the mini-site".
allowed-tools: Read, Bash, Grep, Glob
---

# cf-access-wall — declarative Access provisioning

Zero Trust free tier covers 50 seats; Access attaches **directly to `*.workers.dev` hostnames**
(verified live 2026-07-23 — no zone, no domain purchase). One Access app offers BOTH login paths
on a single screen: **GitHub** for developers, **emailed 6-digit code** for non-technical staff
(no account creation). Enforcement is real: unauthenticated requests 302 to the team login page.

> **Self-Evolving Skill**: Cloudflare's API/dashboard drift → fix scripts + the dashboard-forge
> Vendor Quirks log immediately on real breakage.

## Flow

1. **Spec** — write `<project>/…/access-spec.json` against
   [`schema/access-spec.schema.json`](schema/access-spec.schema.json). The spec lives in the
   PROJECT repo (it carries team emails); this skill stays agnostic.
2. **Scoped token** (once per account) — the existing account token usually lacks Access scopes
   and cannot grant itself more. Forge one via the **dashboard-forge** method (sibling skill):
   human logs into dash.cloudflare.com in the automation Chrome; drive Manage Account → Account
   API Tokens → Edit on `Access`, `Access: Identity Providers`, `Access: Organizations`,
   `Access: Service Tokens`; DOM-extract → `vault set --stdin <scope> cf.api_token`.
   Account-token gotcha: verify with `/accounts/{id}/tokens/verify` (the `/user/…` endpoint
   always rejects account-owned tokens).
3. **GitHub OAuth app** (if the GitHub path is wanted) —
   `node scripts/gh-oauth-app.mjs --name <app> --callback https://<team>.cloudflareaccess.com/cdn-cgi/access/callback --expect-account <owner> --vault-scope <scope>`
   The `--expect-account` identity preflight is mandatory doctrine (wrong-owner incident,
   2026-07-23). Create the app right after a fresh login to ride the sudo grace window.
4. **Provision** — `node scripts/setup-access.mjs <spec.json>` — idempotent (GET-before-POST),
   safe to re-run after every spec edit; pre-existing orgs/idps/apps are adopted, not overwritten.
5. **Verify enforcement** — `curl -s -o /dev/null -w '%{http_code}' https://<host>/` → expect
   `302`; then a service-token request → expect `200`:
   `curl -H "CF-Access-Client-Id: $ID" -H "CF-Access-Client-Secret: $SECRET" …`

## Design rules (learned in production)

- **Session lengths are a safety feature**: field-device apps (a chairside recorder, a kiosk)
  get the 730h maximum so an in-field link NEVER re-auths mid-task; reading material gets days.
- **Allow-list every identity a person may arrive with** — GitHub asserts the account's verified
  email, OTP asserts the typed one; a person with two emails needs both listed.
- **Machine paths stay off the wall**: anything with its own end-to-end auth (signed upload
  tokens, webhook receivers, machine-consumed feeds) must NOT sit behind Access — a browser
  login wall on a non-browser client is an outage. Wall the page, not the pipe.
- **Service workers + Access**: a PWA behind Access must never cache redirected/non-OK responses
  (`res.redirected || !res.ok` → don't cache) or the login page poisons the app shell. Bump the
  SW cache name when adding the wall (purges anything cached pre-guard).
- **CLI/CI clients** get a service token + `non_identity` policy; send
  `CF-Access-Client-Id/Secret` headers IN ADDITION to any app-level auth.
- **Public-by-design sites** (career portals, feeds) are explicitly out of spec — list what you
  deliberately did NOT wall in the project's decision record.

## Reference implementations

- A private client repo's `scripts/access-bootstrap/` + that repo's compliance README §D10
  (2026-07-23: client CF org, two workers.dev apps, OTP+GitHub, a CLI service token).
- eonfleet (`eon.ccmax.uk`, April 2026): GitHub-SSO-only variant on a custom domain
  (ccmax-monitor repo: `production/cloudflare_access_jwt_verifier.py` for server-side JWT
  verification when the origin must double-check).

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did Cloudflare API calls succeed?** — If not, verify the scope-token has Access permissions and the account ID is correct.
2. **Is authentication enforced on the deployed URLs?** — Unauthenticated requests must 302 to the login page; service-token requests must succeed.
3. **Did the spec match the actual deployment?** — If Cloudflare's API/dashboard drifted, update the reference scripts and this skill's documentation.
