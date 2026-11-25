---
name: vibe-webapp-audit
description: Audit a vibe-coded user-facing web app (Lovable, v0, Bolt, Replit, Cursor) and produce a severity-tagged markdown report. Use when the user wants to security-review a generated web app with a UI and backend — "audit my Lovable app," "is my Bolt export safe," "review my Supabase setup," "find the security issues in this Next.js project." Covers Supabase RLS and plain-Postgres access controls, server-side input validation vs browser-only, IDOR on REST routes, and security headers, on top of the shared baseline (gitleaks, SAST, deps, monitoring). Runs safe live probes against a deployed URL (anonymous reads, header probes, error-page leakage) and asks before intrusive probes.
allowed-tools: Read Grep Glob
---

# Vibe-coded web app security audit

This skill audits a user-facing web app — the kind of repo Lovable, Bolt, v0, Replit, or Cursor
ships — and produces a markdown report with severity-tagged findings.

The skill is built around a specific failure mode: AI coding tools ship code that _looks_ secure
but isn't. Validation is in the browser only. RLS is "enabled" but has no policies. The service
role key is in `NEXT_PUBLIC_*`. Authorization checks ask "is the user logged in" instead of "does
this user own this row." This skill catches those.

## When to use this skill

Use this when the user wants to security-review a user-facing web app: a repo with a frontend
(React/Next/Vite/Svelte/etc.), a backend (route handlers, API endpoints, server actions), and a
database. Phrases like "audit my Lovable app," "is my Bolt export safe," "review my Supabase
setup," "find the security issues in this Next.js project," or "is this safe to ship" all qualify.

Don't use this for: backend integrations / webhook handlers (use `vibe-service-audit`),
Slack/Discord/GitHub bots (use `vibe-bot-audit`), manual scripts (use `vibe-script-audit`), or
MCP servers / AI agents (use `vibe-mcp-agent-audit`).

## Inputs the skill expects

- A path to a local repo (the working directory by default).
- Optionally, a **deployed URL** — required for live probes (headers, anonymous-access checks,
  error-page introspection, IDOR enumeration).
- Optionally, the database backend (Supabase, Postgres + app code, or unknown — the skill
  detects).

Ask the user for the deployed URL at the start. If they don't provide one, skip the live tests
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
#   $SKILL_DIR/references/supabase.md     (if Supabase detected)
#   $SKILL_DIR/references/postgres.md     (if Postgres + app framework)
#   $SKILL_DIR/references/live-tests.md   (if a deployed URL is provided)
```

1. **Detect the stack** (~30s — see below).
2. **Ask for the deployed URL.** Record what the user gave you.
3. **Run the baseline.** Read `$SHARED_DIR/references/baseline.md` and run checks A–D (secrets,
   SAST, deps, monitoring).
4. **Run the category-specific static checks** (sections 1–4 below).
5. **Run live tests** (if a deployed URL was provided). Read
   `$SHARED_DIR/references/live-tests-baseline.md` for the protocol and
   `$SKILL_DIR/references/live-tests.md` for the webapp-specific probes.
6. **Render the report** using `$SHARED_DIR/references/report-template.md`.

For each finding, capture: severity (Critical / High / Medium / Low / Info), file path + line
number where applicable, a one-sentence description, and a one-sentence fix.

### Detect the stack first

```bash
# What kind of project? (some manifests are expected to be absent)
ls package.json pyproject.toml requirements.txt Gemfile go.mod 2>/dev/null

# What's in package.json (if present)?
[ -f package.json ] && head -50 package.json

# Supabase?
grep -rl "supabase" --include="*.{ts,tsx,js,jsx,py}" . | head -5

# Postgres directly?
grep -rlE "pg|psycopg|sequelize|prisma|knex|drizzle" --include="*.{ts,js,py}" . | head -5

# Framework?
grep -hE "next|vite|express|fastapi|django|flask|rails" \
  package.json pyproject.toml Gemfile 2>/dev/null
```

If Supabase is in the stack, you'll need `references/supabase.md` for sections 1 and 3 below. If
it's plain Postgres + an app framework, you'll need `references/postgres.md`. If both are present
(rare but possible), read both. If neither, record sections 1 and 3 as "skipped: no recognized
database backend detected" and move on.

## 1 — Database access controls

Backend-specific. **MANDATORY** — based on what was detected:

- **Supabase detected** → **MANDATORY: read `$SKILL_DIR/references/supabase.md` in full before
  proceeding.** Do NOT load `postgres.md` for this path.
- **Plain Postgres + app framework** → **MANDATORY: read `$SKILL_DIR/references/postgres.md` in
  full before proceeding.** Do NOT load `supabase.md` for this path.
- **Both detected** (rare) → read both, in the order above.
- **Neither** → record "skipped: no recognized database backend" and move on. Do NOT load
  either reference.

Don't try to do this check from memory — the per-backend procedures are specific and the
reference files exist for a reason.

## 2 — Server-side input validation

**The failure mode**: forms validate in the browser, but the API endpoint accepts whatever the
client sends. The browser is attacker-controlled — its validation is UX, not security.

**Before flagging, ask yourself**: is the boundary between "user input" and "trusted data"
crossed _before_ a validator runs? If yes, anything downstream is on shaky ground regardless of
how clean the code looks.

**Patterns to flag** (in priority order):

| Pattern                                                                 | Severity                                                                       |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Type assertions (`as MyType`) standing in for runtime validation        | **High** — false sense of security is worse than none; types vanish at runtime |
| `req.body.x` used directly in a DB query or response with no `.parse()` | **High** if it writes / returns user data, **Medium** if read-only             |
| Validation present only in the React form component, not in the route   | **High** — bypassed by any non-browser client                                  |
| File upload endpoint with no size / type / content check                | **High** — DoS + RCE surface depending on processor                            |
| Numeric input without bounds, string without length cap                 | **Medium** — DoS / overflow vector                                             |

**Find the surface** (grep is illustration, not the check):

```bash
find . -path ./node_modules -prune -o \
  \( -path "*/api/*" -o -path "*/routes/*" -o -name "route.ts" -o -name "route.js" \) \
  -print | head -30

