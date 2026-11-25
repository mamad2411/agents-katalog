---
name: vibe-service-audit
description: Audit a vibe-coded backend service, webhook handler, ingestion job, or integration and produce a severity-tagged markdown report. Use when the user wants to security-review a non-user-facing service — "audit my Stripe webhook," "review my ingestion job," "is my integration secure," "audit this Lambda." Covers webhook signature verification (HMAC/JWS, Stripe/GitHub/Shopify/Twilio), API key and OAuth token handling, outbound-call TLS, data egress, idempotency / replay protection, and job-trigger auth, on top of the shared baseline. Runs safe live probes against a webhook or API base URL (unsigned/tampered/replayed/malformed) and asks before intrusive probes.
allowed-tools: Read Grep Glob
---

# Vibe-coded backend service security audit

This skill audits a backend service / integration / webhook handler — the kind of repo people
vibe-code when they want to glue Stripe to their database, run a daily ingestion job, or stand up
a webhook receiver. No UI, no browser threat model. The dominant failure modes are different
from a webapp: missing or wrong signature verification, replay attacks, secret handling in
outbound calls, and error messages that leak internals.

## When to use this skill

Use this when the user wants to security-review a service with no user-facing UI. Examples:

- Stripe / Shopify / GitHub webhook receivers.
- Data ingestion jobs (cron, scheduled GitHub Actions, Vercel cron, Lambda).
- API-to-API glue (Salesforce → Postgres, HubSpot → Segment, etc.).
- Internal APIs called by other services, not by browsers.

Don't use this for: user-facing web apps (use `vibe-webapp-audit`), chat bots that handle
platform events (use `vibe-bot-audit`), manual scripts (use `vibe-script-audit`), or MCP servers
/ AI agents (use `vibe-mcp-agent-audit`).

## Inputs the skill expects

- A path to a local repo (the working directory by default).
- Optionally, a **webhook URL or API base URL** — required for live probes (signature checks,
  replay rejection, malformed payloads).
- Optionally, sample valid request signatures or shared secrets, if the user wants the live
  tests to also exercise the _signed_ path.

Ask the user for the runtime target at the start. If they don't provide one, skip live tests
and note this in the report.

## Workflow

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${SKILL_DIR}}"
SHARED_DIR="$SKILL_DIR/../../shared"
# Always reads:
#   $SHARED_DIR/references/baseline.md
#   $SHARED_DIR/references/live-tests-baseline.md
#   $SHARED_DIR/references/report-template.md
# Conditionally:
#   $SKILL_DIR/references/webhook-verification.md  (if any webhook endpoint found)
#   $SKILL_DIR/references/live-tests.md            (if a live target is provided)
```

1. **Detect the stack and runtime shape** (~30s — see below).
2. **Ask for the live target** (webhook URL, API base URL). Record what the user gave you.
3. **Run the baseline** (`$SHARED_DIR/references/baseline.md`, checks A–D).
4. **Run the category-specific static checks** (sections 1–6 below).
5. **Run live tests** if a target was provided. Read `$SHARED_DIR/references/live-tests-baseline.md`
   then `$SKILL_DIR/references/live-tests.md`.
6. **Render the report** using `$SHARED_DIR/references/report-template.md`.

### Detect the runtime shape

```bash
ls package.json pyproject.toml requirements.txt Gemfile go.mod 2>/dev/null
[ -f package.json ] && head -50 package.json

# Server frameworks
grep -hE "(express|fastify|hono|koa|next|fastapi|flask|django|sanic)" \
  package.json pyproject.toml requirements.txt 2>/dev/null

# Webhook endpoints
find . -path ./node_modules -prune -o \
  \( -path "*/webhooks/*" -o -path "*/webhook/*" -o -name "*webhook*" \) \
  -print | head -20

# Scheduled jobs
ls .github/workflows vercel.json fly.toml render.yaml 2>/dev/null
grep -lE "schedule:|crons|cron:" .github/workflows/*.yml vercel.json 2>/dev/null

# Outbound HTTP clients
grep -hE "(axios|got|node-fetch|undici|requests|httpx|aiohttp)" \
  package.json pyproject.toml requirements.txt 2>/dev/null
```

## 1 — Webhook signature verification

For every webhook endpoint, the handler MUST verify a signature header before reading the body.

- **At least one webhook endpoint found** → **MANDATORY: read
  `$SKILL_DIR/references/webhook-verification.md` in full before flagging anything in this
  section.** Covers HMAC, JWS, and platform-specific patterns (Stripe, GitHub, Shopify, Square,
  Twilio).
- **No webhook endpoint found** (pure ingestion / scheduled-job service) → Do NOT load
  `webhook-verification.md`. Skip this section and continue.

**Before flagging a webhook handler, ask yourself**: does the verification _gate_ the action,
or does it run alongside it? A handler that checks the signature but writes to the DB inside a
`try` that catches the verification error is unverified in practice. Walk the control flow from
request entry to first side effect.

The detailed failure-mode catalog (Bug 1–5: body parsed before verify, non-constant-time
comparison, try/catch-returns-200, replay accepted, wrong secret) lives in
`webhook-verification.md` Step 3, which you've already read per the MANDATORY load above.
Apply that catalog to each endpoint found.

## 2 — API key and OAuth token handling

**The failure mode**: a credential the service holds for a third-party API ends up readable
from an unexpected source — a committed config file, a log line, a world-readable token cache,
or an OAuth refresh that hands back a long-lived access token nobody rotates.

**Before flagging, ask yourself**: if this credential leaked, what's the blast radius? A Stripe
restricted key with one-resource scope is different from a Stripe live key with full account
access. Severity tracks scope, not just exposure.

**Patterns to flag**:

| Pattern                                                                  | Severity     |
| ------------------------------------------------------------------------ | ------------ |
| API key read from a non-env source (hardcoded, JSON-in-repo, unauth URL) | **Critical** |
| Tokens written to a world-readable file (mode 0644 or wider)             | **High**     |
| Tokens logged on success or failure handlers                             | **High**     |
| OAuth refresh tokens stored alongside access tokens with no rotation     | **Medium**   |
| OAuth scopes broader than the service needs                              | **Medium**   |

**Find the surface**:

```bash
grep -rE "process\.env\.|os\.environ\." --include="*.{ts,js,py}" . | head -30
grep -rE "(writeFile|fs\.write|open\(.*['\"]w)" --include="*.{ts,js,py}" . | grep -iE "token|key|secret" | head -10
grep -rE "refresh_token|refreshToken" --include="*.{ts,js,py}" . | head -10
```

## 3 — Outbound calls

**Before flagging an outbound call, ask yourself**: is the _credential_ being sent over a
verified channel? TLS verification disabled means the bearer token, basic-auth header, or API
key in the request is readable by any network attacker on the path. The severity isn't "TLS is
broken" — it's "the secret you're sending is now public to anyone in the middle."

**Patterns to flag:**

| Pattern                                                                 | Severity                                                                       |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| TLS verification disabled (`verify=False`, `rejectUnauthorized: false`) | **Critical** in production code paths; **Low** in clearly-marked test fixtures |
| Cleartext HTTP for any third-party API that carries auth headers        | **High**                                                                       |
| Error message from outbound call echoed verbatim to client / logs       | **High** — these often contain the request including the API key               |

**Find the surface:**

```bash
grep -rE "(rejectUnauthorized: false|verify=False|ssl=False|InsecureSkipVerify)" \
  --include="*.{ts,js,py,go}" . | head -10

grep -rE "http://(?!localhost|127\.)" --include="*.{ts,js,py,env*}" . | head -10
```

## 4 — Data egress

**Before flagging a data-egress finding, ask yourself**: where does this data _actually_ end
up? `logger.info(req.body)` and `analytics.track(payload)` are both "egress" but with different
consumers and retention. A request body in a server log retained 30 days is **High**; the same
data in a customer-facing email is **Critical**.

**Patterns to flag:**

| Pattern                                                                | Severity   |
| ---------------------------------------------------------------------- | ---------- |
| Raw request body or response logged in production                      | **High**   |
| PII forwarded to a third-party (analytics, errors, AI) without DPA ref | **Medium** |
| Secrets/tokens accidentally included in error captures (Sentry et al.) | **High**   |

**Find the surface:**

```bash
grep -rE "(console\.log|logger\.(info|debug)|print\().*\b(body|payload|data|request|response)\b" \
  --include="*.{ts,js,py}" . | head -20
grep -rE "(email|phone|ssn|password|token|api_key)" --include="*.{ts,js,py}" . | head -20
```

## 5 — Idempotency and replay safety

**Before flagging an idempotency gap, ask yourself**: is this handler _naturally_ idempotent
(e.g., upserts a key with a deterministic value) or does it produce duplicates on every retry
(e.g., appends a row, sends an email, charges a card)? Platforms retry deliveries; without
idempotency, a single user event can become 5 charges, 5 emails, 5 rows. Severity tracks the
visible-to-users impact of duplication.

Webhook receivers and event handlers must be safe to receive the same event twice.

- Look for an idempotency-key lookup before performing the action.
- Look for a check on a unique event/delivery ID (Stripe `event.id`, GitHub `X-GitHub-Delivery`).
- Flag handlers that perform side effects (charge a card, send an email) before recording the
  delivery ID.

**Severity:** Handler with side effects and no idempotency: **High**. Critical if the side
effect is a payment, an email to a user, or a row-write that can't be rolled back.

## 6 — Job and scheduled-trigger authentication

**Before flagging a cron handler, ask yourself**: how is the scheduler _talking_ to this code?
Vercel cron hits an HTTP endpoint on your deployment with an `Authorization` header from
`CRON_SECRET`. GitHub Actions invokes a workflow with its own auth. Lambda+EventBridge fires
events through IAM. The scheduler-to-handler edge is what needs auth; an unauthenticated HTTP
endpoint that just _happens_ to be the cron target is a backdoor anyone with the URL can
trigger.

For cron jobs / scheduled tasks (GitHub Actions, Vercel cron, Render cron, Lambda+EventBridge):

- If the scheduled endpoint is reachable from the public internet, it must check a shared secret
  or signed header from the scheduler.
- A scheduled route that's also a public POST endpoint with no auth is a backdoor: anyone can
  trigger the job.

Look for `CRON_SECRET`, `Authorization: Bearer <token>`, or platform-specific scheduler headers
in the handler. Missing: **High**.

## Producing the report

Read `$SHARED_DIR/references/report-template.md`. Save the report to the working directory as
`vibe-service-audit-<YYYY-MM-DD>-<HHMM>.md`. Tell the user the exact path.

## What this skill is NOT

- Not a replacement for SAST/DAST/SCA tooling. It catches the common vibe-coded-service failure
  modes.
- Not a pen test. The live tests probe specific known failure modes (signature, replay,
  malformed); they don't fuzz the application.
- Not a code review. Code quality, performance, and architecture issues are out of scope.