grep -hE '"(zod|yup|joi|valibot|class-validator|pydantic|marshmallow)"' \
  package.json pyproject.toml requirements.txt 2>/dev/null
```

For each handler found, open it and walk the data path from `req.body` / `request.json()` to
its first use. Apply the table above.

## 3 — Authorization (IDOR)

Like section 1, this depends on the backend.

- Supabase with RLS doing the work → covered in `references/supabase.md`.
- App-layer authorization (Express middleware, Django permissions, etc.) → covered in
  `references/postgres.md`.

Read the relevant reference and follow it. The headline failure mode is the same across
backends: the code checks "is the user authenticated" but not "does this user own the row they're
asking about." IDOR (insecure direct object reference) is the canonical AI-coded-app bug.

**Before flagging an IDOR, ask yourself**: where does the resource owner identity come from?
The authenticated session (good) or the request (bad)? If `userId` comes from `req.body` /
query string / a JWT claim the client controls, the check is theatrical. If it comes from a
session lookup the server alone controls, it's real.

**Severity guide** (apply regardless of backend; the references show the patterns):

| Pattern                                                                                           | Severity                                                                             |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Write endpoint (POST/PUT/PATCH/DELETE) accepts a resource ID and skips ownership check            | **Critical**                                                                         |
| Read endpoint returns user-owned resource by ID with no ownership filter (IDOR)                   | **Critical** if data is sensitive (orders, messages, files, PII); **High** otherwise |
| `userId` / `user_id` taken from request body or query string instead of the authenticated session | **Critical**                                                                         |
| Admin/role-gated endpoint with only `requireAuth` (no role check)                                 | **Critical**                                                                         |
| RLS policy `USING (true)` or missing `WITH CHECK` on writes                                       | **Critical**                                                                         |
| Service-role / admin DB client used in a code path without an explicit ownership check            | **High–Critical** by data sensitivity                                                |
| Authorization enforced inconsistently across endpoints (some have it, some don't)                 | **High**                                                                             |
| Authorization correct but only enforced in middleware that can be bypassed by a sibling route     | **High**                                                                             |
| Read endpoint exposes non-sensitive shared data with no ownership check (e.g., public catalog)    | **Low / Info**                                                                       |

## 4 — Security headers (static config)

**Before flagging missing headers, ask yourself**: does the framework set safe defaults, or does
the app need to opt in? Next.js, Express + helmet, and most modern frameworks ship sane
defaults; the finding is when the developer has _overridden_ them (a custom `headers()` function
that drops CSP, a `helmet({ contentSecurityPolicy: false })` call). Missing-config-on-default-
safe-framework is **Info**; explicit-override-removing-protection is **High**.

The live header probe is in `references/live-tests.md` and is more authoritative than the
static config — frameworks can be overridden by proxies and CDNs. This static check exists for
the no-deployed-URL case.

**Where header config lives:**

```bash
# Next.js
grep -A20 "headers" next.config.js next.config.mjs next.config.ts 2>/dev/null
# Vercel / Netlify (override framework defaults)
cat vercel.json netlify.toml 2>/dev/null
# Express helmet
grep -r "helmet" --include="*.{ts,js}" . | head -5
```

If there's no header config in the repo and no deployed URL to probe, record this as
"Headers: cannot verify without deployed URL — no header configuration found in repo, which
suggests defaults are in use." Severity: **Info**.

## Producing the report

Read `$SHARED_DIR/references/report-template.md` for the exact format, then render findings into
it. Save the report to the working directory as `vibe-webapp-audit-<YYYY-MM-DD>-<HHMM>.md` —
always include the time. Tell the user the exact path. Don't file Linear issues, send Slack
messages, or do anything else with the findings unless the user explicitly asks.

## What this skill is NOT

- Not a replacement for a real SAST/DAST/SCA platform. It's an audit pass that catches the
  common vibe-coding failure modes.
- Not a pen test. The live tests probe specific known failure modes; they don't fuzz the
  application.
- Not a compliance audit. It doesn't map to SOC 2, ISO 27001, or any framework.
- Not a code review. It's a security pass — code quality, performance, and architecture issues
  are out of scope.

If the user wants any of the above, say so and stop.
